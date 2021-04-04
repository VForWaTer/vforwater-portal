# TODO @Marcus: this file should work as manager in models.py
"""

"""
import re

from django.contrib.gis.db.models.aggregates import Extent
from django.db import connections
import logging

from vfwheron.models import Entries

logger = logging.getLogger(__name__)


def get_bbox_from_data(*args):
    """
    Get geometry of bbox for available data in the style: [xmin, ymin, xmax, ymax].

    :param args: Ids inside the bounding box
    :type args: list
    :return: list
    """
    try:
        if args:
            bounds = Entries.objects.filter(pk__in=args[0]).aggregate(Extent('location'))
        else:
            bounds = Entries.objects.all().aggregate(Extent('location'))
    except TypeError as ex:
        print('\033[91m Exeption in loading bbox: {}\033[0m'.format(ex))
        logger.warning('\033[91m Data Extend cannot be loaded in query_functions.py. Using fixed values.\033[0m')
        bounds = {'location__extent': [11.221124, 52.08632, 11.222354, 52.086891]}

    return list(bounds['location__extent'])

