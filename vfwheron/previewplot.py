"""

"""
import ast
import copy
import json
import pickle
from datetime import time
from math import radians, ceil, sqrt

from bokeh.layouts import column
from bokeh.models import Band, DatetimeTickFormatter, HoverTool, Range1d, CustomJS, ColumnDataSource, \
    DateSlider, DateRangeSlider, Whisker
from bokeh.transform import linear_cmap
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.palettes import Oranges9, Spectral11

from django.db import connections
from django.http.response import JsonResponse
from numpy import mean, subtract, add
import numpy as np

from vfwheron.models import Entries

import redis
import pandas as pd
import time

from wps_gui.models import WpsResults


def __DB_load_label(ID):
    label = Entries.objects.filter(id=ID).values_list('variable__name',
                                                      'variable__symbol',
                                                      'variable__unit__symbol')
    SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    superscript_label = label[0][2].replace("^", "").translate(SUP)
    return label[0][0] + ' (' + label[0][1] + ')' + ' [' + superscript_label + ']'
    # return label[0][0] + ' (' + label[0][1] + ')' + ' [' + label[0][2] + ']'


def __DB_load_data_avg(ID, scale='day'):
    datatable = Entries.objects.filter(id=ID).values_list('datasource__datatype__name', flat=True)[0]
    if datatable == 'timeseries':
        # TODO: Use django ORM instead of pure sql
        # connect to database and fetch day(x), daily average, daily min, daily max, # of daily values
        cursor = connections['default'].cursor()
        # noinspection SqlResolve
        cursor.execute("SELECT date_trunc('{2}', tstamp) as date, "
                       "avg(value), min(value), max(value), count(*), "
                       "avg(precision) as prec_avg, min(precision) as prec_min, max(precision) as prec_max "
                       "FROM {0} "
                       "WHERE entry_id = {1} "
                       "GROUP BY date_trunc('{2}', tstamp)"
                       "ORDER BY date ASC;".format(datatable, ID, scale))
        dbresult = cursor.fetchall()
        cursor.close()
        result = list(zip(*dbresult))
        # y1 is for the main plot -> min and  max of the day of the day,
        # y2 for the secondary plot with min and max in each group for each day
        axis = {'y1min': min(result[2]), 'y1max': max(result[3]), 'y2min': min(result[4]), 'y2max': max(result[4])}
        return {'data': result, 'axis': axis}
    else:
        print('*** PLEASE IMPLEMENT OTHER DATATYPES, TOO! ***')


