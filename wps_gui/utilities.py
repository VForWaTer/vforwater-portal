# =================================================================
#
# Authors: Marcus Strobl <marcus.strobl@gmx.de>
# Contributors: Safa Bouguezzi <safa.bouguezzi@kit.edu>
#
# Copyright (c) 2024 Marcus Strobl
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

import ast
import datetime
import json
import jsonpickle
import numbers
import re
import requests

from os import path
from pathlib import Path
from urllib.error import HTTPError, URLError

from django.http import Http404, JsonResponse

from django.utils import timezone
from django.utils.timezone import make_aware

from owslib.ogcapi import Collections
from owslib.util import Authentication
from owslib.wps import WebProcessingService

from vfw_home.Figure.data_obj import DataObject
from vfw_home.Figure.datatypes import basicdatatypes, datatypes
from vfw_home.views import get_accessible_data
from .models import WebProcessingService as WpsModel, GeoAPIResults
from .models import WpsResults
from owslib.ogcapi.processes import Processes as ogcProcesses
from heron.settings import VFW_GEOAPI, wps_log, PROCESSES_IN_DIR, PROCESSES_OUT_DIR, DEBUG
import logging
logger = logging.getLogger(__name__)


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
    except Exception as e:
        # print('Impossible to activate wps. Unexpected error: ', e)
        return None

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
        wps_address = VFW_SERVER + '/wps'

        wps_service = WebProcessingService(wps_address,
                                           verbose=False,
                                           skip_caps=True)
        wps_service.getcapabilities()

        new_data = WpsModel(name=wps_service.identification.title,
                            endpoint=wps_address)
        new_data.save()

    except:
        wps_log.debug(
            '--- Exception in utilities.py, find_wps_service_engines. (Maybe no WPS_Service at port 8094.) ---')
        print('--- No WPS_Service at port 8094. ---')


def get_endpoint_data(devel=False):
    """
    Use this funciton to get the correct endpoint (URL) for the geoapi, depending if in development (has endpoint in
    settings) or for production/demo (database)
    :param devel:
    :return: service, endpoint, wps_services
    """
    try:
        wps_services = list(WpsModel.objects.values_list("name", flat=True))
        wps_services_url = list(WpsModel.objects.values_list('endpoint', flat=True))
        service = wps_services[0]  # pygeoapi_vforwater

        if not devel:
            endpoint = wps_services_url[0]  # http://geoapi:5000/
        else:
            endpoint = VFW_GEOAPI
    except Exception as e:
        print("Exception in wps_gui.utilities: {}, service: {}, endpoint: {}".format(e, service, endpoint))
    return service, endpoint, wps_services


def get_process_basics(apiprocess):
    """
    Get a JSON description from a GeoApi process and return basic infos as needed for the toolbox buttons.
    Button data is loaded all at once, so only load needed info, not everything to reduce upload time of workspace and
    improve performance.

    :param apiprocess: complete json of GeoApi
    """
    inputs = {}
    outputs = {}
    for k, v in apiprocess['inputs'].items():
        if 'format' in v['schema']:
            inputs[k] = f"{v['schema']['type']} {v['schema']['format']}"
        else:
            inputs[k] = v['schema']['type']

    for k, v in apiprocess['outputs'].items():
        if 'format' in v['schema']:
            outputs[k] = f"{v['schema']['type']} {v['schema']['format']}"
        else:
            outputs[k] = v['schema']

    return {
        "id": apiprocess['id'],
        "title": apiprocess['title'],
        "description": apiprocess['description'][0:100],  # process.abstract,
        "keywords": apiprocess['keywords'],
        "inputs": json.dumps(inputs),
        "outputs": json.dumps(outputs),
    }


def get_process_info(apiprocess):
    """
    Get a JSON description from a GeoApi process and return complete infos as needed for the toolbox.

    :param apiprocess: complete json of GeoApi
    """
    return {
        "description": apiprocess['description'],  # process.abstract,
        "example": apiprocess['example'],
        "id": apiprocess['id'],
        "identifier": apiprocess['id'],
        "inputs": add_required(apiprocess['inputs']),
        "dataInputs": geoapi_input2wps_datainput(apiprocess['inputs']),
        "outputs": apiprocess['outputs'],
        "processOutputs": geoapi_output2wps_processoutput(apiprocess['outputs']),
        "keywords": apiprocess['keywords'],
        "title": apiprocess['title'],
        "version": apiprocess['version'],
    }


