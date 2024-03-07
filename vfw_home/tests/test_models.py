# from django.test import TestCase
# # from .test_logger import log_test_result
# from django import setup
# import django
# import os
# import logging
# import traceback
# from django.db import IntegrityError
# from django.core.exceptions import ValidationError
# from vfw_home.models import DatasourceTypes, Datasources, Datatypes, Entries

# # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "heron.settings")
# # django.setup()
# # logger = logging.getLogger(__name__)  
# logging.basicConfig(filename='./vfw_home/tests/logs/test_results_models.log', filemode='a', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')


# def log_test_start( test_name):
#     logging.info(f"⭐ [STARTING TEST] ⭐: {test_name}")

# def log_test_success( test_name):
#     logging.info(f"✅ [TEST PASSED] ✅: {test_name}")

# def log_test_failure(test_name, e):
#     logging.error(f"❌ [!!! TEST FAILED !!!] ❌: {test_name}\nException: {str(e)}\nTraceback: {traceback.format_exc()}")


# class DatasourceTypesTest(TestCase):
    
#     def setUp(self):
#         DatasourceTypes.objects.create(name='test_datasource_type', title='Test Datasource Type', description='This is a test datasource type')


#     def test_datasource_type_creation_and_str(self):
#         """
#         Test creating a DatasourceTypes instance and its string representation.

#         This test verifies that a DatasourceTypes instance can be created with the required fields
#         and that its string representation matches the expected format.
#         """
#         test_name = "test_datasource_type_creation_and_str"
#         try:
#             log_test_start(test_name)
#             datasource_type = DatasourceTypes.objects.get(name='test_datasource_type')
#             self.assertEqual(datasource_type.name, 'test_datasource_type')
#             self.assertEqual(datasource_type.title, 'Test Datasource Type')
#             self.assertEqual(str(datasource_type), f'Data source type test_datasource_type')
#             log_test_success(test_name)
#         except Exception as e:
#             log_test_failure(test_name, e)
#             raise
        
# class EntriesTest(TestCase):
    


#     def test_create_entry_with_mandatory_fields(self):
#         """
#         Test creating an entry with only the mandatory fields.

#         This test creates an entry with only the title and variable_id fields, and then
#         verifies that the entry was created successfully.
#         """
#         test_name = "test_create_entry_with_mandatory_fields"
#         try:
#             log_test_start(test_name)
#             entry = Entries(title="Sample Title", variable_id=1)
#             entry.save()
#             self.assertEqual(entry.title, "Sample Title")
#             self.assertEqual(entry.variable_id, 1)
#             log_test_success(test_name)
#         except Exception as e:
#             log_test_failure(test_name, e)
#             raise

#     def test_update_existing_entry(self):
#         """
#         Test updating an existing entry.

#         This test creates an entry with the mandatory fields, 
#         and then updates the entry with a new title.
#         It then verifies that the entry was updated successfully.
#         """

#         test_name = "test_update_existing_entry"

#         try:
#             log_test_start(test_name)
#             entry = Entries(title="Sample Title", variable_id=1)
#             entry.save()
#             entry.title = "Updated Title"
#             entry.save()
#             updated_entry = Entries.objects.get(id=entry.id)
#             self.assertEqual(updated_entry.title, "Updated Title")
#             log_test_success(test_name)
#         except Exception as e:
#             log_test_failure(test_name, e)
#             raise

        
#     def test_create_entry_with_empty_title(self):
#         """
#         Test creating an entry with an empty title.

#         This test creates an entry with an empty title and an existing variable,
#         and then verifies that a ValidationError is raised.
#         """
#         test_name = "test_create_entry_with_empty_title"
#         try:
#             log_test_start(test_name)
#             with self.assertRaises(ValidationError):
#                 entry = Entries(title="", variable_id=1)
#                 entry.full_clean()  # This will raise ValidationError for blank title
#                 entry.save()
#             log_test_success(test_name)
#         except Exception as e:
#             log_test_failure(test_name, e)
#             raise

#     def test_create_entry_with_empty_variable(self):
#         """
#         Test creating an entry with an empty title.

#         This test creates an entry with an empty title and an existing variable,
#         and then verifies that a ValidationError is raised.
#         """
#         test_name = "test_create_entry_with_empty_variable"
#         try:
#             log_test_start(test_name)
#             with self.assertRaises(IntegrityError):
#                 entry = Entries(title="Sample Title")
#                 entry.save()
#             log_test_success(test_name)
#         except Exception as e:
#             log_test_failure(test_name, e)
#             raise



