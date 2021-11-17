"""

"""
import ast
from datetime import time
from math import radians, ceil, sqrt

from django.utils.translation import gettext
from bokeh.io import show
from bokeh.layouts import column
from bokeh.models import Band, DatetimeTickFormatter, HoverTool, Range1d, CustomJS, ColumnDataSource, \
    DateSlider, DateRangeSlider, Whisker, BoxAnnotation
from bokeh.transform import linear_cmap
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.palettes import Oranges9, Spectral11

from numpy import mean

from heron.settings import max_size_preview_plot
from vfwheron.data_tools import __DB_load_directiondata, fill_data_gaps, __DB_load_data_avg, __DB_load_data, \
    precision_to_minmax, __get_axis_limits
from vfwheron.models import Entries

import redis
import pandas as pd
import time

from wps_gui.models import WpsResults


def __DB_load_label(ID: int):
    """
    Load informaton for a plot label from database

    :param ID:
    :return: str
    """
    label = Entries.objects.filter(id=ID)\
        .values_list('variable__name', 'variable__symbol', 'variable__unit__symbol')
    return format_label(label[0][0], label[0][1], label[0][2])


def format_label(name: str, symbol: str, unit_symbol: str):
    """
    format label for plots from variable name, symbol and unit symbol

    :param name:
    :param symbol:
    :param unit_symbol:
    :return:  str
    """
    sup = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    superscript_label = unit_symbol.replace("^", "").translate(sup)
    return "{} ({}) [{}]".format(name, symbol, superscript_label)


def get_bokeh_std_fullres(plot_data: object, full_res: bool, size: list, label: str = "") -> object:
    """
    Plot with full resolution, hence one line with errorbars, no band

    :param plot_data: dict - pandas dataframe to plot and some additional information
    :param full_res: boolean - True if data is complete else only latest n values
    :param size: list - size of plot
    :param label: str - title for plot
    :return:
    """
    nan_in_data = plot_data['nan_in_data']
    source = ColumnDataSource(plot_data['df'])
    missing_source = ColumnDataSource(plot_data['missing_data'])
    if full_res:
        title = ''
    else:
        title = gettext("Showing only latest {0} datapoints.").format(str(max_size_preview_plot))
    # Plot average as main plot
    mainplot = figure(x_axis_label='Time', x_axis_type="datetime",
                      y_axis_label=label,
                      title=title,
                      # sizing_mode='stretch_both',
                      plot_width=size[0], plot_height=int(size[1] * 0.9), toolbar_location="above",
                      tools="pan,wheel_zoom,box_zoom,reset, save", active_drag="box_zoom")

    # plot value line
    mainplot.line(x='tstamp', y='value', source=source, line_width=3)  #, legend_label="measured values")

    mainplot.add_tools(HoverTool(tooltips=[(gettext("Value"), "@value"),
                                           (gettext("Time"), "@tstamp{%T %Z}"),
                                           (gettext("Date"), "@tstamp{%d %b %Y}")],
                                 formatters={"@tstamp": "datetime"}, mode="mouse"))

    # plot white line to hide small band for no data areas
    if nan_in_data:
        mainplot.line(x='tstamp', y='value', line_width=3, line_color='red', line_cap='round',
                      legend_label=gettext('Missing values'), source=missing_source,
                      # visible=False
                      )
        mainplot.legend.click_policy = "hide"
        mis_list = [*range(0, len(plot_data['missing_data']), 4)]
        for i in mis_list:
            box = BoxAnnotation(left=plot_data['missing_data']['tstamp'][i+1],
                                right=plot_data['missing_data']['tstamp'][i+2],
                                fill_alpha=0.2, fill_color='red')
            mainplot.add_layout(box)

    # plot first average precision to have it in the background
    if plot_data['has_preci']:
        # add errorbars
        mainplot.add_layout(Whisker(source=error_source, base="date", upper="upper", lower="lower",
                                    line_width=0.5))

    # Style plot
    mainplot.title.text_font_size = "14pt"
    mainplot.xaxis.axis_label_text_font_size = "14pt"
    mainplot.xaxis.formatter = DatetimeTickFormatter(days=["%d %b %Y"], months=["%d %b %Y"], years=["%d %b %Y"])
    mainplot.yaxis.axis_label_text_font_size = "14pt"
    script, div = components(column(mainplot, sizing_mode="scale_both"), wrap_script=False)
    return {'script': script, 'div': div}


