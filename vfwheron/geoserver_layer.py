"""

"""

import logging
import requests
from heron.settings import LOCAL_GEOSERVER, SECRET_GEOSERVER, DATABASES

"""

"""
logger = logging.getLogger(__name__)


# TODO: Catch if there is no geoserver running at all. Not only here, but in view.py!
def test_geoserver_env(store, workspace):
    """
    Function to test if the workspace and store to build the layers in exist. If not the function first tries to set up
    the new workspace in geoserver, and then in an inner function add the store with the login information for the database
    from the django settings.

    :param store:
    :type store:
    :param workspace:
    :type workspace:
    :return:
    :rtype:
    """
    def build_store():
        """
        Inner function to build the data store
        """
        datastore_xml = '<dataStore>' \
                        '<name>{}</name>' \
                        '<type>PostGIS</type>' \
                        '<connectionParameters>' \
                        '<host>{}</host>' \
                        '<port>{}</port>' \
                        '<database>{}</database>' \
                        '<user>{}</user>' \
                        '<passwd>{}</passwd>' \
                        '<dbtype>postgis</dbtype>' \
                        '</connectionParameters>' \
                        '</dataStore>'.format(store, DATABASES['vforwater']['HOST'],
                                              DATABASES['vforwater']['PORT'], DATABASES['vforwater']['NAME'],
                                              DATABASES['vforwater']['USER'], DATABASES['vforwater']['PASSWORD'])
        url = '{}/rest/workspaces/{}/datastores'.format(LOCAL_GEOSERVER, workspace)
        build = requests.post(url, auth=(eval(SECRET_GEOSERVER)), data=datastore_xml,
                              headers={'Content-type': 'text/xml'})
        if build.status_code != 201:
            logger.warning('Cannot build new store in geoserver, {}: {}'.format(check.status_code, check.text))

    # first check if workspace exists or try to build it if not:
    url = '{}/rest/workspaces/{}'.format(LOCAL_GEOSERVER, workspace)
    check = requests.get(url, auth=(eval(SECRET_GEOSERVER)), headers={"Accept": "application/xml"})
    if check.status_code != 200:  # if workspace doesn't exist build it
        logger.warning('workspace missing, trying to build it, {}: {}'.format(check.status_code, check.text))
        # build new workspace:
        url = '{}/rest/workspaces'.format(LOCAL_GEOSERVER)
        xml = '<workspace><name>{}</name></workspace>'.format(workspace)
        build = requests.post(url, auth=(eval(SECRET_GEOSERVER)), data=xml, headers={'Content-type': 'text/xml'})
        if build.status_code != 201:
            logger.warning('Cannot build new workspace in geoserver, {}: {}'.format(check.status_code, check.text))
        else:
            build_store()
    #
    else:
        url = '{}/rest/workspaces/{}/datastores/{}'.format(LOCAL_GEOSERVER, workspace, store)
        check = requests.get(url, auth=(eval(SECRET_GEOSERVER)), headers={"Accept": "application/xml"})
        if check.status_code != 200:  # if store doesn't exist build it
            logger.warning('datastore missing, trying to build it, {}: {}'.format(check.status_code, check.text))
            # build new workspace:
            build_store()




# TODO: IDs for new layer (for user) are still missing
def create_layer(request, filename, datastore, workspace, srid=3857):
    """

    :param request:
    :type request:
    :param filename:
    :type filename:
    :param datastore:
    :type datastore:
    :param workspace:
    :type workspace:
    :param srid:
    :type srid:
    :return:
    :rtype:
    """
    xml = build_new_layer_xml(request, filename, datastore, workspace, srid)
    url = '{}/rest/workspaces/{}/datastores/{}/featuretypes'.format(LOCAL_GEOSERVER, workspace, datastore)
    build = requests.post(url, auth=(eval(SECRET_GEOSERVER)), data=xml, headers={'Content-type': 'text/xml'})
    if build.status_code != 201:
        logger.warning('{}: {}'.format(build.status_code, build.text))
        # print('create layer: ', str(build.status_code) + ': ' + build.text)


