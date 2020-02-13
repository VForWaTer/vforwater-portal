"""

"""

from datetime import time, datetime, timezone, timedelta
from math import radians, ceil, sqrt

from bokeh.layouts import column
from bokeh.models import Band, DatetimeTickFormatter, HoverTool, AnnularWedge, LinearAxis, Grid, Plot, Range1d, \
    CustomJS
from bokeh.transform import linear_cmap
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.embed import components
from bokeh.palettes import Oranges9

from django.db import connections

from vfwheron.models import TblMeta, TblData

import redis


def DB_load_label(ID):
    label = TblMeta.objects.filter(id=ID).values_list('variable__variable_name',
                                                      'variable__variable_symbol',
                                                      'variable__unit__unit_abbrev')
    return label[0][0] + ' (' + label[0][1] + ')' + ' [' + label[0][2] + ']'


def DB_load_data(ID):
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
    # y1 is for the main plot -> min and  max of the day of the day,
    # y2 for the secondary plot with min and max in each group for each day
    axis = {'y1min': min(result[2]), 'y1max': max(result[3]), 'y2min': min(result[4]), 'y2max': max(result[4])}
    return {'data': result, 'axis': axis}


def get_bokeh_standard(DBdata, label):
    source = ColumnDataSource({'date': DBdata['data'][0], 'y': DBdata['data'][1],
                               'ymin': DBdata['data'][2], 'ymax': DBdata['data'][3],
                               'count': DBdata['data'][4]})
    # Plot average as main plot
    mainplot = figure(title='Daily average, min and max values', x_axis_label='Time', x_axis_type="datetime",
                      y_axis_label=label,
                      plot_width=700, plot_height=500, toolbar_location="above",
                      tools="pan,wheel_zoom,box_zoom,reset, save", active_drag="box_zoom")

    # plot.toolbar.autohide = True
    # plot average line
    mainplot.line(x='date', y='y', source=source, line_width=2, legend_label="average")

    # TODO: Figure out how to use 'source' for multi_line.
    #  Maybe use Glyph? (https://docs.bokeh.org/en/latest/docs/reference/models/glyphs/multi_line.html)
    #  Glyphs maybe also helpful for hover_tool on multiline?
    # plot.add_tools(HoverTool(tooltips=[("value", "$y"), ("Date", "@date{%d %b %Y}")], formatters={"date":
    # "datetime"}, mode="mouse"))

    mainplot.add_tools(HoverTool(tooltips=[("value at pointer", "$y")], mode="mouse"))

    # plot min/max as multiline and fill area with band
    mainplot.multi_line(xs=[DBdata['data'][0], DBdata['data'][0]],
                        ys=[DBdata['data'][2], DBdata['data'][3]], level='underlay',
                        color=['lightblue', 'lightblue'], legend_label="min & max values")
    mainplot.add_layout(Band(base='date', lower='ymin', upper='ymax', source=source, level='underlay',
                             fill_color='lightblue', fill_alpha=0.5))

    # plot bars for the number of values in each group as secondary 'by'plot
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
    return {'script': script, 'div': div}


