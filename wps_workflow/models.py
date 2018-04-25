from django.contrib.auth.models import User
from django.db import models

STATUS = (
    ('0', 'NONE'),
    ('1', 'READY'),
    ('2', 'WAITING'),
    ('3', 'RUNNING'),
    ('4', 'FINISHED'),
    ('5', 'FAILED'),
    ('6', 'DEPRECATED'),
)

ROLE = (
    ('0', 'INPUT'),
    ('1', 'OUTPUT'),
)

DATATYPE = (
    ('0', 'LITERAL'),
    ('1', 'COMPLEX'),
    ('2', 'BOUNDING_BOX'),
)


class Workflow(models.Model):
    """
    Workflow Database Model 
    """
    name = models.CharField(max_length=200)
    description = models.TextField(
        'Descriptive text', default='Add your super descriptive text here...')
    percent_done = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shared = models.BooleanField(default=False)
    creator = models.ForeignKey(
        User, editable=True, related_name='creator_user', on_delete=models.CASCADE)
    last_modifier = models.ForeignKey(
        User, editable=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Workflow"
        verbose_name_plural = "Workflows"

    def __str__(self):
        return self.name


class WPSProvider(models.Model):
    """
    Provider of WPS Server
    """
    provider_name = models.CharField(max_length=200)
    provider_site = models.URLField(max_length=1000)
    individual_name = models.CharField(max_length=200)
    position_name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "WPSProvider"
        verbose_name_plural = "WPSProviders"

    def __str__(self):
        return self.provider_name


class WPS(models.Model):
    """
    PyWPS Server provided by WPSProvider
    """
    service_provider = models.ForeignKey(WPSProvider, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    abstract = models.TextField(
        'Descriptive text', default='Add your super descriptive text here...')
    capabilities_url = models.URLField(max_length=1000)
    describe_url = models.URLField(max_length=1000)
    execute_url = models.URLField(max_length=1000)

    class Meta:
        verbose_name = "WPS"
        verbose_name_plural = "WPS"

    def __str__(self):
        return self.title


class Process(models.Model):
    """
    PyWPS Process available on given PyWPS Server
    """
    wps = models.ForeignKey(WPS, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    abstract = models.TextField(
        'Descriptive text', default='Add your super descriptive text here...')

    class Meta:
        verbose_name = "Process"
        verbose_name_plural = "Processes"

    def __str__(self):
        return "%s from Server '%s'" % (self.title, self.wps.title)


class Task(models.Model):
    """
    PyWPS Task created in Editor and Member of a Workflow
    """
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    x = models.DecimalField(max_digits=5, decimal_places=0)
    y = models.DecimalField(max_digits=5, decimal_places=0)
    status = models.CharField(max_length=1, choices=STATUS)
    title = models.CharField(max_length=200)
    abstract = models.TextField(
        'Descriptive text', default='Add your super descriptive text here...')
    status_url = models.URLField(max_length=1000)
    started_at = models.DateTimeField(null=True)

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return "%s from Workflow '%s'" % (self.title, self.workflow.name)


class Session(models.Model):
    """
    Settings, Session Restore and user specific Data
    """
    user = models.ForeignKey(User, editable=False, on_delete=models.CASCADE)
    last_workflow = models.ForeignKey(
        Workflow, null=True, on_delete=models.SET_NULL)
    language = models.CharField(max_length=3, default='de', null=False)

    class Meta:
        verbose_name = "Session"
        verbose_name_plural = "Sessions"


class InputOutput(models.Model):
    """
    Scheme Definition data for Inputs and Outputs, see PyWPS XML Definition as Reference
    """
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    role = models.CharField(max_length=1, choices=ROLE)
    identifier = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=200)
    abstract = models.TextField(
        'Descriptive text', default='Add your super descriptive text here...', null=True)
    datatype = models.CharField(max_length=1, choices=DATATYPE, null=True)
    format = models.CharField(max_length=200, null=True)
    min_occurs = models.IntegerField()
    max_occurs = models.IntegerField()

    class Meta:
        verbose_name = "InputOutput"
        verbose_name_plural = "InputOutputs"

    def __str__(self):
        input_or_output = 'Input' if self.role == '0' else 'Output'
        return input_or_output + " of Process '" + self.process.title + "'"


class Edge(models.Model):
    """
    Egdes between Tasks in Workflow Graph 
    """
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    from_task = models.ForeignKey(
        Task, related_name='out_task', on_delete=models.CASCADE)  # rename to out_task?
    to_task = models.ForeignKey(
        Task, on_delete=models.CASCADE)  # rename to in_task?
    input = models.ForeignKey(
        InputOutput, related_name='input', null=True, on_delete=models.SET_NULL)
    output = models.ForeignKey(
        InputOutput, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Edge"
        verbose_name_plural = "Edges"

    def __str__(self):
        return self.from_task.title + " to " + self.to_task.title + " (" + self.workflow.name + ")"


class Artefact(models.Model):
    """
    Data of Input or Output element
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    parameter = models.ForeignKey(
        InputOutput, null=True, on_delete=models.SET_NULL)
    role = models.CharField(max_length=1, choices=ROLE)
    format = models.CharField(max_length=200)
    data = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Artefact"
        verbose_name_plural = "Artefacts"
