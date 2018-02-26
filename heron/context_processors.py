from django.conf import settings


def global_settings(request):
    # return any necessary values
    return {
        'HOST_NAME': settings.HOST_NAME,
        'VFW_SERVER': settings.VFW_SERVER,  # TODO: Are you serious!?! You get a value from settings and make it
        'MAP_SERVER': settings.MAP_SERVER,
        'DEMO_VAR': settings.DEMO_VAR,
        # again available for settings?!?
}