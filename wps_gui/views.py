import ast
import datetime
import itertools
import json
import numbers
import re
import sys
import time

import jsonpickle
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, JsonResponse
from django.http.response import Http404
from django.shortcuts import render
from django.utils.timezone import make_aware
from django.views.generic import TemplateView
from django.utils import timezone

from heron.settings import VFW_SERVER, HOST_NAME
from vfw_home.data_tools import get_accessible_data
from vfw_home.models import Entries, Datatypes
from vfw_home.utilities import entry_has_data
from wps_gui.models import WpsResults, WebProcessingService, WpsDescription
from wps_gui.utilities import (
    get_wps_service_engine,
    list_wps_service_engines,
    abstract_is_link,
)

import logging
logger = logging.getLogger(__name__)
datatypes = [
    "varray",
    "iarray",
    "array",
    "vtimeseries",
    "timeseries",
    "raster",
    "ndarray",
    "vraster",
    "2darray",
    "idataframe",
    "vdataframe",
    "time-dataframe",
    "vtime-dataframe",
    # outdated values:
    "ts-aggregate",
    "ts-pickle",
    "ts-merge",
    "aggregate",
    "pickle",
    "merge",
    "merged-pickle",
    "merged-ts-pickle",
]
basicdatatypes = ["string", "boolean", "float", "integer", "number"]


def home(request):
    """
    Home page for Heron WPS tool. Lists all the WPS services that are linked.
    """
    jsondata = {}
    wps_data = {}
    WpsQueryset = WpsDescription.objects
    try:
        wps_services = list_wps_service_engines()
        service = WebProcessingService.objects.values_list("name", flat=True)[0]
        wps = get_wps_service_engine(service)
    except Exception as e:
        print("Exception in wps_gui.views.home: ", e)

    try:
        for process in wps.processes:
            if process.identifier not in jsondata.keys():
                wps_data[process.identifier] = {}
                wps_data[process.identifier] = {
                    "title": process.title,
                    "abstract": process.abstract,
                    "identifier": process.identifier,
                    "processin": "",
                    "processout": "",
                }
                describedprocess = wps.describeprocess(process.identifier)
                wps_data = get_process_metadata(
                    wps_data, describedprocess, process.identifier
                )

                jsondata[process.identifier] = process_to_json(process)
                describedprocess_json = process_to_json(describedprocess)

    except Exception as e:
        logger.error(sys.exc_info()[0])
        service = ""
        wps_services = []
        print("in except: ", e)

    if "dbloader" in wps_data:
        del wps_data["dbloader"]
    if "datareader" in wps_data:
        del wps_data["datareader"]

    if "workflow" in wps_data:
        del wps_data["workflow"]

    context = {
        "wps_services": wps_services,
        "sessiondata": wps_data,
        "service": service,
    }

    return render(request, "wps_gui/home.html", context)


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

    def get(self, request):
        selected_process = json.loads(request.GET.get("processview"))

        wps = get_wps_service_engine(selected_process["serv"])
        wps_process = wps.describeprocess(selected_process["id"])

        wps_description = process_to_json(wps_process)

        return JsonResponse(wps_description)


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
                            if isinstance(v, str) and re.search("(?<=/#)\w+", v):
                                match = re.search("(?<=/#)\w+", v)
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
                if output.dataType in ["string", "integer"]:
                    single_output["data"] = output.data[0]
                else:
                    single_output["data"] = eval(output.data[0])[0]

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
                single_output["error"] = "no output to write to db"

            all_outputs["result"][output.identifier] = single_output
    return all_outputs