def get_bokeh_standard(plot_data: object, size: list, label: str = "") -> object:
    """

    :param plot_data: pandas dataframe to plot
    :param size:
    :param label:
    :return:
    """
    # plot_data = fill_data_gaps(db_data)

    stepsize = plot_data['stepsize']
    has_precision = plot_data['has_precision']
    nan_in_data = plot_data['nan_in_data']
    source = ColumnDataSource(plot_data['df'])
    error_source = ColumnDataSource(plot_data['error_source'])
    # missing_source = ColumnDataSource(plot_data['missing_data'])

    # Plot average as main plot
    mainplot = figure(title='Daily average, min and max values', x_axis_label='Time', x_axis_type="datetime",
                      y_axis_label=label,
                      plot_width=size[0], plot_height=int(size[1] * 0.9), toolbar_location="above",
                      tools="pan,wheel_zoom,box_zoom,reset, save", active_drag="box_zoom")

    # plot average line
    mainplot.line(x='date', y='y', source=source, line_width=2, legend_label="average", level="overlay")

    # TODO: Figure out how to use 'source' for multi_line.
    #  Maybe use Glyph? (https://docs.bokeh.org/en/latest/docs/reference/models/glyphs/multi_line.html)
    #  Glyphs maybe also helpful for hover_tool on multiline?
    mainplot.add_tools(HoverTool(tooltips=[("value", "@y"), ("Date", "@date{%d %b %Y}")],
                                 formatters={"@date": "datetime"}, mode="mouse"))

    # plot min/max as multiline and fill area with band
    mainplot.multi_line(xs=[plot_data['source']['date'], plot_data['source']['date']],
                        ys=[plot_data['source']['ymin'], plot_data['source']['ymax']],
                        level='underlay',
                        color=['lightblue', 'lightblue'], legend_label="min & max values")
    mainplot.add_layout(Band(base='date', lower='ymin', upper='ymax', source=source, level='underlay',
                             fill_color='lightblue', fill_alpha=0.5))

    # plot white line to hide small band for no data areas
    if nan_in_data:
        mainplot.line(x='tstamp', y='value', source=source,
                      line_width=2, line_color='white', line_cap='round')

    # plot first average precision to have it in the background
    if has_precision:
        # add errorbars
        mainplot.add_layout(Whisker(source=error_source, base="date", upper="upper", lower="lower",
                                    line_width=0.5))
        mainplot.vbar(x='date', width=1000 * 60 * 59 * 24, top='upper_avg', bottom='lower_avg', source=error_source,
                      fill_color="darksalmon", line_color="black", fill_alpha=0.3, line_width=0.5,
                      legend_label="Average precision")

    # plot bars for the number of values in each group as secondary 'by'plot
    mapper = linear_cmap(field_name='count', palette=Oranges9, low=0, high=plot_data['axis']['y2max'])
    bin_width = stepsize
    distriplot = distribution_plot(source, mapper, bin_width, 'Number of available values per day', size[0])
    distriplot.x_range = mainplot.x_range

    # Style plot
    mainplot.title.text_font_size = "14pt"
    mainplot.xaxis.axis_label_text_font_size = "14pt"
    mainplot.xaxis.formatter = DatetimeTickFormatter(days=["%d %b %Y"], months=["%d %b %Y"], years=["%d %b %Y"])
    mainplot.yaxis.axis_label_text_font_size = "14pt"
    mainplot.legend.click_policy = "hide"
    script, div = components(column(distriplot, mainplot, sizing_mode="scale_both"), wrap_script=False)
    return {'script': script, 'div': div}