def get_user_results(user_id):
    try:
        results = list(GeoAPIResults.objects.filter(owner_id=user_id).exclude(owner_id__isnull=True).
                       values("id", "inputs", "outputs", "name", "open", "status"))
    except GeoAPIResults.DoesNotExist:
        logger.error('Cannot get user results. There is an issue with the GeoAPIResults model.')
        results = []

    return results



def geoapi_output2wps_processoutput(outputs):
    """
    Change input object as needed for the dropbox in the workspace.
    :param inputs:
    :return:
    """
    dataoutputs = []

    for k, v in outputs.items():
        v['identifier'] = k
        v['dataType'] = v['schema']['type']

        if 'keywords' in v:
            v['keywords'].append(v['schema']['type'])
        else:
            v['keywords'] = []

        if 'contentMediaType' in v['schema'] and v['schema']['type'] == 'object':
            if 'json' in v['schema']['contentMediaType']:
                v['keywords'].append("json")
                v['dataType'] = "json"
            else:
                v['keywords'].append(v['schema']['type'])

        dataoutputs.append(v)

    return dataoutputs


def geoapi_input2wps_datainput(inputs):
    """
    Change input object as needed for the dropbox in the workspace.
    :param inputs:
    :return:
    """
    datainputs = []

    for k, v in inputs.items():
        v['identifier'] = k
        v['dataType'] = v['schema']['type']
        if 'keywords' in v:
            v['keywords'].append(v['schema']['type'])

        datainputs.append(v)

    return datainputs


def add_required(inputs):
    """
    Depending on datatyp (bool) and minOccurs(>0) add a required flag to the input.
    :param inputs: dict
    :return:
    """
    for k, v in inputs.items():
        if 'schema' in v and 'required' in v['schema'] and v['schema']['required'] == 'true' \
            or 'minOccurs' in v and v['minOccurs'] > 0 \
            and 'type' in v['schema'] and v['schema']['type'] != 'boolean' and v['schema']['type'] != 'bool':
            inputs[k]['required'] = True
        else:
            inputs[k]['required'] = False

    return inputs



class ogcCollections(Collections):
    """Abstraction for OGC API - Processes"""

    def __init__(self, url: str, json_: str = None, timeout: int = 30,
                 headers: dict = None, auth: Authentication = None):
        __doc__ = Collections.__doc__  # noqa
        super().__init__(url, json_, timeout, headers, auth)

    def processes(self) -> list:
        """
        implements /processes
        @returns: `list` of available processes
        """

        path = 'processes'
        return self._request(path=path)['processes']

    def process(self, process_id: str) -> dict:
        """
        implements /processs/{processId}
        @type process_id: string
        @param process_id: id of process
        @returns: `dict` of process desceription
        """

        path = f'processes/{process_id}'
        return self._request(path=path)


def create_geoapi_db_entry(db_data: object, user=None, error=False) -> object:
    """
    Create a database entry.
    :param db_data: dict of input identifier of wps and respective value (e.g. a path)
    :param user: user object to create foreign key
    """
    lookup = {
        'inputs': db_data['inputs'],
        'name': db_data['name'],
        'open': db_data['open'],
        'outputs': db_data['outputs'],
        'status': db_data['status'],
    }  # , access=timezone.now())
    if user is not None:
        lookup['owner'] = user

    try:
        obj, created = GeoAPIResults.objects.get_or_create(**lookup)
    except Exception as e:
        print('Cannot create GeoAPIResult: ', e)

    if created:
        return {'id': obj.id, 'obj': obj, 'created': created, 'error': error}
    else:
        return {'error': error, 'obj': obj}


def create_wpsdb_entry(wps_process: str, invalue: list, outputs: object) -> object:
    """
    Create a database entry.
    :param wps_process: identifier of the wps process
    :param invalue: dict of input identifier of wps and respective value (e.g. a path)
    :param outputs: dict of output or a path
    """
    obj, created = WpsResults.objects.get_or_create(
        open=False,
        wps=wps_process,
        inputs=invalue,
        outputs=outputs,
        creation=timezone.now(),
    )  # , access=timezone.now())
    if created:
        return {'id': obj.id}
    else:
        return {'id': 'error while creating db entry.'}


