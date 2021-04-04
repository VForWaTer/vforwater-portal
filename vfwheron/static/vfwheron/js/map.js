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

/** Fetch V-FOR-WaTer base layer **/
function create_map() {
    const GEO_SERVER = DEMO_VAR + "/home/geoserver";
    let mapSource = new ol.source.XYZ({
        attributions: ['Map data from <a href="https://openstreetmap.org/copyright">OpenStreetMap</a>, ' +
        'SRTM | Map style from <a href="https://www.vforwater.de/">V-FOR-WaTer</a> '],
        url: MAP_SERVER + "/osm/{z}/{x}/{y}.png"
    });
    let dataExt = ol.proj.transformExtent(JSON.parse(document.getElementById('dataExt').value),
        'EPSG:4326', 'EPSG:3857'); // bbox of available data

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
            'SRTM | Map style from <a href="http://opentopomap.org/">OpenTopoMap</a> ' +
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

    /** get data points **/
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
                    console.log('Error in building vector wfsPointSource: ', error);
                    wfsPointSource.removeLoadedExtent(extent);
                })
        },
        strategy: ol.loadingstrategy.bbox
    });

    /** Elements that make up the popup. **/
    let container = document.getElementById('popup');
    let content = document.getElementById('popup-content');
    let paginat = document.getElementById('popup-paginat')
    let closer = document.getElementById('popup-closer');
    /** Add a click handler to hide the popup. * @return {boolean} Don't follow the href. **/
    closer.onclick = function () {
        metaData_Overlay.setPosition(undefined);
        closer.blur();
        return false;
    };
    /** Create an metaData_Overlay to anchor the popup to the map. **/
    let metaData_Overlay = new ol.Overlay(/* @type {olx.OverlayOptions} */ ({
        element: container,
        autoPan: true,
        autoPanAnimation: {
            duration: 150
        }
    }));

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
        tipLabel: 'Zoom to your available data',
        extent: dataExt,
        duration: 2500,
        animate: ({duration: 5000} /*, {easing: 'elastic'}*/),
    });
    /** build app for box with drawbuttons **/
    window.cApp = {};
    let cApp = window.cApp;
    cApp.drawControls = function () {
        let element = document.createElement('div');
        element.className = 'custom-control ol-unselectable ol-control';
        element.appendChild(document.getElementById('filterbox'));
        ol.control.Control.call(this, {
            element: element
        });
    };
    ol.inherits(cApp.drawControls, ol.control.Control);

    /** Initialise map **/
    let map_tar = document.getElementById("map");
    olmap = new ol.Map({
        // renderer: 'canvas',
        overlays: [metaData_Overlay],
        target: map_tar,
        layers: [mapLayer, clusterLayer],
        // interactions: ol.interaction.defaults({doubleClickZoom: false}).extend([dcz]),

        controls: [
            new ol.control.Zoom({duration: 300}),
            new ol.control.Attribution({collapsed: false, collapsible: false, }),
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
        if (hit_cL) {
            content.innerHTML = '';
            try {
                content.innerHTML = '<div id="loader" class="loader"></div>';
                buildPopup(evt)
            } catch (err) {
                content.innerHTML = '<div id="loader">Failed to load your selection</div>';
                console.log('err: ', err)
            }

        } else {
            metaData_Overlay.setPosition(undefined) // removes popup from map when clicked on map
        }
    }

    function buildPopup(evt) {
        /** Create spinning loader while getting meta data from server **/
        metaData_Overlay.setPosition(evt.coordinate);

        let nCol = 5; /** number of columns of metadata per page **/
        let clickedFeatures = olmap.getFeaturesAtPixel(evt.pixel)[0].getProperties().features;
        let pos = evt.coordinate;
        let l = clickedFeatures.length;
        let wfsLen = wfsLayerName.length;
        if (l > 0 && l <= nCol) { /** check how many datasets are selected **/
            let ids = [];
            let name, id;
            /** bulid list with selection to send to server **/
            for (let i = 0; i < l; i++) {
                name = clickedFeatures[i].getId();
                id = parseInt(name.substr(wfsLen + 1, 8));
                ids.push(id);
            }
            popupContent(ids);
            paginat.innerHTML = ''

        } else if (l > nCol) {
            let page = 1;
            let name, id;
            let ids = [];
            let idDict = {1: []};
            for (let i = 0, j = 0; i < l; i++, j++) {
                if (j >= nCol) {
                    j = 0;
                    page++;
                    idDict[page] = [];
                }
                name = clickedFeatures[i].getId();
                id = parseInt(name.substr(wfsLen + 1, 8));
                ids.push(id);
                idDict[page].push(id);

            }
            popupContent(idDict[1]);


            /** add paginatation to popup: **/
            paginat.innerHTML = buildPagi(idDict, page);
            /** end of paginatation **/
            // TODO: need a list to click to next objects, to select ids
        }
        metaData_Overlay.setPosition(pos);

    }

    /* change cursor to pointer when hover over data */
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


/** Popup related functions **/
    function buildPagi(idDict, page) {
        let pagi = '';
        let nDat = 16; // number of Datasets shown at once
        if (Object.keys(idDict).length < nDat) {
            for (let i = 1; i <= page; i++) {
                if (i == 1) {
                    pagi = '<li id="pagi' + i + '" class="active"><a><input type="submit" id="popBtn" class="w3-btn-simple"' +
                        'onclick=\"popupContent(\'' + idDict[i] + ',' + i + '\')\" value="' + i + '"></a></li>';
                } else {
                    pagi = pagi + '<li id="pagi' + i + '"><a><input type="submit" class="w3-btn-simple"' +
                        'onclick=\"popupContent(\'' + idDict[i] + ',' + i + '\')\" value="' + i + '"></a></li>';
                }
            }
        } else {

            for (let i = 1; i <= page; i++) {
                if (i == 1) {
                    pagi = '<li id="pagi' + i + '" class="active"><a><input type="submit" id="popBtn" class="w3-btn-simple"' +
                        'onclick=\"popupContent(\'' + idDict[i] + ',' + i + '\')\" value="' + i + '"></a></li>';
                } else {
                    pagi += '<li id="pagi' + i + '"><a><input type="submit" class="w3-btn-simple"' +
                        'onclick=\"popupContent(\'' + idDict[i] + ',' + i + '\')\" value="' + i + '"></a></li>';
                }
            }
        }
        return pagi;
    }

}

    function popupContent(ids, page) {
        if (typeof (ids) === 'string' && typeof (page) === 'undefined') {
            page = JSON.parse("[" + ids + "]").slice(-1);
            ids = JSON.parse("[" + ids + "]").slice(0, -1);
        }
        if (page && page != 'none') document.getElementById("pagi" + page).classList.add("loadspin");
        let popupTableBeforeMeta = '<table id="popupTable"><td>';
        let popUpText = popupTableBeforeMeta +
            '<style>table tr:nth-child(even){background-color:#c8ebee;}</style>' +
            '<table id="metaTable">';

        /** request info from server **/
        $.ajax({
            url: DEMO_VAR + "/home/short_datainfo",
            dataType: 'json',
            data: {
                short_info: JSON.stringify(ids),
                'csrfmiddlewaretoken': csrf_token,
            }, /** data sent with the post request **/
        })
            .done(function (json) {
                document.getElementById('popup-content').innerHTML = buildPopupText(json, popUpText);
                // content.innerHTML = buildPopupText(json, popUpText);
                if (page && page != 'none') {

                    document.getElementsByClassName("active")[0].classList.remove("active");
                    document.getElementsByClassName("loadspin")[0].classList.remove("loadspin");
                    document.getElementById("pagi" + page).classList.add("active");
                }

            })
            .fail(function (e) {
                console.error('fehler: ', e)
                metaData_Overlay.setPosition(undefined);
                document.getElementById('popup-content').remove("loader")
                alert("Ihre Anfrage kann nicht ausgeführt werden!\nYour request cannot be executed!\n" +
                    "Votre demande ne peut pas être exécutée!\nSu solicitud no puede ser ejecutada!\n" +
                    "Din forespørsel kan ikke utføres!\nВаш запрос не может быть выполнен!\n" +
                    "Är Ufro net duerchgefouert ginn!\nدرخواست شما نمی تواند اجرا شود!")
            })
        // });

    }


    function buildPopupText(json, popUpText) {
        let valueLen;
        // loop over "properties" dict with metadata, build columns
        for (let j in json) {
            // let values = eval('properties["' + j + '"]');
            let values = json[j];
            valueLen = values.length;
            popUpText += `<tr><td><b>${j}</b></td>`;
            // loop over dict values and build rows
            for (let k = 0; k < valueLen; k++) {
                popUpText += `<td>${values[k]}</td>`;
            }
            popUpText += '</tr>'
        }
        popUpText += '<tr><td><b></b></td>';

        /** build buttons for each dataset **/
        function moreBtn(listIndex) {
            return '<a><b><input id="show_data_preview' + json.id[listIndex].toString() + '" class="w3-btn-block" ' +
                'type="submit" onclick=\"moreInfoModal(\'db' + json.id[listIndex] + '\')\" value="More" ' +
                'data-toggle="tooltip" title="Show more information about the dataset."></b></a>'}
        function storeBtn(listIndex) {
            if (json.Embargo[listIndex] === "False" || UNBLOCKED_IDS.includes(json.id[listIndex])) {
                return '<a><b><input class="w3-btn-block w3-btn-block:hover store-button" type="submit" ' +
                    'onclick=\"workspace_dataset(\'' + json.id[listIndex] + '\')\" value="Pass to datastore" ' +
                    'data-toggle="tooltip" title="Put dataset to session datastore"></b></a>'
            } else {
                return '<a><b><input class="w3-btn-block w3-btn-block:hover request-button" type="submit" ' +
                    'onclick=\"requestDataset(\'' + json.id[listIndex] + '\')\" value="Send request" ' +
                    'data-toggle="tooltip" title="Send an access request to the data owner."></b></a>'
            }
        }
        for (let k = 0; k < valueLen; k++) {
            popUpText += '<td>' + moreBtn(k) + storeBtn(k) + '</td>'
        }

        let popupTableAfterMeta = popUpText + '</table>';
        return popupTableAfterMeta //+ img_preview;
    }


    function requestDataset(dataId) {
        console.warn('Noch nicht implementiert.')
    }
