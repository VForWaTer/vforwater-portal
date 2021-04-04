import logging

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect  #, _get_queryset  # , render_to_response
from django.template.loader import render_to_string
from django.views import generic
from django.contrib.auth.decorators import login_required
from author_manage.models import *
from django.core.files import File
from django.conf import settings
import os
from django.utils.decorators import method_decorator

from vfwheron.models import Details
from .filters import PersonsFilter, DetailsFilter
from .forms import AddNewResourceForm
from django.template.context_processors import csrf
from . import utilities
from django.http import Http404
from django.core.mail.message import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.core.exceptions import PermissionDenied, ValidationError
from _csv import reader, Error
import mimetypes
# from test.support import resource
from django.db.models import Q
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404
from django.contrib import messages

from itertools import chain
from author_manage.models import Resource
from author_manage.apps import authorManageConfig

logger = logging.getLogger(__name__)


@receiver(user_logged_in)  # function to collect user data - especially resources - on login
def get_user_embargo_resources(request, user, **kwargs):
    maintainer_set = Resource.objects.filter(maintainers=user, dataEntry__embargo=True)
    reader_set = Resource.objects.filter(readers=user, dataEntry__embargo=True)
    owner_set = Resource.objects.filter(owners=user, dataEntry__embargo=True)
    datasets = reader_set | maintainer_set | owner_set
    request.session['datasets'] = list(datasets.values_list('dataEntry_id', flat=True))


# TODO: document
@method_decorator(login_required, name='dispatch')
class HomeView(generic.View):
    """

    """
    model = User
    def get(self, request):
        """

        @param request:
        @type request:
        @return:
        @rtype:
        """
        is_admin = request.user.is_staff
        return render(request, 'author_manage/home.html', {'is_admin': is_admin})


# @method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class ProfileView(generic.ListView):
    """

    """
    model = AccessRequest.objects.none()
    template_name = 'author_manage/profile.html'
    context_object_name = 'requests_list'
    paginate_by = 4

    def get(self, request):
        """

        @param request:
        @type request:
        @return:
        @rtype:
        """
        current_user = self.request.user
        resources = MyResourcesView.get_queryset(self)

        # load access requests if user owns any resources
        if resources.exists():
            self.model = AccessRequest.objects.filter(resource__in=resources)

        # load all deletion request if user is staff
        if self.model.exists():
            if current_user.is_staff and DeletionRequest.objects.all().exists():
                self.model = get_sorted_requests(self.model, DeletionRequest.objects.all().order_by('-creationDate'))
                # self.model = list(chain(self.model,DeletionRequest.objects.all()))
        else:
            if current_user.is_staff and DeletionRequest.objects.all().exists():
                self.model = DeletionRequest.objects.all().order_by('-creationDate')

        return super(ProfileView, self).get(request)

    def get_queryset(self):
        """

        @return:
        @rtype:
        """
        return self.model

    def get_context_data(self, **kwargs):
        """

        @param kwargs:
        @type kwargs:
        @return:
        @rtype:
        """
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['is_admin'] = self.request.user.is_staff
        return context


# the view for showing all the user's resources
@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class MyResourcesView(generic.ListView):
    """

    """
    model = Resource
    template_name = 'author_manage/my-resources.html'
    deletion_requested = Resource.objects.none()

    def get_queryset(self):
        """

        @return:
        @rtype:
        """
        owner_set = Resource.objects.filter(owners=self.request.user)
        maintainer_set = Resource.objects.filter(maintainers=self.request.user)
        reader_set = Resource.objects.filter(readers=self.request.user)
        deletion_set = Resource.objects.filter(deletionrequest__sender=self.request.user)
        access_set = Resource.objects.filter(accessrequest__sender=self.request.user)
        # What about:
        # users = User.objects.all().select_related('profile')
        current_user = owner_set | maintainer_set | reader_set | deletion_set | access_set
        return current_user.all()

    # returns a dictionary representing the template context.
    def get_context_data(self, **kwargs):
        """

        @param kwargs:
        @type kwargs:
        @return:
        @rtype:
        """
        context = super(MyResourcesView, self).get_context_data(**kwargs)
        context['deletion_requested'] = Resource.objects.filter(
            id__in=DeletionRequest.objects.filter(sender=self.request.user).values('resource_id'))
        context['is_admin'] = self.request.user.is_staff
        return context


