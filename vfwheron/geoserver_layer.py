"""

"""
import json
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
    the new workspace in geoserver, and then in an inner function add the store with the login information for the
    database
    from the django settings.

    :param store:
    :type store:
    :param workspace:
    :type workspace:
    :return:
    :rtype:
    """

    def __build_store():
        """
        Inner function to build the data store
        """
        datastore_xml = '<dataStore>' \
                        '<name>{store}</name>' \
                        '<type>PostGIS</type>' \
                        '<enabled>true</enabled>' \
                        '<workspace>' \
                        '<name>{workspace}</name>' \
                        '<atom:link rel="alternate" ' \
                        'href="http://127.0.0.1:8080/geoserver/rest/workspaces/{workspace}.xml" ' \
                        'type="application/xml"/>' \
                        '</workspace>' \
                        '<connectionParameters>' \
                        '<host>{host}</host>' \
                        '<port>{port}</port>' \
                        '<database>{dbname}</database>' \
                        '<user>{user}</user>' \
                        '<passwd>{passwd}</passwd>' \
                        '<dbtype>postgis</dbtype>' \
                        '</connectionParameters>' \
                        '</dataStore>' \
                        '<featureTypes>' \
                        '<atom:link rel="alternate" ' \
                        'href="http://127.0.0.1:8080/geoserver/rest/workspaces/{workspace}' \
                        '/datastores/{store}/featuretypes.xml" ' \
                        'type="application/xml"/>' \
                        '</featureTypes>'.format(store=store, workspace=workspace, host=DATABASES['default']['HOST'],
                                                 port=DATABASES['default']['PORT'],
                                                 dbname=DATABASES['default']['NAME'],
                                                 user=DATABASES['default']['USER'],
                                                 passwd=DATABASES['default']['PASSWORD'])
        datastore_xml = '<dataStore>' \
                        '<name>{store}</name>' \
                        '<connectionParameters>' \
                        '<host>{host}</host>' \
                        '<port>{port}</port>' \
                        '<database>{dbname}</database>' \
                        '<user>{user}</user>' \
                        '<passwd>{passwd}</passwd>' \
                        '<dbtype>postgis</dbtype>' \
                        '</connectionParameters>' \
                        '<Parameter><name>Expose primary keys</name><value>true</value></Parameter>' \
                        '</dataStore>'.format(store=store, host=DATABASES['default']['HOST'],
                                                 port=DATABASES['default']['PORT'],
                                                 dbname=DATABASES['default']['NAME'],
                                                 user=DATABASES['default']['USER'],
                                                 passwd=DATABASES['default']['PASSWORD'])
        rest_url = '{}/rest/workspaces/{}/datastores'.format(LOCAL_GEOSERVER, workspace)
        rest_build = requests.post(rest_url, auth=eval(SECRET_GEOSERVER), data=datastore_xml,
                                   headers={'Content-type': 'text/xml'})
        print('+build store: ', rest_build.status_code)
        print('+build store: ', rest_build.text)
        print('+build store: ', rest_build.reason)
        if rest_build.status_code != 201:
            print('\033[91mCannont build store: {}\033[0m'.format(rest_build.status_code))
            logger.warning('Cannot build new store in geoserver, {}: {}'.format(check.status_code, check.text))

    # first check if workspace exists or try to build it if not:
    url = '{}/rest/workspaces/{}'.format(LOCAL_GEOSERVER, workspace)
    check = requests.get(url, auth=eval(SECRET_GEOSERVER), headers={"Accept": "application/xml"})
    print('check1: ', check)
    if check.status_code != 200:  # if workspace doesn't exist build it
        logger.warning('workspace missing, trying to build it, {}: {}'.format(check.status_code, check.text))
        print('get layer in test (if): ', str(check.status_code) + ': ' + check.text)
        # build new workspace:
        url = '{}/rest/workspaces'.format(LOCAL_GEOSERVER)
        xml = '<workspace><name>{}</name></workspace>'.format(workspace)
        build = requests.post(url, auth=eval(SECRET_GEOSERVER), data=xml, headers={'Content-type': 'text/xml'})
        if build.status_code != 201:
            print('Cannot build new workspace in geoserver, {}: {}'.format(check.status_code, check.text))
            logger.warning('Cannot build new workspace in geoserver, {}: {}'.format(check.status_code, check.text))
        else:
            print('__ so now i build a store? is the workspace there?')
            url = '{}/rest/workspaces/{}'.format(LOCAL_GEOSERVER, workspace)
            check = requests.get(url, auth=eval(SECRET_GEOSERVER), headers={"Accept": "application/xml"})
            print('__ check if workspace is there: ', check)
            __build_store()
    else:
        url = '{}/rest/workspaces/{}/datastores/{}'.format(LOCAL_GEOSERVER, workspace, store)
        check = requests.get(url, auth=eval(SECRET_GEOSERVER), headers={"Accept": "application/xml"})
        print('url2: ', url)
        print('check2: ', check)
        if check.status_code != 200:  # if store doesn't exist build it
            logger.warning('datastore missing, trying to build it, {}: {}'.format(check.status_code, check.text))
            # print('get layer (if): ', str(check.status_code) + ': ' + check.text)
            # build new workspace:
            __build_store()
        # else:
        # print('store exist too: ', check.status_code)
    url = '{}/rest/workspaces/{}/datastores/{}'.format(LOCAL_GEOSERVER, workspace, store)
    check = requests.get(url, auth=eval(SECRET_GEOSERVER), headers={"Accept": "application/xml"})
    print('___url2: ', url)
    print('___check2: ', check)
    # Now we know we have a workspace and store we can test if these access the right database
    url = '{}/rest/workspaces/{}/datastores/{}'.format(LOCAL_GEOSERVER, workspace, store)
    check = requests.get(url, auth=eval(SECRET_GEOSERVER), headers={"Accept": "application/json"})
    content = json.loads(check.content)
    if DATABASES['default']['NAME'] != content['dataStore']['connectionParameters']['entry'][0]['$']:
        print('\033[91m +++ Wrong database in use. Change your store and workspace in views! +++\033[0m')
        __build_store()
        print('Wrong database!!!')


# TODO: IDs for new layer (for user) are still missing
def create_layer(request, filename, datastore, workspace, srid=3857, selection=None):
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
    print('_____start to create a layer')
    xml = __build_new_layer_xml(request, filename, datastore, workspace, srid, selection)
    print('no xml?')
    url = '{}/rest/workspaces/{}/datastores/{}/featuretypes'.format(LOCAL_GEOSERVER, workspace, datastore)
    build = requests.post(url, auth=eval(SECRET_GEOSERVER), data=xml, headers={'Content-type': 'text/xml'})
    print('_____start to create a layer build: ', build)
    if build.status_code != 201:
        logger.warning('{}: {}'.format(build.status_code, build.text))
        print('create layer: ', str(build.status_code) + ': ' + build.text)


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
    print('get layer url: ', url)
    # url = LOCAL_GEOSERVER + '/rest/workspaces/' + workspace + '/datastores/' + datastore + '/featuretypes/' +
    # filename
    build = requests.get(url, auth=eval(SECRET_GEOSERVER), headers={"Accept": "application/xml"})
    if build.status_code != 200:
        logger.warning('{}: {}'.format(build.status_code, build.text))
        print('get layer (if): ', str(build.status_code) + ': ' + build.text)
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
    build = requests.delete(url, auth=eval(SECRET_GEOSERVER),
                            headers={'Content-type': 'application/json', 'Accept': 'application/json'})
    if build.status_code != 200:
        logger.warning('{}: {}'.format(build.status_code, build.text))
        # logger.warning(str(build.status_code) + ': ' + build.text)

    url = '{}/rest/workspaces/{}/datastores/{}/featuretypes/{}'.format(LOCAL_GEOSERVER, workspace, datastore, filename)
    # url = LOCAL_GEOSERVER + '/rest/workspaces/' + workspace + '/datastores/' + datastore + '/featuretypes/' +
    # filename
    build = requests.delete(url, auth=eval(SECRET_GEOSERVER),
                            headers={'Content-type': 'application/json', 'Accept': 'application/json'})
    if build.status_code != 200:
        # logger.warning(str(build.status_code) + ': ' + build.text)
        logger.warning('{}: {}'.format(build.status_code, build.text))


def __create_attributes(attributes_list):
    attributes = ''
    binding_dict = {'bigDeci': 'java.math.BigDecimal', 'bool': 'java.lang.Boolean',
                    'date': 'java.sql.Date', 'int': 'java.lang.Integer',
                    'point': 'com.vividsolutions.jts.geom.Point', 'string': 'java.lang.String',
                    'time': 'java.sql.Time'}

    for element in attributes_list:
        attribute = '<attribute>' \
                    '<name>' + element[0] + '</name>' \
                    '<minOccurs>' + str(element[1]) + '</minOccurs>' \
                    '<maxOccurs>' + str(element[2]) + '</maxOccurs>' \
                    '<nillable>' + str(element[3]).lower() + '</nillable>' \
                    '<binding>' + binding_dict[element[4]] + '</binding>' \
                    '</attribute>'

        attributes += attribute

    return attributes


# TODO: Query needs 'WHERE' for the IDs of data available for user (isn't this already done in '__build_xml_from_id'?)
def __build_new_layer_xml(request, filename, datastore, workspace, srid, selection):
    """

    :param selection:
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
    query = 'SELECT ST_Transform(location, 3857) as "Geometry", ' \
            'title as "Beschreibung", name as "Datentyp", ' \
            'comment as "Kommentar", ' \
            'embargo as "Embargo", ' \
            'entries.id as "eID' \
            'FROM entries LEFT JOIN variables on entries.variable_id = variables.id'
    srid = 4326
    # query = 'SELECT ST_FlipCoordinates(ST_Transform(location, 3857)) ::geometry as "Geometry", ' \

    # query = 'SELECT location ::geometry as "Geometry", ' \
    query = 'SELECT ST_Transform(ST_FlipCoordinates(location), 4326) ::geometry as "Geometry", ' \
            'title as "Beschreibung", name as "Datentyp", ' \
            'comment as "Kommentar", ' \
            'embargo as "Embargo" ' \
            'FROM entries LEFT JOIN variables on entries.variable_id = variables.id'
        #  ' WHERE tbl_meta.public IS TRUE'  # only for test use on portal
    if selection is not None:
        print('is there a selection?')
        query = '{} WHERE entries.id in ({})'.format(query, selection)
    # if not request.user.is_authenticated:
    #     query = '{} {}'.format(query, ' WHERE embargo is false')  # only for test use on portal

    # attributes defined with name: [minOccurs, maxOccurs, nillable, binding]
    attribute_list = [('Geometry', 0, 1, True, 'point'), ('Beschreibung', 1, 1, False, 'string'),
                      ('Datentyp', 1, 1, False, 'string'), ('Kommentar', 0, 1, True, 'string'),
                      ('Embargo', 1, 1, False, 'bool')]#, ('eID', 1, 1, False, 'int')]

    print('attributes list: ', attribute_list)
    attributes = __create_attributes(attribute_list)
    print('attributes: ', attributes)
    xml = '<featureType>' \
            '<name>' + filename + '</name>'\
            '<nativeName>' + filename + '</nativeName>' \
            '<namespace>' \
              '<name>' + workspace + '</name>' \
              '<atom:link xmlns:atom="http://www.w3.org/2005/Atom" rel="alternate" href="' + LOCAL_GEOSERVER + \
              '/rest/namespaces/' + workspace + '.xml" type="application/xml"/>' \
            '</namespace>' \
            '<title>' + filename + '</title>' \
            '<keywords><string>features</string><string>' + filename + '</string></keywords>' \
            '<nativeCRS>EPSG:' + str(srid) + '</nativeCRS>' \
            '<srs>EPSG:' + str(srid) + '</srs><projectionPolicy>FORCE_DECLARED</projectionPolicy>' \
            '<enabled>true</enabled><advertised>true</advertised>' \
            '<metadata>' \
              '<entry key="elevation"><dimensionInfo><enabled>false</enabled></dimensionInfo></entry>' \
              '<entry key="JDBC_VIRTUAL_TABLE">' \
                '<virtualTable><name>' + filename + '</name>' \
                  '<sql>' + query + '</sql>' \
                  '<escapeSql>false</escapeSql>' \
                  '<geometry><name>Geometry</name><type>Point</type><srid>' + str(srid) + '</srid></geometry>' \
                '</virtualTable>' \
              '</entry>' \
              '<entry key="time"><dimensionInfo><enabled>false</enabled><defaultValue/></dimensionInfo></entry>' \
              '<entry key="cachingEnabled">false</entry>' \
            '</metadata>' \
            '<store class="dataStore"><name>' + workspace + ':' + datastore + '</name>' \
              '<atom:link xmlns:atom="http://www.w3.org/2005/Atom" rel="alternate" href="' + LOCAL_GEOSERVER + \
              '/rest/workspaces/' + workspace + '/datastores/' + datastore + '.xml" type="application/xml"/>' \
            '</store>' \
            '<maxFeatures>0</maxFeatures><numDecimals>0</numDecimals>' \
            '<overridingServiceSRS>false</overridingServiceSRS>' \
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
    :param selection: string with list of IDs
    :type selection: list
    :param datastore:
    :type datastore: string
    :param workspace: string
    :type workspace:
    :param srid: integer
    :type srid:
    :return:
    :rtype:
    """
    xml = __build_xml_from_id(request, filename, selection, datastore, workspace, srid)
    # url = LOCAL_GEOSERVER + '/rest/workspaces/' + workspace + '/datastores/' + datastore + '/featuretypes'
    url = '{}/rest/workspaces/{}/datastores/{}/featuretypes'.format(LOCAL_GEOSERVER, workspace, datastore)
    build = requests.post(url, auth=eval(SECRET_GEOSERVER), data=xml, headers={'Content-type': 'text/xml'})
    print('status: ', build.status_code)
    print('status: ', build.text)
    if build.status_code != 201:
        logger.warning(str(build.status_code) + ': ' + build.text)

#
# def get_ID_layer(filename='selection_test', datastore='new_vforwater_gis', workspace='CAOS_update'):
#     """
#
#     :param filename:
#     :type filename:
#     :param datastore:
#     :type datastore:
#     :param workspace:
#     :type workspace:
#     :return:
#     :rtype:
#     """
#     url = LOCAL_GEOSERVER + '/rest/workspaces/' + workspace + '/datastores/' + datastore + '/featuretypes/' + filename
#     build = requests.get(url, auth=(eval(SECRET_GEOSERVER)), headers={"Accept": "application/xml"})
#     if build.status_code != 200:
#         logger.warning(str(build.status_code) + ': ' + build.text)
#         return False
#     return True


