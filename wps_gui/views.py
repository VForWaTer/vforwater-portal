# from inspect import getmembers
import json
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
        print('_________ DA')

        if 'processview' in request.GET:
            print('++++++++++++++++')
            process = json.loads(request.GET.get('processview'))
            identifier = process['id']
            service = process['serv']

            wps = get_wps_service_engine(service)
            wps_process = wps.describeprocess(identifier)
            result = {}
            for wpsinput in wps_process.dataInputs:
                print('+++++ i: ', wpsinput.identifier)
                result[wpsinput.identifier] = {'abstract': wpsinput.abstract,
                                               'allowedValues': wpsinput.allowedValues,
                                               'dataType': wpsinput.dataType,
                                               'maxOccurs': wpsinput.maxOccurs,
                                               'minOccurs': wpsinput.minOccurs,
                                               'title': wpsinput.title,
                                               }
                if wpsinput.dataType == 'ComplexData' and wpsinput.defaultValue:
                    print('default: ', wpsinput.defaultValue)
                    result[wpsinput.identifier]['defaultValue'] = {'encoding': wpsinput.defaultValue.encoding,
                                                                   'mimeType': wpsinput.defaultValue.mimeType,
                                                                   'schema': wpsinput.defaultValue.schema,}
                    print('type: ', wpsinput.supportedValues)
                    print('type: ', type(wpsinput.supportedValues))
                    for i in wpsinput.supportedValues:
                        print('i: ', i)
                    result[wpsinput.identifier]['supportedValues'] = {'encoding': wpsinput.supportedValues.encoding,
                                                                      'mimeType': wpsinput.supportedValues.mimeType,
                                                                      'schema': wpsinput.supportedValues.schema, }
                else:
                    result[wpsinput.identifier]['defaultValue'] = wpsinput.dataType
                    result[wpsinput.identifier]['supportedValues'] = wpsinput.supportedValues

                print('+++++++++++++++++')
                print('supportedValues: ', wpsinput.supportedValues)
                # if wpsinput.supportedValues == 'ComplexData' and wpsinput.defaultValue:
                #
                # else:


                    # result[wpsinput.identifier]['defaultValueMimeType'] = True
                    # result[wpsinput.identifier]['defaultValueEncoding'] = True
            print('result: ', result)
            print('kein fehler 1')
            context = {'process': wps_process,
                       'service': service,
                       #'is_link': abstract_is_link(wps_process),
                       'wps': wps,
                       }

            print('kein fehler 2')
            #return {'context': context}
            return JsonResponse({'result': result})
            #return render(request, 'wps_gui/process.html', context)


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
