# from inspect import getmembers
import ast
import json
import re
import sys
import jsonpickle
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.http.response import Http404
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone

from heron.settings import VFW_SERVER, HOST_NAME
from vfwheron.models import Entries, Datatypes
from vfwheron.views import get_accessible_data, get_dataset
from wps_gui.models import WpsResults, WebProcessingService
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
        # service = 'PyWPS_vforwater'
        service = WebProcessingService.objects.values_list('name', flat=True)[0]
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
                # if i.allowedValues == [] and isinstance(i.dataType, str):
                #     wps.processes[countLoop].processin.append('string')
                # elif i.allowedValues == [] and not isinstance(i.dataType, str):
                #     wps.processes[countLoop].processin.append(i.dataType)
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
                    # elif isinstance(i.dataType, float):
                    #     wps.processes[countLoop].processout.append('float')
                    # elif i.metadata[0] == '_keywords':
                    #     wps.processes[countLoop].processout.append(i.allowedValues[1:])
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

        selected_process = json.loads(request.GET.get('processview'))

        wps = get_wps_service_engine(selected_process['serv'])
        wps_process = wps.describeprocess(selected_process['id'])
        # print('jsonpickle.encode(wps_process): ', jsonpickle.encode(wps_process))
        # for i in wps_process:
        #     print('i: ', i)
        # print('jsonpickle.encode(wps_process, unpicklable=False): ', jsonpickle.encode(wps_process,
        # unpicklable=False))

        # TODO: use of jsonpickle only to simplify readability of wps_process.
        #  Shouldn't be necessary to use jsonpickle for that. Please improve!
        # simply serialize wps to json
        whole_wpsprocess_json = jsonpickle.encode(wps_process, unpicklable=False)
        # print('a: ',whole_wpsprocess_json)
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
                            elif k == 'abstract' and v is not None:  # and not v == [] and v[0] == '_keywords':
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

        return JsonResponse(wps_description)


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
    all_outputs = {'execution_status': execution.status}
    all_outputs['result'] = {}
    path = ''

    loopcount = 0
    for output in execution.processOutputs:
        loopcount += 1

        if output.identifier == 'error':
            error_dict = json.loads(output.data[0])
            all_outputs['error'] = error_dict

            if error_dict['error'] is not False:
                print('error in wps process: ', error_dict)
                all_outputs = {'execution_status': 'error in wps process',
                               'error': error_dict['message']}
                break
        else:
            one_output = {}
            try:
                keywords = json.loads(output.abstract)['keywords'][0]
                one_output['type'] = keywords
                if 'pickle' in keywords:
                    path = output.data[0]
            except TypeError as e:
                one_output['type'] = output.dataType
                print('No keywords (TypeError: {})'.format(e))
            except KeyError as e:
                print('this is a key error: ', e)

            if output.data:
                one_output['data'] = output.data[0]

            # TODO: Discuss if several outputs should have single or multiple buttons, and
            #  how to handle errors from WPS (show nothing, everything and user can check what is okay?)
            if output.data and len(output.data[0]) < 300:  # random number, typical pathlength < 260 chars
                db_output_data = output.data[0]
            elif path != '':
                try:
                    file_name = path[:-4] + one_output['type'] + path[-4:]
                    text_file = open(file_name, "w")
                    text_file.write(output.data[0])
                    text_file.close()
                    db_output_data = file_name
                    one_output['data'] = output.data[0]
                except Exception as e:
                    print('Warning: no file was created for long string')
                    print(e)
            else:
                db_output_data = ''

            if db_output_data != '':
                db_output = [output.identifier, one_output['type'], db_output_data]
                # create db entry
                wpsid = create_wpsdb_entry(wps_process, inputs, db_output)

                one_output['wpsID'] = wpsid
                one_output['dropBtn'] = {'orgid': wpsid,
                                         'type': 'data',
                                         'name': '',
                                         'inputs': [],
                                         'outputs': [one_output['type']]}
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
    return all_outputs


# @login_required
def process_run(request):
    # if request.user.is_authenticated:
    if True:
        request_input = json.loads(request.GET.get('processrun'))
        inputs = list(zip(request_input.get("key_list", ""), request_input.get("value_list", "")))
        inputs = edit_input(inputs)
        wps = get_wps_service_engine(request_input.get("serv", ""))
        wps_process = request_input.get("id", "")
        execution = wps.execute(wps_process, inputs)

        all_outputs = handle_wps_output(execution, wps_process, inputs)

    else:
        all_outputs = {'execution_status': 'auth_error'}
        print('user is not authenticated. ', all_outputs)

    return JsonResponse(all_outputs)


def db_load(request):
    """
    Function to preload data from database, convert it, and store a pickle of the data
    Example for input for wps dbloader:  [('entry_id', '12'), ('uuid', ''), ('start', '1990-10-31T09:06'),
    ('end', '2020-11-21T09:07')]
    :param request: dict
    :return:
    """
    wps_process = 'dbloader'
    request_input = json.loads(request.GET.get('dbload'))
    orgid = request_input.get('dataset')
    accessible_data = get_accessible_data(request, orgid[2:])
    accessible_data = accessible_data['open']

    if len(accessible_data) < 1:
        return JsonResponse({'Error': 'No accessible dataset.'})
    elif len(accessible_data) > 1:
        return JsonResponse({'Error': 'You have to adjust function for list of datasets.'})

    inputs = list(zip(request_input.get("key_list", ""), request_input.get("value_list", "")))
    inputs = edit_input(inputs)

    try:
        preloaded_data = WpsResults.objects.get(wps=wps_process, inputs=inputs)
        output = json.loads(preloaded_data.outputs)
        result = {'orgid': orgid, 'id': 'wps' + str(preloaded_data.id), 'type': output['type'], 'inputs': inputs}
    except ObjectDoesNotExist:
        # collect variables for wps and run wps
        service = WebProcessingService.objects.values_list('name', flat=True)[0]
        wps = get_wps_service_engine(service)
        execution = wps.execute(wps_process, inputs)

        # create output for client
        if execution.status == 'ProcessSucceeded':
            for output in execution.processOutputs:
                if output.identifier == 'data':
                    path = output.data[0]
                elif output.identifier == 'datatype':
                    dtype = output.data[0]
            output = json.dumps({'path': path, 'type': dtype})
            # write result to database
            try:
                dbkey = WpsResults.objects.create(open=True, wps=wps_process, inputs=inputs, outputs=output,
                                                  creation=timezone.now())
            except Exception as e:
                print('Exception while creating DB entry: ', e)
            result = {'orgid': orgid, 'id': 'wps' + dbkey.id, 'type': dtype, 'inputs': inputs}
    except Exception as e:
        print('Exception in db_load: ', e)
        raise Http404

    return JsonResponse(result)


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
        elif key_value[0] == 'start' and key_value[1] == '':
            pass
            # wps_input.append((key_value[0], '0, 0'))
        elif key_value[0] == 'end' and key_value[1] == '':
            pass
            # wps_input.append((key_value[0], '0, 0'))
        elif isinstance(key_value[1], bool):
            wps_input.append((key_value[0], str(key_value[1])))
        else:
            wps_input.append(key_value)
    return wps_input


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
#         for input in wps_process.dataInputs:
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
    return HttpResponse("We apologize for the inconvenience.\\ At the moment this site is under heavy development.")

# TODO:
def clean_wpsresult():
    """
    Delete database entries that have no outputs or that haven't been accessed for a XXX days
    :return:
    """
    return ""
