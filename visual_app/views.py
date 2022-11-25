import json

from django.shortcuts import render

from bokeh.plotting import figure, output_file, show
from bokeh.embed import components, json_item


def home(request):
    """
    Dummy page for Heron Visualisation tool.
    """
    x = [1, 2, 3, 4, 5]
    y = [1, 2, 3, 4, 5]
    plot = figure(title='Line Graph', x_axis_label='X-Axis', y_axis_label='Y-axis', width=400, height=400)
    plot.line(x, y, line_width=2)

    script, div = components(plot)
    return render(request, 'visual_app/home.html', {'script': script, 'div': div})