def edit_input(inputs):
    """

    :param inputs:
    :return: list of tuples, each tuple a pair of wps_input_identifier and its value
    """

    def filepath(fid):
        pass

    wps_input = []
    for key_value in inputs:
        if key_value[1] is None and not (
            key_value[0] == "start" or key_value[0] == "end"
        ):
            wps_input.append((key_value[0], key_value[2]))
        elif isinstance(key_value[1], list):
            for value, type_value in zip(key_value[1], key_value[2]):
                if type_value in datatypes:
                    if value[0:3] == 'wps':
                        ast.literal_eval(WpsResults.objects.get(id=value[3:]).outputs)['path']
                        wps_input.append((key_value[0],
                                          ast.literal_eval(WpsResults.objects.get(id=value[3:]).outputs)['path']))
                    else:
                        wps_input.append((key_value[0],
                                          ast.literal_eval(WpsResults.objects.get(id=value[5:]).outputs)[0]))
        elif isinstance(key_value[1], bool) or isinstance(key_value[1], numbers.Number):
            wps_input.append((key_value[0], str(key_value[1])))
        elif key_value[1][0:2] == "db" and key_value[1][2:].isdecimal():
            wps_input.append((key_value[0], key_value[1][2:]))
        elif key_value[1][0:3] == 'wps' and key_value[1][3:].isdecimal():
            wps_input.append((key_value[0],
                              ast.literal_eval(WpsResults.objects.get(id=key_value[1][3:]).outputs)['path']))
        elif key_value[0] == 'start' or key_value[0] == 'end':
            if key_value[1] != 'None':
                wps_input.append((key_value[0], make_aware(
                    value=datetime.datetime.strptime(key_value[1], '%Y-%m-%d')).strftime("%Y-%m-%dT%H:%M:%S")
                                  ))
        else:
            wps_input.append((key_value[0], key_value[1]))
    return wps_input


def get_url_json(url):
    """
    Retrieve the state update of a process from the provided URL. URL should be from DB column GeoAPIresults.
    It sends a GET request to the specified URL and returns the JSON response from the API.

    Example usage:
    ```
    response = get_url_json('http://example.com/api/process/state')
    ```
    :param url: The URL of the API endpoint to check the state of a process.
    :return: The JSON response from the API indicating the state of the process.
    """
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        logger.error(f'Error checking state of process: {e}')
        return {'error': 'Got no update from PyGeoAPI'}