def get_layer(filename, datastore, workspace):
    """

    :param filename:
    :type filename:
    :param datastore:
    :type datastore:
    :param workspace:
    :type workspace:
    :return:
    :rtype:
    """
    url = '{}/rest/workspaces/{}/datastores/{}/featuretypes/{}'.format(LOCAL_GEOSERVER, workspace, datastore, filename)
    # url = LOCAL_GEOSERVER + '/rest/workspaces/' + workspace + '/datastores/' + datastore + '/featuretypes/' + filename
    build = requests.get(url, auth=(eval(SECRET_GEOSERVER)), headers={"Accept": "application/xml"})
    if build.status_code != 200:
        logger.warning('{}: {}'.format(build.status_code, build.text))
        # print('get layer (if): ', str(build.status_code) + ': ' + build.text)
        return False
    # print('get layer: ', str(build.status_code) + ': ' + build.text)
    return True


def delete_layer(filename, datastore, workspace):
    """

    :param filename:
    :type filename:
    :param datastore:
    :type datastore:
    :param workspace:
    :type workspace:
    :return:
    :rtype:
    """
    # first delete layer, then feature!
    url = '{}/rest/layers/{}'.format(LOCAL_GEOSERVER, filename)
    build = requests.delete(url, auth=(eval(SECRET_GEOSERVER)),
                            headers={'Content-type': 'application/json', 'Accept': 'application/json'})
    if build.status_code != 200:
        logger.warning('{}: {}'.format(build.status_code, build.text))
        # logger.warning(str(build.status_code) + ': ' + build.text)

    url = '{}/rest/workspaces/{}/datastores/{}/featuretypes/{}'.format(LOCAL_GEOSERVER, workspace, datastore, filename)
    # url = LOCAL_GEOSERVER + '/rest/workspaces/' + workspace + '/datastores/' + datastore + '/featuretypes/' + filename
    build = requests.delete(url, auth=(eval(SECRET_GEOSERVER)),
                            headers={'Content-type': 'application/json', 'Accept': 'application/json'})
    if build.status_code != 200:
        # logger.warning(str(build.status_code) + ': ' + build.text)
        logger.warning('{}: {}'.format(build.status_code, build.text))


