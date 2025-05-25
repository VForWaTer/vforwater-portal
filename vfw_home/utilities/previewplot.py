"""

"""
import ast
from datetime import time
from math import radians, ceil, sqrt

from django.utils.translation import gettext
from bokeh.io import show
from bokeh.layouts import column
from bokeh.models import Band, DatetimeTickFormatter, HoverTool, Range1d, CustomJS, ColumnDataSource, \
    DateSlider, DateRangeSlider, Whisker, BoxAnnotation
from bokeh.transform import linear_cmap
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.palettes import Oranges9, Spectral11

from numpy import mean

from heron.settings import MAX_SIZE_PREVIEW_PLOT
from vfw_home.data_tools import DB_load_directiondata
from vfw_home.models import Entries

import redis
try:
    from heron.settings import REDIS_HOST
except:
    REDIS_HOST = 'localhost'
try:
    from heron.settings import REDIS_PORT
except:
    REDIS_PORT = 6379
try:
    from heron.settings import REDIS_DB
except:
    REDIS_DB = 0

import logging

import pandas as pd
import time

from wps_gui.models import WpsResults

logger = logging.getLogger(__name__)

