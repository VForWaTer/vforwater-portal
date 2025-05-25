import time

import numpy as np
from bokeh.models import HoverTool, DatetimeTickFormatter, ColumnDataSource, BoxAnnotation, Whisker, \
    CustomJS, Range1d, LogColorMapper, ColorBar, DateSlider, \
    DateRangeSlider
from bokeh.palettes import Oranges9, viridis
from bokeh.plotting import figure
from bokeh.transform import linear_cmap
from bridget.eddy import footprint
from django.utils.translation import gettext
from numpy import mean
from math import radians, ceil, sqrt

import logging

logger = logging.getLogger(__name__)

class PlotObject:
    """
    Class calculates parameters accroding the parameters.
    """

    def __init__(self, data=None, mainplot=None, style=None):
        self.dataObj = data
        self.source = ColumnDataSource(self.dataObj.dataframe)
        self.y_col = data.value_column

        self.dbinput = None
        self.wpsinput = None
        self.mainplot = mainplot
        self.x_axis_type = None
        self.x_axis_label = "TODO: Find a proper label in your Data!"
        self.script = None
        self.div = None
        self.get_plot = None
        self.xs = []
        self.ys = []
        self.colormap = None
        if style:
            self.style = style
        else:
            self.style = {'linecolor': 'blue'}

    def get_mainplot(self):
        return self.mainplot

    def __add_line__(self):
        try:
            # plot value line
            self.x_col = 'tstamp'
            self.mainplot.line(x=self.x_col, y=self.y_col, source=self.source,
                               line_width=3, line_color=self.style['linecolor'],
                               legend_label=self.y_col.replace('_', ' '))
        except Exception as e:
            print(f'Exception in plot_obj.PlotObject.__add_line__(): {e}')
            logger.debug(f'Cannot add line to fig object, {e}')

    def __add_multiple_lines__(self):
        # plot value line
        self.mainplot.line(x=self.dataObj.dataframe[self.x_col],
                           y=self.dataObj.dataframe[self.y_col],
                           line_width=3, line_color=self.style['linecolor'],
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
            box = BoxAnnotation(left=self.dataObj.missing_data[self.x_col][i + 1].timestamp()*1000,
                                right=self.dataObj.missing_data[self.x_col][i + 2].timestamp()*1000,
                                fill_alpha=0.1, fill_color='red')  # , top=80)
            self.mainplot.add_layout(box)

    def __show_precision__(self):
        self.mainplot.add_layout(Whisker(source=self.source, base="tstamp", upper="upper", lower="lower",
                                         line_width=0.5))

    def __set_colormap__(self):
        self.colormap = viridis(len(self.dataObj.data_names))


class XYTimeseriesPlot(PlotObject):

    def __init__(self, data, mainplot, style):
        super().__init__(data, mainplot, style)
        self.x_col = 'tstamp'
        self.create_plot()

    def create_plot(self):

        self.__datetime_xaxis__()
        if self.dataObj.multiple_lines:
            self.__set_colormap__()
            for i, col_name in enumerate(self.dataObj.data_names):
                self.style['linecolor'] = self.colormap[i]
                self.y_col = col_name
                self.__add_multiple_lines__()
        else:
            self.__datetime_hovertool__()
            if self.dataObj.has_nan:
                self.__show_nan__()

            if self.dataObj.has_precision:
                self.__show_precision__()

            self.__add_line__()

        self.mainplot.legend.click_policy = "hide"

    def __datetime_hovertool__(self):
        value = '@'+self.y_col
        self.mainplot.add_tools(HoverTool(tooltips=[(gettext("Value"), value),
                                                    (gettext("Time"), "@tstamp{%T %Z}"),
                                                    (gettext("Date"), "@tstamp{%d %b %Y}")],
                                          formatters={"@tstamp": "datetime"}, mode="mouse"))

    def __datetime_xaxis__(self):
        self.mainplot.xaxis.formatter = DatetimeTickFormatter(days="%d %b %Y", months="%d %b %Y",
                                                              years="%d %b %Y")


class DirectionPlot(PlotObject):

    def __init__(self, data, mainplot):
        super().__init__(data, mainplot)
        self.__prepare_plot_data__()
        self.create_plot()

    def create_plot(self):
        self.labeltext = ("Selection of " + self.dataObj.timestep_label + "ly histograms")
        self.__get_direction_plot__()
        self.__prepare_main_plot__()
        self.__create_slider__()
        self.__create_range_slider__()
        self.__create_distribution_plot__()

    def __prepare_main_plot__(self):
        # create grid
        rund_perc = ceil(self.maxhist / self.sumhist * 100)
        labels = list(range(0, rund_perc, 2))
        labels.append(rund_perc)
        rad_pos = [i * self.sumhist / 100 for i in labels]
        out_rim = rad_pos[-1]
        label_pos = [sqrt(((i - 1) ** 2) / 2) for i in rad_pos]
        self.mainplot.text(label_pos[1:], label_pos[1:], [str(r) + ' %' for r in labels[1:]],
                           text_font_size="10pt", text_align="left", text_baseline="top")
        for rad in rad_pos:
            self.mainplot.circle(x=0, y=0, radius=rad, fill_color=None, line_color='grey', line_width=0.5,
                                 line_alpha=0.8)
        diagonal = sqrt((out_rim ** 2) / 2)
        self.mainplot.multi_line(xs=[[diagonal, -diagonal], [-diagonal, diagonal], [-out_rim, out_rim], [0, 0]],
                                 ys=[[diagonal, -diagonal], [diagonal, -diagonal], [0, 0], [-out_rim, out_rim]],
                                 line_color="grey", line_width=0.5, line_alpha=0.8)
        self.mainplot.x_range = Range1d(-out_rim * 1.1, out_rim * 1.1)
        self.mainplot.y_range = Range1d(-out_rim * 1.1, out_rim * 1.1)
        self.mainplot.legend.location = "top_left"
        self.mainplot.legend.click_policy = "hide"

    def __prepare_plot_data__(self):
        # use data in percent => transform db_data to percent
        self.df = (self.dataObj.dataframe.transpose().iloc[2:, 0:] / self.dataObj.dataframe['sum']) * 100
        self.df.columns = self.dataObj.dataframe['tstamp']
        db_datadictstr = {
            str(int(time.mktime(item.timetuple()) * 1000)): list(self.df[item]) for item in self.df.columns
        }

        self.hist = self.df.mean(1)

        self.maxhist = mean(self.df.max(1)) * 0.8  # don't use real max of dataset, too many discordant values
        self.sumhist = sum(self.hist)
        self.start = [-radians((i * 10) - 85) for i in list(range(0, 36))]
        self.end = [-radians((i * 10) - 75) for i in list(range(0, 36))]

        pdstart = [-radians((i * 10) - 95) for i in list(range(0, 36))]
        pdend = self.start

        # need two different sources for callback in Bokeh
        self.pdsource = ColumnDataSource(data=dict(radius=self.hist, start=pdstart, end=pdend))
        self.jssource = ColumnDataSource(data=db_datadictstr)

        day = 1  # 1000 * 3600 * 24 #  Bokeh 3 uses stepsize in days
        self.stepsize = day
        if self.dataObj.timestep_label == 'week':
            self.stepsize = day * 7
        elif self.dataObj.timestep_label == 'month':
            self.stepsize = 30 * day
        elif self.dataObj.timestep_label == 'year':
            self.stepsize = 365 * day

    def __create_slider__(self):
        self.slider = DateSlider(start=min(self.df.columns), end=max(self.df.columns), value=min(self.df.columns),
                            step=self.stepsize, title="date within histogram")
        callback = CustomJS(
            args=dict(source=self.pdsource, data=self.jssource, slid=self.slider), code="""
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
        self.slider.js_on_change('value', callback)

    def __create_range_slider__(self):
        # create range slider
        self.rslider = DateRangeSlider(start=min(self.df.columns), end=max(self.df.columns),
                                  value=(min(self.df.columns), max(self.df.columns)),
                                  step=self.stepsize, title="Data within date range from ")
        rcallback = CustomJS(
            args=dict(source=self.pdsource, data=self.jssource, rslid=self.rslider), code="""
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
        self.rslider.js_on_change('value', rcallback)

    def __get_direction_plot__(self):

        # simple rose plot
        self.mainplot.wedge(radius=self.hist, start_angle=self.start, end_angle=self.end, x=0, y=0, direction='clock',
                            line_color='blue', fill_color='lightblue', alpha=0.5, legend_label='Whole dataset')
        # plot connected with slider
        self.mainplot.wedge(radius='radius', start_angle='start', end_angle='end', source=self.pdsource, x=0, y=0,
                            alpha=0.5, direction='clock', line_color='darkred', fill_color='lightsalmon',
                            legend_label=self.labeltext)

    def __create_distribution_plot__(self):
        # plot bars for the number of values in each group as secondary 'by' plot
        mapper = linear_cmap(field_name='count', palette=Oranges9, low=0, high=max(self.dataObj.dataframe['sum']))
        bin_width = self.df.columns[0] - self.df.columns[1]

        source = ColumnDataSource({'date': self.dataObj.dataframe['tstamp'], 'count': self.dataObj.dataframe['sum']})
        self.distriplot = distribution_plot(source, mapper, bin_width, 'Number of values per cluster', 400)

    def get_distribution_plot(self):
        return self.distriplot

    def get_slider(self):
        return self.slider

    def get_rangeslider(self):
        return self.rslider


class EddyFootPrintPlot(PlotObject):

    def __init__(self, data, mainplot):
        super().__init__(data, mainplot)

    def __create_eddy_footprint__(self):

        df_db = self.dataObj.dataframe[['tstamp', 'air_pressure', 'Var(Ts)[deg C]', 'Var(a)[g/m3]', 'Var(u)[m/s]',
                                        "Cov(u'w')[m2/s2]", "Cov(v'w')[m2/s2]", "Cov(w'Ts')[(m*deg C)/s]",
                                        'Var(v)[m/s]', 'wind_direction']]
        # remove rows when there is a nan value (which cannot be plotted as footprint)
        df_db = df_db.dropna()
        df_bla = df_db.reset_index(drop=True)
        grid = 500
        tstamp = 5

        def get_footprint(tstamp):
            try:
                return footprint(dt_index=df_db.tstamp.dt.strftime('%m.%d.%Y %H:%M'),
                                 t_air=df_db['Var(Ts)[deg C]'], a=df_db['Var(a)[g/m3]'],
                                 p=df_db['air_pressure'], u=df_db['Var(u)[m/s]'],
                                 cov_uw=df_db["Cov(u'w')[m2/s2]"],
                                 cov_vw=df_db["Cov(v'w')[m2/s2]"],
                                 cov_wt=df_db["Cov(w'Ts')[(m*deg C)/s]"],
                                 var_v=df_db['Var(v)[m/s]'],
                                 direction=df_db['wind_direction'], tstamp=tstamp, grid=grid)
            except Exception as e:
                print('Error in eddy footprint Function: ', e)
                logger.debug(f'Error while trying to get eddy footprint, {e}')
                pass

        all_fp = np.empty(len(df_db), dtype=object)
        all_fp_norm = np.empty(len(df_db), dtype=object)
        i_list = np.empty(len(df_db))
        all_FP_north = all_FP_east = False
        loop_len = range(df_db.shape[0])

        # loop v1 is etwas langsamer 7.625 vs 7,619
        for i in loop_len:
            single_fp, FP_east, FP_north, single_fp_norm = get_footprint(i)
            single_fp[single_fp == 0] = np.nan
            all_fp[i] = single_fp
            all_fp_norm[i] = single_fp_norm
        all_fp = np.empty(len(df_db), dtype=object)
        all_fp_norm = np.empty(len(df_db), dtype=object)
        i_list = np.empty(len(df_db))
        all_FP_north = all_FP_east = False
        for i, row in enumerate(df_db.itertuples()):
            i_list[i] = i
            single_fp, FP_east, FP_north, single_fp_norm = get_footprint(row.Index)
            single_fp[single_fp == 0] = np.nan
            all_fp[i] = single_fp
            all_fp_norm[i] = single_fp_norm

        x_min = FP_east.min()
        x_max = FP_east.max()
        y_min = FP_north.min()
        y_max = FP_north.max()

        try:
            jssource = ColumnDataSource(data=dict(fp=[all_fp],  # fp_norm=all_fp_norm,
                                                  x=[x_min], y=[y_min],
                                                  dw=[np.abs(x_min) + x_max], dh=[np.abs(y_min) + y_max],
                                                  ))
        except Exception as e:
            print('Error in eddy ColumnDataSource creation: ', e)
            logger.debug(f'Error in eddy ColumnDataSource creation, {e}')
        norm = get_footprint(tstamp)
        self.mainplot = figure(title="Eddy footprint preview",
                               x_range=(x_min, x_max), y_range=(y_min, y_max))
        legend_text = df_db.tstamp[tstamp].strftime('%m.%d.%Y\n%H:%M')

        all_fp_min = min(map(np.nanmin, all_fp))
        all_fp_max = max(map(np.nanmax, all_fp))

        # add a color bar
        color_mapper = LogColorMapper(palette="Viridis256", low=all_fp_min, high=all_fp_max,
                                      nan_color='whitesmoke')
        color_bar = ColorBar(color_mapper=color_mapper, label_standoff=12, major_label_text_font_size='16px')
        self.mainplot.add_layout(color_bar, 'right')

        # create image of footprint
        try:
            self.mainplot.image(image='fp', x='x', y='y', dw='dw', dh='dh', source=jssource,
                                color_mapper=color_mapper, legend_label=legend_text
                                )
            self.mainplot.image(image=[single_fp],
                                x=[FP_east.min()], y=[FP_north.min()],
                                dw=[np.abs(FP_east.max()) + FP_east.max()],
                                dh=[np.abs(FP_north.max()) + FP_north.max()],
                                color_mapper=color_mapper, legend_label=legend_text
                                )

        except Exception as e:
            print('Error while trying to create an image for eddy data: ', e)
            logger.debug(f'Error while trying to create an image for eddy data: {e}')

        self.__style_eddy_plot__()
        self.__create_plot__()

    def __style_eddy_plot__(self):
        self.mainplot.legend.click_policy = "hide"
        self.mainplot.grid.grid_line_width = 0.5

        self.mainplot.add_tools(HoverTool(tooltips=[(gettext("fp"), "@image"),
                                                    (gettext("FP east"), "$x"),
                                                    (gettext("FP north"), "$y")],
                                          mode="mouse"))


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
               # width=plot_width,
               height=50, toolbar_location="above", background_fill_color="black",
               tools="pan,wheel_zoom,box_zoom,reset", active_drag="box_zoom", sizing_mode='stretch_width')
    p.vbar(x='date', source=source, width=bin_width, bottom=0, top=1, color=mapper)
    p.xaxis.visible = False
    p.xgrid.visible = False
    p.yaxis.visible = False
    p.ygrid.visible = False
    p.add_tools(HoverTool(tooltips=[("Values/Day", "@count"), ("Date", "@date{%d %b %Y}")],
                          formatters={"@date": "datetime"}, mode="mouse"))
    return p
