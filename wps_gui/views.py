# =================================================================
#
# Authors: Marcus Strobl <marcus.strobl@kit.edu>
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

# from inspect import getmembers
import datetime
import itertools
import json
import sys
import time
import os
import tempfile
import urllib
import zipfile
from pathlib import Path
from io import BytesIO
from urllib.parse import urlparse

import jsonpickle
import requests
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.utils import translation, timezone
from django.views.decorators.clickjacking import xframe_options_sameorigin
from json2html import json2html
from heron.settings import DEBUG , BASE_DIR, PROCESSES_IN_DIR, PROCESSES_OUT_DIR , GEOAPI_DATA_PATH, PROCESSES_DATA

from wps_gui.models import WpsResults, WebProcessingService, WpsDescription, GeoAPIResults
from wps_gui.utilities import (
    get_wps_service_engine, list_wps_service_engines, get_endpoint_data, get_process_basics, get_process_info,
    prepare_inputs, create_geoapi_db_entry, has_result_error, process_to_json, get_url_json, edit_input,
    handle_wps_output, get_user_results, run_pygeoapi_process, url_join, extract_jobid, update_geoapi_jobs_db,
    get_job_status, fetch_jobs_table, update_job_results, fetch_job_details
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

    "default": ["vforwater_loader", "dataset_profiler", "variogram", "combined_loader_whitebox", "combined_loader_simulation_evaluation"],
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

    if service == 'pygeoapi_vforwater':  
        try:
            apiproc = getProcesses(endpoint)
          
            for process in apiproc.processes():
                if DEBUG and request.user.is_superuser: 
                    ogcapi_proc[process['id']] = get_process_basics(apiproc.process(process['id']))
                elif DEBUG and process['id'] in TOOLDICT['short_running_debug']:
                    ogcapi_proc[process['id']] = get_process_basics(apiproc.process(process['id']))
                # Keep below line for now in case we need to revert to it
                #elif request.user.id and process['id'] in TOOLDICT['default']:  
                elif process['id'] in TOOLDICT['default']:  # if logged in show more tools
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

        # Fetch jobs table per user as well
        jobs, job_table_fields = fetch_jobs_table(request.user.id)
        context = {
            "wps_services": wps_services,
            "processes": ogcapi_proc,
            "service": service,
            "message": message,
            "results": results,
            "jobs": jobs,
            "job_table_fields": job_table_fields 
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
    )  
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


def process_run(request):  
    user_id = None
    temp_dir = None
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


        if "model_file" in request.FILES:
            uploaded = request.FILES["model_file"]

            import os
            from uuid import uuid4

            user_folder = f"user{user_id}_{request.user.username}"
            shared_id = f"upload_{uuid4().hex}"

            # local mounted path 
            # BASE_SHARED_PATH = os.path.expanduser("~/remote_geoapi_data")
            # obs_dir = os.path.join(
            #     BASE_SHARED_PATH,
            #     "in",
            #     user_folder,
            #     shared_id,
            #     "simulation",
            #     "obs"
            # )

            # Mount
            BASE_SHARED_PATH = GEOAPI_DATA_PATH 
            obs_dir = os.path.join(
                BASE_SHARED_PATH,
                "in",
                user_folder,
                shared_id,
                "simulation",
                "obs"
            )

            os.makedirs(obs_dir, exist_ok=True)

            file_path = os.path.join(obs_dir, uploaded.name)

            with open(file_path, "wb+") as dst:
                for chunk in uploaded.chunks():
                    dst.write(chunk)

            print(f"Uploaded observation file saved at: {file_path}")

            # pass path to processor
            input.setdefault("in_dict", {})
            input["in_dict"]["observation_data"] = file_path

            # pass shared_id so processor uses same folder
            input["in_dict"]["shared_id"] = shared_id



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
        logger.info(f'Attempting to execute process {wps_process} at endpoint {endpoint}')
        print(f'Attempting to execute process {wps_process} at endpoint {endpoint}')
        execution = requests.post(f'{endpoint}/processes/{wps_process}/execution',
                              json={
                                  "mode": "async",
                                 
                                  'inputs': {**input.get("in_dict", ""),
                                             'User-Info':  # plant the username in last moment
                                                 f'user{user_id}_{request.user.username}'}
                                      # input.get("in_dict", ""),
                                  # "response": "document"  # this line adds {'outputs': [{result}]} to {result}
                              },
                              headers={'Content-Type': 'application/json',
                                        'Prefer': 'respond-async'  # TODO: Use this for PyGeoAPI 0.16 and newer
                                       }
                              )
    except Exception as e:
        print('e: ', e)
        logger.error(f'Cannot Execute process: {e}.')

    job_path = urlparse(execution.headers['Location']).path
    # TODO: absolute path is bad design, is a problem when accessing data from different machines. Better: store
    #  only path and create endpoint + path when needed.
    db_data = {'inputs': input.get("in_dict", ""),
               'name': wps_process,
               'open': False if user_id else True,
               'outputs': {
                   'path': job_path,
                   # 'path': urljoin(endpoint, job_path),
                   # 'path': execution.headers['Location'],
                   'jobMeta_path': f"{job_path}?f=json",
                   # 'jobMeta_path': f"{execution.headers['Location']}?f=json",
                   'results': ""
                           # 'results': f"{execution.headers['Location']}/results?f=json"
                           },
               # 'user': user_id,
               }
    
    job_id = extract_jobid(job_path)
    job_db_response = update_geoapi_jobs_db(user_queryset, job_id)

    job_status = get_job_status(job_id)
    job_details = fetch_job_details(job_id)
    
    db_data["status"] = job_status
    db_data["id"] = job_id
    db_data['job_details'] = job_details

    #print("JOB STATUS - ", job_status)

    result = db_data
    return JsonResponse(result)


#@csrf_exempt  # Use this only for testing; in production, ensure CSRF protection is properly configured
def job_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse the JSON body
            job_id = data.get('job_id')  # Extract the job_id
            if not job_id:
                return JsonResponse({'error': 'job_id is required'}, status=400)

            status = get_job_status(job_id) 
            if status:
                if status in ['successful', 'completed', 'failed', 'dismissed']:
                    service, endpoint, wps_services = get_endpoint_data(DEBUG)

                    JOB_RESULT_URL = f'{endpoint}/jobs/{job_id}/results?f=json'

                    try:
                        execution = requests.get(JOB_RESULT_URL, headers={'Content-Type': 'application/json'})
                        update_response = update_job_results(job_id, execution.json())
                        if update_response == False:
                            logger.error(f'Error updating job results for job {job_id}')
                            return JsonResponse({'error': 'Error updating job results'}, status=500)
                        job_details = fetch_job_details(job_id)
                        if not job_details:
                            logger.error(f'Error fetching job details for job {job_id}')
                            return JsonResponse({'error': 'Error fetching job details'}, status=500)
                        resp = {'status': job_details['status'], 'job_details': job_details, 'html': json2html.convert(job_details['results'])}
                        return JsonResponse(resp, status=200, safe=False)
                    except Exception as e:
                        logger.error(f'Error fetching job results: {e}')
                        return JsonResponse({'error': 'Error fetching job results'}, status=500)
                    
                return JsonResponse({'status': status})
            else:
                return JsonResponse({'error': 'Job not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


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
        # TODO: is it a good solution to have a tool to delete results? Think about how to delete directly from django
        tinydb_entry_name = f"{entry.name}-{entry.outputs['path'].replace('/jobs/', '')}"
        # tinydb_entry_name = f"{entry.name}-{urllib.parse.urlparse(entry.outputs['path']).path.replace('/jobs/', '')}"
        input = {'in_dict': {'input_folders': [entry.outputs['results'][0]['json']['dir'].split("out", 1)[1]],
                             'output_folders': [entry.outputs['results'][0]['json']['dir'].split("out", 1)[1]],
                             'job_list': [tinydb_entry_name]}}
        service, endpoint, wps_services = get_endpoint_data(DEBUG)
        execution = run_pygeoapi_process(endpoint, 'result_remover', input, user_id, request.user.username)

        # TODO: this report isn't used yet, but might be of interest in future
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



@never_cache
def process_state(request):
    """
    Check the state of a process in GeoAPI and store updates in DB.
    """
    # 1)  check if request includes a process id
    try:
        process_id = int(request.GET.get('processid'))
    except Exception as e:
        logger.error(f'Got no ID to check process state: {e}')
        return JsonResponse({'error': 'Got no ID to check process state.'}, status=400)

    # 2) Load DB entry
    try:
        entry = GeoAPIResults.objects.get(id=process_id)
    except ObjectDoesNotExist:
        return JsonResponse({'error': f"Cannot check state of Process. Entry {process_id} seems not to exist"}, status=404)

    # 3) Permission check
    if not (entry.open or request.user.id == entry.owner_id):
        return JsonResponse({'error': 'No Access'}, status=403)

    # 4) Fetch update JSON (job status)
    service, endpoint, wps_services = get_endpoint_data(DEBUG)
    url = url_join(endpoint, entry.outputs['path'])
    logger.info(f'try to get process state from url: {url}')

    update = None
    try:
        update = get_url_json(f'{url}?f=json')
        if update.get("error"):
            logger.error(f"PyGeoAPI status check error: {update['error']}")
            return JsonResponse({"status": entry.status, "error": update["error"]}, status=502)
    except Exception as e:
        # get_url_json likely failed to parse JSON (empty/html/etc.)
        logger.error(f'Error checking state of process (get_url_json failed): {e}')
        return JsonResponse({'status': entry.status, 'error': 'Invalid/non-JSON status response'}, status=502)

    if not isinstance(update, dict) or not update:
        logger.error(f'Empty/invalid update payload: {update}')
        return JsonResponse({'status': entry.status, 'error': 'Empty/invalid status payload'}, status=502)

    # 5) Read keys safely (avoid KeyError)
    upd_status = update.get('status')
    upd_message = update.get('message')
    upd_progress = update.get('progress')


    if upd_status is None:
        upd_status = update.get('state') or update.get('job_status')
    if upd_progress is None:
        upd_progress = update.get('percent') or update.get('percentage') or update.get('progress_percent')

    # 6) Prepare defaults so response always works
    result_url = None
    result = None

    # same logic with safe access
    if ((upd_status in ("successful", "completed")) and upd_message == 'Job complete' and upd_progress == 100):

        result_url = f'{url}/results?f=json'
        try:
            result = get_url_json(result_url)
        except Exception as e:
            logger.error(f'Could not fetch results JSON: {e}')
            entry.status = "ERROR"
            entry.access = timezone.now().isoformat()
            entry.save()
            return JsonResponse({'status': entry.status, 'error': 'Could not fetch results JSON'}, status=502)

        # container_status checks safely
        container_status = (result or {}).get("container_status")
        err = (result or {}).get("error") or (result or {}).get("error:")  
        geoapi_status = (result or {}).get("geoapi_status")
        completed = (result or {}).get("completed")

        if container_status in ('failed', 'exited'):
            entry.status = "FINISHED"
        elif (err == 'none' and geoapi_status and completed == 'none'):
            entry.status = "FINISHED"
        else:
            entry.status = "ERROR"
            logger.error(f'Process finished but result indicates error. update={update}, result={result}')

        entry.access = timezone.now().isoformat()
        entry.outputs['results'] = [{'path': result_url, 'json': result}]
        try:
            entry.save()
        except Exception as e:
            logger.error(f'Error while trying to update DB: {e}')

    elif (upd_status == "failed" and upd_message == 'InvalidParameterValue: Error updating job'
          and isinstance(upd_progress, (int, float)) and upd_progress < 10):
        logger.error(f'Process failed immediately: {update}')
        return JsonResponse({'status': entry.status, 'error': 'Invalid Parameter Value'})

    elif upd_status == "accepted":
        return JsonResponse({'status': entry.status})

    else:
        logger.error(f'Unexpected job status schema or values. update={update}')

    #  Response to client (always defined)
    response_dict = {'status': entry.status}
    if result_url and result is not None:
        try:
            response_dict['results'] = [{'path': result_url, 'json': result, 'html': json2html.convert(json=result)}]
        except Exception as e:
            logger.error(f"Error while converting results to html: {e}")
            response_dict['results'] = [{'path': result_url, 'json': result}]
    resp = JsonResponse(response_dict)
    resp["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    resp["Pragma"] = "no-cache"
    resp["Expires"] = "0"
    return resp
    # return JsonResponse(response_dict)


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

# def date_to_datetime(date_string):
#
# return datetime_string

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


def move_job(request):
    """
    Fetch job details from the DB by identifier and return them as JSON,
    so the frontend can populate the result card with a historical job.
    """
    job_id = request.GET.get('job_id')
    if not job_id:
        return JsonResponse({'error': 'job_id is required'}, status=400)
    job_details = fetch_job_details(job_id)
    if not job_details:
        return JsonResponse({'error': 'Job not found'}, status=404)
    resp = {'status': job_details['status'], 'job_details': job_details, 'html': json2html.convert(job_details['results'])}
    return JsonResponse(resp, status=200, safe=False)


@method_decorator(login_required(login_url="/login/"), name='dispatch')
class ToolResultsDownload(TemplateView):
    """
    View to handle the download of tool results as a zip file.
    Requires user to be authenticated.
    """

    def get(self, request):
        if 'zip' in request.GET and 'path' in request.GET:
            directory_path = request.GET['path']
            print('directory_path: ', directory_path)
            logger.info(f'directory_path: {directory_path}')
            # if directory_path.startswith(GEOAPI_DATA_PATH):
            #     directory_path = directory_path.replace(GEOAPI_DATA_PATH, PROCESSES_DATA, 1)

            if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
                logging.error(f"Requested path does not exist or is not a directory: {directory_path}")
                # logging.error(f"You might want to check if path from geoapi container is correct (GEOAPI_DATA_PATH = {GEOAPI_DATA_PATH})")
                # logging.error(f"You might want to check if path from django container is correct (PROCESSES_DATA = {PROCESSES_DATA})")
                # print(f"You might want to check if path from geoapi container is correct (GEOAPI_DATA_PATH = {GEOAPI_DATA_PATH})")
                # print(f"You might want to check if path from django container is correct (PROCESSES_DATA = {PROCESSES_DATA})")

                print(f"Requested path does not exist or is not a directory: {directory_path}")
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
@method_decorator(xframe_options_sameorigin, name='dispatch')
class FileDownloadView(View):
    def get(self, request):
        file_path = request.GET.get('path')
        logger = logging.getLogger(__name__)
        #print('i m here')
        #print(BASE_DIR)
        #file_path = os.path.join(BASE_DIR, 'spatial_data.pdf')

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
