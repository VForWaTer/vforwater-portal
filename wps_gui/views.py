# from inspect import getmembers
import json
import re

import jsonpickle
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.cache import cache
from django.views.generic import TemplateView
from owslib.wps import printInputOutput

from heron.settings import VFW_SERVER, HOST_NAME
from wps_gui.utilities import get_wps_service_engine, list_wps_service_engines, abstract_is_link


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
            if isinstance(i.dataType, str):
                wps.processes[countLoop].processout.append('string')
            elif isinstance(i.dataType, float):
                wps.processes[countLoop].processout.append('float')
            elif i.metadata[0] == '_keywords':
                wps.processes[countLoop].processout.append(i.allowedValues[1:])
        countLoop += 1

    context = {'wps_services': wps_services,
               'wps': wps,
               'service': service,
               }

    return render(request, 'wps_gui/home.html', context)


# def service(request, service):
#     """
#     View that lists the processes for a given service.
#     """
#     wps = get_wps_service_engine(service)
#
#     context = {'wps': wps,
#                'service': service}
#     return render(request, 'wps_gui/service.html', context)


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
                                if k == 'allowedValues' and not v == [] and v[0] == '_keywords':
                                    innerdict['keywords'] = v[1:]
                                elif v is not None and not v == []:
                                    # if not v is None and not v == []:
                                    if isinstance(v, str) and re.search("(?<=/#)\w+", v):
                                        match = re.search("(?<=/#)\w+", v)
                                        innerdict[k] = match.group(0)
                                    else:
                                        innerdict[k] = v
                            list_values.append(innerdict)
                        elif not b is None and not b == []:
                            list_values.append(b)
                    wps_description[a] = list_values
                elif not whole_wpsprocess[a] is None and not whole_wpsprocess[a] == []:
                    wps_description[a] = whole_wpsprocess[a]
            return JsonResponse(wps_description)

        if 'processrun' in request.GET:

            request_input = json.loads(request.GET.get('processrun'))
            inputs = list(zip(request_input.get("key_list", ""), request_input.get("value_list", "")))

            wps = get_wps_service_engine(request_input.get("serv", ""))
            wps_process = request_input.get("id", "")

            execution = wps.execute(wps_process, inputs)
            execution_status = execution.status
            image = []
            outputs = []
            for output in execution.processOutputs:
                outputs.append(output.data)
                output_reference = output.reference
                if type(output.data[0] is str):
                    if len(output.data[0]) > 10:
                        substring = output.data[0][:10]
                        if "img" in substring:
                            image = output.data[0]

            if output_reference:
                output_reference = output_reference.replace('localhost', HOST_NAME)
                # output_reference = output_reference.replace('localhost','vforwater-devel')

            context_p = {'processid': wps_process,
                         'outputs': outputs,
                         'image': image,
                         'output_reference': output_reference,
                         'execution_status': execution_status
                         }

            return JsonResponse(context_p)


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
