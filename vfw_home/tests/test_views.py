from django.test import TestCase, Client, RequestFactory, override_settings
from django.contrib.messages import get_messages
from django.urls import reverse
from unittest.mock import patch , call, ANY
from django.contrib.auth.models import User, AnonymousUser
from vfw_home.views import HomeView
import logging
import sys
import os
import django



logger = logging.getLogger(__name__)  
logging.basicConfig(filename='./vfw_home/tests/logs/test_results_views.log', filemode='a', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

# @override_settings(DEBUG=True)  # Ensure settings align with test expectations if needed
class HomePageTest(TestCase):

    def setUp(self):
        # Create a user and log them in 
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.client = Client()


    def tearDown(self):
        # Clean up any objects created during the tests
        User.objects.all().delete()

    def test_template_rendering(self):

        """
        Tests that HomeView uses the correct template for an anonymous user.
        """
        self.client.logout()  # Ensure the test starts with an anonymous user.
        response = self.client.get(reverse('vfw_home:home'))
        self.assertEqual(response.status_code, 200, msg=" ❌ Failed ❌ Home page did not render successfully.")
        self.assertTemplateUsed(response, 'vfw_home/home.html', msg_prefix=" ❌ Failed ❌ test: test_template_rendering  Home page did not use the expected template.")
        logger.debug("✅ OK. ✅ HomeView template rendering test passed.")




  
    def test_layer_name_setting_for_authenticated_users(self):
        """
        Tests that the correct data_layer is set for both regular and superusers.
        """
        # Testing with a regular user
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('vfw_home:home'))


        self.assertNotIn('admin_layer', response.context['data_layer'],
                         msg=" ❌ Failed ❌ Regular user incorrectly assigned admin_layer.")
        self.assertNotIn('admin_areal_layer', response.context['areal_data_layer'],
                         msg=" ❌ Failed ❌ Regular user incorrectly assigned admin_areal_layer.")
        
        logger.debug(" ✅ OK. ✅ Layer name setting for regular user passed.")


        # Testing with a superuser
        superuser = User.objects.create_superuser('superuser', 'super@example.com', 'superpassword')
        self.client.login(username='superuser', password='superpassword')
        response = self.client.get(reverse('vfw_home:home'))


        self.assertIn('admin_layer', response.context['data_layer'],
                      msg=" ❌ Failed ❌ Superuser not assigned admin_layer correctly.")
        self.assertIn('admin_areal_layer', response.context['areal_data_layer'],
                      msg=" ❌ Failed ❌ Superuser not assigned admin_areal_layer correctly.")

        logger.debug(" ✅ OK. ✅ Layer name setting for superuser passed.")




    def test_context_data_accuracy(self):

        """
        Verifies that the HomeView context contains all expected keys, ensuring the view
        correctly prepares data for the template.
        """
        response = self.client.get(reverse('vfw_home:home'))
        expected_keys = ['dataExt', 'data_layer', 'messages', 'unblocked_ids']

        missing_keys = [key for key in expected_keys if key not in response.context]
        self.assertFalse(missing_keys, f" ❌ Failed ❌ Missing expected context keys: {missing_keys}")
        logger.debug(" ✅ OK. ✅ Context data accuracy test passed: All expected keys are present.")



    @patch('vfw_home.views.verify_layer')
    def test_layer_verification_for_regular_user(self, mock_verify_layer):
        """
        Test verify_layer calls for a regular authenticated user.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('vfw_home:home'))

        # Define the expected calls to verify_layer with parameters for regular user
        expected_calls = [
            call(request=ANY, datastore='metacatalogdev', workspace='metacatalogdev', filename=response.context['data_layer']),
            call(request=ANY, datastore='metacatalogdev', workspace='metacatalogdev', filename=response.context['areal_data_layer'], layertype='areal_data')
        ]

        # Assert verify_layer was called with the expected parameters
        mock_verify_layer.assert_has_calls(expected_calls, any_order=True)
        self.assertEqual(mock_verify_layer.call_count, 2, msg=" ❌ Failed ❌ verify_layer was not called twice as expected for layer verification for a regular user.")
        logger.debug("✅ OK. ✅ GeoServer layer creation triggered correctly for authenticated user (regular user).")


    @patch('vfw_home.views.verify_layer')
    def test_layer_verification_for_superuser(self, mock_verify_layer):
        """
        Test verify_layer calls for a superuser.
        """
        User.objects.create_superuser(username='superuser', email='super@example.com', password='superpassword')
        self.client.login(username='superuser', password='superpassword')
        self.client.get(reverse('vfw_home:home'))

        # Define the expected calls to verify_layer with parameters for superuser
        expected_calls = [
            call(request=ANY, datastore='metacatalogdev', workspace='metacatalogdev', filename='admin_layer'),
            call(request=ANY, datastore='metacatalogdev', workspace='metacatalogdev', filename='admin_areal_layer', layertype='areal_data')
        ]

        # Assert verify_layer was called with the expected parameters
        mock_verify_layer.assert_has_calls(expected_calls, any_order=True)
        self.assertEqual(mock_verify_layer.call_count, 2 , msg=" ❌ Failed ❌ verify_layer was not called twice as expected for layer verification for an admin.")
        logger.debug("✅ OK. ✅ GeoServer layer creation triggered correctly for authenticated user (admin user).")



    def test_session_data_for_datasets(self):
        """
        Ensures that HomeView correctly utilizes session data for datasets, reflecting
        the data in its context for use in the template.
        """
        # Prepare session data
        session = self.client.session
        session['datasets'] = ['dataset1', 'dataset2']
        session.save()

        response = self.client.get(reverse('vfw_home:home'))
        self.assertEqual(response.context['unblocked_ids'], ['dataset1', 'dataset2'],
                         "❌ Failed ❌ The view did not correctly utilize session data for 'unblocked_ids'.")
        logger.debug(" ✅ OK. ✅ Session data for datasets test passed: Correctly reflected in view context.")




    @patch('vfw_home.views.verify_layer')
    def test_home_view_geoserver_unavailable(self, mock_verify_layer):

        """
        Objective: Verify HomeView's behavior when Geoserver is unavailable for layer creation.
        Methodology: Use patching to simulate an exception during layer creation, mimicking Geoserver unavailability. The test checks HomeView's ability to handle this exception gracefully.
        Expected Outcome: Despite the simulated Geoserver unavailability, HomeView should load successfully with a status code of 200, indicating robust error handling.
        """
        mock_verify_layer.side_effect = Exception("Geoserver unavailable")
        response = self.client.get(reverse('vfw_home:home'))
        mock_verify_layer.assert_called_once()
        self.assertEqual(response.status_code, 200, msg=" ❌ Failed ❌ Page failed to load when Geoserver was unavailable.")
        # TODO:  Additional checks for user feedback can be added here
        logger.debug("✅ OK. ✅ HomeView gracefully handled Geoserver unavailability.")


    def test_home_view_incorrect_session_data_format(self):

        """
        Objective: Test HomeView's resilience to incorrect session data formats.
        Methodology: Manipulate session data to an incorrect format and load HomeView.
        Expected Outcome: HomeView loads successfully, indicating robust error handling.
        """
        session = self.client.session
        session['datasets'] = "not_a_list"  # Incorrect format intentionally set
        session.save()

        response = self.client.get(reverse('vfw_home:home'))

        # Verify: Ensure the page loads without server errors and handles the edge case gracefully
        self.assertEqual(response.status_code, 200, msg=" ❌ Failed ❌ Page failed to load with incorrect session data format.")
        logger.debug(" ✅OK. ✅ HomeView handled incorrect session data format gracefully.")


    # print("User.objects: ", User.objects.all())
        