def handle_geoapiprocess_output(user, execution, process_description, inputs):
    """

    :param execution: owslib.wps.output object
    :type execution: object
    :param process_description: name of the process
    :type process_description: string
    :param inputs: {'key_list': [], 'value_list': [], 'dataset': ''}
    :type inputs: dict
    :return:
    """
    result = execution.json()
    report_html = ""

    def load_report(report_path, result_type):
        if result_type == 'json':
            with open(report_path + '.json') as user_file:
                file_contents = user_file.read()
                file_contents = json.loads(file_contents)
        elif result_type == 'html':
            with open(report_path + '.html') as user_file:
                file_contents = user_file.read()
        return file_contents

    if 'dir' in result:
        report_path = result['dir'] + '/report'
        report_html = load_report(report_path, 'html')

    # if result is a single output, first make sure the format is as expected like for multiple outputs
    output_keys = list(process_description['outputs'].keys())
    if len(output_keys) == 1 and output_keys[0] not in result.keys():
        result = {output_keys[0]: result}

    # shorten output for the database. TODO: In the model 1024 chars are allowed
    if len(str(result)) < 300:  # random number, typical pathlength < 260 chars
        db_output_data = result
    else:
        db_output_data = str(result)[:300]

    all_outputs = {
        "execution_status": execution.status_code,
        "version": process_description['version'],
        "verbose": execution.reason,
        "errors": [],  # execution.percentCompleted,
        "processTime: ": execution.elapsed.total_seconds(),  # elapsed time in seconds
        "creationTime: ": execution.headers['Date'],
        "result": result,
        "report_html": report_html,
    }

    if 'error' in result and 'value' in result.error and result.error.value == True:
        print(f"Status {execution.status_code}, error in wps process")
        return all_outputs
    elif "res" in result and "description" in result["res"] and "error" in result["res"]["description"]:
        print('error in result: ', execution.status_code)
        return all_outputs
    else:
        result.pop('error', None)  # as there shouldn't be an error, we can remove it from the results
        process_description['outputs'].pop('error',
                                           None)  # as there shouldn't be an error, we can remove it from the results


    def singleOutput2json(output_name: object, result: object, output_description: object) -> object:
        """

        :rtype: object
        """
        single_output = {}
        single_output["data"] = result

        # get datatype
        if output_description[output_name]['schema']['type'] == 'object':
            if 'contentMediaType' in output_description[output_name]['schema'] \
                and 'json' in output_description[output_name]['schema']['contentMediaType']:
                single_output["type"] = 'json'
            else:
                single_output["type"] = output_description[output_name]['schema']['type']
        else:
            single_output["type"] = output_description[output_name]['schema']['type']

        single_output["data"] = result

        if 'URI' in output_description:
            path = output_description['URI']
        elif 'keywords' in output_description and "pickle" in output_description['keywords']:
            path = result['URI']  # get first value of string tuple
        else:
            path = ""

        if 'value' in single_output["data"] and len(
            single_output["data"]['value']) < 300:  # random number, typical pathlength < 260 chars
            single_output["data"] = result['value']
            db_output_data = result['value']
        elif path != "":
            try:
                file_name = path[:-4] + single_output["type"] + path[-4:]
            except Exception as e:
                print("Warning: no file was created for long string")
                print(e)
        else:
            db_output_data = ""

        if db_output_data != "":
            db_output = [output_name, single_output["type"], db_output_data]
            # create db entry

            wpsid = create_wpsdb_entry(wps_process=process_description['identifier'], invalue=inputs,
                                       outputs=db_output)

            single_output["wpsID"] = wpsid
            single_output["dropBtn"] = {
                "orgid": wpsid,
                "type": "data",
                "name": "",
                "inputs": [],
                "outputs": [single_output["type"]],
            }
        else:
            print("*** no output to write to db ***")
            single_output["error"] = "no output to write to db"

        return single_output

    if len(process_description['outputs']) <= 1:
        all_outputs["result"][output_keys[0]] = singleOutput2json(list(process_description['outputs'].keys())[0],
                                                                  execution.json(), process_description['outputs'])
    else:
        # iterate through dict of outputs
        for output_k, output_v in execution.json().items():
            single_output = singleOutput2json(output_k, execution.json()[output_k],
                                              process_description['outputs'][output_k])
            all_outputs["result"][output_k] = single_output

    return all_outputs


def url_join(endpoint, path):
    """
    Make sure concatination of path and result doesn't result in two slashes or no slashes at all.
    :param endpoint: string
    :param path: string
    :return: string
    """
    if endpoint[-1] == "/" and path[0] == "/":
        url = f'{endpoint}{path[1:]}'
    elif endpoint[-1] != "/" and path[0] != "/":
        url = f'{endpoint}/{path}'
    else:
        url = f'{endpoint}{path}'
    return url


