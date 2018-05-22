let data_style = null;
let wfsPointLayer = null;
let createStyle = null;
let wfsLayerName = 'new_ID_as_identifier_update';
// var feature = null;
let selectedIds = null;


//Create own base layer
function create_map() {
    const GEO_SERVER = DEMO_VAR+"/vfwheron/geoserver"
    let mapSource = new ol.source.XYZ({url: MAP_SERVER + "/osm/{z}/{x}/{y}.png"});
    let dataExt = JSON.parse(document.getElementById('dataExt').value); // bbox of available data
    // var data_style = JSON.parse(document.getElementById('data_style').value); // style for wms layer
    data_style = JSON.parse(document.getElementById('data_style').value)['data_style'];
// build the background map
    let mapLayer = new ol.layer.Tile({
        preload: Infinity,
        source: mapSource
    });
// get OSM in case local map is not loading:
    mapLayer.getSource().on('tileloaderror', function () {
        let source = new ol.source.OSM();
        mapLayer.setSource(source)
    });

    let mapView = new ol.View({
        center: ol.proj.fromLonLat([11.8810049, 50.0836865]),
        zoom: 6,
        maxZoom: 18,
        minZoom: 2,
    });
    mapView.animate({duration: 5000}, {easing: 'elastic'});
    // wms layer for use on a local machine
    let wmsPointSource = new ol.source.TileWMS({
        url: GEO_SERVER + '/wms',
        serverType: 'geoserver',
        params: {
            LAYERS: 'CAOS_update:new_ID_as_identifier_update', // 'CAOS:get_pointinfo' 'CAOS:pointdata'
            TILED: true,
            STYLES: data_style //STYLES: Light Blue Circle', 'CAOS:new_point',
        },
        name: 'wmsPointSource'
    });
    let wmsPointLayer = new ol.layer.Tile({
        source: wmsPointSource
    });

    let defaultStyle = new ol.style.Style({
        image: new ol.style.Circle({
            radius: 5,
            fill: new ol.style.Fill({
                color: 'lightblue'
            }),
            stroke: new ol.style.Stroke({
                color: 'blue',
                width: 0.1
            })
        })
    });

    /*   function styleFunction(feature){
           var name = feature.getId();
           var id = parseInt(name.substr(wfsLayerName.length+1,8))
           if (selection.includes(id)) {
               console.log('found: ', id)
               var style = new ol.style.Style({
                   image: new ol.style.Circle({
                       radius: 6,
                       fill: new ol.style.Fill({
                           color: 'blue'
                       }),
                       stroke: new ol.style.Stroke({
                           color: 'black',
                           width: 0.5
                       })
                   })
               })
           } else {
               style = defaultStyle
           }
           return style
         }*/
    function createStyle(feature) {
        var style;
        if (selectedIds) {
            var name = feature.getId();
            var id = parseInt(name.substr(wfsLayerName.length + 1, 8));
            if (selectedIds.includes(id)) {
                // console.log('found: ', id);
                var style = new ol.style.Style({
                    image: new ol.style.Circle({
                        radius: 8,
                        fill: new ol.style.Fill({
                            color: 'blue'
                        }),
                        stroke: new ol.style.Stroke({
                            color: 'black',
                            width: 0.5
                        })
                    })
                })
            } else {
                // defaultStyle.getImage().setRadius(3)
                // style = defaultStyle
            }
        } else {
            style = defaultStyle
        }

        return style
    };

  //  next thing to try: cluster data:
  /*var maxFeatureCount, wfsPointLayer;
      function calculateClusterInfo(resolution) {
        maxFeatureCount = 0;
        var features = wfsPointLayer.getSource().getFeatures();
        console.log('features: ', features.length)
        var feature, radius;
        for (var i = features.length - 1; i >= 0; --i) {
          feature = features[i];
          var originalFeatures = feature.get('features');
          console.log('originalFeatures: ', originalFeatures)
          var extent = ol.extent.createEmpty();
          var j, jj;
          for (j = 0, jj = originalFeatures.length; j < jj; ++j) {
            ol.extent.extend(extent, originalFeatures[j].getGeometry().getExtent());
          }
          maxFeatureCount = Math.max(maxFeatureCount, jj);
          radius = 0.25 * (ol.extent.getWidth(extent) + ol.extent.getHeight(extent)) /
              resolution;
          feature.set('radius', radius);
        }
      }

    var currentResolution;
    function styleFunction(feature, resolution) {
        if (resolution != currentResolution) {
          calculateClusterInfo(resolution);
          currentResolution = resolution;
        }
        var style;
        var size = feature.get('features').length;
        if (size > 1) {
          style = new ol.style.Style({
            image: new ol.style.Circle({
              radius: feature.get('radius'),
              fill: new ol.style.Fill({
                color: [255, 153, 0, Math.min(0.8, 0.4 + (size / maxFeatureCount))]
              })
            }),
            text: new ol.style.Text({
              text: size.toString(),
              fill: textFill,
              stroke: textStroke
            })
          });
        } else {
          var originalFeature = feature.get('features')[0];
          style = createStyle(originalFeature);
        }
        return style;
      }
*/

  // works more or less... but first fix sidebar
    /*var styleCache = {};
    function clusterStyle (feature) {
          var size = feature.get('features').length;
          var style = styleCache[size];
          if (!style) {
            style = new ol.style.Style({
              image: new ol.style.Circle({
                radius: 10,
                stroke: new ol.style.Stroke({
                  color: 'black',
                  width: 0.5
                }),
                fill: new ol.style.Fill({
                  color: 'blue'
                })
              }),
              text: new ol.style.Text({
                text: size.toString(),
                fill: new ol.style.Fill({
                  color: 'white'
                })
              })
            });
            styleCache[size] = style;
          }
          return style;
        }*/
    let wfsPointSource = new ol.source.Vector({
        format: new ol.format.GeoJSON(),
        loader: function (extent) {
            var url = GEO_SERVER + '/wfs/' + extent.join(',') +'/3857';
            var xhr = new XMLHttpRequest();
            xhr.open('GET', url);
            var onError = function () {
                console.log('Error in building vector wfsPointSource');
                wfsPointSource.removeLoadedExtent(extent);
            };
            xhr.onerror = onError;
            xhr.onload = function () {
                if (xhr.status == 200) {
                    wfsPointSource.addFeatures(
                        wfsPointSource.getFormat().readFeatures(xhr.responseText));
                } else {
                    console.log('error in onload for wfs');
                    onError();
                }
            };
            xhr.send();
        },
        strategy: ol.loadingstrategy.bbox
    });
// works more or less 2; first fix sidebar
/*    var clusterSource = new ol.source.Cluster({
        distance: 10,   //parseInt(distance.value, 10),
        source: wfsPointSource
    });*/

    wfsPointLayer = new ol.layer.Vector({
        source: wfsPointSource, //clusterSource,//wfsPointSource,
        renderMode: 'image',
        style: createStyle//clusterStyle//styleFunction//defaultStyle
    });


// Elements that make up the popup.
    let container = document.getElementById('popup');
    let content = document.getElementById('popup-content');
    let closer = document.getElementById('popup-closer');

// Create an metaData_Overlay to anchor the popup to the map.
    let metaData_Overlay = new ol.Overlay(/** @type {olx.OverlayOptions} */ ({
        element: container,
        autoPan: true,
        autoPanAnimation: {
            duration: 150
        }
    }));

    /** * Add a click handler to hide the popup. * @return {boolean} Don't follow the href. */
    closer.onclick = function () {
        metaData_Overlay.setPosition(undefined);
        closer.blur();
        return false;
    };

    let vectorSource = new ol.source.TileWMS({
        url: GEO_SERVER + '/wms',
        params: {LAYERS: 'LUBW:vfwheron_basiseinzugsgebiet'}
        // visible: False,
    });
    let vectorLayer = new ol.layer.Tile({
        source: vectorSource
    });

    let map_tar = document.getElementById("map");
    let map = new ol.Map({
        // renderer: 'canvas',
        overlays: [metaData_Overlay],
        target: map_tar,
        layers: [mapLayer, wfsPointLayer], // *works only your local geoserver
        // layers: [mapLayer, vectorLayer, wfsPointLayer], // *works only your local geoserver
        // layers: [mapLayer, vectorLayer, wmsPointLayer], // *datapoints on a local machine
        controls: [
            new ol.control.Zoom({duration: 300}),
            new ol.control.Attribution(),
            new ol.control.ZoomSlider(),
            new ol.control.MousePosition({
                projection: 'EPSG:4326',
                coordinateFormat: function (coord) {
                    return ol.coordinate.format(coord, ' {y}°N, {x}°E ', 4);
                }
            }),
            new ol.control.ScaleLine(),
            new ol.control.ZoomToExtent({ // zoom button
                label: 'Z',
                tipLabel: 'Zoom to your available data',
                extent: dataExt,
                duration: 2500,
                animate: ({duration: 5000} /*, {easing: 'elastic'}*/),
            })
        ],
        view: mapView//dataview
    });
    //mapView.fit(dataExt, {duration: 15000});
// get information about your data in a popup when you click on a data point in the map
    map.on('singleclick', showInfo);

    function showInfo(evt) {
        let coordinate = evt.coordinate;
        let clickedFeatures = map.getFeaturesAtPixel(evt.pixel);
        if (clickedFeatures != null) {
            let name = clickedFeatures[0].getId();
            let id = parseInt(name.substr(wfsLayerName.length + 1, 8));
            let properties = clickedFeatures[0].getProperties();
            let clickedKeys = clickedFeatures[0].getKeys();
            // TODO: CSS style überarbeiten
            let popupTableBeforeMeta = '<table id="popupTable"><td>'
            let popupTextStyle = '<style>table tr:nth-child(even)  {background-color: #c8ebee;}</style>'
            let popUpText = popupTableBeforeMeta + popupTextStyle + '<table id="metaTable">';
            for (var i = 0; i < clickedKeys.length; i++) {
                if (clickedKeys[i] != 'geometry_type' && clickedKeys[i] != 'srid' && clickedKeys[i] != 'centroid_x' &&
                    clickedKeys[i] != 'centroid_y' && clickedKeys[i] != 'external_id' && clickedKeys[i] != 'site_id' &&
                    clickedKeys[i] != 'geometry' && clickedKeys[i] != 'id') {
                    if (clickedKeys[i] == 'Vorname') {
                        let name = properties[clickedKeys[i]]
                    }
                    else if (clickedKeys[i] == 'Nachname') {
                        popUpText = popUpText + '<tr><td><b>Name</b></td><td>' + name + ' ' + properties[clickedKeys[i]] + '</td></tr>'
                    } else {
                        popUpText = popUpText + '<tr><td><b>' + clickedKeys[i] + '</b></td><td>' + properties[clickedKeys[i]] + '</td></tr>'
                    }
                }
            }
            let buttons = '<a><b><input id="show_data_preview" class="respo-btn-block" type="submit" ' +
                'onclick=\"show_preview(\''+id+'\')\" value="Preview" data-toggle="tooltip" ' +
                'title="Attention! Loading the preview might take a while."></b></a>' +
                '<a><b><input class="respo-btn-block respo-btn-block:hover" type="submit" ' +
                'onclick=\"workspace_dataset(\''+id+'\')\" value="Pass dataset to datastore" data-toggle="tooltip" ' +
                'title="Put dataset to session datastore"></b></a>';
            let popupTableAfterMeta = popUpText + '</table>' + buttons
            let img_preview = '</td><td><p id = "preview_img" ></p></td></table>'
            content.innerHTML =  popupTableAfterMeta + img_preview;
            metaData_Overlay.setPosition(coordinate);
        } else {
            metaData_Overlay.setPosition(undefined) // removes popup from map when clicked on map
        }
    };

    // select data with doubleclick
    //map.on('doubleclick', selectDataset);

    /*comment the following in your development environment to avoid error messages*/
    map.on('pointermove', function (evt) {
        if (evt.dragging) {
            return;
        }
        let pixel = map.getEventPixel(evt.originalEvent);
        let hit = map.forEachLayerAtPixel(pixel, function (feature, layer) {
                return feature;
            }, null, function (layer) {
                return layer === wfsPointLayer
            }
        );
        map.getTargetElement().style.cursor = hit ? 'pointer' : '';
    });

}