def get_bokeh_standard(db_data: object, size: list, label: str = "") -> object:
    """

    :param db_data: data result from DB_load_data_avg
    :param size:
    :param label:
    :return:
    """
    # use first five time steps to estimate resolution/step size of data
    stepsize = []
    steps = 0
    while steps < 5:
        stepsize.append(db_data['data'][0][steps + 1] - db_data['data'][0][steps])
        steps += 1

    # check if data is continuous. If not write position of missing values in noDataPos
    stepsize = min(stepsize)
    datalength = len(db_data['data'][0])
    noDataPos = []
    for steps in range(1, datalength):
        if db_data['data'][0][steps] - db_data['data'][0][steps - 1] > stepsize:
            noDataPos.append(steps - 1)

    # check if dataset has values for precision
    has_precision = True
    try:
        sum(db_data['data'][7])
    except TypeError:
        has_precision = False

    nan_in_data = False
    # To get a discontinuous line add 'nan' when a time step is missing.
    white_line = ()
    if len(noDataPos) > 0:
        nan_in_data = True
        white_line = tuple([float('nan')] * datalength)
        for position in noDataPos[::-1]:
            db_data['data'][0] = db_data['data'][0][: position + 1] + \
                                 (db_data['data'][0][position] + stepsize,
                                  db_data['data'][0][position + 1] - stepsize,) + \
                                 db_data['data'][0][position + 1:]
            db_data['data'][1] = db_data['data'][1][: position + 1] + (float('nan'), float('nan'),) + \
                                 db_data['data'][1][position + 1:]
            bandbef = (db_data['data'][2][position] + db_data['data'][3][position]) / 2
            bandaft = (db_data['data'][2][position + 1] + db_data['data'][3][position + 1]) / 2
            db_data['data'][2] = db_data['data'][2][: position + 1] + (bandbef, bandaft,) + db_data['data'][2][
                                                                                            position + 1:]
            db_data['data'][3] = db_data['data'][3][: position + 1] + (bandbef, bandaft,) + db_data['data'][3][
                                                                                            position + 1:]
            db_data['data'][4] = db_data['data'][4][: position + 1] + (0, 0,) + db_data['data'][4][position + 1:]
            white_line = white_line[: position + 1] + (bandbef, bandaft,) + white_line[position + 1:]
        if has_precision:
            for position in noDataPos[::-1]:
                db_data['data'][5] = db_data['data'][5][: position + 1] + (float('nan'), float('nan'),) + \
                                     db_data['data'][5][position + 1:]
                db_data['data'][6] = db_data['data'][6][: position + 1] + (float('nan'), float('nan'),) + \
                                     db_data['data'][6][position + 1:]
                db_data['data'][7] = db_data['data'][7][: position + 1] + (float('nan'), float('nan'),) + \
                                     db_data['data'][7][position + 1:]
                # prec_bandbef = (db_data['data'][6][position] + db_data['data'][7][position]) / 2
                # prec_bandaft = (db_data['data'][6][position + 1] + db_data['data'][7][position + 1]) / 2

    source = ColumnDataSource({'date': db_data['data'][0], 'y': db_data['data'][1],
                               'ymin': db_data['data'][2], 'ymax': db_data['data'][3],
                               'count': db_data['data'][4]})
    # Plot average as main plot
    mainplot = figure(title='Daily average, min and max values', x_axis_label='Time', x_axis_type="datetime",
                      y_axis_label=label, sizing_mode='scale_both',
                      plot_width=size[0], plot_height=size[1] - 50, toolbar_location="above",
                      tools="pan,wheel_zoom,box_zoom,reset, save", active_drag="box_zoom")
    # plot.toolbar.autohide = True

    # plot average line
    mainplot.line(x='date', y='y', source=source, line_width=2, legend_label="average", level="overlay")

    # TODO: Figure out how to use 'source' for multi_line.
    #  Maybe use Glyph? (https://docs.bokeh.org/en/latest/docs/reference/models/glyphs/multi_line.html)
    #  Glyphs maybe also helpful for hover_tool on multiline?
    mainplot.add_tools(HoverTool(tooltips=[("value", "@y"), ("Date", "@date{%d %b %Y}")],
                                 formatters={"@date": "datetime"}, mode="mouse"))

    # mainplot.add_tools(HoverTool(tooltips=[("value at pointer", "$y")], mode="mouse"))

    # plot min/max as multiline and fill area with band
    mainplot.multi_line(xs=[db_data['data'][0], db_data['data'][0]],
                        ys=[db_data['data'][2], db_data['data'][3]], level='underlay',
                        color=['lightblue', 'lightblue'], legend_label="min & max values")
    mainplot.add_layout(Band(base='date', lower='ymin', upper='ymax', source=source, level='underlay',
                             fill_color='lightblue', fill_alpha=0.5))

    # plot white line to hide small band for no data areas
    if nan_in_data:
        mainplot.line(x=db_data['data'][0], y=white_line, line_width=2, line_color='white', line_cap='round')

    # plot first average precision to have it in the background
    if has_precision:
        # precision = ColumnDataSource({'date': db_data['data'][0], 'y': db_data['data'][5],
        #                               'ymin': db_data['data'][6], 'ymax': db_data['data'][7]})
        # mainplot.line(x='date', y='y', source=precision, line_width=2, line_dash='dashed',
        #               legend_label="average_precision", color='darksalmon')
        # mainplot.multi_line(xs=[db_data['data'][0], db_data['data'][0]],
        #                     ys=[db_data['data'][6], db_data['data'][7]], level='underlay',
        #                     color=['darksalmon', 'darksalmon'], line_dash='dashed',
        #                     legend_label="min & max precision values")
        # mainplot.add_layout(Band(base='date', lower='ymin', upper='ymax', source=precision, level='underlay',
        #                          fill_color='darksalmon', fill_alpha=0.3))

        # add errorbars
        data = np.array(db_data['data'][1], dtype=np.float)
        lower_error = tuple(subtract(data, np.array(db_data['data'][7], dtype=np.float)))
        upper_error = tuple(add(data, np.array(db_data['data'][7], dtype=np.float)))
        low_avg_error = tuple(subtract(data, np.array(db_data['data'][5], dtype=np.float)))
        up_avg_error = tuple(add(data, np.array(db_data['data'][5], dtype=np.float)))
        error_source = ColumnDataSource({'date': db_data['data'][0], 'upper': upper_error, 'lower': lower_error,
                                         'upper_avg': up_avg_error, 'lower_avg': low_avg_error})
        mainplot.add_layout(Whisker(source=error_source, base="date", upper="upper", lower="lower",
                                    line_width=0.5))
        mainplot.vbar(x='date', width=1000 * 60 * 59 * 24, top='upper_avg', bottom='lower_avg', source=error_source,
                      fill_color="darksalmon", line_color="black", fill_alpha=0.3, line_width=0.5,
                      legend_label="Average precision")

    # plot bars for the number of values in each group as secondary 'by'plot
    mapper = linear_cmap(field_name='count', palette=Oranges9, low=0, high=db_data['axis']['y2max'])
    bin_width = db_data['data'][0][1] - db_data['data'][0][0]
    distriplot = distribution_plot(source, mapper, bin_width, 'Number of available values per day', size[0])
    distriplot.x_range = mainplot.x_range
    # Style the plot
    mainplot.title.text_font_size = "14pt"
    mainplot.xaxis.axis_label_text_font_size = "14pt"
    mainplot.xaxis.formatter = DatetimeTickFormatter(days=["%d %b %Y"], months=["%d %b %Y"], years=["%d %b %Y"])
    mainplot.yaxis.axis_label_text_font_size = "14pt"
    mainplot.legend.click_policy = "hide"
    # mainplot.sizing_mode = "stretch_both"
    script, div = components(column(distriplot, mainplot), wrap_script=False)
    return {'script': script, 'div': div}


