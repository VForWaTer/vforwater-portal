from django.contrib import admin

from wps_workflow.models import *


# Register your models here.
class TaskInline(admin.StackedInline):
    """
    Inline class for Tasks.
    Tasks are on the workflow admin page available.
    """
    model = Task
    extra = 0
    # For TabularInline
    # fields = ['title', 'process', 'status', 'status_url']


class WorkflowAdmin(admin.ModelAdmin):
    """
    Admin class for Workflow.
    Specifies which fields of the model "Workflow" should be
    displayed on the admin page.
    should be displayed
    """
    list_display = ['name', 'percent_done', 'creator']
    inlines = [TaskInline]


    class Meta:
        model = Workflow


class TaskAdmin(admin.ModelAdmin):
    """
    Admin class for Workflow.
    Specifies which fields of the model "Task" should be
    displayed on the admin page.
    """
    list_display = ['title', 'workflow', 'status', 'status_url']
    list_filter = ['workflow']


    class Meta:
        model = Task


class EdgeAdmin(admin.ModelAdmin):
    """
    Admin class for Workflow.
    Specifies which fields of the model "Edge" should be
    displayed on the admin page.
    """
    list_filter = ['workflow']


    class Meta:
        model = Edge


class DataEdgeAdmin(admin.ModelAdmin):
    """
    Admin class for Workflow.
    Specifies which fields of the model "DataEdge" should be
    displayed on the admin page.
    """
    list_filter = ['workflow']


    class Meta:
        model = DataEdge


# Register all models


admin.site.register(Workflow, WorkflowAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Edge, EdgeAdmin)
admin.site.register(DataEdge, DataEdgeAdmin)
admin.site.register(SqlData)
admin.site.register(Session)
admin.site.register(Process)
admin.site.register(Artefact)
admin.site.register(WPS)
admin.site.register(WPSProvider)
admin.site.register(InputOutput)
