let data_style = null;
let wfsPointLayer = null;
let wfsPointSource = null;
let vector = null;
let clusterSource = null;
let createStyle = null;
let selectedIds = null;
let filteredWfs = null;


//Create own base layer
function create_map() {
    const GEO_SERVER = DEMO_VAR + "/vfwheron/geoserver";
    let mapSource = new ol.source.XYZ({url: MAP_SERVER + "/osm/{z}/{x}/{y}.png"});
    let dataExt = JSON.parse(document.getElementById('dataExt').value); // bbox of available data
    // var data_style = JSON.parse(document.getElementById('data_style').value); // style for wms layer
    data_style = JSON.parse(document.getElementById('data_style').value)['data_style'];
    let wfsLayerName = document.getElementById('data_layer').value;
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
            radius: 8,
            fill: new ol.style.Fill({
                color: '#AADDF9'
            }),
            stroke: new ol.style.Stroke({
                color: '#00BAEE',
                width: 0.1
            })
        })
    });
     const invisibleFill = new ol.style.Fill({
        color: 'rgba(255, 255, 255, 0.01)'
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
        console.log('createStyle')
        feature = feature.get('features')[0];
        var style;
        if (selectedIds) {
            console.log('there are selectedIds: ');//, selectedIds);
            var name = feature.getId();
            var id = parseInt(name.substr(wfsLayerName.length + 1, 8));
            if (selectedIds.includes(id)) {
                console.log('found id: ', id);
                var style = new ol.style.Style({
                    image: new ol.style.Circle({
                        radius: 10,
                        fill: new ol.style.Fill({
                            color: '#AADDF9'
                        }),
                        stroke: new ol.style.Stroke({
                            color: 'black',
                            width: 1.5
                        })
                    })
                })
            } else {
                console.log('!!! !! ! Else von create style ');
                // defaultStyle.getImage().setRadius(3)
                // style = defaultStyle
            }
        } else {
            style = defaultStyle
        }

        return style
    }

    // works more or less... but first fix sidebar
    /*    let styleCache = {};
        function clusterStyle (feature) {
            let size = feature.get('features').length;
            let style = styleCache[size];
              if (!style) {
                style = new ol.style.Style({
                  image: new ol.style.Circle({
                    radius: Math.round(8+1.3*Math.log(size)),
                    stroke: new ol.style.Stroke({
                      color: 'green',
                      width: 0.1
                    }),
                    fill: new ol.style.Fill({
                      color: 'blue', //'dodgerblue'
                    })
                  }),
                  text: new ol.style.Text({
                    text: size.toString(),
                      font: '12px helvetica,sans-serif',
                    fill: new ol.style.Fill({
                      color: 'white'
                    })
                  })
                });
                styleCache[size] = style;
              }
              console.log('style: ', style)
              return style;
            }*/

    var maxFeatureCount;

    function calculateClusterInfo(resolution) {
        console.log('calculateClusterInfo')
        maxFeatureCount = 0;
        var features = vector.getSource().getFeatures();
        console.log('calculateClusterInfo')
        // console.log(' + + + features: ', features)
        var feature, radius;
        for (var i = features.length - 1; i >= 0; --i) {
            feature = features[i];
            var originalFeatures = feature.get('features');
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

// TODO: Check why styleFunction is called twice and correct it
    function styleFunction(feature, resolution) {
        console.log('styleFunction')
        if (resolution != currentResolution) {
            console.log('if styleFunction')
            calculateClusterInfo(resolution);
            currentResolution = resolution;
        }
        var style;
        var size = feature.get('features').length;
        if (size > 1) {
            var name = feature.getId();
            // console.log('selection feature: ', feature)
            // console.log('selection feature: ', feature.get("features"))
           /* console.log('selection feature: ', feature.getProperties())
            var id = parseInt(name.substr(wfsLayerName.length+1,8))
            if (selection.includes(id)) {
               console.log('selection name, id', name, id)
           }*/
            console.log('features: in styleFunction ', feature.get('features'))
            style = new ol.style.Style({
                image: new ol.style.Circle({
                    radius: Math.round(8 + 1.3 * Math.log(size)),
                    stroke: new ol.style.Stroke({
                        color: '                  color: \'black\'\n',
                        width: 0.1
                    }),
                    fill: new ol.style.Fill({
                        color: '#AADDF9', //'dodgerblue'
                    })
                }),
                text: new ol.style.Text({
                    text: size.toString(),
                    font: '12px helvetica,sans-serif',
                    fill: new ol.style.Fill({
                        color: 'black'
                    })
                })
            });
        } else {
            var originalFeature = feature.get('features')[0];
            console.log('else styleFunction', originalFeature)
            style = createStyle(originalFeature);
        }
        return style;
    }

    wfsPointSource = new ol.source.Vector({
        format: new ol.format.GeoJSON(),
        loader: function (extent) {
            var url = GEO_SERVER + '/wfs/' + wfsLayerName + '/' + extent.join(',') + '/3857';
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

    function filterSource() {
        console.log('filterSource')
    // function filterSource(feature, selection) {
        if (!filteredWfs) {
            filteredWfs = wfsPointSource;
        } else {
            if (selectedIds) {
                console.log('wfsPointSource: ', wfsPointSource)
                console.log('wfsPointSource: ', wfsPointSource.getProperties())
                console.log('wfsPointSource: ', wfsPointSource.getState())
                console.log('wfsPointSource: ', wfsPointSource.getFeatures())
            var name = wfsPointSource.getId();
            var id = parseInt(name.substr(wfsLayerName.length + 1, 8));
            if (selectedIds.includes(id)) {
                console.log('found: ', id);


            } else {
                // defaultStyle.getImage().setRadius(3)
                // style = defaultStyle
            }
        }

        }
    }
    // filterSource();
    // create_map.filterSource = filterSource;

// works more or less 2; first fix sidebar
    vector = new ol.layer.Vector({
        source: new ol.source.Cluster({
            distance: 35,   //parseInt(distance.value, 10),
            source: wfsPointSource,//filteredWfs,


        /*
                        clusterSource = new ol.source.Cluster({
                    distance: 30,   //parseInt(distance.value, 10),
                    source: wfsPointSource,
        */

/*                geometryFunction: function(feature) {
                    // console.log('* ** * * feature: ', feature)
                    if (selectedIds){
                        var name = feature.getId();
                        var id = parseInt(name.substr(wfsLayerName.length + 1, 8));
                        if (selectedIds.includes(id)) {
                            console.log('**** name: ', name)
                            console.log('id: ', id)
                            console.log('feature.getGeometry(): ', feature.getGeometry())
                            feature.removeFeature

                        }
                        // console.log('feature.getProperties: ', feature.get("features"))
                        // console.log('feature.getProperties: ', feature.get("features").length)
            /!*            for (let i = 0; i < feature.get("features").length; i++) {
                            let name =feature.get("features")[i].getId()
                            let id = parseInt(name.substr(wfsLayerName.length + 1, 8));
                            if (selectedIds.includes(id)) {
                                console.log(' *  da * ')
                            }
                        }*!/
                    }
                    // console.log('feature.getGeometry(): ', feature.getGeometry())
                    return feature.getGeometry();
                }*/
                }),
        style: styleFunction,
    });


    /*    wfsPointLayer = new ol.layer.Vector({
            source: clusterSource,//wfsPointSource,
            renderMode: 'image',
            style: clusterStyle//createStyle//clusterStyle//styleFunction//defaultStyle
        });*/


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
        layers: [mapLayer, vector], //wfsPointLayer],
        interactions: ol.interaction.defaults().extend([new ol.interaction.Select({
          condition: function(evt) {
            return  evt.type == 'singleclick';
          },
          style: createStyle
        })]),

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

    function selectStyleFunction(feature) {
        const styles = [new ol.style.Style({
          image: new ol.style.Circle({
            radius: feature.get('radius'),
            fill: invisibleFill
          })
        })];
        const originalFeatures = feature.get('features');
        let originalFeature;
        for (let i = originalFeatures.length - 1; i >= 0; --i) {
          originalFeature = originalFeatures[i];
          // styles.push(defaultStyle(originalFeature));
          styles.push(defaultStyle); // TODO: make a new default style function
        }
        return styles;
      }

    function showInfo(evt) {
        if (map.getFeaturesAtPixel(evt.pixel) != null) {
            let clickedFeatures = map.getFeaturesAtPixel(evt.pixel)[0].getProperties().features;
            if (clickedFeatures.length > 1) {
                console.log('TODO: build list for preview', clickedFeatures)
            } else {
                let name = clickedFeatures[0].getId();
                let id = parseInt(name.substr(wfsLayerName.length + 1, 8));
                let properties = clickedFeatures[0].getProperties();
                let clickedKeys = clickedFeatures[0].getKeys();
                // TODO: CSS style überarbeiten
                let popupTableBeforeMeta = '<table id="popupTable"><td>';
                let popupTextStyle = '<style>table tr:nth-child(even)  {background-color: #c8ebee;}</style>';
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
                    'onclick=\"show_preview(\'' + id + '\')\" value="Preview" data-toggle="tooltip" ' +
                    'title="Attention! Loading the preview might take a while."></b></a>' +
                    '<a><b><input class="respo-btn-block respo-btn-block:hover" type="submit" ' +
                    'onclick=\"workspace_dataset(\'' + id + '\')\" value="Pass dataset to datastore" data-toggle="tooltip" ' +
                    'title="Put dataset to session datastore"></b></a>';
                let popupTableAfterMeta = popUpText + '</table>' + buttons;
                let img_preview = '</td><td><p id = "preview_img" ></p></td></table>';
                content.innerHTML = popupTableAfterMeta + img_preview;
                metaData_Overlay.setPosition(evt.coordinate);
            }
        } else {
            metaData_Overlay.setPosition(undefined) // removes popup from map when clicked on map
        }
    }

    // select data with doubleclick
    //map.on('doubleclick', selectDataset);

    map.on('pointermove', function (evt) {
        if (evt.dragging) {
            return;
        }
        let pixel = map.getEventPixel(evt.originalEvent);
        let hit = map.forEachLayerAtPixel(pixel, function (feature, layer) {
                return feature;
            }, null, function (layer) {
                return layer === vector
            }
        );
        map.getTargetElement().style.cursor = hit ? 'pointer' : '';
    });

}


