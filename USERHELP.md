# User Instructions

#### The V-FOR-WaTer web portal offers data and tools for environmental sciences or any other interested. The following describes how to make use of the V-FOR-WaTer web portal.

## Log in

Your browser has to accept cookies to log in.

## Access Data

One can filter data from the V-FOR-WaTer server on the start page (`Home`). One can always come back there with a click on the V-FOR-WaTer Logo on the top left or accessed from the top bar.

Filtering is implementet inclusive, which means what you select is an requirement for the filtered data. In case of timerange and area, not only data within is selected, but all datasets that has data within the selected range in time and space.

To filter data one can start in the `filter menu` on the sidebar or by drawing on the map. While the order of clicking in the `filter menu` or on the map doesn't influence the result, it is advisable to start filtering in the `filter menu`, as selecting on the map can be very restrictive; yet there is no indication which of the filter options have results in the selected area.

To select an area, one can
1. upload own `GeoJSON` files, with the `upload` button on top of the sidebar.
2. zoom into the map until the Merit Catchments appear. The amount of data strongly reduces the performance on the website, so the layer is hidden until a certain level of zoom. To us the Merit Catchments click in one, an the respective upstream catchments will be selected as well.
3. use the `Draw menu`, that can be opened on top of the left sidebar, or by clicking on the `+` in the box in the upper left corner of the map. In the `Draw menu`, one has different options to define an area:
   - The `finger` symbol lets one click anywhere on the map. The request is processed on the server, and only a polygon with a strongly restricted amount of edge points is used.
   - The `square` lets one draw a square on the map.
   - The `XXXX` symbol lets one draw a polygon.
   - The `square with pen` lets one manipulate an already existing contour.
   - The `shopping cart` lets one store the actual area for later use.
   - With the `wastebin` one can remove the current contour from the map.

Please note, as default meta information is only shown for data one is allowed to access (`is FAIR`). To show other datasets as well remove the checkmark from the respective filter option. Then one can send a request to the data owner to get access to restricted data.

The filtered result is visible on the map (default), or in a tabular view, that can be accessed through the button `XXXX` above the map.

Datasets on the map are primarily visualized as points. When many points are close to each other, they are visualized as a cluster. The number shows the datasets within each cluster, the size of the point also increases with the number of datasets in the cluster.

To select a single dataset one can choose it in the tabular view (`send to datastore`), or click on it in the map. When you click on it you see the meta information of the  respective dataset. On the bottom of this list you find two buttons. One to get a preview, and one to select the dataset.

## Run tools

You can run tools in the `Workspace` from the top bar.

# Contributing

## Data Model

If you want to contribute, you'll have to ensure, that your meta-data fits
the V-FOR-WaTer data model. In practice this means, you'll have to produce a
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
