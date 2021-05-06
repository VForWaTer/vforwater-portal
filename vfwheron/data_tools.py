import pandas as pd
from django.db import connections

from vfwheron.models import Entries, Timeseries


def __get_timescale(df):
    """
    Get a dataframe with a timestamp ('tstmp'), iterate over the first 11 values (or less for shorter datasets)
    and return the smallest time difference.

    :param df: pandas dataframe
    :return: pandas timedelta
    """
    stepsize = []
    steps = 1
    checklength = 11

    if df.shape[0] <= checklength + 1:
        checklength = df.shape[0] - 1

    while steps < checklength:
        stepsize.append(df['tstamp'][steps + 1] - df['tstamp'][steps])
        steps += 1
    return min(stepsize)


# TODO: remove dependency for data from code. Only pandas df should be used => remove 'result'
def __DB_load_data(ID: str):
    """
    Load data from database and return a dict with data, pandas df and axis

    :param ID: string
    :return: dict - {df, axis, scale, has_preci}
    """
    datatable = Entries.objects.filter(id=ID).values_list('datasource__datatype__name', flat=True)[0]
    if datatable == 'timeseries':
        # request data with django ORM
        df = pd.DataFrame(list(Timeseries.objects.filter(entry_id=ID).values('tstamp', 'value', 'precision')))

        timescale = Entries.objects.filter(id=ID).values_list('datasource__temporal_scale__resolution')[0][0]
        if timescale:
            timescale = pd.to_timedelta(timescale)
        else:
            timescale = __get_timescale(df)

        if df['precision'].isnull().values.any():
            precision = False
            axis = {'ymin': df['value'].min(), 'ymax': df['value'].max()}
        else:
            precision = True
            axis = {'ymin': (df['value'] - df['precision']).min(),
                    'ymax': (df['value'] + df['precision']).max()}

        return {'df': df, 'axis': axis, 'scale': timescale, 'has_preci': precision}
    else:
        print('*** PLEASE IMPLEMENT OTHER DATATYPES, TOO! ***')


def __DB_load_data_avg(ID: int, scale='day'):
    """

    :param ID: Entry ID
    :param scale:
    :return:
    """
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

        df = pd.DataFrame(data={'tstamp': result[0], 'avg': result[1], 'min': result[2], 'max': result[3],
                                'count': result[4], 'precavg': result[5], 'precmin': result[6], 'precmax': result[7]})
        # y is for the main plot -> min and  max of the day of the day,
        # y2 for the secondary plot with min and max in each group for each day
        axis = {'ymin': df['min'].min, 'ymax': df['max'].max,
                'y2min': df['precmin'].min, 'y2max': df['precmax'].max}
        # axis = {'y1min': min(result[2]), 'y1max': max(result[3]), 'y2min': min(result[4]), 'y2max': max(result[4])}
        timescale = Entries.objects.filter(id=ID).values_list('datasource__temporal_scale__resolution')[0][0]
        if timescale:
            timescale = pd.to_timedelta(timescale)
        else:
            timescale = __get_timescale(df)

        if df['precavg'].isnull().values.any():
            precision = False
        else:
            precision = True

        return {'data': df, 'axis': axis, 'scale': timescale, 'has_preci': precision}
    else:
        print('*** PLEASE IMPLEMENT OTHER DATATYPES, TOO! ***')


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


