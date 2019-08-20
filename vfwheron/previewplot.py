"""

"""

import base64
import matplotlib as mpl
from django.db import connections
from io import BytesIO

from vfwheron.models import TblMeta

# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# import plotly
# import plotly.plotly as ply
# import plotly.graph_objs as go

mpl.use('Agg')
import matplotlib.pyplot as plt

import redis


def get_preview(preview):
    """

    :param preview:
    :type preview:
    :return:
    :rtype:
    """
    use_redis = True
    in_cache = False
    try:
        r = redis.StrictRedis()
        b64 = r.get("preview_{}".format(preview))
    except:
        use_redis = False
    if use_redis:
        if b64 is None:
            in_cache = False
        else:
            b64 = str(b64, 'utf-8')
            in_cache = True

    if not in_cache:
        # preview = 1157
        label = TblMeta.objects.filter(id=preview).values_list('variable__variable_name',
                                                               'variable__variable_symbol',
                                                               'variable__unit__unit_abbrev')
        ylabel = label[0][0] + ' (' + label[0][1] + ')' + ' [' + label[0][2] + ']'
        # connect to database
        cursor = connections['vforwater'].cursor()
        cursor.execute(
                "SELECT date_trunc('day', tstamp) as date, avg(value) as avg, "
                "min(value) as min, max(value) as max "
                "FROM tbl_data WHERE meta_id = %s GROUP BY date_trunc('day', tstamp);" % preview)
        m = cursor.fetchall()
        cursor.close()

        x = [row[0] for row in m]
        yavg = [row[1] for row in m]
        ymin = [row[2] for row in m]
        ymax = [row[3] for row in m]

        fig, ax = plt.subplots(1, 1, figsize=(6, 4))
        ax.plot(x, ymin, '-c', x, ymax, '-c', lw=0.3, label='Daily min/max')
        ax.plot(x, yavg, '-b', lw=1, label="Daily average")
        fig.autofmt_xdate(),
        ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
        ax.set_xlabel('Date')
        ax.grid(which='major', axis='x')
        ax.set_ylabel(ylabel)
        ax.set_title('Dataset ' + str(preview))
        # create tempfile and read as base64
        tmpfile = BytesIO()
        fig.savefig(tmpfile, format='png')
        tmpfile.seek(0)
        b64 = base64.b64encode(tmpfile.getvalue()).decode('utf8')
        if use_redis:
            r.set("preview_{}".format(preview), b64)

            # create the image-tag
    imgtag = "<img alt='data image' src='data:image/png;base64,%s'>" % b64
    # imgtag = newplotplotly(x, ymax)
    # return newplotbokeh(x, ymax)
    return str(imgtag)

def newplotbokeh(x, ymax):
    print('+++++++++++++++++++++ start')

    import numpy as np
    import pandas as pd
    # from bokeh.palettes import d3 as palette
    # from bokeh.palettes import Spectral4
    # from bokeh.io import output_notebook
    # from bokeh.io import export_svgs
    from bokeh.models import SingleIntervalTicker, LinearAxis, Range1d, plots
    from bokeh.layouts import row, widgetbox
    from bokeh.models import CustomJS, Slider
    from bokeh.plotting import figure, output_file, show, ColumnDataSource
    from bokeh.models import Legend
    import itertools

    colname = ['2_weeks', '4_weeks']
    cols_orig = np.array([[15.68, 32.53], [15.7, 32.6], [16.03, 32.67]])
    cols_evol = np.array([[7.23, 14.83], [7.65, 15.4], [7.4, 15.0]])
    df_runtime_orig = pd.DataFrame(data=cols_orig, columns=colname)
    df_runtime_evol = pd.DataFrame(data=cols_evol, columns=colname)
    legend_it = []

    # output_notebook()

    # color = itertools.cycle(palette['Category10'][6])
    TOOLS = "pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"
    p = figure(tools=TOOLS, plot_width=600, plot_height=350, x_range=df_runtime_orig.columns.values,
               x_axis_label='Simulation Duration', y_axis_label='Run Time (h)')

    pl = p.circle(df_runtime_orig.columns.values, df_runtime_orig.mean(), size=10, fill_color='#d62728',
                  line_color='black')
    legend_it.append(('Original', [pl]))
    pl = p.triangle(df_runtime_evol.columns.values, df_runtime_evol.mean(), size=10, fill_color='#2ca02c',
                    line_color='black')
    legend_it.append(('Evolutionary', [pl]))

    legend = Legend(items=legend_it, location="center")
    p.add_layout(legend, 'right')
    p.legend.click_policy = "hide"

    p.xaxis.major_label_text_font_size = "12pt"
    p.yaxis.major_label_text_font_size = "12pt"
    p.xaxis.axis_label_text_font_size = "12pt"
    p.yaxis.axis_label_text_font_size = "12pt"
    p.legend.label_text_font_size = "12pt"
    # p.output_backend = "svg"
    # export_svgs(p, filename="runtime.svg")
    output_file("interactive_legend.html", title="interactive_legend.py example")
    # show(p)
    print(output_file)
    from bokeh.resources import CDN
    from bokeh.embed import file_html
    from bokeh.embed import components

    html = file_html(p, CDN, "my plot")
    script, div = components(p)
    print('+++++++++++++++++++++ end')
    html = {"script": script, "div": div}
    return html