def handle_wps_output(execution, wps_process, inputs):
    """

    :param execution: owslib.wps.output object
    :type execution: object
    :param wps_process: name of the process
    :type wps_process: string
    :param inputs: {'key_list': [], 'value_list': [], 'dataset': ''}
    :type inputs: dict
    :return:
    """
    # order output for database
    all_outputs = {
        "execution_status": execution.status,
        "version": execution.version,
        "verbose": execution.verbose,
        "timeout": execution.timeout,
        "percentCompleted": execution.percentCompleted,
        "errors": execution.percentCompleted,
        "creationTime: ": execution.creationTime,
        "result": {},
    }
    path = ""

    if execution.errors != []:
        return all_outputs

    # iterate through list of outputs
    for output in execution.processOutputs:

        if output.identifier == "error":
            error_dict = {}
            error = False
            error_dict["error"] = output.data[0] == "True"
            all_outputs["error"] = error_dict

            if error_dict["error"] is not False:
                print("error in wps process: ", error_dict)
                all_outputs = {
                    "execution_status": "error in wps process",
                    "error": error_dict["message"],
                }
                break

        # if no error build output for a result button in portal:
        else:
            single_output = {}

            # get datatype
            try:
                keywords = json.loads(output.abstract)["keywords"][0]
                single_output["type"] = keywords
                if "pickle" in keywords:
                    path = eval(output.data[0])[0]  # get first value of string tuple
            except TypeError as e:
                if output.dataType not in basicdatatypes:
                    matchObj = re.search("[^:]+$", output.dataType)
                    output.dataType = matchObj.group()
                    print(f'No keywords or type (TypeError: {e}). Using <{output.dataType}> as DataType.'
                    )
                single_output["type"] = output.dataType
            except KeyError as e:
                print("this is a key error: ", e)

            # get data
            if output.data:
                if output.dataType in ["string", "integer"]:
                    single_output["data"] = output.data[0]
                else:
                    single_output['data'] = eval(output.data[0])[0]

            # TODO: Decide how to handle errors from WPS (show nothing, everything and user can check what is okay?)
            if (
                output.data and len(single_output["data"]) < 300
            ):  # random number, typical pathlength < 260 chars
                db_output_data = output.data[0]
            elif path != "":
                try:
                    file_name = path[:-4] + single_output["type"] + path[-4:]
                    text_file = open(file_name, "w")
                    text_file.write(eval(output.data[0])[0])
                    text_file.close()
                    db_output_data = file_name
                    single_output["data"] = eval(output.data[0])[0]
                except Exception as e:
                    print("Warning: no file was created for long string")
                    print(e)
            else:
                db_output_data = ""

            if db_output_data != "":
                db_output = [output.identifier, single_output["type"], db_output_data]
                # create db entry
                wpsid = create_wpsdb_entry(wps_process, inputs, db_output)

                single_output["wpsID"] = wpsid
                single_output["dropBtn"] = {
                    "orgid": wpsid,
                    "type": "data",
                    "name": "",
                    "inputs": [],
                    "outputs": [single_output["type"]],
                }
            else:
                print("*** no output to write to db ***")
                single_output["error"] = "no output to write to db"

            all_outputs["result"][output.identifier] = single_output
    return all_outputs


def has_result_error(dataset):
    print('dataset: ', dataset)
    return False


def prepare_inputs(request, request_input):
    """
    Check if input is a basic datatype (like string, int, bool...) or more sophisticated data with source path in db.
    :param request_input:
    :return:
    """
    for i, val in enumerate(request_input['in_type_list']):

        value = ''
        if val in datatypes and str(request_input['value_list'][i])[0:3] == 'wps':  # if basicdatatype and already stored as file. (if not a basicdatatype look for data in db???)
            value = ast.literal_eval(WpsResults.objects
                                     .get(id=int(request_input['value_list'][i][3:])).outputs)['folder']
        elif val in datatypes and str(request_input['value_list'][i])[0:2] == 'db':
            orgid = request_input['value_list'][i]
            result = save_dataset(request=request, orgid=request_input['value_list'][i],
                                  inputs=[('entry_id', str(orgid)), ('uuid', '')], wps_process="dbloader")
            service, endpoint, wps_services = get_endpoint_data(DEBUG)
            value = url_join(endpoint, result['path'])

        elif val in datatypes and isinstance(request_input['value_list'][i], int):
            request_input['value_list'][i]

        elif isinstance(request_input['value_list'][i], list):  # if there is a grouped dataset do:
            value = []
            ids = []
            for element in request_input['value_list'][i]:
                # check if element is a result a simple input or an entries ID.
                if isinstance(element, str) and len(element) > 2 and element[0:3] == 'wps':
                    ids.append(element[3:])
                elif val[i] in datatypes:
                    value.append(element)
                else:  # if element is not on disc load it and write to db
                    value.append(element)
            for j in WpsResults.objects.filter(id__in=ids):
                value.append(ast.literal_eval(j.outputs)['folder'])

        else:
            value = request_input['value_list'][i]

        request_input['value_list'][i] = value
        request_input['in_dict'][request_input['key_list'][i]] = value
    return request_input


