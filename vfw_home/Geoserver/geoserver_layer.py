"""

"""
import json
import logging
import requests
from django.core.cache import cache

from heron.settings import LOCAL_GEOSERVER, SECRET_GEOSERVER, DATABASES
from ..utilities.utilities import check_data_consistency
from django.conf import settings

"""

"""
logger = logging.getLogger(__name__)


def test_geoserver_env(store: str, workspace: str):
    """
    Function to test if the workspace and store to build the layers in exist. If not the function first tries to set up
    the new workspace in geoserver, and then in an inner function add the store with the login information for the
    database
    from the django settings.

    :param store:
    :param workspace:
    """

    def __build_store():
        """
        Inner function to build the data store
        """
        datastore_xml = (
            "<dataStore>"
            f"<name>{store}</name>"
            "<connectionParameters>"
            f"<host>{DATABASES['yourhost']}</host>"
            f"<port>{DATABASES['yourport']}</port>"
            f"<database>{DATABASES['yourdatabase']}</database>"
            f"<user>{DATABASES['youruser']}</user>"
            f"<passwd>{DATABASES['yourpassword']}</passwd>"
            "<dbtype>postgis</dbtype>"
            "</connectionParameters>"
            "<Parameter><name>Expose primary keys</name><value>true</value></Parameter>"
            "</dataStore>"
        )

        rest_url = f'{LOCAL_GEOSERVER}/rest/workspaces/{workspace}/datastores'
        rest_build = requests.post(
            rest_url,
            auth=eval(SECRET_GEOSERVER),
            data=datastore_xml,
            headers={"Content-type": "text/xml"},
        )
        if rest_build.status_code != 201:
            print(f"\033[91mCannont build store: {rest_build.status_code}\033[0m")
            logger.warning(f'Cannot build new store in geoserver, {check.status_code}: {check.text}')

    # first check if workspace exists or try to build it if not:
    url = f"{LOCAL_GEOSERVER}/rest/workspaces/{workspace}"
    check = requests.get(
        url, auth=eval(SECRET_GEOSERVER), headers={"Accept": "application/xml"}
    )
    if check.status_code != 200:  # if workspace doesn't exist build it
        logger.warning(f'workspace missing, trying to build it, {check.status_code}: {check.text}')
        # build new workspace:
        url = f'{LOCAL_GEOSERVER}/rest/workspaces'
        xml = f'<workspace><name>{workspace}</name></workspace>'
        build = requests.post(
            url,
            auth=eval(SECRET_GEOSERVER),
            data=xml,
            headers={"Content-type": "text/xml"},
        )
        if build.status_code != 201:
            print(f'Cannot build new workspace in geoserver, {check.status_code}: {check.text}')
            logger.warning(f'Cannot build new workspace in geoserver, {check.status_code}: {check.text}')
        else:
            url = f'{LOCAL_GEOSERVER}/rest/workspaces/{workspace}'
            check = requests.get(
                url, auth=eval(SECRET_GEOSERVER), headers={"Accept": "application/xml"}
            )
            __build_store()
    else:  # if workspace exists, check if datastore exists or build it if not
        url = f'{LOCAL_GEOSERVER}/rest/workspaces/{workspace}/datastores/{store}'
        check = requests.get(
            url, auth=eval(SECRET_GEOSERVER), headers={"Accept": "application/xml"}
        )
        if check.status_code != 200:  # if store doesn't exist build it
            logger.warning(f'datastore missing, trying to build it, {check.status_code}: {check.text}')
            # build new store:
            __build_store()

    # Now we know we have a workspace and store we can test if these access the right database
    url = f'{LOCAL_GEOSERVER}/rest/workspaces/{workspace}/datastores/{store}'
    check = requests.get(
        url, auth=eval(SECRET_GEOSERVER), headers={"Accept": "application/json"}
    )
    content = json.loads(check.content)
    contlist = content['dataStore']['connectionParameters']['entry']

    contdict = {}
    for item in contlist:
        contdict[item['@key']] = item['$']
    if DATABASES["default"]["NAME"] != contdict['database'] and \
        DATABASES["default"]["NAME"].replace("-", "") != contdict['database'].replace("-", "") and \
        DATABASES["default"]["NAME"].replace("_", "") != contdict['database'].replace("_", ""):
        print(
            '\033[91m +++ Geoserver layer: Wrong database in use. Rename your store and workspace in views! '
            f'{DATABASES["default"]["NAME"]} != {contdict["database"]}, +++\033[0m'
        )
        logger.warning(f'Unexcpected database for GeoServer. Rename your store and workspace in views to update your'
                       f'Geoserver files. '
                       f'Database in use: {contdict["database"]}. Database expected: {DATABASES["default"]["NAME"]}')
        __build_store()



