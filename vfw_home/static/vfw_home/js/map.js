vfw.map.vars.hit_cL = {};
let olmap;
// TODO: Check if clusterlayer has to be global!
//let selectCluster;
// let dcz = new ol.interaction.DoubleClickZoom();

/** build style for cluster **/
vfw.map.style.clusterStyle = function (feature) {
    let size = feature.get('features').length;
    let style = vfw.map.style.cache[size];
    if (!style) {
        style = vfw.map.style.cache[size] = new ol.style.Style({
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
 * Whan clicked on a dataset o the map, then get a modal (pop up) with some information about the datasets
 * at the clicked location.
 * @param {array} ids
 * @param {int} page
 */
vfw.map.buildMapModal = function (ids, page) {
    $.ajax({
        url: vfw.var.DEMO_VAR + "/home/short_info_pagination",
        dataType: 'html',
        data: {
            datasets: JSON.stringify(ids), page: page,
            'csrfmiddlewaretoken': vfw.var.csrf_token,
        }, /** data sent with the post request **/
    })
        .done(function (html) {
            vfw.map.html.mapModal.style.display = "block";
            document.getElementById("infomodal_paginationTable").innerHTML = html;
            document.getElementById('infomodal_paginationTable').style.display = "block";
        })
        .fail(function (bug) {
            console.error('Bug! TODO: Remove this Layer!: ', bug)
            vfw.map.closeMapModal();
        })
        .always(function () {
            vfw.html.loaderOverlayOff();
        })
}

vfw.map.source.getSourceVector = function (layerName) {

}

/** get catchments from server **/
vfw.map.source.wfsMeritCatchment = new ol.source.Vector({
    format: new ol.format.GeoJSON(),
    // format: new ol.format.MVT(),  // TODO: MVT is supposed to be faster than JSON. Figur how to use it.
    loader: function (extent) {
        let layerName = 'merit_catch_test'
        fetch(vfw.var.DEMO_VAR + '/home/geoserver/wfs/' + layerName + '/'
            + extent.join(',') + '/3857',
            // {body: {'csrfmiddlewaretoken': csrf_token},  body is only for post!
            // credentials: 'same-origin'}
        )
            .then(function (response) {
                if (response.ok) {
                    return response.text();
                } else {
                    return Promise.reject(response);
                }
            })
            .then(function (response) {
                vfw.map.source.wfsMeritCatchment.addFeatures(vfw.map.source.wfsMeritCatchment.getFormat().readFeatures(response));
            })
            .catch(function (error) {
                console.warn('No result for selected area. Unable to build vector layer of Catchments.');
                // console.log('Error in building vector vfw.map.source.wfsPointSource: ', error);
                vfw.map.source.wfsMeritCatchment.removeLoadedExtent(extent);
            })
    },
    strategy: ol.loadingstrategy.bbox
});
/** get catchments in coarse scale from server **/
vfw.map.source.wfsCoarseMeritCatchment = new ol.source.Vector({
    format: new ol.format.GeoJSON(),
    // format: new ol.format.MVT(),  // TODO: MVT is supposed to be faster than JSON. Figur how to use it.
    loader: function (extent) {
        let layerName = 'merit_catch_test_v2'
        fetch(vfw.var.DEMO_VAR + '/home/geoserver/wfs/' + layerName + '/'
            + extent.join(',') + '/3857',
        )
            .then(function (response) {
                if (response.ok) {
                    return response.text();
                } else {
                    return Promise.reject(response);
                }
            })
            .then(function (response) {
                vfw.map.source.wfsCoarseMeritCatchment.addFeatures(vfw.map.source.wfsCoarseMeritCatchment.getFormat().readFeatures(response));
            })
            .catch(function (error) {
                console.warn('No result for selected area. Unable to build vector layer of coarse Catchments.');
                vfw.map.source.wfsCoarseMeritCatchment.removeLoadedExtent(extent);
            })
    },
    strategy: ol.loadingstrategy.bbox
});
/** get rivers from server **/
// vfw.map.source.wfsMeritRiver = new ol.source.VectorTile({
//       source: new ol.source.VectorTile({
//         tilePixelRatio: 1, // oversampling when > 1
//         tileGrid: ol.tilegrid.createXYZ({maxZoom: 19}),
//         format: new ol.format.MVT(),
//         url: vfw.var.DEMO_VAR + '/home/geoserver/gwc/service/tms/1.0.0/metacatalogdev:merit_river_test@EPSG%3A3857@pbf/{z}/{x}/{-y}.pbf'
//       })
    /*format: new ol.format.GeoJSON(),
    loader: function (extent) {
        let url = vfw.var.DEMO_VAR + '/home/geoserver/gwc/service/tms/1.0.0/merit_river_test@EPSG%3A3857@pbf/{z}/{x}/{-y}.pbf'
        fetch(vfw.var.DEMO_VAR + '/home/geoserver/wfs/' + vfw.map.vars.wfsLayerName + '/'
            + extent.join(',') + '/3857',
            // {body: {'csrfmiddlewaretoken': csrf_token},  body is only for post!
            // credentials: 'same-origin'}
        )
            .then(function (response) {
                if (response.ok) {
                    return response.text();
                } else {
                    return Promise.reject(response);
                }
            })
            .then(function (response) {
                vfw.map.source.wfsPointSource.addFeatures(vfw.map.source.wfsPointSource.getFormat().readFeatures(response));
            })
            .catch(function (error) {
                console.warn('No result for selected area. Unable to build vector layer.');
                // console.log('Error in building vector vfw.map.source.wfsPointSource: ', error);
                vfw.map.source.wfsPointSource.removeLoadedExtent(extent);
            })
    },
    strategy: ol.loadingstrategy.bbox*/
// });
vfw.map.source.wfsMeritRiver = new ol.source.Vector({
    format: new ol.format.GeoJSON(),
    // format: new ol.format.MVT(),  // TODO: MVT is supposed to be faster than JSON. Figur how to use it.
    loader: function (extent) {
        let layerName = 'merit_river_test'
        fetch(vfw.var.DEMO_VAR + '/home/geoserver/wfs/' + layerName + '/'
            + extent.join(',') + '/3857',
            // {body: {'csrfmiddlewaretoken': csrf_token},  body is only for post!
            // credentials: 'same-origin'}
        )
            .then(function (response) {
                if (response.ok) {
                    return response.text();
                } else {
                    return Promise.reject(response);
                }
            })
            .then(function (response) {
                vfw.map.source.wfsMeritRiver.addFeatures(vfw.map.source.wfsMeritRiver.getFormat().readFeatures(response));
            })
            .catch(function (error) {
                console.warn('No result for selected area. Unable to build vector layer of rivers.');
                // console.log('Error in building vector vfw.map.source.wfsPointSource: ', error);
                vfw.map.source.wfsMeritRiver.removeLoadedExtent(extent);
            })
    },
    strategy: ol.loadingstrategy.bbox
});
/** get data points from server **/
vfw.map.source.wfsPointSource = new ol.source.Vector({
    format: new ol.format.GeoJSON(),
    loader: function (extent) {
        fetch(vfw.var.DEMO_VAR + '/home/geoserver/wfs/' + vfw.map.vars.wfsLayerName + '/'
            + extent.join(',') + '/3857',
            // {body: {'csrfmiddlewaretoken': csrf_token},  body is only for post!
            // credentials: 'same-origin'}
        )
            .then(function (response) {
                if (response.ok) {
                    return response.text();
                } else {
                    return Promise.reject(response);
                }
            })
            .then(function (response) {
                vfw.map.source.wfsPointSource.addFeatures(vfw.map.source.wfsPointSource.getFormat().readFeatures(response));
            })
            .catch(function (error) {
                console.warn('No result for selected area. Unable to build vector layer with data points.');
                // console.log('Error in building vector vfw.map.source.wfsPointSource: ', error);
                vfw.map.source.wfsPointSource.removeLoadedExtent(extent);
            })
    },
    strategy: ol.loadingstrategy.bbox
});
/** get the different background maps **/
// Create vfw style map
vfw.map.source.vfwSource = new ol.source.XYZ({
    attributions: [gettext("Map data from") + ' <a href="https://openstreetmap.org/copyright">OpenStreetMap</a>, ' +
    'SRTM | ' + gettext("Map style from") + ' <a href="https://www.vforwater.de/">V-FOR-WaTer</a> '],
    url: vfw.var.MAP_SERVER + "/osm/{z}/{x}/{y}.png"
});
// Create a OpenStreetMap layer
vfw.map.source.osmSource = new ol.source.XYZ({
    maxZoom: 19,
    attributions: ['&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'],
    url: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'
});
// vfw.map.source.osmSource = new ol.source.OSM({
//     attributions: ['Map © <a href="https://openstreetmap.org/copyright">OpenStreetMap</a>'],
// });

// Create a satellite imagery layer
vfw.map.source.opentopoSource = new ol.source.XYZ({
    attributions: ['Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
    '<a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> ' +
    '(<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'],
    maxZoom: 17,
    url: 'https://tile.opentopomap.org/{z}/{x}/{y}.png'
});
vfw.map.layer.openTopo = new ol.layer.Tile({
    name: 'OpenTopoMap',
    preload: Infinity,
    baseLayer: true,
    visible: false,
    source: vfw.map.source.opentopoSource,
});
// vfw.map.layer.waterColor = new ol.layer.Tile({
//     title: "Watercolor",
//     baseLayer: true,
//     visible: false,
//     source: new ol.source.StadiaMaps({
//         layer: 'stamen_watercolor'
//     })
// });
const osmLayer = new ol.layer.Tile({
    title: "OSM",
    baseLayer: true,
    visible: false,
    source: new ol.source.OSM(),
});

// create a Sentinel-2 basemap layer
// vfw.map.source.sentinel2 = new ol.Layer.WMS({
//     url: 'https://sgx.geodatenzentrum.de/wms_sen2europe?service=wms&version=1.3.0&request=GetMap&Layers=sentinel2-de:rgb&STYLES=&CRS=EPSG:25832&bbox=500000,5700000,550000,5750000&width=500&Height=500&Format=image/png&TIME=2018'
    // 'https://sgx.geodatenzentrum.de/wms_sen2europe?service=wms&version=1.3.0&request=GetMap&Layers=sentinel2-de:rgb&STYLES=&CRS=EPSG:3857&Format=image/png&TIME=2018'
// })
// see: http://sg.geodatenzentrum.de/web_bkg_webmap/doc/factories.html
// see: https://www.ldbv.bayern.de/file/pdf/10544/Diplomarbeit_Wengerter.pdf


/** Fetch V-FOR-WaTer base layer **/
vfw.map.create_map = function () {

    // let basemapControl = {
    //     "Open Street map": vfw.map.source.osmSource,
    //     "VFW map": vfw.map.source.vfwSource,
    //     "Open Topo map": vfw.map.source.opentopoSource
    // };

    let dataExt = ol.proj.transformExtent(vfw.var.DATA_EXT, 'EPSG:4326', 'EPSG:3857'); // bbox of available data (extent, source, destination)

    vfw.map.vars.wfsLayerName = vfw.var.DATA_LAYER;
    if (vfw.map.vars.wfsLayerName.search("Error") !== -1) {
        console.error(vfw.map.vars.wfsLayerName)
        let tabBtn = {'currentTarget': document.getElementById('tableTab')}
        toggleMapTableFilter(tabBtn, 'paginationTable');
        filter_pagination();
    }
    /** build the background map **/
    const backgroundLayer = new ol.layer.Tile({
        name: 'Default Map',
        preload: Infinity,
        baseLayer: true,
        visible: true,
        source: vfw.map.source.vfwSource,
    });
    /** get OSM/OTM in case local map is not loading: **/
    backgroundLayer.getSource().on('tileloaderror', function () {
        backgroundLayer.setSource(vfw.map.source.opentopoSource)
    });

    let mapView = new ol.View({
        center: ol.proj.fromLonLat([11.8810049, 50.0836865]),
        zoom: 6,
        maxZoom: 18,
        minZoom: 2,
    });
    mapView.animate({duration: 5000}, {easing: 'elastic'});


    // TODO: Bei Gelegenheit mal sentinel Daten einführen
    //     url = https://sgx.geodatenzentrum.de/wms_sentinel2_de?service=wms&version=1.3.0&request=GetMap&Layers=sentinel2-de:rgb&STYLES=&CRS=EPSG:25832&bbox=500000,5700000,550000,5750000&width=500&Height=500&Format=image/png&TIME=2019

    /** Make (animated) cluster layer from data points **/
    const clusterLayer = new ol.layer.AnimatedCluster({
        name: 'Data Clusters',
        className: 'cluster-layer',
        source: new ol.source.Cluster({
            distance: 30,
            source: vfw.map.source.wfsPointSource,
            crossOrigin: 'anonymous',
        }),
        animationDuration: 0,
        /** Cluster style  **/
        style: vfw.map.style.clusterStyle
    });
    // vfw.map.layer.hidden = new ol.layer.VectorImage({
    //     className: 'hidden-layer',
    //     source: vfw.map.source.wfsPointSource,
    // });

    /** create a separate layer for merit Rivers **/
    const meritRiverLayer = new ol.layer.Vector({
        style: {
            // 'fill-color': ['string', ['get', 'COLOR'], '#eee'],
            'stroke-color': 'rgba(98,165,241,0.89)',
            'stroke-width': 2,
        },
        source: vfw.map.source.wfsMeritRiver,
        minZoom: 7,
        name: 'Merit River',
        className: 'cluster-layer',
        visible: false,
    });
    /** create a separate layer for merit Rivers **/
    const meritCatchmentLayer = new ol.layer.Vector({
        style: {
            // 'fill-color': ['string', ['get', 'COLOR'], '#eee'],
            'stroke-color': 'rgba(44,51,180,0.89)',
            'stroke-width': 2,
        },
        source: vfw.map.source.wfsMeritCatchment,
        minZoom: 8,
        name: 'Merit Catchment',
        className: 'cluster-layer',
        visible: false,
    });
/** create a separate layer for merit Rivers **/
    const meritCoarseCatchmentLayer = new ol.layer.Vector({
        style: {
            // 'fill-color': ['string', ['get', 'COLOR'], '#eee'],
            'stroke-color': 'rgba(55,19,110,0.89)',
            'stroke-width': 3,
        },
        source: vfw.map.source.wfsCoarseMeritCatchment,
        minZoom: 2,
        name: 'coarse Merit Catchment',
        className: 'cluster-layer',
        visible: false,
    });


    /* /!** Style for selection/single circles around cluster  **!/
     // used for Eddy footprint
         let img = new ol.style.Circle({
             radius: 8,
             stroke: new ol.style.Stroke({
                 color: '#00021d',
                 // color: '#00BAEE',
                 width: 0.1
             }),
             fill: new ol.style.Fill({
                 color: "rgb(53,161,220)"
             })
         });
         let style1 = new ol.style.Style({
             image: img,
             // Draw a link beetween points
             stroke: new ol.style.Stroke({
                 color: '#AADDF9',
                 width: 1
             })
         });
 */
    /*

         // TODO: Eddy footprint example
         /!** Load a 1-band rasterimage 'testlayer' from geoserver and render it as map **!/
        let testExt = [1227200, 6035000, 1229000, 6036000]
        let testlayer = new ol.layer.Image({
            extent: testExt,
            source: new ol.source.ImageWMS({
                url: 'http://localhost:8080/geoserver/wms',
                // params: {'LAYERS': 'testworkspace:Graswang_footprint_0011030'},
                // params: {'LAYERS': 'testworkspace:Graswang_footprint_0010300'},
                // params: {'LAYERS': 'NewRaster:Graswang_footprint_0012330'},
                // params: {'LAYERS': 'NewRaster:Graswang_footprint_0011530'},
                // params: {'LAYERS': 'NewRaster:Graswang_footprint_0010000'},

                params: {'LAYERS': 'NewRaster:Graswang_footprint_0010600'},
                // params: {'LAYERS': 'NewRaster:Graswang_footprint_0011630'},
                // params: {'LAYERS': 'NewRaster:Graswang_footprint_0010930'},
                // params: {'LAYERS': 'NewRaster:Graswang_footprint_0011930'},
                // params: {'LAYERS': 'NewRaster:Graswang_footprint_0010900'},
                // params: {'LAYERS': 'NewRaster:Graswang_footprint_0012100'},
                ratio: 1,
                serverType: 'geoserver',
            }),
        })
        let testpoint = new ol.Feature({
            // geometry: new ol.geom.Point([1240114.37, 6016817.06]),
            // geometry: new ol.geom.Point([47.571, 11.032]),
            geometry: new ol.geom.Point(ol.proj.fromLonLat([11.0326, 47.5708])),
            name: 'Graswang tower',
        });
        testpoint.setStyle(style1);
        let testPointSource = new ol.source.Vector({features: [testpoint],});
        let testPointLayer = new ol.layer.Vector({source: testPointSource,});

    */

    /** functionality for zoom to extent button **/
    vfw.map.control.zoomToExt = new ol.control.ZoomToExtent({ // zoom button
        label: 'Z',
        tipLabel: gettext('Zoom to your available data'),
        // extent: testExt,  // eddy footprint testextent
        extent: dataExt,
        duration: 2500,
        animate: ({duration: 5000} /*, {easing: 'elastic'}*/),
    });

    /** build Class for box with draw buttons **/
    class DrawControls extends ol.control.Control {
        constructor(opt_options) {
            const element = document.createElement('div');
            element.className = 'custom-control ol-unselectable ol-control';
            element.appendChild(document.getElementById('drawfilter'));
            element.appendChild(document.getElementById('closed_drawfilter'));
            super({
                element: element,
            });
        }
    }

    /** Initialise map **/
    let map_tar = document.getElementById("map");
    olmap = new ol.Map({
        // renderer: 'canvas',
        target: map_tar,
        layers: [
            // vfw.map.layer.waterColor,
            osmLayer, vfw.map.layer.openTopo,
            backgroundLayer,
            meritRiverLayer, meritCatchmentLayer, meritCoarseCatchmentLayer,
            clusterLayer,
        ],
        // layers: [mapLayer, testPointLayer, testlayer, clusterLayerNew],  // Eddy footprint testlayer
        // interactions: ol.interaction.defaults({doubleClickZoom: false}).extend([dcz]),
        // interactions: ol.interaction.defaults().extend([featureselect, featuremodify]),

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
            new DrawControls(),
            vfw.map.control.zoomToExt,
            new ol.control.LayerPopup(),
            // new ol.control.LayerSwitcher(),
        ],
        view: mapView//dataview
    });

    /** get information about your data in a popup when you click on a data point in the map **/
    olmap.on('singleclick', checkMode);

    /** check what is clicked and open a modal with information about data **/
    function checkMode(evt) {
        let clickedFeatures, ids, cleanedids, wfsLen;
        // TODO: This code works only on the cluster layer. For other geometries/layers this function must be adjusted!
        clusterLayer.getFeatures(evt.pixel).then((features) => {
            if (features[0]) {
                vfw.html.loaderOverlayOn();
                wfsLen = vfw.map.vars.wfsLayerName.length;
                // clickedFeatures = olmap.getFeaturesAtPixel(evt.pixel)[0].getProperties().features;
                clickedFeatures = features[0].getProperties().features;
                ids = clickedFeatures.map(i => parseInt(i.getId().substr(wfsLen + 1, 8)));
                cleanedids = ids.filter(value => {
                    return !Number.isNaN(value);
                });
                vfw.map.buildMapModal(cleanedids, 1);
            }
        })
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
        clusterLayer.getFeatures(evt.pixel).then((features) => {
            olmap.getTargetElement().style.cursor = features[0] ? 'pointer' : '';
        })
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

/**
 * Create a html button to request a dataset or pass it to the data store, depending on embargo.
 * @param {int} ssid
 * @param {string} embargo "True" or "False"
 */
vfw.map.createStoreBtn = function (ssid, embargo) {
    if (embargo === "False" || vfw.map.UNBLOCKED_IDS.includes(ssid)) {
        return '<a><b><input class="w3-btn-block w3-btn-block:hover store-button" type="submit" ' +
            'onclick=\"vfw.sidebar.workspaceDataset(\'' + ssid + '\')\" ' +
            'value="' + gettext("Pass to datastore") + '" data-toggle="tooltip" ' +
            'title="' + gettext("Put dataset to session datastore.") + '"></b></a>'
    } else {
        return '<a><b><input class="w3-btn-block w3-btn-block:hover request-button" type="submit" ' +
            'onclick=\"vfw.map.requestDataset(\'' + ssid + '\')\" ' +
            'value="' + gettext("Send request") + '" data-toggle="tooltip" ' +
            'title="' + gettext("Send an access request to the data owner.") + '"></b></a>'
    }
}


vfw.map.showGroupBtn = function (ssids) {
    let btn;
    if (ssids.length > 1) {
        btn = '<a><b><input class="w3-btn-block w3-btn-block:hover" type="submit" ' +
            'onclick=\"vfw.map.buildMapModal(' + JSON.stringify(ssids) + ', 1); vfw.html.infoModal.close()\" ' +
            'value="' + gettext("Show group") + '" data-toggle="tooltip" ' +
            'title="' + gettext("Show all ") + ssids.length + gettext(" associated datasets.") + '"></b></a>'
    } else {
        btn = '<a><b><div class="request-button">"' + gettext("No other group members") + '"</div></b></a>'
    }
    return btn
}


// TODO: Distinguish if (some) of datasets have embargo. Give option to send grouped requests.
vfw.map.storeGroupBtn = function (ssids, embargo) {
    if (ssids.length > 1 && (embargo === "False" || vfw.map.UNBLOCKED_IDS.includes(ssids))) {
        return '<a><b><input class="w3-btn-block w3-btn-block:hover store-button" type="submit" ' +
            'onclick=\"vfw.sidebar.workspaceDataset(' + JSON.stringify(ssids) + '); vfw.html.infoModal.close()\" ' +
            'value="' + gettext("Pass group to datastore") + '" data-toggle="tooltip" ' +
            'title="' + gettext("Select all ") + ssids.length + gettext(" datasets of one group.") + '"></b></a>'
    } else if (ssids.length > 1) {
        return '<a><b><input class="w3-btn-block w3-btn-block:hover request-button" type="submit" ' +
            'onclick=\"vfw.map.requestDataset(' + JSON.stringify(ssids) + '); vfw.html.infoModal.close()\" ' +
            'value="' + gettext("Send group request") + '" data-toggle="tooltip" ' +
            'title="' + gettext("Send access request(s) to the data owner(s).") + '"></b></a>'
    } else {
        return ''
    }
}


vfw.map.requestDataset = function (dataId) {
    console.warn('Noch nicht implementiert.')
}
