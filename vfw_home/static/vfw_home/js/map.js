/*
 * Project Name: V-FOR-WaTer
 * Author: Marcus Strobl
 * Contributors:
 * License: MIT License
 */

vfw.map.vars.hit_cL = {};

/**
 * Calculates a circular image style for the map marker.
 *
 * @param {number} size - The radius of the circle in pixels.
 * @param {string} strokeColor - The stroke Color of the image to be used.
 * @param {string} fillColor - The fill Color of the image to be used.
 * @return {object} - The map marker style with the circular image.
 */
vfw.map.style.calcImageCircle = function(size, strokeColor=vfw.colors.blue3, fillColor=vfw.colors.blue2) {
    return new ol.style.Circle({
        radius: Math.round(8 + 1.3 * Math.log(size)),
        stroke: new ol.style.Stroke({
            color: strokeColor,
            width: 0.5
        }),
        fill: new ol.style.Fill({
            color: fillColor
        })
    })
}
/** build style for cluster **/
vfw.map.style.clusterData = function (feature) {
    const size = feature.get('features').length;
    let style = vfw.map.style.cache[size];
    if (!style) {
        style = vfw.map.style.cache[size] = new ol.style.Style({
            image: vfw.map.style.calcImageCircle(size),
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
/** build style for merrit catchments **/
vfw.map.style.merritCatchment = new ol.style.Style({
    fill: new ol.style.Fill({
        color: 'rgba(255,255,255,0)',
    }),
    stroke: new ol.style.Stroke({
        color: 'rgba(44,51,180,0.89)',
        width: 2
    })
})

/**
 * When clicked on a dataset o the map, then get a modal (pop up) with some information about the datasets
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
    loader: function (extent) {
        const layerName = 'merit_catchment';  // 'merit_catch_test';
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
                vfw.map.source.wfsMeritCatchment.addFeatures(vfw.map.source.wfsMeritCatchment.getFormat().readFeatures(response));
            })
            .catch(function (error) {
                console.warn('No result for selected area. Unable to build vector layer of Catchments.');
                vfw.map.source.wfsMeritCatchment.removeLoadedExtent(extent);
            })
    },
    strategy: ol.loadingstrategy.bbox
});
/** get catchments in coarse scale from server **/
vfw.map.source.wfsCoarseMeritCatchment = new ol.source.Vector({
    format: new ol.format.GeoJSON(),
    loader: function (extent) {
        const layerName = 'merit_catchment_coarse';  // 'merit_catch_test_v2';
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

/** get simplified merit rivers from server. Only used to select upstream catchment, not for visualisation **/
vfw.map.source.wfsMeritRiver = new ol.source.Vector({
    format: new ol.format.GeoJSON(),
    loader: function (extent) {
        let layerName = 'merit_river_simple'
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
                vfw.map.source.wfsMeritRiver.addFeatures(vfw.map.source.wfsMeritRiver.getFormat().readFeatures(response));
            })
            .catch(function (error) {
                console.warn('No result for selected area. Unable to build vector layer of rivers.');
                vfw.map.source.wfsMeritRiver.removeLoadedExtent(extent);
            })
    },
    strategy: ol.loadingstrategy.bbox
});

/** get data points from server **/
vfw.map.source.wfsPointSource = new ol.source.Vector({
    format: new ol.format.GeoJSON(),
    loader: function (extent) {
        fetch(vfw.var.DEMO_VAR + '/home/geoserver/wfs/' + vfw.var.DATA_LAYER_NAME + '/'
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
                vfw.map.source.wfsPointSource.addFeatures(vfw.map.source.wfsPointSource.getFormat().readFeatures(response));
            })
            .catch(function (error) {
                if (vfw.var.obj.selectedIds.mapIds) {
                    console.error('Error in building vector vfw.map.source.wfsPointSource: ', error);
                } else {
                    console.log(error)
                    console.warn('No result for selected area. Unable to build vector layer with data points.');
                }
            })
    },
    strategy: ol.loadingstrategy.bbox
});
/** get areal data (to select from) from server **/
vfw.map.source.wfsArealSource = new ol.source.Vector({
    format: new ol.format.GeoJSON(),
    loader: function (extent) {
        fetch(vfw.var.DEMO_VAR + '/home/geoserver/wfs/' + vfw.var.AREAL_DATA_LAYER_NAME + '/'
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
                vfw.map.source.wfsArealSource.addFeatures(vfw.map.source.wfsArealSource.getFormat().readFeatures(response));
            })
            .catch(function (error) {
                console.warn('No result for selected area. Unable to build vector layer with data points.');
                vfw.map.source.wfsArealSource.removeLoadedExtent(extent);
            })
    },
    strategy: ol.loadingstrategy.bbox
});

/** get areal data (to select from) from server as TileWMS **/
vfw.map.source.wmsTileArealSource = new ol.source.TileWMS({
          url: 'http://localhost:8888/geoserver/metacatalogdev/wms',
          params: {'FORMAT': 'image/png',
                   tiled: true,
                "STYLES": '',
                "LAYERS": 'metacatalogdev:marcus_areal_devel',
                "exceptions": 'application/vnd.ogc.se_inimage',
             tilesOrigin: 10.093123972656114 + "," + 50.400550842285156
          }
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

const osmLayer = new ol.layer.Tile({
    title: "OSM",
    baseLayer: true,
    visible: false,
    source: new ol.source.OSM(),
});

/** create a Sentinel-2 basemap layer
* for details how to handle see: http://sg.geodatenzentrum.de/web_bkg_webmap/doc/factories.html
* license info at https://sgx.geodatenzentrum.de/web_public/gdz/lizenz/eng/Sentinel_Data_Legal_Notice_eng.pdf
* details about the source at https://gdz.bkg.bund.de/index.php/default/open-data/wms-europamosaik-aus-sentinel-2-daten-wms-sen2europe.html
*/
vfw.map.source.sentinel2 = new ol.source.TileWMS({
    name: 'Sentinel-2-Europe',
    attributions: 'European Union, ' +
        '<a href="https://mis.bkg.bund.de/trefferanzeige?docuuid=3E02B389-41A9-4AD2-A1AA-FDE5676D3DF5">' +
        'Contains modified Copernicus Sentinel data (' + new Date().toLocaleString('de-de', {  year: 'numeric' }) + ')' +
        '</a> ',
    url: 'https://sgx.geodatenzentrum.de/wms_sen2europe',
    params: {
        'LAYERS': 'sentinel2-de:rgb',
        'VERSION': '1.3.0',
        'FORMAT': 'image/png',
        'TIME': '2021',
        'CRS': 'EPSG:25832',
    },
    serverType: 'geoserver'
})
vfw.map.layer.sentinel2 = new ol.layer.Tile({
    title: 'Sentinel-2-Europe',
    source: vfw.map.source.sentinel2,
    baseLayer: true,
    visible: false,
})

/**
 * Creates a WMTS tile grid for the TopPlusOpen basemap layer.
 */
vfw.map.func.createWmtsTileGrid = function()  {
    const projection = ol.proj.get('EPSG:3857');
    const projectionExtent = projection.getExtent();
    const size = ol.extent.getWidth(projectionExtent) / 256;
    let resolutions = new Array(19);
    let matrixIds = new Array(19);
    for (let z = 0; z < 19; ++z) {
        resolutions[z] = size / Math.pow(2, z);
        matrixIds[z] = z;
    }
    return new ol.tilegrid.WMTS({
        origin: ol.extent.getTopLeft(projectionExtent),
        resolutions: resolutions,
        matrixIds: matrixIds,
    });
}
vfw.map.source.TopPlusOpen = new ol.source.WMTS({
    name: 'TopPlusOpen-Webkarten',
    attributions: 'Kartendarstellung: <a href="https://www.bkg.bund.de">&copy; Bundesamt für Kartographie und ' +
        'Geodäsie (' + new Date().toLocaleString('de-de', {  year: 'numeric' }) + '), </a>' +
        '<a href="https://sgx.geodatenzentrum.de/web_public/Datenquellen_TopPlus_Open.pdf ">Datenquellen</a> ',
    url: 'https://sgx.geodatenzentrum.de/wmts_topplus_open/tile/1.0.0/web/default/WEBMERCATOR/{TileMatrix}/{TileRow}/' +
        '{TileCol}.png',
    tileGrid: vfw.map.func.createWmtsTileGrid(),
    requestEncoding: 'REST',
    projection: 'EPSG:3857',
    format: 'image/png',
    layer: 'web',
    style: 'default',
})
vfw.map.layer.TopPlusOpen = new ol.layer.Tile({
    title: 'TopPlusOpen-Webmaps',
    source: vfw.map.source.TopPlusOpen,
    baseLayer: true,
    visible: false,
})

/** Fetch V-FOR-WaTer base layer **/
vfw.map.createMap = function () {

    let dataExt = ol.proj.transformExtent(vfw.var.DATA_EXT, 'EPSG:4326', 'EPSG:3857'); // bbox of available data (extent, source, destination)

    if (vfw.var.DATA_LAYER_NAME.search("Error") !== -1) {
        console.error(vfw.var.DATA_LAYER_NAME)
        let tabBtn = {'currentTarget': document.getElementById('tableTab')}
        vfw.util.toggleMapTableFilter(tabBtn, 'paginationTable');
        filter_pagination();
    } else {
        let tabBtn = {'currentTarget': document.getElementById('defaultMapTab')}
        vfw.util.toggleMapTableFilter(tabBtn, 'Map');
    }
    /** build the background map **/
    const backgroundLayer = new ol.layer.Tile({
        name: 'V-FOR-WaTer style',
        preload: Infinity,
        baseLayer: true,
        visible: true,
        maxZoom: 20,
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
        style: vfw.map.style.clusterData
    });

    const arealDataLayer = new ol.layer.Vector({  // TODO: not working
        style: {
            'stroke-color': 'rgba(13,188,194,0.65)',
            'stroke-width': 5,
            'fill-color': 'rgba(13,188,194,0.02)',
        },
        source: vfw.map.source.wfsArealSource,
        name: 'Areal Data Layer',
        displayInLayerSwitcher: true,
        visible: false,
    })
    /** create a separate layer for merit Rivers. This layer is not visible and hidden in the menu on the map **/
    const meritRiverLayer = new ol.layer.Vector({
        style: {
            'stroke-color': 'rgba(98,165,241,0)',
        },
        source: vfw.map.source.wfsMeritRiver,
        minZoom: 8,
        name: 'Merit River Simple',
        displayInLayerSwitcher: false,
    });
    /** create a separate layer for merit Catchments **/
    const meritCatchmentLayer = new ol.layer.Vector({
        style: vfw.map.style.merritCatchment,
        source: vfw.map.source.wfsMeritCatchment,
        minZoom: 8,
        name: 'Merit Catchment',
        visible: true,
        on: function (e) {
            console.log(e)
        },
    });
    /** create a separate layer for coarse merit Catchments **/
    const meritCoarseCatchmentLayer = new ol.layer.Vector({
        style: {
            'stroke-color': 'rgba(55,19,110,0.89)',
            'stroke-width': 3,
        },
        source: vfw.map.source.wfsCoarseMeritCatchment,
        minZoom: 2,
        name: 'coarse Merit Catchment',
        visible: false,
    });


    /** functionality for zoom to extent button **/
    vfw.map.control.zoomToExt = new ol.control.ZoomToExtent({ // zoom button
        label: 'Z',
        tipLabel: gettext('Zoom to your available data'),
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

    const selectedCatchmentStyle = new ol.style.Style({
        fill: new ol.style.Fill({
            color: 'rgba(229,113,40,0.8)',
        }),
        stroke: new ol.style.Stroke({
            color: '#9f3700',
            width: 2
        }),
        image: vfw.map.style.calcImageCircle(30, vfw.colors.blue3, vfw.colors.blue4),
        text: new ol.style.Text({
            font: '12px helvetica,sans-serif',
            fill: new ol.style.Fill({
                color: 'black'
            })
        })
    });

    vfw.map.selectStyle = function (feature) {
        /**
         * Returns the selected style for a given feature. By writing this used for style of selected Merit Catchment
         * and areal data layer.
         *
         * @param {Feature} feature - The feature to select the style for.
         * @return {Style} The selected style for the feature.
         */
        const color = feature.get('COLOR') || 'rgba(229,75,40,0.3)';
        selectedCatchmentStyle.getFill().setColor(color);
        return selectedCatchmentStyle;
    }

    const selectCatch = new ol.interaction.Select({
        style: vfw.map.selectStyle
    })

    /** Initialise map **/
    let map_tar = document.getElementById("map");
    vfw.map.olmap = new ol.Map({
        target: map_tar,
        layers: [
            new ol.layer.Group({
                title: 'Base layers',  // shown on the map in the menu
                layers: [vfw.map.layer.TopPlusOpen, osmLayer, vfw.map.layer.openTopo, backgroundLayer, vfw.map.layer.sentinel2],
                name: 'Maps shown in the background.',
            }),
            new ol.layer.Group({
                openInLayerSwitcher: true,
                layers: [meritCatchmentLayer, meritRiverLayer, meritCoarseCatchmentLayer,
                    clusterLayer, arealDataLayer, ], //meritRiverLayer,vfw.map.source.wfsMeritRiver,
                name: 'Datalayers',
            }),
            vfw.map.layer.selectionLayer,
        ],
        interactions: ol.interaction.defaults.defaults().extend([selectCatch]),

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
            new ol.control.LayerSwitcher({
                label: 'layers',
                fold: 'open',
                collapsed: false,

                tipLabel: 'Legend',
                title: 'Lllayers',
                name: 'nLllayers',
            }),
        ],
        view: mapView//dataview
    });

    /** get information about your data in a popup when you click on a data point in the map,
     * or select by catchment when clicked within a catchment **/
    vfw.map.olmap.on('singleclick', checkMode);

    /** check what is clicked, if clicked on dataset open a modal with information about data **/
    function checkMode(evt) {
        let clickedFeatures, clickedArea, ids, cleanedids, dataLayerNameLen, catchmentID;
        dataLayerNameLen = vfw.var.DATA_LAYER_NAME.length;

         /**
         * Check if the specified layer is present.
         *
         * @param {string} checkLayer - the layer to check if under click position
         * @return {boolean} - true if layer is under the click position
         */
        let hasLayer = function (checkLayer) {
            return vfw.map.olmap.hasFeatureAtPixel(evt.pixel,
                {
                    layerFilter: function (layer) {
                        return layer.get('name') === checkLayer;
                    }
                })
        }
        if (hasLayer('Areal Data Layer')) {
            // collect IDs of areal data under click
            clickedArea = vfw.map.olmap.getFeaturesAtPixel(evt.pixel, {layerFilter: function (layer) {
                return layer.get('name') === 'Areal Data Layer'}
            })
            let areaIds = clickedArea.map(i => parseInt(i.getProperties().id));

            //  Add Point data IDs
            if (hasLayer('Data Clusters')) {
                clickedFeatures = vfw.map.olmap.getFeaturesAtPixel(evt.pixel, {
                    layerFilter: function (layer) {
                        return layer.get('name') === 'Data Clusters'
                    }
                })
                ids = areaIds.concat(clickedFeatures[0].values_.features.map(function (i)
                    {return parseInt(i.id_.substr(dataLayerNameLen + 1, 8));}
                ));
            } else {
                ids = areaIds;
            }
            cleanedids = ids.filter(value => {
                return !Number.isNaN(value);
            });
            vfw.map.buildMapModal(cleanedids, 1);

        } else if (hasLayer('Data Clusters')) {
            clusterLayer.getFeatures(evt.pixel).then((features) => {

                vfw.html.loaderOverlayOn();
                clickedFeatures = features[0].getProperties().features;
                ids = clickedFeatures.map(i => parseInt(i.getId().substr(dataLayerNameLen + 1, 8)));
                cleanedids = ids.filter(value => {
                    return !Number.isNaN(value);
                });
                vfw.map.buildMapModal(cleanedids, 1);
            })
        } else if (hasLayer('Merit Catchment')) {
            meritCatchmentLayer.getFeatures(evt.pixel).then((catchment) => {
                if (catchment[0]) {
                    catchmentID = catchment[0].getProperties().comid;
                    vfw.map.func.getCatchment({'startID': catchmentID})
                }
            })
        }
    }

    /** change cursor to pointer when hover over data **/
    vfw.map.olmap.on('pointermove', function (evt) {
        if (evt.dragging) {
            return;
        }
        clusterLayer.getFeatures(evt.pixel).then((features) => {
            vfw.map.olmap.getTargetElement().style.cursor = features[0] ? 'pointer' : '';
        })
    });
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

vfw.map.vars.styledMerritCatchments = [];
vfw.map.requestDataset = function (dataId) {
    console.warn('Noch nicht implementiert.')
}

/**
 * Creates the contour of a river basin based on the provided startID.
 *
 * @param {int} startID - The ID of the river to start creating the basin from.
 */
vfw.map.createRiverBasin = function (startID) {
    let catchmentIDsList = [];
    let rivFeatureList = [];
    let catchFeatureList = [];
    // Get all the features from the meritRiverLayer
    let riverFeatures = vfw.map.source.wfsMeritRiver.getFeatures();
    let catchmentFeatures = vfw.map.source.wfsMeritCatchment.getFeatures();

    //first reset style of previously selected catchments
    for (let i in vfw.map.vars.styledMerritCatchments) {
        vfw.map.vars.styledMerritCatchments[i].setStyle(vfw.map.defaultStyle);
    }

    function colorCatchment(catchFeature) {
        catchFeature.setStyle(vfw.map.selectStyle);
        vfw.map.vars.styledMerritCatchments.push(catchFeature);
    }

/** Recursive function to loop through the features and find the one with the desired values
 *
 * @param {int} riverID - The ID of the river to start creating the basin from.
 */
    function getAllRivers(riverID) {
        const rivFeature = riverFeatures.find(feature => feature.get('comid') === riverID);
        if (!rivFeature) return;
        catchmentIDsList.push(riverID);
        rivFeatureList.push(rivFeature)

        const catchFeature = catchmentFeatures.find(feature => feature.get('comid') === riverID);
        catchFeatureList.push(catchFeature)
        for (let j = 1; j < 5; j++) {
            const upstreamID = rivFeature.values_['up' + j];
            if (upstreamID !== 0) {
                getAllRivers(upstreamID);
            } else {
                break;
            }
        }
    }

    getAllRivers(startID)

    vfw.map.source.selectionSource = new ol.source.Vector({features: catchFeatureList,});
    vfw.map.layer.selectionLayer.setSource(vfw.map.source.selectionSource);
}
