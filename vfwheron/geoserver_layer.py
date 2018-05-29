import requests

from heron.settings import LOCAL_GEOSERVER

import logging
logger = logging.getLogger(__name__)


# TODO: IDs for new layer (for user) are still missing
def create_layer(filename='rest_test', datastore='new_vforwater_gis', workspace='CAOS_update', srid=3857):

    xml = build_new_layer_XML(filename, datastore, workspace, srid)
    url = LOCAL_GEOSERVER + '/rest/workspaces/' + workspace + '/datastores/' + datastore + '/featuretypes'
    build = requests.post(url, auth=('admin', 'vfwaterv2'), data=xml, headers={'Content-type': 'text/xml'})
    if build.status_code != 201:
        logger.warning(str(build.status_code) + ': ' + build.text)


def get_layer(filename='rest_test', datastore='new_vforwater_gis', workspace='CAOS_update'):

    url = LOCAL_GEOSERVER + '/rest/workspaces/' + workspace + '/datastores/' + datastore + '/featuretypes/' + filename
    build = requests.get(url, auth=('admin', 'vfwaterv2'), headers={"Accept": "application/xml"})
    if build.status_code != 200:
        logger.warning(str(build.status_code) + ': ' + build.text)
        return False
    return True


def delete_layer(filename='rest_test', datastore='new_vforwater_gis', workspace='CAOS_update'):
    # first delete layer, then feature!
    url = LOCAL_GEOSERVER + '/rest/layers/' + filename
    build = requests.delete(url, auth=('admin', 'vfwaterv2'),
                            headers={'Content-type': 'application/json', 'Accept': 'application/json'})
    if build.status_code != 200:
        logger.warning(str(build.status_code) + ': ' + build.text)

    url = LOCAL_GEOSERVER + '/rest/workspaces/' + workspace + '/datastores/' + datastore + '/featuretypes/' + filename
    build = requests.delete(url, auth=('admin', 'vfwaterv2'),
                            headers={'Content-type': 'application/json', 'Accept': 'application/json'})
    if build.status_code != 200:
        logger.warning(str(build.status_code) + ': ' + build.text)