def process_to_json(wps_process):
    # simply serialize wps to json
    whole_wpsprocess_json = jsonpickle.encode(wps_process, unpicklable=False)

    # convert to dict to remove unwanted keys and empty values
    whole_wpsprocess = json.loads(whole_wpsprocess_json)
    whole_wpsprocess.pop("_root", None)
    wps_description = {}
    for a in whole_wpsprocess:
        if isinstance(whole_wpsprocess[a], list):
            list_values = []
            for b in whole_wpsprocess[a]:
                if isinstance(b, dict):
                    innerdict = {}
                    for k, v in b.items():
                        if k == "allowedValues" and v != [] and v[0] == "_keywords":
                            innerdict["keywords"] = v[1:]
                        elif k == "version":
                            innerdict["version"] = v
                        elif k == "processVersion":
                            innerdict["processVersion"] = v
                        elif (
                            k == "abstract" and v is not None
                        ):  # and not v == [] and v[0] == '_keywords':
                            try:
                                for abst in json.loads(v):
                                    if abst == "keywords":
                                        innerdict[abst] = json.loads(v)[abst]
                                    else:
                                        innerdict["abstract"] = v
                            except ValueError:
                                innerdict["abstract"] = v
                        elif v is not None and v != []:
                            if isinstance(v, str) and re.search(r"(?<=/#)\w+", v):
                                match = re.search(r"(?<=/#)\w+", v)
                                innerdict[k] = match.group(0)
                            else:
                                innerdict[k] = v

                    if (
                        "minOccurs" in innerdict
                        and innerdict["minOccurs"] > 0
                        and innerdict["dataType"] != "boolean"
                    ):
                        innerdict["required"] = True

                    list_values.append(innerdict)
                elif b is not None and b != []:
                    list_values.append(b)

            wps_description[a] = list_values
        elif not whole_wpsprocess[a] is None and whole_wpsprocess[a] != []:
            wps_description[a] = whole_wpsprocess[a]

    return wps_description


def run_pygeoapi_process(endpoint, wps_process, input, user_id, username):
    return requests.post(f'{endpoint}/processes/{wps_process}/execution',
                         json={
                             "mode": "async",
                             'inputs': {**input.get("in_dict", ""),
                                        'User-Info':  # plant the username in last moment
                                             f'user{user_id}_{username}'}
                              },
                              headers={'Content-Type': 'application/json',
                                       }
                              )


def save_dataset(request, orgid, inputs, wps_process, date=None):
    try:
        dataset = DataObject(orgid, date)  # load data from database
        now = datetime.datetime.now()

        folder = f'{request.user.pk}_dbload_{now.strftime("%d%m%y_%H%M%S%f")}'  # use user, toolname, and datetime
        fullpath = Path(f'{PROCESSES_IN_DIR}/{folder}/')
        fullpath.mkdir(mode=0o775, parents=True, exist_ok=True)

        # Create a dictionary with metadata that might be needed for a tool, e.g.coordinates, datatype, ...
        basic_metadata = dataset.coords
        basic_metadata['ordig'] = orgid
        # basic_metadata.update(dataset)
        # writing from pandas is slower but more flexible
        with open(fullpath.joinpath('dataframe.json'), "w") as outfile:
            json.dump(basic_metadata, outfile)
        fullpath.chmod(0o775)

        output = {'path': str(fullpath), 'type': dataset.type, 'folder': str(folder)}

        dbkey = WpsResults.objects.create(
            open=True,
            wps=wps_process,
            inputs=inputs,
            outputs=output,
            creation=timezone.now(),
        )

        # Create a dictionary with metadata that might be needed for a tool, e.g.coordinates, datatype, ...
        basic_metadata = dataset.coords
        basic_metadata['orgid'] = orgid
        basic_metadata['id'] = "wps" + str(dbkey.id)

        with open(fullpath.joinpath('dataframe.json'), "w") as outfile:
            json.dump(basic_metadata, outfile)
        fullpath.chmod(0o775)

        result = {"id": "wps" + str(dbkey.id),
                  "inputs": json.dumps(inputs),
                  "orgid": orgid,
                  "outputs": output,
                  "process": wps_process,
                  "type": dataset.type,
                  }

    except Exception as e:
        print('Exception in save_dataset: ', e)
        raise Http404

    return {"short_info": result, "path": folder}


