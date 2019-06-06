# from inspect import getmembers
import json

import jsonpickle
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.cache import cache
from django.views.generic import TemplateView

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

    context = {'wps_services': wps_services,
               'wps': wps,
               'service': service}
    return render(request, 'wps_gui/home.html', context)


def service(request, service):
    """
    View that lists the processes for a given service.
    """
    print('++++fdaasg++++++++++++  1: ', request)
    print('+++++++afg+++++++++  1: ', service)
    wps = get_wps_service_engine(service)

    context = {'wps': wps,
               'service': service}
    return render(request, 'wps_gui/service.html', context)


class ProcessView(TemplateView):

    def get(self, request):

        if 'processview' in request.GET:
            selected_process = json.loads(request.GET.get('processview'))

            wps = get_wps_service_engine(selected_process['serv'])
            wps_process = wps.describeprocess(selected_process['id'])
            result = {'abstract': wps_process.abstract,
                      'identifier': wps_process.identifier,
                      'title': wps_process.title,
                      'statusSupported': wps_process.statusSupported,
                      'storeSupported': wps_process.storeSupported,
                      'verbose': wps_process.verbose}
            if wps_process.processVersion is not None:
                result['processVersion'] = wps_process.processVersion

            for wpsoutput in wps_process.processOutputs:
                if 'processOutputs' not in result:
                    result['processOutputs'] = {}
                result['processOutputs'][wpsoutput.identifier] = {'dataType': wpsoutput.dataType,
                                                                  'anyValue': wpsoutput.anyValue,
                                                                  'data': wpsoutput.data,
                                                                  'defaultValue': wpsoutput.defaultValue,
                                                                  'title': wpsoutput.title,
                                                                  }
                if wpsoutput.abstract is not None:
                    result['processOutputs'][wpsoutput.identifier]['abstract'] = wpsoutput.abstract
                if not isinstance(wpsoutput.allowedValues, list) and wpsoutput.allowedValues is not None:
                    result['processOutputs'][wpsoutput.identifier]['allowedValues'] = wpsoutput.allowedValues

            for wpsinput in wps_process.dataInputs:
                if not 'dataInputs' in result:
                    result['dataInputs'] = {}
                result['dataInputs'][wpsinput.identifier] = {'dataType': wpsinput.dataType,
                                                             'maxOccurs': wpsinput.maxOccurs,
                                                             'minOccurs': wpsinput.minOccurs,
                                                             'title': wpsinput.title, }
                if wpsinput.abstract is not None:
                    result['dataInputs'][wpsinput.identifier]['abstract'] = wpsinput.abstract
                if wpsinput.dataType == 'ComplexData':
                    print('1 - -  - is complex')
                    if not isinstance(wpsinput.defaultValue, list) and wpsinput.defaultValue is not None:
                        print('2 # wpsinput.defaultValue: ', wpsinput.defaultValue)
                        result['dataInputs'][wpsinput.identifier].update({'defaultValue': {}})
                        if wpsinput.defaultValue.encoding:
                            result['dataInputs'][wpsinput.identifier]['defaultValue'][
                                'encoding'] = wpsinput.defaultValue.encoding
                        if wpsinput.defaultValue.mimeType:
                            result['dataInputs'][wpsinput.identifier]['defaultValue'][
                                'mimeType'] = wpsinput.defaultValue.mimeType
                        if wpsinput.defaultValue.schema:
                            result['dataInputs'][wpsinput.identifier]['defaultValue'][
                                'schema'] = wpsinput.defaultValue.schema

                    print('3 # wpsinput.allowedValues: ', wpsinput.allowedValues)
                    if not isinstance(wpsinput.allowedValues, list) and wpsinput.allowedValues is not None:
                        result['dataInputs'][wpsinput.identifier].update({'allowedValues': {}})
                        if wpsinput.allowedValues.encoding:
                            print('4 # wpsinput.allowedValues.encoding: ', wpsinput.allowedValues.encoding)
                            result['dataInputs'][wpsinput.identifier]['allowedValues'][
                                'encoding'] = wpsinput.allowedValues.encoding
                        if wpsinput.allowedValues.mimeType:
                            result['dataInputs'][wpsinput.identifier]['allowedValues'][
                                'mimeType'] = wpsinput.allowedValues.mimeType
                        if wpsinput.allowedValues.schema:
                            result['dataInputs'][wpsinput.identifier]['allowedValues'][
                                'schema'] = wpsinput.allowedValues.schema

                    print('5 # wpsinput.supportedValues: ', wpsinput.supportedValues[0])
                    print('6 # type of wpsinput.supportedValues: ', type(wpsinput.supportedValues[0]))
                    print(' 7b länge: ', len(wpsinput.supportedValues))
                    if isinstance(wpsinput.supportedValues[0], complex):
                        print('7 +++ complex erkannt')
                    else:
                        print('8 +++ nicht erkannt')
                    if not isinstance(wpsinput.supportedValues, list) and wpsinput.supportedValues is not None:
                        result['dataInputs'][wpsinput.identifier].update({'supportedValues': {}})

                        if wpsinput.supportedValues.encoding:
                            result['dataInputs'][wpsinput.identifier]['supportedValues'][
                                'encoding'] = wpsinput.supportedValues.encoding
                        if wpsinput.supportedValues.mimeType:
                            result['dataInputs'][wpsinput.identifier]['supportedValues'][
                                'mimeType'] = wpsinput.supportedValues.mimeType
                        if wpsinput.supportedValues.schema:
                            result['dataInputs'][wpsinput.identifier]['supportedValues'][
                                'schema'] = wpsinput.supportedValues.schema
                else:
                    print('9 +  im else')
                    if wpsinput.defaultValue is not None:
                        result['dataInputs'][wpsinput.identifier]['defaultValue'] = wpsinput.defaultValue
                    if wpsinput.allowedValues is not None:
                        result['dataInputs'][wpsinput.identifier]['allowedValues'] = wpsinput.allowedValues
                    if wpsinput.supportedValues is not None:
                        result['dataInputs'][wpsinput.identifier]['supportedValues'] = wpsinput.supportedValues
                    print('10 +++++++++++++++++')

            print('11 result: ', result)
            print('11 result: ', jsonpickle.encode(wps_process))
            print('------ ')
            # json_data = json.dumps(wps_process.__dict__, lambda o: o.__dict__, indent=4)

            return JsonResponse({'result': result})


