import pytest
from django.urls import reverse
from unittest.mock import patch, call, ANY , MagicMock
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django.conf import settings
from django.http import Http404
from urllib.parse import urlparse

from django.test import RequestFactory, override_settings


@pytest.fixture
def user(db):
    """
    Creates a user for testing
    """
    return get_user_model().objects.create_user(username='testuser', password='testpassword')


@pytest.fixture
def superuser(db):
    return User.objects.create_superuser("superuser", "super@example.com", "superpassword")

@pytest.fixture
def client_with_user(client, user):
    client.login(username="testuser", password="testpassword")
    return client

@pytest.fixture
def client_with_superuser(client, superuser):
    client.login(username="superuser", password="superpassword")
    return client


@override_settings(TEST_MODE=True)
# Mock to simulate geoserver layer and environment check without real connections
@pytest.mark.django_db
def test_template_rendering(client):
    client.logout()  # Ensure the test starts with an anonymous user.
    response = client.get(reverse("vfw_home:home"))
    assert response.status_code == 200, " ❌ Failed ❌ Home page did not render successfully."
    assert "vfw_home/home.html" in [t.name for t in response.templates], " ❌ Failed ❌ Home page did not use the expected template."

# @pytest.mark.xfail(reason="fixture 'mock_verify_layer' not found")
@patch("vfw_home.views.verify_layer")
@pytest.mark.django_db
def test_layer_name_setting_for_regular_user(mock_verify_layer, client_with_user):
    response = client_with_user.get(reverse("vfw_home:home"))
    assert "admin_layer" not in response.context["data_layer"], " ❌ Failed ❌ Regular user incorrectly assigned admin_layer."
    assert "admin_areal_layer" not in response.context["areal_data_layer"], " ❌ Failed ❌ Regular user incorrectly assigned admin_areal_layer."

@pytest.mark.django_db
def test_layer_name_setting_for_superuser(client_with_superuser):
    response = client_with_superuser.get(reverse("vfw_home:home"))
    assert "admin_layer" in response.context["data_layer"], " ❌ Failed ❌ Superuser not assigned admin_layer correctly."
    assert "admin_areal_layer" in response.context["areal_data_layer"], " ❌ Failed ❌ Superuser not assigned admin_areal_layer correctly."

@pytest.mark.django_db
def test_context_data_accuracy(client):
    response = client.get(reverse("vfw_home:home"))
    expected_keys = ["dataExt", "data_layer", "messages", "unblocked_ids"]
    missing_keys = [key for key in expected_keys if key not in response.context]
    assert not missing_keys, f" ❌ Failed ❌ Missing expected context keys: {missing_keys}"


@patch("vfw_home.views.verify_layer", autospec=True)
@pytest.mark.django_db
def test_layer_verification_for_regular_user(mock_verify_layer, client_with_user, django_db_blocker):
    with django_db_blocker.unblock():
        print("Patch applied to:", "vfw_home.Geoserver.geoserver_layer.verify_layer")

        # Simulate a request to the view
        response = client_with_user.get(reverse("vfw_home:home"))

        expected_calls = [
            call( request=ANY, datastore="db_test", workspace="db_test", filename=response.context["data_layer"]),
            call(request=ANY, datastore="db_test", workspace="db_test", filename=response.context["areal_data_layer"], layertype="areal_data"),
        ]

        print("Expected mock calls: ", expected_calls)
        print("Actual mock calls: ", mock_verify_layer.mock_calls)
        try:
            mock_verify_layer.assert_has_calls(expected_calls, any_order=True)
        except AssertionError as e:
            print(f"AssertionError: {e}")
            raise

        assert mock_verify_layer.call_count == 2, " ❌ Failed ❌ verify_layer was not called twice as expected for layer verification for a regular user."


@patch("vfw_home.views.verify_layer")
@pytest.mark.django_db
def test_layer_verification_for_superuser( mock_verify_layer, client_with_superuser):
    response = client_with_superuser.get(reverse("vfw_home:home"))
    expected_calls = [
        call(request=ANY, datastore="db_test", workspace="db_test", filename="admin_layer"),
        call(request=ANY, datastore="db_test", workspace="db_test", filename="admin_areal_layer", layertype="areal_data"),
    ]
    mock_verify_layer.assert_has_calls(expected_calls, any_order=True)
    assert mock_verify_layer.call_count == 2, " ❌ Failed ❌ verify_layer was not called twice as expected for layer verification for an admin."

@pytest.mark.django_db
def test_session_data_for_datasets(client):
    session = client.session
    session["datasets"] = ["dataset1", "dataset2"]
    session.save()
    response = client.get(reverse("vfw_home:home"))
    assert response.context["unblocked_ids"] == ["dataset1", "dataset2"], "❌ Failed ❌ The view did not correctly utilize session data for 'unblocked_ids'."

