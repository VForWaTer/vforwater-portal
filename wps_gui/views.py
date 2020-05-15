# from inspect import getmembers
import ast
import json
import re
import sys
import jsonpickle
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone

from heron.settings import VFW_SERVER, HOST_NAME
from vfwheron.models import TblMeta, TblData
from wps_gui.models import WpsResults
from wps_gui.utilities import get_wps_service_engine, list_wps_service_engines, abstract_is_link

import logging
logger = logging.getLogger(__name__)
datatypes = ['timeseries', 'ts-aggregate', 'ts-pickle', 'ts-merge', 'array', 'aggregate',
              'pickle', 'merge', 'merged-pickle', 'merged-ts-pickle']

# from heron_wps.forms import InputForm


def home(request):
    """
    Home page for Heron WPS tool. Lists all the WPS services that are linked.
    """
    # TODO: Ugly hack because keywords are yet not supported from owslib. Check upcoming versions of owslib!
    try:
        wps_services = list_wps_service_engines()
        service = 'PyWPS_vforwater'
        wps = get_wps_service_engine(service)
        countLoop = 0
        for process in wps.processes:
            describedprocess = wps.describeprocess(process.identifier)
            wps.processes[countLoop].processin = []
            for i in describedprocess.dataInputs:
                if i.allowedValues == [] or not i.allowedValues[0] == '_keywords':
                    if i.abstract and len(i.abstract) > 10 and "keywords" in i.abstract[2:10]:
                        # TODO: another ugly hack to improve: Problems with allowed values in pywps when min_occurs > 1
                        keywords = ast.literal_eval(i.abstract[:1+i.abstract.find("}", 10)])['keywords']
                        wps.processes[countLoop].processin.append(keywords)
                    else:
                        wps.processes[countLoop].processin.append(i.dataType)
                elif i.allowedValues[0] == '_keywords':
                    wps.processes[countLoop].processin.append(i.allowedValues[1:])

            wps.processes[countLoop].processout = []
            for i in describedprocess.processOutputs:
                if 'error' not in i.identifier:
                    if i.abstract is not None:
                        if 'keywords' in json.loads(i.abstract):
                            wps.processes[countLoop].processout.append(json.loads(i.abstract)['keywords'])
                    elif isinstance(i.dataType, str) or isinstance(i.dataType, float):
                        wps.processes[countLoop].processout.append(i.dataType)
            countLoop += 1
    except:
        logger.error(sys.exc_info()[0])
        service = ''
        wps = []
        wps_services = []

    context = {'wps_services': wps_services,
               'wps': wps,
               'service': service,
               }
    return render(request, 'wps_gui/home.html', context)


# TODO: consider also storing the type of the output to the outputs

def get_or_create_wpsdb_entry(service: str, wps_process: str, input: tuple):
    """
    Get or create a database entry.
    :param service: name of the wps service
    :param wps_process: identifier of the wps process
    """
    db_result, created = WpsResults.objects.get_or_create(open=True, wps=wps_process, inputs={input[0]: input[1]},
                                                          defaults={'creation': timezone.now(),
                                                                    'access': timezone.now()})
    result = {'wps_id': db_result.id}
    if not created:
        db_result.access = timezone.now()
        db_result.save()
    else:
        wps = get_wps_service_engine(service)
        execution = wps.execute(wps_process, [input])
        execution_status = execution.status
        wpsError = {}
        if 'Exception' in execution_status:
            result = {'Error': 'dbload did not work. Please check log file'}
            db_result.delete()
            logger.error('Got no result from wps for %s: %s',
                         (service, wps_process, input), execution_status)
        elif execution_status == "ProcessSucceeded" and wpsError['error'] == 'False':
            # if execution_status == "ProcessSucceeded" and not execution.processOutputs[1].data[0]:
            db_result.outputs = execution.processOutputs[0].data
            db_result.save()
        else:
            db_result.delete()
            result = {'Error': 'dbload did not work. Please check log file'}
            logger.error('get_or create wps execution_status for %s: %s',
                         (service, wps_process, input), execution_status)
    return result


def create_wpsdb_entry(wps_process: str, invalue: list, outputs):
    """
    Create a database entry.
    :param wps_process: identifier of the wps process
    :param invalue: list of tuples of input identifier of wps and respective value (e.g. a path)
    """
    db_result = WpsResults.objects.create(open=False, wps=wps_process, inputs=dict(invalue), outputs=outputs,
                                          creation=timezone.now())#, access=timezone.now())
    return db_result.id