def create_layer(request: object, filename: str, datastore: str, workspace: str, selection: object = None, srid: int = 4326,
                 layertype: str = "point", ) -> object:
    """
    Create a layer in your GeoServer.

    :param selection:
    :param request: No use for this yet. Maybe some time...
    :type request:
    :param filename: Name of layer for Geoserver
    :param datastore: Name of datastore where to find the layer
    :param workspace: Name of workspace where to store the datastore
    :param srid:  The coordinate reference system according to the EPSG database for the new layer.
    :param layertype:  String defining the geo object. Default is "point". Other are "areal_data", "filtercatchment",
    "merit_catchment_coarse", "merit_catchment", "merit_river", "merit_river_simple"
    """

    xml = __build_layer_xml(request, filename, datastore, workspace, srid, selection, layertype)

    url = f'{LOCAL_GEOSERVER}/rest/workspaces/{workspace}/datastores/{datastore}/featuretypes'

    build = requests.post(
        url, auth=eval(SECRET_GEOSERVER), data=xml, headers={"Content-type": "text/xml"}
    )
    if build.status_code != 201:
        logger.warning(f'{build.status_code}: {build.text}')
        # print("create layer: ", str(build.status_code) + ": " + build.text)


def delete_layer(filename: str, datastore: str, workspace: str):
    """
    Delete a layer in GeoServer

    :param filename: Name of layer for Geoserver.
    :param datastore: Name of store the layer is stored in.
    :param workspace: Name of workspace for the store.
    """
    def delete_request(url):
        build = requests.delete(
            url,
            auth=eval(SECRET_GEOSERVER),
            headers={"Content-type": "application/json", "Accept": "application/json"},
        )
        if build.status_code != 200:
            # print("delete layer: ", str(build.status_code) + ": " + build.text)
            logger.warning(f"{build.status_code}: {build.text}")

    # first delete layer, then feature!
    delete_request(f"{LOCAL_GEOSERVER}/rest/layers/{filename}")
    delete_request(f"{LOCAL_GEOSERVER}/rest/workspaces/{workspace}/datastores/{datastore}/featuretypes/{filename}")


def get_layer(layer_name: str, datastore: str, workspace: str, format: str='json') -> bool:
    """
    Load a layer from GeoServer

    :rtype: object
    :param layer_name: Name of layer for Geoserver.
    :param datastore: Name of store the layer is stored in.
    :param workspace: Name of workspace for the store.
    :param workspace: Format of result can be 'json' (default) or 'xml', yet.
    """

    match format.lower():
        case 'json':
            url = f'{LOCAL_GEOSERVER}/rest/workspaces/{workspace}/datastores/{datastore}/featuretypes/{layer_name}.json'
        case 'xml':
            url = f'{LOCAL_GEOSERVER}/rest/workspaces/{workspace}/datastores/{datastore}/featuretypes/{layer_name}.xml'
        case _:
            raise ValueError("Unexpected parameter value in get_layer()")

    build = requests.get(
        url, auth=eval(SECRET_GEOSERVER), headers={"Accept": "application/xml"}
    )
    if build.status_code != 200:
        # print(f'error getting layer {build.status_code} {build.text}')
        logger.warning("{}: {}".format(build.status_code, build.text))
        return False
    return True


def has_layer(layer_name: str, datastore: str, workspace: str) -> bool:
    """
    Load a layer status from GeoServer

    :rtype: object
    :param layer_name: Name of layer for Geoserver.
    :param datastore: Name of store the layer is stored in.
    :param workspace: Name of workspace for the store.
    """
    url = f'{LOCAL_GEOSERVER}/rest/workspaces/{workspace}/datastores/{datastore}/featuretypes/{layer_name}'

    build = requests.get(
        url, auth=eval(SECRET_GEOSERVER), headers={"Accept": "application/xml"}
    )
    if build.status_code != 200:
        # print(f'error finding layer {build.status_code} {build.text}')
        logger.warning("{}: {}".format(build.status_code, build.text))
        return False
    return True


def __create_attributes(attributes_list):
    """
    Create valid xml attribute list to get data from Geoserver.

    :param attributes_list:
    :return:
    """
    attributes = ""
    binding_dict = {
        "bigDeci": "java.math.BigDecimal",
        "bool": "java.lang.Boolean",
        "date": "java.sql.Date",
        "int": "java.lang.Integer",
        "point": "com.vividsolutions.jts.geom.Point",
        "polygon": "org.locationtech.jts.geom.Polygon",
        "MultiPolygon": "org.locationtech.jts.geom.MultiPolygon",
        "MultiLine": "org.locationtech.jts.geom.MultiLineString",
        "string": "java.lang.String",
        "time": "java.sql.Time",
    }

    for element in attributes_list:
        attribute = (
            '<attribute>'
            f'<name>{element[0]}</name>'
            f'<minOccurs>{str(element[1])}</minOccurs>'
            f'<maxOccurs>{str(element[2])}</maxOccurs>'
            f'<nillable>{str(element[3]).lower()}</nillable>'
            f'<binding>{binding_dict[element[4]]}</binding>'
            '</attribute>'
        )

        attributes += attribute

    return attributes


