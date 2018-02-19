import base64
from io import BytesIO
from django.db import connections
from django.http import request

from vfwheron.models import TblMeta

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


def maelicke_plot():
    preview = request.GET.get('preview')
    label = TblMeta.objects.filter(id=preview).values_list('variable__variable_name',
                                                           'variable__variable_symbol', 'variable__unit__unit_abbrev')
    ylabel = label[0][0] + ' (' + label[0][1] + ')' + ' [' + label[0][2] + ']'

    # connect to database
    cursor = connections['vforwater'].cursor()
    cursor.execute(
        'SELECT tbl_data.tstamp, tbl_data.value FROM public.tbl_data WHERE tbl_data.meta_id = %s' % preview)
    m = cursor.fetchall()
    cursor.close()

    # create image
    fig, ax = plt.subplots(1, 1, figsize=(6, 4))
    ax.plot([row[0] for row in m], [row[1] for row in m], '-b', lw=2)
    fig.autofmt_xdate(),
    ax.set_xlabel('Date')
    ax.grid(which='major', axis='x')
    ax.set_ylabel(ylabel)
    ax.set_title('Dataset preview')

    # create tempfile and read as base64
    tmpFile = BytesIO()
    fig.savefig(tmpFile, format='png')
    tmpFile.seek(0)
    b64 = base64.b64encode(tmpFile.getvalue())

    # create the image-tag
    imgtag = "<img alt='data image' src='data:image/png;base64,%s'>" % b64.decode('utf8')
    return imgtag