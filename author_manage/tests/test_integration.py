from django.test import Client, TestCase
from author_manage.models import *


def setUpUsers():
    """

    @return:
    @rtype:
    """
    test_admin = User.objects.create(username='admin')
    test_admin.set_password('123456')
    test_admin.is_staff = True
    test_admin.is_admin = True
    test_admin.save()

    test_user = User.objects.create(username='user1', first_name='John', last_name='Smith')
    test_user.set_password('123456')
    test_user.save()

    test_user2 = User.objects.create(username='user2')
    test_user2.set_password('123456')
    test_user2.save()

    return {'test_admin': test_admin, 'test_user1': test_user, 'test_user2': test_user2}

def setUpResourceAndRequests(users):
    """

    @param users:
    @type users:
    @return:
    @rtype:
    """

    res1 = Resource.objects.create(name='res1', type='text', description='desc', link='res.txt')
    res1.readers.add(users['test_user1'].id)
    res1.owners.add(users['test_user1'].id)
    res1.readers.add(users['test_admin'].id)

    res2 = Resource.objects.create(name='resource2', type='text', description='description', link='res2.txt')
    res2.readers.add(users['test_user2'].id)
    res2.owners.add(users['test_user2'].id)
    res2.readers.add(users['test_user1'].id)
    res2.save()

    res3 = Resource.objects.create(name='resource3', type='text', description='description', link='res3.txt')
    res3.readers.add(users['test_admin'].id)
    res3.owners.add(users['test_admin'].id)
    res3.save()

    res4 = Resource.objects.create(name='resource4', type='text', description='description', link='res4.txt')
    res4.readers.add(users['test_user1'].id)
    res4.owners.add(users['test_user1'].id)
    res4.save()

    res5 = Resource.objects.create(name='resource5', type='text', description='description', link='res5.txt')
    res5.readers.add(users['test_user2'].id)
    res5.owners.add(users['test_user2'].id)
    res5.save()

    req1 = AccessRequest.objects.create(sender=users['test_user2'], resource=res1)
    req1.save()
    req2 = AccessRequest.objects.create(sender=users['test_user2'], resource=res4)
    req2.save()
    req3 = AccessRequest.objects.create(sender=users['test_user2'], resource=res3)
    req3.save()
    req4 = DeletionRequest.objects.create(sender=users['test_user2'], resource=res2)
    req4.save()
    req5 = DeletionRequest.objects.create(sender=users['test_user2'], resource=res5)
    req5.save()

def deleteUsers():
    """

    @return:
    @rtype:
    """
    User.objects.all().delete()

def deleteResourcesAndRequests():
    """

    @return:
    @rtype:
    """
    AccessRequest.objects.all().delete()
    DeletionRequest.objects.all().delete()
    Resource.objects.all().delete()


class TestUserData(TestCase):
    """

    """
    @classmethod
    def setUpClass(cls):
        """

        @return:
        @rtype:
        """
        super().setUpClass()
        users = setUpUsers()
        setUpResourceAndRequests(users)

    def setUp(self):
        """

        @return:
        @rtype:
        """
        self.client = Client()
        self.client.login(username='user1', password='123456')

    @classmethod
    def tearDownClass(cls):
        """

        @return:
        @rtype:
        """
        deleteUsers()
        deleteResourcesAndRequests()
        super().tearDownClass()

    def test_edit_name(self):
        """

        @return:
        @rtype:
        """
        self.client.post('/profile/edit-name/', {'firstName': 'bob', 'lastName': 'dylan'})
        self.assertEqual(User.objects.get_by_natural_key('user1').first_name, 'bob')

    def test_my_requests(self):
        """

        @return:
        @rtype:
        """
        response = self.client.get('/profile/')
        resources = Owner.objects.get_by_natural_key('user1').owner.all()
        requests = AccessRequest.objects.all().filter(resource__in=resources)
        self.assertCountEqual(response.context['requests_list'], requests)

    def test_my_resources(self):
        """

        @return:
        @rtype:
        """
        response = self.client.get('/profile/my-resources/')
        resources = Owner.objects.get_by_natural_key('user1').owner.all()
        self.assertCountEqual(response.context['resource_list'], resources)


class TestResourcesData(TestCase):
    """

    """

    @classmethod
    def setUpClass(cls):
        """

        @return:
        @rtype:
        """
        super().setUpClass()
        users = setUpUsers()
        setUpResourceAndRequests(users)

    def setUp(self):
        """"""

        self.client = Client()
        self.client.login(username='user1', password='123456')

    @classmethod
    def tearDownClass(cls):
        """

        @return:
        @rtype:
        """
        deleteUsers()
        deleteResourcesAndRequests()
        super().tearDownClass()

    def test_resources_overview(self):
        """

        @return:
        @rtype:
        """
        response = self.client.get('/resources-overview/')
        resources = Resource.objects.all()
        self.assertCountEqual(response.context['resources_list'], resources)

    def test_access_permissions(self):
        """

        @return:
        @rtype:
        """
        response = self.client.get('/resources-overview/')
        resources = CustomUser.objects.get_by_natural_key('user1').reader.all()
        self.assertCountEqual(response.context['can_access'], resources)

    def test_resource_permissions(self):
        """

        @return:
        @rtype:
        """
        response = self.client.get('/profile/my-resources/')
        resources = response.context['resource_list']
        for resource in resources:
            response = self.client.get('/profile/my-resources/' + str(resource.id) + '-edit-users-permissions/');
            owners = response.context['owners']
            readers = response.context['readers']

            self.assertCountEqual(readers, resource.readers.all())
            self.assertCountEqual(owners, resource.owners.all())