#     def test_create_entry_with_invalid_location(self):
#         """
#         Test creating an entry with an invalid location.

#         This test creates an entry with a sample title and variable, and an invalid location,
#         and then verifies that a ValueError is raised.
#         """
#         test_name = "test_create_entry_with_invalid_location"
#         try:
#             log_test_start(test_name)
#             with self.assertRaises(ValueError):
#                 entry = Entries(title="Sample Title", variable_id=1, location="INVALID")
#                 entry.save()
#             log_test_success(test_name)
#         except Exception as e:
#             log_test_failure(test_name, e)
#             raise





# class ForeignKeyTests(TestCase):
    
#     def setUp(self):
#         self.type1 = DatasourceTypes.objects.create(name='type1', title='Type 1', description='Type 1 Description')
#         self.type2 = DatasourceTypes.objects.create(name='type2', title='Type 2', description='Type 2 Description')
#         self.datatype = Datatypes.objects.create(name='Example Datatype', title='Example')

#     def test_create_datasource_with_valid_fk(self):
#         """
#         Test creating a datasource with a valid foreign key reference.

#         This test creates a datasource with a foreign key reference to an existing datasource type,
#         and then verifies that the datasource was created successfully.
#         """
#         test_name = "test_create_datasource_with_valid_fk"
#         try:
#             log_test_start(test_name)
#             datasource = Datasources.objects.create(type=self.type1, path='/path/to/data', datatype=self.datatype)
#             self.assertEqual(datasource.type, self.type1)
#             log_test_success(test_name)
#         except Exception as e:
#             log_test_failure(test_name, e)
#             raise

#     def test_update_datasource_fk_reference(self):
#         """
#         Test updating a datasource's foreign key reference.

#         This function creates a datasource with a foreign key reference to a datasource type,
#         updates the datasource's foreign key reference to a different datasource type, and then
#         verifies that the datasource was updated successfully.
#         """
#         test_name = "test_update_datasource_fk_reference"
#         try:
#             log_test_start(test_name)
#             datasource = Datasources.objects.create(type=self.type1, path='/path/to/data' , datatype=self.datatype)
#             datasource.type = self.type2
#             datasource.save()
#             self.assertEqual(datasource.type, self.type2)
#             log_test_success(test_name)
#         except Exception as e:
#             log_test_failure(test_name, e)
#             raise

#     def test_invalid_fk_reference(self):
#         """
#         Test creating a datasource with an invalid foreign key reference.

#         This test creates a datasource with an invalid foreign key reference to a non-existent datasource type,
#         and then verifies that a ValueError is raised.
#         """
#         test_name = "test_invalid_fk_reference"
#         try:
#             log_test_start(test_name)
#             with self.assertRaises(django.db.utils.IntegrityError):
#                 Datasources.objects.create(type_id=999, path='/path/to/data', datatype=self.datatype)
#             log_test_success(test_name)
#         except Exception as e:
#             log_test_failure(test_name, e)
#             raise

#     def test_cascade_delete_behavior(self):
#         """
#         Test that deleting a parent object cascades and deletes child objects.

#         This test creates a Datasource instance and then deletes its associated DatasourceType.
#         It verifies that the Datasource instance was deleted and that the DatasourceType instance
#         was also deleted.
#         """
        

#         test_name = "test_cascade_delete_behavior"
#         try:
#             log_test_start(test_name)

#             datasource = Datasources.objects.create(type=self.type1, path='/path/to/data', datatype=self.datatype)

#             datasource.delete()

#             self.type1.delete()

#             log_test_success(test_name)
#         except Exception as e:
#             log_test_failure(test_name, e)
#             raise




#     def test_reverse_relationships(self):
#         """
#         Test the reverse relationship between Datasource and DatasourceType.

#         This function creates two Datasource instances with the same DatasourceType, and then
#         retrieves the DatasourceType's Datasource instances using the reverse relationship.
#         It verifies that both Datasource instances are included in the result set.
#         """
#         test_name = "test_reverse_relationships"
#         try:
#             log_test_start(test_name)
#             datasource1 = Datasources.objects.create(type=self.type1, path='/path/to/data1', datatype=self.datatype)
#             datasource2 = Datasources.objects.create(type=self.type1, path='/path/to/data2', datatype=self.datatype)
#             related_sources = self.type1.datasources_set.all()
#             self.assertIn(datasource1, related_sources)
#             self.assertIn(datasource2, related_sources)
#             log_test_success(test_name)
#         except Exception as e:
#             log_test_failure(test_name, e)
#             raise