# def delete_ID_layer(filename='selection_test', datastore='new_vforwater_gis', workspace='CAOS_update'):
#     """
#
#     :param filename:
#     :type filename:
#     :param datastore:
#     :type datastore:
#     :param workspace:
#     :type workspace:
#     :return:
#     :rtype:
#     """
#     # first delete layer, then feature!
#     url = LOCAL_GEOSERVER + '/rest/layers/' + filename
#     build = requests.delete(url, auth=(eval(SECRET_GEOSERVER)),
#                             headers={'Content-type': 'application/json', 'Accept': 'application/json'})
#     if build.status_code != 200:
#         logger.warning(str(build.status_code) + ': ' + build.text)
#
#     url = LOCAL_GEOSERVER + '/rest/workspaces/' + workspace + '/datastores/' + datastore + '/featuretypes/' + filename
#     build = requests.delete(url, auth=(eval(SECRET_GEOSERVER)),
#                             headers={'Content-type': 'application/json', 'Accept': 'application/json'})
#     if build.status_code != 200:
#         logger.warning(str(build.status_code) + ': ' + build.text)


def __build_xml_from_id(request, filename, selection, datastore, workspace, srid):
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

    # attributes defined with name: [minOccurs, maxOccurs, nillable, binding]
    attribute_list = [('Geometry', 0, 1, True, 'point'), ('Datentyp', 1, 1, False, 'string'),
                      ('site_id', 0, 1, True, 'string'),
                      ('centroid_x', 0, 1, True, 'bigDeci'), ('centroid_y', 0, 1, True, 'bigDeci'),
                      ('srid', 0, 1, True, 'int'), ('geometry_type', 0, 1, True, 'string'),
                      ('geom', 1, 1, False, 'point')]

    attributes = __create_attributes(attribute_list)

    xml = '<featureType>' \
            '<name>' + filename + '</name><nativeName>' + filename + '</nativeName>' \
            '<namespace>' \
              '<name>' + workspace + '</name>' \
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
              '<entry key="JDBC_VIRTUAL_TABLE">' \
                '<virtualTable>' \
                  '<name>' + filename + '</name>' \
                  '<sql>' + query + '</sql>' \
                  '<escapeSql>false</escapeSql>' \
                  '<keyColumn>id</keyColumn>' \
                  '<geometry><name>Geometry</name><type>Point</type><srid>' + str(srid) + '</srid></geometry>' \
                  '<geometry><name>geom</name><type>Point</type><srid>' + str(srid) + '</srid></geometry>' \
                '</virtualTable>' \
              '</entry>' \
              '<entry key="time"><dimensionInfo><enabled>false</enabled><defaultValue/></dimensionInfo></entry>' \
              '<entry key="cachingEnabled">false</entry>' \
            '</metadata>' \
            '<store class="dataStore">' \
              '<name>' + workspace + ':' + datastore + '</name>' \
              '<atom:link xmlns:atom="http://www.w3.org/2005/Atom" rel="alternate" ' \
                'href="' + LOCAL_GEOSERVER + '/rest/workspaces/' + workspace + '/datastores/' + datastore + '.xml" ' \
                'type="application/xml"/>' \
            '</store>' \
            '<maxFeatures>0</maxFeatures><numDecimals>0</numDecimals>' \
            '<overridingServiceSRS>false</overridingServiceSRS>' \
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
    xml = __build_datalayer(request, filename, selection, datastore, workspace, srid)
    url = '{}/rest/workspaces/{}/datastores/{}/featuretypes'.format(LOCAL_GEOSERVER, workspace, datastore)
    # url = LOCAL_GEOSERVER + '/rest/workspaces/' + workspace + '/datastores/' + datastore + '/featuretypes'
    build = requests.post(url, auth=eval(SECRET_GEOSERVER), data=xml, headers={'Content-type': 'text/xml'})
    if build.status_code != 201:
        logger.warning(str(build.status_code) + ': ' + build.text)

