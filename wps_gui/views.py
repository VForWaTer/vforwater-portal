# =================================================================
#
# Authors: Marcus Strobl <marcus.strobl@kit.edu>
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

# from inspect import getmembers
import ast
import datetime
import itertools
import json
import numbers
import re
import subprocess
import sys
import time
from pathlib import Path

import jsonpickle
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, JsonResponse
from django.http.response import Http404
from django.shortcuts import render
from django.utils.timezone import make_aware
from django.views.generic import TemplateView
from django.utils import translation, timezone
from json2html import json2html

from heron.settings import VFW_SERVER, HOST_NAME, DEBUG, PROCESSES_IN_DIR
from vfw_home.data_obj import DataObject
from vfw_home.datatypes import basicdatatypes, datatypes
from vfw_home.models import Entries, Datatypes, EntrygroupTypes, Datasources, Timeseries_1D
from vfw_home.utilities import entry_has_data
from vfw_home.views import get_accessible_data, get_dataset
from wps_gui.models import WpsResults, WebProcessingService, WpsDescription, GeoAPIResults
from wps_gui.utilities import (
    get_wps_service_engine,
    list_wps_service_engines,
    abstract_is_link, get_endpoint_data, get_process_basics, get_process_info, handle_geoapiprocess_output,
    prepare_inputs, save_dataset, create_geoapi_db_entry,
)
from owslib.ogcapi.processes import Processes as getProcesses

import logging

logger = logging.getLogger(__name__)


# datatypes = ['timeseries', 'ts-aggregate', 'ts-pickle', 'ts-merge', 'array', 'aggregate',
#              'pickle', 'merge', 'merged-pickle', 'merged-ts-pickle']

# from heron_wps.forms import InputForm

def home(request):
    ogcapi_proc = {}

    service, endpoint, wps_services = get_endpoint_data(DEBUG)

    if service == 'pygeoapi_vforwater':  # Do we need this 'if'?
        try:
            apiproc = getProcesses(endpoint)
            for process in apiproc.processes():
                ogcapi_proc[process['id']] = {}
                ogcapi_proc[process['id']] = get_process_basics(apiproc.process(process['id']))

        except Exception as e:
            logger.error(sys.exc_info()[0])
            print(f'Exception in wps_gui.views.home: {e}, service: {service}, endpoint: {endpoint}')
            context = {
                "wps_services": translation.gettext(
                    "At the moment the processes are not available. We apologize for the inconvenience."),
                "processes": "",
                "service": "Error",
            }
            return render(request, "wps_gui/home.html", context)

        # Remove process that should not be visible for users
        if "dbloader" in ogcapi_proc:
            del ogcapi_proc["dbloader"]
        if "datareader" in ogcapi_proc:
            del ogcapi_proc["datareader"]
        if "workflow" in ogcapi_proc:
            del ogcapi_proc["workflow"]

        context = {
            "wps_services": wps_services,
            "processes": ogcapi_proc,
            "service": service,
        }

        return render(request, "wps_gui/home.html", context)


