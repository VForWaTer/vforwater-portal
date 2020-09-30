import unittest
from django.test import Client
from django.test import TestCase
from unittest import skip
from django.contrib.auth.models import User

from author_manage.models import *
from test.support import resource

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

    test_user = User.objects.create(username='boncho')
    test_user.set_password('123456')
    test_user.save()

    test_user2 = User.objects.create(username='evlogi')
    test_user2.set_password('123456')
    test_user2.save()

    return {'test_admin':test_admin,'test_user':test_user,'test_user2':test_user2}


def setUpResourceAndRequests(users):
    """

    @param users:
    @type users:
    @return:
    @rtype:
    """
    res = Resource.objects.create(name='res',type='text',description='desc',link='res.txt')
    res.readers.add(users['test_user'].id)
    res.owners.add(users['test_user'].id)
    res.readers.add(users['test_admin'].id)
    res.owners.add(users['test_admin'].id)
    res.save()

    res2 = Resource.objects.create(name='res2',type='text',description='desc',link='res2.txt')
    res2.readers.add(users['test_user'].id)
    res2.owners.add(users['test_user'].id)
    res2.readers.add(users['test_admin'].id)
    res2.owners.add(users['test_admin'].id)
    res2.save()

    res3 = Resource.objects.create(name='res3',type='text',description='desc',link='res3.txt')
    res3.readers.add(users['test_user2'].id)
    res3.owners.add(users['test_user2'].id)
    res3.save();

    res4 = Resource.objects.create(name='res4',type='text',description='desc',link='res4.txt')
    res4.readers.add(users['test_user2'].id)
    res4.owners.add(users['test_user2'].id)
    res4.readers.add(users['test_admin'].id)
    res4.owners.add(users['test_admin'].id)
    res4.save();

    access_req = AccessRequest.objects.create(sender=users['test_user2'],resource=res)
    access_req.save()
    access_req2 = AccessRequest.objects.create(sender=users['test_user2'],resource=res2)
    access_req2.save()

    deletion_req = DeletionRequest.objects.create(sender=users['test_user'],resource=res)
    deletion_req.save()
    deletion_req2 = DeletionRequest.objects.create(sender=users['test_user'],resource=res2)
    deletion_req2.save()
    deletion_req3 = DeletionRequest.objects.create(sender=users['test_user2'],resource=res3)
    deletion_req3.save()

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