def get_bokeh_direction(DBdata, label):
    source = ColumnDataSource({'date': DBdata['data'][0], 'avg': DBdata['data'][1],
                               'count': DBdata['data'][2], 'med': DBdata['data'][3]})
    avghist = [0] * 36
    for i in DBdata['data'][1]:
        avghist[i] += 1
    # better to use modal values:
    hist = [0] * 36
    for i in DBdata['data'][3]:
        hist[i] += 1
    x = list(range(0, 36))
    maxhist = max(hist)
    sumhist = sum(hist)

    # print('DBdata: ', DBdata['data'][2])
    print('avghist: ', avghist)

    mainplot = figure(title='Daily average and median count', plot_width=400, plot_height=400,
                      x_axis_type=None, y_axis_type=None, tools="save",
                      min_border=0, outline_line_color=None)
    mainplot.title.text_font_size = "14pt"
    for i in x:
        mainplot.wedge(radius=avghist[i], start_angle=-radians((i * 10) - 95), end_angle=-radians((i * 10) - 85),
                       x=0, y=0, direction='clock', fill_color='lightblue', legend_label='average')
        mainplot.wedge(radius=hist[i], start_angle=-radians((i * 10) - 95), end_angle=-radians((i * 10) - 85),
                       x=0, y=0, direction='clock', line_color='darkred', fill_color='lightsalmon', alpha=0.5,
                       legend_label='median')

    # create grid
    rund_perc = ceil(maxhist / sumhist * 100)
    labels = list(range(0, rund_perc, 2))
    labels.append(rund_perc)
    rad_pos = [i * sumhist / 100 for i in labels]
    out_rim = rad_pos[-1]
    label_pos = [sqrt(((i - 1) ** 2) / 2) for i in rad_pos]
    mainplot.text(label_pos[1:], label_pos[1:], [str(r) + ' %' for r in labels[1:]],
                  text_font_size="10pt", text_align="left", text_baseline="top")
    for rad in rad_pos:
        mainplot.circle(x=0, y=0, radius=rad, fill_color=None, line_color='grey', line_width=0.5, line_alpha=0.8)
    diagonal = sqrt((out_rim ** 2) / 2)
    mainplot.multi_line(xs=[[diagonal, -diagonal], [-diagonal, diagonal], [-out_rim, out_rim], [0, 0]],
                        ys=[[diagonal, -diagonal], [diagonal, -diagonal], [0, 0], [-out_rim, out_rim]],
                        line_color="grey", line_width=0.5, line_alpha=0.8)
    mainplot.x_range = Range1d(-out_rim*1.1, out_rim*1.1)
    mainplot.y_range = Range1d(-out_rim*1.1, out_rim*1.1)
    mainplot.legend.location = "top_left"
    mainplot.legend.click_policy = "hide"

    # add a slider
    # callback = CustomJS(args=dict(source=source), code="""
    #     var data = source.data;
    #     var f = cb_obj.value
    #     var x = data['x']
    #     var y = data['y']
    #     for (var i = 0; i < x.length; i++) {
    #         y[i] = Math.pow(x[i], f)
    #     }
    #     source.change.emit();
    # """)

    # plot bars for the number of values in each group as secondary 'by'plot
    mapper = linear_cmap(field_name='count', palette=Oranges9, low=0, high=max(DBdata['data'][2]))
    width = DBdata['data'][0][1] - DBdata['data'][0][0]
    byplot = figure(title='Number of available values per day', x_axis_type="datetime", #x_range=mainplot.x_range,
                    plot_width=400, plot_height=50, toolbar_location="above", background_fill_color="black",
                    tools="pan,wheel_zoom,box_zoom,reset", active_drag="box_zoom")
    byplot.vbar(x='date', source=source, width=width, bottom=0, top=1, color=mapper)
    byplot.xaxis.visible = False
    byplot.xgrid.visible = False
    byplot.yaxis.visible = False
    byplot.ygrid.visible = False
    byplot.add_tools(HoverTool(tooltips=[("value", "@count"), ("Date", "@date{%d %b %Y}")],
                               formatters={"date": "datetime"}, mode="mouse"))



    script, div = components(column(byplot, mainplot), wrap_script=False)
    # script, div = components(mainplot, wrap_script=False)
    return {'script': script, 'div': div}


def DB_load_directiondata(id):
    # TODO: Use django ORM instead of pure sql
    # create 36 groups with group 1 from 355-5 degree and 36 from 345-355 degree
    cursor = connections['default'].cursor()
    cursor.execute("SELECT date_trunc('day', tstamp)::date as date, "  # 0 = date
                   "trunc(degrees(atan2(avg(cos(radians(value))), avg(sin(radians(value)))))/10)::smallint as avg, "
                   "count(*) as amount, "  # 2 = amount
                   "trunc(percentile_disc(0.5) within group (order by value)/10)::smallint as med "  # 3 = med
                   "FROM tbl_data "
                   "WHERE meta_id = %s "
                   "GROUP BY date_trunc('day', tstamp) "
                   "ORDER BY date asc;" % id)
    dbresult = cursor.fetchall()
    cursor.close()
    result = list(zip(*dbresult))
    axis = {'y1min': min(result[1]), 'y1max': max(result[1])}
    return {'data': result, 'axis': axis}
    # return DB_load_data(id)


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
        label = DB_load_label(id)
        if label.find('direction') != -1:
            DBdata = DB_load_directiondata(id)
            # img = get_bokeh_standard(DBdata, label)
            img = get_bokeh_direction(DBdata, label)
        else:
            DBdata = DB_load_data(id)
            img = get_bokeh_standard(DBdata, label)

        if use_redis:
            r.set("preview_{}".format('b' + id), img)

    return img
