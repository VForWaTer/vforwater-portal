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

import datetime
import itertools
import json
import sys
import time
import os
import urllib
import zipfile
from pathlib import Path
from io import BytesIO
from urllib.parse import urlparse

import jsonpickle
import requests
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.utils import translation, timezone
from json2html import json2html

from heron.settings import DEBUG , BASE_DIR #, GEOAPI_DATA_PATH, PROCESSES_DATA
from wps_gui.models import WpsResults, WebProcessingService, WpsDescription, GeoAPIResults
from wps_gui.utilities import (
    get_wps_service_engine, list_wps_service_engines, get_endpoint_data, get_process_basics, get_process_info,
    prepare_inputs, create_geoapi_db_entry, has_result_error, process_to_json, get_url_json, edit_input,
    handle_wps_output, get_user_results, run_pygeoapi_process, url_join
)
from owslib.ogcapi.processes import Processes as getProcesses

import logging

logger = logging.getLogger(__name__)


"""
Not every Tool we have should be available for everyone. E.g. because they are in development.
The following dict defines who can see which tools.
default is accessible for everyone after log-in, the rest only for admins or on devel environments.
"""
TOOLDICT = {
    "default": ["vforwater_loader", "dataset_profiler", "variogram", "combined_loader_whitebox"],
    "short_running_debug": ["hello-world"],  # available for any user in debug mode
    "short_running": [],  # available for any user, also if not logged in
}


def home(request):
    ogcapi_proc = {}
    message = ""

    if request.user:
        results = get_user_results(request.user.id)
    else:
        results = []

    service, endpoint, wps_services = get_endpoint_data(DEBUG)

    if service == 'pygeoapi_vforwater':  # Do we need this 'if'?
        try:
            apiproc = getProcesses(endpoint)
            # load process description according to user and devel state
            for process in apiproc.processes():
                if DEBUG and request.user.is_superuser:  # in debug mode or for superusers show all tools
                    ogcapi_proc[process['id']] = get_process_basics(apiproc.process(process['id']))
                elif DEBUG and process['id'] in TOOLDICT['short_running_debug']:
                    ogcapi_proc[process['id']] = get_process_basics(apiproc.process(process['id']))

                elif request.user.id and process['id'] in TOOLDICT['default']:  # if logged in show more tools
                    ogcapi_proc[process['id']] = get_process_basics(apiproc.process(process['id']))
                elif process['id'] in TOOLDICT['short_running']:
                    ogcapi_proc[process['id']] = get_process_basics(apiproc.process(process['id']))
                    message = translation.gettext("You have to log in to see more Tools.")

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
        # workflow is kind of a helper process. It is called when several process are connected to call the workflow.
        # So the user should call this implicitly by creating a workflow and shouldn't be shown in the list of tools.
        # if "workflow" in ogcapi_proc:
        #     del ogcapi_proc["workflow"]

        context = {
            "wps_services": wps_services,
            "processes": ogcapi_proc,
            "service": service,
            "message": message,
            "results": results
        }

        return render(request, "wps_gui/home.html", context)


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
            process_description = get_process_info(apiproc.process(selected_process['id']))
        else:
            wps = get_wps_service_engine(selected_process["serv"])
            wps_process = wps.describeprocess(selected_process["id"])

            process_description = process_to_json(wps_process)

        return JsonResponse(process_description)