# def home(request):
#     """
#     Home page for Heron WPS tool. Lists all the WPS services that are linked.
#     """
#     # TODO: Ugly hack because keywords are yet not supported from owslib. Check upcoming versions of owslib!
#     # TODO: IMPORTANT! Process description is only loaded once.
#     #  When changing a process, the version number has to be updated.
#     jsondata = {}
#     wps_data = {}
#     WpsQueryset = WpsDescription.objects
#     try:
#         wps_services = list_wps_service_engines()
#         # service = 'PyWPS_vforwater'
#         service = WebProcessingService.objects.values_list("name", flat=True)[1] # [1] PyWPS_Elnaz_Local_Server #[0] PyWPS_vforwater #[2] pygeoapi
#         wps = get_wps_service_engine(service)
#     except Exception as e:
#         print("Exception in wps_gui.views.home: ", e)
#
#     # if WpsQueryset.exists():
#     #     for process in list(WpsQueryset.values('identifier', 'service', 'title', 'abstract', 'inputs', 'outputs',
#     #                                            'verbose', 'metadata', 'dataInputs', 'processOutputs', 'version',
#     #                                            'storeSupported', 'statusSupported'
#     #                                            )):
#     #         wps_data[process['identifier']] = {'service': process['service'],
#     #                                            'title': process['title'],
#     #                                            'abstract': process['abstract'],
#     #                                            'processin': process['inputs'],
#     #                                            'processout': process['outputs']}
#     #         jsondata[process['identifier']] = {'service': process['service'],
#     #                                            'verbose': json.dumps(process['verbose']),
#     #                                            'storeSupported': json.dumps(process['storeSupported']),
#     #                                            'statusSupported': json.dumps(process['statusSupported']),
#     #                                            'title': process['title'], 'abstract': process['abstract'],
#     #                                            'metadata': process['metadata'],
#     #                                            'dataInputs': json.dumps(process['dataInputs']),
#     #                                            'processOutputs': json.dumps(process['processOutputs']),
#     #                                            'version': json.dumps(process['version'])}
#
#     try:
#         for process in wps.processes:
#             if process.identifier not in jsondata.keys():
#                 wps_data[process.identifier] = {}
#                 wps_data[process.identifier] = {
#                     "title": process.title,
#                     "abstract": process.abstract,
#                     "identifier": process.identifier,
#                     "processin": "",
#                     "processout": "",
#                 }
#                 describedprocess = wps.describeprocess(process.identifier)
#                 wps_data = get_process_metadata(
#                     wps_data, describedprocess, process.identifier
#                 )
#
#                 jsondata[process.identifier] = process_to_json(process)
#                 describedprocess_json = process_to_json(describedprocess)
#
#                 # WpsQueryset.create(service=service, title=wps_data[process.identifier]['title'],
#                 #                    identifier=process.identifier,
#                 #                    abstract=wps_data[process.identifier]['abstract'],
#                 #                    inputs=wps_data[process.identifier]['processin'],
#                 #                    outputs=wps_data[process.identifier]['processout'],
#                 #                    verbose=jsondata[process.identifier]['verbose'],
#                 #                    statusSupported=describedprocess_json['statusSupported'],
#                 #                    storeSupported=describedprocess_json['storeSupported'],
#                 #                    metadata=jsondata[process.identifier]['metadata'],
#                 #                    dataInputs=describedprocess_json['dataInputs'],
#                 #                    processOutputs=describedprocess_json['processOutputs'],
#                 #                    version=jsondata[process.identifier]['processVersion']
#                 #                    )
#     except Exception as e:
#         logger.error(sys.exc_info()[0])
#         service = ""
#         wps_services = []
#         print('in except: ', e)
#
#     if "dbloader" in wps_data:
#         del wps_data["dbloader"]
#         # del jsondata['dbloader']
#     if "datareader" in wps_data:
#         del wps_data["datareader"]
#         # del jsondata['datareader']
#
#     if "workflow" in wps_data:
#         del wps_data["workflow"]
#
#     context = {
#         "wps_services": wps_services,
#         "sessiondata": wps_data,
#         "service": service,
#         # 'tools': jsondata
#         # 'tools': {service: jsondata}
#         # 'tools': json.dumps({service: jsondata})
#     }
#
#     return render(request, "wps_gui/home.html", context)


# def use_pandoc(bla):
#     from subprocess import Popen, PIPE, STDOUT
#     input_text = bla
#     p = Popen(['pandoc', '-f', 'rst', '-t', 'html', '--wrap=preserve'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
#     blala = p.communicate(input=input_text)[0]
#     return blala

# TODO: consider also storing the type of the output to the outputs
# TODO: This way a result might get calculated, but used is a older stored value, right? Rethink this!
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
            # if execution_status == "ProcessSucceeded" and not execution.processOutputs[1].data[0]:
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
        # else:
        #     try:
        #         wpsError['error'] = execution.processOutputs[1].data[0]
        #         print('+ im try 2')
        #     except ObjectDoesNotExist:
        #         print('+ im except')
        #         wpsError['error'] = 'True'
        #         wpsError['text'] = 'Something strange (Error?) in wps.'
        #         print('+ im except 2')
        #         logger.error('Something strange (Error?) in wps for %s: %s',
        #                      (service, wps_process, input), execution_status)

    return result


