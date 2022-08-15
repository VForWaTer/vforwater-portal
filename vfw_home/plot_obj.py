import time

from bokeh.embed import components
from bokeh.layouts import column
from bokeh.models import HoverTool, DatetimeTickFormatter, ColumnDataSource, BoxAnnotation, Whisker, DateRangeSlider, \
    DateSlider, CustomJS, Range1d
from bokeh.palettes import Oranges9, viridis
from bokeh.plotting import figure
from bokeh.transform import linear_cmap
from django.utils.translation import gettext
from numpy import mean
from math import radians, ceil, sqrt

from heron.settings import max_size_preview_plot
from vfw_home.previewplot import distribution_plot


class PlotObject:
    """
    Class calculates parameters accroding the parameters.
    """

    def __init__(self, data=None, plot_size=[700, 500]):
        self.dataObj = data
        self.source = ColumnDataSource(self.dataObj.dataframe)
        self.y_col = data.value_column
        self.plot_size = plot_size

        self.dbinput = None
        self.wpsinput = None
        self.title = ""
        self.mainplot = None
        self.x_axis_type = None
        self.x_axis_label = "TODO: Find a proper label in your Data!"
        self.script = None
        self.div = None
        self.get_plot = None
        self.xs = []
        self.ys = []
        self.colormap = None
        self.linecolor = 'blue'

        self.__set_values__()

    def __set_values__(self):

        if self.dataObj.full:
            self.title = ''
        else:
            self.title = gettext("Showing only latest {0} datapoints.").format(str(max_size_preview_plot))

        if self.dataObj.label.lower().find('direction') != -1:
            print('its a direction plot ___________________')
            self.__get_direction_plot__()
        elif self.dataObj.label.lower().find('eddy covariance') != -1:
            print('its an eddy covariance plot ___________________')
        elif self.dataObj.data_table_name == ['evapotranspiration']:
            # 1D timeseries plot
            print('its an evapotranspiration (1d timeseries) plot ___________________')
            self.__create_standard_timeseries__()
        elif self.dataObj.data_table_name == ['u', 'v', 'w']:
            print('we need a 3d plot ___________________')
        elif self.dataObj.label.lower().find('windspeed') != -1:
            print('we need a wind SPEED!! plot _________________')
        elif self.dataObj.data_format == '3D':
            print('we need a 3D plot ________________-')
        elif self.dataObj.data_table_name.lower().find('timeseries') != -1:
            print('its a 1d timeseries plot ___________________')

            self.__create_standard_timeseries__()

        else:
            print('we need a standard plot!_______________')

        self.get_plot = {'script': self.script, 'div': self.div}

    def __create_standard_timeseries__(self):
        self.x_axis_type = "datetime"  # use "mercator" for geodata!
        self.x_axis_label = "Time"
        self.x_col = 'tstamp'
        self.__set_mainplot__()

        if self.dataObj.multiple_lines:
            # self.__prepare_multiline_data__()
            self.__set_colormap__()
            for i, col_name in enumerate(self.dataObj.data_names):
                self.linecolor = self.colormap[i]
                self.y_col = col_name
                self.__add_multiple_lines__()
            # self.__add_multiline__()
        else:
            self.__datetime_hovertool__()
            if self.dataObj.has_nan:
                self.__show_nan__()

            if self.dataObj.has_precision:
                self.__show_precision__()

            self.__add_line__()

        self.mainplot.legend.click_policy = "hide"
        self.__datetime_xaxis__()
        self.__style_plot__()
        self.__create_plot__()

    def __set_mainplot__(self):
        self.mainplot = figure(x_axis_label=self.x_axis_label, x_axis_type=self.x_axis_type,
                               y_axis_label=self.dataObj.label,
                               title=self.title,
                               # sizing_mode='stretch_both',
                               plot_width=self.plot_size[0], plot_height=int(self.plot_size[1] * 0.9),
                               toolbar_location="above", tools="pan,wheel_zoom,box_zoom,reset, save",
                               active_drag="box_zoom")

    def __add_line__(self):
        # plot value line
        self.mainplot.line(x=self.x_col, y=self.y_col, source=self.source,
                           line_width=3, line_color=self.linecolor,
                           legend_label=self.y_col.replace('_', ' '))
    def __add_multiple_lines__(self):
        # plot value line
        self.mainplot.line(x=self.dataObj.dataframe[self.x_col],
                           y=self.dataObj.dataframe[self.y_col],
                           line_width=3, line_color=self.linecolor,
                           legend_label=self.y_col.replace('_', ' '))

    def __add_multiline__(self):
        # plot value line
        self.mainplot.multi_line(xs=self.xs, ys=self.ys, line_width=3, line_color=self.colormap)

    def __prepare_multiline_data__(self):

        for i in self.dataObj.data_names:
            self.ys.append(self.dataObj.dataframe[i])
            self.xs.append(self.dataObj.dataframe[self.x_col])

    def __show_nan__(self):
        self.mainplot.line(x=self.x_col, y=self.y_col, line_width=3, line_color='red', line_cap='round',
                           legend_label=gettext('Missing values'), source=ColumnDataSource(self.dataObj.missing_data),
                           # visible=False
                           )
        mis_list = [*range(0, len(self.dataObj.missing_data), 4)]
        for i in mis_list:
            box = BoxAnnotation(left=self.dataObj.missing_data[self.x_col][i + 1],
                                right=self.dataObj.missing_data[self.x_col][i + 2],
                                fill_alpha=0.2, fill_color='red')
            self.mainplot.add_layout(box)

    def __show_precision__(self):
        self.mainplot.add_layout(Whisker(source=self.source, base="tstamp", upper="upper", lower="lower",
                                         line_width=0.5))

    def __datetime_hovertool__(self):
        value = '@'+self.y_col
        self.mainplot.add_tools(HoverTool(tooltips=[(gettext("Value"), value),
                                                    (gettext("Time"), "@tstamp{%T %Z}"),
                                                    (gettext("Date"), "@tstamp{%d %b %Y}")],
                                          formatters={"@tstamp": "datetime"}, mode="mouse"))

    def __datetime_xaxis__(self):
        self.mainplot.xaxis.formatter = DatetimeTickFormatter(days=["%d %b %Y"], months=["%d %b %Y"],
                                                              years=["%d %b %Y"])

    def __style_plot__(self):
        self.mainplot.title.text_font_size = "14pt"
        self.mainplot.xaxis.axis_label_text_font_size = "14pt"
        self.mainplot.yaxis.axis_label_text_font_size = "14pt"
        # self.mainplot.BoxAnnotation(top=80, fill_alpha=0.1, fill_color='red')

    def __create_plot__(self):
        self.script, self.div = components(column(self.mainplot, sizing_mode="scale_both"), wrap_script=False)

    def __get_direction_plot__(self):
        # use data in percent => transform db_data to percent
        df = (self.dataObj.dataframe.transpose().iloc[2:, 0:] / self.dataObj.dataframe['sum']) * 100
        df.columns = self.dataObj.dataframe['tstamp']
        db_datadictstr = {str(int(time.mktime(item.timetuple()) * 1000)): list(df[item]) for item in df.columns}

        maxlist = df.max(1)
        hist = df.mean(1)

        # maxhist = sorted(maxlist)[-3]
        maxhist = mean(maxlist) * 0.8  # don't use real max of dataset, too many discordant values
        sumhist = sum(hist)
        # start = list(map(lambda i: -radians((i * 10) - 85), range(0, 36)))
        start = [-radians((i * 10) - 85) for i in list(range(0, 36))]
        end = [-radians((i * 10) - 75) for i in list(range(0, 36))]
        pdstart = [-radians((i * 10) - 95) for i in list(range(0, 36))]
        pdend = start
        # pdend = [-radians((i * 10) - 85) for i in list(range(0, 36))]
        labeltext = ("Selection of " + self.dataObj.timestep_label + "ly histograms")
        titletext = (self.dataObj.timestep_label + 'ly median and sum of all histograms').capitalize()

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
        if self.dataObj.timestep_label == 'week':
            stepsize = day
        elif self.dataObj.timestep_label == 'month':
            stepsize = 7 * day
        elif self.dataObj.timestep_label == 'year':
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
        mapper = linear_cmap(field_name='count', palette=Oranges9, low=0, high=max(self.dataObj.dataframe['sum']))
        bin_width = df.columns[0] - df.columns[1]

        source = ColumnDataSource({'date': self.dataObj.dataframe['tstamp'], 'count': self.dataObj.dataframe['sum']})
        distriplot = distribution_plot(source, mapper, bin_width, 'Number of values per cluster', 400)

        self.script, self.div = components(column(distriplot, mainplot, slider, rslider), wrap_script=False)

    def __set_colormap__(self):
        # self.colormap = brewer['Viridis'][len(self.dataObj.data_names)]
        self.colormap = viridis(len(self.dataObj.data_names))
