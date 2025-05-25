import json
import logging

import numpy as np
import pandas as pd
from decimal import Decimal
from django.core.exceptions import EmptyResultSet
from django.http import Http404

from heron.settings import MAX_SIZE_PREVIEW_PLOT
from .data_tools import DB_load_directiondata
from vfw_home.models import Entries, NmEntrygroups

logger = logging.getLogger(__name__)


class DataObject:

    def __init__(self, webID: object = "", date: object = None) -> object:
        """

        :param webID: string like 'wps123' or 'db123'
        :param date: should be formated with make_aware(datetime.datetime.strptime(request_dict['end'], '%Y-%m-%d')
        """
        self.__data_qs__ = None
        self.__general_data_qs__ = None
        self.__interest_in_gaps__ = True
        self.__qs_cols__ = None
        self.__qs_entry__ = None
        self.__qs_group__ = None
        self.__row_limit__ = MAX_SIZE_PREVIEW_PLOT
        self.__value_before_gap__ = None
        self.coords = None
        self.data_columns = None
        self.data_format = None
        self.data_table_name = None
        self.dataframe = None
        self.date = date
        self.db_cols_timeseries = ['tstamp', 'data', 'precision']
        self.db_cols_timeseries_1d = ['tstamp', 'value', 'precision']
        self.full = True
        self.has_nan = False
        self.has_precision = False
        self.ID = None
        self.split_in = []
        self.is_split = False   # True when dataset is split due to different resolutions
        self.label = ""
        self.length = None
        self.metadata = {}
        self.missing_data = None
        self.multiple_lines = False
        self.range_dict = {"x_min": None, "x_max": None, "y_min": None, "y_max": None}
        self.source = None
        self.timescale = None
        self.timestep_label = ""
        self.type = ""
        self.uuID = None
        self.webID = webID

        self.__set_vars__()

    def __str__(self):
        return self.label

    def __set_vars__(self):

        if self.webID[0:2] == 'db':
            self.ID = self.webID[2:]
            self.source = 'db'
            self.__qs_entry__ = Entries.objects.filter(id=self.ID)
            self.type = self.__qs_entry__.values_list('datasource__datatype__name', flat=True)[0]
            self.uuID = self.__qs_entry__.values_list('uuid', flat=True)[0]
            label = self.__qs_entry__.values_list('variable__name', 'variable__symbol', 'variable__unit__symbol')
            self.label = self.format_label(label[0][0], label[0][1], label[0][2])
            location = self.__qs_entry__.values_list('location', flat=True)[0]
            self.coords = json.loads(location.geojson)
            self.coords['srid'] = location.srid  # TODO: check how many queries for coords
            self.data_table_name = self.__qs_entry__.values_list('datasource__path', flat=True)[0]
            self.data_names = self.__qs_entry__.values_list('datasource__data_names', flat=True)[0]
            if not self.data_names:
                print(f'WARNING: Dataset with ID {self.ID} has no data name in datasource table!')
                self.data_names = [label[0][0]]
            self.__general_data_qs__ = self.__set_general_data_qs__(self.data_table_name, self.date, self.ID)
            self.length = self.db_data_length()
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

        if self.data_table_name == 'timeseries_1d':
            self.data_columns = self.db_cols_timeseries_1d
            self.value_column = 'value'
            qs = self.__general_data_qs__.order_by(self.data_table_name + '__' +'tstamp')
        elif self.data_table_name == 'timeseries':
            self.data_columns = self.db_cols_timeseries
            self.value_column = 'data'
            qs = self.__general_data_qs__.order_by(self.data_table_name + '__' + 'tstamp')
            if len(self.data_names) > 1:
                self.multiple_lines = True

        else:
            print('\033[31mYou try to access a new table. Handle it!\033[0m ')

        if not self.full:
            qs = qs[:self.__row_limit__]

        self.__qs_cols__ = [self.data_table_name + '__' + i for i in self.data_columns]
        self.__data_qs__ = qs.values(*self.__qs_cols__)
    def __get_db_data__(self):

        try:
            if self.label.find('direction') != -1:
                self.timestep_label = 'week'  # time interval used to plot, choose 'year', 'month', 'week' or 'day'
                self.dataframe, self.timestep_label = DB_load_directiondata(self.ID, self.timestep_label,
                                                                            self.date, self.full)
                self.__interest_in_gaps__ = False
            elif self.label.find('windspeed') != -1:
                print('its SPEED!! _________________')
            elif self.label.find('Eddy Covariance') != -1:
                self.__row_limit__ = 10
                self.__set_data_qs__()
                self.__get_eddy_data__()
            else:
                df = pd.DataFrame(list(self.__data_qs__))
                self.dataframe = df.rename(columns=dict(zip(self.__qs_cols__, self.data_columns)), errors="raise")
                if isinstance(self.dataframe[self.value_column][0], list) \
                    and len(self.dataframe[self.value_column][0]) == 1:
                    self.dataframe[self.value_column] = [i[0] for i in self.dataframe[self.value_column]]
                elif isinstance(self.dataframe[self.value_column][0], list) \
                    and len(self.dataframe[self.value_column][0]) > 1:
                    print('ERROR: Expect only one column for timeseries_1d')
                    logger.debug('ERROR: Expect only one column for timeseries_1d')
        except Exception as e:
            print('\033[33mUnable to access database:\033[0m ', e)
            raise Http404

        if self.multiple_lines:
            self.dataframe = self.__mulitvalcol_to_mulitcolval__(self.dataframe, self.data_names, self.value_column)

        for i in self.dataframe.select_dtypes(include=['object']).columns:
            if isinstance(self.dataframe[i][0], (Decimal,)):
                self.dataframe[i] = self.dataframe[i].astype(float)

    def __get_eddy_data__(self):
        df = pd.DataFrame(list(self.__data_qs__))
        self.dataframe = df.rename(columns=dict(zip(self.__qs_cols__, self.data_columns)), errors="raise")

        # additional data is needed for footprint. Get group qs:
        group_id = NmEntrygroups.objects.filter(entry_id=self.ID).values_list('group_id', flat=True)[0]
        self.__qs_group__ = NmEntrygroups.objects.filter(group_id=group_id) \
            .values('entry__datasource__data_names', 'entry_id', 'entry__datasource__path')

        # get additional metadata:
        additional_datasets = {
            'p': ['air pressure', self.db_cols_timeseries, 'data'],
            'direction': ['wind direction', self.db_cols_timeseries, 'data'],
        }
        for i in additional_datasets.values():
            new_df, col_names = self.__get_extra_columns__(*i)
            self.dataframe[col_names] = new_df[col_names]

    def __get_extra_columns__(self, var_name, db_cols, data_col):
        """

        :param var_name: variable name of the dataset in the database
        :param db_cols:  name of the columns in the respective data table (e.g. in timeseries)
        :param data_col: name of the column containing the actual values
        :return:
        """
        air_tmp_metadat = self.__qs_group__.filter(entry__variable__name=var_name)[0]
        air_tmp_path = air_tmp_metadat['entry__datasource__path']
        air_tmp_cols_split = air_tmp_metadat['entry__datasource__data_names']

        # get additional data:
        air_tmp_data_qs = self.__set_general_data_qs__(air_tmp_path, self.date, air_tmp_metadat['entry_id'])
        if not self.full:
            air_tmp_data_qs = air_tmp_data_qs[:self.__row_limit__]

        air_tmp_cols = [air_tmp_path + '__' + i for i in db_cols]
        air_tmp_data_qs = air_tmp_data_qs.values(*air_tmp_cols)

        air_tmp_df = pd.DataFrame(list(air_tmp_data_qs))
        air_tmp_df = air_tmp_df.rename(columns=dict(zip(air_tmp_cols, db_cols)), errors="raise")
        air_tmp_df = self.__mulitvalcol_to_mulitcolval__(air_tmp_df, air_tmp_cols_split, data_col)
        return air_tmp_df, air_tmp_cols_split

    @staticmethod
    def __mulitvalcol_to_mulitcolval__(df, new_col_names, source_col):
        """

        :param df: pandas df
        :param new_col_names: list of names for the new columns
        :param source_col: source column name
        :return:
        """
        for (i, n) in enumerate(new_col_names):
            df[n] = [x[i] for x in df[source_col]]
        return df

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

    @staticmethod
    def __set_general_data_qs__(data_table_name, date, ID):
        """
        Django QuerySet to access data (with respect to data_table_name and date).
        Use qs_data to get value or values_list of interest.

        """
        if data_table_name is None:
            raise LookupError({'error': 'Dataset has no datasource__path.'})

        query_path = {f'{data_table_name}': ID}
        if date and date[0]:
            query_path[data_table_name + '__tstamp__gte'] = date[0]
            query_path[data_table_name + '__tstamp__lte'] = date[1]

        return Entries.objects.filter(**query_path)

    def db_data_length(self):
        """
        Get length of Dataset stored in the database.
        If size is greater than allowed in settings.MAX_SIZE_PREVIEW_PLOT the "full" flag is set to False
        """
        self.length = self.__general_data_qs__.count()
        if self.length == 0:  # if not qs.exists():
            print('Data_obj.db_data_length: Problems with query_path: ', self.__general_data_qs__)
            logger.debug(f'Problems with query_path, {self.__general_data_qs__}')
            raise EmptyResultSet(f'Problems with query_path for id={self.ID}, {self.__general_data_qs__}')

        if self.length > self.__row_limit__:
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
        """
        if self.has_precision and 'avg' in self.dataframe.columns:
            self.range_dict['y_max'] = self.dataframe['avg'] + self.dataframe['precmax']
            self.range_dict['y_min'] = self.dataframe['avg'] - self.dataframe['precmax']
            self.range_dict['y_max_avg'] = self.dataframe['avg'] + self.dataframe['precavg']
            self.range_dict['y_min_avg'] = self.dataframe['avg'] - self.dataframe['precavg']
        elif self.has_precision:
            self.range_dict['y_max'] = self.dataframe[self.value_column] + self.dataframe['precision']
            self.range_dict['y_min'] = self.dataframe[self.value_column] - self.dataframe['precision']
        else:
            self.range_dict['y_max'] = max(self.dataframe[self.value_column])
            self.range_dict['y_min'] = min(self.dataframe[self.value_column])

    def __get_gap_pos__(self):
        """
        Iterate over a dataset and find all positions where the distance
        between two rows is greater than the given scale.
        """
        index = 'tstamp'
        # use datetime as index and request the list of datetimes your looking for
        starttime = self.dataframe[index][0]
        endtime = self.dataframe.iloc[-1][index]
        # check if dataset has already NaNs
        if len(self.dataframe[self.dataframe[self.value_column].isna()]) > 0:
            self.dataframe.dropna(subset=[self.value_column], inplace=True)
            self.dataframe.reset_index(drop=True, inplace=True)
        # create a perfect DataFrame without gaps
        perfect_frame = pd.DataFrame(pd.date_range(start=starttime,
                                                   end=endtime, freq=self.timescale), columns=['tstamp'])
        # fill the empty (perfect) frame without gaps with the data from original frame
        combined_dataframes = pd.merge(perfect_frame, self.dataframe, how="outer", on="tstamp")
        # get rows without values
        empty_list = combined_dataframes.loc[combined_dataframes[self.value_column].isna()].index.values

        # use two shifted lists for comparison to find the first value of a gap
        shifted_list = np.append(0, empty_list)
        empty_list = np.append(empty_list, 0)  # all indices without a value in a perfect timeseries
        diff_list = np.subtract(empty_list, shifted_list)  # value at index position of first row of gap is greater 1

        # get indices of the perfect dataframe (without gaps)
        perfectframe_gaps = empty_list[diff_list > 1] - 1  # index of last value before gap
        # get list of dates just before the gap
        gaps_date_list = combined_dataframes.loc[perfectframe_gaps.tolist()][index].tolist()  # dates at last values before gap

        # make a list of the indices (from the original dataframe) of the position before the gaps
        self.__value_before_gap__ = self.dataframe.loc[self.dataframe[index].isin(gaps_date_list)].index.values.tolist()

    def __fill_data_gaps__(self):
        """
        Fill gaps in datasets with nan and
        prepare another dataframe to plot linear interpolated areas with missing data.
        """
        self.has_nan = True
        defect_x = []
        defect_y = []
        col = self.value_column
        gap_length = len(self.__value_before_gap__)

        if 'avg' in self.dataframe.columns:  # if dataset with average, min, max  values
            for pos in self.__value_before_gap__[::-1]:
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
                defect_x.extend([self.dataframe[col][0][pos] - self.timescale, self.dataframe[col][0][pos],
                                 self.dataframe[col][0][pos + 3], self.dataframe[col][0][pos] + self.timescale])
                defect_y.extend([float('nan'), self.dataframe[col][1][pos],
                                 self.dataframe[col][1][pos + 3], float('nan'), ])
            source = pd.DataFrame({'date': self.dataframe[col][0], 'y': self.dataframe[col][1],
                                   'ymin': self.dataframe[col][2], 'ymax': self.dataframe[col][3],
                                   'count': self.dataframe[col][4]})
            self.missing_data = pd.DataFrame({'tstamp': defect_x, self.value_column: defect_y})
        else:  # if full dataset, without average, min, max values
            # copy rows before and after a gap
            row_before = self.dataframe.loc[self.dataframe.index.isin(self.__value_before_gap__)].copy()
            row_after = self.dataframe.loc[self.dataframe.index.isin(np.array(self.__value_before_gap__) + 1)].copy()

            defectrow1 = pd.DataFrame(row_before['tstamp'] - self.timescale)
            defectrow1['value'] = pd.NA
            defectrow2 = pd.DataFrame(row_before['tstamp'])
            defectrow3 = pd.DataFrame(row_after['tstamp'])
            if self.data_format == '3D':
                defectrow2['value'] = pd.NA
                defectrow3['value'] = pd.NA
            else:
                defectrow2['value'] = row_before[self.value_column]
                defectrow3['value'] = row_after[self.value_column]

            defectrow4 = pd.DataFrame(row_after['tstamp'] + self.timescale)
            defectrow4['value'] = pd.NA

            # add column just to bring 'no data' in the right order
            defectrow1['orderCol'] = list(range(0, gap_length * 4, 4))
            defectrow2['orderCol'] = list(range(1, gap_length * 4, 4))
            defectrow3['orderCol'] = list(range(2, gap_length * 4, 4))
            defectrow4['orderCol'] = list(range(3, gap_length * 4, 4))

            defect = pd.concat([defectrow1, defectrow2, defectrow3, defectrow4])
            # reindex rows before and after a gap
            defect.sort_values(by='orderCol', inplace=True)
            defect.drop(columns=['orderCol'])

            defect_x = defect.tstamp.tolist()
            defect_y = defect.value.tolist()

            # Now use rows before and after to add NaNs to dataframe
            row_before.index = row_before.index + 0.3
            row_after.index = row_before.index + 0.3
            # add datetime for the first and the last gap position
            row_before['tstamp'] = row_before['tstamp'] + self.timescale
            row_after['tstamp'] = row_after['tstamp'] - self.timescale
            # combine new rows in one dataframe
            new_df_rows = pd.concat([row_before, row_after])
            # set all columns except tstamp to nan
            new_df_rows.iloc[:, range(1, len(self.dataframe.columns))] = pd.NA
            # add new rows to dataframe and reset the index to integer
            self.dataframe = pd.concat([self.dataframe, new_df_rows]).sort_index().reset_index(drop=True)
            self.missing_data = pd.DataFrame({'tstamp': defect_x, self.value_column: defect_y})

    def __get_split__(self):
        split_datasets = (Entries.objects.filter(pk=self.ID, nmentrygroups__group__type__name='Split dataset')
                          .values('id', 'nmentrygroups__group_id')
                          .order_by('nmentrygroups__group_id'))
        pass