def process_run(request):  # TODO: Maybe check if identical input exists in db before starting the process again
    user_id = None

    try:
        user_id = request.user.id
        user_queryset = User.objects.get(id=user_id)
    except User.DoesNotExist as e:
        logger.error('User does not exist when running a process: ', e)
        user_queryset = None

    process_description = ""
    try:
        if request.GET.get('processrun'):
            request_inputs = request.GET.get('processrun')
        else:
            request_inputs = request.POST.get('processrun')

        input = prepare_inputs(request=request, request_input=json.loads(request_inputs))
    except Exception as e:
        logger.error(f'Problems preparing inputs {e}')

    wps_process = input.get("id", "")

    if input['serv'] == 'pygeoapi_vforwater':
        service, endpoint, wps_services = get_endpoint_data(DEBUG)
        apiproc = getProcesses(endpoint)
        process_description = get_process_info(apiproc.process(wps_process))
    else:
        logger.error(f'Cannot run process. Server "{input["serv"]}" is unknown.')

    try:
        execution = requests.post(f'{endpoint}/processes/{wps_process}/execution',
                              json={
                                  "mode": "async",
                                  'inputs': {**input.get("in_dict", ""),
                                             'User-Info':  # plant the username in last moment
                                                 f'user{user_id}_{request.user.username}'}
                              },
                              headers={'Content-Type': 'application/json',
                                       }
                              )
    except Exception as e:
        logger.error(f'Cannot Execute process: {e}.')

    job_path = urlparse(execution.headers['Location']).path
    db_data = {'inputs': input.get("in_dict", ""),
               'name': wps_process,
               'open': False if user_id else True,
               'outputs': {
                   'path': job_path,
                   'jobMeta_path': f"{job_path}?f=json",
                   'results': ""
                           },
               }

    if execution.status_code == 201:  # if request is created
        # Save the job url for later use
        db_data['status'] = 'CREATED'
        newEntry = create_geoapi_db_entry(db_data, user_queryset)
    elif execution.status_code == 202:  # if request is accepted
        db_data['status'] = 'ACCEPTED'
        newEntry = create_geoapi_db_entry(db_data, user_queryset)
    elif execution.status_code == 200:  # if done
        if has_result_error(db_data):
            db_data['status'] = 'ERROR'
        else:
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
        logger.error(f'Error creating database entry for process result: {newEntry["error"]}')
        result = {'error': 'true'}

    return JsonResponse(result)


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
        user_id = request.user.id
        user_queryset = User.objects.get(id=user_id)
    except User.DoesNotExist as e:
        print('User does not exist when running a process: ', e)
        user_id = None
        user_queryset = None

    except Exception as e:
        logger.error(f'Got no ID to delete process: {e}')
        return JsonResponse({'error': 'Got no ID to delete process.'})

    try:
        entry = GeoAPIResults.objects.filter(owner_id=user_queryset).get(id=process_id)
    except Exception as e:
        logger.error(f'Unable to delete not existing dataset: {e}')
        return JsonResponse({'error': 'Deletion of dataset did not work.',
                             'report': {'status': {'server': 'failed', 'db': 'failed'},
                                        'error': f'Unable to delete dataset. {e}'},
                             'message': 'delete'})

    try:
        tinydb_entry_name = f"{entry.name}-{entry.outputs['path'].replace('/jobs/', '')}"
        input = {'in_dict': {'input_folders': [entry.outputs['results'][0]['json']['dir'].split("out", 1)[1]],
                             'output_folders': [entry.outputs['results'][0]['json']['dir'].split("out", 1)[1]],
                             'job_list': [tinydb_entry_name]}}
        service, endpoint, wps_services = get_endpoint_data(DEBUG)
        execution = run_pygeoapi_process(endpoint, 'result_remover', input, user_id, request.user.username)

        deletion_report = {'status': {'server': execution.status_code},
                           'report': get_url_json(f'{execution.headers["Location"]}/results?f=json'),
                           'error': ''}
    except Exception as e:
        logger.error(f'Unable to delete dataset: {e}')
        deletion_report = {'status': {'server': 'failed'},
                           'error': f'Unable to delete dataset. {e}'}

    try:
        entry.delete()
        deletion_report['status']['db'] = 'done'
    except Exception as e:
        logger.error(f'Unable to delete result from db: {e}')
        deletion_report['status']['db'] = 'failed'
        deletion_report['error'] = f"{deletion_report['error']}; Delete from DB failed with {e}"

    if deletion_report['status'] == '201':
        return JsonResponse({'report': deletion_report,
                             'message': 'delete'})
    else:
        return JsonResponse({'error': 'Deletion of folders did not work.',
                             'report': deletion_report,
                             'message': 'delete'})


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
        logger.error(f'Got no ID to check process state: {e}')
        return JsonResponse({'error': 'Got no ID to check process state.'})

    # get element from database
    try:
        entry = GeoAPIResults.objects.get(id=process_id)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': f"Cannot check state of Process. Entry {process_id} seems not to exist"})

    # check if user has access to this dataset. If yes get state from GeoAPI
    if entry.open or request.user.id == entry.owner_id:
        service, endpoint, wps_services = get_endpoint_data(DEBUG)
        url = url_join(endpoint, entry.outputs['path'])
        logger.info(f'try to get process state from url: {url}')
        update = get_url_json(f'{url}?f=json')
    else:
        return JsonResponse({'error': 'No Access'})

    # check status. If successful update database and send update
    if ((update['status'] == "successful" or update['status'] == "completed") and update['message'] == 'Job complete'
        and update['progress'] == 100):

        result_url = f'{url}/results?f=json'
        result = get_url_json(result_url)
        if result["container_status"] and result["container_status"] == 'failed':
            entry.status = "FINISHED"
            entry.access = timezone.now().isoformat()
        elif result["container_status"] and result["container_status"] == 'exited':
            entry.status = "FINISHED"
            entry.access = timezone.now().isoformat()
        elif ((result["error"] and result["error"] == 'none') and
              (result["geoapi_status"] and result["completed"] == 'none')):
            entry.status = "FINISHED"
            entry.access = timezone.now().isoformat()
        else:
            entry.status = "ERROR"
            entry.access = timezone.now().isoformat()
            logger.error(f'Process failed but container was able to finish: {update}')

        entry.outputs['results'] = [{'path': result_url, 'json': result}]
        try:
            entry.save()

        except ValueError as e:
            logger.error(f'ValueError while trying to update DB: {e}')

        except Exception as e:
            logger.error(f'Unexpected error while trying to update DB: {e}')
    elif (update['status'] == "failed" and update['message'] == 'InvalidParameterValue: Error updating job'
          and update['progress'] < 10):
        logger.error(f'Process failed immediately: {update}')
        return JsonResponse({'status': entry.status, 'error': 'Invalid Parameter Value'})
    elif update['status'] == "accepted":
        return JsonResponse({'status': entry.status})
    else:
        logger.error(f'New style of result in dataset. Status, message, or progress is not as expected. {update}')
        # style is the combination of 'status', 'message' and 'progress'

    try:
        response_dict = {'status': entry.status,
                     'results': [{'path': result_url, 'json': result, 'html': json2html.convert(json=result)}]
                     }
    except Exception as e:
        logger.error(f"Unexpected error while trying to refresh client: {e}")

    return JsonResponse(response_dict)


