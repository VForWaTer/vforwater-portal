import calendar
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView, View

from wps_workflow import cron, utils
from .models import InputOutput, WPSProvider, Process, Artefact, Edge, Task, Workflow, WPS

def as_json_response(response):
    """
    method stub to return a JsonResponse
    @param response: parameter list which is returned
    @type response: dict|list
    @return: JsonResponse
    @rtype: django.http.JsonResponse
    """
    return JsonResponse(response, safe=False)


class UserView(View):
    """
    Sends user data to the client
    """

    @staticmethod
    def get(request):
        """
        Sends the requested User information to the server.
        @param request: the request sent from the client
        @type request: django.http.request.HttpRequest
        @return: a json response containing the user information
        @rtype: django.http.JsonResponse
        """
        user = model_to_dict(request.user)
        del user['password']

        return as_json_response(user)


class WorkflowView(View):
    """
    Exchanges workflow data with the client
    """

    @staticmethod
    def can_user_access_workflow(user, workflow_id):
        """"
        Checks wether the user has access to a workflow
        @param user the user
        @type user django.contrib.auth.models.User
        @param workflow_id the id of the workflow
        @type workflow_id int int
        @return: if the user can access the workflow
        @rtype: bool
        """

        if not user.is_authenticated:
            return False

        if user.is_staff:
            return True

        workflow = get_object_or_404(Workflow, pk=workflow_id)
        return workflow.shared or workflow.creator_id == user.id

    # needed because Django needs CSRF token in cookie unless you put this
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        """
        Sends a http response to the client
        @param args: non-keyworded arguments passed to models.Model.dispatch() method
        @type args: list
        @param kwargs: keyworded arguments passed to models.Model.dispatch() method
        @type kwargs: list
        @return: the response
        @rtype: django.http.response.HttpResponse
        """
        return super(WorkflowView, self).dispatch(*args, **kwargs)

    @staticmethod
    def get(request, **kwargs):
        """
        Sends the requested workflow information to the server.
        @param request: the request sent from the client
        @type request: django.http.request.HttpRequest
        @param kwargs: keyworded arguments passed to models.Model.dispatch() method
        @type kwargs: list
        @return: a JsonResponse containing the requested workflow data
        @rtype: django.http.JsonResponse
        """
        if 'workflow_id' in kwargs:
            if not WorkflowView.can_user_access_workflow(request.user, kwargs['workflow_id']):
                return JsonResponse({'error': 'no access'})

            workflow = get_object_or_404(Workflow, pk=kwargs['workflow_id'])

            # get_object_or_404() ist not used here because for some reason
            # it does not include created_at and updated_at fields
            returned = list(Workflow.objects.filter(
                pk=kwargs['workflow_id']).values())[0]

            returned['title'] = returned['name']
            returned['created_at'] = calendar.timegm(
                returned['created_at'].timetuple())
            returned['updated_at'] = calendar.timegm(
                returned['updated_at'].timetuple())

            returned['edges'] = list(workflow.edge_set.all().values())
            tasks = list(workflow.task_set.all().values())

            for (i, task) in enumerate(tasks):
                tasks[i]['state'] = int(tasks[i]['status'])
                tasks[i]['x'] = float(task['x'])
                tasks[i]['y'] = float(task['y'])

                if task['started_at'] is not None:
                    tasks[i]['started_at'] = calendar.timegm(
                        task['started_at'].timetuple())

                input_artefacts = list(Artefact.objects.filter(
                    task=task['id']).filter(role=0).values())
                output_artefacts = list(Artefact.objects.filter(
                    task=task['id']).filter(role=1).values())

                for (j, input_artefact) in enumerate(input_artefacts):
                    input_artefacts[j]['role'] = (
                        'input' if input_artefact['role'] == '0' else 'output')
                    input_artefacts[j]['created_at'] = calendar.timegm(
                        input_artefact['created_at'].timetuple())
                    input_artefacts[j]['updated_at'] = calendar.timegm(
                        input_artefact['updated_at'].timetuple())

                for (j, output_artefact) in enumerate(output_artefacts):
                    output_artefacts[j]['role'] = (
                        'input' if output_artefact['role'] == '0' else 'output')
                    output_artefacts[j]['created_at'] = calendar.timegm(
                        output_artefact['created_at'].timetuple())
                    output_artefacts[j]['updated_at'] = calendar.timegm(
                        output_artefact['updated_at'].timetuple())

                tasks[i]['input_artefacts'] = input_artefacts
                tasks[i]['output_artefacts'] = output_artefacts

            returned['tasks'] = tasks

            return as_json_response(returned)
        else:
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'no access'})

            returned = list(Workflow.objects.filter(Q(shared=True) | Q(creator_id=request.user.id)).order_by(
                '-updated_at').values())

            for (i, workflow) in enumerate(returned):
                returned[i]['title'] = workflow['name']
                returned[i]['created_at'] = calendar.timegm(
                    workflow['created_at'].timetuple())
                returned[i]['updated_at'] = calendar.timegm(
                    workflow['updated_at'].timetuple())

                returned[i]['edges'] = list(
                    Edge.objects.filter(workflow=workflow['id']).values())
                tasks = list(Task.objects.filter(
                    workflow=workflow['id']).values())

                for (j, task) in enumerate(tasks):
                    tasks[j]['state'] = int(task['status'])
                    tasks[j]['x'] = float(task['x'])
                    tasks[j]['y'] = float(task['y'])

                    if task['started_at'] is not None:
                        tasks[j]['started_at'] = calendar.timegm(
                            task['started_at'].timetuple())

                    input_artefacts = list(Artefact.objects.filter(
                        task=task['id']).filter(role=0).values())
                    output_artefacts = list(Artefact.objects.filter(
                        task=task['id']).filter(role=1).values())

                    for (k, input_artefact) in enumerate(input_artefacts):
                        input_artefacts[k]['role'] = (
                            'input' if input_artefact['role'] == '0' else 'output')
                        input_artefacts[k]['created_at'] = calendar.timegm(
                            input_artefact['created_at'].timetuple())
                        input_artefacts[k]['updated_at'] = calendar.timegm(
                            input_artefact['updated_at'].timetuple())

                    for (k, output_artefact) in enumerate(output_artefacts):
                        output_artefacts[k]['role'] = (
                            'input' if output_artefact['role'] == '0' else 'output')
                        output_artefacts[k]['created_at'] = calendar.timegm(
                            output_artefact['created_at'].timetuple())
                        output_artefacts[k]['updated_at'] = calendar.timegm(
                            output_artefact['updated_at'].timetuple())

                    tasks[j]['input_artefacts'] = input_artefacts
                    tasks[j]['output_artefacts'] = output_artefacts

                returned[i]['tasks'] = tasks

            return as_json_response(returned)

    @staticmethod
    def post(request):
        """
        Sends requested data to the client
        @param request: the request sent from the client
        @type request: django.http.request.HttpRequest
        @return: a JsonResponse containing the requested workflow data
        @rtype: django.http.JsonResponse
        """
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'no access'})

        new_data = json.loads(request.body)

        new_workflow = Workflow.objects.create(
            name=new_data['title'],
            percent_done=0,
            shared=new_data['shared'],
            creator_id=request.user.id,
            last_modifier_id=request.user.id
        )

        temporary_to_new_task_ids = {}

        for new_task_data in new_data['tasks']:
            new_task = Task.objects.create(
                workflow_id=new_workflow.id,
                process_id=new_task_data['process_id'],
                x=new_task_data['x'],
                y=new_task_data['y'],
                status=new_task_data['state']
            )

            temporary_to_new_task_ids[new_task_data['id']] = new_task.id

            artefacts_data = new_task_data['input_artefacts'] + \
                new_task_data['output_artefacts']

            for artefact_data in artefacts_data:
                Artefact.objects.create(
                    task_id=new_task.id,
                    parameter_id=artefact_data['parameter_id'],
                    role=(0 if artefact_data['role'] == 'input' else 1),
                    format=artefact_data['format'],
                    data=artefact_data['data']
                )

        for new_edge_data in new_data['edges']:
            Edge.objects.create(
                workflow_id=new_workflow.id,
                from_task_id=temporary_to_new_task_ids[new_edge_data['from_task_id']],
                to_task_id=temporary_to_new_task_ids[new_edge_data['to_task_id']],
                input_id=new_edge_data['input_id'],
                output_id=new_edge_data['output_id']
            )

        return WorkflowView.get(request, workflow_id=new_workflow.id)

    @staticmethod
    def patch(request, **kwargs):
        """
        Updates a workflow if it exists
        @param request: the request sent from the client
        @type request: django.http.request.HttpRequest
        @param kwargs: keyworded arguments passed to models.Model.dispatch() method
        @type kwargs: list
        @return: a JsonResponse which contains either the workflow or an error message
        @rtype: django.http.JsonResponse
        """
        if not WorkflowView.can_user_access_workflow(request.user, kwargs['workflow_id']):
            return JsonResponse({'error': 'no access'})

        new_data = json.loads(request.body)
        workflow = get_object_or_404(Workflow, pk=kwargs['workflow_id'])

        workflow.name = new_data['title']
        workflow.shared = new_data['shared']
        workflow.last_modifier_id = request.user.id

        workflow.save()

        not_deleted_task_ids = []
        temporary_to_new_task_ids = {}

        for task_data in new_data['tasks']:
            artefacts_data = task_data['input_artefacts'] + \
                task_data['output_artefacts']

            if task_data['id'] > 0:
                task = get_object_or_404(Task, pk=task_data['id'])

                task.workflow_id = workflow.id
                task.process_id = task_data['process_id']
                task.x = task_data['x']
                task.y = task_data['y']
                task.status = task_data['state']

                task.save()

                not_deleted_artefact_ids = []

                for artefact_data in artefacts_data:
                    if ('id' in artefact_data) and (artefact_data['id'] > 0):
                        artefact = get_object_or_404(
                            Artefact, pk=artefact_data['id'])

                        artefact.task_id = task.id
                        artefact.parameter_id = artefact_data['parameter_id']
                        artefact.role = (
                            0 if artefact_data['role'] == 'input' else 1)
                        artefact.format = artefact_data['format']
                        artefact.data = artefact_data['data']

                        artefact.save()
                    else:
                        artefact = Artefact.objects.create(
                            task_id=task.id,
                            parameter_id=artefact_data['parameter_id'],
                            role=(
                                0 if artefact_data['role'] == 'input' else 1),
                            format=artefact_data['format'],
                            data=artefact_data['data']
                        )

                    not_deleted_artefact_ids.append(artefact.pk)

                task.artefact_set.exclude(
                    pk__in=not_deleted_artefact_ids).delete()
            else:
                task = Task.objects.create(
                    workflow_id=workflow.id,
                    process_id=task_data['process_id'],
                    x=task_data['x'],
                    y=task_data['y'],
                    status=task_data['state']
                )

                for artefact_data in artefacts_data:
                    Artefact.objects.create(
                        task_id=task.id,
                        parameter_id=artefact_data['parameter_id'],
                        role=(0 if artefact_data['role'] == 'input' else 1),
                        format=artefact_data['format'],
                        data=artefact_data['data']
                    )

            not_deleted_task_ids.append(task.pk)
            temporary_to_new_task_ids[task_data['id']] = task.id

        workflow.task_set.exclude(pk__in=not_deleted_task_ids).delete()

        not_deleted_edge_ids = []

        for edge_data in new_data['edges']:
            if edge_data['id'] > 0:
                edge = get_object_or_404(Edge, pk=edge_data['id'])

                edge.workflow = workflow
                edge.from_task_id = temporary_to_new_task_ids[edge_data['from_task_id']]
                edge.to_task_id = temporary_to_new_task_ids[edge_data['to_task_id']]
                edge.input_id = edge_data['input_id']
                edge.output_id = edge_data['output_id']

                edge.save()
            else:
                edge = Edge.objects.create(
                    workflow_id=workflow.id,
                    from_task_id=temporary_to_new_task_ids[edge_data['from_task_id']],
                    to_task_id=temporary_to_new_task_ids[edge_data['to_task_id']],
                    input_id=edge_data['input_id'],
                    output_id=edge_data['output_id']
                )

            not_deleted_edge_ids.append(edge.pk)

        workflow.edge_set.exclude(pk__in=not_deleted_edge_ids).delete()

        return WorkflowView.get(request, workflow_id=kwargs['workflow_id'])

    @staticmethod
    def delete(request, **kwargs):
        """
        Deletes the a workflow if it exists
        @param request: the request sent from the client
        @type request: django.http.request.HttpRequest
        @param kwargs: keyworded arguments passed to models.Model.dispatch() method
        @type kwargs: list
        @return: a JsonResponse with either a success or an error message
        @rtype: django.http.JsonResponse
        """
        if not WorkflowView.can_user_access_workflow(request.user, kwargs['workflow_id']):
            return JsonResponse({'error': 'no access'})

        workflow = get_object_or_404(Workflow, pk=kwargs['workflow_id'])
        (deletedWorkflowCount, countOfDeletionsPerType) = workflow.delete()
        deleted = (deletedWorkflowCount > 0)

        return JsonResponse({'deleted': deleted})

    @staticmethod
    @require_GET
    def start(request, workflow_id):
        """
        Starts the workflow with the passed id if it exists
        @param request: the request sent from the client
        @type request: django.http.request.HttpRequest
        @param workflow_id: the id of the workflow that is started
        @type workflow_id: int
        @return: a JsonResponse which is either empty on success or contains an error message on failure
        @rtype: django.http.JsonResponse
        """

        # if not WorkflowView.can_user_access_workflow(request.user, workflow_id):
        #    return JsonResponse({'error': 'no access'})

        Task.objects.filter(workflow=workflow_id).update(status=1)
        return JsonResponse({})

    @staticmethod
    @require_GET
    def stop(request, workflow_id):
        """
        Stops the workflow with the passed id if it exists
        @param request: the request sent from the client
        @type request: django.http.request.HttpRequest
        @param workflow_id: the id of the workflow
        @type workflow_id: int
        @return: a JsonResponse with either no content or an error message
        @rtype: django.http.JsonResponse
        """
        # if not WorkflowView.can_user_access_workflow(request.user, workflow_id):
        #    return JsonResponse({'error': 'no access'})

        workflow = get_object_or_404(Workflow, pk=workflow_id)
        tasks = workflow.task_set.all()

        tasks.update(status=0)

        for task in tasks:
            task.artefact_set.filter(role=1).delete()

        artefacts = Artefact.objects.filter(
            task__workflow_id=workflow_id).filter(role=0)
        for artefact in artefacts:
            edge = Edge.objects.filter(workflow_id=workflow_id).filter(
                to_task_id=artefact.task_id).filter(input_id=artefact.parameter_id).values()

            if edge.count() > 0:
                artefact.delete()

        return JsonResponse({})

    @staticmethod
    @require_GET
    def refresh(request, workflow_id):
        """
        Refresh method called by the client
        @param request: the request sent from the client
        @type request: django.http.request.HttpRequest
        @param workflow_id: the id of the users current workflow
        @type workflow_id: int
        @return: an empty JsonResponse
        @rtype: django.http.JsonResponse
        """

        # TODO: This needs some kind of throttling
        cron.scheduler()
        cron.receiver()

        return JsonResponse({})


