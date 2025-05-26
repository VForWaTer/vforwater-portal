/*
 * Project Name: V-FOR-WaTer
 * Author: Marcus Strobl
 * Contributors:
 * License: MIT License
 */

/**
 * Global Element (source layer) to drawn on
 */
vfw.var.ACTIVEMAP = true;
let sessionStorageData = {};
vfw.var.obj.bokehImage = false;

vfw.var.obj.selectedIds = {
    mapIds: null,
    quickMenuIds: null,
    combinedIds: null,

    /**
     * @param {array} idList
     */
    set map(idList) {
        this.mapIds = idList;
        this._setCombinedIds()
    },
    get map() {
        return this.mapIds
    },

    /**
     * @param {array} idList
     */
    set quickMenu(idList) {
        this.quickMenuIds = idList;
        this._setCombinedIds()
    },
    get quickMenu() {
        return this.quickMenuIds
    },
    get result() {
        return this.combinedIds
    },

    resetIds: function () {
        this.mapIds = null;
        this.quickMenuIds = null;
        this.combinedIds = null;
    },

    /**
     * if selection changes update table (when HTML in table tab)
     * @param {array} oldIds
     */
    _updateFilterTable: function (oldIds) {
        if (!vfw.var.ACTIVEMAP && this.combinedIds !== oldIds) {
            filter_pagination(1);
        }
    },

    /**
     * update combined Ids when selection on map or in Quick Menu
     */
    _setCombinedIds: function () {
        let oldIds = this.combinedIds
        if (this.mapIds == null) {
            this.combinedIds = this.quickMenuIds
        } else if (this.quickMenuIds == null) {
            this.combinedIds = this.mapIds
        } else {
            this.combinedIds = this.mapIds.filter(x => this.quickMenuIds.includes(x))
        }
        this._updateFilterTable(oldIds);
    }
};

/**
 * Class to store data used on different URLs. Every change should be stored in session storage.
 */
class StoreData {

    constructor(definition) {
        this.data = {};
        this.data.name = definition.name;
        this.data.abbr = definition.abbr;
        this.data.unit = definition.unit;
        this.data.type = definition.type;
        this.data.source = definition.source;
        this.data.dbID = definition.dbID;
        this.data.webID = definition.source + definition.dbID; // + 'from' + start + 'to' + end
        this.data.dispName = createBtnName(definition.name, definition.abbr, definition.unit, definition.dbID);
        this.data.orgID = definition.orgID;
        this.data.start = definition.start;
        this.data.end = definition.end;
        this.data.inputs = definition.inputs;
        this.data.outputs = definition.outputs;
        this.data.error = null;
        this.data.toolName = null;
    }

    save() {
        let thisID = this.data.webID;
    }
}

/**
 * wps tools datatypes and relationships to each other.
 *
 * @type {{validInput(string, string): boolean, accepts(list): set, HIERACHY: {idataframe: [string], timeseries: [string], array: string[], raster: [string], iarray: [string], html: [string], ndarray: string[], "time-dataframe": [string]}, bHIERACHY: {vtimeseries: string[], idataframe: [string], timeseries: [string], "vtime-dataframe": string[], vraster: string[], raster: [string], iarray: [string], varray: string[], vdataframe: string[], "2darray": [string], "time-dataframe": [string]}}}
 */
const DATATYPE = new class AbstractType {
    constructor() {
        this.HIERACHY = {
            'array': ['iarray', 'timeseries'],
            'iarray': ['varray'],
            'timeseries': ['vtimeseries'],
            'ndarray': ['raster', '2darray', 'idataframe', 'time-dataframe'],
            'raster': ['vraster'],
            'idataframe': ['vdataframe'],
            'time-dataframe': ['vtime-dataframe'],
            'html': ['plot']
        }
        this.bHIERACHY = {
            'iarray': ['array'],
            'varray': ['iarray', 'array'],
            'timeseries': ['array'],
            'vtimeseries': ['timeseries', 'array'],
            'raster': ['ndarray'],
            'vraster': ['raster', 'ndarray'],
            '2darray': ['ndarray'],
            'idataframe': ['ndarray'],
            'vdataframe': ['idataframe', 'ndarray'],
            'time-dataframe': ['ndarray'],
            'vtime-dataframe': ['time-dataframe', 'ndarray']
        }
    }

    /**
     * Check if your data/output is valid for a process.
     *
     * @param {string} inputType - Datatype you want to use in process
     * @param {string} outputType - Datatype accepted from process
     * @return {boolean}
     */
    validInput(inputType, outputType) {
        return outputType in this.HIERACHY[inputType] || inputType === outputType
    }

    /**
     * Return possible inputTypes for given type(s) of data.
     *
     * @param {list} inputTypeList - Datatype(s) you want to use in process
     * @return {set} - set of strings with accepted input types
     */
    accepts(inputTypeList) {
        let acceptedList = inputTypeList;
        for (let i of inputTypeList) {
            acceptedList = acceptedList.concat(this.HIERACHY[i])
            if (Array.isArray(this.HIERACHY[i])) {
                for (let j of this.HIERACHY[i]) {
                    acceptedList = acceptedList.concat(this.HIERACHY[j])
                }
            }
        }
        return new Set(acceptedList)
    }
}


/**
 * Create a name for buttons according to the length of the name string
 *
 * @param {string} name
 * @param {string} abbr
 * @param {string} unit
 * @param {string} dbID
 */