def development(request):
    """
    Create a page to show when something isn't working.
    """
    return HttpResponse(
        "We apologize for the inconvenience.\\ At the moment this site is under heavy development."
    )


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
                "wps_process": workflow[i]["id"],
            }
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
                    outputs=wps_data[process["identifier"]]["processOutputs"],
                    verbose=wps_data[process["identifier"]]["verbose"],
                    statusSupported=wps_data[process["identifier"]]["statusSupported"],
                    storeSupported=wps_data[process["identifier"]]["storeSupported"],
                    metadata=wps_data[process["identifier"]]["metadata"],
                    dataInputs=wps_data[process["identifier"]]["dataInputs"],
                    processOutputs=wps_data[process["identifier"]]["processOutputs"],
                    version=wps_data[process["identifier"]]["processVersion"],
                )
                updatedwps.append(process["identifier"])
            except Exception as e:
                print("Error while trying to update WpsDescrition: ", e)

    return JsonResponse({"wps": updatedwps})


@method_decorator(login_required(login_url="/login/"), name='dispatch')
class ToolResultsDownload(TemplateView):
    """
    View to handle the download of tool results as a zip file.
    Requires user to be authenticated.
    """

    def get(self, request):
        if 'zip' in request.GET and 'path' in request.GET:
            directory_path = request.GET['path']
            logger.info(f'directory_path: {directory_path}')

            if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
                logging.error(f"Requested path does not exist or is not a directory: {directory_path}")
                return HttpResponse(status=404)

            zip_filename = "geo_data.zip"
            response = HttpResponse(content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
            buffer = BytesIO()

            with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for root, _, files in os.walk(directory_path):
                    for file in files:
                        if not file.endswith((".zip", ".log")):
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, start=directory_path)
                            zip_file.write(file_path, arcname=arcname)

            buffer.seek(0)
            response.write(buffer.read())
            return response
        else:
            logging.error("Missing required query parameters.")
            return HttpResponse(status=400)


@method_decorator(login_required(login_url="/login/"), name='dispatch')
class FileDownloadView(View):
    def get(self, request):
        file_path = request.GET.get('path')
        logger = logging.getLogger(__name__)

        if not file_path:
            logger.error("Missing 'path' parameter.")
            return HttpResponse("Missing 'path' parameter.", status=400)

        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            logger.error(f"File does not exist: {file_path}")
            return HttpResponse("File not found.", status=404)

        try:
            return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        except Exception as e:
            logger.exception(f"Error while reading file: {e}")
            return HttpResponse("Failed to read the file.", status=500)