# ------------------- old functions. Check if still in use and delete if unused --------------------
def db_load(request):
    """
    Function to preload data from database, convert it, and store a pickle of the data
    Example for input for wps dbloader:  [('entry_id', '12'), ('uuid', ''), ('start', '1990-10-31T09:06'),
    ('end', datetime.datetime(2018, 12, 31, 0, 0))]

    This function was to make data available before the user runs a tool. Was used to improve user experience.
    :param request: dict
    :return:
    """
    wps_process = "dbloader"
    request_input = json.loads(request.GET.get("dbload"))
    request_dict = dict(zip(request_input['key_list'], request_input['value_list']))
    orgid = request_input.get("dataset")

    # check if user has access to dataset
    accessible_data = get_accessible_data(request, orgid[2:])
    accessible_data = accessible_data["open"]
    if len(accessible_data) < 1:
        return JsonResponse({"Error": "No accessible dataset."})
    elif len(accessible_data) > 1:
        return JsonResponse(
            {"Error": "You have to adjust function for list of datasets."}
        )

    # format inputs for wps server
    inputs = edit_input(list(zip(request_input.get("key_list", ""), request_input.get("value_list", ""))))

    if request_dict['start'] != 'None':
        date = [make_aware(datetime.datetime.strptime(request_dict['start'], '%Y-%m-%d')),
                make_aware(datetime.datetime.strptime(request_dict['end'], '%Y-%m-%d'))]
    else:
        date = None

    # Try to read path from database. If not available load in except block from db and store (meta-)data o disk.
    try:
        preloaded_data = WpsResults.objects.get(wps=wps_process, inputs=inputs)
        output = ast.literal_eval(preloaded_data.outputs)
        result = {"id": "wps" + str(preloaded_data.id),
                  "inputs": inputs,
                  "orgid": orgid,
                  "type": output["type"],
                  }
    except Exception as e:
        save_result = save_dataset(request=request, orgid=orgid, inputs=inputs, wps_process=wps_process, date=date)
        result = save_result['short_info']

    return JsonResponse(result)


def get_or_create_wpsdb_entry(service: str, wps_process: str, input: tuple):
    """
    Get or create a database entry.
    :param service: name of the wps service
    :param wps_process: identifier of the wps process
    """
    db_result, created = WpsResults.objects.get_or_create(
        open=True,
        wps=wps_process,
        inputs={input[0]: input[1]},
        defaults={"creation": timezone.now(), "access": timezone.now()},
    )
    result = {"wps_id": db_result.id}
    if not created:
        db_result.access = timezone.now()
        db_result.save()
    else:
        wps = get_wps_service_engine(service)
        execution = wps.execute(wps_process, [input])
        execution_status = execution.status
        wpsError = {}
        if "Exception" in execution_status:
            result = {"Error": "dbload did not work. Please check log file"}
            db_result.delete()
            logger.error(
                "Got no result from wps for %s: %s",
                (service, wps_process, input),
                execution_status,
            )
        elif execution_status == "ProcessSucceeded" and wpsError["error"] == "False":
            db_result.outputs = execution.processOutputs[0].data
            db_result.save()
        else:
            db_result.delete()
            result = {"Error": "dbload did not work. Please check log file"}
            logger.error(
                "get_or create wps execution_status for %s: %s",
                (service, wps_process, input),
                execution_status,
            )

    return result


def get_process_metadata(sessiondata, describedprocess, identifier):
    sessiondata[identifier]["processin"] = []
    sessiondata[identifier]["processout"] = []

    for i in describedprocess.dataInputs:
        if i.allowedValues == [] or not i.allowedValues[0] == "_keywords":
            if i.abstract and len(i.abstract) > 10 and "keywords" in i.abstract[2:10]:
                keywords = ast.literal_eval(i.abstract[: 1 + i.abstract.find("}", 10)])[
                    "keywords"
                ]
                sessiondata[identifier]["processin"].append(keywords)
            else:
                sessiondata[identifier]["processin"].append(i.dataType)

        elif i.allowedValues[0] == "_keywords":
            if i.allowedValues[1] == "pattern":
                patternList = i.allowedValues[1:]
                patternList.insert(0, i.dataType)
                sessiondata[identifier]["processin"].append(patternList)
            else:
                sessiondata[identifier]["processin"].append(i.allowedValues[1:])

    for i in describedprocess.processOutputs:
        if "error" not in i.identifier:
            if i.abstract is not None:
                if "keywords" in json.loads(i.abstract):
                    sessiondata[identifier]["processout"].append(
                        json.loads(i.abstract)["keywords"]
                    )
            elif isinstance(i.dataType, str) or isinstance(i.dataType, float):
                sessiondata[identifier]["processout"].append(i.dataType)

    return sessiondata