def create_wpsdb_entry(wps_process: str, invalue: list, outputs):
    """
    Create a database entry.
    :param wps_process: identifier of the wps process
    :param invalue: list of tuples of input identifier of wps and respective value (e.g. a path)
    """
    db_result = WpsResults.objects.create(
        open=False,
        wps=wps_process,
        inputs=dict(invalue),
        outputs=outputs,
        creation=timezone.now(),
    )  # , access=timezone.now())
    return db_result.id


class ProcessView(TemplateView):

    def get(self, request: object) -> object:
        selected_process = json.loads(request.GET.get("processview"))

        if selected_process['serv'] == 'pygeoapi_vforwater':
            service, endpoint, wps_services = get_endpoint_data(DEBUG)
            apiproc = getProcesses(endpoint)
            print("selected_process['id']: ", selected_process['id'])
            print("apiproc.process(selected_process['id']): ", apiproc.process(selected_process['id']))
            process_description = get_process_info(apiproc.process(selected_process['id']))
            print('process_description: ', process_description)
        else:
            wps = get_wps_service_engine(selected_process["serv"])
            wps_process = wps.describeprocess(selected_process["id"])

            process_description = process_to_json(wps_process)

        return JsonResponse(process_description)


def process_to_json(wps_process):
    # TODO: use of jsonpickle only to simplify readability of wps_process.
    #  Shouldn't be necessary to use jsonpickle for that. Please improve!
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
                        # TODO: ugly hack because keywords are still not implemented in pywps. Use
                        #  allow_values with first value '_keywords' instead
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

                    # TODO: The following 'if' can be removed when there is a 'required' flag to use in pywps/owslib
                    if (
                        "minOccurs" in innerdict
                        and innerdict["minOccurs"] > 0
                        and innerdict["dataType"] != "boolean"
                    ):
                        innerdict["required"] = True

                    list_values.append(innerdict)
                elif b is not None and b != []:
                    list_values.append(b)

                # print('__list_values[0]: ', list_values[0])
                # print('list_values[]["minOccours"]: ', list_values[0]['minOccours'])
            wps_description[a] = list_values
        elif not whole_wpsprocess[a] is None and whole_wpsprocess[a] != []:
            # from docutils.writers.html4css1 import Writer, HTMLTranslator
            # from docutils import core
            # class HTMLFragmentTranslator(HTMLTranslator):
            #     def __init__(self, document):
            #         HTMLTranslator.__init__(self, document)
            #         self.head_prefix = ['', '', '', '', '']
            #         self.body_prefix = []
            #         self.body_suffix = []
            #         self.stylesheet = []
            #     def astext(self):
            #         return ''.join(self.body)
            # html_fragment_writer = Writer()
            # html_fragment_writer.translator_class = HTMLFragmentTranslator
            # print("reST_to_html(v): ", core.publish_string(whole_wpsprocess[a], writer=html_fragment_writer))

            # import simplicity
            # print('rst_to_json: ', simplicity.rst_to_json(whole_wpsprocess[a]))

            # import docutils.core  # not tested yet
            # docutils.core.publish_file(v, destination_path="output.json",
            # result = open("output.json").read()
            # innerdict['abstract'] = result

            import docutils.core
            # print('+ +  +: ', docutils.core.publish_parts(whole_wpsprocess[a], writer_name="html"))

            # parts = core.publish_parts(source = whole_wpsprocess[a], writer_name = 'html')
            # print(parts['body_pre_docinfo'] + parts['fragment'])

            # print('pandoc: ', use_pandoc(whole_wpsprocess[a]))

            wps_description[a] = whole_wpsprocess[a]

    # print('wps_description: ', wps_description)
    # for i in wps_description:
    #     print('i: ', i)
    #     print('wps_description[i]: ', wps_description[i])
    #
    # for j in wps_description['dataInputs']:
    #     print('j: ', j)
    return wps_description


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
        # 'process': execution.process,
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
            # error_dict = json.loads(output.data[0])
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
                    print(
                        'No keywords or type (TypeError: {}). Using "{}" as DataType.'.format(
                            e, output.dataType
                        )
                    )
                single_output["type"] = output.dataType
            except KeyError as e:
                print("this is a key error: ", e)

            # get data
            if output.data:
                # if output.identifier == 'fig':
                # if output.dataType == 'string':
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