# TODO: Query needs 'WHERE' for the IDs of data available for user
def build_new_layer_XML(filename, datastore, workspace, srid):

    query ='SELECT ST_Transform(ST_SetSRID(ST_Point(ST_X(geom), ST_Y(geom)), srid), 3857) ::geometry'\
        ' as "Geometry",'\
        ' tbl_variable.variable_name AS "Datentyp",'\
        ' tbl_meta.spacing AS "Schrittweite",'\
        ' lt_site.landuse AS "Landnutzung",'\
        ' lt_soil.geology AS "Geologie",'\
        ' lt_user.first_name AS "Vorname",'\
        ' lt_user.last_name AS "Nachname",'\
        ' lt_user.institution_name AS "Institut",'\
        ' lt_user.department AS "Abteilung",'\
        ' lt_project.project_name AS "Projekt",'\
        ' lt_domain.domain_name AS "Domäne",'\
        ' tbl_meta.comment AS "Kommentar",'\
        ' tbl_meta.id,'\
        ' tbl_meta.site_id,'\
        ' tbl_meta.external_id,'\
        ' lt_location.centroid_x,'\
        ' lt_location.centroid_y,'\
        ' lt_location.srid,'\
        ' lt_location.geometry_type,'\
        ' lt_location.geom'\
        ' FROM tbl_meta'\
        ' LEFT JOIN nm_meta_domain ON tbl_meta.id = nm_meta_domain.meta_id'\
        ' LEFT JOIN lt_domain ON nm_meta_domain.domain_id = lt_domain.id'\
        ' LEFT JOIN lt_project ON lt_domain.project_id = lt_project.id'\
        ' LEFT JOIN lt_user ON tbl_meta.publisher_id = lt_user.id'\
        ' LEFT JOIN tbl_data_source ON tbl_meta.source_id = tbl_data_source.id'\
        ' LEFT JOIN lt_source_type ON tbl_data_source.source_type_id = lt_source_type.id'\
        ' LEFT JOIN lt_site ON tbl_meta.site_id = lt_site.id'\
        ' LEFT JOIN lt_soil ON tbl_meta.soil_id = lt_soil.id'\
        ' LEFT JOIN tbl_variable ON tbl_meta.variable_id = tbl_variable.id'\
        ' LEFT JOIN lt_location ON tbl_meta.geometry_id = lt_location.id'\

    # attributes have to be defined according to the selected table columns in the query
    attributes = '<attribute>'\
        '<name>Geometry</name>'\
        '<minOccurs>0</minOccurs>'\
        '<maxOccurs>1</maxOccurs>'\
        '<nillable>true</nillable>'\
        '<binding>com.vividsolutions.jts.geom.Point</binding>'\
        '</attribute>'\
        '<attribute>'\
        '<name>Datentyp</name>'\
        '<minOccurs>1</minOccurs>'\
        '<maxOccurs>1</maxOccurs>'\
        '<nillable>false</nillable>'\
        '<binding>java.lang.String</binding>'\
        '</attribute>'\
        '<attribute>'\
        '<name>Schrittweite</name>'\
        '<minOccurs>0</minOccurs>'\
        '<maxOccurs>1</maxOccurs>'\
        '<nillable>true</nillable>'\
        '<binding>java.lang.String</binding>'\
        '</attribute>'\
        '<attribute>'\
        '<name>Landnutzung</name>'\
        '<minOccurs>0</minOccurs>'\
        '<maxOccurs>1</maxOccurs>'\
        '<nillable>true</nillable>'\
        '<binding>java.lang.String</binding>'\
        '</attribute>'\
        '<attribute>'\
        '<name>Geologie</name>'\
        '<minOccurs>0</minOccurs>'\
        '<maxOccurs>1</maxOccurs>'\
        '<nillable>true</nillable>'\
        '<binding>java.lang.String</binding>'\
        '</attribute>'\
        '<attribute>'\
        '<name>Vorname</name>'\
        '<minOccurs>0</minOccurs>'\
        '<maxOccurs>1</maxOccurs>'\
        '<nillable>true</nillable>'\
        '<binding>java.lang.String</binding>'\
        '</attribute>'\
        '<attribute>'\
        '<name>Nachname</name>'\
        '<minOccurs>0</minOccurs>'\
        '<maxOccurs>1</maxOccurs>'\
        '<nillable>true</nillable>'\
        '<binding>java.lang.String</binding>'\
        '</attribute>'\
        '<attribute>'\
        '<name>Institut</name>'\
        '<minOccurs>0</minOccurs>'\
        '<maxOccurs>1</maxOccurs>'\
        '<nillable>true</nillable>'\
        '<binding>java.lang.String</binding>'\
        '</attribute>'\
        '<attribute>'\
        '<name>Abteilung</name>'\
        '<minOccurs>0</minOccurs>'\
        '<maxOccurs>1</maxOccurs>'\
        '<nillable>true</nillable>'\
        '<binding>java.lang.String</binding>'\
        '</attribute>'\
        '<attribute>'\
        '<name>Projekt</name>'\
        '<minOccurs>1</minOccurs>'\
        '<maxOccurs>1</maxOccurs>'\
        '<nillable>false</nillable>'\
        '<binding>java.lang.String</binding>'\
        '</attribute>'\
        '<attribute>'\
        '<name>Domäne</name>'\
        '<minOccurs>1</minOccurs>'\
        '<maxOccurs>1</maxOccurs>'\
        '<nillable>false</nillable>'\
        '<binding>java.lang.String</binding>'\
        '</attribute>'\
        '<attribute>'\
        '<name>Kommentar</name>'\
        '<minOccurs>0</minOccurs>'\
        '<maxOccurs>1</maxOccurs>'\
        '<nillable>true</nillable>'\
        '<binding>java.lang.String</binding>'\
        '</attribute>'\
        '<attribute>'\
        '<name>site_id</name>'\
        '<minOccurs>0</minOccurs>'\
        '<maxOccurs>1</maxOccurs>'\
        '<nillable>true</nillable>'\
        '<binding>java.lang.Integer</binding>'\
        '</attribute>'\
        '<attribute>'\
        '<name>external_id</name>'\
        '<minOccurs>0</minOccurs>'\
        '<maxOccurs>1</maxOccurs>'\
        '<nillable>true</nillable>'\
        '<binding>java.lang.String</binding>'\
        '</attribute>'\
        '<attribute>'\
        '<name>centroid_x</name>'\
        '<minOccurs>0</minOccurs>'\
        '<maxOccurs>1</maxOccurs>'\
        '<nillable>true</nillable>'\
        '<binding>java.math.BigDecimal</binding>'\
        '</attribute>'\
        '<attribute>'\
        '<name>centroid_y</name>'\
        '<minOccurs>0</minOccurs>'\
        '<maxOccurs>1</maxOccurs>'\
        '<nillable>true</nillable>'\
        '<binding>java.math.BigDecimal</binding>'\
        '</attribute>'\
        '<attribute>'\
        '<name>srid</name>'\
        '<minOccurs>0</minOccurs>'\
        '<maxOccurs>1</maxOccurs>'\
        '<nillable>true</nillable>'\
        '<binding>java.lang.Integer</binding>'\
        '</attribute>'\
        '<attribute>'\
        '<name>geometry_type</name>'\
        '<minOccurs>0</minOccurs>'\
        '<maxOccurs>1</maxOccurs>'\
        '<nillable>true</nillable>'\
        '<binding>java.lang.String</binding>'\
        '</attribute>'\
        '<attribute>'\
        '<name>geom</name>'\
        '<minOccurs>1</minOccurs>'\
        '<maxOccurs>1</maxOccurs>'\
        '<nillable>false</nillable>'\
        '<binding>com.vividsolutions.jts.geom.Point</binding>'\
        '</attribute>'

    xml = '<featureType>'\
        '<name>' + filename + '</name>'\
        '<nativeName>' + filename + '</nativeName>'\
        '<namespace>'\
        '<name>' + workspace + '</name>'\
        '<atom:link xmlns:atom="http://www.w3.org/2005/Atom" rel="alternate" href="' + LOCAL_GEOSERVER + '/rest/namespaces/' + workspace + '.xml" type="application/xml"/>'\
        '</namespace>'\
        '<title>' + filename + '</title>'\
        '<keywords>'\
        '<string>features</string>'\
        '<string>' + filename + '</string>'\
        '</keywords>'\
        '<srs>EPSG:' + str(srid) + '</srs>'\
        '<projectionPolicy>FORCE_DECLARED</projectionPolicy>'\
        '<enabled>true</enabled>'\
        '<advertised>true</advertised>'\
        '<metadata>'\
        '<entry key="elevation">'\
        '<dimensionInfo>'\
        '<enabled>false</enabled>'\
        '</dimensionInfo>'\
        '</entry>'\
        '<entry key="JDBC_VIRTUAL_TABLE">'\
        '<virtualTable>'\
        '<name>' + filename + '</name>'\
        '<sql>' + query + \
        '</sql>'\
        '<escapeSql>false</escapeSql>'\
        '<keyColumn>id</keyColumn>'\
        '<geometry>'\
        '<name>Geometry</name>'\
        '<type>Point</type>'\
        '<srid>' + str(srid) + '</srid>'\
        '</geometry>'\
        '<geometry>'\
        '<name>geom</name>'\
        '<type>Point</type>'\
        '<srid>4326</srid>'\
        '</geometry>'\
        '</virtualTable>'\
        '</entry>'\
        '<entry key="time">'\
        '<dimensionInfo>'\
        '<enabled>false</enabled>'\
        '<defaultValue/>'\
        '</dimensionInfo>'\
        '</entry>'\
        '<entry key="cachingEnabled">false</entry>'\
        '</metadata>'\
        '<store class="dataStore">'\
        '<name>' + workspace + ':' + datastore + '</name>'\
        '<atom:link xmlns:atom="http://www.w3.org/2005/Atom" rel="alternate" href="' + LOCAL_GEOSERVER + '/rest/workspaces/' + workspace + '/datastores/' + datastore + '.xml" type="application/xml"/>'\
        '</store>'\
        '<maxFeatures>0</maxFeatures>'\
        '<numDecimals>0</numDecimals>'\
        '<overridingServiceSRS>false</overridingServiceSRS>'\
        '<skipNumberMatched>false</skipNumberMatched>'\
        '<circularArcPresent>false</circularArcPresent>'\
        '<attributes>' + attributes + \
        '</attributes>'\
        '</featureType>'

    return xml
