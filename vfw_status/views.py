import requests
from django.shortcuts import render

from heron.settings import LOCAL_GEOSERVER, SECRET_GEOSERVER, MAP_SERVER, DEBUG
from wps_gui.models import WebProcessingService


def home(request):
    """
    Dummy page for Self Monitor tool.
    """
    services = {}

    def get_status(url, secret):
        checked_service = {'runs': False}
        if secret:
            check = requests.get(url, auth=eval(secret), headers={"Accept": "application/json"})
        else:
            check = requests.get(url, headers={"Accept": "application/json"})

        if check.status_code == 200:
            checked_service['runs'] = True

        checked_service['code'] = check.status_code
        checked_service['url'] = url

        return checked_service

    services['DEBUG is off'] = {'runs': not DEBUG, 'code': '¡666!' if DEBUG else '',
                                'url': 'Make sure DEBUG is only on when needed'}

    services['GeoServer'] = get_status("{}/rest/about/status.json".format(LOCAL_GEOSERVER), SECRET_GEOSERVER)
    services['Map'] = get_status("{}/osm/{z}/{x}/{y}.png".format(MAP_SERVER, x=0, y=0, z=0), False)

    db_pywps = (WebProcessingService.objects.values('name', 'endpoint', 'username', 'password'))
    for pywps in db_pywps:
        services[pywps['name']] = get_status("{}?service=WPS&request=GetCapabilities".format(pywps['endpoint']),
                                             "'{}', '{}'".format(pywps['username'], pywps['password']))
        # services[pywps['name'] + ' process Access'] = get_status(
        #     "{}?service=WPS&request=DescribeProcess&version=1.0.0&identifier=flowdurationcurve".format(
        #         pywps['endpoint']), "'{}', '{}'".format(pywps['username'], pywps['password']))

    return render(request, 'vfw_status/home.html', {'services': services})
