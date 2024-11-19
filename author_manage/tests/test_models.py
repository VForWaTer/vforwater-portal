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


@pytest.mark.django_db
def test_assign_data_single_matching_person():
    # Create a test user and a matching Person entry
    user = User.objects.create(username='testuser', first_name='Match', last_name='User')
    person = Persons.objects.create(first_name='Match', last_name='User')
    profile = Profile.objects.create(user=user)

    with patch("author_manage.models.logger") as mock_logger:
        __assign_data(user, profile)

        # Ensure profile is associated with the person and checkedAssociation is True
        profile.refresh_from_db()
        assert profile.checkedAssociation is True
        assert profile.metacatalogPerson == person  # Should associate with the matching person

        # No warning logs should be present for single match
        mock_logger.warning.assert_not_called()


@pytest.mark.django_db
def test_assign_data_multiple_matching_persons():
    # Create a test user and multiple matching Person entries
    user = User.objects.create(username='testuser', first_name='Multiple', last_name='User')
    person1 = Persons.objects.create(first_name='Multiple', last_name='User')
    person2 = Persons.objects.create(first_name='Multiple', last_name='User')  # Second matching person
    profile = Profile.objects.create(user=user)

    with patch("author_manage.models.logger") as mock_logger:
        __assign_data(user, profile)

        # Ensure profile is associated with the first person match and checkedAssociation is True
        profile.refresh_from_db()
        assert profile.checkedAssociation is True
        assert profile.metacatalogPerson == person1  # Should associate with the first match by default

        # Verify that a warning was logged for multiple matches
        mock_logger.warning.assert_called_once_with(
            f"Multiple persons found for user '{user}'. Associating with the first match."
        )


@pytest.mark.django_db
def test_assign_data_existing_association():
    # Create a test user and matching Person entry with an existing Profile
    user = User.objects.create(username='testuser', first_name='Associated', last_name='User')
    person = Persons.objects.create(first_name='Associated', last_name='User')
    existing_profile = Profile.objects.create(user=user, metacatalogPerson=person, checkedAssociation=True)

    # Call the __assign_data function on an already-associated profile
    with patch("author_manage.models.logger") as mock_logger:
        __assign_data(user, existing_profile)

        # Ensure profile remains associated and checkedAssociation is True
        existing_profile.refresh_from_db()
        assert existing_profile.checkedAssociation is True
        assert existing_profile.metacatalogPerson == person  # Association remains intact

        # Expect a warning log that the person is already linked
        mock_logger.warning.assert_called_once_with(f"The person '{person}' is already linked to another profile.")