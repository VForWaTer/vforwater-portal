import pandas as pd
from django.core.exceptions import EmptyResultSet

from heron.settings import max_size_preview_plot
from vfw_home.data_tools import DB_load_directiondata, DB_load_data
from vfw_home.models import Entries


class DataObject:

    def __init__(self, webID="", date=None):

        self.has_precision = None
        self.dataframe = None
        self.qs_cols = None
        self.data_columns = None
        self.data_qs = None
        self.qs = None
        self.data_table_name = None
        self.timescale = None
        self.df = None
        self.data_format = None
        self.webID = webID
        self.date = date

        self.full = True
        self.ID = None
        self.source = None
        self.qs_entry = None
        self.general_data_qs = None
        self.label = ""

        self.metadata = {}

        self.length = None
        self.timestep_label = ""
        self.timestep_size = 0

        self.__set_vars__()
        print('data_table_name: ', self.data_table_name)

    def __str__(self):
        return self.label

    def __set_vars__(self):

        if self.webID[0:2] == 'db':
            self.ID = self.webID[2:]
            self.source = 'db'
            self.qs_entry = Entries.objects.filter(id=self.ID)
            self.data_table_name = self.qs_entry.values_list('datasource__path', flat=True)[0]
            self.set_general_data_qs()
            self.length = self.db_data_length()

            label = self.qs_entry.values_list('variable__name', 'variable__symbol', 'variable__unit__symbol')
            self.label = self.format_label(label[0][0], label[0][1], label[0][2])
            self.set_data_qs()
            self.get_db_data()
            self.set_precision()
            self.has_precision = False

        elif self.webID[0:3] == 'wps':
            self.ID = self.webID[3:]
            self.source = 'wps'

    def set_precision(self):
        if not self.dataframe['precision'].isnull().values.any():
            self.has_precision = True

    def set_data_qs(self):
        qs = self.general_data_qs
        if not self.full:
            qs = self.general_data_qs[:max_size_preview_plot]
        if self.data_table_name == 'timeseries_1d':
            self.data_columns = ['tstamp', 'value', 'precision']
            self.qs_cols = [self.data_table_name + '__' + i for i in self.data_columns]
            self.data_qs = qs.values(*self.qs_cols)  # .explain(verbose=True)

    def get_db_data(self):
        if self.label.find('direction') != -1:
            self.timestep_label = 'week'  # time interval used to plot, choose 'year', 'month', 'week' or 'day'
            # if full_res is False:
            self.dataframe, self.timestep_label = DB_load_directiondata(self.ID, self.timestep_label,
                                                                        self.date, self.full)
        elif self.label.find('windspeed') != -1:
            print('its SPEED!! _________________')
        else:
            print('______ else')
            df = pd.DataFrame(list(self.data_qs))
            self.dataframe = df.rename(columns=dict(zip(self.qs_cols, self.data_columns)), errors="raise")

    def timescale_from_data(self):
        stepsize = []
        steps = 1
        checklength = 11

        if self.df.shape[0] <= checklength + 1:
            checklength = self.df.shape[0] - 1

        if 'tstamp' in self.df:
            relcol = self.df['tstamp']
        elif self.df.index.name == 'tstamp':
            relcol = self.df.index

        while steps < checklength:
            stepsize.append(relcol[steps + 1] - relcol[steps])
            steps += 1
        self.timescale = min(stepsize)

    def set_timescale(self):
        timescale = self.qs_entry.values_list('datasource__temporal_scale__resolution')[0][0]
        if timescale:
            self.timescale = pd.to_timedelta(timescale)
        else:
            self.timescale_from_data(self)

    def set_general_data_qs(self):
        """
        Django QuerySet to access data (with respect to data_table_name and date).
        Use qs_data to get value or values_list of interest.

        """
        if self.data_table_name is None:
            raise {'error': 'Dataset has no datasource__path.'}

        query_path = {'{0}'.format(self.data_table_name): self.ID}
        if self.date and self.date[0]:
            query_path[self.data_table_name + '__tstamp__gte'] = self.date[0]
            query_path[self.data_table_name + '__tstamp__lte'] = self.date[1]

        self.general_data_qs = Entries.objects.filter(**query_path)

    def db_data_length(self):
        """
        Get length of Dataset stored in the database.
        If size is greater than allowd in settings.max_size_preview_plot the "full" flag is set to False
        """
        self.length = self.general_data_qs.count()
        if self.length == 0:  # if not qs.exists():
            print('Problems with query_path: ', self.general_data_qs)
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

