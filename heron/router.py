# Based on http://diegobz.net/2011/02/10/django-database-router-using-settings/

from . import settings


class DatabaseRouter(object):
    """
    A router to control all database operations on models for different
    databases.

    In case an app is not set in settings.DATABASE_APPS_MAPPING, the router
    will fallback to the `default` database.

    Settings example:

    DATABASE_APPS_MAPPING = {'app1': 'db1', 'app2': 'db2'}
    """

# TODO: document

    def db_for_read(self, model, **hints):
        """
        Point all read operations to the specific database.

        @param model:
        @type model:
        @param hints:
        @type hints:
        @return:
        @rtype:
        """
        if model._meta.app_label in settings.DATABASE_APPS_MAPPING:
            return settings.DATABASE_APPS_MAPPING[model._meta.app_label]
        return None

    def db_for_write(self, model, **hints):
        """
        Point all write operations to the specific database.
        @param model:
        @type model:
        @param hints:
        @type hints:
        @return:
        @rtype:
        """
        if model._meta.app_label in settings.DATABASE_APPS_MAPPING:
            return settings.DATABASE_APPS_MAPPING[model._meta.app_label]
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow any relation between apps that use the same database.
        @param obj1:
        @type obj1:
        @param obj2:
        @type obj2:
        @param hints:
        @type hints:
        @return:
        @rtype:
        """
        db_obj1 = settings.DATABASE_APPS_MAPPING.get(obj1._meta.app_label)
        db_obj2 = settings.DATABASE_APPS_MAPPING.get(obj2._meta.app_label)
        if db_obj1 and db_obj2:
            return db_obj1 == db_obj2
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure that apps only appear in the related database.
        @param db:
        @type db:
        @param app_label:
        @type app_label:
        @param model_name:
        @type model_name:
        @param hints:
        @type hints:
        @return:
        @rtype:
        """
        if db in settings.DATABASE_APPS_MAPPING.values():
            return settings.DATABASE_APPS_MAPPING.get(app_label) == db
        elif app_label in settings.DATABASE_APPS_MAPPING:
            return False
        return None
