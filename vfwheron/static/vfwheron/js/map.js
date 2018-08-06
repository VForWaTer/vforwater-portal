let zoomToExt;
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
            let url = GEO_SERVER + '/wfs/' + wfsLayerName + '/' + extent.join(',') + '/3857';
            let xhr = new XMLHttpRequest();
            xhr.open('GET', url);
            let onError = function () {
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

// Elements that make up the popup.
    let container = document.getElementById('popup');
    let content = document.getElementById('popup-content');
    let paginat = document.getElementById('popup-paginat')
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
    let clusterLayer = new ol.layer.AnimatedCluster({
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


    let styleCache = {};

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

    zoomToExt = new ol.control.ZoomToExtent({ // zoom button
        label: 'Z',
        tipLabel: 'Zoom to your available data',
        extent: dataExt,
        duration: 2500,
        animate: ({duration: 5000} /*, {easing: 'elastic'}*/),
    });

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
            zoomToExt,
        ],
        view: mapView//dataview
    });

// get information about your data in a popup when you click on a data point in the map
    map.on('singleclick', buildPopup);

    function buildPopup(evt) {
        if (map.getFeaturesAtPixel(evt.pixel) != null) {
            // Create spinning loader while getting meta data from server
            content.innerHTML = '<div id="loader" class="loader"></div>';
            metaData_Overlay.setPosition(evt.coordinate);

            let numOfCol = 5;
            let clickedFeatures = map.getFeaturesAtPixel(evt.pixel)[0].getProperties().features;
            let pos = evt.coordinate;
            if (clickedFeatures.length > 0 && clickedFeatures.length <= numOfCol) { // check how many datasets are selected
                let ids = [];
                let name, id;
                // bulid list with selection to send to server
                for (let i = 0; i < clickedFeatures.length; i++) {
                    name = clickedFeatures[i].getId();
                    id = parseInt(name.substr(wfsLayerName.length + 1, 8));
                    ids.push(id);
                }
                popupContent(ids, pos)
                paginat.innerHTML = []

            } else if (clickedFeatures.length > numOfCol) {
                let page = 1;
                let name, id;
                let ids = [];
                let idDict = {1:[]};
                for (let i = 0, j = 0; i < clickedFeatures.length; i++, j++) {
                    if (j >= numOfCol) {
                        j = 0;
                        page++;
                        idDict[page]=[];
                    }
                    name = clickedFeatures[i].getId();
                    id = parseInt(name.substr(wfsLayerName.length + 1, 8));
                    ids.push(id);
                    idDict[page].push(id);

                }
                popupContent(idDict[1], pos);

                // add paginatation to popup:
                let pagi = '';
                for (let i = 1; i <= page; i++) {
                    if (i == 1) {
                        pagi = '<li id="pagi'+i+'" class="active"><a><input type="submit" id="popBtn" class="respo-btn-simple"' +
                            'onclick=\"popupContentvfw(\''+idDict[i]+','+i+'\')\" value="' + i + '"></a></li>';
                    } else {
                        pagi = pagi + '<li id="pagi'+i+'"><a><input type="submit" class="respo-btn-simple"' +
                            'onclick=\"popupContentvfw(\''+idDict[i]+','+i+'\')\" value="' + i + '"></a></li>';
                    }
                }
                paginat.innerHTML = pagi;
                // end of paginatation
                // TODO: need a list to click to next objects, to select ids
            }


        } else {
            metaData_Overlay.setPosition(undefined) // removes popup from map when clicked on map
        }

    }
    function popupContent(ids, pos) {
    // TODO: CSS style überarbeiten
        let popupTableBeforeMeta = '<table id="popupTable"><td>';
        let popUpText = popupTableBeforeMeta +
            '<style>table tr:nth-child(even) {background-color: #c8ebee;}</style>' +
            '<table id="metaTable">';

        // request info from server
        $.ajax({
            url: DEMO_VAR + "/vfwheron/menu",
            dataType: 'json',
            data: {
                show_info: JSON.stringify(ids),
                'csrfmiddlewaretoken': csrf_token,
            }, // data sent with the post request
            success: function (json) {
                    document.getElementById('popup-content').innerHTML = buildPopupText(json, popUpText);
                    // content.innerHTML = buildPopupText(json, popUpText);
                    metaData_Overlay.setPosition(pos);
            }

        });

    }
    // TODO: buildPopupText is the same as buildPopupTextvfw.js ==> figure out how(where) to use only one of the two functions for both cases
    function buildPopupText(json, popUpText) {
        let properties = json.get;
        let valueLen;
        let buttonId = [];
        // loop over "properties" dict with metadata, build columns
        for (let j in properties) {
            let values = eval('properties["' + j + '"]');
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
        return popupTableAfterMeta + img_preview;
    }

    // select data with doubleclick
    //map.on('doubleclick', selectDataset);
    let selectCluster = new ol.interaction.SelectCluster(
        {	// Point radius: to calculate distance between the features
            pointRadius: 8.5,
            animate: 100,
            // Feature style when it springs apart
            featureStyle: style1,
            // selectCluster: false,	// disable cluster selection
            // Style to draw cluster when selected
            style: function (f) {
                let cluster = f.get('features');
                if (cluster.length > 1) {
                    let s = getStyle(f);
                    if (ol.coordinate.convexHull) {
                        var coords = [];
                        for (i = 0; i < cluster.length; i++) coords.push(cluster[i].getGeometry().getFirstCoordinate());
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
        let c = e.element.get('features');
        if (c.length == 1) {
            let feature = c[0];
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