function createBtnName(name, abbr, unit, dbID) {
    let btnName;
    const vnLen = name.length;
    if (vnLen + abbr.length + unit.length <= 13) {
        btnName = name + '(' + abbr + ' in ' + unit + ') - ' + dbID;
    } else if (vnLen + abbr.length <= 15) {
        btnName = name + '(' + abbr + ') - ' + dbID;
    } else if (vnLen <= 17) {
        btnName = name + ' - ' + dbID;
    } else {
        btnName = abbr + ' in ' + unit + ' - ' + dbID;
    }
    return btnName
}

/**
 * Create HTML element for buttons to be placed on the sidebar
 *
 * @param {string} storeID
 * @param {dict} btnData
 * @param {string} btnName
 * @param {string} title
 */
vfw.html.createSidebarBtn = function (storeID, btnData, btnName, title) {
    let drag_html = "";

    let noData = "";
    if (btnData['type'] == null) {
        noData = "noDataBtn";
        title = "Internal error. No data available for this metadata record.";
    }

    if (window.location.pathname == '/workspace/') {
        drag_html = 'draggable="true" ondragstart="dragstart_handler(event)"'
    }
    const elementID = "sidebtn" + storeID;
    return '<li ' + drag_html + ' class="w3-padding task" data-sessionstore="dataBtn" ' +
        'data-orgid="' + btnData['orgID'] + '" ' +
        'data-id="' + btnData['source'] + btnData['dbID'] + '" btnName="' + btnName + '" onmouseover="" ' +
        'data-btnName="' + btnName + '" style="cursor:pointer;" id="' + elementID + '">' +
        '<span class="w3-medium" title="' + title + '">' +
        '<div class="task__content ' + noData + '">' + btnName + '</div><div class="task__actions"></div>' +
        '</span><span class="data ' + btnData['type'] + '"></span>' +
        '<a onclick="vfw.datasets.dataObjects[\'' + storeID + '\'].removeData(\'' + storeID + '\')" ' +
        'class="w3-hover-white w3-right"><i class="fa fa-remove fa-fw"></i>' +
        '</a><br></li>';
}

//--- draw start -------------------------------------------------------------------------------------------------------
vfw.map.source.selectionSource = new ol.source.Vector({
    wrapX: false,
    features: new ol.Collection(),
    useSpatialIndex: false,
    zindex: -100
});
// Create a layer used to select data on the map
vfw.map.layer.selectionLayer = new ol.layer.Vector({
    name: 'Selection Layer',
    source: vfw.map.source.selectionSource,
    style: new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: '#ff0040',
            width: 2.5
        }),
    }),
    updateWhileAnimating: true, // optional, for instant visual feedback
    updateWhileInteracting: true // optional, for instant visual feedback
});
/**
 * Reset the draw menu, clear selections in memory and on map
 */
