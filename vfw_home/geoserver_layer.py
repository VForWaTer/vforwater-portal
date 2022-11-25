"""

"""
import json
import logging
import requests
from heron.settings import LOCAL_GEOSERVER, SECRET_GEOSERVER, DATABASES

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

        rest_url = "{}/rest/workspaces/{}/datastores".format(LOCAL_GEOSERVER, workspace)
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
            logger.warning(
                "Cannot build new store in geoserver, {}: {}".format(
                    check.status_code, check.text
                )
            )

    # first check if workspace exists or try to build it if not:
    url = "{}/rest/workspaces/{}".format(LOCAL_GEOSERVER, workspace)
    check = requests.get(
        url, auth=eval(SECRET_GEOSERVER), headers={"Accept": "application/xml"}
    )
    if check.status_code != 200:  # if workspace doesn't exist build it
        logger.warning(
            "workspace missing, trying to build it, {}: {}".format(
                check.status_code, check.text
            )
        )
        # build new workspace:
        url = "{}/rest/workspaces".format(LOCAL_GEOSERVER)
        xml = "<workspace><name>{}</name></workspace>".format(workspace)
        build = requests.post(
            url,
            auth=eval(SECRET_GEOSERVER),
            data=xml,
            headers={"Content-type": "text/xml"},
        )
        if build.status_code != 201:
            print(
                "Cannot build new workspace in geoserver, {}: {}".format(
                    check.status_code, check.text
                )
            )
            logger.warning(
                "Cannot build new workspace in geoserver, {}: {}".format(
                    check.status_code, check.text
                )
            )
        else:
            url = "{}/rest/workspaces/{}".format(LOCAL_GEOSERVER, workspace)
            check = requests.get(
                url, auth=eval(SECRET_GEOSERVER), headers={"Accept": "application/xml"}
            )
            __build_store()
    else:
        url = "{}/rest/workspaces/{}/datastores/{}".format(
            LOCAL_GEOSERVER, workspace, store
        )
        check = requests.get(
            url, auth=eval(SECRET_GEOSERVER), headers={"Accept": "application/xml"}
        )
        if check.status_code != 200:  # if store doesn't exist build it
            logger.warning(
                "datastore missing, trying to build it, {}: {}".format(
                    check.status_code, check.text
                )
            )
            # build new workspace:
            __build_store()
        # else:
        # print('store exist too: ', check.status_code)

    # Now we know we have a workspace and store we can test if these access the right database
    url = "{}/rest/workspaces/{}/datastores/{}".format(
        LOCAL_GEOSERVER, workspace, store
    )
    check = requests.get(
        url, auth=eval(SECRET_GEOSERVER), headers={"Accept": "application/json"}
    )
    content = json.loads(check.content)
    if (
        DATABASES["default"]["NAME"]
        != content["dataStore"]["connectionParameters"]["entry"][0]["$"]
    ):
        print(
            "\033[91m +++ Geoserver layer: "
            "Wrong database in use. Rename your store and workspace in views! +++\033[0m"
        )
        __build_store()


def create_layer(
    request,
    filename: str,
    datastore: str,
    workspace: str,
    selection=None,
    srid: int = 4326,
):
    """

    :param selection:
    :param request:
    :type request:
    :param filename: Name of layer for Geoserver
    :param datastore: Name of datastore where to find the layer
    :param workspace: Name of workspace where to store the datastore
    :param srid:  The coordinate reference system according to the EPSG database for the new layer.
    """
    xml = __build_new_layer_xml(
        request, filename, datastore, workspace, srid, selection
    )
    url = "{}/rest/workspaces/{}/datastores/{}/featuretypes".format(
        LOCAL_GEOSERVER, workspace, datastore
    )
    build = requests.post(
        url, auth=eval(SECRET_GEOSERVER), data=xml, headers={"Content-type": "text/xml"}
    )
    if build.status_code != 201:
        logger.warning("{}: {}".format(build.status_code, build.text))
        print("create layer: ", str(build.status_code) + ": " + build.text)


def get_layer(filename: str, datastore: str, workspace: str) -> bool:
    """
    Load a layer from GeoServer

    :param filename: Name of layer for Geoserver.
    :param datastore: Name of store the layer is stored in.
    :param workspace: Name of workspace for the store.
    """
    url = "{}/rest/workspaces/{}/datastores/{}/featuretypes/{}".format(
        LOCAL_GEOSERVER, workspace, datastore, filename
    )
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
        "string": "java.lang.String",
        "time": "java.sql.Time",
    }

    for element in attributes_list:
        attribute = (
            "<attribute>"
            "<name>" + element[0] + "</name>"
            "<minOccurs>" + str(element[1]) + "</minOccurs>"
            "<maxOccurs>" + str(element[2]) + "</maxOccurs>"
            "<nillable>" + str(element[3]).lower() + "</nillable>"
            "<binding>" + binding_dict[element[4]] + "</binding>"
            "</attribute>"
        )

        attributes += attribute

    return attributes


# TODO: Query needs 'WHERE' for the IDs of data available for user (isn't this already done in '__build_xml_from_id'?)
def __build_new_layer_xml(
    request, filename: str, datastore: str, workspace: str, srid: int, selection
):
    """

    :param selection:
    :param request:
    :type request:
    :param filename: Name of layer for Geoserver.
    :param datastore: Name of store the layer is stored in.
    :param workspace: Name of workspace for the store.
    :param srid:  The coordinate reference system according to the EPSG database for the new layer.
    :return:
    :rtype:
    """
    # attributes have to be defined according to the selected table columns in the query
    query = (
        'SELECT ST_Transform(location, 4326) ::geometry as "Geometry", '
        'title as "Beschreibung", name as "Datentyp", '
        'comment as "Kommentar", '
        'embargo as "Embargo", '
        "entries.id "
        "FROM entries LEFT JOIN variables on entries.variable_id = variables.id"
    )
    if selection is not None:
        query = f'{query} WHERE entries.id in ({selection})'
    attribute_list = [
        ("Geometry", 0, 1, True, "point"),
        ("Beschreibung", 1, 1, False, "string"),
        ("Datentyp", 1, 1, False, "string"),
        ("Kommentar", 0, 1, True, "string"),
        ("Embargo", 1, 1, False, "bool"),
    ]  # , ('id', 1, 1, False, 'int')]

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
        "<keyColumn>id</keyColumn>"
        "<geometry><name>Geometry</name><type>Point</type><srid>"
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

    return xml
