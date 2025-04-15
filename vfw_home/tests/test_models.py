import pytest
from django.urls import reverse
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from vfw_home.models import DatasourceTypes, Datasources, Datatypes, Entries
import logging
import traceback

logging.basicConfig(filename='./vfw_home/tests/logs/test_results_models.log', filemode='a', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

def log_test_start(test_name):
    logging.info(f"⭐ [STARTING TEST] ⭐: {test_name}")

def log_test_success(test_name):
    logging.info(f"✅ [TEST PASSED] ✅: {test_name}")

def log_test_failure(test_name, e):
    logging.error(f"❌ [!!! TEST FAILED !!!] ❌: {test_name}\nException: {str(e)}\nTraceback: {traceback.format_exc()}")

@pytest.fixture
def datasource_type(db):
    return DatasourceTypes.objects.create(name='test_datasource_type', title='Test Datasource Type', description='This is a test datasource type')

@pytest.mark.django_db
def test_datasource_type_creation_and_str(datasource_type):
    test_name = "test_datasource_type_creation_and_str"
    try:
        log_test_start(test_name)
        datasource_type = DatasourceTypes.objects.get(name='test_datasource_type')
        assert datasource_type.name == 'test_datasource_type'
        assert datasource_type.title == 'Test Datasource Type'
        assert str(datasource_type) == 'Data source type test_datasource_type'
        log_test_success(test_name)
    except Exception as e:
        log_test_failure(test_name, e)
        raise

@pytest.mark.django_db
def test_create_entry_with_mandatory_fields():
    test_name = "test_create_entry_with_mandatory_fields"
    try:
        log_test_start(test_name)
        entry = Entries(title="Sample Title", variable_id=1)
        entry.save()
        assert entry.title == "Sample Title"
        assert entry.variable_id == 1
        log_test_success(test_name)
    except Exception as e:
        log_test_failure(test_name, e)
        raise

@pytest.mark.django_db
def test_update_existing_entry():
    test_name = "test_update_existing_entry"
    try:
        log_test_start(test_name)
        entry = Entries(title="Sample Title", variable_id=1)
        entry.save()
        entry.title = "Updated Title"
        entry.save()
        updated_entry = Entries.objects.get(id=entry.id)
        assert updated_entry.title == "Updated Title"
        log_test_success(test_name)
    except Exception as e:
        log_test_failure(test_name, e)
        raise

@pytest.mark.django_db
def test_create_entry_with_empty_title():
    test_name = "test_create_entry_with_empty_title"
    try:
        log_test_start(test_name)
        with pytest.raises(ValidationError):
            entry = Entries(title="", variable_id=1)
            entry.full_clean()  # This will raise ValidationError for blank title
            entry.save()
        log_test_success(test_name)
    except Exception as e:
        log_test_failure(test_name, e)
        raise

@pytest.mark.django_db
def test_create_entry_with_empty_variable():
    test_name = "test_create_entry_with_empty_variable"
    try:
        log_test_start(test_name)
        with pytest.raises(IntegrityError):
            entry = Entries(title="Sample Title")
            entry.save()
        log_test_success(test_name)
    except Exception as e:
        log_test_failure(test_name, e)
        raise

@pytest.mark.django_db
def test_create_entry_with_invalid_location():
    test_name = "test_create_entry_with_invalid_location"
    try:
        log_test_start(test_name)
        with pytest.raises(ValueError):
            entry = Entries(title="Sample Title", variable_id=1, location="INVALID")
            entry.save()
        log_test_success(test_name)
    except Exception as e:
        log_test_failure(test_name, e)
        raise

@pytest.fixture
def datasource_type1(db):
    return DatasourceTypes.objects.create(name='type1', title='Type 1', description='Type 1 Description')

@pytest.fixture
def datasource_type2(db):
    return DatasourceTypes.objects.create(name='type2', title='Type 2', description='Type 2 Description')

@pytest.fixture
def datatype(db):
    return Datatypes.objects.create(name='Example Datatype', title='Example')

@pytest.mark.django_db
def test_create_datasource_with_valid_fk(datasource_type1, datatype):
    test_name = "test_create_datasource_with_valid_fk"
    try:
        log_test_start(test_name)
        datasource = Datasources.objects.create(type=datasource_type1, path='/path/to/data', datatype=datatype)
        assert datasource.type == datasource_type1
        log_test_success(test_name)
    except Exception as e:
        log_test_failure(test_name, e)
        raise

@pytest.mark.django_db
def test_update_datasource_fk_reference(datasource_type1, datasource_type2, datatype):
    test_name = "test_update_datasource_fk_reference"
    try:
        log_test_start(test_name)
        datasource = Datasources.objects.create(type=datasource_type1, path='/path/to/data', datatype=datatype)
        datasource.type = datasource_type2
        datasource.save()
        assert datasource.type == datasource_type2
        log_test_success(test_name)
    except Exception as e:
        log_test_failure(test_name, e)
        raise

@pytest.mark.django_db
def test_invalid_fk_reference(datatype):
    test_name = "test_invalid_fk_reference"
    try:
        log_test_start(test_name)
        with pytest.raises(IntegrityError):
            Datasources.objects.create(type_id=999, path='/path/to/data', datatype=datatype)
        log_test_success(test_name)
    except Exception as e:
        log_test_failure(test_name, e)
        raise

@pytest.mark.django_db
def test_cascade_delete_behavior(datasource_type1, datatype):
    test_name = "test_cascade_delete_behavior"
    try:
        log_test_start(test_name)
        datasource = Datasources.objects.create(type=datasource_type1, path='/path/to/data', datatype=datatype)
        datasource.delete()
        datasource_type1.delete()
        log_test_success(test_name)
    except Exception as e:
        log_test_failure(test_name, e)
        raise

@pytest.mark.django_db
def test_reverse_relationships(datasource_type1, datatype):
    test_name = "test_reverse_relationships"
    try:
        log_test_start(test_name)
        datasource1 = Datasources.objects.create(type=datasource_type1, path='/path/to/data1', datatype=datatype)
        datasource2 = Datasources.objects.create(type=datasource_type1, path='/path/to/data2', datatype=datatype)
        related_sources = datasource_type1.datasources_set.all()
        assert datasource1 in related_sources
        assert datasource2 in related_sources
        log_test_success(test_name)
    except Exception as e:
        log_test_failure(test_name, e)
        raise
