import pytest
from unittest.mock import patch, MagicMock
from django.contrib.auth.models import User
from author_manage.models import Profile, __assign_data, Resource
from vfw_home.models import  Persons
import logging
import traceback




@pytest.mark.django_db
def test_assign_data_no_matching_person():
    # Create a test user with no matching Person entries
    user = User.objects.create(username='testuser', first_name='NoMatch', last_name='User')
    profile = Profile.objects.create(user=user)

    with patch("author_manage.models.logger") as mock_logger:
        __assign_data(user, profile)

        # Ensure profile checkedAssociation is set to True
        profile.refresh_from_db()
        assert profile.checkedAssociation is True
        assert profile.metacatalogPerson is None  # No person should be associated

        # Verify log entry for no matching person found
        mock_logger.info.assert_called_once_with(f"No persons found in metacatalog matching user '{user}'.")