# TODO: Query needs 'WHERE' for the IDs of data available for user (isn't this already done in 'build_XML_from_ID'?)
def build_new_layer_xml(request, filename, datastore, workspace, srid):
    """

    :param request:
    :type request:
    :param filename:
    :type filename:
    :param datastore:
    :type datastore:
    :param workspace:
    :type workspace:
    :param srid:
    :type srid:
    :return:
    :rtype:
    """
    # attributes have to be defined according to the selected table columns in the query
    query = 'SELECT ST_Transform(ST_SetSRID(ST_Point(ST_X(geom), ST_Y(geom)), srid), 3857) ::geometry' \
            ' as "Geometry",' \
            ' tbl_variable.variable_name AS "Datentyp",' \
            ' tbl_meta.spacing AS "Schrittweite",' \
            ' lt_site.landuse AS "Landnutzung",' \
            ' lt_soil.geology AS "Geologie",' \
            ' lt_user.first_name AS "Vorname",' \
            ' lt_user.last_name AS "Nachname",' \
            ' lt_user.institution_name AS "Institut",' \
            ' lt_user.department AS "Abteilung",' \
            ' lt_project.project_name AS "Projekt",' \
            ' lt_domain.domain_name AS "Dom&#228;ne",' \
            ' tbl_meta.comment AS "Kommentar",' \
            ' lt_license.license_abbrev AS "Lizenz",' \
            ' lt_license.text_url AS "Lizenz_URL",' \
            ' tbl_meta.id,' \
            ' tbl_meta.site_id,' \
            ' tbl_meta.external_id,' \
            ' lt_location.centroid_x,' \
            ' lt_location.centroid_y,' \
            ' lt_location.srid,' \
            ' lt_location.geometry_type,' \
            ' lt_location.geom' \
            ' FROM tbl_meta' \
            ' LEFT JOIN nm_meta_domain ON tbl_meta.id = nm_meta_domain.meta_id' \
            ' LEFT JOIN lt_domain ON nm_meta_domain.domain_id = lt_domain.id' \
            ' LEFT JOIN lt_project ON lt_domain.project_id = lt_project.id' \
            ' LEFT JOIN lt_user ON tbl_meta.publisher_id = lt_user.id' \
            ' LEFT JOIN tbl_data_source ON tbl_meta.source_id = tbl_data_source.id' \
            ' LEFT JOIN lt_source_type ON tbl_data_source.source_type_id = lt_source_type.id' \
            ' LEFT JOIN lt_site ON tbl_meta.site_id = lt_site.id' \
            ' LEFT JOIN lt_soil ON tbl_meta.soil_id = lt_soil.id' \
            ' LEFT JOIN lt_license ON tbl_meta.license_id = lt_license.id' \
            ' LEFT JOIN tbl_variable ON tbl_meta.variable_id = tbl_variable.id' \
            ' LEFT JOIN lt_location ON tbl_meta.geometry_id = lt_location.id' \
            #  ' WHERE tbl_meta.public IS TRUE'  # only for test use on portal
    if not request.user.is_authenticated:
        query = '{} {}'.format(query, ' WHERE lt_license.share is true')  # only for test use on portal

    attributes = '<attribute>' \
                 '<name>Geometry</name>' \
                 '<minOccurs>0</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>true</nillable>' \
                 '<binding>com.vividsolutions.jts.geom.Point</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>Datentyp</name>' \
                 '<minOccurs>1</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>false</nillable>' \
                 '<binding>java.lang.String</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>Schrittweite</name>' \
                 '<minOccurs>0</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>true</nillable>' \
                 '<binding>java.lang.String</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>Landnutzung</name>' \
                 '<minOccurs>0</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>true</nillable>' \
                 '<binding>java.lang.String</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>Geologie</name>' \
                 '<minOccurs>0</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>true</nillable>' \
                 '<binding>java.lang.String</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>Vorname</name>' \
                 '<minOccurs>0</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>true</nillable>' \
                 '<binding>java.lang.String</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>Nachname</name>' \
                 '<minOccurs>0</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>true</nillable>' \
                 '<binding>java.lang.String</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>Institut</name>' \
                 '<minOccurs>0</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>true</nillable>' \
                 '<binding>java.lang.String</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>Abteilung</name>' \
                 '<minOccurs>0</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>true</nillable>' \
                 '<binding>java.lang.String</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>Projekt</name>' \
                 '<minOccurs>1</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>false</nillable>' \
                 '<binding>java.lang.String</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>Dom&#228;ne</name>' \
                 '<minOccurs>1</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>false</nillable>' \
                 '<binding>java.lang.String</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>Kommentar</name>' \
                 '<minOccurs>0</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>true</nillable>' \
                 '<binding>java.lang.String</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>Lizenz</name>' \
                 '<minOccurs>1</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>false</nillable>' \
                 '<binding>java.lang.String</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>Lizenz_URL</name>' \
                 '<minOccurs>0</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>true</nillable>' \
                 '<binding>java.lang.String</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>site_id</name>' \
                 '<minOccurs>0</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>true</nillable>' \
                 '<binding>java.lang.Integer</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>external_id</name>' \
                 '<minOccurs>0</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>true</nillable>' \
                 '<binding>java.lang.String</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>centroid_x</name>' \
                 '<minOccurs>0</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>true</nillable>' \
                 '<binding>java.math.BigDecimal</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>centroid_y</name>' \
                 '<minOccurs>0</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>true</nillable>' \
                 '<binding>java.math.BigDecimal</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>srid</name>' \
                 '<minOccurs>0</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>true</nillable>' \
                 '<binding>java.lang.Integer</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>geometry_type</name>' \
                 '<minOccurs>0</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>true</nillable>' \
                 '<binding>java.lang.String</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>geom</name>' \
                 '<minOccurs>1</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>false</nillable>' \
                 '<binding>com.vividsolutions.jts.geom.Point</binding>' \
                 '</attribute>'

    xml = '<featureType>' \
        '<name>' + filename + '</name><nativeName>' + filename + '</nativeName>' \
        '<namespace><name>' + workspace + '</name>' \
        '<atom:link xmlns:atom="http://www.w3.org/2005/Atom" rel="alternate" href="' + LOCAL_GEOSERVER + \
        '/rest/namespaces/' + workspace + '.xml" type="application/xml"/>' \
        '</namespace>' \
        '<title>' + filename + '</title>' \
        '<keywords><string>features</string><string>' + filename + '</string></keywords>' \
        '<srs>EPSG:' + str(srid) + '</srs><projectionPolicy>FORCE_DECLARED</projectionPolicy>' \
        '<enabled>true</enabled><advertised>true</advertised>' \
        '<metadata>' \
        '<entry key="elevation"><dimensionInfo><enabled>false</enabled></dimensionInfo></entry>' \
        '<entry key="JDBC_VIRTUAL_TABLE"><virtualTable><name>' + filename + '</name>' \
        '<sql>' + query + '</sql><escapeSql>false</escapeSql><keyColumn>id</keyColumn>' \
        '<geometry><name>Geometry</name><type>Point</type><srid>' + str(srid) + '</srid></geometry>' \
        '<geometry><name>geom</name><type>Point</type><srid>' + str(4326) + '</srid></geometry>' \
        '</virtualTable></entry>' \
        '<entry key="time"><dimensionInfo><enabled>false</enabled><defaultValue/></dimensionInfo></entry>' \
        '<entry key="cachingEnabled">false</entry>' \
        '</metadata>' \
        '<store class="dataStore"><name>' + workspace + ':' + datastore + '</name>' \
        '<atom:link xmlns:atom="http://www.w3.org/2005/Atom" rel="alternate" href="' + LOCAL_GEOSERVER + \
        '/rest/workspaces/' + workspace + '/datastores/' + datastore + '.xml" type="application/xml"/>' \
        '</store>' \
        '<maxFeatures>0</maxFeatures><numDecimals>0</numDecimals><overridingServiceSRS>false</overridingServiceSRS>' \
        '<skipNumberMatched>false</skipNumberMatched><circularArcPresent>false</circularArcPresent>' \
        '<attributes>' + attributes + '</attributes>' \
        '</featureType>'

    return xml