class ProcessView(View):
    """
    Exchanges process data with the client
    """

    # needed because Django needs CSRF token in cookie unless you put this
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        """
        Sends a http response to the client
        @param args: non-keyworded arguments passed to models.Model.dispatch() method
        @type args: list
        @param kwargs: keyworded arguments passed to models.Model.dispatch() method
        @type kwargs: list
        @return: the response
        @rtype: django.http.response.HttpResponse
        """
        return super(ProcessView, self).dispatch(*args, **kwargs)

    @staticmethod
    def get(request, **kwargs):
        """
        Sends the requested process information to the server.
        @param request: the request sent from the client
        @type request: django.http.request.HttpRequest
        @param kwargs: keyworded arguments passed to models.Model.dispatch() method
        @type kwargs: list
        @return: a JsonResponse containing the requested process data
        @rtype: django.http.JsonResponse
        """
        if 'process_id' in kwargs:
            process = Process.objects.get(pk=kwargs['process_id'])
            returned = model_to_dict(process)
            inputs = list(
                process.inputoutput_set.all().filter(role=0).values())
            outputs = list(
                process.inputoutput_set.all().filter(role=1).values())

            for (j, input) in enumerate(inputs):
                inputs[j]['type'] = int(input['datatype'])
                inputs[j]['role'] = (
                    'input' if input['role'] == '0' else 'output')

            for (j, output) in enumerate(outputs):
                outputs[j]['type'] = int(output['datatype'])
                outputs[j]['role'] = (
                    'input' if output['role'] == '0' else 'output')

            returned['inputs'] = inputs
            returned['outputs'] = outputs

            return as_json_response(returned)
        else:
            returned = list(Process.objects.all().values())

            for (i, process) in enumerate(returned):
                inputs = list(InputOutput.objects.filter(
                    process=process['id']).filter(role=0).values())
                outputs = list(InputOutput.objects.filter(
                    process=process['id']).filter(role=1).values())

                for (j, input) in enumerate(inputs):
                    inputs[j]['type'] = int(input['datatype'])
                    inputs[j]['role'] = (
                        'input' if input['role'] == '0' else 'output')

                for (j, output) in enumerate(outputs):
                    outputs[j]['type'] = int(output['datatype'])
                    outputs[j]['role'] = (
                        'input' if output['role'] == '0' else 'output')

                returned[i]['inputs'] = inputs
                returned[i]['outputs'] = outputs

            return as_json_response(returned)

    @staticmethod
    def post(request):
        """
        Sends requested data to the client
        @param request: the request sent from the client
        @type request: django.http.request.HttpRequest
        @return: a JsonResponse containing the requested process data
        @rtype: django.http.JsonResponse
        """
        return JsonResponse({'error': 'this REST interface is not supported'})

    @staticmethod
    def patch(request):
        """
        Updates a process if it exists
        @param request: the request sent from the client
        @type request: django.http.request.HttpRequest
        @return: a JsonResponse which contains either the process or an error message
        @rtype: django.http.JsonResponse
        """
        return JsonResponse({'error': 'this REST interface is not supported'})

    @staticmethod
    def delete(request):
        """
        Deletes a process if it exists
        @param request: the request sent from the client
        @type request: django.http.request.HttpRequest
        @return: a JsonResponse containing an error message because this is not supported
        @rtype: django.http.JsonResponse
        """
        return JsonResponse({'error': 'this REST interface is not supported'})