vfw.map.func.resetDraw = function() {
    vfw.filter.coords = [];
    vfw.html.getQuickSelection({'draw': []});
    vfw.html.getQuickSelection({'catchout': []});
    vfw.html.getQuickSelection({'catchStartID': []});
    vfw.var.obj.selectedIds.map = null;
    vfw.map.source.selectionSource.clear();
    vfw.map.func.removeCatchmentDrawings();

    vfw.map.olmap.removeInteraction(vfw.map.control.draw);
    vfw.map.olmap.removeInteraction(vfw.map.control.modify);


/**
 * Transforms coordinates for django, writes them in a variable and resets the original coordinates.
 *
 * @returns Array
 */
 vfw.map.func.getSelectionEdgeCoords = function() {
    // return  ol.proj.transform(vfw.map.vars.selectionEdgeCoords.getCoordinates(), 'EPSG:3857', 'EPSG:4326');
    let coords = vfw.map.vars.selectionEdgeCoords.transform('EPSG:3857', 'EPSG:4326').getCoordinates()
    vfw.map.vars.selectionEdgeCoords.transform('EPSG:4326', 'EPSG:3857')
    return coords
}
/**
 * Catchments are drawn as a feature in their own source. To enable the standard openlayers drawing,
 * the original source has to be set again for the selectionLayer. The catchment source and the catchment
 * in the sessionStorage aren't needed anymore and removed as well.
 */
vfw.map.func.removeCatchmentDrawings = function() {
    vfw.map.source.selectionSource_catchment = {};
    sessionStorage.removeItem("catchment");
    vfw.map.layer.selectionLayer.setSource(vfw.map.source.selectionSource);
}

/**
 * Open menu to draw polygon on map and use the polygon to select data
 *
 * @param test
 */
vfw.map.func.drawOnMapMenu = function (test) {
    vfw.map.func.toggleDrawFilter();

    /**
     * Create and add interactions - Connect the draw button with the open layers interactions to draw on the map.
     */

    /** Interaction to draw a polygon. */
    vfw.map.control.draw = new ol.interaction.Draw({
        source: vfw.map.source.selectionSource,
        type: 'Polygon',
        stopClick: true,
    });
    /** Interaction for drawing a Square. */
    vfw.map.control.drawSquare = new ol.interaction.Draw({
        source: vfw.map.source.selectionSource,
        type: 'Circle',
        geometryFunction: ol.interaction.Draw.createBox(),
        stopClick: true
    });
    /** Interaction to click on the map and get the contour line of a catchment from the server. */
    vfw.map.control.drawCatchmentOutlet = new ol.interaction.Draw({
        source: vfw.map.source.selectionSource,
        type: 'Point',
    })

    const overlayStyle = new ol.style.Style({stroke: new ol.style.Stroke({color: '#03ad1a', width: 3})})
    const select = new ol.interaction.Select({style: overlayStyle,});
    vfw.map.olmap.addInteraction(select)

    /**
     * Modify an element drawn on the map. Works on the select layer, so works for uploaded layers as well as for layers
     * from geoserver.
     */
    vfw.map.control.modify = new ol.interaction.Modify({ // TODO: Modify has to be fixed!
        features: select.getFeatures(),
        pixelTolerance: 25,  // default is 10
        style: overlayStyle,
        insertVertexCondition: function () {
            // prevent new vertices to be added to the polygons
            return !select.getFeatures().getArray().every(function (feature) {
                return feature.getGeometry().getType().match(/Polygon/);
            });
        },
        // the SHIFT key must be pressed to delete vertices, so that new
        // vertices can be drawn at the same position of existing vertices
        deleteCondition: function (event) {
            return ol.events.condition.shiftKeyOnly(event) &&
                ol.events.condition.singleClick(event);
        }
    });


    vfw.var.obj.selectedIds.map = null;
    let sketch, listener, polygon;

    /**
     * Point features select/deselect as you move polygon.
     Deactivate select interaction.
     */
    vfw.map.control.modify.on('modifystart', function (event) {
        sketch = event.features;
        listener = selectStartFun(event)
    }, this);
    /* Reactivate select function */
    vfw.map.control.modify.on('modifyend', function (event) {
        sketch = null;
        delaySelectActivate();
        vfw.var.obj.selectedIds.map = null;
        polygon = event.features.getArray()[0].getGeometry();
        vfw.map.vars.selectionEdgeCoords = polygon;
        vfw.filter.coords = vfw.map.func.getSelectionEdgeCoords();
        vfw.html.getQuickSelection({'draw': vfw.map.func.getSelectionEdgeCoords()});
    }, this);

    /* //////////// SUPPORTING FUNCTIONS */
    function delaySelectActivate() {
        setTimeout(function () {
            select.setActive(true)
        }, 300);
    }

    /**
     * Get geometry of drawing, check which features are inside drawing and push result to selectedFeatures.
     *
     * @param event
     * @returns {*}
     */
    function selectStartFun(event) {
        let changes;
        try {
            changes = event.feature.getGeometry().on('change', function (event) {
                // clear features so they deselect when polygon moves away
                vfw.map.vars.selectionEdgeCoords = event.target;
            });
        } catch (e) {
            changes = {}
        }
        return changes
    }

    vfw.map.control.drawSquare.on('drawstart', function (event) {
        vfw.map.source.selectionSource.clear();
        vfw.map.func.removeCatchmentDrawings();
        listener = selectStartFun(event)
    }, this);
    vfw.map.control.drawSquare.on('drawend', function () {

        vfw.filter.coords = vfw.map.func.getSelectionEdgeCoords();
        vfw.html.getQuickSelection({'draw': vfw.map.func.getSelectionEdgeCoords()});  // update selection on map
        vfw.map.vars.mapSelect = vfw.map.func.getSelectionEdgeCoords()[0][0];  // store selection in var. Might be useful for an undo button
        vfw.map.func.removeDrawInteractions();
        vfw.map.func.toggleDrawBackground(document.getElementById("draw_square"))
    });

    vfw.map.control.draw.on('drawstart', function (event) {
        vfw.map.source.selectionSource.clear();
        vfw.map.func.removeCatchmentDrawings();
        listener = selectStartFun(event)
    }, this);
    vfw.map.control.draw.on('drawend', function () {

        vfw.filter.coords = vfw.map.func.getSelectionEdgeCoords();
        vfw.html.getQuickSelection({'draw': vfw.map.func.getSelectionEdgeCoords()});
        vfw.map.vars.mapSelect = vfw.map.func.getSelectionEdgeCoords()[0][0];  // store selection in var. Might be useful for a undo button
        vfw.map.func.removeDrawInteractions();
        vfw.map.func.toggleDrawBackground(document.getElementById("draw_polygon"))

    });

    vfw.map.control.drawCatchmentOutlet.on('drawstart', function (event) {
        vfw.html.loaderOverlayOn()
        vfw.map.vars.selectionEdgeCoords = event.feature.getGeometry()
        listener = selectStartFun(event)
        let click_coords = vfw.map.func.getSelectionEdgeCoords()
        click_coords[0] = click_coords[0].toFixed(6);
        click_coords[1] = click_coords[1].toFixed(6);

        // load watershed from clickpoint (not exactly from clickpoint but from the catchment containing the clickpoint)
        $.when(vfw.map.func.getCatchment({'coords': click_coords}))
            .done(catchment => {
                sessionStorage.setItem('catchment', JSON.stringify(catchment))
                vfw.map.func.renderCatchment(catchment, 'wkt')
                vfw.html.loaderOverlayOff();
            })
            .fail(error => {
                console.warn('Unable to create Catchment from Outlet: ', error);
                vfw.html.loaderOverlayOff();
            })
    }, this);
    vfw.map.control.drawCatchmentOutlet.on('drawend', function () {
        vfw.map.func.removeDrawInteractions();
        vfw.map.func.toggleDrawBackground(document.getElementById("draw_catchment"))
    })
}

/**
 * Remove interactions from draw menu options (draw, drawSquare, modify...).
 */
vfw.map.func.removeDrawInteractions = function () {
    vfw.map.olmap.removeInteraction(vfw.map.control.draw);
    vfw.map.olmap.removeInteraction(vfw.map.control.modify);
    vfw.map.olmap.removeInteraction(vfw.map.control.drawSquare);
    vfw.map.olmap.removeInteraction(vfw.map.control.drawCatchmentOutlet);
}

/**
 * Toggle between showing and hiding the draw filter on the map
 */
vfw.map.func.toggleDrawFilter = function () {
    let drawfilter = document.getElementById("drawfilter");
    let closedDrawfilter = document.getElementById("closed_drawfilter");
    if (drawfilter.style.display === "none") {
        closedDrawfilter.style.display = "none";
        drawfilter.style.display = "block";
    } else {
        closedDrawfilter.style.display = "block";
        drawfilter.style.display = "none";
    }
}


/**
 * Toggle function for background of draw and modify button, and remove background by press on delete and close
 */
vfw.map.func.toggleDrawBackground = function (self) {
    let siblings = document.getElementsByClassName('draw-hover');
    let s;
    const sLen = siblings.length - 1;  // avoid to toggle on the delete button
    if (self.classList.contains('activeM')) {
        self.classList.remove('activeM');
        vfw.map.control.draw.finishDrawing();
    } else {
        for (s = 0; s < sLen; s++) {
            if (siblings[s].classList.contains('activeM')) siblings[s].classList.remove('activeM')
        }
        if (self.id !== siblings[sLen].id && self.id !== 'draw_close') self.classList.add('activeM')
    }
}

//--- draw end ---------------------------------------------------------------------------------------------------------

//Search
function closeSearch() {

    document.getElementById("search_box").outerHTML = "<a href='#' onclick='open_search()' id='srch_box' " +
        "class='w3-hover-white'><i class='fa fa-search fa-fw'></i>  Search</a>";
    document.getElementById("search_but").outerHTML = "<a id='srch_but' class='w3-hover-none'></a>";
    document.getElementById("search_close_but").outerHTML = "<a id='srch_close_but' class='w3-hover-none'></a>";
}

function search_open() {
    if (!document.getElementById("search_box")) {
        let searchBox = document.getElementById("srch_box");
        searchBox.outerHTML = "<a class='w3-hover-none' style='height:103px' id='search_box'><input type='search' " +
            "value='' placeholder='Search ...' style='height:26px; font-size:70%;'></a>";

        let searchBut = document.getElementById("srch_but");
        searchBut.outerHTML = "<a href='#' class='w3-hover-white' style='height:103px' id='search_but' " +
            "onclick='closeSearch()'><i class='fa fa-search fa-fw'></i></a>";

        let closeBut = document.getElementById("srch_close_but");
        closeBut.outerHTML = "<a href='javascript:void(0)' class='w3-hover-white' style='height:103px' " +
            "id='search_close_but' onclick='closeSearch()'><i class='fa fa-remove fa-fw'></i></a>";
    }
}

vfw.util.getCookie = function(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        const nLen = name.length;
        const cLen = cookies.length;
        for (let i = 0; i < cLen; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, nLen + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(nLen + 1));
                break;
            }
        }
    }
    return cookieValue;
}