class TestRequestsData(TestCase):
    """

    """

    @classmethod
    def setUpClass(cls):
        """

        @return:
        @rtype:
        """
        super().setUpClass()
        users = setUpUsers()
        setUpResourceAndRequests(users)

    def setUp(self):
        """

        @return:
        @rtype:
        """
        self.client = Client()

    @classmethod
    def tearDownClass(cls):
        """

        @return:
        @rtype:
        """
        deleteUsers()
        deleteResourcesAndRequests()
        super().tearDownClass()

    def test_create_access_request(self):
        """"""

        self.client.login(username='user1', password='123456')
        self.client.get('/resources-overview/')
        resources = Resource.objects.all()
        resources_can_access = CustomUser.objects.get_by_natural_key('user1').reader.all()

        for resource in resources:
            if resource not in resources_can_access:
                self.client.post('/send-access-request/' + str(resource.id), {'descr': 'message'})
        requests = AccessRequest.objects.filter(sender=CustomUser.objects.get_by_natural_key('user1'))

        self.assertEqual(requests.count(), resources.count() - resources_can_access.count())

    def test_cancel_access_request(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='user2', password='123456')
        response = self.client.get('/resources-overview/')
        requested_resources = response.context['requested_resources']

        for resource in requested_resources:
            self.client.post('/cancel-access-request/' + str(resource.id), {'descr': 'message'})

        self.assertFalse(AccessRequest.objects.filter(sender=CustomUser.objects.get_by_natural_key('user1')).exists())

    def test_create_deletion_request(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='user1', password='123456')
        user = Owner.objects.get_by_natural_key('user1')
        response = self.client.get('/profile/my-resources/')
        resources = response.context['resource_list']

        for resource in resources:
            self.client.post('/send-deletion-request/' + str(resource.id), {'descr': 'message'})

        self.assertEqual(DeletionRequest.objects.filter(sender=user).count(), user.owner.all().count())

    def test_cancel_deletion_request(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='user2', password='123456')
        response = self.client.get('/profile/my-resources/')
        requested_resources = response.context['deletion_requested']

        for resource in requested_resources:
            self.client.post('/cancel-deletion-request/' + str(resource.id), {'descr': 'message'})

        self.assertFalse(DeletionRequest.objects.filter(sender=Owner.objects.get_by_natural_key('user2')).exists())

    def test_accept_access_request(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='user1', password='123456')
        response = self.client.get('/profile/')
        requests = response.context['requests_list']

        for request in requests:
            sender = request.sender
            resource = request.resource
            self.client.post('/approve-access-request/' + str(request.id), {'descr': 'message'})
            resources = sender.reader.all()
            self.assertTrue(resource in resources)

        resources = Owner.objects.get_by_natural_key('user1').owner.all()
        requests = AccessRequest.objects.filter(resource__in=resources)
        self.assertFalse(requests.exists())

    def test_deny_access_request(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='user1', password='123456')
        response = self.client.get('/profile/')
        requests = response.context['requests_list']

        for request in requests:
            sender = request.sender
            resource = request.resource
            self.client.post('/deny-access-request/' + str(request.id), {'descr': 'message'})
            resources = sender.reader.all()
            self.assertFalse(resource in resources)

        resources = Owner.objects.get_by_natural_key('user1').owner.all()
        requests = AccessRequest.objects.filter(resource__in=resources)
        self.assertFalse(requests.exists())

    def test_accept_deletion_request(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='admin', password='123456')
        response=self.client.get('/profile/')
        requests = response.context['requests_list']

        for request in requests:
            if isinstance(request, DeletionRequest):
                resource = request.resource
                self.client.post('/approve-deletion-request/' + str(request.id), {'descr': 'message'})
                self.assertTrue(resource not in Resource.objects.all())

        requests = DeletionRequest.objects.all()
        self.assertFalse(requests.exists())

    def test_deny_deletion_request(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='admin', password='123456')
        response = self.client.get('/profile/')
        requests = response.context['requests_list']

        for request in requests:
            if isinstance(request, DeletionRequest):
                resource = request.resource
                self.client.post('/deny-deletion-request/' + str(request.id), {'descr': 'message'})
                self.assertTrue(resource in Resource.objects.all())

        requests = DeletionRequest.objects.all()
        self.assertFalse(requests.exists())


