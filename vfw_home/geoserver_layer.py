"""

"""
import json
import logging
import requests
from django.core.cache import cache

from heron.settings import LOCAL_GEOSERVER, SECRET_GEOSERVER, DATABASES
from vfw_home.utilities import check_data_consistency

"""

"""
logger = logging.getLogger(__name__)


# TODO: Catch if there is no geoserver running at all. Not only here, but in view.py!
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
            "<name>{store}</name>"
            "<connectionParameters>"
            "<host>{host}</host>"
            "<port>{port}</port>"
            "<database>{dbname}</database>"
            "<user>{user}</user>"
            "<passwd>{passwd}</passwd>"
            "<dbtype>postgis</dbtype>"
            "</connectionParameters>"
            "<Parameter><name>Expose primary keys</name><value>true</value></Parameter>"
            "</dataStore>".format(
                store=store,
                host=DATABASES["default"]["HOST"],
                port=DATABASES["default"]["PORT"],
                dbname=DATABASES["default"]["NAME"],
                user=DATABASES["default"]["USER"],
                passwd=DATABASES["default"]["PASSWORD"],
            )
        )

        rest_url = f'{LOCAL_GEOSERVER}/rest/workspaces/{workspace}/datastores'
        rest_build = requests.post(
            rest_url,
            auth=eval(SECRET_GEOSERVER),
            data=datastore_xml,
            headers={"Content-type": "text/xml"},
        )
        if rest_build.status_code != 201:
            print(
                "\033[91mCannont build store: {}\033[0m".format(rest_build.status_code)
            )
            logger.warning(f'Cannot build new store in geoserver, {check.status_code}: {check.text}')

    # first check if workspace exists or try to build it if not:
    url = "{}/rest/workspaces/{}".format(LOCAL_GEOSERVER, workspace)
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
    else:
        url = f'{LOCAL_GEOSERVER}/rest/workspaces/{workspace}/datastores/{store}'
        check = requests.get(
            url, auth=eval(SECRET_GEOSERVER), headers={"Accept": "application/xml"}
        )
        if check.status_code != 200:  # if store doesn't exist build it
            logger.warning(f'datastore missing, trying to build it, {check.status_code}: {check.text}')
            # build new workspace:
            __build_store()
        # else:
        # print('store exist too: ', check.status_code)

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
            "\033[91m +++ Geoserver layer: "
            "Wrong database in use. Rename your store and workspace in views! {} != {}, +++\033[0m".format(DATABASES["default"]["NAME"] , contdict['database'])
        )
        __build_store()

def create_layer(
    request,
    filename: str,
    datastore: str,
    workspace: str,
    selection=None,
    srid: int = 4326,
    layertype: str = "point",
):
    """
    Create a layer in your GeoServer.

    :param selection:
    :param request:
    :type request:
    :param filename: Name of layer for Geoserver
    :param datastore: Name of datastore where to find the layer
    :param workspace: Name of workspace where to store the datastore
    :param srid:  The coordinate reference system according to the EPSG database for the new layer.
    :param layertype:  String defining the geo object. Default is point.
    """
    xml = __build_new_layer_xml(
        request, filename, datastore, workspace, srid, selection, layertype
    )
    url = f'{LOCAL_GEOSERVER}/rest/workspaces/{workspace}/datastores/{datastore}/featuretypes'

    build = requests.post(
        url, auth=eval(SECRET_GEOSERVER), data=xml, headers={"Content-type": "text/xml"}
    )
    if build.status_code != 201:
        logger.warning(f'{build.status_code}: {build.text}')
        print("create layer: ", str(build.status_code) + ": " + build.text)


def get_layer(filename: str, datastore: str, workspace: str) -> bool:
    """
    Load a layer from GeoServer

    :param filename: Name of layer for Geoserver.
    :param datastore: Name of store the layer is stored in.
    :param workspace: Name of workspace for the store.
    """
    url = f'{LOCAL_GEOSERVER}/rest/workspaces/{workspace}/datastores/{datastore}/featuretypes/{filename}'

    build = requests.get(
        url, auth=eval(SECRET_GEOSERVER), headers={"Accept": "application/xml"}
    )
    if build.status_code != 200:
        logger.warning("{}: {}".format(build.status_code, build.text))
        return False
    return True


def delete_layer(filename: str, datastore: str, workspace: str):
    """
    Delete a layer in GeoServer

    :param filename: Name of layer for Geoserver.
    :param datastore: Name of store the layer is stored in.
    :param workspace: Name of workspace for the store.
    """
    # first delete layer, then feature!
    url = "{}/rest/layers/{}".format(LOCAL_GEOSERVER, filename)
    build = requests.delete(
        url,
        auth=eval(SECRET_GEOSERVER),
        headers={"Content-type": "application/json", "Accept": "application/json"},
    )
    if build.status_code != 200:
        logger.warning("{}: {}".format(build.status_code, build.text))
        # logger.warning(str(build.status_code) + ': ' + build.text)

    url = "{}/rest/workspaces/{}/datastores/{}/featuretypes/{}".format(
        LOCAL_GEOSERVER, workspace, datastore, filename
    )
    build = requests.delete(
        url,
        auth=eval(SECRET_GEOSERVER),
        headers={"Content-type": "application/json", "Accept": "application/json"},
    )
    if build.status_code != 200:
        # logger.warning(str(build.status_code) + ': ' + build.text)
        logger.warning("{}: {}".format(build.status_code, build.text))


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