class WPSView(View):
    """
    Exchanges wps data with the client
    """

    # needed because Django needs CSRF token in cookie unless you put this
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        """
        Sends a http response to the client
        @param args: non-keyworded arguments passed to models.Model.dispatch() method
        @type args: list
        @param kwargs: keyworded arguments passed to models.Model.dispatch() method
        @type kwargs: list
        @return: the response
        @rtype: django.http.response.HttpResponse
        """
        return super(WPSView, self).dispatch(*args, **kwargs)

    @staticmethod
    def get(request, **kwargs):
        """
        Sends the requested wps information to the server.
        @param request: the request sent from the client
        @type request: django.http.request.HttpRequest
        @param kwargs: keyworded arguments passed to models.Model.dispatch() method
        @type kwargs: list
        @return: a JsonResponse containing the requested wps data
        @rtype: django.http.JsonResponse
        """
        if 'wps_id' in kwargs:
            wps = WPS.objects.get(pk=kwargs['wps_id'])
            returned = model_to_dict(wps)
            returned['provider'] = model_to_dict(wps.service_provider)
            returned['provider']['title'] = returned['provider']['provider_name']
            returned['provider']['site'] = returned['provider']['provider_site']
            return as_json_response(returned)
        else:
            returned = list(WPS.objects.all().values())

            for (i, wps) in enumerate(returned):
                returned[i]['provider'] = model_to_dict(
                    WPSProvider.objects.get(pk=wps['service_provider_id']))
                returned[i]['provider']['title'] = returned[i]['provider']['provider_name']
                returned[i]['provider']['site'] = returned[i]['provider']['provider_site']

            return as_json_response(returned)

    @staticmethod
    def post(request):
        """
        Sends requested data to the client
        @param request: the request sent from the client
        @type request: django.http.request.HttpRequest
        @return: a JsonResponse containing the requested wps data
        @rtype: django.http.JsonResponse
        """

        utils.add_wps_server(request.body.decode('utf-8'))
        return JsonResponse({})

    @staticmethod
    def patch(request, **kwargs):
        """
        Updates a wps if it exists
        @param request: the request sent from the client
        @type request: django.http.request.HttpRequest
        @param kwargs: keyworded arguments passed to models.Model.dispatch() method
        @type kwargs: list
        @return: a JsonResponse which contains either the wps or an error message
        @rtype: django.http.JsonResponse
        """
        new_data = json.loads(request.body)
        wps = get_object_or_404(WPS, pk=kwargs['wps_id'])

        if new_data['provider']['id'] > 0:
            wps_provider = get_object_or_404(
                WPSProvider, pk=new_data['provider']['id'])

            wps_provider.provider_name = new_data['provider']['title']
            wps_provider.provider_site = new_data['provider']['site']

            wps_provider.save()

            wps_provider_id = new_data['provider']['id']
        else:
            new_wps_provider = WPSProvider.objects.create(
                provider_name=new_data['provider']['title'],
                provider_site=new_data['provider']['url']
            )

            wps_provider_id = new_wps_provider.id

        wps.service_provider_id = wps_provider_id
        wps.title = new_data['title']
        wps.abstract = new_data['abstract']

        wps.save()

        return WPSView.get(request, wps_id=kwargs['wps_id'])

    @staticmethod
    def delete(request, **kwargs):
        """
        Deletes a wps if it exists
        @param request: the request sent from the client
        @type request: django.http.request.HttpRequest
        @param kwargs: keyworded arguments passed to models.Model.dispatch() method
        @type kwargs: list
        @return: a JsonResponse with either a success or an error message
        @rtype: django.http.JsonResponse
        """
        wps = get_object_or_404(WPS, pk=kwargs['wps_id'])
        (deletedWPSCount, countOfDeletionsPerType) = wps.delete()
        deleted = (deletedWPSCount > 0)

        return JsonResponse({'deleted': deleted})

    @staticmethod
    @require_GET
    def refresh(request):
        """
        Is called by an admin from the client, refreshes all wps servers checking for processes
        @param request: the request sent from the client
        @type request: django.http.request.HttpRequest
        @return: an empty JsonResponse
        @rtype: django.http.JsonResponse
        """
        cron.update_wps_processes()

        return JsonResponse({})


