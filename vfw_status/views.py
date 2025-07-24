import django
import requests
from django.shortcuts import render

from heron.settings import LOCAL_GEOSERVER, SECRET_GEOSERVER, MAP_SERVER, DEBUG
from wps_gui.models import WebProcessingService
from vfw_home.utilities.utilities import raise_logging_exception, logger
from django.views import View

import redis

try:
    from heron.settings import REDIS_HOST
except:
    REDIS_HOST = 'localhost'
try:
    from heron.settings import REDIS_PORT
except:
    REDIS_PORT = 6379
try:
    from heron.settings import REDIS_DB
except:
    REDIS_DB = 0




class HomeStatusView(View):

    def get(self, request):

        endpoint = request.path

        try:
            services = {}
            
            services['DEBUG is off'] = {'runs': not DEBUG,
                                    'url': 'Make sure DEBUG is only on when needed'}
            
            services['Database connection'] = self.check_database(endpoint)

            services.update(self.check_redis(endpoint))

            services['GeoServer'] = get_status("{}/rest/about/status.json".format(LOCAL_GEOSERVER), endpoint, SECRET_GEOSERVER)
            services['Map'] = get_status("{}/osm/{z}/{x}/{y}.png".format(MAP_SERVER, x=0, y=0, z=0), endpoint, False)

            db_pywps = (WebProcessingService.objects.values('name', 'endpoint', 'username', 'password'))
            for pywps in db_pywps:
                services[pywps['name']] = get_status("{}?service=WPS&request=GetCapabilities".format(pywps['endpoint']), endpoint,
                                                    "'{}', '{}'".format(pywps['username'], pywps['password']))
                services[pywps['name'] + ' process Access'] = get_status(
                    "{}?service=WPS&request=DescribeProcess&version=1.0.0&identifier=flowdurationcurve".format(
                        pywps['endpoint']), endpoint, "'{}', '{}'".format(pywps['username'], pywps['password']))

            return render(request, 'vfw_status/home.html', {'services': services})

        except Exception as e :

            raise_logging_exception(e, endpoint ,'Can not ping Redis')


    @classmethod
    def check_database(cls, endpoint):

        try:
            db_connection = django.db.connection.ensure_connection()
            if db_connection is None:
                return {'runs': True, 'url': 'django.db.connection.ensure_connection()'}
            else:
                return {'runs': False, 'url': 'django.db.connection.ensure_connection()'}

        except Exception as e:

            raise_logging_exception(e, endpoint , "Database connection failed")

            return {'runs': False, 'url': 'Database connection failed'}



    @classmethod
    def check_redis(cls, endpoint):

        rs = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        services = {}

        try:
            rs.ping()
            connected = True

        except Exception as e:
            connected = False
            raise_logging_exception(e, endpoint ,'Can not ping Redis')

        services['Redis connection'] = {'runs': connected, 'url': 'redis.Redis(host={}, port={}, db={}).ping()'.format(REDIS_HOST, REDIS_PORT, REDIS_DB)}

        try:
            rs.client_list()
            connected = True
        except redis.ConnectionError as e:
            connected = False
            raise_logging_exception(e, endpoint , 'Can not connect to Redis')

        services['Redis running'] = {'runs': connected, 'url': 'redis.Redis(host={}, port={}, db={}).client_list()'.format(REDIS_HOST, REDIS_PORT, REDIS_DB)}

        return services


    @classmethod
    def get_status(cls, url, endpoint,  secret=None):
        checked_service = {'runs': False}

        try:
            headers = {"Accept": "application/json"}
            auth = eval(secret) if secret else None
            response = requests.get(url, auth=auth, headers=headers)

            if response.status_code == 200:
                checked_service['runs'] = True

            checked_service['code'] = response.status_code
            checked_service['url'] = url

        except requests.RequestException as e:
            raise_logging_exception(e, endpoint , f"Error connecting to {url}: {e}")
            checked_service['code'] = "Error"
            checked_service['url'] = url


        return checked_service