def newplotplotly(x, ymax):
    print('------------------------------')
    print('start plotly')
    # import plotly.offline as opy
    import plotly.graph_objs as go
    from plotly.offline import plot
    # from django.template import context
    trace1 = go.Scatter(
        x=x,
        y=ymax,
        mode='lines',
        name='lines',
    )
    layout = go.Layout(
        # autosize=True,
        # width = 800,
        # height=900,
        xaxis=dict(
            autorange=True
        ),
        yaxis=dict(
            autorange=True
        )
    )
    plot_data = [trace1]
    figure = go.Figure(data=plot_data, layout=layout)
    plot_div = plot(figure, output_type='div', include_plotlyjs=False)
    print('end plotly: ', plot_div)
    return plot_div

# class DataDisplayDownsampler(object):
#     def __init__(self, xdata, ydata):
#         self.origYData = ydata
#         self.origXData = xdata
#         self.max_points = 50
#         self.delta = xdata[-1] - xdata[0]
#
#     def downsample(self, xstart, xend):
#         # get the points in the view range
#         mask = (self.origXData > xstart) & (self.origXData < xend)
#         # dilate the mask by one to catch the points just outside
#         # of the view range to not truncate the line
#         mask = np.convolve([1, 1], mask, mode='same').astype(bool)
#         # sort out how many points to drop
#         ratio = max(np.sum(mask) // self.max_points, 1)
#
#         # mask data
#         xdata = self.origXData[mask]
#         ydata = self.origYData[mask]
#
#         # downsample data
#         xdata = xdata[::ratio]
#         ydata = ydata[::ratio]
#
#         print("using {} of {} visible points".format(
#             len(ydata), np.sum(mask)))
#
#         return xdata, ydata
#
#     def update(self, ax):
#         # Update the line
#         lims = ax.viewLim
#         if np.abs(lims.width - self.delta) > 1e-8:
#             self.delta = lims.width
#             xstart, xend = lims.intervalx
#             self.line.set_data(*self.downsample(xstart, xend))
#             ax.figure.canvas.draw_idle()


#
# def plotly_plot():
#     plotly.offline.plot()
#     # preview = request.GET.get('preview')
#     t = time.time()
#     preview = 1157
#     label = TblMeta.objects.filter(id=preview).values_list('variable__variable_name',
#                                                            'variable__variable_symbol', 'variable__unit__unit_abbrev')
#     ylabel = label[0][0] + ' (' + label[0][1] + ')' + ' [' + label[0][2] + ']'
#     label_time = time.time()
#     # connect to database
#     cursor = connections['vforwater'].cursor()
#     cursor.execute(
#         # 'SELECT tbl_data.tstamp, tbl_data.value FROM public.tbl_data WHERE tbl_data.meta_id = %s' % preview)
#         "SELECT date_trunc('day', tstamp) as date, avg(value) as avg, "
#         "min(value) as min, max(value) as max "
#         # "stddev(value) as stddev "
#         "FROM tbl_data WHERE meta_id = %s GROUP BY date_trunc('day', tstamp);" % preview)
#     m = cursor.fetchall()
#     cursor.close()
#
#     DB_time = time.time()
#     x = [row[0] for row in m]
#     yavg = [row[1] for row in m]
#     ymin = [row[2] for row in m]
#     ymax = [row[3] for row in m]
#     DB_list_time = time.time()
#
#     print('----plotly plot --------------')
#     # django queryset seems to be fast, but query is executed when data is accessed. And that is very slow
#     # dataset_query = TblData.objects.filter(meta_id=preview).annotate(day=TruncDay('tstamp')).values_list('day').\
#     #     annotate(avg=Avg('value')).annotate(max=Max('value')).annotate(min=Min('value')) #  .order_by('tstamp')
#     # the following is slow, because there is the access to the database
#     # x = [row[0] for row in dataset_query]
#     # yavg = [row[1] for row in dataset_query]
#     # ymin = [row[2] for row in dataset_query]
#     # ymax = [row[3] for row in dataset_query]
#
#     fig, ax = plt.subplots(1, 1, figsize=(6, 4))
#     ax.plot(x, yavg, '-b', lw=2)
#     fig.autofmt_xdate(),
#     ax.set_xlabel('Date')
#     ax.grid(which='major', axis='x')
#     ax.set_ylabel(ylabel)
#     ax.set_title('Dataset preview')
#
#     data = [go.Scatter(
#         x=x,
#         y=m[1])]
#     ply.plot(data)
#
#     image_time = time.time()
#     # create tempfile and read as base64
#     tmpFile = BytesIO()
#     fig.savefig(tmpFile, format='png')
#     tmpFile.seek(0)
#     b64 = base64.b64encode(tmpFile.getvalue())
#
#     tmpfile_time = time.time()
#
#
#     Gesamtzeit = time.time() - t
#     print('** label_time: ', round(label_time - t, 2))
#     print('** DB_time: ', round(DB_time - t, 2), round(DB_time - t - (label_time - t), 2))
#     print('** DB_list_time: ', round(DB_list_time - t, 2), round(DB_list_time - t - (DB_time - t), 2))
#     print('** image_time: ', round(image_time - t, 2), round(image_time - t - (DB_list_time - t), 2))
#     print('** tmpfile_time: ', round(tmpfile_time - t, 2), round(tmpfile_time - t - (image_time - t), 2))
#     print('** Gesamtzeit: ', round(Gesamtzeit, 2))
#     # create the image-tag
#     imgtag = "<img alt='data image' src='data:image/png;base64,%s'>" % b64.decode('utf8')
#     return 0
