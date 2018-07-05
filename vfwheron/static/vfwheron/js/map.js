let data_style = null;
let wfsPointLayer = null;
let wfsPointSource = null;
let vector = null;
// let clusterSource = null;
let selectedIds = null;
let clusterLayer = null;
let filteredPoints = null;
// Style for the clusters
let styleCache = {};


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


    wfsPointSource = new ol.source.Vector({
        format: new ol.format.GeoJSON(),
        loader: function (extent) {
            console.log(' - - - - - - -  loader is running - - - - -  ')
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

    function PointFilter(feature) {
        console.log('wfsPointSource ', wfsPointSource);
        if (selectedIds) {
            console.log('wfsPointSource: ', wfsPointSource)
            console.log('wfsPointSource: ', wfsPointSource.getProperties())
            console.log('wfsPointSource: ', wfsPointSource.getState())
            console.log('wfsPointSource: ', wfsPointSource.getFeatures())
            console.log('filteredPoints: ', filteredPoints.getFeatures())
            filteredPoints.clear()
            console.log('filteredPoints: ', filteredPoints.getFeatures())
            var name = feature.getId();
            console.log(' -- - - - - -  in get filteredPoints  - -  -  - ', name)
            var id = parseInt(name.substr(wfsLayerName.length + 1, 8));
            if (selectedIds.includes(id)){
                console.log('selectedIds.includes(id): ', selectedIds.includes(id))
            }
        }
        return filteredPoints}

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

    // Cluster Source
/*
    function clusterSource() {
        console.log('wfsPointSource', wfsPointSource)
        return [new ol.source.Cluster({
            distance: 30,
            source: wfsPointSource
        })];
    }
*/
    if (!selectedIds) {
        filteredPoints = wfsPointSource;
    }

    // Cluster Source
    clusterSource = new ol.source.Cluster({
        distance: 30,
        source: filteredPoints//wfsPointSource//filteredPoints
    });

    // Animated cluster layer
    clusterLayer = new ol.layer.AnimatedCluster(
        {
            name: 'Cluster',
            source: clusterSource,
            animationDuration: 0,
            // Cluster style
            style: getStyle
        });

    // Style for selection
    let img = new ol.style.Circle(
        {
            radius: 8,
            stroke: new ol.style.Stroke({
                color: '#00BAEE',
                width: 0.1
            }),
            fill: new ol.style.Fill({
                color: "rgba(170, 221, 249,0.7)"
            })
        });
    let style1 = new ol.style.Style(
        {
            image: img,
            // Draw a link beetween points (or not)
            stroke: new ol.style.Stroke(
                {
                    color: '#AADDF9',
                    width: 1
                })
        });




    function getStyle(feature) {
        // PointFilter(feature);
        console.log('filteredPoints in getStyle: ', filteredPoints.getFeatures())
        let size = feature.get('features').length;
        let style = styleCache[size];
        console.log(' -- - - - - -  in get style  - -  -  - ', style, selectedIds, size)

        if (!style) {
            style = styleCache[size] = new ol.style.Style(
                {
                    image: new ol.style.Circle(
                        {
                            radius: Math.round(8 + 1.3 * Math.log(size)),
                            stroke: new ol.style.Stroke(
                                {
                                    color: '#00BAEE',
                                    width: 0.5
                                }),
                            fill: new ol.style.Fill(
                                {
                                    color: '#AADDF9'
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
        }

        return [style];
    }


    let map_tar = document.getElementById("map");
    let map = new ol.Map({
        // renderer: 'canvas',
        overlays: [metaData_Overlay],
        target: map_tar,
        layers: [mapLayer, clusterLayer], //vector], //wfsPointLayer],

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
    var selectCluster = new ol.interaction.SelectCluster(
        {	// Point radius: to calculate distance between the features
            pointRadius: 8.5,
            animate: 100,
            // Feature style when it springs apart
            featureStyle: style1,
            // selectCluster: false,	// disable cluster selection
            // Style to draw cluster when selected
            style: function (f) {
                console.log(' + + + + + + in select cluster + + + + ')
                var cluster = f.get('features');
                console.log('cluster: ', cluster);
        if (selectedIds) {
            console.log('there are selectedIds: ');//, selectedIds);
            var name = f.getId();
            console.log('name: ', name)
            var id = parseInt(name.substr(wfsLayerName.length + 1, 8));
            if (selectedIds.includes(id)) {


            }
        }
                if (cluster.length > 1) {
                    var s = getStyle(f);
                    if (ol.coordinate.convexHull) {
                        var coords = [];
                        for (i = 0; i < cluster.length; i++) coords.push(cluster[i].getGeometry().getFirstCoordinate());
                        // var chull = ol.coordinate.convexHull(coords);
                        s.push(new ol.style.Style( // spread datapoints around the center of the cluster
                            {
                                stroke: new ol.style.Stroke({color: "rgba(0,0,192,0.4)", width: 2}),
                                fill: new ol.style.Fill({color: "rgba(0,0,192,0.3)"}),
                                geometry: new ol.geom.Polygon([ol.coordinate.convexHull(coords)]),
                                zIndex: 1
                            }));
                    }
                    return s;
                }
                else {
                    return [
                        new ol.style.Style( // draw a circle around your selection
                            {
                                image: new ol.style.Circle(
                                    {
                                        stroke: new ol.style.Stroke({color: "rgba(0,73,120,0.5)", width: 2}),
                                        fill: new ol.style.Fill({color: "rgba(0,73,120,0.3)"}),
                                        radius: 15
                                    })
                            })];
                }
            }
        });

    map.addInteraction(selectCluster);
    map.on('pointermove', function (evt) {
        if (evt.dragging) {
            return;
        }
        let pixel = map.getEventPixel(evt.originalEvent);
        let hit = map.forEachLayerAtPixel(pixel, function (feature) {
                return feature;
            }, null, function (layer) {
                return layer === vector
            }
        );
        map.getTargetElement().style.cursor = hit ? 'pointer' : '';
    });

    // On selected => get feature in cluster and show info
    selectCluster.getFeatures().on(['add'], function (e) {
        var c = e.element.get('features');
        if (c.length == 1) {
            var feature = c[0];
            $(".infos").html("One feature selected...<br/>(id=" + feature.get('id') + ")");
        }
        else {
            $(".infos").text("Cluster (" + c.length + " features)");
        }
    });
    selectCluster.getFeatures().on(['remove'], function (e) {
        $(".infos").html("");
    })

}
