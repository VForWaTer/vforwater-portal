from django.urls import path
# from author_manage import views
from django.urls.conf import re_path
from author_manage.admin import resource_manager
from author_manage.admin import user_manager
from author_manage.views import *

# for security reasons all urls are accessible only for logged in users

app_name = 'author_manage'  # jm

urlpatterns = [

    # entry point to the web site, home page
    path('', HomeView.as_view(), name='home'),

    # pages, accessible only for the admin - for managing resources/users
    re_path(r'^resource-manager/', resource_manager.urls),
    re_path(r'^user-manager/', user_manager.urls),

    # profile page, where the user can change his name/see his current access requests
    # the admin can additionally see his current deletion requests
    re_path(r'^profile/$', ProfileView.as_view(), name='profile'),

    # subpage of the profile page, where the user can see all the resources that he owns
    re_path(r'^profile/my-resources/$', MyResourcesView.as_view(), name='my-resources'),

    # for every resource that a user owns, he has the option to edit its permissions
    # initially only the users that have ANY permissions about this resource are displayed
    re_path(r'^profile/my-resources/(?P<resourceid>\d+)-edit-users-permissions/$', PermissionEditingView.as_view(),
            name='edit permissions'),

    # the user has also the option to search for a user, who does not have any permission about
    # this resource to this point, and grant him such
    re_path(r'^profile/my-resources/(?P<resourceid>\d+)-edit-users-permissions/search$',
            PermissionEditingViewSearch.as_view(), name='edit permissions searching for user'),

    # subpage for adding a new resource
    re_path(r'^profile/my-resources/add-new-resource/$', AddNewResourceView.as_view(), name='add-new-resource'),

    # subpage for editing first and/or last name; can not be null
    re_path(r'^profile/edit-name/$', EditNameView.as_view(), name='edit-name'),

    # page for displaying all resources in the portal
    # the user sees 'access' button only if he is privileged to access the resource
    # otherwise he has the option to send an access request
    re_path(r'^resources-overview/$', ResourcesOverview.as_view(), name='resources-overview'),

    # search function in case the resources in the portal are too many
    re_path(r'^resources-overview/search$', ResourcesOverviewSearch.as_view(), name='search-resources'),

    # url for accessing a resource (download function)
    re_path(r'^resources/(?P<resourceid>\d+)$', OpenResourceView.as_view(), name='open resources'),

    # urls for sending/canceling an access request
    re_path(r'^send-access-request/(?P<resourceid>\d+)$', SendAccessRequestView.as_view(), name='send-access-request'),
    re_path(r'^cancel-access-request/(?P<resourceid>\d+)$', CancelAccessRequest.as_view(),
            name='cancel-access-request'),

    # urls for approving/denying an access request; accessible only if requestid
    # is valid and the current user has rights too handle the request
    re_path(r'^approve-access-request/(?P<requestid>\d+)$', ApproveAccessRequest.as_view(),
            name='approve-access-request'),
    re_path(r'^deny-access-request/(?P<requestid>\d+)$', DenyAccessRequest.as_view(), name='deny-access-request'),

    # urls for sending/canceling a deletion request
    re_path(r'^send-deletion-request/(?P<resourceid>\d+)$', SendDeletionRequestView.as_view(),
            name='send-delete-request'),
    re_path(r'^cancel-deletion-request/(?P<resourceid>\d+)$', CancelDeletionRequestView.as_view(),
            name='cancel-delete-request'),

    # urls for approving/denying a deletion request; accessible only if requestid
    # is valid and the current user has rights too handle the request
    re_path(r'^approve-deletion-request/(?P<requestid>\d+)*$', ApproveDeletionRequest.as_view(),
            name='approve deletion request'),
    re_path(r'^deny-deletion-request/(?P<requestid>\d+)$', DenyDeletionRequest.as_view(),
            name='deny deletion request'),

    # url for deleting a resource, accessible only for the admin
    re_path(r'^delete-resource/(?P<resourceid>\d+)*$', DeleteResourceView.as_view(), name='delete resource'),

]
