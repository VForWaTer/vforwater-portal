from bokeh.embed import components
from bokeh.io import show
from bokeh.layouts import column
from bokeh.palettes import brewer
from bokeh.plotting import figure
from django.utils.translation import gettext
import pandas as pd

from heron.settings import MAX_SIZE_PREVIEW_PLOT
from .plot_obj import XYTimeseriesPlot, DirectionPlot
from .data_obj import DataObject
import logging

logger = logging.getLogger(__name__)

class FigObject:
    def __init__(self, data=None, plot_size=[700, 500]):

        self.data = data
        self.plot_size = plot_size
        self.title = ""
        self.script = None
        self.div = None
        self.x_axis_type = None
        self.x_axis_label = "TODO: Find a proper label in your Data!"
        self.mainplot = None

        self.__set_values__()

    def __set_values__(self):

        def choose_plottype(new_figure=True, style=None):
            try:
                if self.dataObj.full:
                    self.title = ''
                else:
                    self.title = gettext("Showing only latest {0} datapoints.").format(str(MAX_SIZE_PREVIEW_PLOT))

                if self.dataObj.label.lower().find('direction') != -1:
                    self.__get_direction_plot__()
                elif self.dataObj.label.lower().find('eddy covariance') != -1:
                    self.__create_eddy_footprint__
                elif self.dataObj.data_table_name == ['evapotranspiration']:
                    # 1D timeseries plot
                    self.__create_standard_timeseries__()
                elif self.dataObj.data_table_name == ['u', 'v', 'w']:
                    print('we need a 3d plot ___________________')
                elif self.dataObj.label.lower().find('windspeed') != -1:
                    print('we need a wind SPEED!! plot _________________')
                elif self.dataObj.data_format == '3D':
                    print('self.dataObj.data_format: ', self.dataObj.data_format)
                    print('we need a 3D plot ________________-')
                elif self.dataObj.data_table_name.lower().find('timeseries') != -1:
                    self.__plot_timeseries__(new_figure, style)

                else:
                    print('we need a standard plot!_______________')
            except Exception as e:
                print('Fig_obj.FigObject.__set_values__.choose_plottype; Unable to create Figure: ', e)
                logger.debug(f'Unable to create Figure, {e}')

        if isinstance(self.data, list):
            if len(self.data) > 2:
                self.colormap = brewer['Blues'][len(self.data)]
            else:
                self.colormap = ('royalblue', 'blue')
            for count, dataset in enumerate(self.data):
                style = {'linecolor': self.colormap[count]}
                self.dataObj = dataset
                choose_plottype(new_figure=not bool(count), style=style)
        else:
            self.dataObj = self.data
            choose_plottype()

        if not self.script:
            try:
                self.script, self.div = components(column(self.mainplot, sizing_mode="scale_both"), wrap_script=False)
            except Exception as e:
                print(f'Error in Fig_obj.FigObject__set_values__(). Error getting script and div: {e}')
                logger.debug(f'Error getting script and div: {e}')

    def __set_mainplot__(self):
        try:
            self.mainplot = figure(x_axis_label=self.x_axis_label, x_axis_type=self.x_axis_type,
                                   y_axis_label=self.dataObj.label,
                                   title=self.title,
                                   sizing_mode='scale_width',  # sidebar works
                                   # sizing_mode='scale_height',  # wide siebar, tiny map
                                   width=self.plot_size[0], height=int(self.plot_size[1] * 0.9),
                                   toolbar_location="above", tools="pan,wheel_zoom,box_zoom,reset, save",
                                   active_drag="box_zoom")
            self.mainplot.title.text_font_size = "14pt"
            self.mainplot.xaxis.axis_label_text_font_size = "14pt"
            self.mainplot.yaxis.axis_label_text_font_size = "14pt"

        except Exception as e:
            print('Error in Fig Object. Cannot set mainplot: ', e)
            logger.debug(f'Cannot set mainplot, {e}')

    def __plot_timeseries__(self, new_figure, style):
        try:
            if new_figure:
                self.x_axis_type = "datetime"
                self.x_axis_label = "Time"
                self.__set_mainplot__()

            # Assume self.data is a list of DataObjects
            if type(self.data) == DataObject:
                XYTimeseriesPlot(self.dataObj, self.mainplot, style)
            else :
                try:
                    # Combine DataFrames from each DataObject in the list
                    dataframes = [data_obj.dataframe for data_obj in self.data]  # Extract the dataframes
                    combined_dataframe = pd.concat(dataframes, ignore_index=True)
                    # combined_dataframe.sort_values(by='tstamp', ascending=True, inplace=True)
                    combined_dataframe = combined_dataframe.tail(MAX_SIZE_PREVIEW_PLOT)
                    self.dataObj.dataframe = combined_dataframe
                except Exception as e:
                    print(f"Error combining dataframes: {e}")

                try:
                    # Determine the oldest time in the combined data.
                    min_timestamp = combined_dataframe['tstamp'].min()
                    # Ensure there is missing data to process.
                    combined_missing_data = pd.concat(
                        [obj.missing_data for obj in self.data if isinstance(obj.missing_data, pd.DataFrame)],
                        ignore_index=True
                    )
                    filtered_missing_data = combined_missing_data[combined_missing_data['tstamp'] >= min_timestamp]
                    self.dataObj.missing_data = filtered_missing_data
                except Exception as e:
                    print(f"Error processing missing data: {e}")

                try:
                    XYTimeseriesPlot(self.dataObj, self.mainplot, style)
                except Exception as e:
                    print(f"Error plotting time series: {e}")

        except Exception as e:
            print('Error in Fig Object. Cannot create timeseries plot: ', e)
            logger.debug(f'Cannot create timeseries plot, {e}')

    def __get_direction_plot__(self):
        try:
            self.titletext = (self.dataObj.timestep_label + 'ly median and sum of all histograms').capitalize()
            self.mainplot = figure(title=self.titletext, width=400, height=400,
                                   x_axis_type=None, y_axis_type=None, tools="save",
                                   min_border=0, outline_line_color=None)
            self.mainplot.title.text_font_size = "14pt"

            plot = DirectionPlot(self.dataObj, self.mainplot)
            mainplot = plot.get_mainplot()
            distriplot = plot.get_distribution_plot()
            slider = plot.get_slider()
            rslider = plot.get_rangeslider()
            self.script, self.div = components(column(distriplot, mainplot, slider, rslider), wrap_script=False)
        except Exception as e:
            print('Error in Fig Object. Cannot create direction plot: ', e)
            logger.debug(f'Cannot create direction plot, {e}')

    def get_plot(self):
        return {'script': self.script, 'div': self.div}