def direction_plot(dataframe: object, ti: str) -> object:
    """

    :param dataframe: pandas dataframe
    :param ti: string defining 'week', 'month'...
    :return:
    """
    # use data in percent => transform db_data to percent
    df = (dataframe.transpose().iloc[2:, 0:] / dataframe['sum']) * 100
    df.columns = dataframe['tstamp']

    db_datadictstr = {str(int(time.mktime(item.timetuple()) * 1000)): list(df[item]) for item in df.columns}

    maxlist = df.max(1)
    hist = df.mean(1)

    # maxhist = sorted(maxlist)[-3]
    maxhist = mean(maxlist) * 0.8  # don't use real max of dataset, too many discordant values
    sumhist = sum(hist)
    start = [-radians((i * 10) - 85) for i in list(range(0, 36))]
    end = [-radians((i * 10) - 75) for i in list(range(0, 36))]
    pdstart = [-radians((i * 10) - 95) for i in list(range(0, 36))]
    pdend = start
    # pdend = [-radians((i * 10) - 85) for i in list(range(0, 36))]
    labeltext = ("Selection of " + ti + "ly histograms")
    titletext = (ti + 'ly median and sum of all histograms').capitalize()

    # need two different sources for callback in Bokeh
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

    # plot bars for the number of values in each group as secondary 'by' plot
    mapper = linear_cmap(field_name='count', palette=Oranges9, low=0, high=max(dataframe['sum']))
    bin_width = df.columns[0]-df.columns[1]

    source = ColumnDataSource({'date': dataframe['tstamp'], 'count': dataframe['sum']})
    distriplot = distribution_plot(source, mapper, bin_width, 'Number of values per cluster', 400)

    script, div = components(column(distriplot, mainplot, slider, rslider), wrap_script=False)
    return {'div': div, 'script': script}


def timeseries_plot(data, size):
    mainplot = xyplot_base_figure(data, size, y_label='value', x_label="Time", x_type="datetime",
                                  type='line', title='Daily average, min and max values')
    script, div = components(mainplot, wrap_script=False)
    return {'script': script, 'div': div}


def xyplot(data, size):
    x_label = data.columns[0]
    y_label = data.columns[1]

    mainplot = xyplot_base_figure(data, size, y_label=y_label, x_label=x_label, x_type="linear", type='scatter', title='')
    mainplot.sizing_mode = 'scale_both'
    script, div = components(mainplot, wrap_script=False)
    return {'script': script, 'div': div}