def create_id_layer(request, filename, selection, datastore, workspace, srid=3857):
    """
    creates a layer in geoserver with the elements defined in SELECTION
    :param request:
    :type request: object
    :param filename:
    :type filename: string
    :param selection:
    :type selection: string (list of IDs)
    :param datastore:
    :type datastore: string
    :param workspace: string
    :type workspace:
    :param srid: integer
    :type srid:
    :return:
    :rtype:
    """
    xml = build_xml_from_id(request, filename, selection, datastore, workspace, srid)
    url = '{}/rest/workspaces/{}/datastores/{}/featuretypes'.format(LOCAL_GEOSERVER, workspace, datastore)
    build = requests.post(url, auth=(eval(SECRET_GEOSERVER)), data=xml, headers={'Content-type': 'text/xml'})
    if build.status_code != 201:
        logger.warning(str(build.status_code) + ': ' + build.text)


def build_xml_from_id(request, filename, selection, datastore, workspace, srid):
    """
    XML to send to geoserver; Geoserver builds the layer according to the query defined with the xml
    :param request:
    :type request: object
    :param filename:
    :type filename:
    :param selection:
    :type selection:
    :param datastore:
    :type datastore:
    :param workspace:
    :type workspace:
    :param srid:
    :type srid:
    :return:
    :rtype:
    """
    # attributes have to be defined according to the selected table columns in the query
    query = 'SELECT ST_Transform(ST_SetSRID(ST_Point(ST_X(geom), ST_Y(geom)), srid), 3857) ::geometry' \
            ' as "Geometry",' \
            ' tbl_variable.variable_name AS "Datentyp",' \
            ' tbl_meta.id,' \
            ' tbl_meta.site_id,' \
            ' lt_location.centroid_x,' \
            ' lt_location.centroid_y,' \
            ' lt_location.srid,' \
            ' lt_location.geometry_type,' \
            ' lt_location.geom' \
            ' FROM tbl_meta' \
            ' LEFT JOIN tbl_data_source ON tbl_meta.source_id = tbl_data_source.id' \
            ' LEFT JOIN lt_source_type ON tbl_data_source.source_type_id = lt_source_type.id' \
            ' LEFT JOIN lt_site ON tbl_meta.site_id = lt_site.id' \
            ' LEFT JOIN tbl_variable ON tbl_meta.variable_id = tbl_variable.id' \
            ' LEFT JOIN lt_location ON tbl_meta.geometry_id = lt_location.id' \
            ' LEFT JOIN lt_license ON tbl_meta.license_id = lt_license.id' \
            ' WHERE ' \
            ' tbl_meta.id in (' + selection + ')'

    if not request.user.is_authenticated:
        query = '{} {}'.format(query, ' and lt_license.commercial is false')  # only for test use on portal

    attributes = '<attribute>' \
                 '<name>Geometry</name>' \
                 '<minOccurs>0</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>true</nillable>' \
                 '<binding>com.vividsolutions.jts.geom.Point</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>Datentyp</name>' \
                 '<minOccurs>1</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>false</nillable>' \
                 '<binding>java.lang.String</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>site_id</name>' \
                 '<minOccurs>0</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>true</nillable>' \
                 '<binding>java.lang.Integer</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>centroid_x</name>' \
                 '<minOccurs>0</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>true</nillable>' \
                 '<binding>java.math.BigDecimal</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>centroid_y</name>' \
                 '<minOccurs>0</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>true</nillable>' \
                 '<binding>java.math.BigDecimal</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>srid</name>' \
                 '<minOccurs>0</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>true</nillable>' \
                 '<binding>java.lang.Integer</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>geometry_type</name>' \
                 '<minOccurs>0</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>true</nillable>' \
                 '<binding>java.lang.String</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>geom</name>' \
                 '<minOccurs>1</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>false</nillable>' \
                 '<binding>com.vividsolutions.jts.geom.Point</binding>' \
                 '</attribute>'

    xml = '<featureType><name>' + filename + '</name><nativeName>' + filename + '</nativeName>' \
        '<namespace><name>' + workspace + '</name>' \
        '<atom:link xmlns:atom="http://www.w3.org/2005/Atom" rel="alternate" href="' + LOCAL_GEOSERVER + \
        '/rest/namespaces/' + workspace + '.xml" type="application/xml"/>' \
        '</namespace>' \
        '<title>' + filename + '</title>' \
        '<keywords><string>features</string><string>' + filename + '</string></keywords>' \
        '<srs>EPSG:' + str(srid) + '</srs>' \
        '<projectionPolicy>FORCE_DECLARED</projectionPolicy>' \
        '<enabled>true</enabled>' \
        '<advertised>true</advertised>' \
        '<metadata>' \
        '<entry key="elevation"><dimensionInfo><enabled>false</enabled></dimensionInfo></entry>' \
        '<entry key="JDBC_VIRTUAL_TABLE"><virtualTable><name>' + filename + '</name><sql>' + query + '</sql>' \
        '<escapeSql>false</escapeSql><keyColumn>id</keyColumn><geometry><name>Geometry</name><type>Point</type>' \
        '<srid>' + str(srid) + '</srid></geometry><geometry><name>geom</name><type>Point</type>' \
        '<srid>' + str(srid) + '</srid>' \
        '</geometry></virtualTable></entry>' \
        '<entry key="time"><dimensionInfo><enabled>false</enabled><defaultValue/></dimensionInfo></entry>' \
        '<entry key="cachingEnabled">false</entry></metadata><store class="dataStore">' \
        '<name>' + workspace + ':' + datastore + '</name>' \
        '<atom:link xmlns:atom="http://www.w3.org/2005/Atom" rel="alternate" href="' + LOCAL_GEOSERVER + \
        '/rest/workspaces/' + workspace + '/datastores/' + datastore + '.xml" type="application/xml"/>' \
        '</store>' \
        '<maxFeatures>0</maxFeatures><numDecimals>0</numDecimals><overridingServiceSRS>false</overridingServiceSRS>' \
        '<skipNumberMatched>false</skipNumberMatched><circularArcPresent>false</circularArcPresent>' \
        '<attributes>' + attributes + '</attributes>' \
        '</featureType>'

    return xml


