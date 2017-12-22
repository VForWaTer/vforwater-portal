var data_style = null;
var wfsPointLayer = null;
var createStyle = null;
var wfsLayerName = 'ID_as_identifier';
// var feature = null;
var selectedIds = null;

//Create own base layer
function create_map() {
    var mapSource = new ol.source.XYZ({url: window.location.origin + "/osm/{z}/{x}/{y}.png"});
    var dataExt = JSON.parse(document.getElementById('dataExt').value); // bbox of available data
    // var data_style = JSON.parse(document.getElementById('data_style').value); // style for wms layer
    data_style = JSON.parse(document.getElementById('data_style').value)['data_style'];
// build the background map
    var mapLayer = new ol.layer.Tile({
        preload: Infinity,
        source: mapSource
    });
// get OSM in case local map is not loading:
    mapLayer.getSource().on('tileloaderror', function () {
        var source = new ol.source.OSM();
        mapLayer.setSource(source)
    });

    var mapView = new ol.View({
        center: ol.proj.fromLonLat([11.8810049, 50.0836865]),
        zoom: 6,
        maxZoom: 18,
        minZoom: 2
    });

    // wms layer for use on a local machine
    var wmsPointSource = new ol.source.TileWMS({
        url: 'https://vforwater-gis.scc.kit.edu/geoserver/wms',
        serverType: 'geoserver',
        params: {
            LAYERS: 'CAOS:ID_as_identifier', // 'CAOS:get_pointinfo' 'CAOS:pointdata'
            TILED: true,
            STYLES: data_style //STYLES: Light Blue Circle', 'CAOS:new_point',
        },
        name: 'wmsPointSource'
    });
    var wmsPointLayer = new ol.layer.Tile({
        source: wmsPointSource
    });

    var defaultStyle = new ol.style.Style({
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
                console.log('found: ', id);
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

    var wfsPointSource = new ol.source.Vector({
        format: new ol.format.GeoJSON(),
        loader: function (extent) {
            var url = 'https://vforwater-gis.scc.kit.edu/geoserver/CAOS/wfs?service=WFS&version=2.0.0&' +
            // var url = 'http://127.0.0.1:8080/geoserver/CAOS/wfs?service=WFS&version=2.0.0&' + // for local geoserver
                'request=GetFeature&typename=CAOS:' + wfsLayerName + '&outputFormat=application/json&srsname=EPSG:3857' +
                '&bbox=' + extent.join(',') + ',EPSG:3857';
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
    wfsPointLayer = new ol.layer.Vector({
        source: wfsPointSource,
        renderMode: 'image',
        style: createStyle //defaultStyle
    });
    // console.log('wfsPointLayer.getStyle(): ', wfsPointLayer.getStyle());

// Elements that make up the popup.
    var container = document.getElementById('popup');
    var content = document.getElementById('popup-content');
    var closer = document.getElementById('popup-closer');

// Create an overlay to anchor the popup to the map.
    var overlay = new ol.Overlay(/** @type {olx.OverlayOptions} */ ({
        element: container,
        autoPan: true,
        autoPanAnimation: {
            duration: 150
        }
    }));

    /** * Add a click handler to hide the popup. * @return {boolean} Don't follow the href. */
    closer.onclick = function () {
        overlay.setPosition(undefined);
        closer.blur();
        return false;
    };

    var vectorSource = new ol.source.TileWMS({
        url: 'https://vforwater-gis.scc.kit.edu/geoserver/wms',
        params: {LAYERS: 'LUBW:vfwheron_basiseinzugsgebiet'}
        // visible: False,
    });
    var vectorLayer = new ol.layer.Tile({
        source: vectorSource
    });

    var map_tar = document.getElementById("map");
    var map = new ol.Map({
        // renderer: 'canvas',
        overlays: [overlay],
        target: map_tar,
        layers: [mapLayer, vectorLayer, wfsPointLayer], // *works only your local geoserver
        // layers: [mapLayer, vectorLayer, wmsPointLayer], // *datapoints on a local machine
        controls: [
            new ol.control.Zoom(),
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
                tipLabel: 'Auf die verfügbaren Daten zoomen',
                extent: dataExt
            })
        ],
        view: mapView//dataview
    });

// get information about your data in a popup when you click on a data point in the map
    map.on('singleclick', showInfo);

    function showInfo(evt) {
        var coordinate = evt.coordinate;
        var clickedFeatures = map.getFeaturesAtPixel(evt.pixel);
        if (clickedFeatures != null) {
            var name = clickedFeatures[0].getId();
            var id = parseInt(name.substr(wfsLayerName.length + 1, 8));
            var properties = clickedFeatures[0].getProperties();
            var clickedKeys = clickedFeatures[0].getKeys();
            // TODO: CSS style überarbeiten
            var popupTextStyle = '<style>table tr:nth-child(even) {background-color: #c8ebee;}</style>'
            var popUpText = popupTextStyle + '<table id="metaTable">';
            // var popUpText = '<table class="respo-table">';
            for (var i = 0; i < clickedKeys.length; i++) {
                if (clickedKeys[i] != 'geometry_type' && clickedKeys[i] != 'srid' && clickedKeys[i] != 'centroid_x' &&
                    clickedKeys[i] != 'centroid_y' && clickedKeys[i] != 'external_id' && clickedKeys[i] != 'site_id' &&
                    clickedKeys[i] != 'geometry') {
                    if (clickedKeys[i] == 'Vorname') {
                        var name = properties[clickedKeys[i]]
                    }
                    else if (clickedKeys[i] == 'Nachname') {
                        popUpText = popUpText + '<tr><td><b>Name</b></td><td>' + name + ' ' + properties[clickedKeys[i]] + '</td></tr>'
                    } else {
                        popUpText = popUpText + '<tr><td><b>' + clickedKeys[i] + '</b></td><td>' + properties[clickedKeys[i]] + '</td></tr>'
                    }
                }
            }
            console.log('evt: ', clickedKeys)
            var buttons = /*' <a> <input type="button" class="button " onclick="toggleLayer(vectorMap)" value="Vorschau">'+*/
                '<a><b><input id="show_metafiltered_data" class="respo-btn-block" type="submit" ' +
                'onclick="onclick_show_datasets_func()" value="Vorschau" data-toggle="tooltip" ' +
                'title="Achtung! Das Laden der Vorschau kann lange dauern."></b></a>' +
                '<a><b><input class="respo-btn-block respo-btn-block:hover" type="submit" ' +
                'onclick=\"workspace_dataset(\''+id+'\')\" value="Datensatz übernehmen" data-toggle="tooltip" ' +
                'title="Den Datensatz in den Workspace übernehmen"></b></a>'
            content.innerHTML = popUpText + '</table>' + buttons;
            overlay.setPosition(coordinate);

            // '<tr onclick=\"getClickedUserObject(\'' + dict["value"][key].Initials + '\')\">';
        } else {
            overlay.setPosition(undefined) // removes popup from map when clicked on map
        }
    };


    // select data with doubleclick
    //map.on('doubleclick', selectDataset);

    /*comment the following in your development environment to avoid error messages*/
    map.on('pointermove', function (evt) {
        if (evt.dragging) {
            return;
        }
        var pixel = map.getEventPixel(evt.originalEvent);
        var hit = map.forEachLayerAtPixel(pixel, function (feature, layer) {
                return feature;
            }, null, function (layer) {
                return layer === wfsPointLayer
            }
        );
        map.getTargetElement().style.cursor = hit ? 'pointer' : '';
    });

}