@patch("vfw_home.views.verify_layer")
@pytest.mark.django_db
def test_home_view_geoserver_unavailable(mock_verify_layer, client):
    mock_verify_layer.side_effect = Exception("Geoserver unavailable")
    response = client.get(reverse("vfw_home:home"))
    mock_verify_layer.assert_called_once()
    assert response.status_code == 200, " ❌ Failed ❌ Page failed to load when Geoserver was unavailable."

@pytest.mark.django_db
def test_home_view_incorrect_session_data_format(client):
    session = client.session
    session["datasets"] = "not_a_list"  # Incorrect format intentionally set
    session.save()
    response = client.get(reverse("vfw_home:home"))
    assert response.status_code == 200 , " ❌ Failed ❌ Page failed to load with incorrect session data format."






@pytest.fixture
def rf():
    return RequestFactory()


@patch('vfw_home.views.logger')
def test_dispatch_logs_message_for_authenticated_user(mock_logger, rf, user, django_db_blocker):
    with django_db_blocker.unblock():
        from vfw_home.views import LoginView
        request = rf.get('/login/')
        request.user = user
        view = LoginView.as_view()
        response = view(request)
        mock_logger.debug.assert_called_with(f'{user.username} logged in as')


@patch('vfw_home.views.logger')
def test_dispatch_logs_message_for_unauthenticated_user(mock_logger, rf):
    from vfw_home.views import LoginView

    request = rf.get('/login/')
    request.user = MagicMock(is_authenticated=False)
    view = LoginView.as_view()
    response = view(request)
    mock_logger.debug.assert_called_with('The user is not authenticated!')

    

# Test Cases for LogoutView
#    1. Test Case: User Logout and Redirection

@pytest.fixture
def client_with_login(client, user):
    """
    Logs in the user for testing
    """
    client.login(username='testuser', password='testpassword')
    return client

def test_logout_user_and_redirect(client_with_login):
    """
    Test that the user is logged out and redirected to the home page.
    """
    response = client_with_login.post(reverse('vfw_home:logout'))
    
    # Ensure that the user is redirected to the home page
    assert response.status_code == 302
    # Normalize URLs to compare only the path
    assert urlparse(response.url).path == urlparse(reverse('vfw_home:home')).path


    
    # Ensure the user is logged out
    assert '_auth_user_id' not in client_with_login.session


# 2. Test Case: Logging Out an Unauthenticated User
def test_logout_unauthenticated_user(client):
    """
    Test that an unauthenticated user is redirected to the home page without error.
    """
    response = client.post(reverse('vfw_home:logout'))
    
    # Ensure that the user is redirected to the home page
    assert response.status_code == 302
    # assert response.url == reverse('vfw_home:home')
    assert urlparse(response.url).path == urlparse(reverse('vfw_home:home')).path


# 3. Test Case: Logging Message for Logged Out User

def add_session_to_request(request):
    """Helper function to add session to the request."""
    from django.contrib.sessions.middleware import SessionMiddleware

    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request)
    request.session.save()

@patch('vfw_home.views.logger')
@pytest.mark.django_db
def test_logout_logging(mock_logger, rf):
    """
    Test that the correct logging message is generated when a user logs out.
    """

    from vfw_home.views import LogoutView

    # Set up a mock request
    request = rf.post(reverse('vfw_home:logout'))
    
    # Manually add session and user to the request
    add_session_to_request(request)
    request.user = MagicMock(username='testuser', is_authenticated=True)

    # Call the view's post method directly
    view = LogoutView.as_view()
    response = view(request)

    # Check for redirect status and home page redirection
    assert response.status_code == 302
    assert response.url == reverse('vfw_home:home')

    # Check if logger was called and print message
    if mock_logger.debug.called:
        print("Actual debug log message:", mock_logger.debug.call_args)
    else:
        print("mock_logger.debug was not called.")

    # Assert expected log message
    mock_logger.debug.assert_called_with('testuser logged out (auth status: False)')



# Base URL template for the Geoserver view
GEOSERVER_URL_TEMPLATE = '/geoserver/{service}/{layer}/{bbox}/{srid}'

