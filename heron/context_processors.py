from django.conf import settings
from vfw_home.Figure.datatypes import datatypes, basicdatatypes


# TODO: document
def global_settings(request):
    """

    @param request:
    @type request:
    @return:
    @rtype:
    """
    # return any necessary values
    return {
        'HOST_NAME': settings.HOST_NAME,
        'VFW_SERVER': settings.VFW_SERVER,  # TODO: Are you serious!?! You get a value from settings and make it
        # again available for settings?!?
        'MAP_SERVER': settings.MAP_SERVER,
        # 'PORTAL_GEOSERVER': settings.PORTAL_GEOSERVER,
        'DEMO_VAR': settings.DEMO_VAR,
        'EXT_DATATYPES': datatypes,
        'BASE_DATATYPES': basicdatatypes,
        }