class ProcessView(TemplateView):

    def get(self, request):

        if 'processview' in request.GET:
            selected_process = json.loads(request.GET.get('processview'))

            wps = get_wps_service_engine(selected_process['serv'])
            wps_process = wps.describeprocess(selected_process['id'])

            # TODO: use of jsonpickle only to simplify readability of wps_process.
            #  Shouldn't be necessary to use jsonpickle for that. Please improve!
            # simply serialize wps to json
            whole_wpsprocess_json = jsonpickle.encode(wps_process, unpicklable=False)
            # convert to dict to remove unwanted keys and empty values
            whole_wpsprocess = json.loads(whole_wpsprocess_json)
            whole_wpsprocess.pop('_root', None)
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
                                if k == 'allowedValues' and v != [] and v[0] == '_keywords':
                                    innerdict['keywords'] = v[1:]
                                elif k == 'abstract' and v != None:  # and not v == [] and v[0] == '_keywords':
                                    try:
                                        for abst in json.loads(v):
                                            if abst == 'keywords':
                                                innerdict[abst] = json.loads(v)[abst]
                                            else:
                                                innerdict['abstract'] = v
                                    except ValueError:
                                        # print('v: ', v)
                                        innerdict['abstract'] = v
                                elif v is not None and v != []:
                                    # if not v is None and not v == []:
                                    if isinstance(v, str) and re.search("(?<=/#)\w+", v):
                                        match = re.search("(?<=/#)\w+", v)
                                        innerdict[k] = match.group(0)
                                    else:
                                        innerdict[k] = v
                            list_values.append(innerdict)
                        elif not b is None and b != []:
                            list_values.append(b)
                    wps_description[a] = list_values
                elif not whole_wpsprocess[a] is None and whole_wpsprocess[a] != []:
                    wps_description[a] = whole_wpsprocess[a]

            return JsonResponse(wps_description)

        # function to preload data from database, convert it, and store a pickle of the data
        if 'dbload' in request.GET:
            wps_process = 'dbloader_m'
            inkey = 'sql-filter'
            request_input = json.loads(request.GET.get('dbload'))
            result = {}
            for dataset in request_input:
                # TODO: Check if user has rights to access dataset
                if request_input[dataset]['type'] == 'timeseries':
                    invalue = 'SELECT tstamp, value FROM tbl_data WHERE meta_id=' + dataset + ';'
                    datatype = 'ts-pickle'
                else:
                    invalue = 'SELECT value FROM tbl_data WHERE meta_id=' + dataset + ';'
                    datatype = 'pickle'
                datalink = get_or_create_wpsdb_entry('PyWPS_vforwater', wps_process, (inkey, invalue))
                result[dataset] = datalink
                if 'Error' not in datalink:
                    result[dataset]['datatype'] = datatype
            return JsonResponse(result)

        if 'processrun' in request.GET:

            # if request.user.is_authenticated:
            if True:
                request_input = json.loads(request.GET.get('processrun'))
                inputs = list(zip(request_input.get("key_list", ""), request_input.get("value_list", "")))
                inputs = edit_input(inputs)
                wps = get_wps_service_engine(request_input.get("serv", ""))
                wps_process = request_input.get("id", "")
                execution = wps.execute(wps_process, inputs)
                # order output for database
                all_outputs = {'execution_status': execution.status}
                all_outputs['result'] = {}
                path = ''

                for output in execution.processOutputs:
                    one_output = {}

                    if output.identifier == 'error':
                        all_outputs['error'] = output.data[0]

                        if output.data[0] != "False":
                            print('error in wps process: ', output.data[0])
                            all_outputs = {'execution_status': 'error in wps process',
                                           'error': output.data[0]}
                            break
                    else:
                        try:
                            keywords = json.loads(output.abstract)['keywords'][0]
                            one_output['type'] = keywords
                            if 'pickle' in keywords:
                                path = output.data[0]
                        except:
                            one_output['type'] = output.dataType
                            print('no keywords')

                        one_output['data'] = output.data[0]

                        # TODO: Discuss if several outputs should have single or multiple buttons, and
                        #  how to handle errors from WPS (show nothing, everything and user can check what is okay?)
                        if len(output.data[0]) < 300:  # random number, typical pathlength < 260 chars
                            db_output_data = output.data[0]
                        elif path != '':
                            try:
                                file_name = path[:-4] + one_output['type'] + path[-4:]
                                text_file = open(file_name, "w")
                                text_file.write(output.data[0])
                                text_file.close()
                                db_output_data = file_name
                                one_output['data'] = output.data[0]
                            except:
                                print('Warning: no file was created for long string')
                        else:
                            db_output_data = ''


                        if db_output_data != '':
                            db_output = [output.identifier, one_output['type'], db_output_data]
                            # create the db entry
                            wpsid = create_wpsdb_entry(wps_process, inputs, db_output)

                            one_output['wpsID'] = wpsid
                        else:
                            print('*** no output to write to db ***')
                            one_output['error'] = 'no output to write to db'

                        all_outputs['result'][output.identifier] = one_output
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
            else:
                all_outputs = {'execution_status': 'auth_error'}
                print('user is not authenticated. ', all_outputs)

            return JsonResponse(all_outputs)


def edit_input(inputs):
    wps_input = []
    for key_value in inputs:
        if key_value[0] in datatypes and isinstance(key_value[1], list):
            for value in key_value[1]:
                new_pair = (key_value[0], ast.literal_eval(WpsResults.objects.get(id=value[5:]).outputs)[2])
                wps_input.append(new_pair)
        elif key_value[0] in datatypes:
            wps_input.append((key_value[0], ast.literal_eval(WpsResults.objects.get(id=key_value[1][5:]).outputs)[0]))
        elif key_value[0] == 'sql-filter':
            wps_input.append((key_value[0], "SELECT tstamp, value FROM tbl_data WHERE meta_id=" + key_value[1] + ";"))
        elif key_value[0] == 'name_time' and key_value[1].isdigit():
            wps_input.append((key_value[0], "SELECT tstamp, value FROM tbl_data WHERE meta_id=" + key_value[1] + ";"))
        elif key_value[0] == 'name' and key_value[1].isdigit():
            wps_input.append((key_value[0], "SELECT tstamp, value FROM tbl_data WHERE meta_id=" + key_value[1] + ";"))
        elif key_value[0] == 'number' and key_value[1].isdigit():
            wps_input.append((key_value[0], "SELECT tstamp, value FROM tbl_data WHERE meta_id=" + key_value[1] + ";"))
        elif isinstance(key_value[1], bool):
            wps_input.append((key_value[0], str(key_value[1])))
        else:
            wps_input.append(key_value)
    return wps_input


def get_pickle(ident):
    return


def development(request):
    """
    Create a page to show when something isn't working.
    """
    return HttpResponse("We apologize for the inconvenience.\\ At the moment this site is under heavy development.")


def clean_wpsresult():
    """
    Delete database entries that have no outputs or that haven't been accessed for a XXX days
    :return:
    """
    return ""