def __build_catchment_layer_xml(request, filename, datastore, workspace, srid, selection, layertype):
    pass


def __get_selectables_query(selection):
    ids_without_data = cache.get('ids_without_data')
    if ids_without_data is None:
        ids_without_data = check_data_consistency()
    if selection is None:
        selection = []

    selectable_data = tuple(set(selection) - set(ids_without_data))
    if len(selectable_data) == 0:
        where_clause = f'entries.id not in {tuple(ids_without_data)}'
    elif len(selectable_data) > 1:
        where_clause = f'entries.id in {selectable_data}'
    else:
        where_clause = f'entries.id = {selectable_data[0]}'
    return where_clause


def __build_layer_xml(
    request, filename: str, datastore: str, workspace: str, srid: int, selection, layertype="point"
):
    """
    Build XML to create a layer through the rest API of Geoserver.

    :param request: Might be used some time to connect layers to users
    :param filename: Name of layer for Geoserver.
    :param datastore: Name of store the layer is stored in.
    :param workspace: Name of workspace for the store.
    :param srid:  The coordinate reference system according to the EPSG database for the new layer.
    :param selection:
    :param layertype: string - for now there is "point" (default) and "filtercatchment"
    :return:
    :rtype:
    """
    # layer specific data
    simpleConversion = ""
    keycolumn = ""

    # attributes have to be defined according to the selected table columns in the query
    match layertype:
        case "point":
            keycolumn = "<keyColumn>id</keyColumn>"
            geometrytype = "Point"

            query = (
                'SELECT ST_Transform(locations.point_location, 4326) ::geometry as "Geometry", '
                'entries.title as "Beschreibung", '
                'variables.name as "Datentyp", '
                'entries.comment as "Kommentar", '
                'entries.embargo as "Embargo", '
                'entries.id '
                'FROM entries LEFT JOIN variables on entries.variable_id = variables.id '
                'LEFT JOIN locations ON entries.id = locations.id'
            )
            query = f'{query} WHERE {__get_selectables_query(selection)}'

            attribute_list = [
                ("Geometry", 0, 1, True, "point"),
                ("Beschreibung", 1, 1, False, "string"),
                ("Datentyp", 1, 1, False, "string"),
                ("Kommentar", 0, 1, True, "string"),
                ("Embargo", 1, 1, False, "bool"),
            ]  # , ('id', 1, 1, False, 'int')]


        case "areal_data":
            keycolumn = ""
            geometrytype = "MultiPolygon"

            query = (
                'SELECT ST_GeometryType(locations.geom) as "FeatureType",'
                'ST_Transform(locations.geom, 4326) ::geometry as "Geometry", '
                'entries.title as "Beschreibung", '
                'variables.name as "Datentyp", '
                'entries.comment as "Kommentar", '
                'entries.embargo as "Embargo", '
                'entries.id '
                'FROM entries LEFT JOIN variables on entries.variable_id = variables.id '
                'LEFT JOIN locations ON entries.id = locations.id '
                'WHERE locations.area_sqm > 0'
            )
            query = f'{query} AND {__get_selectables_query(selection)}'
            attribute_list = [
                ("Geometry", 0, 1, True, geometrytype),
                ("Beschreibung", 1, 1, False, "string"),
                ("Datentyp", 1, 1, False, "string"),
                ("Kommentar", 0, 1, True, "string"),
                ("Embargo", 1, 1, False, "bool"),
                ('id', 1, 1, False, 'int')
            ]
        case "filtercatchment":
            geometrytype = "Polygon"
            selectstring = ""

            if len(selection) > 1:
                query = f'SELECT ST_Union(ARRAY[{tuple(*zip(*selection))}])'
            else:
                query = f'SELECT geom FROM cat_pfaf_merit_hydro_v07_basins_v01 WHERE comid={selection[0]}'

            attribute_list = [
                ("geom", 0, 1, True, "polygon"),
            ]
        case "merit_catchment_coarse":
            keycolumn = "<keyColumn>basin</keyColumn>"
            geometrytype = "MultiPolygon"
            query = ('SELECT basin, geom FROM merit_hydro_vect_level2')
            attribute_list = [
                ("geom", 0, 1, True, geometrytype),
            ]
        case "merit_catchment":
            keycolumn = ""
            geometrytype = "MultiPolygon"
            query = ('SELECT geom, comid FROM cat_pfaf_merit_hydro_v07_basins_v01')
            attribute_list = [
                ("comid", 0, 1, True, 'int'),
                ("geom", 0, 1, True, geometrytype),
            ]
        case "merit_river":
            keycolumn = ""
            geometrytype = "MultiLine"
            query = ('SELECT comid, up1, up2, up3, up4, geom FROM riv_pfaf_merit_hydro_v07_basins_v01 WHERE up1 != 0')
            attribute_list = [
                ("comid", 0, 1, False, "int"),
                ("up1", 0, 1, False, "int"),
                ("up2", 0, 1, False, "int"),
                ("up3", 0, 1, False, "int"),
                ("up4", 0, 1, False, "int"),
                ("geom", 0, 1, False, geometrytype),
            ]
        case "merit_river_simple":
            keycolumn = ""
            geometrytype = "MultiLine"
            query = ('SELECT comid, up1, up2, up3, up4, ST_Simplify(geom, 100) AS geom '
                     'FROM riv_pfaf_merit_hydro_v07_basins_v01')
            attribute_list = [
                ("comid", 0, 1, False, "int"),
                ("up1", 0, 1, False, "int"),
                ("up2", 0, 1, False, "int"),
                ("up3", 0, 1, False, "int"),
                ("up4", 0, 1, False, "int"),
                ("geom", 0, 1, False, geometrytype),
            ]
        case _:
            # print(f'unknown layertype: {layertype}')
            logger.warning(f"unknown layertype: {layertype}")
            return

    attributes = __create_attributes(attribute_list)
    xml = (
        '<featureType>'
        f'<name>{filename}</name>'
        f'<nativeName>{filename}</nativeName>'
        '<namespace>'
        f'<name>{workspace}</name>'
        f'<atom:link xmlns:atom="http://www.w3.org/2005/Atom" rel="alternate" '
        f'href="{LOCAL_GEOSERVER}/rest/namespaces/{workspace}.xml" type="application/xml"/>'
        '</namespace>'
        f'<title>{filename}</title>'
        f'<keywords><string>features</string><string>{filename}</string></keywords>'
        f'<nativeCRS>EPSG:{str(srid)}</nativeCRS>'
        f'<srs>EPSG:{str(srid)}</srs>'
        '<projectionPolicy>FORCE_DECLARED</projectionPolicy>'
        '<enabled>true</enabled>'
        '<metadata>'
        '<entry key="JDBC_VIRTUAL_TABLE">'
        f'<virtualTable><name>{filename}</name>'
        f'<sql>{query}</sql>'
        '<escapeSql>false</escapeSql>'
        f'{keycolumn}'
        f'<geometry><name>Geometry</name><type>{geometrytype}</type>'
        f'<srid>{str(srid)}</srid>'
        '</geometry>'
        '</virtualTable>'
        '</entry>'
        '</metadata>'
        f'<store class="dataStore"><name>{workspace}:{datastore}</name>'
        '<atom:link xmlns:atom="http://www.w3.org/2005/Atom" rel="alternate" '
        f'href="{LOCAL_GEOSERVER}/rest/workspaces/{workspace}/datastores/{datastore}.xml" type="application/xml"/>'
        '</store>'
        '<maxFeatures>0</maxFeatures><numDecimals>0</numDecimals>'
        '<overridingServiceSRS>false</overridingServiceSRS>'
        '<skipNumberMatched>false</skipNumberMatched><circularArcPresent>false</circularArcPresent>'
        f'<attributes>{attributes}</attributes>'
        "</featureType>"
    )

    return xml


def verify_layer(request, filename, datastore, workspace, layertype="point"):
    """
    This method verifies the existence of a layer in Geoserver. If the layer does not exist, it creates it.
    If the layer already exists, it deletes it and then creates it again.

    To delete and recreate the layer is only for development, to make sure geoserver always uses the most
    recent data. The production version needs a different implementation of that.

    :param request: The HTTP request object.
    :param filename: The name of the layer file.
    :param datastore: The name of the data store.
    :param workspace: The name of the workspace.
    :param layertype: The type of the layer (default is "point").
    :return: None
    """

    if not has_layer(layer_name=filename, datastore=datastore, workspace=workspace):
        create_layer(request=request, filename=filename, datastore=datastore, workspace=workspace,
                     layertype=layertype)
    else:
        delete_layer(filename=filename, datastore=datastore, workspace=workspace)
        create_layer(request=request, filename=filename, datastore=datastore, workspace=workspace,
                     layertype=layertype)