# TODO: Rethink if this is still usefull
def __build_datalayer(request, filename, selection, datastore, workspace, srid):
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

    # attributes defined with name: [minOccurs, maxOccurs, nillable, binding]
    attribute_list = [('Date', 0, 1, True, 'date'), ('Time', 0, 1, True, 'time'),
                      ('value', 1, 1, False, 'bigDeci'), ('Geometry', 0, 1, True, 'point'),
                      ('id', 1, 1, False, 'int'),
                      ('centroid_x', 0, 1, True, 'bigDeci'), ('centroid_y', 0, 1, True, 'bigDeci'),
                      ('srid', 0, 1, True, 'int'), ('geometry_type', 0, 1, True, 'string'),
                      ('geom', 1, 1, False, 'point')]

    attributes = __create_attributes(attribute_list)

    xml = '<featureType>' \
            '<name>' + filename + '</name><nativeName>' + filename + '</nativeName>' \
            '<namespace>' \
              '<name>' + workspace + '</name>' \
              '<atom:link rel="alternate" href="' + LOCAL_GEOSERVER + '/rest/namespaces/' + workspace + '.xml" ' \
                'type="application/xml"/>' \
            '</namespace>' \
            '<title>' + filename + '</title>' \
            '<keywords><string>features</string><string>' + filename + '</string></keywords>' \
            '<srs>EPSG:' + str(srid) + '</srs>' \
            '<projectionPolicy>FORCE_DECLARED</projectionPolicy><enabled>true</enabled>' \
            '<metadata>' \
              '<entry key="JDBC_VIRTUAL_TABLE">' \
                '<virtualTable>' \
                  '<name>' + filename + '</name>' \
                  '<sql>' + query + '</sql><escapeSql>false</escapeSql>' \
                  '<geometry><name>Geometry</name><type>Point</type><srid>' + str(srid) + '</srid></geometry>' \
                  '<geometry><name>geom</name><type>Point</type><srid>' + str(srid) + '</srid></geometry>' \
                '</virtualTable>' \
              '</entry>' \
            '</metadata>' \
            '<store class="dataStore">' \
              '<name>' + workspace + ':' + datastore + '</name>' \
              '<atom:link rel="alternate" href="' + LOCAL_GEOSERVER + '/rest/workspaces/' + workspace + \
              '/datastores/' + datastore + '.xml" type="application/xml"/>' \
            '</store>' \
            '<maxFeatures>0</maxFeatures><numDecimals>0</numDecimals>' \
            '<overridingServiceSRS>false</overridingServiceSRS>' \
            '<skipNumberMatched>false</skipNumberMatched><circularArcPresent>false</circularArcPresent>' \
            '<attributes>' + attributes + '</attributes>' \
          '</featureType>'

    return xml
