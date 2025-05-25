from django.conf import settings
from vfw_home.Figure.datatypes import datatypes, basicdatatypes


def global_settings(request):
    """

    @param request:
    @type request:
    @return:
    @rtype:
    """
    return {
        'HOST_NAME': settings.HOST_NAME,
        'VFW_SERVER': settings.VFW_SERVER,
        'MAP_SERVER': settings.MAP_SERVER,
        'DEMO_VAR': settings.DEMO_VAR,
        'EXT_DATATYPES': datatypes,
        'BASE_DATATYPES': basicdatatypes,
        }
