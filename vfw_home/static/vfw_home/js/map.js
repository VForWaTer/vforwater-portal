
vfw.map.vars.hit_cL = {};
let olmap;
// TODO: Check if clusterlayer has to be global!

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
 * Get a modal (pop up) with some information about the datasets at the clicked location.
 * @param {array} ids
 * @param {int} page
 */
vfw.map.buildMapModal = function (ids, page) {
    let basemapControl = {
        "Open Street map": vfw.map.source.osmSource,
        "VFW map": vfw.map.source.vfwSource,
        "Open Topo map": vfw.map.source.opentopoSource
    };
    $.ajax({
        url: vfw.var.DEMO_VAR + "/home/short_info_pagination",
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
            vfw.map.closeMapModal();
        })
}


/** get data points from server **/
vfw.map.source.wfsPointSource = new ol.source.Vector({
    format: new ol.format.GeoJSON(),
    loader: function (extent) {
        fetch(vfw.var.DEMO_VAR + '/home/geoserver/wfs/' + vfw.map.vars.wfsLayerName + '/'
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
                console.warn('No result for selected area. Unable to build vector layer.');
                vfw.map.source.wfsPointSource.removeLoadedExtent(extent);
            })
    },
    strategy: ol.loadingstrategy.bbox
});

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
    url: 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png'
});

/** Fetch V-FOR-WaTer base layer **/
vfw.map.create_map = function () {

    let dataExt = ol.proj.transformExtent(JSON.parse(document.getElementById('dataExt').value),
        'EPSG:4326', 'EPSG:3857'); // bbox of available data (extent, source, destination)

    vfw.map.vars.wfsLayerName = document.getElementById('data_layer').value;
    if (vfw.map.vars.wfsLayerName.search("Error") !== -1) {
        console.error(vfw.map.vars.wfsLayerName)
        let tabBtn = {'currentTarget': document.getElementById('tableTab')}
        toggleMapTableFilter(tabBtn, 'paginationTable');
        filter_pagination();
    }
    /** build the background map **/
    vfw.map.layer.map = new ol.layer.Tile({
        preload: Infinity,
        source: vfw.map.source.vfwSource,
    });
    /** get OSM/OTM in case local map is not loading: **/
    vfw.map.layer.map.getSource().on('tileloaderror', function () {
        vfw.map.layer.map.setSource(vfw.map.source.opentopoSource)
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
    vfw.map.layer.cluster = new ol.layer.AnimatedCluster({
        name: 'Cluster',
        className: 'cluster-layer',
        source: new ol.source.Cluster({
            distance: 30,
            source: vfw.map.source.wfsPointSource
        }),
        animationDuration: 0,
        /** Cluster style  **/
        style: vfw.map.style.clusterStyle
    });
    vfw.map.layer.hidden = new ol.layer.VectorImage({
        className: 'hidden-layer',
        source: vfw.map.source.wfsPointSource,
    });



    /** functionality for zoom to extent button **/
    vfw.map.control.zoomToExt = new ol.control.ZoomToExtent({ // zoom button
        label: 'Z',
        tipLabel: gettext('Zoom to your available data'),
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
        target: map_tar,
        layers: [
            vfw.map.layer.map, vfw.map.layer.cluster],

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
            vfw.map.control.zoomToExt,
            new ol.control.LayerPopup(),
        ],
        view: mapView//dataview
    });

    /** get information about your data in a popup when you click on a data point in the map **/
    olmap.on('singleclick', checkMode);

    /** check what is clicked **/
    function checkMode(evt) {
        let clickedFeatures, ids, cleanedids, wfsLen;
        if (vfw.map.vars.hit_cL) {
            content.innerHTML = '';
            try {
                content.innerHTML = '<div id="loader" class="loader">bla</div>';
                positionPopup(vfw.html.popup);
                wfsLen = vfw.map.vars.wfsLayerName.length;
                clickedFeatures = olmap.getFeaturesAtPixel(evt.pixel)[0].getProperties().features;
                ids = clickedFeatures.map(i => parseInt(i.getId().substr(wfsLen + 1, 8)));
                cleanedids = ids.filter(value => {
                    return !Number.isNaN(value);
                });
                vfw.map.buildMapModal(cleanedids, 1);
                mapmodal.style.display = "block";
            } catch (err) {
                content.innerHTML = '<div id="loader">Failed to load your selection</div>';
                console.log('err: ', err)
            }

        } else {
            // console.log('Nothing to click here')
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
        vfw.map.vars.hit_cL = olmap.forEachLayerAtPixel(evt.pixel, function (feature) {
                return feature;
            },
            {
                layerFilter: function (layer) {
                    return layer === vfw.map.layer.cluster
                }
            }
        );
        olmap.getTargetElement().style.cursor = vfw.map.vars.hit_cL ? 'pointer' : '';
    });

}

}

/**
 * Create a html button to request a dataset or pass it to the data store, depending on embargo.
 * @param {int} ssid
 * @param {string} embargo "True" or "False"
 */
vfw.map.storeBtn = function (ssid, embargo) {
    if (embargo === "False" || vfw.map.UNBLOCKED_IDS.includes(ssid)) {
        return '<a><b><input class="w3-btn-block w3-btn-block:hover store-button" type="submit" ' +
            'onclick=\"vfw.sidebar.workspace_dataset(\'' + ssid + '\')\" ' +
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
    let btn = '';
    if (ssids.length > 1) {
        btn = '<a><b><input class="w3-btn-block w3-btn-block:hover" type="submit" ' +
            'onclick=\"vfw.map.buildMapModal(' + JSON.stringify(ssids) + ', 1); closeInfoModal()\" ' +
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
            'onclick=\"vfw.sidebar.workspace_dataset(' + JSON.stringify(ssids) + '); closeInfoModal()\" ' +
            'value="' + gettext("Pass group to datastore") + '" data-toggle="tooltip" ' +
            'title="' + gettext("Select all ") + ssids.length + gettext(" datasets of one group.") + '"></b></a>'
    } else if (ssids.length > 1) {
        return '<a><b><input class="w3-btn-block w3-btn-block:hover request-button" type="submit" ' +
            'onclick=\"vfw.map.requestDataset(' + JSON.stringify(ssids) + '); closeInfoModal()\" ' +
            'value="' + gettext("Send group request") + '" data-toggle="tooltip" ' +
            'title="' + gettext("Send access request(s) to the data owner(s).") + '"></b></a>'
    } else {
        return ''
    }
}


vfw.map.requestDataset = function (dataId) {
    console.warn('Noch nicht implementiert.')
}