# TODO: Query needs 'WHERE' for the IDs of data available for user (isn't this already done in '__build_xml_from_id'?)
def __build_new_layer_xml(
    request, filename: str, datastore: str, workspace: str, srid: int, selection, layertype="point"
):
    """

    :param request:
    :type request:
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
    # query = 'SELECT ST_Transform(ST_FlipCoordinates(location), 4326) ::geometry as "Geometry", ' \
    if layertype == "point":
        keycolumn = "<keyColumn>id</keyColumn>"
        geometrytype = "Point"
        query = (
            'SELECT ST_Transform(location, 4326) ::geometry as "Geometry", '
            'title as "Beschreibung", name as "Datentyp", '
            'comment as "Kommentar", '
            'embargo as "Embargo", '
            'entries.id '
            'FROM entries LEFT JOIN variables on entries.variable_id = variables.id'
        )
        #  ' WHERE tbl_meta.public IS TRUE'  # only for test use on portal
        ids_without_data = cache.get('ids_without_data')
        if ids_without_data is None:
            ids_without_data = check_data_consistency()
            # cache.set('ids_without_data', ids_without_data, 3*60)

        if selection is None:
            query = f'{query} WHERE entries.id not in ({str(ids_without_data)[1:-1]})'
        else:
            selection = list(set(selection) - set(ids_without_data))
            query = f'{query} WHERE entries.id in ({str(selection)[1:-1]})'

        # if not request.user.is_authenticated:
        #     query = '{} {}'.format(query, ' WHERE embargo is false')  # only for test use on portal
        # attributes defined with name: [minOccurs, maxOccurs, nillable, binding]
        attribute_list = [
            ("Geometry", 0, 1, True, "point"),
            # ("GroupTypeName", 1, 1, False, "string"),
            ("Beschreibung", 1, 1, False, "string"),
            ("Datentyp", 1, 1, False, "string"),
            ("Kommentar", 0, 1, True, "string"),
            ("Embargo", 1, 1, False, "bool"),
        ]  # , ('id', 1, 1, False, 'int')]

    elif layertype == "filtercatchment":
        # simpleConversion = "<simpleConversionEnabled>false</simpleConversionEnabled>"
        geometrytype = "Polygon"
        selectstring = ""
        for i in selection:
            selectstring += f'(SELECT geom FROM cat_pfaf_merit_hydro_v07_basins_v01 WHERE comid={i}),'

        if len(selection) > 1:
            query = f'SELECT ST_Union(ARRAY[{selectstring[:-1]}])'
            # query = "SELECT ST_Union(ARRAY[{}]) as catchment".format(selectstring[:-1])
        else:
            query = selectstring[1:-2]
            # query = "{} as catchment".format(selectstring[1:-2])

        attribute_list = [
            ("geom", 0, 1, True, "polygon"),
        ]

    attributes = __create_attributes(attribute_list)
    xml = (
        "<featureType>"
        "<name>" + filename + "</name>"
        "<nativeName>" + filename + "</nativeName>"
        "<namespace>"
        "<name>" + workspace + "</name>"
        '<atom:link xmlns:atom="http://www.w3.org/2005/Atom" rel="alternate" href="'
        + LOCAL_GEOSERVER
        + "/rest/namespaces/"
        + workspace
        + '.xml" type="application/xml"/>'
        "</namespace>"
        "<title>" + filename + "</title>"
        "<keywords><string>features</string><string>"
        + filename
        + "</string></keywords>"
        "<nativeCRS>EPSG:" + str(srid) + "</nativeCRS>"
        "<srs>EPSG:"
        + str(srid)
        + "</srs><projectionPolicy>FORCE_DECLARED</projectionPolicy>"
        "<enabled>true</enabled>"
        "<metadata>"
        '<entry key="JDBC_VIRTUAL_TABLE">'
        "<virtualTable><name>" + filename + "</name>"
        "<sql>" + query + "</sql>"
        "<escapeSql>false</escapeSql>"
        + keycolumn
        + "<geometry><name>Geometry</name><type>" + geometrytype + "</type><srid>"
        + str(srid)
        + "</srid></geometry>"
        "</virtualTable>"
        "</entry>"
        "</metadata>"
        '<store class="dataStore"><name>' + workspace + ":" + datastore + "</name>"
        '<atom:link xmlns:atom="http://www.w3.org/2005/Atom" rel="alternate" href="'
        + LOCAL_GEOSERVER
        + "/rest/workspaces/"
        + workspace
        + "/datastores/"
        + datastore
        + '.xml" type="application/xml"/>'
        "</store>"
        "<maxFeatures>0</maxFeatures><numDecimals>0</numDecimals>"
        "<overridingServiceSRS>false</overridingServiceSRS>"
        "<skipNumberMatched>false</skipNumberMatched><circularArcPresent>false</circularArcPresent>"
        "<attributes>" + attributes + "</attributes>"
        "</featureType>"
    )
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
