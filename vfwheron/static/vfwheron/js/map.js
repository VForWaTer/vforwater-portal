let wfsLayerName;

//Create own base layer
function create_map() {
    const GEO_SERVER = DEMO_VAR + "/vfwheron/geoserver";
    let mapSource = new ol.source.XYZ({url: MAP_SERVER + "/osm/{z}/{x}/{y}.png"});
    let dataExt = JSON.parse(document.getElementById('dataExt').value); // bbox of available data
    wfsLayerName = document.getElementById('data_layer').value;
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
    })

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

    // Animated cluster layer
    clusterLayer = new ol.layer.AnimatedCluster({
        name: 'Cluster',
        source: new ol.source.Cluster({
            distance: 30,
            source: wfsPointSource
        }),
        animationDuration: 0,
        // Cluster style
        style: getStyle
    });

    // Style for selection/single circles around cluster
    let img = new ol.style.Circle({
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
            // Draw a link beetween points
            stroke: new ol.style.Stroke({
                color: '#AADDF9',
                width: 1
            })
        });


    let styleCache = {}

    function getStyle(feature) {
        let size = feature.get('features').length;
        let style = styleCache[size];
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
        layers: [mapLayer, clusterLayer],

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
    map.on('singleclick', buildPopup);

    function buildPopup(evt) {
        console.log('evt: ', evt)
        if (map.getFeaturesAtPixel(evt.pixel) != null) {
            let clickedFeatures = map.getFeaturesAtPixel(evt.pixel)[0].getProperties().features;
            console.log('clickedFeatures: ', clickedFeatures)
            // TODO: CSS style überarbeiten
            let popupTableBeforeMeta = '<table id="popupTable"><td>';
            let popupTextStyle = '<style>table tr:nth-child(even)  {background-color: #c8ebee;}</style>';
            let popUpText = popupTableBeforeMeta + popupTextStyle + '<table id="metaTable">';
            if (clickedFeatures.length > 0) { // check how many datasets are selected
                let ids = [];
                let name, id;
                // bulid list with selection to send to server
                for (let i = 0; i < clickedFeatures.length; i++) {
                    console.log('TODO: build list for preview', clickedFeatures[i]);
                    name = clickedFeatures[i].getId();
                    id = parseInt(name.substr(wfsLayerName.length + 1, 8));
                    console.log('id: ', id)
                    ids.push(id)
                }
                // let name = clickedFeatures[0].getId();
                // let id = parseInt(name.substr(wfsLayerName.length + 1, 8));
                // console.log('id: ', id)

                // request info from server
                $.ajax({
                    url: DEMO_VAR + "/vfwheron/menu",
                    dataType: 'json',
                    data: {
                        show_info: JSON.stringify(ids),
                        // show_info: JSON.stringify(parseInt(name.substr(wfsLayerName.length + 1, 8))),
                        'csrfmiddlewaretoken': csrf_token,
                    }, // data sent with the post request
                    success: function (json) {
                        try {
                            let properties = json.get;
                            let lastProperty = json.get[json.get.length];
                            let buttons = [];
                            let valueLen;
                            let buttonId = [];
                            // loop over "properties"dict with metadata, build columns
                            for (let j in properties) {
                                // console.log('j: : ', j, eval('json.get["' + j + '"]'), eval('json.get["' + j + '"]').length);
                                let values = eval('json.get["' + j + '"]');
                                valueLen = values.length;
                                popUpText = popUpText + '<tr><td><b>' + j + '</b></td>';
                                // loop over dict values and build rows
                                for (let k = 0; k < valueLen; k++) {
                                    popUpText = popUpText + '<td>' + values[k] + '</td>';
                                    if (j.toLowerCase() == 'id') {
                                        buttonId.push(values[k])
                                    }
                                }
                                popUpText = popUpText + '</tr>'
                            }
                            popUpText = popUpText + '<tr><td><b></b></td>';
                            // build buttons for each dataset
                            for (let k = 0; k < valueLen; k++) {
                                popUpText = popUpText + '<td><a><b><input id="show_data_preview' + buttonId[k].toString() + '" class="respo-btn-block" type="submit" ' +
                                    'onclick=\"show_preview(\'' + buttonId[k] + '\')\" value="Preview" data-toggle="tooltip" ' +
                                    'title="Attention! Loading the preview might take a while."></b></a>' +
                                    '<a><b><input class="respo-btn-block respo-btn-block:hover" type="submit" ' +
                                    'onclick=\"workspace_dataset(\'' + buttonId[k] + '\')\" value="Pass to datastore" data-toggle="tooltip" ' +
                                    'title="Put dataset to session datastore"></b></a></td>';
                            }

                            let popupTableAfterMeta = popUpText + '</table>';
                            let img_preview = '</td><td><p id = "preview_img" ></p></td></table>';
                            content.innerHTML = popupTableAfterMeta + img_preview;
                            metaData_Overlay.setPosition(evt.coordinate);

                        } catch (err) {
                            document.getElementById("popup-content").removeChild(document.getElementById("loader"));
                            content.innerHTML = '<td><a style="background-color:White;color:Red;"><b> Error: Unable to load data</td></a></b>'
                            console.error(err); // TODO: remove for production
                        }
                    }

                });
                // TODO: reduce width of window for loader
                // Create spinning loader while getting meta data from server
                content.innerHTML = '<div id="loader" class="loader"></div>';
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
                var cluster = f.get('features');
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
                return layer === clusterLayer
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
