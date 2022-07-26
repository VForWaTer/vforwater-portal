import requests
from django.shortcuts import render

from heron.settings import LOCAL_GEOSERVER, SECRET_GEOSERVER, MAP_SERVER, DEBUG
from wps_gui.models import WebProcessingService


def home(request):
    """
    Dummy page for Self Monitor tool.
    """
    services = {}
    rs = redis.Redis("localhost")

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

    # local 'services'
    services['DEBUG is off'] = {'runs': not DEBUG,
                                'url': 'Make sure DEBUG is only on when needed'}
    db_connection = django.db.connection.ensure_connection()
    services['Database connection'] = {'runs': True} if db_connection is None else {'runs': False}
    services['Database connection']['url'] = 'django.db.connection.ensure_connection()'

    try:
        rs.client_list()
        connected = True
    except redis.ConnectionError as e:
        connected = False
        print('Can not connect to Redis: ', e)
    services['Redis connection'] = {'runs': connected, 'url': 'redis.Redis("localhost").client_list()'}
    try:
        rs.ping()
        connected = True
    except Exception as e:
        connected = False
        print('Can not ping Redis: ', e)
    services['Redis running'] = {'runs': connected, 'url': 'redis.Redis("localhost").ping()'}

    # url tests
    services['GeoServer'] = get_status("{}/rest/about/status.json".format(LOCAL_GEOSERVER), SECRET_GEOSERVER)
    services['Map'] = get_status("{}/osm/{z}/{x}/{y}.png".format(MAP_SERVER, x=0, y=0, z=0), False)

    db_pywps = (WebProcessingService.objects.values('name', 'endpoint', 'username', 'password'))
    for pywps in db_pywps:
        services[pywps['name']] = get_status("{}?service=WPS&request=GetCapabilities".format(pywps['endpoint']),
                                             "'{}', '{}'".format(pywps['username'], pywps['password']))
        services[pywps['name'] + ' process Access'] = get_status(
            "{}?service=WPS&request=DescribeProcess&version=1.0.0&identifier=flowdurationcurve".format(
                pywps['endpoint']), "'{}', '{}'".format(pywps['username'], pywps['password']))

    return render(request, 'vfw_status/home.html', {'services': services})