# the view for sending a deletion request
@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class SendDeletionRequestView(generic.View):
    """

    """

    def post(self, request, *args, **kwargs):
        """

        @param request:
        @type request:
        @param args:
        @type args:
        @param kwargs:
        @type kwargs:
        @return:
        @rtype:
        """
        pk = self.kwargs['resourceid']  # get the id of the resource which is included in the url

        try:
            res = Resource.objects.get(id=pk)
        except Resource.DoesNotExist:
            # redirects the current user to profile/my-resources if a resource with such an id does not exist
            logger.info(
                "User %s tried to send a deletion request for non-existing resource \n" % request.user.username)
            raise Http404()

        # raises the PermissionDenied exception if the current user has no ownership for this resource
        if not res.owners.filter(id=request.user.id).exists():
            logger.info("User %s tried to send a deletion request for resource '%s' without being an owner! \n" %
                        (request.user.username, res.name))
            raise PermissionDenied
        # redirects the current user to profile/my-resources if the user is a staff user or the user has already
        # requested to delete the resource
        if request.user.is_staff or DeletionRequest.objects.filter(resource=res, sender=request.user).exists():
            logger.info("User %s tried to inconsistently send a deletion request for resource '%s' \n" %
                        (request.user.username, res.name))
            # return redirect("/profile/my-resources")
            return redirect('author_manage:my-resources')

        # creates a deletion request with the given description
        req = DeletionRequest.objects.create(sender=request.user,
                                             resource=Resource.objects.get(id=pk),
                                             description=request.POST['descr'])
        message = req.description

        # notifies all the staff users
        html_content = render_to_string('author_manage/mail/delete-resource-request-mail.html',
                                        {'user': request.user, 'resource': req.resource,
                                         'request': req, 'message': message})
        text_content = strip_tags(html_content)
        email_to = [x[0] for x in CustomUser.objects.filter(is_staff=True).values_list('email')]
        email_from = request.user.email
        msg = EmailMultiAlternatives('Request for deletion of a resource', text_content, email_from, email_to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        logger.info("Deletion request for '%s' resource was sent by %s \n" % (res.name, request.user.username))
        logger.info("An email was sent to the Staff members from %s, Subject: Deletion Request for '%s' \n" %
                    (request.user.username, res.name))
        # return redirect("/profile/my-resources")
        return redirect('author_manage:my-resources')


# the view for canceling a deletion request
@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class CancelDeletionRequestView(generic.View):
    """

    """

    def post(self, request, *args, **kwargs):
        """

        @param request:
        @type request:
        @param args:
        @type args:
        @param kwargs:
        @type kwargs:
        @return:
        @rtype:
        """
        pk = self.kwargs['resourceid']  # get the id of the resource which is included in the url

        try:
            res = Resource.objects.get(id=pk)
        except Resource.DoesNotExist:
            # redirects the current user to the 404 if a resource with such an id does not exist
            logger.info(
                "User %s tried to cancel a deletion request for non-existing resource \n" % request.user.username)
            raise Http404()

        # raises the PermissionDenied exception if the current user has no ownership for this resource
        if not res.owners.filter(id=request.user.id).exists():
            logger.info("User %s tried to cancel a deletion request for resource '%s' without being an owner! \n" %
                        (request.user.username, res.name))
            raise PermissionDenied

        # redirects the current user to /profile/my-resources if the user is a staff user
        if request.user.is_staff:
            logger.info(
                "User %s tried to cancel a deletion request for resource '%s' \n" % (request.user.username, res.name))
            return redirect('author_manage:my-resources')

        # requests_of_user = DeletionRequest.objects.filter(sender=request.user)
        request_to_delete = get_object_or_404(DeletionRequest, sender=request.user, resource=res)

        # notifies all the staff users
        html_content = render_to_string('author_manage/mail/deletion-request-canceled-mail.html',
                                        {'user': request.user,
                                         'resource': request_to_delete.resource,
                                         'request': request_to_delete})
        text_content = strip_tags(html_content)
        email_to = [x[0] for x in CustomUser.objects.filter(is_staff=True).values_list('email')]
        email_from = request.user.email
        msg = EmailMultiAlternatives('Request for deletion of a resource canceled', text_content, email_from, email_to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        logger.info("Deletion request for '%s' was canceled by %s \n" %
                    (request_to_delete.resource.id, request.user.username))
        logger.info(
            "An email was sent to the Staff members from %s, Subject: Cancel the Deletion Request for '%s' \n" %
            (request.user.username, request_to_delete.resource.id))
        request_to_delete.delete()
        # return redirect("/profile/my-resources")
        return redirect('author_manage:my-resources')


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class ResourcesOverview(generic.ListView):
    """

    """
    model = Resource.objects.all()
    template_name = 'author_manage/resources-overview.html'
    context_object_name = "resources_list"
    paginate_by = 5

    query = ''
    can_access = Resource.objects.none()
    requested_resources = Resource.objects.none()

    def get_queryset(self):
        """

        @return:
        @rtype:
        """
        return self.model

    # returns a dictionary representing the template context.
    def get_context_data(self, **kwargs):
        """

        @param kwargs:
        @type kwargs:
        @return:
        @rtype:
        """
        context = super(ResourcesOverview, self).get_context_data(**kwargs)
        context['is_admin'] = self.request.user.is_staff
        context['query'] = self.query
        context['query_pagination_string'] = ''
        # list of resources for which the user has an access permission
        context['can_access'] = Resource.objects.filter(readers=self.request.user)
        # context['can_access'] = self.request.user.reader.filter(id__in=self.model)
        context['requested_resources'] = Resource.objects.filter(
            id__in=AccessRequest.objects.filter(sender=self.request.user).values('resource_id'))
        return context


# the view for ResourcesOverview after search
@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class ResourcesOverviewSearch(ResourcesOverview):
    """

    """

    # shows  all the resources that was sought or redirects the user if there is no or empty query
    def get(self, request):
        """

        @param request:
        @type request:
        @return:
        @rtype:
        """
        if 'q' in self.request.GET and self.request.GET['q']:
            self.query = self.request.GET['q']
            self.model = Resource.objects.filter(dataEntry__entries__title__icontains=self.query)
            self.can_access = self.request.user.reader.filter(id__in=self.model)
            current_user_has_requested = AccessRequest.objects.filter(sender=self.request.user).values('resource_id')
            self.requested_resources = Resource.objects.filter(id__in=current_user_has_requested)
            return super(ResourcesOverviewSearch, self).get(request)
        else:
            return redirect('author_manage:resources-overview')
            # "/resources-overview"

    # returns a dictionary representing the template context.
    def get_context_data(self, **kwargs):
        """

        @param kwargs:
        @type kwargs:
        @return:
        @rtype:
        """
        context = super(ResourcesOverviewSearch, self).get_context_data(**kwargs)
        context['is_admin'] = self.request.user.is_staff
        context['query'] = self.query;
        context['query_pagination_string'] = 'q=' + self.query + '&'
        context['can_access'] = self.can_access
        context['requested_resources'] = self.requested_resources
        return context


# the view for approving an access request
@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class ApproveAccessRequest(generic.View):
    """

    """

    def post(self, request, *args, **kwargs):
        """

        @param request:
        @type request:
        @param args:
        @type args:
        @param kwargs:
        @type kwargs:
        @return:
        @rtype:
        """
        pk = self.kwargs['requestid']  # gets the id of the request which is included in the url

        try:
            req = AccessRequest.objects.get(id=pk)
        except AccessRequest.DoesNotExist:
            # redirects the current user to the 404 if a request with a such id does not exist
            logger.info("User %s tried to approve a non-existing access request" % request.user)
            raise Http404()

        # raises the PermissionDenied exception if the current user has no ownership for this resource
        if not req.resource.owners.filter(id=request.user.id).exists():
            logger.info("User %s tried to approve an access request without being owner of the requested resource" %
                        request.user)
            raise PermissionDenied

        # adds the sender to the readers list of this resource
        req.resource.readers.add(req.sender)
        message = req.description

        # sends an email to sender of the request
        html_content = render_to_string('author_manage/mail/access-request-approved-mail.html',
                                        {'user': request.user, 'resource': req.resource,
                                         'request': req, 'message': message})
        text_content = strip_tags(html_content)
        email_to = req.sender.email
        email_from = request.user.email
        msg = EmailMultiAlternatives('Access Request approved', text_content, email_from, [email_to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        req.delete()
        logger.info("Request from %s to access '%s' was approved by %s \n" %
                    (req.sender, req.resource.id, request.user.username))
        logger.info("An email was sent from %s to %s, Subject: Access request for '%s' approved \n" %
                    (request.user.username, req.sender, req.resource.id))
        return redirect('author_manage:profile')


# the view for denying an access request
@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class DenyAccessRequest(generic.View):
    """

    """

    def post(self, request, *args, **kwargs):
        """

        @param request:
        @type request:
        @param args:
        @type args:
        @param kwargs:
        @type kwargs:
        @return:
        @rtype:
        """
        pk = self.kwargs['requestid']  # gets the id of the request which is included in the url

        try:
            req = AccessRequest.objects.get(id=pk)
        except AccessRequest.DoesNotExist:
            # redirects the current user to the 404 if a request with a such id does not exist
            logger.info("User %s tried to deny a non-existing access request" % (request.user))
            raise Http404()

        # raises the PermissionDenied exception if the current user has no ownership for this resource
        if not req.resource.owners.filter(id=request.user.id).exists():
            logger.info("User %s tried to deny an access request without being owner of the requested resource" %
                        request.user)
            raise PermissionDenied

        message = request.POST['descr']  # gets the description of the request

        # sends an email to sender of this request
        html_content = render_to_string('author_manage/mail/access-request-denied-mail.html',
                                        {'user': request.user, 'resource': req.resource,
                                         'request': req, 'message': message})
        text_content = strip_tags(html_content)
        email_to = req.sender.email
        email_from = request.user.email
        msg = EmailMultiAlternatives('Access Request denied', text_content, email_from, [email_to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        req.delete()
        logger.info("Request from %s to access '%s' was denied by %s \n" %
                    (req.sender, req.resource.id, request.user.username))
        logger.info("An email was sent from %s to %s, Subject: Access Request for '%s' denied \n" %
                    (request.user.username, req.sender, req.resource.id))
        return redirect('author_manage:profile')


# the view for sending an access request
@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class SendAccessRequestView(generic.View):
    """

    """

    def post(self, request, *args, **kwargs):
        """

        @param request:
        @type request:
        @param args:
        @type args:
        @param kwargs:
        @type kwargs:
        @return:
        @rtype:
        """
        pk = self.kwargs['resourceid']  # gets the id of the resource which is included in the url

        try:
            res = Resource.objects.get(id=pk)
        except Resource.DoesNotExist:
            # redirects the current user to the 404 if a resource with a such id does not exist
            logger.info(
                "User %s tried to send an access request for non-existing resource \n" % request.user.username)
            raise Http404()

        # redirects the current user to resources-overview if the user is a staff user or already has an access
        # permission to this resource
        # or if the user has already requested to access this resource
        if res.readers.filter(id=request.user.id).exists() or request.user.is_staff or \
            AccessRequest.objects.filter(resource=res, sender=request.user).exists():
            logger.info("User %s tried to inconsistently send an access request for resource '%s' \n" %
                        (request.user.username, res.name))
            return redirect('author_manage:resources-overview')

        # creates an access request with the given description
        req = AccessRequest.objects.create(sender=request.user, resource=res, description=request.POST['descr'])
        message = req.description

        # notifies all the owners via email
        html_content = render_to_string('author_manage/mail/access-resource-mail.html', {'user': request.user,
                                                                                         'resource': res,
                                                                                         'request': req,
                                                                                         'message': message})
        text_content = strip_tags(html_content)
        email_to = [x[0] for x in res.owners.values_list('email')]
        email_from = request.user.email
        msg = EmailMultiAlternatives('AccessPermission', text_content, email_from, email_to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        logger.info("Access request for resource '%s' with id '%s' was sent by %s \n" %
                    (res.name, pk, request.user.username))
        logger.info("An email was sent from %s to '%s' owners, Subject: Access Request for '%s' \n" %
                    (request.user.username, res.name, res.name))
        return redirect('author_manage:resources-overview')


# the view for canceling an access request
@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class CancelAccessRequest(generic.View):
    """

    """

    def post(self, request, *args, **kwargs):
        """

        @param request:
        @type request:
        @param args:
        @type args:
        @param kwargs:
        @type kwargs:
        @return:
        @rtype:
        """
        pk = self.kwargs['resourceid']  # gets the id of the resource which is included in the url

        try:
            res = Resource.objects.get(id=pk)
        except Resource.DoesNotExist:
            # redirects the current user to the 404 if a resource with a such id does not exist
            logger.info(
                "User %s tried to cancel an access request for non-existing resource \n" % request.user.username)
            raise Http404()

        # redirects the current user to the 404 if the user is a staff user or already has an access permission to
        # this resource
        if res.readers.filter(id=request.user.id).exists() or request.user.is_staff:
            logger.info("User %s tried to inconsistently cancel an access request for resource '%s' \n" % (
            request.user.username, res.name))
            raise Http404()

        # deletes the request
        # requests_of_user = AccessRequest.objects.filter(sender=request.user)
        request_to_delete = get_object_or_404(AccessRequest, sender=request.user, resource=res)
        request_to_delete.delete()

        # notifies all owners  via email
        html_content = render_to_string('author_manage/mail/access-request-canceled-mail.html',
                                        {'user': request.user, 'resource': request_to_delete.resource,
                                         'request': request_to_delete})
        text_content = strip_tags(html_content)
        email_to = [x[0] for x in request_to_delete.resource.owners.values_list('email')]
        email_from = request.user.email
        msg = EmailMultiAlternatives('Access Request canceled', text_content, email_from, email_to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        logger.info("Access request for '%s' was canceled by %s \n" %
                    (request_to_delete.resource.id, request.user.username))
        logger.info("An email was sent from %s to '%s' owners, Subject: Cancel the Access Request for '%s' \n" %
                    (request.user.username, request_to_delete.resource.id, request_to_delete.resource.id))
        return redirect('author_manage:resources-overview')


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class OpenResourceView(generic.View):
    """

    """

    def get(self, request, *args, **kwargs):
        """

        @param request:
        @type request:
        @param args:
        @type args:
        @param kwargs:
        @type kwargs:
        @return:
        @rtype:
        """
        pk = self.kwargs['resourceid']  # gets the id of the resource which is included in the url

        try:
            resource = Resource.objects.get(id=pk)
        except Resource.DoesNotExist:
            logger.info("User %s tried to access a non-existing resource \n" % request.user.username)
            raise Http404()

        # raises the PermissionDenied exception if the current user is a staff user or has no access permission to
        # this resource
        if (not resource.readers.filter(id=request.user.id).exists()) and (not request.user.is_staff):
            raise PermissionDenied

        logger.info("User %s accessed '%s' with id = %s \n" % (request.user.username, resource.type, resource.id))
        # Download function that tests the functionality.
        # It could be replaced with another view according to the specific resource
        return download(request, resource)


def download(request, resource):
    """

    @param request:
    @type request:
    @param resource:
    @type resource:
    @return:
    @rtype:
    """
    relative_path = request.path
    if relative_path.find(os.sep) == -1:
        relative_path = relative_path.replace(utilities.get_opposite_os_directory_sep(), os.sep)

    relative_path_elements = relative_path.split(os.sep, 1)
    relative_path = relative_path_elements[len(relative_path_elements) - 1]

    file_name = resource.link.name
    relative_path = relative_path.replace(str(resource.id), file_name)

    absolute_path = os.path.join(settings.BASE_DIR, relative_path)
    data = mimetypes.guess_type(absolute_path)

    f = open(absolute_path, 'rb')

    myfile = File(f)
    response = HttpResponse(myfile.read(), content_type=data[0])

    response['Content-Disposition'] = 'attachment; filename=' + file_name
    return response


@method_decorator(never_cache, name='dispatch')
class PermissionEditingView(generic.ListView):
    """

    """
    model = User = User.objects.none()
    template_name = 'author_manage/edit-permissions.html'
    resource = Resource.objects.all()
    query = ''
    context_object_name = "user_list"
    paginate_by = 10

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """

        @param request:
        @type request:
        @param args:
        @type args:
        @param kwargs:
        @type kwargs:
        @return:
        @rtype:
        """
        try:
            resource = Resource.objects.get(id=self.kwargs['resourceid'])
        except Resource.DoesNotExist:
            if request.method == "POST":
                logger.info(
                    "User %s tried to edit the permissions of a non-existing resource \n" % request.user.username)
            raise Http404()

        # checks if the current user has permission to access this resource
        if resource.owners.filter(id=request.user.id).exists():
            return super().dispatch(request, *args, **kwargs)

        logger.info("User %s tried to edit the permissions of resource %s \n" % (request.user.username, resource.id))
        raise PermissionDenied

    def post(self, request, *args, **kwargs):
        """

        @param request:
        @type request:
        @param args:
        @type args:
        @param kwargs:
        @type kwargs:
        @return:
        @rtype:
        """
        resource = Resource.objects.get(id=self.kwargs['resourceid'])
        new_readers_list = request.POST.getlist('reader[]')
        new_owners_list = request.POST.getlist('owner[]')
        users_on_page = request.POST.getlist('usersIdsOnPage[]')

        real_readers_list = list(resource.readers.values_list('id', flat=True))
        real_owners_list = list(resource.owners.values_list('id', flat=True))

        user_removed_own_right = False
        no_rights_users = 0

        for userId in users_on_page:
            user = CustomUser.objects.get(id=userId)
            # checks if a user granted the access permission for this resource
            if userId in new_readers_list and int(userId) not in real_readers_list:

                resource.readers.add(user)
                AccessRequest.objects.filter(sender=user, resource=resource).delete()

                html_content = render_to_string('author_manage/mail/access-granted-mail.html',
                                                {'user': request.user, 'resource': resource})
                text_content = strip_tags(html_content)
                email_to = [user.email]
                email_from = request.user.email
                msg = EmailMultiAlternatives('Access Permission granted', text_content, email_from, email_to)
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                logger.info("Access permission for '%s' was granted by %s \n" % (resource.id, request.user.username))
                logger.info("An email was sent from %s to '%s' , Subject: Access permission granted \n" %
                            (request.user.username, user.username))

                # checks if the access permission  was removed from a user
            elif userId not in new_readers_list and int(userId) in real_readers_list and userId not in new_owners_list:

                no_rights_users += 1
                resource.readers.remove(user)

                html_content = render_to_string('author_manage/mail/access-removed-mail.html',
                                                {'user': request.user, 'resource': resource})
                text_content = strip_tags(html_content)
                email_to = [user.email]
                email_from = request.user.email
                msg = EmailMultiAlternatives('Access Permission removed', text_content, email_from, email_to)
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                logger.info("Access permission for '%s' was removed by %s from %s \n" %
                            (resource.id, request.user.username, user.username))
                logger.info("An email was sent from %s to '%s' , Subject: Access permission removed \n" %
                            (request.user.username, user.username))

            owner = Owner.objects.get(id=userId)

            # checks if a user granted the ownership of this resource
            if userId in new_owners_list and int(userId) not in real_owners_list:

                resource.owners.add(owner)
                if not resource.readers.filter(id=userId).exists():
                    resource.readers.add(user)
                    AccessRequest.objects.filter(sender=user, resource=resource).delete()

                html_content = render_to_string('author_manage/mail/ownership-granted-mail.html',
                                                {'user': request.user,
                                                 'resource': resource})
                text_content = strip_tags(html_content)
                email_to = [user.email]
                email_from = request.user.email
                msg = EmailMultiAlternatives('Ownership granted', text_content, email_from, email_to)
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                logger.info("ownership for '%s' was granted by %s \n" % (resource.id, request.user.username))
                logger.info("An email was sent from %s to '%s' , Subject: ownership granted \n" %
                            (request.user.username, user.username))

            # checks if the ownership of this resource was revoked from a user
            elif userId not in new_owners_list and int(userId) in real_owners_list and len(resource.owners.all()) > 1:

                resource.owners.remove(owner)
                DeletionRequest.objects.filter(sender=owner, resource=resource).delete()

                if int(userId) == self.request.user.id:
                    user_removed_own_right = True

                html_content = render_to_string('author_manage/mail/ownership-revoked-mail.html',
                                                {'user': request.user,
                                                 'resource': resource})
                text_content = strip_tags(html_content)
                email_to = [user.email]
                email_from = request.user.email
                msg = EmailMultiAlternatives('Ownership revoked', text_content, email_from, email_to)
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                logger.info("ownership for '%s' was revoked by %s from %s \n" %
                            (resource.id, request.user.username, user.username))
                logger.info("An email was sent from %s to '%s' , Subject: ownership revoked \n" %
                            (request.user.username, user.username))

        if user_removed_own_right:
            path_to_redirect = 'author_manage:my-resources'
        # All users on the page are removed and there is no search
        elif not ('q' in self.request.GET and self.request.GET['q']) and no_rights_users == len(users_on_page):
            path_to_redirect = 'author_manage:my-resources'
        else:
            path_to_redirect = utilities.get_relative_path_with_parameters(self.request)
        return redirect(path_to_redirect)

    def get_queryset(self):
        """

        @return:
        @rtype:
        """
        return self.model

    def get(self, request, *args, **kwargs):
        """

        @param request:
        @type request:
        @param args:
        @type args:
        @param kwargs:
        @type kwargs:
        @return:
        @rtype:
        """
        is_owner_of_resource = Resource.objects.get(id=self.kwargs['resourceid']).\
            owners.all().values_list('id', flat=True)
        is_reader_of_resource = Resource.objects.get(id=self.kwargs['resourceid']).\
            readers.all().values_list('id', flat=True)
        self.model = User.objects.filter(Q(id__in=is_owner_of_resource) | Q(id__in=is_reader_of_resource))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """

        @param kwargs:
        @type kwargs:
        @return:
        @rtype:
        """
        context = super(PermissionEditingView, self).get_context_data(**kwargs)
        context['resource'] = Resource.objects.get(id=self.kwargs['resourceid'])
        context['owners'] = Resource.objects.get(id=self.kwargs['resourceid']).owners.all()
        context['readers'] = Resource.objects.get(id=self.kwargs['resourceid']).readers.all()
        context['query'] = self.query
        context['query_pagination_string'] = ''
        context['is_admin'] = self.request.user.is_staff
        return context


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class PermissionEditingViewSearch(PermissionEditingView):
    """

    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """

        @param request:
        @type request:
        @param args:
        @type args:
        @param kwargs:
        @type kwargs:
        @return:
        @rtype:
        """
        # If there is no or empty query, the user is redirected to the main edit permission page
        if 'q' in self.request.GET and self.request.GET['q']:
            return super().dispatch(request, *args, **kwargs)
        else:
            path_to_redirect = utilities.get_one_level_lower_path(self.request.path)
            return redirect(path_to_redirect)

    def get(self, request, *args, **kwargs):
        """

        @param request:
        @type request:
        @param args:
        @type args:
        @param kwargs:
        @type kwargs:
        @return:
        @rtype:
        """
        self.query = self.request.GET['q']
        self.model = User.objects.filter(Q(username__icontains=self.query) | Q(first_name__icontains=self.query) |
                                         Q(last_name__icontains=self.query))
        return super(generic.ListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """

        @param kwargs:
        @type kwargs:
        @return:
        @rtype:
        """
        context = super(PermissionEditingViewSearch, self).get_context_data(**kwargs)
        context['resource'] = Resource.objects.get(id=self.kwargs['resourceid'])
        context['owners'] = Resource.objects.get(id=self.kwargs['resourceid']).owners.all()
        context['readers'] = Resource.objects.get(id=self.kwargs['resourceid']).readers.all()
        context['query'] = self.query
        context['query_pagination_string'] = 'q=' + self.query + '&'
        return context


# the view for deleting a resource
@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class DeleteResourceView(generic.View):
    """

    """
    def post(self, request, *args, **kwargs):
        """

        @param request:
        @type request:
        @param args:
        @type args:
        @param kwargs:
        @type kwargs:
        @return:
        @rtype:
        """
        pk = self.kwargs['resourceid']  # gets the id of the resource which is included in the url

        try:
            res = Resource.objects.get(id=pk)
        except Resource.DoesNotExist:
            # raises Http404 if a resource with a such id does not exist
            logger.info("User %s tried to delete a non-existing resource" % request.user)
            raise Http404()

        # raises the PermissionDenied exception if the current user is not a staff user
        if not request.user.is_staff:
            logger.info(
                "User %s tried to delete the resource '%s' without being an administrator" % (request.user, res.name))
            raise PermissionDenied

        html_content = render_to_string('author_manage/mail/resource-deleted-mail.html',
                                        {'user': request.user,
                                         'resource': res,
                                         'message': request.POST['descr']})
        text_content = strip_tags(html_content)

        # deletes all the requests for this resource
        AccessRequest.objects.filter(resource=res).delete()
        DeletionRequest.objects.filter(resource=res).delete()

        # notifies all the owners
        email_to = [x[0] for x in res.owners.values_list('email')]
        email_from = request.user.email
        msg = EmailMultiAlternatives('File deleted by admin', text_content, email_from, [email_to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        logger.info("User %s deleted resource %s " % (request.user.username, res.name))
        logger.info("An email was sent to all '%s' owners, Subject: '%s' is deleted " % (res.name, res.name))

        # deletes the resource
        res.delete()
        return redirect('author_manage:my-resources')


# the view for approving a deletion request
@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class ApproveDeletionRequest(generic.View):
    """

    """

    def post(self, request, *args, **kwargs):
        """

        @param request:
        @type request:
        @param args:
        @type args:
        @param kwargs:
        @type kwargs:
        @return:
        @rtype:
        """
        pk = self.kwargs['requestid']

        try:
            req = DeletionRequest.objects.get(id=pk)
        except DeletionRequest.DoesNotExist:
            # raises Http404 if a request with a such id does not exist
            logger.info("User %s tried to approve a non-existing deletion request" % request.user)
            raise Http404()

        # raises the PermissionDenied exception if the current user is a staff user
        if not request.user.is_staff:
            logger.info("User %s tried to approve a deletion request without being an administrator" % request.user)
            raise PermissionDenied

        message = req.description  # gets the description of the request

        html_content1 = render_to_string('author_manage/mail/delete-request-accepted-mail.html',
                                         {'user': request.user,
                                          'resource': req.resource,
                                          'message': message})
        text_content1 = strip_tags(html_content1)

        html_content2 = render_to_string('author_manage/mail/resource-deleted-mail.html',
                                         {'user': request.user,
                                          'resource': req.resource,
                                          'message': message})
        text_content2 = strip_tags(html_content2)

        res = req.resource

        # deletes all the requests for this resource
        AccessRequest.objects.filter(resource=res).delete()
        DeletionRequest.objects.filter(resource=res).delete()

        # sends an email to the sender of the request
        email_to = req.sender.email
        email_from = request.user.email
        msg = EmailMultiAlternatives('Deletion Request approved', text_content1, email_from, [email_to])
        msg.attach_alternative(html_content1, "text/html")
        msg.send()
        logger.info("An email was sent from %s to %s, Subject: Deletion Request for '%s' accepted \n" %
                    (request.user.username, req.sender, req.resource.id))

        # notifies all the owners
        email_to = [x[0] for x in res.owners.values_list('email')]
        email_from = request.user.email
        msg = EmailMultiAlternatives('Resource deleted', text_content2, email_from, [email_to])
        msg.attach_alternative(html_content2, "text/html")
        msg.send()
        logger.info(
            "An email was sent to all '%s' owners, Object: '%s' is deleted " % (req.resource.id, req.resource.id))

        # deletes the resource and the deletion request
        res.delete()
        req.delete()

        logger.info("Request from %s to delete '%s' accepted by %s \n" % (
        req.sender, req.resource.id, request.user.username))

        return redirect('author_manage:profile')


# the view for denying a deletion request
@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class DenyDeletionRequest(generic.View):
    """

    """

    def post(self, request, *args, **kwargs):
        """

        @param request:
        @type request:
        @param args:
        @type args:
        @param kwargs:
        @type kwargs:
        @return:
        @rtype:
        """
        pk = self.kwargs['requestid']

        try:
            req = DeletionRequest.objects.get(id=pk)
        except DeletionRequest.DoesNotExist:
            # raises Http404 if a request with a such id does not exist
            logger.info("User %s tried to deny a non-existing deletion request" % request.user)
            raise Http404()

        # raises the PermissionDenied exception if the current user is a staff user
        if not request.user.is_staff:
            logger.info("User %s tried to deny a deletion request without being an administrator" % request.user)
            raise PermissionDenied

        message = request.POST['descr']  # gets the description of this request

        # notifies the sender of this request via email
        html_content = render_to_string('author_manage/mail/delete-request-denied-mail.html',
                                        {'user': request.user,
                                         'resource': req.resource,
                                         'request': req,
                                         'message': message})
        text_content = strip_tags(html_content)
        email_to = req.sender.email
        email_from = request.user.email
        msg = EmailMultiAlternatives('Deletion Request denied', text_content, email_from, [email_to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        logger.info("Request from %s to delete '%s' was denied by %s \n" %
                    (req.sender, req.resource.id, request.user.username))
        logger.info("An email was sent from %s to %s, Subject: Deletion Request for '%s' denied\n" %
                    (request.user.username, req.sender, req.resource.id))

        # deletes the request
        req.delete()
        return redirect('author_manage:profile')


# the view for adding a new resource
@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class AddNewResourceView(generic.View):
    """

    """

    # adds a new resource with the given informations
    def post(self, request):
        """
        Store in resource table (and owner, reader...)

        @param request:
        @type request:
        @return:
        @rtype:
        """
        form = AddNewResourceForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            # instance.save()
            # instance.owners.add(request.user.id)
            # instance.readers.add(request.user.id)
            logger.info("User %s created the '%s' Resource \n" % (request.user.username, instance.link))

        else:
            logger.info("User %s tried to inconsistently create a resource \n" % request.user.username)
        return redirect('author_manage:my-resources')

    def get(self, request):
        form = AddNewResourceForm()

        args = {}
        args.update(csrf(request))

        args['form'] = form
        args['is_admin'] = self.request.user.is_staff
        args['user'] = self.request.user
        # return render_to_response('author_manage/add-new-resource.html', args) # not working in django > 3
        return render(None, 'author_manage/add-new-resource.html', args)


# the view for editing the name of the user
@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class EditNameView(generic.View):
    """
    updates the firstname and the lastname with the given firstname and lastname
    """

    def post(self, request):
        """

        @param request:
        @type request:
        @return:
        @rtype:
        """
        if request.POST['firstName'] and (not request.POST['firstName'].isspace()):
            request.user.first_name = request.POST['firstName']
            request.user.save()
        if request.POST['lastName'] and (not request.POST['lastName'].isspace()):
            request.user.last_name = request.POST['lastName']
            request.user.save()
        return redirect('author_manage:profile')


# returns a sorted list of combination of the access requests and the deletion requests
def get_sorted_requests(access_request_queryset, deletion_request_queryset):
    """

    @param access_request_queryset:
    @type access_request_queryset:
    @param deletion_request_queryset:
    @type deletion_request_queryset:
    @return:
    @rtype:
    """
    access_requests_list = list(access_request_queryset)
    deletion_requests_list = list(deletion_request_queryset)

    result = []
    longer_list_len = max(len(access_requests_list), len(deletion_requests_list))
    shorter_list_len = min(len(access_requests_list), len(deletion_requests_list))

    if longer_list_len == len(access_requests_list):
        longer_list = access_requests_list
        shorter_list = deletion_requests_list
    else:
        longer_list = deletion_requests_list
        shorter_list = access_requests_list

    for i in range(0, longer_list_len):
        result.append(longer_list[i])
        if i < shorter_list_len:
            result.append(shorter_list[i])

    return result


def upload_persons(request):
    """
    Options for upload form to define person and person roles

    :param request:
    :return:
    """
    print('persons upload request: ', request.GET)
    selection = NmPersonsEntries.objects.all().distinct('entry_id')
    myFilter = PersonsFilter(request.GET, queryset=selection)

    selection = myFilter.qs
    print('selection: ', selection)
    context = {'myFilter': myFilter, 'selection': selection}
    return render(request, 'author_manage/upload_persons.html', context)


def upload_details(request):
    """
    Options for upload form to define details

    :param request:
    :return:
    """
    print('details upload request: ', request.GET)
    selection = Details.objects.all().distinct('entry_id')
    myFilter = DetailsFilter(request.GET, queryset=selection)

    selection = myFilter.qs
    print('selection: ', selection)
    context = {'myFilter': myFilter, 'selection': selection}
    return render(request, 'author_manage/upload_details.html', context)
