import json

from django.shortcuts import render
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components, json_item
from django.views import View






class HomeView(View):
    """
    Class-based view for the Heron Visualization Tool.
    """

    def get(self, request):
        """Handles GET requests and renders a Bokeh plot in the template."""

   
        x = [1, 2, 3, 4, 5]
        y = [1, 2, 3, 4, 5]

       
        plot = figure(title='Line Graph', x_axis_label='X-Axis', y_axis_label='Y-Axis', width=400, height=400)
        plot.line(x, y, line_width=2)

        script, div = components(plot)

        return render(request, 'visual_app/home.html', {'script': script, 'div': div})