# from requests_futures.sessions import FuturesSession


@login_required(login_url="/oidc/authenticate/")
def process_run(request):  # TODO: Maybe check if identical input exists in db before starting the process again
    user_id = None
    try:
        user_id = request.user.id
        user_queryset = User.objects.get(id=user_id)
    except User.DoesNotExist as e:
        print('User does not exist when running a process: ', e)
        user_queryset = None

    # if request.user.is_authenticated:
    process_description = ""
    # request_input = json.loads(request.GET.get('processrun'))
    input = prepare_inputs(request=request, request_input=json.loads(request.GET.get('processrun')))
    wps_process = input.get("id", "")

    if input['serv'] == 'pygeoapi_vforwater':
        service, endpoint, wps_services = get_endpoint_data(DEBUG)
        apiproc = getProcesses(endpoint)
        process_description = get_process_info(apiproc.process(wps_process))
    else:
        logger.error(f'Cannot run process. Server "{input['serv']}" is unknown.')
        # print('You try to run a process, but I do not know your server.')

    try:
        execution = requests.post(f'{endpoint}/processes/{wps_process}/execution',
                              json={
                                  "mode": "async",
                                  # TODO: old setting from PyGeoAPI 0.13. Change for newer version
                                  'inputs': {**input.get("in_dict", ""),
                                             'User-Info':  # plant the username in last moment
                                                 f'userID{user_id}_'}
                                      # input.get("in_dict", ""),
                                  # "response": "document"  # this line adds {'outputs': [{result}]} to {result}
                              },
                              headers={'Content-Type': 'application/json',
                                       # "Prefer": "respond-async"  # TODO: Use this for PyGeoAPI 0.16 and newer
                                       }
                              )
    except Exception as e:
        print('e: ', e)
        logger.error(f'Cannot Execute process: {e}.')

    db_data = {'inputs': input.get("in_dict", ""),
               'name': wps_process,
               'open': False if user_id else True,
               'outputs': {'path': execution.headers['Location'],
                           'jobMeta_path': f"{execution.headers['Location']}?f=json",
                           'results': ""
                           # 'results': f"{execution.headers['Location']}/results?f=json"
                           },
               # 'user': user_id,
               }

    if execution.status_code == 201:  # if request is created
        # Save the job url for later use
        db_data['status'] = 'CREATED'
        newEntry = create_geoapi_db_entry(db_data, user_queryset)
    elif execution.status_code == 202:  # if request is accepted
        db_data['status'] = 'ACCEPTED'
        newEntry = create_geoapi_db_entry(db_data, user_queryset)
    elif execution.status_code == 200:  # if done
        db_data['status'] = 'FINISHED'
        newEntry = create_geoapi_db_entry(db_data, user_queryset)
    else:
        db_data['status'] = 'ERROR'
        newEntry = create_geoapi_db_entry(db_data, user_queryset)

    # add the database id to the dataset. Needed to enable request of state from client to django
    if not hasattr(db_data, 'id'):
        db_data['id'] = newEntry['id']
    result = db_data

    if newEntry['error']:
        logger.error(f'Error creating database entry for process result: {newEntry['error']}')
        print(f'Error creating database entry for process result: {newEntry['error']}')
        result = {'error': 'true'}

    return JsonResponse(result)


def get_url_json(url):
    """
    Retrieve the state update of a process from the provided URL. URL should be from DB column GeoAPIresults.
    It sends a GET request to the specified URL and returns the JSON response from the API.

    Example usage:
    ```
    response = get_url_json('http://example.com/api/process/state')
    print(response)
    ```
    :param url: The URL of the API endpoint to check the state of a process.
    :return: The JSON response from the API indicating the state of the process.
    """
    try:
        response = requests.get(url)
    except Exception as e:
        logger.error(f'Error checking state of process: {e}')
        print(f'Error checking state of process: {e}')
        response = {'error': 'Got no update from PyGeoAPI'}
    return response.json()


