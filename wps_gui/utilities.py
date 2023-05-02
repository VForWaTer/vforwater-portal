import ast
import json
import re
from os import path
from urllib.error import HTTPError, URLError

from owslib.wps import WebProcessingService

from vfw_home.datatypes import datatypes
from .models import WebProcessingService as WpsModel, WpsResults
from owslib.ogcapi.processes import Processes as ogcProcesses
from heron.settings import VFW_SERVER, VFW_GEOAPI, wps_log


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


def get_endpoint_data(devel = False):

    try:
        wps_services = list(WpsModel.objects.values_list("name", flat=True))
        wps_services_url = list(WpsModel.objects.values_list('endpoint', flat=True))
        # print('wps_ services & wps_services_url: ', wps_services, wps_services_url)
        service = wps_services[0]  # pygeoapi_vforwater

        if not devel:
            endpoint = wps_services_url[0] # http://geoapi:5000/
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
        inputs[k] = v['schema']['type']

    for k, v in apiprocess['outputs'].items():
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
        "keywords": apiprocess['keywords'],  # ATTENTION! old wps hack used keywords to get info about accepted data in workplace.js - vfw.workspace.modal.build_modal(),
        "title": apiprocess['title'],
        "version": apiprocess['version'],
    }


def geoapi_output2wps_processoutput(outputs):
    """
    Change input object as needed for the dropbox in the workspace.
    :param inputs:
    :return:
    """
    dataoutputs = []

    # Todo: frontend (e.g. vfw.workspace.workflow.process_drop_params) is still as needed for wps. Update for geoapi!
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

    # Todo: frontend (e.g. vfw.workspace.workflow.process_drop_params) is still as needed for wps. Update for geoapi!
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
        if v['minOccurs'] > 0 and v['schema']['type'] != 'boolean' and v['schema']['type'] != 'bool':
            inputs[k]['required'] = True
        else:
            inputs[k]['required'] = False

    return inputs



from owslib.ogcapi import Collections
from owslib.util import Authentication

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


