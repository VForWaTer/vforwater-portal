"""

"""

import base64
from datetime import time, datetime, timezone, timedelta

import matplotlib as mpl
from bokeh.layouts import column
from bokeh.models import Band, DatetimeTickFormatter, HoverTool, VBar, LinearAxis, Range1d
from bokeh.transform import linear_cmap
from django.db import connections
from io import BytesIO

from vfwheron.models import TblMeta, TblData
# mpl.use('Agg')
import matplotlib.pyplot as plt

import redis


# def get_preview(preview):
#     """
#
#     :param preview:
#     :type preview:
#     :return:
#     :rtype:
#     """
#     use_redis = True
#     in_cache = False
#     try:
#         r = redis.StrictRedis()
#         b64 = r.get("preview_{}".format(preview))
#     except:
#         use_redis = False
#     if use_redis:
#         if b64 is None:
#             in_cache = False
#         else:
#             b64 = str(b64, 'utf-8')
#             in_cache = True
#
#     if not in_cache:
#         # preview = 1157
#         label = TblMeta.objects.filter(id=preview).values_list('variable__variable_name',
#                                                                'variable__variable_symbol',
#                                                                'variable__unit__unit_abbrev')
#         ylabel = label[0][0] + ' (' + label[0][1] + ')' + ' [' + label[0][2] + ']'
#         # connect to database
#         cursor = connections['default'].cursor()
#         cursor.execute(
#                 "SELECT date_trunc('day', tstamp) as date, avg(value) as avg, "
#                 "min(value) as min, max(value) as max "
#                 "FROM tbl_data WHERE meta_id = %s GROUP BY date_trunc('day', tstamp);" % preview)
#         m = cursor.fetchall()
#         cursor.close()
#
#         x = [row[0] for row in m]
#         yavg = [row[1] for row in m]
#         ymin = [row[2] for row in m]
#         ymax = [row[3] for row in m]
#
#         fig, ax = plt.subplots(1, 1, figsize=(6, 4))
#         ax.plot(x, ymin, '-c', x, ymax, '-c', lw=0.3, label='Daily min/max')
#         ax.plot(x, yavg, '-b', lw=1, label="Daily average")
#         fig.autofmt_xdate(),
#         ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
#         ax.set_xlabel('Date')
#         ax.grid(which='major', axis='x')
#         ax.set_ylabel(ylabel)
#         ax.set_title('Dataset ' + str(preview))
#         # create tempfile and read as base64
#         tmpfile = BytesIO()
#         fig.savefig(tmpfile, format='png')
#         tmpfile.seek(0)
#         b64 = base64.b64encode(tmpfile.getvalue()).decode('utf8')
#         if use_redis:
#             r.set("preview_{}".format(preview), b64)
#
#             # create the image-tag
#     imgtag = "<img alt='data image' src='data:image/png;base64,%s'>" % b64
#     return str(imgtag)


def DB_load(ID):
    label = TblMeta.objects.filter(id=ID).values_list('variable__variable_name',
                                                      'variable__variable_symbol',
                                                      'variable__unit__unit_abbrev')
    ylabel = label[0][0] + ' (' + label[0][1] + ')' + ' [' + label[0][2] + ']'
    print('Label: ', label)
    print('yLabel: ', ylabel)
    print('yLabel: ', type(ylabel))
    # TODO: Use django ORM instead of pure sql
    # connect to database and fetch day(x), daily average, daily min, daily max, # of daily values
    cursor = connections['default'].cursor()
    cursor.execute("SELECT date_trunc('day', tstamp) as date, avg(value), "
                   "min(value), max(value), count(*) "
                   "FROM tbl_data "
                   "WHERE meta_id = %s "
                   "GROUP BY date_trunc('day', tstamp)"
                   "ORDER BY date ASC;" % ID)
    dbresult = cursor.fetchall()
    cursor.close()
    result = list(zip(*dbresult))
    axis = {'y1min': min(result[2]), 'y1max': max(result[3]), 'y2min': min(result[4]), 'y2max': max(result[4])}
    return {'data': result, 'ylabel': ylabel, 'axis': axis}