def get_bokeh_direction(db_data, ti):
    # use data in percent => transform db_data to percent
    pct_data = []
    for tc in range(0, len(db_data)):  # 4
        all_direct = db_data[tc][1]
        datalist = [db_data[tc][0], all_direct]
        for single_bin in range(2, len(db_data[tc])):
            datalist.append(db_data[tc][single_bin] * 100 / all_direct)
        pct_data.append(tuple(datalist))

    db_datadict = {item[0]: item[2:] for item in pct_data}
    df = pd.DataFrame(db_datadict)
    db_datadictstr = {str(int(time.mktime(item[0].timetuple()) * 1000)): list(item[2:]) for item in pct_data}

    hist = [0] * 36
    maxlist = [0] * 36
    data_list = list(zip(*(pct_data)))

    for i in range(2, len(data_list)):
        hist[i - 3] = mean(data_list[i])
        maxlist[i - 3] = max(data_list[i])

    # maxhist = sorted(maxlist)[-3]
    maxhist = mean(maxlist) * 0.8  # don't use real max of dataset, too many discordant values
    sumhist = sum(hist)
    start = [-radians((i * 10) - 85) for i in list(range(0, 36))]
    end = [-radians((i * 10) - 75) for i in list(range(0, 36))]
    pdstart = [-radians((i * 10) - 95) for i in list(range(0, 36))]
    pdend = [-radians((i * 10) - 85) for i in list(range(0, 36))]
    labeltext = ("Selection of " + ti + "ly histograms")
    titletext = (ti + 'ly median and sum of all histograms').capitalize()
    pdsource = ColumnDataSource(data=dict(radius=hist, start=pdstart, end=pdend))
    jssource = ColumnDataSource(data=db_datadictstr)

    mainplot = figure(title=titletext, plot_width=400, plot_height=400,
                      x_axis_type=None, y_axis_type=None, tools="save",
                      min_border=0, outline_line_color=None)
    mainplot.title.text_font_size = "14pt"
    # simple rose plot
    mainplot.wedge(radius=hist, start_angle=start, end_angle=end, x=0, y=0, direction='clock', line_color='blue',
                   fill_color='lightblue', alpha=0.5, legend_label='Whole dataset')
    # plot connected to slider
    mainplot.wedge(radius='radius', start_angle='start', end_angle='end', source=pdsource, x=0, y=0, alpha=0.5,
                   direction='clock', line_color='darkred', fill_color='lightsalmon', legend_label=labeltext)

    # create slider
    day = 1000 * 3600 * 24
    stepsize = day
    if ti == 'week':
        stepsize = day
    elif ti == 'month':
        stepsize = 7 * day
    elif ti == 'year':
        stepsize = 30 * day

    slider = DateSlider(start=min(df.columns), end=max(df.columns), value=min(df.columns), step=stepsize,
                        title="date within histogram")
    callback = CustomJS(
        args=dict(source=pdsource, data=jssource, slid=slider), code="""
            const S = slid.value;
            let radius = source.data.radius;
            const radii = Object.keys(data.data)
            let slidestop = radii.reduce(function(prev, curr) {
            (Math.abs(curr - S) < Math.abs(prev - S) ? curr : prev)
             return (Math.abs(curr - S) < Math.abs(prev - S) ? curr : prev);
            });
            source.data.radius = data.data[slidestop]
            source.change.emit();
        """)
    slider.js_on_change('value', callback)

    # create range slider
    rslider = DateRangeSlider(start=min(df.columns), end=max(df.columns), value=(min(df.columns), max(df.columns)),
                              step=stepsize, title="Data within date range from ")
    rcallback = CustomJS(
        args=dict(source=pdsource, data=jssource, rslid=rslider), code="""
            const smin = rslid.value[0]
            const smax = rslid.value[1]
            let radius = source.data.radius;
            const radii = Object.keys(data.data)
            let lstop = radii.reduce(function(prev, curr) {
             return (Math.abs(curr - smin) < Math.abs(prev - smin) ? curr : prev);
            });
            let rstop = radii.reduceRight(function(prev, curr) {
             return (Math.abs(curr - smax) < Math.abs(prev - smax) ? curr : prev);
            });
            let keylist = [];
            for (let k in data.data) keylist.push(k);
            let fromkey = keylist.indexOf(lstop);
            let tokey = keylist.indexOf(rstop);
            let rangekeys = keylist.slice(fromkey, tokey)
            var dataavg = Array(36).fill(0)
            var count = 0;
            for (let k of rangekeys) {
                dataavg = dataavg.map(function (num, idx) {return num + data.data[k][idx];});
                count += 1
            }
            dataavg = dataavg.map(function (num, idx) {return num/count;});
            source.data.radius = dataavg;
            source.change.emit();
        """)
    rslider.js_on_change('value', rcallback)

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
    mainplot.x_range = Range1d(-out_rim * 1.1, out_rim * 1.1)
    mainplot.y_range = Range1d(-out_rim * 1.1, out_rim * 1.1)
    mainplot.legend.location = "top_left"
    mainplot.legend.click_policy = "hide"

    allcounts = [i[1] for i in db_data]
    alldates = [i[0] for i in db_data]

    # plot bars for the number of values in each group as secondary 'by' plot
    mapper = linear_cmap(field_name='count', palette=Oranges9, low=0, high=max(allcounts))
    bin_width = db_data[0][0] - db_data[1][0]
    source = ColumnDataSource({'date': alldates, 'count': allcounts})
    distriplot = distribution_plot(source, mapper, bin_width, 'Number of values per cluster', 400)

    script, div = components(column(distriplot, mainplot, slider, rslider), wrap_script=False)
    return {'div': div, 'script': script}