def create_data_layer(request, filename, selection, datastore, workspace, srid=3857):
    """

    :param request:
    :type request:
    :param filename:
    :type filename:
    :param selection:
    :type selection:
    :param datastore:
    :type datastore:
    :param workspace:
    :type workspace:
    :param srid:
    :type srid:
    :return:
    :rtype:
    """
    xml = build_datalayer(request, filename, selection, datastore, workspace, srid)
    url = '{}/rest/workspaces/{}/datastores/{}/featuretypes'.format(LOCAL_GEOSERVER, workspace, datastore)
    build = requests.post(url, auth=(eval(SECRET_GEOSERVER)), data=xml, headers={'Content-type': 'text/xml'})
    if build.status_code != 201:
        logger.warning(str(build.status_code) + ': ' + build.text)


def build_datalayer(request, filename, selection, datastore, workspace, srid):
    """
    build layer on geoserver to extract date, time and value from timeseries from geoserver.
    :param request:
    :type request:
    :param filename:
    :type filename:
    :param selection:
    :type selection:
    :param datastore:
    :type datastore:
    :param workspace:
    :type workspace:
    :param srid:
    :type srid:
    :return:
    :rtype:
    """
    # attributes have to be defined according to the selected table columns in the query
    query = 'SELECT tbl_data.tstamp::timestamp::date as "Date", ' \
            'tbl_data.tstamp::timestamp::time as "Time", ' \
            'tbl_data.value, ST_Transform(ST_SetSRID(ST_Point(ST_X(geom), ST_Y(geom)), srid), 3857) ::geometry as ' \
            '"Geometry", ' \
            'tbl_meta.id, ' \
            'lt_location.centroid_x, ' \
            'lt_location.centroid_y, ' \
            'lt_location.srid, ' \
            'lt_location.geometry_type, ' \
            'lt_location.geom ' \
            'FROM tbl_meta ' \
            'LEFT JOIN tbl_data ON tbl_meta.id = tbl_data.meta_id ' \
            'LEFT JOIN lt_location ON tbl_meta.geometry_id = lt_location.id ' \
            'LEFT JOIN lt_license ON tbl_meta.license_id = lt_license.id ' \
            'WHERE tbl_meta.id in (' + selection + ')'

    if not request.user.is_authenticated:
        query = '{} {}'.format(query, ' and lt_license.commercial is false')  # only for test use on portal

    attributes = '<attribute>' \
                 '<name>Date</name>' \
                 '<minOccurs>0</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>true</nillable>' \
                 '<binding>java.sql.Date</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>Time</name>' \
                 '<minOccurs>0</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>true</nillable>' \
                 '<binding>java.sql.Time</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>value</name>' \
                 '<minOccurs>1</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>false</nillable>' \
                 '<binding>java.math.BigDecimal</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>Geometry</name>' \
                 '<minOccurs>0</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>true</nillable>' \
                 '<binding>com.vividsolutions.jts.geom.Point</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>id</name>' \
                 '<minOccurs>1</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>false</nillable>' \
                 '<binding>java.lang.Integer</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>centroid_x</name>' \
                 '<minOccurs>0</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>true</nillable>' \
                 '<binding>java.math.BigDecimal</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>centroid_y</name>' \
                 '<minOccurs>0</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>true</nillable>' \
                 '<binding>java.math.BigDecimal</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>srid</name>' \
                 '<minOccurs>0</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>true</nillable>' \
                 '<binding>java.lang.Integer</binding>' \
                 '</attribute><attribute>' \
                 '<name>geometry_type</name>' \
                 '<minOccurs>0</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>true</nillable>' \
                 '<binding>java.lang.String</binding>' \
                 '</attribute>' \
                 '<attribute>' \
                 '<name>geom</name>' \
                 '<minOccurs>1</minOccurs>' \
                 '<maxOccurs>1</maxOccurs>' \
                 '<nillable>false</nillable>' \
                 '<binding>com.vividsolutions.jts.geom.Point</binding>' \
                 '</attribute>'

    xml = '<featureType><name>' + filename + '</name><nativeName>' + filename + '</nativeName>' \
        '<namespace><name>' + workspace + '</name>' \
        '<atom:link rel="alternate" href="' + LOCAL_GEOSERVER + '/rest/namespaces/' + workspace + \
        '.xml" type="application/xml"/>' \
        '</namespace>' \
        '<title>' + filename + '</title>' \
        '<keywords><string>features</string><string>' + filename + '</string></keywords>' \
        '<srs>EPSG:' + str(srid) + '</srs>' \
        '<projectionPolicy>FORCE_DECLARED</projectionPolicy>' \
        '<enabled>true</enabled>' \
        '<metadata><entry key="JDBC_VIRTUAL_TABLE"><virtualTable>' \
        '<name>' + filename + '</name><sql>' + query + '</sql><escapeSql>false</escapeSql>' \
        '<geometry><name>Geometry</name><type>Point</type><srid>' + str(srid) + '</srid></geometry>' \
        '<geometry><name>geom</name><type>Point</type><srid>' + str(srid) + '</srid></geometry>' \
        '</virtualTable></entry></metadata>' \
        '<store class="dataStore"><name>' + workspace + ':' + datastore + '</name>' \
        '<atom:link rel="alternate" href="' + LOCAL_GEOSERVER + '/rest/workspaces/' + workspace + '/datastores/' \
        + datastore + '.xml" type="application/xml"/></store>' \
        '<maxFeatures>0</maxFeatures><numDecimals>0</numDecimals><overridingServiceSRS>false</overridingServiceSRS>' \
        '<skipNumberMatched>false</skipNumberMatched><circularArcPresent>false</circularArcPresent>' \
        '<attributes>' + attributes + '</attributes>' \
        '</featureType>'

    return xml
