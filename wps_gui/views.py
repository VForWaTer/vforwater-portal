# from inspect import getmembers
import json
import re
import sys
import xml.etree.ElementTree as ET
import jsonpickle
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.cache import cache
from django.views.generic import TemplateView
from django.utils import timezone
from owslib.wps import printInputOutput

from heron.settings import VFW_SERVER, HOST_NAME
from vfwheron.models import TblMeta, TblData
from wps_gui.models import WpsResults
from wps_gui.utilities import get_wps_service_engine, list_wps_service_engines, abstract_is_link

import logging
logger = logging.getLogger(__name__)


# from heron_wps.forms import InputForm


def home(request):
    """
    Home page for Heron WPS tool. Lists all the WPS services that are linked.
    """
    wps_services = list_wps_service_engines()

    try:
        service = 'PyWPS_vforwater'
        wps = get_wps_service_engine(service)
    except:
        service = ''
        wps = []

    processin = {}
    processout = {}
    countLoop = 0
    for process in wps.processes:
        describedprocess = wps.describeprocess(process.identifier)
        wps.processes[countLoop].processin = []
        for i in describedprocess.dataInputs:
            if i.allowedValues == [] and isinstance(i.dataType, str):
                wps.processes[countLoop].processin.append('string')
            elif i.allowedValues == [] and isinstance(i.dataType, float):
                wps.processes[countLoop].processin.append('float')
            elif i.allowedValues[0] == '_keywords':
                wps.processes[countLoop].processin.append(i.allowedValues[1:])

        wps.processes[countLoop].processout = []
        for i in describedprocess.processOutputs:
            if i.abstract is not None:
                if 'keywords' in json.loads(i.abstract):
                    wps.processes[countLoop].processout.append(json.loads(i.abstract)['keywords'])
            elif isinstance(i.dataType, str):
                wps.processes[countLoop].processout.append('string')
            elif isinstance(i.dataType, float):
                wps.processes[countLoop].processout.append('float')
            # elif i.metadata[0] == '_keywords':
            #     wps.processes[countLoop].processout.append(i.allowedValues[1:])
        countLoop += 1

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

def get_or_create_wpsdb_entry(service, wps_process, inkey, invalue):
    db_result, created = WpsResults.objects.get_or_create(open=True, wps=wps_process, inputdict=invalue,
                                                          defaults={'creation': timezone.now(),
                                                                    'access': timezone.now()})
    result = {'wps_id': db_result.id}
    if not created:
        db_result.access = timezone.now()
        db_result.save()
    else:
        wps = get_wps_service_engine(service)
        execution = wps.execute(wps_process, [(inkey, invalue)])
        execution_status = execution.status
        if execution_status == "ProcessSucceeded":
            db_result.link = execution.processOutputs[0].data
            db_result.save()
        else:
            db_result.delete()
            result = 'dbload did not work. Please check log file'
            logger.error('get_or create wps execution_status for %s: %s',
                         ((service, wps_process, inkey, invalue), execution_status))
    return result


class ProcessView(TemplateView):

    def get(self, request):

        if 'processview' in request.GET:
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
                    from docutils.writers.html4css1 import Writer, HTMLTranslator
                    from docutils import core
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

        if 'dbload' in request.GET:
            wps_process = 'dbloader_m'
            inkey = 'sql-filter'
            request_input = json.loads(request.GET.get('dbload'))
            result = {}
            for dataset in request_input:
                # TODO: Check if user has rights to access dataset
                if request_input[dataset]['type'] == 'timeseries':
                    invalue = 'SELECT tstamp, value FROM tbl_data WHERE meta_id=' + dataset + ';'
                else:
                    invalue = 'SELECT value FROM tbl_data WHERE meta_id=' + dataset + ';'
                result[dataset] = get_or_create_wpsdb_entry('PyWPS_vforwater', wps_process, inkey, invalue)
            return JsonResponse(result)

        if 'processrun' in request.GET:

            if True:
            # if request.user.is_authenticated:
                request_input = json.loads(request.GET.get('processrun'))
                inputs = list(zip(request_input.get("key_list", ""), request_input.get("value_list", "")))
                inputs = edit_input(inputs)
                wps = get_wps_service_engine(request_input.get("serv", ""))
                wps_process = request_input.get("id", "")
                execution = wps.execute(wps_process, inputs)
                execution_status = execution.status
                image = []
                outputs = []
                # output = edit_outputs(execution.processOutputs)
                for output in execution.processOutputs:
                    outputs.append(output.data)
                    output_reference = output.reference
                    if type(output.data[0]) is str:
                        if len(output.data[0]) > 10:
                            substring = output.data[0][:10]
                            if "img" in substring:
                                image = output.data[0]
                    elif type(output.data[0]) is bytes:
                        if len(output.data[0]) > 30:
                            substring = str(output.data[0][:30])
                            if "xml" in substring:
                                print('XML as input not implemented yet. Got: ', output.data[0])
                                logger.error('XML as input not implemented yet.')
                                # tree = ET.fromstring(output.data[0])
                                # for child in tree:
                                #     print(child.tag, child.attrib)
                                del outputs[-1]

                context_p = {'processid': wps_process,
                             'outputs': outputs,
                             'image': image,
                             'execution_status': execution_status
                             }

                try:
                    #            if output_reference:
                    output_reference = output_reference.replace('localhost', HOST_NAME)
                    context_p.update({'output_reference': output_reference})
                    # output_reference = output_reference.replace('localhost','vforwater-devel')
                except:
                    print('--- no output_reference')
            else:
                context_p = {'execution_status': 'auth_error'}
                print('user is not authenticated. ', context_p)

            return JsonResponse(context_p)


def edit_input(inputs):
    input_dict = dict((x, y) for x, y in inputs)
    for key, value in input_dict.items():
        if key == 'sql-filter':
            input_dict[key] = "SELECT tstamp, value FROM tbl_data WHERE meta_id=" + value + ";"
        if key == 'name_time' and value.isdigit():
            input_dict[key] = "SELECT tstamp, value FROM tbl_data WHERE meta_id=" + value + ";"
        if key == 'name' and value.isdigit():
            input_dict[key] = "SELECT tstamp, value FROM tbl_data WHERE meta_id=" + value + ";"
        if key == 'number' and value.isdigit():
            input_dict[key] = "SELECT tstamp, value FROM tbl_data WHERE meta_id=" + value + ";"

    return [(k, v) for k, v in input_dict.items()]


def get_pickle(ident):
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


def development(request):
    """
    Create a page to show when something isn't working.
    """
    return HttpResponse("We apologize for the inconvenience.\\ At the moment this site is under heavy development.")