def create_wpsdb_entry(wps_process: str, invalue: list, outputs: object) -> object:
    """
    Create a database entry.
    :param wps_process: identifier of the wps process
    :param invalue: dict of input identifier of wps and respective value (e.g. a path)
    :param outputs: dict of output or a path
    """
    db_result = {'id': 'bla'}
    # db_result = WpsResults.objects.get_or_create(
    #     # owner=user,
    #     open=False,
    #     wps=wps_process,
    #     inputs=invalue,
    #     outputs=outputs,
    #     creation=timezone.now(),
    # )  # , access=timezone.now())
    return db_result['id']


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
    # if result is a single output, first make sure the format is as expected like for multiple outputs
    output_keys = list(process_description['outputs'].keys())
    if len(output_keys) == 1 and output_keys[0] not in result.keys():
        result = {output_keys[0]: result}

    if len(str(result)) < 300:  # random number, typical pathlength < 260 chars
        db_output_data = result
    else:
        db_output_data = str(result)[:300]

    wpsid = create_wpsdb_entry(inputs['id'], inputs['in_dict'], db_output_data)
    # wpsid = create_wpsdb_entry(user, inputs['id'], inputs['in_dict'], db_output_data)

    all_outputs = {
        "execution_status": execution.status_code,
        "version": process_description['version'],
        "verbose": execution.reason,
        # "timeout": execution.timeout,
        # "percentCompleted": execution.percentCompleted,
        "errors": [],  # execution.percentCompleted,
        "processTime: ": execution.elapsed.total_seconds(),  # elapsed time in seconds
        "creationTime: ": execution.headers['Date'],
        # 'process': execution.process,
        "result": result,
    }

    if 'error' in result and 'value' in result.error and result.error.value == True:
        print(f"Status {execution.status_code}, error in wps process")
        return all_outputs
    else:
        result.pop('error', None) # as there shouldn't be an error, we can remove it from the results
        process_description['outputs'].pop('error', None) # as there shouldn't be an error, we can remove it from the results

    def singleOutput2json(output_name, result, output_description):
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

        if 'value' in single_output["data"] and len(single_output["data"]['value']) < 300:  # random number, typical pathlength < 260 chars
            single_output["data"] = result['value']
            db_output_data = result['value']
        elif path != "":  # TODO: fix it (compare with handle_wps_output)
            try:
                file_name = path[:-4] + single_output["type"] + path[-4:]
                # text_file = open(file_name, "w")
                # text_file.write(eval(output.data[0])[0])
                # text_file.close()
                # db_output_data = file_name
                # single_output["data"] = eval(output.data[0])[0]
            except Exception as e:
                print("Warning: no file was created for long string")
                print(e)
        else:
            db_output_data = ""

        # TODO: create function to write to db
        if db_output_data != "":
            db_output = [output_name, single_output["type"], db_output_data]
            # create db entry
            wpsid = create_wpsdb_entry(process_description, inputs, db_output)
            # wpsid = create_wpsdb_entry(user, process_description, inputs, db_output)

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
        all_outputs["result"][output_keys[0]] = singleOutput2json(list(process_description['outputs'].keys())[0], execution.json(), process_description['outputs'])
    else:
        # iterate through dict of outputs
        for output_k, output_v in execution.json().items():
            single_output = singleOutput2json(output_k, execution.json()[output_k], process_description['outputs'][output_k])
            all_outputs["result"][output_k] = single_output

    # TODO: Have to handle bytes result
    # if type(output.data[0]) is bytes:
    #     if len(output.data[0]) > 30:
    #         substring = str(output.data[0][:30])
    #         if "xml" in substring:
    #             print('XML as input not implemented yet. Got: ', output.data[0])
    #             logger.error('XML as input not implemented yet.')
    #             # tree = ET.fromstring(output.data[0])
    #             # for child in tree:
    #             #     print(child.tag, child.attrib)
    #             del outputs_for_db[-1]

    return all_outputs



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
        # "timeout": execution.timeout,
        # "percentCompleted": execution.percentCompleted,
        "errors": [],  # execution.percentCompleted,
        "processTime: ": execution.elapsed.total_seconds(),  # elapsed time in seconds
        "creationTime: ": execution.headers['Date'],
        # 'process': execution.process,
        "result": execution.json(),
    }

    if execution.status_code != 200 or ('error' in result and 'value' in result.error and result.error.value == True):
        print(f"{execution.status_code}, error in wps process")
        return all_outputs
    else:
        result.pop('error', None) # as there shouldn't be an error, we can remove it from the results
        process_description['outputs'].pop('error', None) # as there shouldn't be an error, we can remove it from the results

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
        elif path != "":  # TODO: fix it (compare with handle_wps_output)
            try:
                file_name = path[:-4] + single_output["type"] + path[-4:]
                # text_file = open(file_name, "w")
                # text_file.write(eval(output.data[0])[0])
                # text_file.close()
                # db_output_data = file_name
                # single_output["data"] = eval(output.data[0])[0]
            except Exception as e:
                print("Warning: no file was created for long string")
                print(e)
        else:
            db_output_data = ""

        # TODO: create function to write to db
        if db_output_data != "":
            pass
        #     db_output = [inputs.id, single_output["type"], db_output_data]
        #     # create db entry
        #     wpsid = create_wpsdb_entry(inputs['id'], inputs, db_output)
        #
        #     single_output["wpsID"] = wpsid
        #     single_output["dropBtn"] = {
        #         "orgid": wpsid,
        #         "type": "data",
        #         "name": "",
        #         "inputs": [],
        #         "outputs": [single_output["type"]],
        #     }
        else:
            print("*** no output to write to db ***")
            single_output["error"] = "no output to write to db"

        return single_output

    if len(process_description['outputs']) <= 1:
        single_output = singleOutput2json(list(process_description['outputs'].keys())[0], execution.json(), process_description['outputs'])
    else:
        # iterate through dict of outputs
        for output_k, output_v in execution.json().items():
            single_output = singleOutput2json(output_k, execution.json()[output_k], process_description['outputs'][output_k])

    def singleoutput2db():
        pass


    for output_k, output_v in execution.json().items():
        # single_output["data"] = output_v

        # prepare data for database
        if len(single_output["data"]) < 300:  # random number, typical pathlength < 260 chars
            db_output_data = output_v
        elif path != "":  # TODO: fix it (compare with handle_wps_output)
            print('output.data: ', output_v)
            try:
                file_name = path[:-4] + single_output["type"] + path[-4:]
                # text_file = open(file_name, "w")
                # text_file.write(eval(output.data[0])[0])
                # text_file.close()
                db_output_data = file_name
                # single_output["data"] = eval(output.data[0])[0]
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
        # TODO: Have to handle bytes result
        # if type(output.data[0]) is bytes:
        #     if len(output.data[0]) > 30:
        #         substring = str(output.data[0][:30])
        #         if "xml" in substring:
        #             print('XML as input not implemented yet. Got: ', output.data[0])
        #             logger.error('XML as input not implemented yet.')
        #             # tree = ET.fromstring(output.data[0])
        #             # for child in tree:
        #             #     print(child.tag, child.attrib)
        #             del outputs_for_db[-1]

    return all_outputs


def prepare_inputs(request_input):
    """
    Check if input is a basic datatype (like string, int, bool...) or more sophisticated data with source path in db.
    :param request_input:
    :return:
    """
    for i, val in enumerate(request_input['in_type_list']):
        if val in datatypes and request_input['value_list'][i][0:3] == 'wps':  # if not a basicdatatype look for data in db
            folder = ast.literal_eval(WpsResults.objects.get(id=request_input['value_list'][i][3:]).outputs)['folder']
            request_input['value_list'][i] = folder
            request_input['in_dict'][request_input['key_list'][i]] = folder

    return request_input