class TestHomeView(TestCase):
    """

    """

    @classmethod
    def setUpClass(cls):
        """

        @return:
        @rtype:
        """
        super().setUpClass()
        setUpUsers()

    def setUp(self):
        """"""

        self.client = Client()

    @classmethod
    def tearDownClass(cls):
        """

        @return:
        @rtype:
        """
        deleteUsers()
        super().tearDownClass()

    def test_not_logged_in(self):
        """

        @return:
        @rtype:
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_normal(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.get('/')
        self.assertEqual(str(response.context['user']),'boncho')
        self.assertEqual(response.status_code, 200)



class TestResourceManager(TestCase):
    """

    """

    @classmethod
    def setUpClass(cls):
        """

        @return:
        @rtype:
        """
        super().setUpClass()
        setUpUsers()

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
        super().tearDownClass()

    def test_not_logged_in(self):
        """

        @return:
        @rtype:
        """
        response = self.client.get('/resource-manager/')
        self.assertEqual(response.status_code, 302)

    def test_logged_in_no_admin(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.get('/resource-manager/')
        self.assertEqual(response.status_code, 302)

    def test_normal(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='admin', password='123456')
        response = self.client.get('/resource-manager/')
        self.assertEqual(str(response.context['user']),'admin')
        self.assertEqual(response.status_code, 200)

class TestUserManager(TestCase):
    """

    """

    @classmethod
    def setUpClass(cls):
        """

        @return:
        @rtype:
        """
        super().setUpClass()
        setUpUsers()

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
        super().tearDownClass()

    def test_not_logged_in(self):
        """

        @return:
        @rtype:
        """
        response = self.client.get('/user-manager/')
        self.assertEqual(response.status_code, 302)

    def test_logged_in_no_admin(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.get('/user-manager/')
        self.assertEqual(response.status_code, 302)

    def test_normal(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='admin', password='123456')
        response = self.client.get('/user-manager/')
        self.assertEqual(str(response.context['user']),'admin')
        self.assertEqual(response.status_code, 200)


class TestProfileView(TestCase):
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
        deleteResourcesAndRequests()
        deleteUsers()
        super().tearDownClass()

    def test_not_logged_in(self):
        """

        @return:
        @rtype:
        """
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 302)

    def test_normal(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.get('/profile/')
        self.assertEqual(str(response.context['user']),'boncho')
        self.assertEqual(response.status_code, 200)

    def test_pagination_user(self):
        """

        @return:
        @rtype:
        """
        #User has to see only the two access requests for him
        self.client.login(username='boncho', password='123456')
        response = self.client.get('/profile/')
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == False)
        self.assertEqual(len(response.context['requests_list']), 2)

    def test_pagination_admin_page_1(self):
        """

        @return:
        @rtype:
        """
        #Admin has to see the two access and the three deletion requests for him
        #Only 4 of them are shown on page 1
        self.client.login(username='admin', password='123456')
        response = self.client.get('/profile/')
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['requests_list']), 4)


    def test_pagination_admin_page_2(self):
        """

        @return:
        @rtype:
        """
        #Admin has to see the two access and the three deletion requests for him
        #The last deletion request is shown on page 2
        self.client.login(username='admin', password='123456')
        response = self.client.get('/profile/?page=2')
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['requests_list']), 1)

class TestMyResourcesView(TestCase):
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
        deleteResourcesAndRequests()
        deleteUsers()
        super().tearDownClass()

    def test_not_logged_in(self):
        """

        @return:
        @rtype:
        """
        response = self.client.get('/profile/my-resources/')
        self.assertEqual(response.status_code, 302)

    def test_normal(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.get('/profile/my-resources/')
        self.assertEqual(str(response.context['user']),'boncho')
        self.assertEqual(response.status_code, 200)

    def test_resources_shown(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.get('/profile/my-resources/')
        self.assertTrue('resource_list' in response.context)
        self.assertEqual(len(response.context['resource_list']), 2)

class TestSendDeletionRequestView(TestCase):
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
        deleteResourcesAndRequests()
        deleteUsers()
        super().tearDownClass()

    def test_not_logged_in(self):
        """

        @return:
        @rtype:
        """
        response = self.client.post('/send-deletion-request/1')
        self.assertEqual(response.status_code, 302)

    def test_not_existing_resource(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='evlogi', password='123456')
        response = self.client.post('/send-deletion-request/50')
        self.assertEqual(response.status_code, 404)

    def test_not_owner(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.post('/send-deletion-request/4')
        self.assertEqual(response.status_code, 403)

    def test_staff_user(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='admin', password='123456')
        response = self.client.post('/send-deletion-request/4')
        self.assertEqual(response.status_code, 302)

    def test_deletion_request_exists(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='evlogi', password='123456')
        response = self.client.post('/send-deletion-request/3')
        self.assertEqual(response.status_code, 302)

    def test_normal(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='evlogi', password='123456')
        response = self.client.post('/send-deletion-request/4', {'descr':''})
        self.assertEqual(response.status_code, 302)
class TestCancelDeletionRequestView(TestCase):
    """

    """

    @classmethod
    def setUpClass(cls):
        """"""

        super().setUpClass()
        users = setUpUsers()
        setUpResourceAndRequests(users)

    def setUp(self):
        self.client = Client()

    @classmethod
    def tearDownClass(cls):
        """

        @return:
        @rtype:
        """
        deleteResourcesAndRequests()
        deleteUsers()
        super().tearDownClass()

    def test_not_logged_in(self):
        """

        @return:
        @rtype:
        """
        response = self.client.post('/cancel-deletion-request/1')
        self.assertEqual(response.status_code, 302)

    def test_not_existing_resource(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='evlogi', password='123456')
        response = self.client.post('/cancel-deletion-request/50')
        self.assertEqual(response.status_code, 404)

    def test_not_owner(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='evlogi', password='123456')
        response = self.client.post('/cancel-deletion-request/1')
        self.assertEqual(response.status_code, 403)

    def test_staff_user(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='admin', password='123456')
        response = self.client.post('/cancel-deletion-request/1')
        self.assertEqual(response.status_code, 302)


    def test_deletion_request_doesnt_exist(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='evlogi', password='123456')
        response = self.client.post('/cancel-deletion-request/4')
        self.assertEqual(response.status_code, 404)

    def test_normal(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.post('/cancel-deletion-request/1')
        self.assertEqual(response.status_code, 302)

class TestApproveAccessRequestView(TestCase):
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
        deleteResourcesAndRequests()
        deleteUsers()
        super().tearDownClass()

    def test_not_logged_in(self):
        response = self.client.post('/approve-access-request/1')
        self.assertEqual(response.status_code, 302)


    def test_not_existing_request(self):
        self.client.login(username='boncho', password='123456')
        response = self.client.post('/approve-access-request/50')
        self.assertEqual(response.status_code, 404)


    def test_not_owner(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='evlogi', password='123456')
        response = self.client.post('/approve-access-request/1')
        self.assertEqual(response.status_code, 403)

    def test_normal(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.post('/approve-access-request/1', {'descr':''})
        self.assertEqual(response.status_code, 302)

class TestDenyAccessRequestView(TestCase):
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

        deleteResourcesAndRequests()
        deleteUsers()
        super().tearDownClass()

    def test_not_logged_in(self):
        """

        @return:
        @rtype:
        """
        response = self.client.post('/deny-access-request/1')
        self.assertEqual(response.status_code, 302)


    def test_not_existing_request(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.post('/deny-access-request/50')
        self.assertEqual(response.status_code, 404)


    def test_not_owner(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='evlogi', password='123456')
        response = self.client.post('/deny-access-request/1')
        self.assertEqual(response.status_code, 403)

    def test_normal(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.post('/deny-access-request/1', {'descr':''})
        self.assertEqual(response.status_code, 302)


class TestSendAccessRequestView(TestCase):
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
        deleteResourcesAndRequests()
        deleteUsers()
        super().tearDownClass()

    def test_not_logged_in(self):
        """

        @return:
        @rtype:
        """
        response = self.client.post('/send-access-request/4')
        self.assertEqual(response.status_code, 302)

    def test_not_existing_resource(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.post('/send-access-request/50')
        self.assertEqual(response.status_code, 404)

    def test_reader(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='evlogi', password='123456')
        response = self.client.post('/send-access-request/4')
        self.assertEqual(response.status_code, 302)


    def test_staff_user(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='admin', password='123456')
        response = self.client.post('/send-access-request/3')
        self.assertEqual(response.status_code, 302)

    def test_access_request_exists(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='evlogi', password='123456')
        response = self.client.post('/send-access-request/1')
        self.assertEqual(response.status_code, 302)

    def test_normal(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.post('/send-access-request/4', {'descr':''})
        self.assertEqual(response.status_code, 302)

class TestCancelAccessRequestView(TestCase):
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
        deleteResourcesAndRequests()
        deleteUsers()
        super().tearDownClass()

    def test_not_logged_in(self):
        """

        @return:
        @rtype:
        """
        response = self.client.post('/cancel-access-request/1')
        self.assertEqual(response.status_code, 302)

    def test_not_existing_resource(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.post('/cancel-access-request/50')
        self.assertEqual(response.status_code, 404)

    def test_reader(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='evlogi', password='123456')
        response = self.client.post('/cancel-access-request/4')
        self.assertEqual(response.status_code, 404)


    def test_staff_user(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='admin', password='123456')
        response = self.client.post('/cancel-access-request/3')
        self.assertEqual(response.status_code, 404)

    def test_access_request_doesnt_exist(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.post('/cancel-access-request/4')
        self.assertEqual(response.status_code, 404)

    def test_normal(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='evlogi', password='123456')
        response = self.client.post('/cancel-access-request/1')
        self.assertEqual(response.status_code, 302)

class TestDeleteResourceView(TestCase):
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
        deleteResourcesAndRequests()
        deleteUsers()
        super().tearDownClass()

    def test_not_logged_in(self):
        """

        @return:
        @rtype:
        """
        response = self.client.post('/delete-resource/1')
        self.assertEqual(response.status_code, 302)

    def test_not_existing_resource(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.post('/delete-resource/50')
        self.assertEqual(response.status_code, 404)

    def test_not_staff_user(self):
        """"""

        self.client.login(username='evlogi', password='123456')
        response = self.client.post('/delete-resource/1')
        self.assertEqual(response.status_code, 403)

    def test_normal(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='admin', password='123456')
        response = self.client.post('/delete-resource/1', {'descr':''})
        self.assertEqual(response.status_code, 302)




class TestEditNameView(TestCase):
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
        deleteResourcesAndRequests()
        deleteUsers()
        super().tearDownClass()

    def test_not_logged_in(self):
        """

        @return:
        @rtype:
        """
        response = self.client.get('/profile/edit-name/')
        self.assertEqual(response.status_code, 302)

    def test_normal(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.post('/profile/edit-name/', {'firstName':'', 'lastName': ''})
        self.assertEqual(response.status_code, 302)


class TestResourcesOverview(TestCase):
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
        deleteResourcesAndRequests()
        deleteUsers()
        super().tearDownClass()

    def test_not_logged_in(self):
        """

        @return:
        @rtype:
        """
        response = self.client.get('/resources-overview/')
        self.assertEqual(response.status_code, 302)

    def test_normal(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.get('/resources-overview/')
        self.assertEqual(str(response.context['user']),'boncho')
        self.assertEqual(response.status_code, 200)

    def test_pagination_user(self):
        """

        @return:
        @rtype:
        """
        #User has to see only the four resources
        self.client.login(username='boncho', password='123456')
        response = self.client.get('/resources-overview/')
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == False)
        self.assertEqual(len(response.context['resources_list']), 4)

class TestResourcesOverviewSearch(TestCase):
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
        deleteResourcesAndRequests()
        deleteUsers()
        super().tearDownClass()

    def test_not_logged_in(self):
        """

        @return:
        @rtype:
        """
        response = self.client.get('/resources-overview/search?q=2')
        self.assertEqual(response.status_code, 302)


    def test_normal(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.get('/resources-overview/search?q=2')
        self.assertEqual(response.status_code, 200)

    def test_no_query(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.get('/resources-overview/search')
        self.assertEqual(response.status_code, 302)

    def test_valid_query(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.get('/resources-overview/search?q=2')
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == False)
        self.assertEqual(len(response.context['resources_list']), 1)

class TestPermissionEditingView(TestCase):
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
        deleteResourcesAndRequests()
        deleteUsers()
        super().tearDownClass()

    def test_not_logged_in(self):
        """

        @return:
        @rtype:
        """
        response = self.client.get('/profile/my-resources/1-edit-users-permissions')
        self.assertEqual(response.status_code, 301)

    def test_not_existing_resource_get(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.get('/profile/my-resources/50-edit-users-permissions/')
        self.assertEqual(response.status_code, 404)

    def test_not_existing_resource_post(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.post('/profile/my-resources/50-edit-users-permissions/')
        self.assertEqual(response.status_code, 404)

    def test_not_authorized_user(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='evlogi', password='123456')
        response = self.client.get('/profile/my-resources/1-edit-users-permissions/')
        self.assertEqual(response.status_code, 403)

    def test_normal_get(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.get('/profile/my-resources/1-edit-users-permissions/')
        self.assertEqual(response.status_code, 200)

    def test_normal_post(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.post('/profile/my-resources/1-edit-users-permissions/')
        self.assertEqual(response.status_code, 302)

    def test_pagination_users(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.get('/profile/my-resources/1-edit-users-permissions/')
        self.assertTrue('user_list' in response.context)
        self.assertEqual(len(response.context['user_list']), 2)

class TestPermissionEditingViewSearch(TestCase):
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
        deleteResourcesAndRequests()
        deleteUsers()
        super().tearDownClass()

    def test_not_logged_in(self):
        """

        @return:
        @rtype:
        """
        response = self.client.get('/profile/my-resources/1-edit-users-permissions/search?q=evl')
        self.assertEqual(response.status_code, 302)

    def test_not_existing_resource_get(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.get('/profile/my-resources/50-edit-users-permissions/search?q=evl')
        self.assertEqual(response.status_code, 404)

    def test_not_existing_resource_post(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.post('/profile/my-resources/50-edit-users-permissions/search?q=evl')
        self.assertEqual(response.status_code, 404)

    def test_not_authorized_user(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='evlogi', password='123456')
        response = self.client.get('/profile/my-resources/1-edit-users-permissions/search?q=evl')
        self.assertEqual(response.status_code, 403)

    def test_no_query(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.get('/profile/my-resources/1-edit-users-permissions/search')
        self.assertEqual(response.status_code, 302)

    def test_normal_get(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.get('/profile/my-resources/1-edit-users-permissions/search?q=evl')
        self.assertEqual(response.status_code, 200)

    def test_valid_query(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.get('/profile/my-resources/1-edit-users-permissions/search?q=evl')
        self.assertTrue('user_list' in response.context)
        self.assertEqual(len(response.context['user_list']), 1)

    def test_normal_post(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.post('/profile/my-resources/1-edit-users-permissions/')
        self.assertEqual(response.status_code, 302)

class TestAddNewResourceView(TestCase):
    """

    """

    @classmethod
    def setUpClass(cls):
        """

        @return:
        @rtype:
        """
        super().setUpClass()
        setUpUsers()

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
        super().tearDownClass()

    def test_not_logged_in(self):
        """

        @return:
        @rtype:
        """
        response = self.client.get('/profile/my-resources/add-new-resource/')
        self.assertEqual(response.status_code, 302)

    def test_normal_get(self):
        """

        @return:
        @rtype:
        """

        self.client.login(username='boncho', password='123456')
        response = self.client.get('/profile/my-resources/add-new-resource/')
        self.assertEqual(response.status_code, 200)

    def test_no_resource_form(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.post('/profile/my-resources/add-new-resource/',{'name':'a','type':'a','description':'a','link':''})
        self.assertEqual(response.status_code, 302)

class TestOpenResourceView(TestCase):
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
        deleteResourcesAndRequests()
        deleteUsers()
        super().tearDownClass()

    def test_not_logged_in(self):
        """

        @return:
        @rtype:
        """
        response = self.client.get('/resources/1')
        self.assertEqual(response.status_code, 302)

    def test_not_existing_resource(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.get('/resources/50')
        self.assertEqual(response.status_code, 404)

    def test_not_reader(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.get('/resources/4')
        self.assertEqual(response.status_code, 403)

    @skip
    def test_normal(self):
        """

        @return:
        @rtype:
        """
        #It will work normally only if there is file res.txt in the resources folder of the web project
        self.client.login(username='boncho', password='123456')
        response = self.client.get('/resources/1')
        self.assertEqual(response.status_code, 200)


class TestApproveDeletionRequestView(TestCase):
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
        deleteResourcesAndRequests()
        deleteUsers()
        super().tearDownClass()

    def test_not_logged_in(self):
        """

        @return:
        @rtype:
        """
        response = self.client.post('/approve-deletion-request/1')
        self.assertEqual(response.status_code, 302)


    def test_not_existing_request(self):
        """

        @return:
        @rtype:
        """

        self.client.login(username='boncho', password='123456')
        response = self.client.post('/approve-deletion-request/50')
        self.assertEqual(response.status_code, 404)


    def test_not_admin(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='evlogi', password='123456')
        response = self.client.post('/approve-deletion-request/1')
        self.assertEqual(response.status_code, 403)

    def test_normal(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='admin', password='123456')
        response = self.client.post('/approve-deletion-request/1', {'descr':''})
        self.assertEqual(response.status_code, 302)

class TestDenyDeletionRequestView(TestCase):
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
        deleteResourcesAndRequests()
        deleteUsers()
        super().tearDownClass()


    def test_not_logged_in(self):
        """

        @return:
        @rtype:
        """
        response = self.client.post('/deny-deletion-request/1')
        self.assertEqual(response.status_code, 302)


    def test_not_existing_request(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='boncho', password='123456')
        response = self.client.post('/deny-deletion-request/50')
        self.assertEqual(response.status_code, 404)


    def test_not_admin(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='evlogi', password='123456')
        response = self.client.post('/deny-deletion-request/1')
        self.assertEqual(response.status_code, 403)

    def test_normal(self):
        """

        @return:
        @rtype:
        """
        self.client.login(username='admin', password='123456')
        response = self.client.post('/deny-deletion-request/1', {'descr':''})
        self.assertEqual(response.status_code, 302)
