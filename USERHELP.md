# User Instructions

## Log in

Your browser has to accept cookies to log in. 

## Access your Data

You can filter data in the `Home` page, which can be accessed from the top bar. First you should restrict the datasets 
in the sidebar by using the `filter menu`. Please note, that only meta information for data you are allowed to access 
is visible yet.

To select a distinct dataset you have to choose it on the map. When you click on it you see the meta information of the 
respective dataset. On the bottom of this list you find two buttons. One to get a preview, and one to select the dataset.

## Run your tools

You can run tools in the `Workspace` from the top bar.

# Contributing

## Data Model

If you want to contribute, you'll have to ensure, that your meta-data fits 
the V-FOR-WaTer data model. In practice this means, yu'll have to produce a 
minimum amount of meta data and fit additional information into our scheme of
optional meta data.

### Minimum Metadata Requirements

  * **Name**  -  specify a name for your dataset
  * **Variable** - What kind of data does your record hold, refer to the 
  variables section to learn more
  * **Owner** - Who owns the data, can be a person or an institution
  * **license** - attach a license to your data, refer to the license section
   to learn more.
  * **attribution** - how shall the use of your data be attributed?
  * **location** + **srid**, the location of the data (as WKT) and the 
  identifier for the used coordinate reference system (EPSG number)
  
Additionally, your meta data will be associated to at least one project. This
project has a name and will link the metadata entries by a hierarchical 
_domain_ structure. This is basically a hierarchical labeling for 
structuring the data in a project specific way.
The metadata entries can also be grouped by different domains in different 
ways by associating more than one project to them.
  
### Optional Metadata

In addition, the following metadata can be stored in V-FOR-WaTer:

  * **external_id** - can be any ID, e.g. to associate the V-FOR-WaTer entry 
  with thrid party versions of the same data.
  * **support** and **spacing**  -  specify the scale your data is describing
  * **sensor**:
    * sensor_name, manufacturer, valid_until, last_configured, 
    documentation_url and comment
  * **site** information:
    * site_name, elevation, rel_height (sensor height relative to the 
    elevation), orientation, slope, landuse, comment
  * **soil** and geology parameter:
    *  soil_type, geology, porosity, field_capacity, residual_moisture

### variables

Only time series are available so far.
The following variables can be stored in V-FOR-WaTer.

  * air temperature
  * realtive humidity
  * air pressure
  * precipitation
  * terrain height (??? why?!)
  * saturation
  * wind direction
  * soil temperature
  * matric potential
  * water level
  * specific conductivity
  * water temperature
  * net radiation
  * wind speed
  * sap flow
  * discharge
  * electric conductivity
  * water content

### licenses

The following license can be linked to the data so far:

  * [CC BY 2.0 DE](https://creativecommons.org/licenses/by/2.0/de/)
  * [CC BY-ND 3.0 DE](https://creativecommons.org/licenses/by-nd/3.0/de/)
  * [CC BY-NC 3.0 DE](https://creativecommons.org/licenses/by-nc/3.0/de/)
  * [CC BY-NC-ND 3.0](https://creativecommons.org/licenses/by-nc-nd/3.0/de/)
  * [CC BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/de/)
  * [CC BY-SA 3.0 DE](https://creativecommons.org/licenses/by-sa/3.0/de/)
  * [dl-de/by-2-0](https://www.govdata.de/dl-de/by-2-0) 
  * [dl-de/zero-2.0](https://www.govdata.de/dl-de/zero-2-0)
  * [dl-de/by-nc-1-0](https://www.govdata.de/dl-de/by-nc-1-0)
