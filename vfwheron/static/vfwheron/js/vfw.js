let draw, modify, selectedFeatures, vector;
let activeMap = true;
// TODO: Don't read always from session storage. Do this "onload" and use the following var instead to read
let sessionStorageData = {};

let selectedIds = {
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
     * @param {array} oldCombinedIds
     */
    _updateFilterTable: function (oldIds) {
        if (!activeMap && this.combinedIds != oldIds) {
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

class storeData {

    constructor(definition) {
        console.log('constructor: ', definition)
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
        console.log('data: ', this.data)
        let thisID = this.data.webID;

    }
}

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
        return true ? outputType in this.HIERACHY[inputType] || inputType == outputType : false
    }

    /**
     * Return possible inputTypes for given type(s) of data.
     *
     * @param {list} inputTypeList - Datatype(s) you want to use in process
     * @return {set} - set of strings with accepted input types
     */
    accepts(inputTypeList) {
        let acceptedList = inputTypeList;
        // TODO: Use a recursive function to be prepared for a deeper hierarchy
        for (let i of inputTypeList) {
            acceptedList = acceptedList.concat(this.HIERACHY[i])
            if (Array.isArray(this.HIERACHY[i])) {
                for (let j of this.HIERACHY[i]) {
                    acceptedList = acceptedList.concat(this.HIERACHY[j])
                }
            }
        }
        // TODO: Use set more often. They are faster for 'has' tasks.
        return new Set(acceptedList)
    }
}


function createBtnName(name, abbr, unit, dbID) {
    let btnName;
    let vnLen = name.length;
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

function sidebar_btn_html(storeID, btnData, btnName, title) {
    let drag_html = "";
    if (window.location.pathname == '/workspace/') {
        drag_html = 'draggable="true" ondragstart="dragstart_handler(event)"'
    }
    let elementID = "sidebtn" + storeID;
    return '<li ' + drag_html + ' class="w3-padding task" ' +
        'data-id="' + storeID + '" btnName="' + btnName + '" onmouseover="" ' +
        'style="cursor:pointer;" id="' + elementID + '">' +
        '<span class="w3-medium" title="' + title + '">' +
        '<div class="task__content">' + btnName + '</div><div class="task__actions"></div>' +
        '</span><span class="data ' + btnData['type'] + '"></span>' +
        '<a onclick="remove_single_data(\'' + storeID + '\')" ' +
        'class="w3-hover-white w3-right"><i class="fa fa-remove fa-fw"></i>' +
        '</a><br></li>';
}

function resetDraw() {
    selectedIds.map = null;
    selectedFeatures.clear();
    olmap.removeInteraction(draw);
    olmap.removeInteraction(modify);
    olmap.removeLayer(vector);
}

// Menu to draw polygon on map
function drawPolygon(shortParent, shortChild) {
    filterbox_open();

    let collection = new ol.Collection();

    let source = new ol.source.Vector({
        wrapX: false,
        features: collection,
        useSpatialIndex: false,
        zindex: -100
    });

    // create source layer
    vector = new ol.layer.Vector({
        source: source,
        style: new ol.style.Style({
            fill: new ol.style.Fill({
                color: 'rgba(255, 255, 255, 0.2)'
            }),
            stroke: new ol.style.Stroke({
                color: '#ff0040',
                width: 1
            }),
        }),
        updateWhileAnimating: true, // optional, for instant visual feedback
        updateWhileInteracting: true // optional, for instant visual feedback
    });
    olmap.addLayer(vector);

    let select = new ol.interaction.Select(
    );

    olmap.addInteraction(select);

    draw = new ol.interaction.Draw({
        source: source,
        type: 'Polygon',
        stopClick: true
    });

    modify = new ol.interaction.Modify({
        features: collection,
        // the SHIFT key must be pressed to delete vertices, so that new
        // vertices can be drawn at the same position of existing vertices
        deleteCondition: function (event) {
            return ol.events.condition.shiftKeyOnly(event) &&
                ol.events.condition.singleClick(event);
        }
    });

    selectedFeatures = select.getFeatures();
    selectedIds.map = null;
    let sketch, listener, polygon;
    let append_str = wfsLayerName + '.';
    let features = hiddenLayer.getSource().getFeatures();

    /* Point features select/deselect as you move polygon.
        Deactivate select interaction. */
    modify.on('modifystart', function (event) {
        sketch = event.features;
        // select.setActive(false);
        listener = event.features.getArray()[0].getGeometry().on('change', function (event) {
            // clear features so they deselect when polygon moves away
            selectedFeatures.clear();
            polygon = event.target;

            for (var i = 0; i < features.length; i++) {
                if (polygon.intersectsExtent(features[i].getGeometry().getExtent())) {
                    selectedFeatures.push(features[i]);
                }
            }
        });
    }, this);
    /* Reactivate select function */
    modify.on('modifyend', function (event) {
        sketch = null;
        delaySelectActivate();
        selectedFeatures.clear();
        selectedIds.map = null;
        polygon = event.features.getArray()[0].getGeometry();

        /* select features in polygon */
        let fLen = features.length;
        for (let i = 0; i < fLen; i++) {
            if (polygon.intersectsExtent(features[i].getGeometry().getExtent())) selectedFeatures.push(features[i]);
        }
        /* get id of selected features for menu */
        selectedFeatures.getArray().forEach(function (val) {
            selectedIds.map.push(parseInt(val.getId().replace(append_str, '')))
        });
        mapSelectFuntion(shortParent, shortChild, selectedIds.map);
    }, this);

    /* //////////// SUPPORTING FUNCTIONS */
    function delaySelectActivate() {
        setTimeout(function () {
            select.setActive(true)
        }, 300);
    }

    let drwst = document.getElementById('draw_polygon');
    drwst.addEventListener('click', function () {
        olmap.removeInteraction(modify);
        olmap.addInteraction(draw);
        /* Deactivate select and delete any existing polygons.
            Only one polygon drawn at a time. */
    });
    draw.on('drawstart', function (event) {
        source.clear();
        sketch = event.feature;

        listener = sketch.getGeometry().on('change', function (event) {
            selectedFeatures.clear();
            polygon = event.target;
            let fLen = features.length;
            for (let i = 0; i < fLen; i++) {
                if (polygon.intersectsExtent(features[i].getGeometry().getExtent())) selectedFeatures.push(features[i]);
            }
        });
    }, this);

    draw.on('drawend', function () {
        // TODO: Set zindex in background (<0), and for the hidden layer in foreground e.g. 99
        selectedIds.map = [];
        selectedFeatures.getArray().forEach(function (val) {
            selectedIds.map.push(parseInt(val.getId().replace(append_str, '')))  // PaulsLayer1 to int(1)
        });
        if (selectedIds.map.length > 0) {
            mapSelectFunction(shortParent, shortChild, selectedIds.map);
        }
        olmap.removeInteraction(draw);
        toggle_draw(document.getElementById("draw_polygon"))

    });


    let modst = document.getElementById('modify_polygon');
    modst.addEventListener('click', function () {
        olmap.removeInteraction(draw);
        olmap.addInteraction(modify);
    });

    let delst = document.getElementById('' +
        'remove_polygon');
    delst.addEventListener('click', function () {
        source.clear();
        select.setActive(false);
        mapSelectFunction(shortParent, shortChild, []);
        resetDraw();
    });

    let closst = document.getElementById('draw_close');
    closst.addEventListener('click', function () {
        olmap.removeInteraction(draw);
        olmap.removeInteraction(modify);
        filterbox_close()
    });
}

//Toggle between showing and hiding filterbox
function filterbox_open() {
    let filterbox = document.getElementById("filterbox");
    filterbox.style.display = "block";
}

function filterbox_close() {
    let filterbox = document.getElementById("filterbox");
    filterbox.style.display = "none";

}

// add toggle function for background of draw and modify button, and remove background by press on delete and close
function toggle_draw(self) {
    let siblings = document.getElementsByClassName('draw-hover');
    let s;
    let sLen = siblings.length - 1;  // avoid to toggle on the delete button
    if (self.classList.contains('activeM')) {
        self.classList.remove('activeM');
        draw.finishDrawing();
    } else {
        for (s = 0; s < sLen; s++) {
            if (siblings[s].classList.contains('activeM')) siblings[s].classList.remove('activeM')
        }
        if (self.id !== siblings[sLen].id && self.id !== 'draw_close') self.classList.add('activeM')
    }
}

//Search
function search_close() {

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
            "onclick='search_close()'><i class='fa fa-search fa-fw'></i></a>";

        let closeBut = document.getElementById("srch_close_but");
        closeBut.outerHTML = "<a href='javascript:void(0)' class='w3-hover-white' style='height:103px' " +
            "id='search_close_but' onclick='search_close()'><i class='fa fa-remove fa-fw'></i></a>";
    }
}

// TODO: check if CSRF is properly implemented! vgl. https://godjango.com/18-basic-ajax/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        let nLen = name.length;
        let cLen = cookies.length;
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

// TODO: not used in this file. So from where comes the used token? Which one is better?
let csrf_token = getCookie('csrftoken');

//build menu on sidebar
$(document).ready(function (menuTitle) {
    $('#accordion').accordion({
        heightStyle: "content",
        active: false,
        collapsible: true,
    });
    $("h5.w3-hover-blue.nav").click(function () {
        // var menuValue = $(this).attr("value");
// open accordion
        $('div #subaccordion').accordion({
            heightStyle: "content",
            active: false,
            collapsible: true,
        });
    });
}); // end ready

/**
 * Load metadata and preview plot of dataset from server asynchronous.
 *
 * @param {string} id of dataset as string.
 */
function moreInfoModal(id) {
    let tb = false, pb = false;
    let modLock = false;
    let pdata, tdata;

    let ajaxTable = function () {
        return $.ajax({
            url: DEMO_VAR + "/home/show_info",
            dataType: 'json',
            data: {
                show_info: id,
                'csrfmiddlewaretoken': csrf_token,
            }, // data sent with post request
        })
    }
    // load preview image parallel to metadata
    let ajaxPlot = function () {
        // id = 'bla'
        return $.ajax({
            url: DEMO_VAR + "/home/previewplot",
            datatype: 'image/png;base64',
            // datatype: 'html',
            data: {
                preview: id,
                'csrfmiddlewaretoken': csrf_token,
            }, // data sent with the post request
        })

    }
    document.getElementById('mod_dat_inf').innerHTML = "";
    document.getElementById("mod_prev").innerHTML = "";
    document.getElementById("mod_prev").classList.add("loader");

    // The following is used to make sure to add first the table then the plot.
    function tableToModal(properties) {
        let metaText = '<table>';
        // loop over "properties" dict with metadata, build columns
        for (let j in properties) {
            // TODO: compare with let values = eval('properties["' + j + '"]'); in buildPopupTextvfw why eval?
            metaText += '<tr><td><b>' + j + '</b></td><td>' + properties[j] + '</td></tr>';
        }
        document.getElementById('mod_dat_inf').innerHTML = metaText + '</table>';
        showDataInfo(properties);
    }

    function plotToModal(json) {
        document.getElementById('mod_prev').innerHTML = json.div; // add plot
        // bokehPreviewScript is a global variable to set and remove the script of bokeh
        bokehPreviewScript = document.createElement('script');
        bokehPreviewScript.type = 'text/javascript';
        bokehPreviewScript.text = json.script;
        document.head.appendChild(bokehPreviewScript);
    }

    function fillModal(td, pd) {
        tableToModal(td)
        if (pdata !== false) {
            plotToModal(pd)
        }
        document.getElementById("mod_prev").classList.remove("loader")
    }

    // Following .done calls are made to ensure that table is first and plot is second created in the modal
    // TODO: better errorhandling, especially for ajaxTable
    ajaxTable()
        .done((data) => {
            tdata = data
            tb = true
            if (pb == true && modLock == false) {
                modLock = true
                fillModal(tdata, pdata)
            }
        })
    // .always(document.getElementById("mod_prev").classList.remove("loader"))
    ajaxPlot()
        .done((data) => {
            pdata = data
            pb = true
            if (tb == true && modLock == false) {
                modLock = true
                fillModal(tdata, pdata)
            }
        })
        .fail(() => {
            pb = true;
            pdata = false
        })

    let modal = document.getElementById("infoModal");
    modal.style.display = "block";
}

/**
 * send request to view to get info about selection
 * @param {string} id - can be a single id or a list of ids
 */
function workspace_dataset(id) {
    if (id !== 'null') {
        $.ajax({
            url: DEMO_VAR + "/home/workspace_data",
            datatype: 'json',
            data: {
                workspaceData: id,
                'csrfmiddlewaretoken': csrf_token,
            }, // data sent with post request
        })
            .done(function (json) {
                if (json['error']['message']) {
                    console.log("json['error']['message']: ", json['error']['message'])
                    // TODO: handle errors/data selected but without access
                    console.warn('Some of the data you requested shouldn\'t be available to request. Implement fix!')
                }
                if (sessionStorage.getItem("dataBtn")) {
                    let stored = JSON.parse(sessionStorage.getItem("dataBtn"));
                    $.each(json['workspaceData'], function (key, value) {
                        console.log('key: ', key)
                        console.log('value: ', value)
                        if (!stored[key]) stored[key] = value;
                    });
                    sessionStorage.setItem("dataBtn", JSON.stringify(stored))
                    sessionStorageData = stored;
                } else {
                    console.log("json['workspaceData']: ", json['workspaceData'])
                    sessionStorage.setItem("dataBtn", JSON.stringify(json['workspaceData']));
                    sessionStorageData = json['workspaceData']

                    $.each(json['workspaceData2'], function (k, v) {
                        let dataset = new storeData(json['workspaceData2'][k])
                        //dataset.save(json['workspaceData2'][k])
                        console.log('dataset.data: ', dataset.data)
                        sessionStorage.setItem("data", JSON.stringify({[dataset.data.webID]: dataset.data}))
                    });
                }
                // build buttons
                build_datastore_button(json['workspaceData']);
            }) // function in sidebar.js
    }
}

/**
 * Send ID to server to build preview and add preview image to html
 * @param {int} id - Id of dataset
 */
function show_preview(id) {
    document.getElementById("show_data_preview" + id.toString()).value = "Loading Preview";
    $.ajax({
        url: DEMO_VAR + "/home/previewplot",
        datatype: 'image/png;base64',
        data: {
            preview: id,
            'csrfmiddlewaretoken': csrf_token,
        }, // data sent with the post request
    })
        .done(function (json) {
            $.each(json, function (key, value) {
                // document.getElementById("preview_img").innerHTML = '<img src="data:image/svg,' + value; // Strobl svg
                document.getElementById("preview_img").innerHTML = value; // png
                document.getElementById("show_data_preview" + id.toString()).value = "Reload Preview"
            });
        })
        .fail(function (e) {
            console.error('fehler: ', e)
        })
}

function toggleMapTable(evt, tabName) {
    // Declare all variables
    let i, tabcontent, tablinks;
    activeMap = tabName === "Map";

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}


function toggleFilter(evt, tabName) {
    // Declare all variables
    let i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("filter-tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("filter-tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}


function filter_pagination(page) {
    console.log('page: ', page)
    console.log('selectedIds.result: ', selectedIds.result)
    $.ajax({
        url: DEMO_VAR + "/home/entries_pagination",
        datatype: 'json',
        data: {
            page: page, datasets: JSON.stringify(selectedIds.result),
            'csrfmiddlewaretoken': csrf_token,
        }, // data sent with the post request
    })
        .done(function (json) {
            document.getElementById("paginationTable").innerHTML = json

        })
        .fail(function (e) {
            console.error('Fehler: ', e)
        })
}


function advanced_filter_query(selection) {
    $.ajax({
        url: "/home/advanced_filter",
        datatype: 'json',
        data: {
            selection: selection,
            'csrfmiddlewaretoken': csrf_token,
        }, // data sent with the post request
    })
        .done(function (json) {
            console.log('json: ', json)
            document.getElementById("advancedFilter").innerHTML = json

        })
        .fail(function (e) {
            console.error('Fehler: ', e)
        })
}


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
     * @param {string} title - Title used in the popup for the dataset.
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

function place_bokeh(divID, data) {
    document.getElementById(divID).innerHTML = data.div; // add plot
    bokehResultScript = document.createElement('script');
    bokehResultScript.type = 'text/javascript';
    bokehResultScript.text = data.script;
    document.head.appendChild(bokehResultScript);
}

/**
 * Set Data to receive in the drop event, which is a list consisting of
 * the id of the moving element and of the parent element.
 * @private
 * @listens event:DragEvent
 * @param {Object} ev Start of the drag event outside of the canvas.
 */
function dragstart_handler(ev) {
    ev.dataTransfer.setData("text/plain", JSON.stringify([
        ev.target.id,
        // ev.target.getAttribute('data-process'),
        ev.path[1].id,
        ev.target.getAttribute('data-service')
    ]));
}

/**
 * @private
 * @listens event:DragEvent
 * @param {Object} ev The drag event on the Canvas.
 */
function dragover_handler(ev) {
    ev.preventDefault();
}