def xyplot_base_figure(data, size, y_label='value', x_label="x axis", x_type="linear", type="line",
                       title='Daily average, min and max values'):
    """
    Create the base xy plot used to add specific information.

    :param data: pandas dataframe
    :param size: size of plot in px
    :param y_label: string
    :param x_label: string
    :param x_type: linear, log, datetime or mercator
    :param type: yet implemented is line and scatter
    :param title: string with name of plot
    :return: bokeh figure
    """
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
    :return: bokeh figure object
    """
    p = figure(title=title, x_axis_type="datetime",  # x_range=mainplot.x_range,
               # plot_width=plot_width,
               plot_height=50, toolbar_location="above", background_fill_color="black",
               tools="pan,wheel_zoom,box_zoom,reset", active_drag="box_zoom", sizing_mode='stretch_width')
    p.vbar(x='date', source=source, width=bin_width, bottom=0, top=1, color=mapper)
    p.xaxis.visible = False
    p.xgrid.visible = False
    p.yaxis.visible = False
    p.ygrid.visible = False
    p.add_tools(HoverTool(tooltips=[("Values/Day", "@count"), ("Date", "@date{%d %b %Y}")],
                          formatters={"@date": "datetime"}, mode="mouse"))
    return p


def get_cache(cache_obj: dict) -> tuple:
    """
    Check if redis is used to cache images, and if image 'name' is cached.
    Return state of redis, if image in cache and image if it is in cache.

    :param name:
    :return: returns two values. First cache object, second Bokeh image as dict of 'script' and 'div'
    """
    img = None
    try:
        img = cache_obj['redis'].get(cache_obj['name'])
    except:
        cache_obj['use_redis'] = False

    if cache_obj['use_redis']:
        if img is None:
            cache_obj['in_cache'] = False
        else:
            img = str(img, 'utf-8')
            cache_obj['in_cache'] = True
    return cache_obj, img


def get_plot_from_db_id(ID: str, full_res: bool, date: list, size: list = [700, 500]) -> dict:
    """
    Check if plot is stored with redis or build a new one with Bokeh.
    Bokeh builds an object with 'script' and 'div'. Redis stores this as string, which is fine, as
    the data is send to the website as string anyways.

    :param ID: Entry id in metacatalog
    :param full_res: Boolean to set if plot should be of full dataset
    :param date:
    :param size:
    :return: Bokeh image consisting of 'script' and 'div'
    """
    cache_obj = {'use_redis': True, 'redis': redis.StrictRedis(),
                 'in_cache': False, 'name': "plot_{}".format('b' + str(ID) + str(size) + str(date))}
    cache_obj, img = get_cache(cache_obj)

    if not cache_obj['in_cache']:
        label = __DB_load_label(ID)
        if label.find('direction') != -1:
            ti = 'week'  # time interval used to plot, choose 'year', 'month', 'week' or 'day'
            db_data, ti = __DB_load_directiondata(ID, ti, date, full_res)
            # plot_data = fill_data_gaps(db_data)
            img = direction_plot(db_data, ti)
        else:
        #             db_data = __DB_load_data_avg(id)
        #             db_data = __get_axis_limits(db_data)
        #             img = get_bokeh_standard(db_data, size, label)
        # get data
            db_data = __DB_load_data(ID, date, full_res)
            if db_data['has_preci']:
                db_data['df'] = precision_to_minmax(db_data['df'])
            plot_data = fill_data_gaps(db_data)
            # prepare plot
            plot_data = __get_axis_limits(plot_data)
            img = get_bokeh_std_fullres(plot_data=plot_data, full_res=full_res, size=size, label=label)

        if cache_obj['use_redis']:
            cache_obj['redis'].set("plot_{}".format(cache_obj['name']), str(img))

    return img

#
# def get_preview(id: str, date: list, size=[700, 500]):
#     """
#     Check which is the source for the dataset and if a preview image is already cached. Return html of a plot.
#
#     :param id: id of a dataset. Integers or dbXX for DB as source, wpsXX for wps result.
#     :param size: size of resulting plot [width, height]
#     :type date: list
#     :type size: list
#     :return: html ready to render
#     """
#     # id = 2657 # small test dataset
#     try:
#         wps_result = True if 'wps' in id[0:3] else False
#     except:
#         wps_result = False
#
#     imgname = "preview_{}".format('b' + str(id) + str(size) + str(date))
#     cache_obj = {'use_redis': True, 'redis': redis.StrictRedis(),
#                  'in_cache': False, 'name': imgname}
#     cache_obj, img = get_cache(cache_obj)
#
#     if not cache_obj['in_cache'] and not wps_result:
#         label = __DB_load_label(id)
#         if label.find('direction') != -1:
#             ti = 'week'  # time interval used to plot, choose 'year', 'month', 'week' or 'day'
#             db_data = __DB_load_directiondata(id, ti)
#             plot_data = fill_data_gaps(db_data)
#             # img = get_bokeh_standard(db_data, label)
#             img = direction_plot(plot_data, ti)
#         else:
#             db_data = __DB_load_data_avg(id)
#             db_data = __get_axis_limits(db_data)
#             img = get_bokeh_standard(db_data, size, label)
#
#         if cache_obj['use_redis']:
#             r = cache_obj['redis']
#             r.set(imgname, img)
#
#     if wps_result:
#         DBstring = ast.literal_eval(WpsResults.objects.get(id=id[3:]).outputs)
#         try:
#             if 'pickle' in DBstring[1]:
#                 df = pd.read_pickle(DBstring[2])
#                 if 'ts-pickle' in DBstring[1]:
#                     img = timeseries_plot(df, size)
#                 elif DBstring[1] == 'pickle':
#                     img = xyplot(df, size)
#             elif DBstring[1] == 'image':
#                 try:
#                     file = open(DBstring[2], mode='r')
#                     htmlimg = file.read()
#                     file.close()
#                 except FileNotFoundError:
#                     print('Error: Can not load your image')
#                     htmlimg = 'Error: Can not load your image'
#                 img = {'html': htmlimg}
#             else:
#                 print('Error: Con not plot. Unknown type')
#
#         except FileNotFoundError:
#             print('The data file %s was not found.' % (DBstring[2]))
#
#     return img