def handle_geoapiprocess_output_old(execution, process_description, inputs):
    """

    :param execution: owslib.wps.output object
    :type execution: object
    :param process_description: name of the process
    :type process_description: string
    :param inputs: {'key_list': [], 'value_list': [], 'dataset': ''}
    :type inputs: dict
    :return:
    """
    result = execution.json();

    all_outputs = {
        "execution_status": execution.status_code,
        "version": process_description['version'],
        "verbose": execution.reason,
        "errors": [],  # execution.percentCompleted,
        "processTime: ": execution.elapsed.total_seconds(),  # elapsed time in seconds
        "creationTime: ": execution.headers['Date'],
        "result": execution.json(),
    }

    if execution.status_code != 200 or ('error' in result and 'value' in result.error and result.error.value == True):
        print(f"{execution.status_code}, error in wps process")
        return all_outputs
    else:
        result.pop('error', None)  # as there shouldn't be an error, we can remove it from the results
        process_description['outputs'].pop('error',
                                           None)  # as there shouldn't be an error, we can remove it from the results

    def singleOutput2json(output_name, result, output_description):
        single_output = {}
        # get datatype
        if output_description[output_name]['schema']['type'] == 'object':
            if 'contentMediaType' in output_description[output_name]['schema'] \
                and 'json' in output_description[output_name]['schema']['contentMediaType']:
                single_output["type"] = 'json'
            else:
                single_output["type"] = output_description[output_name]['schema']['type']
        else:
            single_output["type"] = output_description[output_name]['schema']['type']

        single_output["data"] = result

        if 'keywords' in output_description and "pickle" in output_description['keywords']:
            path = result['URI']  # get first value of string tuple
        else:
            path = ""

        if len(single_output["data"]['value']) < 300:  # random number, typical pathlength < 260 chars
            single_output["data"] = result['value']
            db_output_data = result['value']
        elif path != "":
            try:
                file_name = path[:-4] + single_output["type"] + path[-4:]
            except Exception as e:
                print("Warning: no file was created for long string")
                print(e)
        else:
            db_output_data = ""

        # TODO: create function to write to db
        if db_output_data != "":
            pass
        else:
            print("*** no output to write to db ***")
            single_output["error"] = "no output to write to db"

        return single_output

    if len(process_description['outputs']) <= 1:
        single_output = singleOutput2json(list(process_description['outputs'].keys())[0], execution.json(),
                                          process_description['outputs'])
    else:
        # iterate through dict of outputs
        for output_k, output_v in execution.json().items():
            single_output = singleOutput2json(output_k, execution.json()[output_k],
                                              process_description['outputs'][output_k])

    def singleoutput2db():
        pass

    for output_k, output_v in execution.json().items():

        # prepare data for database
        if len(single_output["data"]) < 300:  # random number, typical pathlength < 260 chars
            db_output_data = output_v
        elif path != "":
            try:
                file_name = path[:-4] + single_output["type"] + path[-4:]
                db_output_data = file_name
            except Exception as e:
                print("Warning: no file was created for long string")
                print(e)
        else:
            db_output_data = ""

        print('db_output_data: ', db_output_data)
        # add data to database
        if db_output_data != "":
            db_output = [output.identifier, single_output["type"], db_output_data]
            # create db entry
            wpsid = create_wpsdb_entry(process_description, inputs, db_output)

            single_output["wpsID"] = wpsid
            single_output["dropBtn"] = {
                "orgid": wpsid,
                "type": "data",
                "name": "",
                "inputs": [],
                "outputs": [single_output["type"]],
            }
        else:
            print("*** no output to write to db ***")
            single_output["error"] = "no output to write to db"

        all_outputs["result"][output] = single_output

    return all_outputs
