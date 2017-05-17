class VforwaterRouter(object):
    """
    Determine how to route database calls for an app's models.
    All other models will be routed to the next router in the DATABASE_ROUTERS setting if applicable,
    or otherwise to the default database.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'vfwheron':
            return 'vforwater'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'vfwheron':
            return 'vforwater'
        return None

    def allow_relation(self, obj1, obj2, **hints):

        # Allow any relation between two models that are both in the vfwheron app.
        if obj1._meta.app_label == 'vfwheron' and obj2._meta.app_label == 'vfwheron':
            return True
        # No opinion if neither object is in the Example app (defer to default or other routers).
        elif 'vfwheron' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return None

        # Block relationship if one object is in the Example app and the other isn't.
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure that the app's models get created on the right database."""
        if app_label == 'vfwheron':
            # The Example app should be migrated only on the example_db database.
            return db == 'vforwater'

        # No opinion for all other scenarios
        return None