def delete_result(request):
    """
    Delete a specific result entry from the GeoAPIResults model based on the provided process ID.
    Deletion works only if request user and DB entry owner are the same. (TODO: later we want ownership to be shared. Who can delete then?)

    First retrieve the user record based on the user ID from the request object.
    Next, retrieve the GeoAPIResults entry based on the owner_id (user) and the process_id from the request object.

    If the user does not exist or the entry cannot be found, an exception is send to the server.
    If entry is found, the method deletes it. A deletion result with the number of deleted rows is send to the client.

    :param request: HttpRequest object containing the request data id.
    :return: JsonResponse sending done if deletion worked, else some error message.

    """
    try:
        process_id = int(request.GET['processid'])
        user_queryset = User.objects.get(id=request.user.id)

    except User.DoesNotExist as e:
        print('User does not exist when running a process: ', e)
        user_queryset = None

    except Exception as e:
        print('Got no ID to delete process: ', e)
        logger.error(f'Got no ID to delete process: {e}')
        return JsonResponse({'error': 'Got no ID to delete process.'})

    try:
        entry = GeoAPIResults.objects.filter(owner_id=user_queryset).get(id=process_id)
        deletion_report = entry.delete()
    except Exception as e:
        print('Unable to delete dataset: ', e)
        logger.error(f'Unable to delete dataset: {e}')
        return JsonResponse({'error': 'Unable to delete dataset.'})

    if deletion_report[0] == 0:
        return JsonResponse({'error': 'Nothing was deleted.'})
    else:
        return JsonResponse({'done': deletion_report[0]})


def process_state(request):
    """
    Check the state of a process in GeoAPI and store updates in DB.

    :param request: A request object that includes a process ID.
    :return: A JSON response containing the process state or an error message.
    """
    # check if request includes a process id
    try:
        process_id = int(request.GET['processid'])
    except Exception as e:
        print('Got no ID to check process state: ', e)
        logger.error(f'Got no ID to check process state: {e}')
        return JsonResponse({'error': 'Got no ID to check process state.'})

    # get element from database
    try:
        entry = GeoAPIResults.objects.get(id=process_id)
    except ObjectDoesNotExist:
        return JsonResponse({'error': f"Cannot check state of Process. Entry {process_id} seems not to exist"})

    # check if user has access to this dataset. If yes get state from GeoAPI
    if entry.open or request.user.id == entry.owner_id:
        url = entry.outputs['path']
        update = get_url_json(f'{url}?f=json')
    else:
        return JsonResponse({'error': 'No Access'})

    # check status. If successful update database and send update
    if update['status'] == "successful" and update['message'] == 'Job complete' and update['progress'] == 100:
        result_url = f'{url}/results?f=json'
        result = get_url_json(result_url)
        entry.outputs['results'] = [{'path': result_url, 'json': result}]

        entry.status = "FINISHED"
        entry.access = timezone.now().isoformat()
        try:
            entry.save()

        except ValueError as e:
            print(f"ValueError while trying to update DB: {e}")
            logger.error(f'ValueError while trying to update DB: {e}')

        except Exception as e:
            print(f"Unexpected error while trying to update DB: {e}")
            logger.error(f'Unexpected error while trying to update DB: {e}')

    else:
        logger.error(f'New style of result in dataset. Status, message, or progress is not as expected. {update}')
        print(f'New style of result in dataset. Status, message, or progress is not as expected. {update}')

    response_dict = {'status': entry.status,
                     'results': [{'path': result_url, 'json': result, 'html': json2html.convert(json=result)}]
                     }
    return JsonResponse(response_dict)


# # @login_required
# def process_run(request):
#     # if request.user.is_authenticated:
#     if True:
#         request_input = json.loads(request.GET.get('processrun'))
#         inputs = list(zip(request_input.get("key_list", ""), request_input.get("value_list", ""),
#                           request_input.get("in_type_list", "")))
#         inputs = edit_input(inputs)
#         wps = get_wps_service_engine(request_input.get("serv", ""))
#         wps_process = request_input.get("id", "")
#         execution = wps.execute(wps_process, inputs)
#
#         all_outputs = handle_wps_output(execution, wps_process, inputs)
#     else:
#         all_outputs = {'execution_status': 'auth_error'}
#         print('user is not authenticated. ', all_outputs)
#
#     return JsonResponse(all_outputs)


