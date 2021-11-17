let zoomToExt;
let wfsLayerName;
let olmap, hit_cL, clusterLayer, hiddenLayer;
let selectCluster;
let wfsPointSource;

/** build style for cluster **/
let styleCache = {};

function clusterStyle(feature) {
    let size = feature.get('features').length;
    let style = styleCache[size];
    if (!style) {
        style = styleCache[size] = new ol.style.Style({
            image: new ol.style.Circle({
                radius: Math.round(8 + 1.3 * Math.log(size)),
                stroke: new ol.style.Stroke({
                    color: '#00BAEE',
                    width: 0.5
                }),
                fill: new ol.style.Fill({
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

/**
 * Get a modal (pop up) with some information about the datasets at the clicked location.
 * @param {array} ids
 * @param {int} page
 */
function buildMapModal(ids, page) {
    $.ajax({
        url: DEMO_VAR + "/home/short_info_pagination",
        dataType: 'html',
        data: {
            datasets: JSON.stringify(ids), page: page,
            'csrfmiddlewaretoken': csrf_token,
        }, /** data sent with the post request **/
    })
        .done(function (html) {
            document.getElementById("infomodal_paginationTable").innerHTML = html;
            document.getElementById('infomodal_paginationTable').style.display = "block";
        })
        .fail(function (bug) {
            console.error('Bug! TODO: Remove this Layer!: ', bug)
            closeMapModal();
        })
}

/** Fetch V-FOR-WaTer base layer **/
function create_map() {
    const GEO_SERVER = DEMO_VAR + "/home/geoserver";
    let mapSource = new ol.source.XYZ({
        attributions: [gettext("Map data from") + ' <a href="https://openstreetmap.org/copyright">OpenStreetMap</a>, ' +
        'SRTM | ' + gettext("Map style from") + ' <a href="https://www.vforwater.de/">V-FOR-WaTer</a> '],
        url: MAP_SERVER + "/osm/{z}/{x}/{y}.png"
    });
    let dataExt = ol.proj.transformExtent(JSON.parse(document.getElementById('dataExt').value),
        'EPSG:4326', 'EPSG:3857'); // bbox of available data (extent, source, destination)

    wfsLayerName = document.getElementById('data_layer').value;
    if (wfsLayerName.search("Error") !== -1) {
        console.error(wfsLayerName)
    }
    /** build the background map **/
    let mapLayer = new ol.layer.Tile({
        preload: Infinity,
        source: mapSource
    });
    /** get OSM/OTM in case local map is not loading: **/
    mapLayer.getSource().on('tileloaderror', function () {
        let source = new ol.source.XYZ({
            attributions: ['Map data from <a href="https://openstreetmap.org/copyright">OpenStreetMap</a>, ' +
            'SRTM | Map style from <a href="https://opentopomap.org/">OpenTopoMap</a> ' +
            '<a href="https://creativecommons.org/licenses/by-sa/3.0/">(CC-BY-SA)</a> '],
            url: 'https://{a-c}.tile.opentopomap.org/{z}/{x}/{y}.png'
        });

        mapLayer.setSource(source)
    });

    let mapView = new ol.View({
        center: ol.proj.fromLonLat([11.8810049, 50.0836865]),
        zoom: 6,
        maxZoom: 18,
        minZoom: 2,
    });
    mapView.animate({duration: 5000}, {easing: 'elastic'});

    /** get data points from server **/
    wfsPointSource = new ol.source.Vector({
        format: new ol.format.GeoJSON(),
        loader: function (extent) {
            fetch(GEO_SERVER + '/wfs/' + wfsLayerName + '/' + extent.join(',') + '/3857',

                )
                .then(function (response) {
                    if (response.ok) {
                        return response.text();
                    } else {
                        return Promise.reject(response);
                    }
                })
                .then(function (response) {
                    wfsPointSource.addFeatures(wfsPointSource.getFormat().readFeatures(response));
                })
                .catch(function (error) {
                    console.warn('No result for selected area. Unable to build vector layer.');
                    // console.log('Error in building vector wfsPointSource: ', error);
                    wfsPointSource.removeLoadedExtent(extent);
                })
        },
        strategy: ol.loadingstrategy.bbox
    });

    // TODO: Bei Gelegenheit mal sentinel Daten einführen
    //     url = https://sgx.geodatenzentrum.de/wms_sentinel2_de?service=wms&version=1.3.0&request=GetMap&Layers=sentinel2-de:rgb&STYLES=&CRS=EPSG:25832&bbox=500000,5700000,550000,5750000&width=500&Height=500&Format=image/png&TIME=2019

    /** Make (animated) cluster layer from data points **/
    clusterLayer = new ol.layer.AnimatedCluster({
        name: 'Cluster',
        className: 'cluster-layer',
        source: new ol.source.Cluster({
            distance: 30,
            source: wfsPointSource
        }),
        animationDuration: 0,
        /** Cluster style  **/
        style: clusterStyle
    });
    hiddenLayer = new ol.layer.VectorImage({
        className: 'hidden-layer',
        source: wfsPointSource,
    });



    /** functionality for zoom to extent button **/
    zoomToExt = new ol.control.ZoomToExtent({ // zoom button
        label: 'Z',
        tipLabel: gettext('Zoom to your available data'),
        // extent: testExt,  // eddy footprint testextent
        extent: dataExt,
        duration: 2500,
        animate: ({duration: 5000} /*, {easing: 'elastic'}*/),
    });

    /** build app for box with draw buttons **/
    window.cApp = {};
    let cApp = window.cApp;
    cApp.drawControls = function () {
        let element = document.createElement('div');
        element.className = 'custom-control ol-unselectable ol-control';
        element.appendChild(document.getElementById('drawfilter'));
        element.appendChild(document.getElementById('closed_drawfilter'));
        ol.control.Control.call(this, {
            element: element
        });
    };
    ol.inherits(cApp.drawControls, ol.control.Control);

    /** Initialise map **/
    let map_tar = document.getElementById("map");
    olmap = new ol.Map({
        // renderer: 'canvas',
        target: map_tar,
        layers: [mapLayer, clusterLayer],
        // interactions: ol.interaction.defaults({doubleClickZoom: false}).extend([dcz]),

        controls: [
            new ol.control.Zoom({
                zoomInTipLabel: gettext("Zoom in"),
                zoomOutTipLabel: gettext("Zoom out"),
                duration: 300
            }),
            new ol.control.Attribution({collapsed: false, collapsible: false,}),
            new ol.control.ZoomSlider(),
            new ol.control.MousePosition({
                projection: 'EPSG:4326',
                coordinateFormat: function (coord) {
                    return ol.coordinate.format(coord, ' {y}°N, {x}°E ', 4);
                }
            }),
            new ol.control.ScaleLine(),
            new cApp.drawControls,
            zoomToExt,
        ],
        view: mapView//dataview
    });

    /** get information about your data in a popup when you click on a data point in the map **/
    olmap.on('singleclick', checkMode);

    /** check what is clicked **/
    function checkMode(evt) {
        let clickedFeatures, ids, cleanedids, wfsLen;
        if (hit_cL) {
            content.innerHTML = '';
            try {
                content.innerHTML = '<div id="loader" class="loader"></div>';
                wfsLen = wfsLayerName.length;
                clickedFeatures = olmap.getFeaturesAtPixel(evt.pixel)[0].getProperties().features;
                ids = clickedFeatures.map(i => parseInt(i.getId().substr(wfsLen + 1, 8)));
                cleanedids = ids.filter(value => {return !Number.isNaN(value);});
                buildMapModal(cleanedids, 1);
                mapmodal.style.display = "block";
            } catch (err) {
                content.innerHTML = '<div id="loader">Failed to load your selection</div>';
                console.log('err: ', err)
            }

        } else {
            metaData_Overlay.setPosition(undefined) // removes popup from map when clicked on map
        }
    }

    /** select data with doubleclick **/
    //olmap.on('doubleclick', selectDataset);
    // TODO: Cluster gives error when click on sketched polygon. Not used yet anyways, so uncommented until usefull
    /*    selectCluster = new ol.interaction.SelectCluster(
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
                            let coords = [];
                            let l = cluster.length;
                            for (i = 0; i < l; i++) coords.push(cluster[i].getGeometry().getFirstCoordinate());
                            s.push(new ol.style.Style({ // spread datapoints around the center of the cluster
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
                            new ol.style.Style({ // draw a circle around your selection
                                image: new ol.style.Circle({
                                    stroke: new ol.style.Stroke({color: "rgba(0,73,120,0.5)", width: 2}),
                                    fill: new ol.style.Fill({color: "rgba(0,73,120,0.3)"}),
                                    radius: 15
                                    })
                            })];
                    }
                }
            });
        olmap.addInteraction(selectCluster);*/

    /** change cursor to pointer when hover over data **/
    olmap.on('pointermove', function (evt) {
        if (evt.dragging) {
            return;
        }
        // let pixel = olmap.getEventPixel(evt.originalEvent);
        hit_cL = olmap.forEachLayerAtPixel(evt.pixel, function (feature) {
                return feature;
            },
            {
                layerFilter: function (layer) {
                    // console.log('+++++ layer: ', layer === clusterLayer)
                    // return layer === vector
                    return layer === clusterLayer
                }
            }
        );
        olmap.getTargetElement().style.cursor = hit_cL ? 'pointer' : '';
    });

    // On selected => get feature in cluster and show info
    /*    selectCluster.getFeatures().on(['add'], function (e) {
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
        })*/

}

// function storeBtn(listIndex) {
/**
 * Create a html button to request a dataset or pass it to the data store, depending on embargo.
 * @param {int} ssid
 * @param {string} embargo "True" or "False"
 */
function storeBtn(ssid, embargo) {
    if (embargo === "False" || UNBLOCKED_IDS.includes(ssid)) {
        return '<a><b><input class="w3-btn-block w3-btn-block:hover store-button" type="submit" ' +
            'onclick=\"workspace_dataset(\'' + ssid + '\')\" ' +
            'value="' + gettext("Pass to datastore") + '" data-toggle="tooltip" ' +
            'title="' + gettext("Put dataset to session datastore.") + '"></b></a>'
    } else {
        return '<a><b><input class="w3-btn-block w3-btn-block:hover request-button" type="submit" ' +
            'onclick=\"requestDataset(\'' + ssid + '\')\" ' +
            'value="' + gettext("Send request") + '" data-toggle="tooltip" ' +
            'title="' + gettext("Send an access request to the data owner.") + '"></b></a>'
    }
}


function requestDataset(dataId) {
    console.warn('Noch nicht implementiert.')
}