vfw.var.csrf_token = vfw.util.getCookie('csrftoken');

vfw.html.loaderOverlayOn = function () {
    document.getElementById("loader-overlay").style.display = "block";
}

vfw.html.loaderOverlayOff = function () {
    document.getElementById("loader-overlay").style.display = "none";
}

/**
 * Load metadata and preview plot of dataset from server asynchronous.
 *
 * @param {string} id of dataset as string.
 */
vfw.html.moreInfoModal = function (id) {
    vfw.html.loaderOverlayOn();
    let pdata;
    let startdate, enddate;
    const urlParams = new URLSearchParams(window.location.search);
    const date = urlParams.getAll('date');

    if ($.isEmptyObject(date)) {
        startdate = 'None'
        enddate = 'None'
    } else {
        startdate = date[0].toString();
        enddate = date[1].toString();
    }

    let ajaxTable = async function () {
        let result;
        await $.ajax({
            url: vfw.var.DEMO_VAR + "/home/show_info",
            dataType: 'json',
            data: {
                show_info: id,
                'csrfmiddlewaretoken': vfw.var.csrf_token,
            }, // data sent with post request
        })
            .done(function (data) {
                result = data['table'];
                if (data['warning'] !== '') {
                    console.warn(data['warning']);
                }
            })
            .fail(function (e) {
                console.error('Failed to load table: ', e)
            });
        return result
    }
    // load preview image parallel to metadata
    let ajaxPlot = async function () {
        let result;
        await $.ajax({
            url: vfw.var.DEMO_VAR + "/home/previewplot",
            datatype: 'image/png;base64',
            // datatype: 'html',
            data: {
                preview: id,
                // date: date.toString(),
                startdate: startdate,
                enddate: enddate,
                'csrfmiddlewaretoken': vfw.var.csrf_token,
            }, // data sent with the post request
        })
            .done(function (data) {
                if ('error' in data) {
                    console.warn('Error while preparing data: ', data.error)
                    pdata = false
                } else {
                    result = data;
                }
            })
            .fail(function (e) {
                console.warn('Unable to plot. Inform Admin.')
                pdata = false
                // console.error('Failed to load plot: ', e)
            });
        return result
    }
    document.getElementById('mod_dat_inf').innerHTML = "";
    document.getElementById("mod_prev").innerHTML = "";

    // The following is used to make sure to add first the table then the plot.
    /**
     * Create html code for a table with metainformation of a dataset
     * and a button accordingly if dataset has embargo or not
     *
     * @param {dict} properties
     */
    function tableToModal(properties) {
        let metaText = '<table>';
        // loop over "properties" dict with metadata, build columns
        for (let j in properties) {
            if (j !== 'has_embargo' && j !== 'group_entry_ids') {
                metaText += '<tr>' +
                    '<td><div style="max-width:120px;"><b>' + j + '</b></div></td>' +
                    '<td><div style="max-height:300px; max-width:320px; ' +
                    'overflow-x: hidden; overflow-y:auto;">' + properties[j] + '</div></td>' +
                    '</tr>';
            } else if (j == 'has_embargo') {
                metaText += '<tr>' +
                    '<td colspan = "2">' + vfw.map.createStoreBtn(properties.id, properties.has_embargo) + '</td></tr>' +
                    '<tr><td colspan = "2"><div style="height:20px"></div></td></tr>'
            } else if (j == 'group_entry_ids') {
                metaText += '<tr><td colspan = "2">' + vfw.map.showGroupBtn(properties.group_entry_ids) + '</td></tr>' +
                    '<tr><td colspan = "2">' + vfw.map.storeGroupBtn( properties.group_entry_ids, properties.has_embargo) + '</td></tr>'
            }
        }
        document.getElementById('mod_dat_inf').innerHTML = metaText + '</table>';
    }

    /**
     * Set data (HTML and JavaScript) for bokeh plot.
     *
     * @param {string} json
     */
    function plotToModal(json) {
        if ('warning' in json) {
            document.getElementById('mod_prev').innerHTML = json.warning;
        } else {
            document.getElementById('mod_prev').style.width = "700px";  // set size for plot
            document.getElementById('mod_prev').innerHTML = json.div; // add plot
            // bokehPreviewScript is a global variable to set and remove the script of bokeh
            vfw.util.bokehPreviewScript = document.createElement('script');
            vfw.util.bokehPreviewScript.type = 'text/javascript';
            vfw.util.bokehPreviewScript.text = json.script;
            document.head.appendChild(vfw.util.bokehPreviewScript);
        }
    }

    $.when(ajaxTable(), ajaxPlot())
        .done(function (td, pd) {
            let modal = document.getElementById("infoModal");
            modal.style.display = "block";
            tableToModal(td)
            if (pdata !== false) {
                plotToModal(pd)
            }
        })
        .fail(function(e) {
            document.getElementById('mod_dat_inf').innerHTML = '<p>Error in dataset. Please try again later.</p>';
        })
        .always(function() {
          vfw.html.loaderOverlayOff();
        })
}

