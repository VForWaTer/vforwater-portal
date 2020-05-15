from urllib.error import HTTPError, URLError

from owslib.wps import WebProcessingService
from .models import WebProcessingService as WpsModel
from heron.settings import VFW_SERVER, wps_log


def abstract_is_link(process):
    """
    Determine if the process abstract is a link.

    Args:
      process (owslib.wps.Process): WPS Process object.

    Returns:
      (bool): True if abstract is a link, False otherwise.
    """
    try:
        abstract = process.abstract
    except AttributeError:
        return False

    if abstract[:4] == 'http':
        return True

    else:
        return False


def activate_wps(wps, endpoint, name):
    """
    Activate a WebProcessingService object by calling getcapabilities() on it and handle errors appropriately.

    Args:
      wps (owslib.wps.WebProcessingService): A owslib.wps.WebProcessingService object.

    Returns:
      (owslib.wps.WebProcessingService): Returns an activated WebProcessingService object or None if it is invalid.
    :param wps:
    :type wps:
    :param endpoint:
    :type endpoint:
    :param name:
    :type name:
    """
    # Initialize the object with get capabilities call
    try:
        wps.getcapabilities()
    except HTTPError as e:
        if e.code == 404:
            e.msg = 'The WPS service could not be found at given endpoint "{0}" for site WPS service ' \
                    'named "{1}". Check the configuration of the WPS service in your ' \
                    'settings.py.'.format(endpoint, name)
            wps_log.debug('Error in activate_wps wps.getcapabilities(): {1] '.format(e))
            raise e
        else:
            wps_log.debug('Error in activate_wps wps.getcapabilities(): {1] '.format(e))
            raise e
    except URLError as e:
        wps_log.debug(e)
        return None
    except:
        raise

    return wps


def list_wps_service_engines(app_class=None):
    """
    Get all wps engines offered.

    Args:
      app_class (class, optional): The app class to include in the search for wps engines.

    Returns:
      (tuple): A tuple of WPS engine dictionaries.
    """
    # Init vars
    wps_services_list = []

    # If the app_class is given, check it first for a wps engine
    app_wps_services = None

    if app_class and issubclass(app_class):
        #         Instantiate app class and retrieve wps services list
        app = app_class()
        app_wps_services = app.wps_services()

    if app_wps_services:
        # Search for match
        for app_wps_service in app_wps_services:
            wps = WebProcessingService(app_wps_service.endpoint,
                                       username=app_wps_service.username,
                                       password=app_wps_service.password,
                                       verbose=False,
                                       skip_caps=True)

            activated_wps = activate_wps(wps=wps, endpoint=app_wps_service.endpoint, name=app_wps_service.name)

            if activated_wps:
                wps_services_list.append(activated_wps)

    # If no wps_services are known yet check for port 8090 to 8099
    if not WpsModel.objects.all():
        find_wps_service_engines()

    # If the wps engine cannot be found in the app_class, check settings for site-wide wps engines
    site_wps_services = WpsModel.objects.all()

    for site_wps_service in site_wps_services:

        # Create OWSLib WebProcessingService engine object
        wps = WebProcessingService(site_wps_service.endpoint,
                                   username=site_wps_service.username,
                                   password=site_wps_service.password,
                                   verbose=False,
                                   skip_caps=True)

        # Initialize the object with get capabilities call
        activated_wps = activate_wps(wps=wps,
                                     endpoint=site_wps_service.endpoint,
                                     name=site_wps_service.name)

        if activated_wps:
            wps_services_list.append(activated_wps)

    return wps_services_list


def get_wps_service_engine(name, app_class=None):
    """
    Get a wps engine with the given name.

    Args:
      name (string): Name of the wps engine to retrieve.
      app_class (class, optional): The app class to include in the search for wps engines.

    Returns:
      (owslib.wps.WebProcessingService): A owslib.wps.WebProcessingService object.
    """
    # If the app_class is given, check it first for a wps engine
    app_wps_services = None

    if app_class and issubclass(app_class):
        # Instantiate app class and retrieve wps services list
        app = app_class()
        app_wps_services = app.wps_services()

    if app_wps_services:
        # Search for match
        for app_wps_service in app_wps_services:

            # If match is found, initiate engine object
            if app_wps_service.name == name:
                wps = WebProcessingService(app_wps_service.endpoint,
                                           username=app_wps_service.username,
                                           password=app_wps_service.password,
                                           verbose=False,
                                           skip_caps=True)

                return activate_wps(wps=wps, endpoint=app_wps_service.endpoint, name=app_wps_service.name)

    # If the wps engine cannot be found in the app_class, check database for site-wide wps engines
    site_wps_services = WpsModel.objects.all()

    if site_wps_services:
        # Search for match
        for site_wps_service in site_wps_services:

            # If match is found initiate engine object
            if site_wps_service.name == name:
                # Create OWSLib WebProcessingService engine object
                wps = WebProcessingService(site_wps_service.endpoint,
                                           username=site_wps_service.username,
                                           password=site_wps_service.password,
                                           verbose=False,
                                           skip_caps=True)

                # Initialize the object with get capabilities call
                return activate_wps(wps=wps, endpoint=site_wps_service.endpoint, name=site_wps_service.name)

    error_msg = ('Could not find wps service with name "{0}". Please check that a wps service with that name '
                    'exists in the admin console or in your app.py.'.format(name))
    wps_log.debug(error_msg)
    raise NameError(error_msg)


def find_wps_service_engines():

    try:
        # wps_address = 'http://localhost:5000/wps'
        wps_address = VFW_SERVER + '/wps'

        wps_service = WebProcessingService(wps_address,
                                           verbose=False,
                                           skip_caps=True)
        wps_service.getcapabilities()

        new_data = WpsModel(name=wps_service.identification.title,
                            endpoint=wps_address)
        new_data.save()

    except:
        wps_log.debug('--- Exception in utilities.py, find_wps_service_engines. (Maybe no WPS_Service at port 8094.) ---')
        print('--- No WPS_Service at port 8094. ---')
