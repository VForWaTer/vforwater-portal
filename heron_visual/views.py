import json

from django.shortcuts import render, render_to_response

#from heron_wps.forms import InputForm
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components, json_item


def home(request):
    """
    Dummy page for Heron Visualisation tool.
    """
    x = [1, 2, 3, 4, 5]
    y = [1, 2, 3, 4, 5]
    plot = figure(title='Line Graph', x_axis_label='X-Axis', y_axis_label='Y-axis', plot_width=400, plot_height=400)
    plot.line(x, y, line_width=2)

    script, div = components(plot)
    # print(script)
    # print(div)
    # return render('heron_visual/home.html', {'scipt': script, 'div': div})
    return render(request, 'heron_visual/home.html', {'script': script, 'div': div})

# def home(request):
#     """
#     Dummy page for Heron Visualisation tool.
#     """
#     return render(request, 'heron_visual/home.html')
#