def get_preview(id):
    # id = 2657 # small test dataset
    use_redis = True
    in_cache = False
    try:
        r = redis.StrictRedis()
        img = r.get("preview_{}".format('b' + id))
    except:
        use_redis = False
    if use_redis:
        if img is None:
            in_cache = False
        else:
            img = str(img, 'utf-8')
            in_cache = True

    if not in_cache:
        DBdata = DB_load(id)

        from bokeh.plotting import figure
        from bokeh.models import ColumnDataSource
        from bokeh.embed import components
        source = ColumnDataSource({'date': DBdata['data'][0], 'y': DBdata['data'][1],
                                   'ymin': DBdata['data'][2], 'ymax': DBdata['data'][3],
                                   'count': DBdata['data'][4]})
        # TOOLTIPS = [("date", "@x{%F}"), ("value", "$y")]
        # formatters={'date': '@date{%F}'}

        # Plot average as main plot
        mainplot = figure(title='Daily average, min and max values', x_axis_label='Time', x_axis_type="datetime",
                          y_axis_label=DBdata['ylabel'],
                      plot_width=700, plot_height=500, toolbar_location="above",
                      tools="pan,wheel_zoom,box_zoom,reset", active_drag="box_zoom")
                      # tools="pan,wheel_zoom,box_zoom,reset,crosshair", active_drag="box_zoom", tooltips=TOOLTIPS)
        # mainplot.y_range = Range1d(round(DBdata['axis']['y1min']), round(DBdata['axis']['y1max']))

        # plot.toolbar.autohide = True
        # plot average line
        mainplot.line(x='date', y='y', source=source, line_width=2, legend_label="average")

        # TODO: Figure out how to use 'source' for multi_line.
        #  Maybe use Glyph? (https://docs.bokeh.org/en/latest/docs/reference/models/glyphs/multi_line.html)
        #  Glyphs maybe also helpful for hover_tool on multiline?
        # plot.add_tools(HoverTool(tooltips=[("value", "$y"), ("Date", "@date{%d %b %Y}")], formatters={"date": "datetime"}, mode="mouse"))

        mainplot.add_tools(HoverTool(tooltips=[("value at pointer", "$y")], mode="mouse"))

        # plot min/max as multiline and fill area with band
        mainplot.multi_line(xs=[DBdata['data'][0], DBdata['data'][0]],
                            ys=[DBdata['data'][2], DBdata['data'][3]], level='underlay',
                            color=['lightblue', 'lightblue'], legend_label="min & max values")
        mainplot.add_layout(Band(base='date', lower='ymin', upper='ymax', source=source, level='underlay',
                                 fill_color='lightblue', fill_alpha=0.5))

        # plot bars for the number of values in each group as secondary 'by'plot
        from bokeh.palettes import Oranges9
        mapper = linear_cmap(field_name='count', palette=Oranges9, low=0, high=DBdata['axis']['y2max'])
        width = DBdata['data'][0][1] - DBdata['data'][0][0]
        byplot = figure(title='Number of available values per day', x_axis_type="datetime", x_range=mainplot.x_range,
                        plot_width=700, plot_height=50, toolbar_location=None, background_fill_color="black")
        byplot.vbar(x='date', source=source, width=width, bottom=0, top=1, color=mapper)
        # byplot.vbar(x='date', source=source, width=width, bottom=0, top='count', color=mapper)
        byplot.xaxis.visible = False
        byplot.xgrid.visible = False
        byplot.yaxis.visible = False
        byplot.ygrid.visible = False
        byplot.add_tools(HoverTool(tooltips=[("# of values", "@count")], mode="mouse"))

        # Style the plot
        mainplot.title.text_font_size = "14pt"
        mainplot.xaxis.axis_label_text_font_size = "14pt"
        mainplot.xaxis.formatter = DatetimeTickFormatter(days=["%d %b %Y"], months=["%d %b %Y"], years=["%d %b %Y"])
        mainplot.yaxis.axis_label_text_font_size = "14pt"

        script, div = components(column(byplot, mainplot), wrap_script=False)
        img = {'script': script, 'div': div}
        if use_redis:
            r.set("preview_{}".format('b' + id), img)

    return img