def __DB_load_directiondata(id, ti):
    # TODO: Use django ORM instead of pure sql
    cursor = connections['default'].cursor()
    # create 36 groups with group 1 from 355-5 degree and 36 from 345-355 degree
    sum_string = ""
    for i in range(1, 36):
        sum_string += "count(*) FILTER (WHERE trunc(((value)+5)/10)::smallint = %i ) as b%i," % (i, i)

    cursor.execute("SELECT date_trunc('%s', tstamp)::date as date, count(*), "
                   "count(*) FILTER (WHERE trunc(((value)+5)/10)::smallint = 0 "
                   "or trunc(((value)+5)/10)::smallint = 36) as b0, %s "
                   "from tbl_data where meta_id = %s "
                   "group by date_trunc('%s', tstamp);" % (ti, sum_string[:-1], id, ti))

    dbresult = cursor.fetchall()
    cursor.close()
    return dbresult


def get_timeseries_plot(data, size):
    mainplot = get_main_plot(data, size, y_label='value', x_label="Time", x_type="datetime", type='line',
                             title='Daily average, min and max values')
    script, div = components(mainplot, wrap_script=False)
    return {'script': script, 'div': div}


def get_xy_plot(data, size):
    x_label = data.columns[0]
    y_label = data.columns[1]

    mainplot = get_main_plot(data, size, y_label=y_label, x_label=x_label, x_type="linear", type='scatter', title='')
    mainplot.sizing_mode = 'scale_both'
    script, div = components(mainplot, wrap_script=False)
    return {'script': script, 'div': div}