/**
 * Collect filltered data and use it to build a group button
 */
vfw.sidebar.collectWorkspaceDatasets = function () {
    let selection = vfw.var.obj.selectedIds.quickMenu;

}


vfw.url.getDateFromURL = function () {
    let startdate, enddate;
    const urlParams = new URLSearchParams(window.location.search);
    const date = urlParams.getAll('date');

    if ($.isEmptyObject(date)) {
        startdate = 'None'
        enddate = 'None'
    } else {
        startdate = date[0].toString();
        enddate = date[1].toString();
    }
    return {'start': startdate, 'end': enddate}
}


/**
 * send request to view to get info about selection
 * @param {string} id - can be a single id or a list of ids
 */
vfw.sidebar.workspaceDataset = function (id) {
    let date = vfw.url.getDateFromURL();

    id = JSON.stringify(id);  // ensure id is a string

    if (id !== 'null') {
        $.ajax({
            url: vfw.var.DEMO_VAR + "/home/workspace_data",
            datatype: 'json',
            data: {
                workspaceData: id,
                startDate: date['start'],
                endDate: date['end'],
                'csrfmiddlewaretoken': vfw.var.csrf_token,
            }, // data sent with post request
        })
            .done(function (json) {
                let stored = JSON.parse(sessionStorage.getItem("dataBtn")) || {};

                /** create an object for each requested dataset */
                $.each(json['workspaceData'], function (k) {
                    /** if object is not already in store, create it / ensure buttons are created only once
                    if (!(k in stored)) {
                        vfw.datasets.dataObjects[k] = new vfw.datasets.DataObj(json['workspaceData'][k]);
                    }
                });
            }) // function in sidebar.js
            .fail(function (json) {
                console.warn('failed to get data for workspace: ', json)
            })
    }
}

/**
 * Toggle function to switch between map and table view, and in the future between quick and advanced filter.
 *
 * @param {Event} evt
 * @param {string} tabName
 * @param {boolean} isFilter
 */
vfw.util.toggleMapTableFilter = function (evt, tabName, isFilter = false) {
    // Declare all variables
    let i, tabcontent, tablinks;
    let classNamePrefex = "";

    if (isFilter) {
        classNamePrefex = "filter-"
    } else {
        vfw.var.ACTIVEMAP = tabName === "Map";
    }

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName(classNamePrefex + "tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName(classNamePrefex + "tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}


/**
 * Update options in the quickfilter and on the map according to the given URL, during onload()
 */
vfw.filter.updateQuickfilter = function() {

    const urlParams = new URLSearchParams(window.location.search);
    let urlKey, long_search_id, ajax_element;
    let date = 0;
    let selector_string = "";

    if (urlParams !== false) {
        for (urlKey of urlParams) {
            selector_string = "#id_" + urlKey[0]
            ajax_element = $(selector_string);

            if (ajax_element.prop('type') === 'checkbox') {
                ajax_element.prop('checked', JSON.parse(urlKey[1].toLowerCase()));
            } else if (ajax_element.prop('type') === 'select-multiple' ||
                ajax_element.prop('type') === 'select') {
                long_search_id = selector_string + " [value=\"" + urlKey[1] + "\"]"
                $(long_search_id).attr("selected", "selected");
            } else if (ajax_element.prop('name') === 'date') {
                if (date === 0) {
                    date = new Date(urlKey[1]);
                } else {
                    ajax_element.prop('value', [date.toLocaleDateString() + " - " + (new Date(urlKey[1])).toLocaleDateString()]);  // textbox
                    $('#from_' + urlKey[0]).val(date.toLocaleDateString())  // update date picker
                    $('#to_' + urlKey[0]).val((new Date(urlKey[1])).toLocaleDateString())  // update date picker
                    $('#slider-date-range-' + urlKey[0])
                        .slider('values', [
                            (new Date(date)).getTime(),
                            (new Date(urlKey[1])).getTime()
                        ]).val()  // update slider
                }
            } else if (urlKey[0] === 'draw') {
                const coords_list = vfw.filter.coords.length > 0 ? vfw.filter.coords :
                    urlParams.get('draw').split(",").map(Number);
                const coords_len = coords_list.length;
                let coords = []
                for (let i = 0; i < coords_len; i += 2) {
                    coords.push(ol.proj.fromLonLat([coords_list[i], coords_list[i + 1]]))
                }

                vfw.map.source.selectionSource = new ol.source.Vector({
                    features: [new ol.Feature({
                        geometry: new ol.geom.Polygon([coords]),
                    })],
                });
                vfw.map.layer.selectionLayer.setSource(vfw.map.source.selectionSource);
            } else if (urlKey[0] === 'catchout') {
                vfw.map.func.renderCatchment(JSON.parse(sessionStorage.getItem('catchment')), 'wkt')
            } else {
                console.log('TODO: Implement something for: ', $("#id_" + urlKey[0]).prop('type'))
            }
        }
    } else {
    }

}


function filter_pagination(page) {
    let data = JSON.stringify(vfw.var.obj.selectedIds.result);
    if (Array.isArray(data) && !data.length) {data = 'None'}
    $.ajax({
        url: vfw.var.DEMO_VAR + "/home/entries_pagination",
        datatype: 'json',
        data: {
            page: page, datasets: data,
            'csrfmiddlewaretoken': vfw.var.csrf_token,
        }, // data sent with post request
    })
        .done(function (json) {
            document.getElementById("paginationTable").innerHTML = json

        })
        .fail(function (e) {
            console.error('Fehler: ', e)
        })
}

/**
 * Build url from values from map (as coordinates), form object (send as selection) and from existing URL
 *
 * @param {string} selection
 */
vfw.url.updateFilterURL = function(selection)  {
    vfw.html.loaderOverlayOn();
    const drawKeys = ['draw', 'catchout', 'catchStartID']
    const url = window.location
    let urlParams = new URLSearchParams(url.search);
    let nextURL;

    let urlPath = url.origin + url.pathname;
    if (selection) {
        let selectedKey = Object.keys(selection)[0]
        let selectedValues = Object.values(selection)[0]

        // if one wants to use another drawing method then already given in the url, remove the old url params
        if (drawKeys.includes(selectedKey)) {
            drawKeys
                .filter(item => item !== selectedKey)
                .forEach(item => urlParams.delete(item))
        }

        // add new parameter to URL
        urlParams.delete(selectedKey);
        if (Symbol.iterator in Object(selectedValues)) {  // check if Object can be iterated
            for (let value of selectedValues) {
                urlParams.append(selectedKey, value);
            }
        } else {
            return false
        }
    }
    nextURL = urlParams.toString() === '' ? urlPath : urlPath + '?' + urlParams.toString();
    window.history.pushState({additionalInformation: 'Updated the URL with JS'}, '', nextURL);
    if (urlParams.toString() === "") {
        urlParams = 'reset'
    }
    return urlParams.toString();

}


/**
 * Get state of quickfilter from url. Executed on every click in the quick filter and when filtered on the map.
 *
 * @param {string} selection
 */
vfw.html.getQuickSelection = function (selection) {
    let coords = vfw.filter.coords;
    let url = vfw.url.updateFilterURL(selection)
    if (selection && ('draw' in selection || 'catchout' in selection)) {
        coords = vfw.filter.coords;
    }
    if (url !== false) {
        $.ajax({
            url: vfw.var.DEMO_VAR + '/home/quick_filter_args/' + url,
            data: {
                'coords': JSON.stringify(coords),
                'csrfmiddlewaretoken': vfw.var.csrf_token,
            }, // data sent with the post request
            type: "POST",
            dataType: "text",
        })
            .done(function (result) {
                let json = JSON.parse(result)
                vfw.map.updateMapSelection(json)

                /** update total Value for available datasets in HTML code (and color it when no filter result): */
                $("#quickfilter-form p:first").html(
                    function (i, txt) {
                        return txt.replace(/\d+/, json['total'].toString());
                    }
                )
                if (json['total'] == 0) {
                    $("#quickfilter-form p:first").css({'background-color': 'khaki'});
                } else {
                    $("#quickfilter-form p:first").css({'background-color': 'white'});
                }

                /** Add button to select group if no more than 100 datasets are selected. The responsible button
                 * is defined with class 'group-store-button' **/
                if (json['total'] <= 100 && json['total'] > 0) {
                    $(".group-store-button").show();
                } else {
                    $(".group-store-button").hide();
                }
            })
            .fail(function (bug) {
                console.warn('got a bug in getQuickSelection: ', bug)
            })
            .always(vfw.html.loaderOverlayOff())
    }
}


/**
 * Get a river catchment / watershed according to the given coords.
 * This might take a while, so tell depending functions to wait!
 *
 * Handle creation of River Basin in django instead of geoserver to have more uniform way to access created and
 * uploaded data.
 */
vfw.map.func.getCatchment = function (start_value) {
    vfw.html.loaderOverlayOn();
    let url = '';
    let urlPart = {};
    if ('startID' in start_value) {
        urlPart = {'catchStartID': [start_value['startID']]}
        url = vfw.url.updateFilterURL(urlPart)
    } else if ('coords'in start_value) {
        urlPart = {'catchout': start_value['coords']}
        url = vfw.url.updateFilterURL(urlPart)
    }

    if (url !== false) {
        return $.ajax({
            url: vfw.var.DEMO_VAR + '/home/delineator/' + url,
            type: "GET",
            datatype: 'json',
        })
            .done(function (result) {
                vfw.filter.coords = [];
                vfw.map.func.renderCatchment(result, 'wkt')
                vfw.html.getQuickSelection(urlPart);
                vfw.map.vars.mapSelect = vfw.map.func.getSelectionEdgeCoords()[0][0];  // maybe use this var for an undo funciton in the draw menu
                return result.wkt
            })
            .fail(function (bug) {
                console.warn('3 got a bug: ', bug)
            })
            .always(vfw.html.loaderOverlayOff())
    }
}


/**
 * Renders the catchment on the map and add it as a 'Selection Layer' (and filters accordingly).
 *
 * @param {Object} catchment - the catchment object to be rendered
 */
vfw.map.func.renderCatchment = function (catchment, format, dataprojection='EPSG:4326') {
    let catch_format, dataset;
    switch (format) {
        case 'wkt':
            catch_format = new ol.format.WKT();
            dataset = catchment.wkt;
            break;
        case 'json':
            catch_format = new ol.format.GeoJSON();
            dataset = catchment;
            break;
        default:
            console.warn('Something wrong in render Catchment. ')
            return;
    }

    let catch_feature = catch_format.readFeature(dataset, {
      dataProjection: dataprojection,  // projection of your data
      featureProjection: 'EPSG:3857',  // projection used on the map
    });
    vfw.map.vars.selectionEdgeCoords = catch_feature.getGeometry();
    vfw.map.vars.mapSelect = vfw.map.vars.selectionEdgeCoords[0];

    // To visualize catchment on map a new feature is needed. The new feature is injected to the layer through a new
    // source. This source is only for catchment drawing, so when the user wants to draw again with OL standard tools,
    // the original source has to be set again in the selection layer in drawstart
    // => vfw.map.layer.selectionLayer.setSource(vfw.map.source.selectionSource);
    vfw.map.source.selectionSource_catchment = new ol.source.Vector({features: [catch_feature],});
    vfw.map.layer.selectionLayer.setSource(vfw.map.source.selectionSource_catchment);

    let coords = vfw.map.func.getSelectionEdgeCoords()
        if (vfw.util.getArrayDepth(coords) === 4) {
            vfw.filter.coords = coords[0];
        } else if (vfw.util.getArrayDepth(coords) === 3) {
            vfw.filter.coords = coords;
        } else {
            console.error('ERROR: New type of geometry. Cannot find coordinates for Button.')
        }
}

function advanced_filter_query(selection) {
    $.ajax({
        url: vfw.var.DEMO_VAR + "/home/advanced_filter",
        datatype: 'json',
        data: {
            selection: selection,
            'csrfmiddlewaretoken': vfw.var.csrf_token,
        }, // data sent with the post request
    })
        .done(function (json) {
            document.getElementById("advancedFilter").innerHTML = json

        })
        .fail(function (e) {
            console.error('Fehler: ', e)
        })
}


/**
 * Takes the ID of a button element. Used to toggle show/hide of the element following to this button element.
 * @param {string} element
 */
vfw.util.collapsibleFun = function (element) {
    let x = document.getElementById(element);
    let content = x.nextElementSibling;
    x.classList.toggle("openElement");
    if (content.style.display === "block") {
        content.style.display = "none";
    } else {
        content.style.display = "block";
    }
}


/**
 * Takes a list and returns the depth of the list as integer.
 * @param {array} value
 */
vfw.util.getArrayDepth = value => Array.isArray(value) ?
    1 + Math.max(0, ...value.map(vfw.util.getArrayDepth)) :
    0;

class SidebarButton {
    /**
     * Create base Object to create buttons from.
     * @param {string} id - The id used in the html code.
     * @param {string} orgid - The id used on the server.
     * @param {list} inputs - List of input types.
     * @param {list} outputs - List of output types.
     */
    constructor(id, orgid, inputs, outputs) {
        if (this.constructor === SidebarButton) {
            throw new TypeError('Abstract class "SidebarButton" cannot be instantiated directly.');
        }
        this.id = id;
        this.orgid = orgid;
        this.inputs = inputs;
        this.outputs = outputs;
    }
}

class SidebarButtonData extends SidebarButton {
    /**
     * Create base Object to create buttons for selected data.
     * @param {string} id - The id used in the html code.
     * @param {string} orgid - The id used on the server.
     * @param {list} inputs - List of input types.
     * @param {list} outputs - List of output types.
     * @param {string} name - Name of Dataset.
     * @param {string} unit - Unit of Dataset.
     * @param {string} abbr - Abbreviation of the name of the dataset.
     * @param {string} title - Title used in the popup for the dataset.
     * @param {date} start - Start date of selected data.
     * @param {date} end - End date of selected data.
     * @param {boolean} pickle - True (1) if pickled, else false (0).
     */
    constructor(id, orgid, inputs, outputs, name, unit
        , abbr, title, pickle, start, end) {
        super(id, orgid, inputs, outputs);
        this.name = name;
        this.unit = unit;
        this.abbr = abbr;
        this.title = this.titlefunc();
        this.pickle = pickle;
        this.start = start;
        this.end = end;
        this.type = 'data';
        this.btnName = createBtnName(this.name, this.abbr, this.unit, this.orgid);

    }

    titlefunc() {
        return this.name + ' (' + this.abbr + ' in ' + this.unit + ')';
    }
}

class SidebarButtonResult extends SidebarButton {
    /**
     * Create base Object to create buttons for selected data.
     * @param {string} id - The id used in the html code.
     * @param {string} orgid - The id used on the server.
     * @param {list} inputs - List of input types.
     * @param {list} outputs - List of output types.
     * @param {string} name - Name of Dataset.
     * @param {string} unit - Unit of Dataset.
     */
    constructor(id, orgid, inputs, outputs, name, unit) {
        super(id, orgid, inputs, outputs);
        this.name = name;
        this.unit = unit;
        this.title = this.titlefunc();
        this.pickle = true;
        this.type = 'data';
        this.btnName = this.btnNamefunc();
    }

    btnNamefunc() {
        var newName = name;
        if (sessionStorage.getItem("resultBtn")) {
            let result_btns = JSON.parse(sessionStorage.getItem("resultBtn"));
            newName = name;
            if (Object.keys(result_btns).includes(name)) {
                var i = 0;
                while (Object.keys(result_btns).includes(newName)) {
                    newName = name + i++;
                }
            }
        }
        return newName
    }

    titlefunc() {
        return this.name + ' in ' + this.unit;
    }
}

class SidebarButtonWPS extends SidebarButton {
    /**
     * Create base Object to create buttons for wps processes.
     * @param {string} id - The id used in the html code.
     * @param {string} orgid - The id used on the server.
     * @param {string} name - name written on the button.
     * @param {list} inputs - List of input types.
     * @param {list} outputs - List of output types.
     * @param {string} type - define if data or tool.
     */
    constructor(id, orgid, name, inputs, outputs) {
        super(id, orgid, name);
        this.inputs = inputs;
        this.outputs = outputs;
        this.type = 'tool'
    }
}

/**
 * Place Bokeh html code in a given html element (defiened with its ID)
 * @param {string} divID - element to add code into it
 * @param {string} data - Html code to add
 */
vfw.html.place_html_with_js = function (divID, data, ) {
    document.getElementById(divID).innerHTML = data.div; // add plot
    vfw.util.bokehResultScript = document.createElement('script');
    vfw.util.bokehResultScript.type = 'text/javascript';
    vfw.util.bokehResultScript.text = data.script;
    document.head.appendChild(vfw.util.bokehResultScript);
}

/**
 * Set Data to receive in the drop event, which is a list consisting of
 * the id of the moving element and of the parent element.
 * @private
 * @listens event:DragEvent
 * @param {Object} ev Start of the drag event outside of the canvas.
 */
function dragstart_handler(ev) {
    let path = event.path || (event.composedPath && event.composedPath());
    ev.dataTransfer.setData("text/html", JSON.stringify([
        ev.target.id,
        // ev.target.getAttribute('data-process'),
        path[1].id,
        ev.target.getAttribute('data-service')
    ]));
}

/**
 * @listens event:DragEvent
 * @param {Object} ev The drag event on the Canvas.
 */
function dragover_handler(ev) {
    ev.preventDefault();
}

/**
 * Very basic check if the given object is a valid GeoJSON.
 *
 * @param {Object} geojson - The geometry to be checked.
 * @returns {boolean} - True if the object is a valid GeoJSON, false otherwise.
 */
vfw.util.isValidGeoJson = function (geojson) {
    if (!geojson.type || typeof geojson.type === "undefined" || !geojson.coordinates) {
        return false;
    }

    if (Array.isArray(geojson.coordinates) && Array.isArray(geojson.coordinates[0])) {
        let isValid = true;

        geojson.coordinates[0].forEach(coordinate => {
            if (!Array.isArray(coordinate) || coordinate.length < 2 || typeof coordinate[0] !== "number"
                || typeof coordinate[1] !== "number") {
                isValid = false;
                return;
            }
        });
        return isValid;
    }

    if (Array.isArray(geojson.geometries) || Array.isArray(geojson.features)) {
        let isValid = true;
        (geojson.geometries || geojson.features).forEach(entry => {
            if (!isValidGeoJson(entry)) {
                isValid = false;
                return;
            }
        });
        return isValid;
    }
    return false;
}


/**
 * Checks whether a given polygon is valid or not.
 *
 * @param {Array} geojson - The polygon to be validated.
 * @returns {boolean} - True if the polygon is valid, false otherwise.
 */
vfw.util.isValidPolygon = function (geojson) {
    if (geojson.type !== "Polygon" || !Array.isArray(geojson.coordinates)) {
        return false;
    }

    for (let ring of geojson.coordinates) {
        if (!Array.isArray(ring) || ring.length < 3) {
            // Each ring of a polygon should have at least 3 points (excluding the repeated point) to be valid.
            return false;
        }

        let firstPoint = ring[0];
        let lastPoint = ring[ring.length - 1];

        for (let point of ring) {
            if (!Array.isArray(point) || point.length < 2 || typeof point[0] !== "number" || typeof point[1] !== "number") {
                return false;
            }
        }

        // Check if first and last point of ring are the same to form a closed loop, if not add the first point to the end
        if (firstPoint[0] !== lastPoint[0] || firstPoint[1] !== lastPoint[1]) {
            ring.push(firstPoint);
            console.log("The last point was missing and was automatically added to form a valid Polygon");
        }
    }
    return true;
}