# TODO: document 
# class OurLogoutView(TemplateView):
#     """
#     
#     """
#     template_name = "index.html"
# 
#     # needed because Django needs CSRF token in cookie unless you put this
#     @csrf_exempt
#     def dispatch(self, *args, **kwargs):
#         """
# 
#         @param args: non-keyworded arguments passed to models.Model.dispatch() method
#         @type args:
#         @param kwargs: keyworded arguments passed to models.Model.dispatch() method
#         @type kwargs:
#         @return:
#         @rtype: django.http.response.HttpResponse
#         """
#         return super(OurLogoutView, self).dispatch(*args, **kwargs)
# 
#     @staticmethod
#     def delete(request):
#         logout(request)
#         return JsonResponse({'logged': 'out'})
# 
# 
# # TODO: document
# class OurLoginView(TemplateView):
#     """
# 
#     """
#     template_name = "index.html"
# 
#     # needed because Django needs CSRF token in cookie unless you put this
#     @csrf_exempt
#     def dispatch(self, *args, **kwargs):
#         """
#         Sends a http response to the client
#         @param args: non-keyworded arguments passed to models.Model.dispatch() method
#         @type args: list
#         @param kwargs: keyworded arguments passed to models.Model.dispatch() method
#         @type kwargs: list
#         @return: the response
#         @rtype: django.http.response.HttpResponse
#         """
#         print('   *2  OurLoginView views.py', self, *args, **kwargs)
# 
#         return super(OurLoginView, self).dispatch(*args, **kwargs)
# 
#     @staticmethod  # TODO: document
#     def post(request):
#         """
# 
#         @param request:
#         @type request:
#         @return:
#         @rtype:
#         """
#         login_data = json.loads(request.body)
#         user = authenticate(
#             username=login_data['username'], password=login_data['password'])
# 
#         if user is not None:
#             login(request, user)
#             user = model_to_dict(user)
#             del user['password']
#             return as_json_response(user)
#         else:
#             return JsonResponse({'error': 'no access'})


# TODO: document
class WorkflowsView(LoginRequiredMixin, TemplateView):
    """
 
    """
    #login_url = '/wps_workflow/login/'
 
    template_name = "index.html"


# TODO: document
class EditorView(LoginRequiredMixin, TemplateView):
    """

    """
    #login_url = '/wps_workflow/login/'
    login_url = 'vfwheron:watts_login'

    template_name = "index.html"


# TODO: document
class SettingsView(LoginRequiredMixin, TemplateView):

    #login_url = '/wps_workflow/login/'

    template_name = "index.html"