def get_main_plot(data, size, y_label='value', x_label="x axis", x_type="linear", type="line",
                  title='Daily average, min and max values'):
    mainplot = figure(title=title, x_axis_label=x_label, x_axis_type=x_type,
                      y_axis_label=y_label,
                      plot_width=size[0], plot_height=size[1], toolbar_location="above",
                      tools="pan,wheel_zoom,box_zoom,reset, save", active_drag="box_zoom")
    # plot.toolbar.autohide = True
    # plot line
    # mainplot.line(data.index.values, data['value'], line_width=2)
    if type == 'line':
        numlines = len(data.columns)
        mainplot.multi_line(xs=[data.index.values] * numlines, ys=[data[name].values for name in data],
                            line_color=Spectral11[0:numlines], line_width=2)
    elif type == 'scatter':
        mainplot.line(x=data[x_label], y=data[y_label], line_width=2)

    # mainplot.line(x='tstamp', y='value', source=source, line_width=2)
    # Style the plot
    mainplot.title.text_font_size = "14pt"
    mainplot.xaxis.axis_label_text_font_size = "14pt"
    if x_type == 'datetime':
        mainplot.xaxis.formatter = DatetimeTickFormatter(days=["%d %b %Y"], months=["%d %b %Y"], years=["%d %b %Y"])
    mainplot.yaxis.axis_label_text_font_size = "14pt"
    return mainplot


def distribution_plot(source: object, mapper: dict, bin_width, title: str, plot_width: int):
    """
    Small bar on top of the main plot to show how many datasets are available in each trunc.

    :param source: a ColumnDataSource
    :param mapper: e.g. {'field': 'count', 'transform': LinearColorMapper(id='1092', ...)}
    :param bin_width: bin width in format of x axes, e.g. 1 day
    :param title: headline for distribution
    :param plot_width: width of the plot
    :return:
    """
    p = figure(title=title, x_axis_type="datetime",  # x_range=mainplot.x_range,
               plot_width=plot_width, plot_height=50, toolbar_location="above", background_fill_color="black",
               tools="pan,wheel_zoom,box_zoom,reset", active_drag="box_zoom", sizing_mode='scale_width')
    p.vbar(x='date', source=source, width=bin_width, bottom=0, top=1, color=mapper)
    p.xaxis.visible = False
    p.xgrid.visible = False
    p.yaxis.visible = False
    p.ygrid.visible = False
    p.add_tools(HoverTool(tooltips=[("Values/Day", "@count"), ("Date", "@date{%d %b %Y}")],
                          formatters={"@date": "datetime"}, mode="mouse"))
    return p


def get_preview(id: str, size=[700, 500]):
    """
    Check which is the source for the dataset and if a preview image is already cached. Return html of a plot.

    :param id: id of a dataset. Integers or dbXX for DB as source, wpsXX for wps result.
    :param size: size of resulting plot [width, height]
    :type size: list
    :return: html ready to render
    """
    # id = 2657 # small test dataset
    try:
        wps_result = True if 'wps' in id[0:3] else False
    except:
        wps_result = False
    use_redis = True
    in_cache = False

    try:
        r = redis.StrictRedis()
        img = r.get("preview_{}".format('b' + id + size))
    except:
        use_redis = False

    if use_redis:
        if img is None:
            in_cache = False
        else:
            img = str(img, 'utf-8')
            in_cache = True

    if not in_cache and not wps_result:
        label = __DB_load_label(id)
        if label.find('direction') != -1:
            ti = 'week'  # time interval used to plot, choose 'year', 'month', 'week' or 'day'
            db_data = __DB_load_directiondata(id, ti)
            # img = get_bokeh_standard(db_data, label)
            img = get_bokeh_direction(db_data, ti)
        else:
            db_data = __DB_load_data_avg(id)
            img = get_bokeh_standard(db_data, size, label)

        if use_redis:
            r.set("preview_{}".format('b' + id), img)

    if wps_result:
        DBstring = ast.literal_eval(WpsResults.objects.get(id=id[3:]).outputs)
        try:
            # if 'ts-pickle' in DBstring[1]:
            if 'pickle' in DBstring[1]:
                df = pd.read_pickle(DBstring[2])
                if 'ts-pickle' in DBstring[1]:
                    img = get_timeseries_plot(df, size)
                elif DBstring[1] == 'pickle':
                    img = get_xy_plot(df, size)
            elif DBstring[1] == 'image':
                try:
                    file = open(DBstring[2], mode='r')
                    htmlimg = file.read()
                    file.close()
                except FileNotFoundError:
                    print('Error: Can not load your image')
                    htmlimg = 'Error: Can not load your image'
                img = {'html': htmlimg}
            else:
                print('Error: Con not plot. Unknown type')

        # with open(DBstring, 'rb') as f:
        #    data = pickle.load(f)
        except FileNotFoundError:
            print('The data file %s was not found.' % (DBstring[2]))

    return img
