let zoomToExt;
let wfsLayerName;
let selectedIdsFilter = null;
let olmap, hit_cL, clusterLayer, hiddenLayer;
let selectCluster;
let dcz = new ol.interaction.DoubleClickZoom();
let wfsPointSource;
let styleCache = {};
// define style for clustered data points on map
function _ClusterStyle(feature) {
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

//Create own base layer
function create_map() {
    // let mapPopup = {}
    const GEO_SERVER = DEMO_VAR + "/vfwheron/geoserver";
    let mapSource = new ol.source.XYZ({url: MAP_SERVER + "/osm/{z}/{x}/{y}.png"});
    let dataExt = JSON.parse(document.getElementById('dataExt').value); // bbox of available data
    wfsLayerName = document.getElementById('data_layer').value;
    if (wfsLayerName.search("Error") !== -1) {
        console.error(wfsLayerName)
    }
// build the background map
    let mapLayer = new ol.layer.Tile({
        preload: Infinity,
        source: mapSource,
        className: 'background-map'
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

    /* get data points */
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

    /* Make (animated) cluster layer from data points */
    clusterLayer = new ol.layer.AnimatedCluster({
        name: 'Cluster',
        className: 'cluster-layer',
        source: new ol.source.Cluster({
            distance: 30,
            source: wfsPointSource
        }),
        animationDuration: 0,
        style: _ClusterStyle
    });
    hiddenLayer = new ol.layer.VectorImage({
        className: 'hidden-layer',
        source: wfsPointSource,
    });
    // hiddenLayer.setZIndex(50);

    // Style for selection/single circles around cluster
    /*    let img = new ol.style.Circle({
            radius: 8,
            stroke: new ol.style.Stroke({
                color: '#00BAEE',
                width: 0.1
            }),
            fill: new ol.style.Fill({
                color: "rgba(170, 221, 249,0.7)"
            })
        });
        let style1 = new ol.style.Style({
            image: img,
            // Draw a link beetween points
            stroke: new ol.style.Stroke({
                color: '#AADDF9',
                width: 1
            })
        });*/

    /* functionality for zoom to extent button */
    zoomToExt = new ol.control.ZoomToExtent({ // zoom button
        label: 'Z',
        tipLabel: 'Zoom to your available data',
        extent: dataExt,
        duration: 2500,
        animate: ({duration: 5000} /*, {easing: 'elastic'}*/),
    });
    /* build app for box with drawbuttons */
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

    let mapPopup = new Popup()

    /* Initialise map */
    let map_tar = document.getElementById("map");
    olmap = new ol.Map({
        target: map_tar,
        layers: [mapLayer, clusterLayer],
        overlay: [mapPopup.overlay],
        // interactions: ol.interaction.defaults({doubleClickZoom: false}).extend([dcz]),

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
            new cApp.drawControls,
            zoomToExt,
        ],
        view: mapView//dataview
    });

    /* get information about your data in a popup when you click on a data point in the map */
    olmap.on('singleclick', checkClick);
    // check what is clicked
    function checkClick(evt) {

        if (hit_cL) {
            content.innerHTML = '';
            try {
                content.innerHTML = '<div id="loader" class="loader"></div>';
                /* content.innerHTML = '<div id="loader"  class="fading-dot-loader">\n' +
                    '  <div class="dot-loader1 dot-loader"></div>\n' +
                    '  <div class="dot-loader2 dot-loader"></div>\n' +
                    '  <div class="dot-loader3 dot-loader"></div>\n' +
                    '  <div class="dot-loader4 dot-loader"></div>\n' +
                    '  <div class="dot-loader5 dot-loader"></div>\n' +
                    '  <div class="dot-loader6 dot-loader"></div> \n' +
                    '</div>';*/

                // popupOverlay = mapPopup.overlay
                // olmap.addOverlay(mapPopup.overlay)
                console.log('olmap: ', olmap)
                console.log('-----------------')
                mapPopup._create(evt)
                // buildPopup(evt)
            } catch (err) {
                content.innerHTML = '<div id="loader">Failed to load your selection</div>';
                console.error('err: ', err)
            }

        } else {
            olmap.removeOverlay(mapPopup._metaData_Overlay)
            mapPopup.remove()
            mapPopup = {};
            console.log('olmap: ', olmap)
            // this._metaData_Overlay.setPosition(undefined) // removes popup from map when clicked on map
        }
    }

    /*    function buildPopup(evt) {
            // if (olmap.getFeaturesAtPixel(evt.pixel)) {
            // Create spinning loader while getting meta data from server
            metaData_Overlay.setPosition(evt.coordinate);

            let nCol = 5; // number of columns of metadata per page

            // console.log('feature 1', olmap)
            // console.log('feature 2', olmap.getFeaturesAtPixel(evt.pixel))
            // console.log('feature 3', olmap.getFeaturesAtPixel(evt.pixel)[0])
            // console.log('+ feature 4', olmap.getFeaturesAtPixel(evt.pixel)[0].getProperties())
            // console.log('feature 5', olmap.getFeaturesAtPixel(evt.pixel)[0].getProperties().features)
            let clickedFeatures = olmap.getFeaturesAtPixel(evt.pixel)[0].getProperties().features;
            let pos = evt.coordinate;
            // console.log('+ clickedFeatures: ', clickedFeatures)
            // console.log('+ clickedFeatures.length: ', clickedFeatures.length)
            let l = clickedFeatures.length;
            let wfsLen = wfsLayerName.length;
            if (l > 0 && l <= nCol) { // check how many datasets are selected
                let ids = [];
                let name, id;
                // bulid list with selection to send to server
                for (let i = 0; i < l; i++) {
                    name = clickedFeatures[i].getId();
                    id = parseInt(name.substr(wfsLen + 1, 8));
                    ids.push(id);
                }
                popupContent(ids);
                paginat.innerHTML = []

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


                // add paginatation to popup:
                paginat.innerHTML = buildPagi(idDict, page);
                // end of paginatation
                // TODO: need a list to click to next objects, to select ids
            }
            metaData_Overlay.setPosition(pos);

        }*/


    // select data with doubleclick
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

    // On selected => get feature in cluster and show info
    /*    selectCluster.getFeatures().on(['add'], function (e) {
            console.log(' ------------ im add')
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


class Popup {
    // closer;

    constructor() {
        // Elements that make up the popup.
        this._container = document.getElementById('popup');
        this._content = document.getElementById('popup-content');
        this._paginat = document.getElementById('popup-paginat')
        this._closer = document.getElementById('popup-closer');
        this._evt = {};
        console.log('this: ', this)

        /* Create an metaData_Overlay to anchor the popup to the map. */
        this._metaData_Overlay = new ol.Overlay(/* @type {olx.OverlayOptions} */ ({
            element: this._container,
            autoPan: true,
            autoPanAnimation: {
                duration: 150
            }
        }));
        /* Add a click handler to hide the popup. * @return {boolean} Don't follow the href. */
        this._closer.onclick = function () {
            this._metaData_Overlay.setPosition(undefined);
            this._closer.blur();
            return false;
        };
    }

    get overlay() {
        this._createpopup();
        return this._metaData_Overlay;
    }

    hide() {
        this._closer.onclick
    }

    /**
     * Function to create the popup. Called from get popup()
     * @private
     */
    _createpopup() {
        // Add a click handler to hide the popup. * @return {boolean} Don't follow the href.
        this._closer.onclick = function () {
            this._metaData_Overlay.setPosition(undefined);
            this._closer.blur();
            return false;
        };
        // Create an metaData_Overlay to anchor the popup to the map.
        this._metaData_Overlay.setPosition(this._evt.coordinate);

        let nCol = 5; // number of columns of metadata per page

        let clickedFeatures = olmap.getFeaturesAtPixel(this._evt.pixel)[0].getProperties().features;
        let pos = this._evt.coordinate;
        let l = clickedFeatures.length;
        let wfsLen = wfsLayerName.length;
        if (l > 0 && l <= nCol) { // check how many datasets are selected
            let ids = [];
            let name, id;
            // bulid list with selection to send to server
            for (let i = 0; i < l; i++) {
                name = clickedFeatures[i].getId();
                id = parseInt(name.substr(wfsLen + 1, 8));
                ids.push(id);
            }
            this._popupContent(ids);
            this._paginat.innerHTML = ''
            console.log('im _createpopup')
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
            this._popupContent(idDict[1]);


            // add paginatation to popup:
            this._paginat.innerHTML = this._buildPagi(idDict, page);
            // end of paginatation
            // TODO: need a list to click to next objects, to select ids
        }
        this._metaData_Overlay.setPosition(pos);
    }


    _buildPagi(idDict, page) {
        let pagi = '';
        let nDat = 16; // number of Datasets shown at once
        let self = this;
        if (Object.keys(idDict).length < nDat) {
            for (let i = 1; i <= page; i++) {
                if (i == 1) {
                    console.log('buildPagi')
                    pagi = '<li id="pagi' + i + '" class="active"><a><input type="submit" id="popBtn" class="respo-btn-simple"' +
                        'onclick=\"mapPopup._popupContent(\'' + idDict[i] + ',' + i + '\')\" value="' + i + '"></a></li>';
                } else {
                    pagi = pagi + '<li id="pagi' + i + '"><a><input type="submit" class="respo-btn-simple"' +
                        'onclick=\"mapPopup._popupContent(\'' + idDict[i] + ',' + i + '\')\" value="' + i + '"></a></li>';
                }
            }
        } else {
            // TODO: Show only 16 pages to select in pagination and arrows
            //  Pagination durch Django:
            //  https://medium.com/@sumitlni/paginate-properly-please-93e7ca776432
            //  https://simpleisbetterthancomplex.com/tutorial/2016/08/03/how-to-paginate-with-django.html

            /* console.log(' + +  idDict: ', idDict)
             let nPagi = Math.ceil(Object.keys(idDict).length / nDat); // Number of Pagination menues
             // let pagiObj = {1:[]}; // very nice, but useless for the button!
             let pagiStr; // very nice, but useless for the button!
             for (let j = 1; j <= nPagi; j++) {
                 let minP = nDat * (j - 1);
                 let maxP = nDat * j - 1;
                 // pagiObj[j] = [];
                 console.log('minP, maxP, pagiObj[j], j: ', minP, maxP, pagiObj[j], j)
                 pagi = '';
                 for (let k = minP; k <= maxP; k++) {
                     pagiObj[j].push(idDict[k])
                 }
             }
             console.log('pagiObj: ', pagiObj)
             let prePagi = '<li id="prePagi"><a><input type="submit" class="respo-btn-simple"' +
                         'onclick=\"buildPagivfw(\''+pagiObj+','+page+'\')\" value="<"></a></li>';
             pagi = prePagi*/
            for (let i = 1; i <= page; i++) {
                if (i == 1) {
                    pagi = '<li id="pagi' + i + '" class="active"><a><input type="submit" id="popBtn" class="respo-btn-simple"' +
                        'onclick=\"this._popupContent(\'' + idDict[i] + ',' + i + '\')\" value="' + i + '"></a></li>';
                } else {
                    pagi += '<li id="pagi' + i + '"><a><input type="submit" class="respo-btn-simple"' +
                        'onclick=\"this._popupContent(\'' + idDict[i] + ',' + i + '\')\" value="' + i + '"></a></li>';
                }
            }
        }
        return pagi;
    }


    _buildPopupText(json, popUpText) {
        let valueLen;
        let buttonId = [];
        // loop over "properties" dict with metadata, build columns
        for (let j in json) {
            // let values = eval('properties["' + j + '"]');
            let values = json[j];
            valueLen = values.length;
            popUpText += `<tr><td><b>${j}</b></td>`;
            // loop over dict values and build rows
            for (let k = 0; k < valueLen; k++) {
                popUpText += `<td>${values[k]}</td>`;
                if (j.toLowerCase() == 'id') {
                    buttonId.push(values[k])
                }
            }
            popUpText += '</tr>'
        }
        popUpText += '<tr><td><b></b></td>';
        // build buttons for each dataset
        for (let k = 0; k < valueLen; k++) {
            popUpText += '<td><a><b><input id="show_data_preview' + buttonId[k].toString() + '" class="respo-btn-block" type="submit" ' +
                'onclick=\"moreInfoModal(\'' + buttonId[k] + '\')\" value="More" data-toggle="tooltip" ' +
                'title="Show more information about the dataset."></b></a>' +
                // 'title="Attention! Loading the preview might take a while."></b></a>' +
                '<a><b><input class="respo-btn-block respo-btn-block:hover" type="submit" ' +
                'onclick=\"workspace_dataset(\'' + buttonId[k] + '\')\" value="Pass to datastore" data-toggle="tooltip" ' +
                'title="Put dataset to session datastore"></b></a></td>';
        }

        let popupTableAfterMeta = popUpText + '</table>';
        // let img_preview = '</td><td><p id = "preview_img" ></p></td></table>';
        return popupTableAfterMeta //+ img_preview;
    }


    _popupContent(ids, page) {
        console.log('popup Content')
        if (typeof (ids) === 'string' && typeof (page) === 'undefined') {
            page = JSON.parse("[" + ids + "]").slice(-1);
            ids = JSON.parse("[" + ids + "]").slice(0, -1);
        }
        if (page && page != 'none') document.getElementById("pagi" + page).classList.add("loadspin");
        let popupTableBeforeMeta = '<table id="popupTable"><td>';
        let popUpText = popupTableBeforeMeta +
            '<style>table tr:nth-child(even){background-color:#c8ebee;}</style>' +
            '<table id="metaTable">';
        // request info from server
        let self = this
        $.ajax({
            url: DEMO_VAR + "/vfwheron/menu",
            dataType: 'json',
            data: {
                short_info: JSON.stringify(ids),
                'csrfmiddlewaretoken': csrf_token,
            }, // data sent with the post request
        })
            .done(function (json) {
                document.getElementById('popup-content').innerHTML = self._buildPopupText(json, popUpText);
                // content.innerHTML = buildPopupText(json, popUpText);
                if (page && page != 'none') {
                    document.getElementsByClassName("active")[0].classList.remove("active");
                    document.getElementsByClassName("loadspin")[0].classList.remove("loadspin");
                    document.getElementById("pagi" + page).classList.add("active");
                }

            })
            .fail(function (e) {
                // console.log('fehler: ', e)
                self._metaData_Overlay.setPosition(undefined);
                document.getElementById('popup-content').remove("loader")
                alert("Ihre Anfrage kann nicht ausgeführt werden!\nYour request cannot be executed!\n" +
                    "Votre demande ne peut pas être exécutée!\nSu solicitud no puede ser ejecutada!\n" +
                    "Din forespørsel kan ikke utføres!\nВаш запрос не может быть выполнен!\n" +
                    "Är Ufro net duerchgefouert ginn!\nدرخواست شما نمی تواند اجرا شود!")
            })
        // });

    }
}
