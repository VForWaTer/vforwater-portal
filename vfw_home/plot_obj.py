from bokeh.embed import components
from bokeh.layouts import column
from bokeh.models import HoverTool, DatetimeTickFormatter, ColumnDataSource, BoxAnnotation, Whisker
from bokeh.plotting import figure
from django.utils.translation import gettext

from heron.settings import max_size_preview_plot


class PlotObject:
    """
    Class calculates parameters accroding the parameters.
    """

    def __init__(self, data=None, plot_size=[700, 500]):
        self.dataObj = data
        self.source = ColumnDataSource(self.dataObj.dataframe)
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

        self.__set_values__()

    def __set_values__(self):

        if self.dataObj.full:
            self.title = ''
        else:
            self.title = gettext("Showing only latest {0} datapoints.").format(str(max_size_preview_plot))

        if self.dataObj.label.find('direction') != -1:
            print('we need a direction plot ____________________')
        elif self.dataObj.label.find('windspeed') != -1:
            print('we need a wind SPEED!! plot _________________')
        elif self.dataObj.data_format == '3D':
            print('we need a 3D plot ________________-')
        elif self.dataObj.data_table_name.find('timeseries') != -1:
            self.x_axis_type = "datetime"  # use "mercator" for geodata!
            self.x_axis_label = "Time"
            self.x_col = 'tstamp'
            self.y_col = 'value'

            self.__set_mainplot__()
            self.__add_data__()
            self.__add_timeseries_specifics__()
            self.__style_plot__()
            if self.dataObj.has_nan:
                self.__show_nan__()

            if self.dataObj.has_precision:
                self.__show_precision__()
        else:
            print('we need a standard plot!_______________')

        self.__create_plot__()
        self.get_plot = {'script': self.script, 'div': self.div}

    def __set_mainplot__(self):
        self.mainplot = figure(x_axis_label=self.x_axis_label, x_axis_type=self.x_axis_type,
                               y_axis_label=self.dataObj.label,
                               title=self.title,
                               # sizing_mode='stretch_both',
                               plot_width=self.plot_size[0], plot_height=int(self.plot_size[1] * 0.9),
                               toolbar_location="above", tools="pan,wheel_zoom,box_zoom,reset, save",
                               active_drag="box_zoom")

    def __add_data__(self):
        # plot value line
        self.mainplot.line(x=self.x_col, y=self.y_col, source=self.source,
                           line_width=3)  # , legend_label="measured values")

    def __show_nan__(self):
        self.mainplot.line(x=self.x_col, y=self.y_col, line_width=3, line_color='red', line_cap='round',
                           legend_label=gettext('Missing values'), source=ColumnDataSource(self.dataObj.missing_data),
                           # visible=False
                           )
        self.mainplot.legend.click_policy = "hide"
        mis_list = [*range(0, len(self.dataObj.missing_data), 4)]
        for i in mis_list:
            box = BoxAnnotation(left=self.dataObj.missing_data[self.x_col][i + 1],
                                right=self.dataObj.missing_data[self.x_col][i + 2],
                                fill_alpha=0.2, fill_color='red')
            self.mainplot.add_layout(box)

    def __show_precision__(self):
        self.mainplot.add_layout(Whisker(source=self.source, base="tstamp", upper="upper", lower="lower",
                                         line_width=0.5))

    def __add_timeseries_specifics__(self):

        self.mainplot.add_tools(HoverTool(tooltips=[(gettext("Value"), "@value"),
                                                    (gettext("Time"), "@tstamp{%T %Z}"),
                                                    (gettext("Date"), "@tstamp{%d %b %Y}")],
                                          formatters={"@tstamp": "datetime"}, mode="mouse"))
        self.mainplot.xaxis.formatter = DatetimeTickFormatter(days=["%d %b %Y"], months=["%d %b %Y"], years=["%d %b %Y"])

    def __style_plot__(self):
        self.mainplot.title.text_font_size = "14pt"
        self.mainplot.xaxis.axis_label_text_font_size = "14pt"
        self.mainplot.yaxis.axis_label_text_font_size = "14pt"
        # self.mainplot.BoxAnnotation(top=80, fill_alpha=0.1, fill_color='red')

    def __create_plot__(self):
        self.script, self.div = components(column(self.mainplot, sizing_mode="scale_both"), wrap_script=False)

