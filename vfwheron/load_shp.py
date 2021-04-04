"""

"""

import os
from django.contrib.gis.utils import LayerMapping

# from vfwheron.models import Basiseinzugsgebiet
#
#
# """
# Simple code to populate database with data from shp file (with load_shp.run() in django shell)
# """
# Basiseinzugsgebiet_mapping = {
#     'objectid': 'OBJECTID',
#     'object_id': 'OBJECT_ID',
#     'fg_id': 'FG_ID',
#     'fgkz_nr': 'FGKZ_NR',
#     'langname': 'LANGNAME',
#     'area': 'FLAECHE',
#     'einzugsgeb': 'EINZUGSGEB',
#     'einzugsg00': 'EINZUGSG00',
#     'einzugsg01': 'EINZUGSG01',
#     'einzugsg02': 'EINZUGSG02',
#     'vor_fgkz_n': 'VOR_FGKZ_N',
#     'vor_fg_id': 'VOR_FG_ID',
#     'vor_fg_lan': 'VOR_FG_LAN',
#     'wasserkoer': 'WASSERKOER',
#     'wasserko00': 'WASSERKO00',
#     'aenderungs': 'AENDERUNGS',
#     'aenderun00': 'AENDERUN00',
#     'length': 'LENGTH',
#     'mod_by': 'MOD_BY',
#     'last_mod': 'LAST_MOD',
#     'se_anno_ca': 'SE_ANNO_CA',
#     'wasserko01': 'WASSERKO01',
#     'mpoly': 'MULTIPOLYGON',
#     }
#
# """
# GeoDjango-specific: a geometry field (MultiPolygonField)
# """
# Basiseinzugsgebiet_shp = os.path.abspath(
#         '/tmp/Basiseinzugsgebiet (AWGN)_polygon.shp'
#         )
#
#
# def run(path=Basiseinzugsgebiet_shp, verbose=True):
#     """
#
#     :param path:
#     :type path:
#     :param verbose:
#     :type verbose:
#     :return:
#     :rtype:
#     """
#     lm = LayerMapping(
#             Basiseinzugsgebiet, Basiseinzugsgebiet_shp, Basiseinzugsgebiet_mapping,
#             transform=False, encoding='iso-8859-1',
#             )
#     lm.save(strict=True, verbose=verbose)