# TODO: Not used now, with processes that need only IDs. Maybe usable at a later state again.
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

        # TODO: data is saved, now create metadata
    return JsonResponse(result)


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
                    # new_pair = (key_value[0], ast.literal_eval(WpsResults.objects.get(id=value[5:]).outputs)[2])
                    # wps_input.append(new_pair)
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
        # elif key_value[1] is None:
        #     print('Yes! It is None!')
        else:
            wps_input.append((key_value[0], key_value[1]))
    return wps_input


# def date_to_datetime(date_string):
#
# return datetime_string


def load_data_local(inputs):
    return


#
# def process(request, service, identifier):
#     """
#     View that displays a detailed description for a WPS process.
#     """
#     print('??????????????????????????????????????')
#     #    form_class = InputForm
#     wps = get_wps_service_engine(service)
#     wps_process = wps.describeprocess(identifier)
#
#     context = {'process': wps_process,
#                'service': service,
#                'is_link': abstract_is_link(wps_process),
#                'wps': wps,
#                }
#
#     if request.method == 'POST':  # If the form has been submitted...
#         #        form = form_class(request.POST) # A form bound to the POST data
#         #        if form.is_valid(): # All validation rules pass
#         #        value_list = form['input']
#         value_list = []
#         key_list = []
#         inputs = []
#         outputs = []
#
#         value_list = request.POST.getlist('input')
#
#         for input in wps_process.processsin:
#             key_list.append(input.identifier)
#
#         inputs = list(zip(key_list, value_list))
#
#         processid = wps_process.identifier
#
#         execution = wps.execute(processid, inputs)
#         execution_status = execution.status
#
#         image = []
#         for output in execution.processOutputs:
#             outputs.append(output.data)
#             output_reference = output.reference
#             if type(output.data[0] is str):
#                 if len(output.data[0]) > 10:
#                     substring = output.data[0][:10]
#                     if "img" in substring:
#                         image = output.data[0]
#
#         for output in execution.processOutputs:
#             outputs.append(output.data)
#             output_reference = output.reference
#
#         if output_reference:
#             output_reference = output_reference.replace('localhost', HOST_NAME)
#             # output_reference = output_reference.replace('localhost','vforwater-devel')
#
#         context_p = {'process': wps_process,
#                      'inputs': inputs,
#                      'processid': processid,
#                      'outputs': outputs,
#                      'image': image,
#                      'output_reference': output_reference,
#                      'execution_status': execution_status
#                      }
#         return render(request, 'wps_gui/result.html', context_p)
#
#     return render(request, 'wps_gui/process.html', context)

# TODO:
def development(request):
    """
    Create a page to show when something isn't working.
    """
    return HttpResponse(
        "We apologize for the inconvenience.\\ At the moment this site is under heavy development."
    )


# TODO:
def clean_wpsresult():
    """
    Delete database entries that have no outputs or that haven't been accessed for a XXX days
    :return:
    """
    return ""


def workflow_run(request):

    if True:
        request_input = json.loads(request.GET.get("processrun"))
        workflow = request_input["workflow"]
        chain = request_input["chain"]
        service = ""
        processes = {}
        inputs = []
        for i in chain:
            if workflow[i]["serv"] != service:
                service = workflow[i]["serv"]
                wps_service_engine = WebProcessingService.objects.filter(
                    name=service
                ).values_list("endpoint", flat=True)[0]
            edited_inputs = edit_input(
                list(
                    itertools.zip_longest(
                        workflow[i].get("key_list", ""),
                        workflow[i].get("value_list", ""),
                        workflow[i].get("inId_list", ""),
                        workflow[i].get("in_type_list", ""),
                    )
                )
            )

            processes[i] = {
                "inputs": edited_inputs,
                "server": wps_service_engine,
                # 'server': workflow[i]['serv'],
                "wps_process": workflow[i]["id"],
            }
            # inputs[i]['inputs'] = edit_input(inputs[i]['inputs'])
        # inputs = list(zip(request_input.get("key_list", ""), request_input.get("value_list", ""),
        #                   request_input.get("in_type_list", "")))
        # inputs = edit_input(inputs)
        wps = get_wps_service_engine("PyWPS_vforwater")
        inputs = [("processlist", json.dumps(processes)), ("chain", json.dumps(chain))]
        execution = wps.execute("workflow", inputs)

        all_outputs = handle_wps_output(execution, "workflow", inputs)
    else:
        all_outputs = {"execution_status": "auth_error"}
        print("user is not authenticated. ", all_outputs)

    return JsonResponse(all_outputs)


