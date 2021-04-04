# from inspect import getmembers

from django.shortcuts import render
from django.core.cache import cache

from heron.settings import VFW_SERVER, HOST_NAME, wps_log
from heron_wps.utilities import get_wps_service_engine, list_wps_service_engines, abstract_is_link
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
        print('--- No PyWPS_vforwater views.home available')
        wps_log.debug('No PyWPS_vforwater in views.home available')
        service = ''
        wps = []

    context = {'wps_services': wps_services,
               'wps': wps,
               'service': service}

    return render(request, 'heron_wps/home.html', context)


def service(request, service):
    """
    View that lists the processes for a given service.
    """
    wps = get_wps_service_engine(service)

    context = {'wps': wps,
               'service': service}

    return render(request, 'heron_wps/service.html', context)


def process(request, service, identifier):
    """
    View that displays a detailed description for a WPS process.
    """
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

        return render(request, 'heron_wps/result.html', context_p)
    
    return render(request, 'heron_wps/process.html', context)
