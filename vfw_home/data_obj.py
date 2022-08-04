import numpy as np
import pandas as pd
from django.core.exceptions import EmptyResultSet

from heron.settings import max_size_preview_plot
from vfw_home.data_tools import DB_load_directiondata
from vfw_home.models import Entries


class DataObject:

    def __init__(self, webID="", date=None):

        self.__data_qs__ = None
        self.__general_data_qs__ = None
        self.__interest_in_gaps__ = True
        self.__qs_cols__ = None
        self.__qs_entry__ = None
        self.__value_before_gap__ = None
        self.data_columns = None
        self.data_format = None
        self.data_table_name = None
        self.dataframe = None
        self.date = date
        self.full = True
        self.has_nan = False
        self.has_precision = False
        self.ID = None
        self.label = ""
        self.length = None
        self.metadata = {}
        self.missing_data = None
        self.range_dict = {"x_min": None, "x_max": None, "y_min": None, "y_max": None}
        self.source = None
        self.timescale = None
        self.timestep_label = ""
        self.webID = webID

        self.__set_vars__()

    def __str__(self):
        return self.label

    def __set_vars__(self):

        if self.webID[0:2] == 'db':
            self.ID = self.webID[2:]
            self.source = 'db'
            self.__qs_entry__ = Entries.objects.filter(id=self.ID)
            self.data_table_name = self.__qs_entry__.values_list('datasource__path', flat=True)[0]
            self.data_names = self.__qs_entry__.values_list('datasource__data_names', flat=True)[0]
            self.__set_general_data_qs__()
            self.length = self.db_data_length()
            label = self.__qs_entry__.values_list('variable__name', 'variable__symbol', 'variable__unit__symbol')
            self.label = self.format_label(label[0][0], label[0][1], label[0][2])
            self.__set_data_qs__()
            self.__get_db_data__()
            self.__set_precision__()
            self.__set_timescale__()
            if self.__interest_in_gaps__:
                self.__get_gap_pos__()
                if len(self.__value_before_gap__) > 0:
                    self.__fill_data_gaps__()

        elif self.webID[0:3] == 'wps':
            self.ID = self.webID[3:]
            self.source = 'wps'

    def __set_precision__(self):
        """
        Check if dataframe has a precision column and if there is any value in that column.
        """
        if 'precision' in self.dataframe.columns and not self.dataframe['precision'].isnull().values.any():
            self.has_precision = True

    def __set_data_qs__(self):
        """
        Define the queryset to the respective data set according to its data_table_name.
        """
        qs = self.__general_data_qs__
        if not self.full:
            qs = self.__general_data_qs__[:max_size_preview_plot]
        if self.data_table_name == 'timeseries_1d':
            self.data_columns = ['tstamp', 'value', 'precision']
            self.__qs_cols__ = [self.data_table_name + '__' + i for i in self.data_columns]
            self.__data_qs__ = qs.values(*self.__qs_cols__)  # .explain(verbose=True)
        if self.data_table_name == 'timeseries':
            self.data_columns = ['tstamp', 'data', 'precision']
            self.data_format = '3D'
            self.__qs_cols__ = [self.data_table_name + '__' + i for i in self.data_columns]
            self.__data_qs__ = qs.values(*self.__qs_cols__)
        else:
            print('\033[31mYou try to access a new table. Handle it!\033[0m ')

    def __get_db_data__(self):

        if self.label.find('direction') != -1:
            self.timestep_label = 'week'  # time interval used to plot, choose 'year', 'month', 'week' or 'day'
            # if full_res is False:
            self.dataframe, self.timestep_label = DB_load_directiondata(self.ID, self.timestep_label,
                                                                        self.date, self.full)
            self.__interest_in_gaps__ = False
        elif self.label.find('windspeed') != -1:
            print('its SPEED!! _________________')
        else:
            print('else: ')
            df = pd.DataFrame(list(self.__data_qs__))
            self.dataframe = df.rename(columns=dict(zip(self.__qs_cols__, self.data_columns)), errors="raise")

    def __timescale_from_data__(self):
        steplist = []
        steps = 1
        relcol = {}
        testlength = self.dataframe.shape[0] if self.dataframe.shape[0] <= 11 else 11

        if self.dataframe.shape[0] <= testlength + 1:
            testlength = self.dataframe.shape[0] - 1

        if 'tstamp' in self.dataframe:
            relcol = self.dataframe['tstamp']
        elif self.dataframe.index.name == 'tstamp':
            relcol = self.dataframe.index

        while steps < testlength:
            steplist.append(relcol[steps + 1] - relcol[steps])
            steps += 1
        self.timescale = min(steplist)

    def __set_timescale__(self):
        timescale = self.__qs_entry__.values_list('datasource__temporal_scale__resolution')[0][0]
        if timescale:
            self.timescale = pd.to_timedelta(timescale)
        else:
            self.__timescale_from_data__()

    def __set_general_data_qs__(self):
        """
        Django QuerySet to access data (with respect to data_table_name and date).
        Use qs_data to get value or values_list of interest.

        """
        if self.data_table_name is None:
            raise LookupError({'error': 'Dataset has no datasource__path.'})

        query_path = {'{0}'.format(self.data_table_name): self.ID}
        if self.date and self.date[0]:
            query_path[self.data_table_name + '__tstamp__gte'] = self.date[0]
            query_path[self.data_table_name + '__tstamp__lte'] = self.date[1]

        self.__general_data_qs__ = Entries.objects.filter(**query_path)

    def db_data_length(self):
        """
        Get length of Dataset stored in the database.
        If size is greater than allowd in settings.max_size_preview_plot the "full" flag is set to False
        """
        self.length = self.__general_data_qs__.count()
        if self.length == 0:  # if not qs.exists():
            print('Problems with query_path: ', self.__general_data_qs__)
            raise EmptyResultSet('Got no data in data_tools.is_data_short for id={}'.format(self.ID))

        if self.length > max_size_preview_plot:
            self.full = False

    @staticmethod
    def format_label(name: str, symbol: str, unit_symbol: str):
        """
        format label for plots from variable name, symbol and unit symbol
        """
        sup = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
        superscript_label = unit_symbol.replace("^", "").translate(sup)
        return "{} ({}) [{}]".format(name, symbol, superscript_label)

    def __set_range__(self):
        """
        TODO: shouldn't I use min/max of sums?
        """
        if self.has_precision and 'value' in self.dataframe.columns:
            self.range_dict['y_max'] = self.dataframe['value'] + self.dataframe['precision']
            self.range_dict['y_min'] = self.dataframe['value'] - self.dataframe['precision']
        elif self.has_precision and 'avg' in self.dataframe.columns:
            self.range_dict['y_max'] = self.dataframe['avg'] + self.dataframe['precmax']
            # self.range_dict['y_min'] = self.dataframe['acg'] - self.dataframe['precmax']
            self.range_dict['y_min'] = self.dataframe['avg'] - self.dataframe['precmax']
            self.range_dict['y_max_avg'] = self.dataframe['avg'] + self.dataframe['precavg']
            # self.range_dict['y_min_avg'] = self.dataframe['acg'] - self.dataframe['precavg']
            self.range_dict['y_min_avg'] = self.dataframe['avg'] - self.dataframe['precavg']
        elif 'value' in self.dataframe.columns:
            self.range_dict['y_max'] = max(self.dataframe['value'])
            self.range_dict['y_min'] = min(self.dataframe['value'])
        else:
            print('WARNING: there is a unknown dataset to convert precision in precision to minmax.')

    def __get_gap_pos__(self):
        """
        Iterate over a dataset and find all positions where the distance
        between two rows is greater than the given scale.
        """
        index = 'tstamp'
        val_beforeGap = []
        # use datetime as index and request the list of datetimes your looking for
        starttime = self.dataframe[index][0]
        endtime = self.dataframe.iloc[-1][index]
        # create a perfect DataFrame without gaps
        perfect_frame = pd.DataFrame(pd.date_range(start=starttime,
                                                   end=endtime, freq=self.timescale), columns=['tstamp'])
        # fill the empty frame without gaps with the data from original frame
        combined_dataframes = pd.merge(perfect_frame, self.dataframe, how="outer", on="tstamp")
        # get rows without values
        try:
            empty_list = combined_dataframes.loc[combined_dataframes['value'].isna()].index.values
        except Exception as e:
            empty_list = combined_dataframes.loc[combined_dataframes['data'].isna()].index.values

        # use two shifted lists for comparison to find the first value of a gap
        shifted_list = np.append(0, empty_list)
        empty_list = np.append(empty_list, 0)
        diff_list = np.subtract(empty_list, shifted_list)

        # get indices of the perfect dataframe (without gaps)
        perfectframe_gaps = empty_list[diff_list > 1] - 1
        # get list of dates just before the gap
        gaps_date_list = combined_dataframes.loc[perfectframe_gaps.tolist()][index].tolist()

        # make a list of the indices (from the original dataframe) of the position before the gaps
        for i in gaps_date_list:
            val_beforeGapRow = self.dataframe.loc[self.dataframe[index] == i]
            val_beforeGap.append(val_beforeGapRow.index[0])

        self.__value_before_gap__ = val_beforeGap

    def __fill_data_gaps__(self):
        """
        Fill gaps in datasets and prepare for plot
        """
        self.has_nan = True
        defect_x = []
        defect_y = []
        col = ''
        if 'data' in self.data_columns:
            col = 'data'
        elif 'value' in self.data_columns:
            col = 'value'
        # if 'precision' in df.columns and df['precision'].sum() > 0:  # if preview with average, min, max  values
        if 'avg' in self.dataframe.columns:  # if dataset with average, min, max  values
            for pos in self.__value_before_gap__[::-1]:
                # TODO: change this code to pandas df.
                print('TODO: change this code to pandas df.')
                self.dataframe[col][0] = self.dataframe[col][0][: pos + 1] + \
                                         (self.dataframe[col][0][pos] + self.timescale,
                                          self.dataframe[col][0][pos + 1] - self.timescale,) + \
                                         self.dataframe[col][0][pos + 1:]
                self.dataframe[col][1] = self.dataframe[col][1][: pos + 1] + (float('nan'), float('nan'),) + \
                                         self.dataframe[col][1][pos + 1:]
                bandbef = (self.dataframe[col][2][pos] + self.dataframe[col][3][pos]) / 2
                bandaft = (self.dataframe[col][2][pos + 1] + self.dataframe[col][3][pos + 1]) / 2
                self.dataframe[col][2] = self.dataframe[col][2][: pos + 1] + (bandbef, bandaft,) + self.dataframe[col][
                                                                                                       2][
                                                                                                   pos + 1:]
                self.dataframe[col][3] = self.dataframe[col][3][: pos + 1] + (bandbef, bandaft,) + self.dataframe[col][
                                                                                                       3][
                                                                                                   pos + 1:]
                self.dataframe[col][4] = self.dataframe[col][4][: pos + 1] + (0, 0,) + self.dataframe[col][4][pos + 1:]
                # white_line = white_line[: pos + 1] + (bandbef, bandaft,) + white_line[pos + 1:]
                defect_x.extend([self.dataframe[col][0][pos] - self.timescale, self.dataframe[col][0][pos],
                                 self.dataframe[col][0][pos + 3], self.dataframe[col][0][pos] + self.timescale])
                defect_y.extend([float('nan'), self.dataframe[col][1][pos],
                                 self.dataframe[col][1][pos + 3], float('nan'), ])
            source = pd.DataFrame({'date': self.dataframe[col][0], 'y': self.dataframe[col][1],
                                   'ymin': self.dataframe[col][2], 'ymax': self.dataframe[col][3],
                                   'count': self.dataframe[col][4]})
            self.missing_data = pd.DataFrame({'tstamp': defect_x, 'value': defect_y})
        else:  # if full dataset, without average, min, max values
            # copy random rows which happen to be the first two
            empty_rows = self.dataframe.loc[1:2].copy()
            # set all columns except tstamp to nan
            empty_rows.loc[:, empty_rows.columns != 'tstamp'] = float('nan')
            for pos in self.__value_before_gap__[::-1]:
                # set correct tstamp to new rows
                empty_rows['tstamp'] = self.dataframe['tstamp'][pos] + self.timescale, self.dataframe['tstamp'][
                    pos + 1] - self.timescale
                # insert new rows with float index positions
                self.dataframe.loc[pos + 0.3] = empty_rows.loc[1]
                # df.loc[pos+0.3] = df['tstamp'][pos] + scale, float('nan'), float('nan')
                self.dataframe.loc[pos + 0.6] = empty_rows.loc[2]
                # df.loc[pos+0.6] = df['tstamp'][pos + 1] - scale, float('nan'), float('nan')
                defect_x.extend([self.dataframe['tstamp'][pos] - self.timescale, self.dataframe['tstamp'][pos],
                                 self.dataframe['tstamp'][pos + 1],
                                 self.dataframe['tstamp'][pos + 1] + self.timescale])
                if self.data_format == '3D':
                    defect_y.extend([float('nan'), float('nan'), float('nan'), float('nan'), ])
                elif 'value' in self.dataframe.columns:
                    defect_y.extend(
                        [float('nan'), self.dataframe['value'][pos], self.dataframe['value'][pos + 1], float('nan'), ])
                elif 'data' in self.dataframe.columns:
                    defect_y.extend(
                        [float('nan'), self.dataframe['data'][pos], self.dataframe['data'][pos + 1], float('nan'), ])
            # reset the index to integer
            self.dataframe = self.dataframe.sort_index().reset_index(drop=True)
            self.missing_data = pd.DataFrame({'tstamp': defect_x, 'value': defect_y})