def update_tools(request, updateinterval=5):
    """

    :param request:
    :param updateinterval: int Minutes to wait between checks for updates on wps server
    :return:
    """

    updatedwps = []
    wps_data = {}
    jsondata = {}
    tools_for_updatecheck = []
    db_versions = {}
    WpsQueryset = WpsDescription.objects

    wps_services = list_wps_service_engines()
    # service = 'PyWPS_vforwater'
    service = WebProcessingService.objects.values_list("name", flat=True)[0]
    wps = get_wps_service_engine(service)

    updateDates = list(
        WpsQueryset.values("lastUpdateDateCheck", "identifier", "version")
    )
    for process in updateDates:
        timediff = timezone.now() - process["lastUpdateDateCheck"]
        if timediff.total_seconds() / 60 > updateinterval:
            tools_for_updatecheck.append(process["identifier"])
            db_versions[process["identifier"]] = process["version"]
    db_data = list(
        WpsQueryset.filter(identifier__in=tools_for_updatecheck).values(
            "service", "identifier", "version"
        )
    )
    for process in db_data:
        #                                    'processout': process['outputs']}
        if wps_data == {}:
            describedprocess = wps.describeprocess(process['identifier'])
            described_wps = json.loads(jsonpickle.encode(wps, unpicklable=False))
            for i in described_wps["processes"]:
                wps_data[i["identifier"]] = i

        if process["version"] != wps_data[process["identifier"]]["processVersion"]:
            try:
                WpsQueryset.filter(identifier=process["identifier"]).update(
                    service=service,
                    title=wps_data[process["identifier"]]["title"],
                    abstract=wps_data[process["identifier"]]["abstract"],
                    inputs=wps_data[process["identifier"]]["dataInputs"],
                    # inputs=wps_data[process['identifier']]['processin'],
                    outputs=wps_data[process["identifier"]]["processOutputs"],
                    # outputs=wps_data[process['identifier']]['processout'],
                    verbose=wps_data[process["identifier"]]["verbose"],
                    statusSupported=wps_data[process["identifier"]]["statusSupported"],
                    storeSupported=wps_data[process["identifier"]]["storeSupported"],
                    metadata=wps_data[process["identifier"]]["metadata"],
                    dataInputs=wps_data[process["identifier"]]["dataInputs"],
                    processOutputs=wps_data[process["identifier"]]["processOutputs"],
                    version=wps_data[process["identifier"]]["processVersion"],
                )
                # TODO: Figure out why some processes don't have a version here and fix this
                print("*** updated ***")
                updatedwps.append(process["identifier"])
            except Exception as e:
                print("Error while trying to update WpsDescrition: ", e)

    return JsonResponse({"wps": updatedwps})


def get_process_metadata(sessiondata, describedprocess, identifier):
    sessiondata[identifier]["processin"] = []
    sessiondata[identifier]["processout"] = []

    for i in describedprocess.dataInputs:
        if i.allowedValues == [] or not i.allowedValues[0] == "_keywords":
            if i.abstract and len(i.abstract) > 10 and "keywords" in i.abstract[2:10]:
                # TODO: another ugly hack to improve: Problems with allowed values in pywps when min_occurs > 1
                keywords = ast.literal_eval(i.abstract[: 1 + i.abstract.find("}", 10)])[
                    "keywords"
                ]
                sessiondata[identifier]["processin"].append(keywords)
            else:
                sessiondata[identifier]["processin"].append(i.dataType)

        # if i.allowedValues == [] and isinstance(i.dataType, str):
        #     wps.processes[loopCount].processin.append('string')
        # elif i.allowedValues == [] and not isinstance(i.dataType, str):
        #     wps.processes[loopCount].processin.append(i.dataType)
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
            # elif isinstance(i.dataType, float):
            #     wps.processes[loopCount].processout.append('float')
            # elif i.metadata[0] == '_keywords':
            #     wps.processes[loopCount].processout.append(i.allowedValues[1:])

    return sessiondata
