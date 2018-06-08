#!bin/bash
## v1.0
##
## This script will generate code documentation from epydoc-pydoc strings in code.
## For a file to be included it has to be added to the epydoc command. Even files with no functions
## should be included for a complete documentation.
## A list with all files can be found in the utilities folder.
##

cd ..
epydoc -v -o code_docu/ --parse-only --html wps_workflow/cron.py wps_workflow/admin.py wps_workflow/apps.py wps_workflow/models.py wps_workflow/tests.py wps_workflow/urls.py wps_workflow/utils.py wps_workflow/views.py wps_workflow/__init__.py heron/wsgi.py heron/router.py heron/urls.py heron/__init__.py heron/context_processors.py dashboard/admin.py dashboard/views.py dashboard/models.py dashboard/apps.py dashboard/urls.py dashboard/__init__.py dashboard/tests.py heron_upload/views.py heron_upload/models.py heron_upload/apps.py heron_upload/urls.py heron_upload/__init__.py heron_upload/forms.py heron_monitor/views.py heron_monitor/apps.py heron_monitor/urls.py heron_monitor/__init__.py AuthorizationManagement/admin.py AuthorizationManagement/views.py AuthorizationManagement/models.py AuthorizationManagement/apps.py AuthorizationManagement/tests/test_views.py AuthorizationManagement/tests/__init__.py AuthorizationManagement/tests/test_integration.py AuthorizationManagement/utilities.py AuthorizationManagement/urls.py AuthorizationManagement/__init__.py AuthorizationManagement/forms.py vfwheron/load_shp.py vfwheron/admin.py vfwheron/views.py vfwheron/query_functions.py vfwheron/models.py vfwheron/apps.py vfwheron/filter.py vfwheron/urls.py vfwheron/previewplot.py vfwheron/__init__.py vfwheron/geoserver_layer.py vfwheron/templatetags/markdown_filter.py vfwheron/templatetags/menutags.py vfwheron/templatetags/__init__.py vfwheron/tests.py heron_wps/templatetags_unused/tethys_wps.py heron_wps/templatetags_unused/__init__.py heron_wps/admin.py heron_wps/base.py heron_wps/views.py heron_wps/models.py heron_wps/apps.py heron_wps/utilities.py heron_wps/urls.py heron_wps/__init__.py heron_wps/forms.py heron_visual/views.py heron_visual/apps.py heron_visual/urls.py heron_visual/__init__.py
