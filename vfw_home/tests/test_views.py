import pytest
from django.urls import reverse
from unittest.mock import patch, call, ANY , MagicMock
from django.contrib.auth.models import User

@pytest.fixture
def user(db):
    return User.objects.create_user("testuser", "test@example.com", "testpassword")

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

@pytest.mark.django_db
def test_template_rendering(client):
    client.logout()  # Ensure the test starts with an anonymous user.
    response = client.get(reverse("vfw_home:home"))
    assert response.status_code == 200, " ❌ Failed ❌ Home page did not render successfully."
    assert "vfw_home/home.html" in [t.name for t in response.templates], " ❌ Failed ❌ Home page did not use the expected template."

# @pytest.mark.xfail(reason="fixture 'mock_verify_layer' not found")
@patch("vfw_home.geoserver_layer.verify_layer")
@pytest.mark.django_db
def test_layer_name_setting_for_regular_user(client_with_user, mock_verify_layer):
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

# @pytest.mark.xfail(reason="fixture 'mock_verify_layer' not found")
# @patch("vfw_home.Geoserver.geoserver_layer.verify_layer")
# @pytest.mark.django_db
# def test_layer_verification_for_regular_user(mock_verify_layer, client_with_user):
#     print("Patch applied to:", "vfw_home.Geoserver.geoserver_layer.verify_layer"),
#     response = client_with_user.get(reverse("vfw_home:home"))
#     expected_calls = [
#         call(request=ANY, datastore="db_test", workspace="db_test", filename=response.context["data_layer"]),
#         call(request=ANY, datastore="db_test", workspace="db_test", filename=response.context["areal_data_layer"], layertype="areal_data"),
#     ]
#     print("Expected mock calls: ", expected_calls)
#     print("Actual mock calls: ", mock_verify_layer.mock_calls)
#     mock_verify_layer.assert_has_calls(expected_calls, any_order=True)
#     assert mock_verify_layer.call_count == 2, " ❌ Failed ❌ verify_layer was not called twice as expected for layer verification for a regular user."



# @pytest.mark.xfail(reason=" verify_layer mock is not recording the calls as expected ; including the mock not being \
#                    correctly applied or the calls not matching exactly due to differences in parameter order or values.")
@patch("vfw_home.views.verify_layer", autospec=True)
@pytest.mark.django_db
def test_layer_verification_for_regular_user(mock_verify_layer, client_with_user, django_db_blocker):
    with django_db_blocker.unblock():
        from vfw_home.views import HomeView

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

        

##########################
    # @patch("vfw_home.geoserver_layer.verify_layer")
# def test_layer_verification_for_regular_user(mock_verify_layer, client, create_user):
#     print("Starting test_layer_verification_for_regular_user ")
#     client.login(username="testuser", password="testpassword")
#     response = client.get(reverse("vfw_home:home"))
#     print("Response received for regular user home page : ", response)

#     expected_calls = [
#         call(
#             request=ANY,
#             datastore="db_test",
#             workspace="db_test",
#             filename=response.context["data_layer"],
#         ),
#         call(
#             request=ANY,
#             datastore="db_test",
#             workspace="db_test",
#             filename=response.context["areal_data_layer"],
#             layertype="areal_data",
#         ),
#     ]

#     print("Actual calls before assertion REGULAR: ", mock_verify_layer.mock_calls)
#     mock_verify_layer.assert_has_calls(expected_calls, any_order=True)
#     assert mock_verify_layer.call_count == 2
#     print("Regular user layer verification test passed")

#################
    
# @pytest.mark.xfail(reason="fixture 'mock_verify_layer' not found")
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

# @pytest.mark.xfail(reason="fixture 'mock_verify_layer' not found")
@patch("vfw_home.geoserver_layer.verify_layer")
@pytest.mark.django_db
def test_home_view_geoserver_unavailable(client, mock_verify_layer):
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
    assert response.status_code == 200, " ❌ Failed ❌ Page failed to load with incorrect session data format."