def process(request, service, identifier):
    """
    View that displays a detailed description for a WPS process.
    """
    print('??????????????????????????????????????')
    #    form_class = InputForm
    wps = get_wps_service_engine(service)
    wps_process = wps.describeprocess(identifier)

    context = {'process': wps_process,
               'service': service,
               'is_link': abstract_is_link(wps_process),
               'wps': wps,
               }

    if request.method == 'POST':  # If the form has been submitted...
        #        form = form_class(request.POST) # A form bound to the POST data
        #        if form.is_valid(): # All validation rules pass
        #        value_list = form['input']
        value_list = []
        key_list = []
        inputs = []
        outputs = []

        value_list = request.POST.getlist('input')

        for input in wps_process.dataInputs:
            key_list.append(input.identifier)

        inputs = list(zip(key_list, value_list))

        processid = wps_process.identifier

        execution = wps.execute(processid, inputs)
        execution_status = execution.status

        image = []
        for output in execution.processOutputs:
            outputs.append(output.data)
            output_reference = output.reference
            if type(output.data[0] is str):
                if len(output.data[0]) > 10:
                    substring = output.data[0][:10]
                    if "img" in substring:
                        image = output.data[0]

        for output in execution.processOutputs:
            outputs.append(output.data)
            output_reference = output.reference

        if output_reference:
            output_reference = output_reference.replace('localhost', HOST_NAME)
            # output_reference = output_reference.replace('localhost','vforwater-devel')

        context_p = {'process': wps_process,
                     'inputs': inputs,
                     'processid': processid,
                     'outputs': outputs,
                     'image': image,
                     'output_reference': output_reference,
                     'execution_status': execution_status
                     }
        return render(request, 'wps_gui/result.html', context_p)

    return render(request, 'wps_gui/process.html', context)


def development(request):
    """
    Create a page to show when something isn't working.
    """
    return HttpResponse("We apologize for the inconvenience.\\ At the moment this site is under heavy development.")