def fill_data_gaps(db_data: object):
    """
    Fill gaps in datasets and prepare for plot

    :param db_data: dict - dictionary with pandas dataframe 'df' and 'scale'
    :return:
    """
    # use first five time steps to estimate resolution/step size of data
    scale = db_data['scale']
    df = db_data['df']
    missing_data = {}

    # check if data has a scaling
    if not scale:
        scale = __get_scaling(df)

    # check if data is continuous. If not write position of missing values in noDataPos
    noDataPos = __get_gap_position(df, scale, 'tstamp')
    # check if dataset has values for precision

    nan_in_data = False
    # To get a discontinuous line add 'nan' when a time step is missing.
    if len(noDataPos) > 0:
        nan_in_data = True
        defect_x = []
        defect_y = []
        # if 'precision' in df.columns and df['precision'].sum() > 0:  # if preview with average, min, max  values
        if 'avg' in df.columns:  # if dataset with average, min, max  values
            for pos in noDataPos[::-1]:
                # TODO: change this code to pandas df.
                print('TODO: change this code to pandas df.')
                db_data['data'][0] = db_data['data'][0][: pos + 1] + \
                                     (db_data['data'][0][pos] + scale,
                                      db_data['data'][0][pos + 1] - scale,) + \
                                     db_data['data'][0][pos + 1:]
                db_data['data'][1] = db_data['data'][1][: pos + 1] + (float('nan'), float('nan'),) + \
                                     db_data['data'][1][pos + 1:]
                bandbef = (db_data['data'][2][pos] + db_data['data'][3][pos]) / 2
                bandaft = (db_data['data'][2][pos + 1] + db_data['data'][3][pos + 1]) / 2
                db_data['data'][2] = db_data['data'][2][: pos + 1] + (bandbef, bandaft,) + db_data['data'][2][
                                                                                           pos + 1:]
                db_data['data'][3] = db_data['data'][3][: pos + 1] + (bandbef, bandaft,) + db_data['data'][3][
                                                                                           pos + 1:]
                db_data['data'][4] = db_data['data'][4][: pos + 1] + (0, 0,) + db_data['data'][4][pos + 1:]
                # white_line = white_line[: pos + 1] + (bandbef, bandaft,) + white_line[pos + 1:]
                defect_x.extend([db_data['data'][0][pos] - scale, db_data['data'][0][pos],
                                 db_data['data'][0][pos + 3], db_data['data'][0][pos] + scale])
                defect_y.extend([float('nan'), db_data['data'][1][pos],
                                 db_data['data'][1][pos + 3], float('nan'), ])
            source = pd.DataFrame({'date': db_data['data'][0], 'y': db_data['data'][1],
                                   'ymin': db_data['data'][2], 'ymax': db_data['data'][3],
                                   'count': db_data['data'][4]})
            missing_data = pd.DataFrame({'defect_x': defect_x, 'defect_y': defect_y})
        else:  # if full dataset, without average, min, max values
            for pos in noDataPos[::-1]:
                # insert new rows with float index positions
                df.loc[pos+0.3] = df['tstamp'][pos] + scale, float('nan'), float('nan')
                df.loc[pos+0.6] = df['tstamp'][pos + 1] - scale, float('nan'), float('nan')

                defect_x.extend([df['tstamp'][pos] - scale, df['tstamp'][pos],
                                 df['tstamp'][pos + 1], df['tstamp'][pos + 1] + scale])
                defect_y.extend([float('nan'), df['value'][pos], df['value'][pos + 1], float('nan'), ])

            # reset the index to integer
            df = df.sort_index().reset_index(drop=True)

            missing_data = pd.DataFrame({'defect_x': defect_x, 'defect_y': defect_y})

    return {'df': df, 'scale': scale, 'nan_in_data': nan_in_data,
            'missing_data': missing_data, 'has_preci': db_data['has_preci']}


def __get_scaling(df):
    """
    Make a list of the distance between the first ten datasets and return te smallest difference as scale.

    :param df: pandas dataframe
    :return:
    """
    scalelist = []

    testlength = df.shape[0] if df.shape[0] <= 10 else 10

    for row in range(1, testlength):
        scalelist.append(df['tstamp'][row] - df['tstamp'][row-1])
    return min(scalelist)


def __get_gap_position(df, scale, index):
    """
    Iterate over a dataset and find all positions where the distance between two rows is greater than the given scale.

    :param df:
    :param scale:
    :param index: string - name of the column of the dataframe that is to be checked for gaps
    :return: list - row(s) before the gap(s)
    """
    beforeGap = []
    datalength = df.shape[0]

    for row in range(1, datalength):
        if df[index][row] - df[index][row - 1] > scale:
            beforeGap.append(row - 1)
    return beforeGap


def precision_to_minmax(df):
    """
    Get a pandas dataframe with columns 'value', 'precision' or with 'avg', 'precmax', 'precavg' and calculate the min
    and max values for it, and add it to the dataframe.

    :param df: pandas dataframe 'value', 'precision' or with 'avg', 'precmax', 'precavg'
    :return: pandas dataframe + upper, lower, (upper_avg, lower_avg)
    """
    if 'value' in df.columns:
        df['upper'] = df['value'] + df['precision']
        df['lower'] = df['value'] - df['precision']
    elif 'avg' in df.columns:
        df['upper'] = df['avg'] + df['precmax']
        df['lower'] = df['acg'] - df['precmax']
        df['upper_avg'] = df['avg'] + df['precavg']
        df['lower_avg'] = df['acg'] - df['precavg']
    else:
        print('WARNING: there is a unknown dataset to convert precision in precision to minmax.')

    return df