@pytest.mark.django_db
@patch('urllib.request.urlopen')
class TestGeoserverView:
    @classmethod
    def setup_class(cls):
        from urllib.error import URLError
        from vfw_home.views import GeoserverView
        cls.GeoserverView = GeoserverView
        cls.URLError = URLError

    # Test case 1: Basic Valid Request
    def test_geoserver_view_basic_valid_request(self, mock_urlopen):
        """
        Test a basic, valid request to the GeoserverView. 
        
        This test verifies that the view correctly builds the URL, 
        sends a request, and returns the expected JSON data for valid input parameters.
        """
  
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"success": true, "data": "sample layer data"}'
        mock_urlopen.return_value = mock_response

        url = GEOSERVER_URL_TEMPLATE.format(
            service='wfs', layer='sample_layer', bbox='-976.82,530.56,2741.65,702.43', srid=4326
        )
        request = RequestFactory().get(url)
        
        response = self.GeoserverView.as_view()(request, 'wfs', 'sample_layer', '-976.82,530.56,2741.65,702.43', 4326)

        assert response.status_code == 200
        assert "success" in response.content.decode('utf-8')
        assert "sample layer data" in response.content.decode('utf-8')
        print("Test Case - Basic Valid Request: Passed")



    # Test case 2: Invalid Bbox Format
    def test_geoserver_view_invalid_bbox(self, mock_urlopen):
        """
        Test the GeoserverView with an invalid bbox format.
        
        This test checks if the view properly raises an URLError for invalid bbox format.
        """

        mock_urlopen.side_effect = self.URLError("Invalid bbox format")

        url = GEOSERVER_URL_TEMPLATE.format(
            service='wfs', layer='sample_layer', bbox='invalid_bbox', srid=4326
        )
        request = RequestFactory().get(url)
        
        with pytest.raises(self.URLError) as e:
            self.GeoserverView.as_view()(request, 'wfs', 'sample_layer', 'invalid_bbox', 4326)
        print(f"Test Case - Invalid Bbox Format: Raised URLError as expected with message '{e.value}'")


    # Test case 3: Unsupported SRID
    def test_geoserver_view_unsupported_srid(self, mock_urlopen):
        """
        Test the GeoserverView with an unsupported SRID.
        
        This test ensures that the view raises an URLError if an unsupported SRID is provided.
        """
   
        mock_urlopen.side_effect = self.URLError("Unsupported SRID")

        url = GEOSERVER_URL_TEMPLATE.format(
            service='wfs', layer='sample_layer', bbox='-976.82,530.56,2741.65,702.43', srid=1234
        )
        request = RequestFactory().get(url)
        
        with pytest.raises(self.URLError) as e:
            self.GeoserverView.as_view()(request, 'wfs', 'sample_layer', '-976.82,530.56,2741.65,702.43', 1234)
        print(f"Test Case - Unsupported SRID: Raised URLError as expected with message '{e.value}'")


    # Test case 4: Geoserver Down
    def test_geoserver_view_geoserver_down(self ,mock_urlopen):
        """
        Simulate the Geoserver being down and ensure the GeoserverView handles this gracefully.
        
        This test raises an URLError simulating server downtime, and verifies that it is correctly raised.
        """

        mock_urlopen.side_effect = self.URLError("Unable to reach Geoserver")

        url = GEOSERVER_URL_TEMPLATE.format(
            service='wfs', layer='sample_layer', bbox='-976.82,530.56,2741.65,702.43', srid=4326
        )
        request = RequestFactory().get(url)

        with pytest.raises(self.URLError) as e:
            self.GeoserverView.as_view()(request, 'wfs', 'sample_layer', '-976.82,530.56,2741.65,702.43', 4326)
        print(f"Test Case - Geoserver Down: Raised URLError as expected with message '{e.value}'")



    # Test case 5: Unsupported Service Type
    def test_geoserver_view_invalid_service_type(self, mock_urlopen):
        """
        Test the GeoserverView with an unsupported service type.
        
        This test ensures that an unsupported service type raises an URLError, as expected.
        """

        mock_urlopen.side_effect = self.URLError("Unsupported service type")

        url = GEOSERVER_URL_TEMPLATE.format(
            service='xyz', layer='sample_layer', bbox='-976.82,530.56,2741.65,702.43', srid=4326
        )
        request = RequestFactory().get(url)
        
        with pytest.raises(self.URLError) as e:
            self.GeoserverView.as_view()(request, 'xyz', 'sample_layer', '-976.82,530.56,2741.65,702.43', 4326)
        print(f"Test Case - Unsupported Service Type: Raised URLError as expected with message '{e.value}'")



# Mock the `test_geoserver_env` function to prevent database or external server calls.
@pytest.mark.django_db
@patch('vfw_home.views.test_geoserver_env')
@patch('vfw_home.views.get_accessible_data')
@patch('vfw_home.views.get_dataset')
def test_csv_download(mock_get_dataset, mock_get_accessible_data, mock_test_geoserver_env):
    from django.http import StreamingHttpResponse
    from vfw_home.views import DatasetDownloadView
    mock_test_geoserver_env.return_value = None  # Prevents it from calling actual Geoserver or DB
    mock_get_accessible_data.return_value = {'open': [1], 'blocked': []}
    mock_get_dataset.return_value = [['header1', 'header2'], ['data1', 'data2']]

    request = RequestFactory().get(reverse('vfw_home:datasetdownload') + '?csv=1')
    response = DatasetDownloadView.as_view()(request)

    assert isinstance(response, StreamingHttpResponse)
    assert response.status_code == 200
    assert response['Content-Disposition'] == 'attachment; filename="somefilename.csv"'

    # Access the streaming content and check for expected CSV output
    content = b''.join(response.streaming_content)
    assert b'header1,header2\r\n' in content
    assert b'data1,data2\r\n' in content