def process_run(request):
    if True:
        request_input = json.loads(request.GET.get("processrun"))
        inputs = list(
            zip(
                request_input.get("key_list", ""),
                request_input.get("value_list", ""),
                request_input.get("in_type_list", ""),
            )
        )
        inputs = edit_input(inputs)
        wps = get_wps_service_engine(request_input.get("serv", ""))
        wps_process = request_input.get("id", "")
        execution = wps.execute(wps_process, inputs)

        all_outputs = handle_wps_output(execution, wps_process, inputs)
    else:
        all_outputs = {"execution_status": "auth_error"}
        print("user is not authenticated. ", all_outputs)

    return JsonResponse(all_outputs)


def db_load(request):
    """
    Function to preload data from database, convert it, and store a pickle of the data
    Example for input for wps dbloader:  [('entry_id', '12'), ('uuid', ''), ('start', '1990-10-31T09:06'),
    ('end', datetime.datetime(2018, 12, 31, 0, 0))]
    :param request: dict
    :return:
    """
    wps_process = "dbloader"
    request_input = json.loads(request.GET.get("dbload"))
    orgid = request_input.get("dataset")
    result = {}

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

    try:
        preloaded_data = WpsResults.objects.get(wps=wps_process, inputs=inputs)
        output = json.loads(preloaded_data.outputs)
        result = {
            "orgid": orgid,
            "id": "wps" + str(preloaded_data.id),
            "type": output["type"],
            "inputs": inputs,
        }
    except ObjectDoesNotExist:
        # collect variables for wps and run wps
        service = WebProcessingService.objects.values_list("name", flat=True)[0]
        wps = get_wps_service_engine(service)
        execution = wps.execute(wps_process, inputs)

        # create output for client
        if execution.status == "ProcessSucceeded":
            for output in execution.processOutputs:
                if output.identifier == "data":
                    path = output.data[0]
                elif output.identifier == "datatype":
                    dtype = output.data[0]
            output = json.dumps({"path": path, "type": dtype})
            # write result to database
            try:
                dbkey = WpsResults.objects.create(
                    open=True,
                    wps=wps_process,
                    inputs=inputs,
                    outputs=output,
                    creation=timezone.now(),
                )
            except Exception as e:
                print("Exception while creating DB entry: ", e)

            result = {
                "orgid": orgid,
                "id": "wps" + str(dbkey.id),
                "type": dtype,
                "inputs": inputs,
                "outputs": output,
            }
        elif execution.status == 'Exception':
            print('WPS error while trying to preload dataset ', inputs)

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
                    if value[0:3] == "wps":
                        ast.literal_eval(WpsResults.objects.get(id=value[3:]).outputs)[
                            "path"
                        ]
                        wps_input.append(
                            (
                                key_value[0],
                                ast.literal_eval(
                                    WpsResults.objects.get(id=value[3:]).outputs
                                )["path"],
                            )
                        )
                    else:
                        wps_input.append(
                            (
                                key_value[0],
                                ast.literal_eval(
                                    WpsResults.objects.get(id=value[5:]).outputs
                                )[0],
                            )
                        )
        elif isinstance(key_value[1], bool) or isinstance(key_value[1], numbers.Number):
            wps_input.append((key_value[0], str(key_value[1])))
        elif key_value[1][0:2] == "db" and key_value[1][2:].isdecimal():
            wps_input.append((key_value[0], key_value[1][2:]))
        elif key_value[1][0:3] == "wps" and key_value[1][3:].isdecimal():
            wps_input.append(
                (
                    key_value[0],
                    ast.literal_eval(
                        WpsResults.objects.get(id=key_value[1][3:]).outputs
                    )["path"],
                )
            )
        elif key_value[0] == "start" or key_value[0] == "end":
            if key_value[1] != "None":
                wps_input.append(
                    (
                        key_value[0],
                        make_aware(
                            datetime.datetime.strptime(
                                key_value[1], "%Y-%m-%d"
                            ).strftime("%Y-%m-%dT%H:%M:%S")
                        ),
                    )
                )
        else:
            wps_input.append((key_value[0], key_value[1]))
    return wps_input


def load_data_local(inputs):
    return

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
            describedprocess = wps.describeprocess(process["identifier"])
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
