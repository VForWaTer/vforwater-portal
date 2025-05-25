/*
 * Project Name: V-FOR-WaTer
 * Author: Marcus Strobl
 * Contributors: Safa Bouguezzi
 * License: MIT License
 */

/**
 * Represents a data set of the VFW datasets.
 * create new object with new vfw.datasets.DataObj(json).
 *
 * @class
 * @memberof vfw.datasets
 *
 * @param {object} data - The data that the object should contain.
 */
vfw.datasets.DataObj = class {
    orgID = "";
    uuID = "";
    workID = "";
    abbr = "";
    name = "";
    unit = "";
    title = "";
    type = "";
    start = "";
    end = "";
    inputs = {};
    outputs = {};
    location = {};
    geom = {};
    isGroupMember = "";
    group = "";
    source = "";

    constructor(data, newElement=true) {
        const defaultParams = {
            orgID: "",  // used also as ID for buttons and in session storage
            uuID: "",
            workID: "",
            abbr: "",
            name: "",
            unit: "",
            title: "",
            type: "",   // datatype for combining datasets in workspace
            start: "",  // min selection
            end: "",    // max selection
            dateTimeLimits: [],  // [minDateTime, maxDateTime]
            spatialLimit: [],
            inputs: {},
            outputs: {},
            location: {},   // {type: string, coordinates: [lat, lon]
            geom: {},
            isGroupMember: "",
            group: "",
            groupID: "",
            DBgroup: "",
            DBgroupID: "",
            source: "", //this.setSource(),
            sessionStorage: "",
        };
        this.htmlName = "";  // run createHtmlName to fill this
        this.inputs = [];
        this.noData = "";  // TODO: what was the purpose of this variable again?
        this.title = "";
        this.isResult = false;
        this.url = window.location.pathname;

        Object.assign(this, {...defaultParams, ...data});

        if (!this.orgID) {
            console.error("Error creating Data Object. An orgID is required to create Data Object.");
            return
        }
        if (this.isResult) {
            this.storeKey = "resultBtn";
            this.btnPosition = "";
        } else {
            this.storeKey = "dataBtn";
            this.btnPosition = "workspace";
        }

        this._setTitle();
        this._createHtmlName();
        this._setSource();
        if (this.group.trim().length !== 0) {
            this.isGroupMember = true;
            this._buildHtmlGroup()
        }
        this._placeHtmlButton();
        if (newElement) {
            this.save(data);
        }
    }

    /**
     * Retrieves a plot of the represented data from the server and displays it on the page.
     *
     * @returns {void}
     */
    getPlot() {
        vfw.html.loaderOverlayOn();
        $.ajax({
            url: vfw.var.DEMO_VAR + "/home/previewplot",
            datatype: 'json',
            data: {
                preview: this.orgID,
                'csrfmiddlewaretoken': vfw.var.csrf_token,
                startdate: this.start,
                enddate: this.end,
            }, // data sent with post
        })
            .done(function (requestResult) {
                if ('html' in requestResult) {
                    document.getElementById("mod_result").innerHTML = requestResult.html; // add plot
                } else {  // plot from bokeh
                    vfw.var.obj.bokehImage = requestResult;
                    vfw.html.place_html_with_js("mod_result", requestResult)
                }
                vfw.html.resultModal.style.display = "block";
            })
            .fail(function (e) {
                console.error('Fehler: ', e)
            })
            .always(function () {
                vfw.html.loaderOverlayOff();
            })
    }

    /**
     * Creates the unique ID of an HTML element.
     *
     * The ID is composed of three parts: btnPosition, workID, and orgID.
     *
     * @return {string} The unique ID of the HTML element.
     */
    htmlElementID() {
        return this.btnPosition + this.workID + this.orgID; // storeID;  // TODO: not sure what storeID should be or any other ID here...}
    }

    /**
     * Removes data from portal and session storage.
     *
     * @param {string} [removeData=this.orgID] - The identifier of the data to be removed.
     * @return {void}
     */
    removeData(removeData = this.orgID) {  // TODO: removeData var should be taken from this!
        /** remove data from portal: **/
        document.getElementById(this.htmlElementID()).remove();

        /** remove data from session: **/
        let workspaceData = JSON.parse(sessionStorage.getItem(this.storeKey));

        delete workspaceData[removeData];
        delete vfw.datasets.dataObjects[removeData];
        sessionStorage.setItem(this.storeKey, JSON.stringify(workspaceData))
        sessionStorageData = workspaceData  // is this already in use somewhere? Then add it also in Result Buttons
    }


    Downloadcsv = function() {
        vfw.html.loaderOverlayOn();
        const obj = this;
        $.ajax({
            url: vfw.var.DEMO_VAR + "/home/datasetdownload",
            datatype: 'json', 
            data: {
                csv: obj.orgID, 
            },
        })
        .done(function(csvData) {
            const blob = new Blob([csvData], {type: "text/csv;charset=utf-8"});
            saveAs(blob, vfw.datasets.dataObjects[obj.orgID].name  + ".csv"); 
        })
        .fail(function(error) {
            console.error('Download failed', error);
        })
        .always(function() {
            vfw.html.loaderOverlayOff();
        });
    };


    DownloadGeoJSON = function() {
        const obj = this; 
        $.ajax({
            url: vfw.var.DEMO_VAR + "/home/datasetdownload", 
            datatype: 'json', 
            data: {
                geojson: obj.orgID, 
            },
        })
        .done(function(geojsonData) {
            const blob = new Blob([JSON.stringify(geojsonData)], {type: "application/json"});
            saveAs(blob, vfw.datasets.dataObjects[obj.orgID].name  + ".geojson"); 
        })
        .fail(function(error) {
            console.error('Download failed', error);
        })
        .always(function() {
            vfw.html.loaderOverlayOff();
        });
    };

    /**
     * Saves data to session storage.
     * @param {Object} data - The data to be saved.
     * @param {boolean} [update=false] - Indicates whether to update existing data or not.
     * @return {void}
     */
    save(data, update = false) {
        let stored;
        data['inSessionStorage'] = true;
        if (sessionStorage.getItem(this.storeKey)) {
            stored = JSON.parse(sessionStorage.getItem(this.storeKey));
            if (update || !stored[this.orgID]) {
                stored[this.orgID] = data;
            }
            sessionStorage.setItem(this.storeKey, JSON.stringify(stored))
            sessionStorageData = stored;
        } else {
            let sessionEntry = {};
            if (this.orgID) {
                sessionEntry[this.orgID] = data;
            } else {
                sessionEntry[this.orgID] = this.name;
            }
            sessionStorage.setItem(this.storeKey, JSON.stringify(sessionEntry));
            sessionStorageData = data
        }
    }

    /** Several functions to fill and show a context menu
     * - actually its a more user friendly  dropdown instead of a context menu -
     * **/
    showContextMenu() {
        let htmlElements = `<ul class="context-menu__items">${this._createContextMenu(this.orgID)}</ul>`

        vfw.sidebar.html.contextModal.open(htmlElements)
    }

    /**
     * Builds the HTML group panel content.
     *
     * @returns {string} The HTML code for the group panel.
     */
    _buildHtmlGroup() {
        let html = `<div class="grouppanel content">${this.group}</div>`
    }

    /**
     * Create a context menu for the given dataset according to its datatype.
     *
     * @param {string} orgID - The ID of the organization.
     * @return {string} - The HTML elements of the context menu.
     */
    _createContextMenu(orgID) {
        let htmlElements = ""
        let itemParams = {
            "geometry": [
                ["Downloadshp", "fa-download", gettext("Download data") + " (.shp)"],
                ["RemoveDataSet", "fa-eraser", gettext("Remove dataset")]
            ],
            "timeseries": [
                ["Plot", "fa-eye", gettext("Plot data"), "getPlot"],
                ["Downloadxml", "fa-download", gettext("Download metadata") + " (.xml)"],
                ["Downloadcsv", "fa-download", gettext("Download data") + " (.csv)", "Downloadcsv"],
                ["DownloadGeoJSON", "fa-download", gettext("Download data") + " (.geojson)", "DownloadGeoJSON"],
                ["Downloadshp", "fa-download", gettext("Download data") + " (.shp)"],
                ["RemoveDataSet", "fa-eraser", gettext("Remove dataset"), "removeData"]
            ],
            "default": [
                ["RemoveDataSet", "fa-eraser", gettext("Remove dataset"), "removeData"]
            ]
        }

        /** Build a html button for the context menu
         *
         * */
        function createMenuItem(action, iconClass, name, func) {

            htmlElements += `<li class="context-menu__item"> ` +
                `<a class="context-menu__link" data-action=${action} ` +
                `onclick=vfw.datasets.dataObjects['${orgID}'].${func}('${orgID}') > ` +
                `<i class="fa ${iconClass}"></i> ${name}</a>` +
                `</li>`
        }

        if (this.type in itemParams) {
            itemParams[this.type].forEach((value) => createMenuItem(...value))
        } else {
            itemParams["default"].forEach((value) => createMenuItem(...value))
        }

        return htmlElements

    }

    /**
     * Creates an HTML button element with drag and drop functionality in the sidebar.
     *
     * @return {string} - The HTML string of the button element.
     */
    _createHtmlButton() {
        /** set where to place the button **/
        let dragHtml = "";
        if (this.url === '/workspace/') {
            dragHtml = 'draggable="true" ondragstart="dragstart_handler(event)"'
        }
        return `<li ` + dragHtml + ` class="w3-padding task" data-sessionstore=${this.storeKey} ` +
            `data-orgid="${this.orgID}"` +
            `data-id="${this.orgID}" btnName="${this.htmlName}" onmouseover="" ` +  // TODO: remove btnName - might be used when dropped i dropzone
            `data-btnName="${this.htmlName}" style="cursor:pointer;" id="${this.htmlElementID()}">` +
            `<span class="w3-medium" title="${this.title}">` +
            `<div class="task__content ${this.noData}">${this.htmlName}</div><div class="task__actions"></div>` +
            `</span><span class="data ${this.type}" title="Type: ${this.type}"></span>` +
            `<a onclick=vfw.datasets.dataObjects['${this.orgID}'].removeData('${this.orgID}') ` +
            `class="w3-hover-white w3-right"><i class="fa fa-remove fa-fw"></i>` +
            `</a>` +
            `<a onclick=vfw.datasets.dataObjects['${this.orgID}'].showContextMenu('${this.orgID}') ` +
            `class="w3-hover-white w3-right"><i class="fa fa-caret-down fa-fw"></i>` +
            `</a><br></li>`;
    }

    /**
     * Create a name for buttons according to the length of the name string
     */
    _createHtmlName() {
        let vnLen = this.name.length;
        if (this.source === "userUpload") {
            this.htmlName = this.name.slice(0, 17);
        } else if (vnLen + this.abbr.length + this.unit.length <= 13) {
            if (this.abbr !== "" && this.unit !== "") {
                this.htmlName = this.name + '(' + this.abbr + ' in ' + this.unit + ') - ' + this.dbID;
            } else {
                this.htmlName = this.name + ' - ' + this.dbID;
            }

        } else if (vnLen + this.abbr.length <= 15) {
            this.htmlName = this.name + '(' + this.abbr + ') - ' + this.dbID;
        } else if (vnLen <= 17) {
            this.htmlName = this.name + ' - ' + this.dbID;
        } else {
            this.htmlName = this.abbr + ' in ' + this.unit + ' - ' + this.dbID;
        }
        //     check if the name is unique and append a number if not
        let newName = this.htmlName;
        if (sessionStorage.getItem(this.storeKey)) {
            let result_btns = JSON.parse(sessionStorage.getItem(this.storeKey));
            let i = 0;
            while (Object.keys(result_btns).includes(newName)) {
                newName = name + i++;
            }
        }
        this.htmlName = newName;
    }

    _loadPlot() {
        $.ajax({
            url: vfw.var.DEMO_VAR + "/home/previewplot",
            datatype: 'json',
            data: {
                preview: this.id,
                'csrfmiddlewaretoken': vfw.var.csrf_token,
                startdate: this.start,
                enddate: this.end,
            }, // data sent with post
        })
    }

    _placeHtmlButton() {
        document.getElementById(this.btnPosition).innerHTML += this._createHtmlButton();
    }

    _replaceHtmlButton() {
        let thisHtmlButton = document.getElementById(this.htmlElementID())
        $(thisHtmlButton).replaceWith(this._createHtmlButton());
    }

    async _requestData(url, data) {
        let preloadData = {};
        return new Promise((resolve, reject) => {
                $.ajax({
                    url: vfw.var.DEMO_VAR + url,
                    "timeout": 5000,
                    data: {
                        dbload: JSON.stringify(data), 'csrfmiddlewaretoken': vfw.var.csrf_token,
                    }, /** data sent with post request **/
                })
                    .done(resultJson => {
                        preloadData = resultJson;
                        resolve(resultJson);
                    })
                    .fail(wpsDBInfo => {
                        console.error('Error in preload of data. ', wpsDBInfo)
                        reject(wpsDBInfo);
                    });
            }
        )
    }

    _setSource() {
        if (this.source) {
            if (this.source.substring(0, 2) === 'db') {
                this.source = 'db'
            } else if (this.source.substring(0, 3) === 'wps') {
                this.source = 'wps'
            }
        } else {
            this.source = ''
        }
    }

    _setTitle() {
        if (this.type == null) {
            this.noData = "noDataBtn";
            this.title = "Internal error. No data available for this metadata record.";
        } else {
            this.title = `${this.name} (${this.abbr} in ${this.unit})`;
        }
    }

    async _update() {
        /**
         * Ensure datasets without type will not be loaded (because usually they have no actual data)
         * Function to make data available before the user runs a tool. Was used to improve user experience.
         **/
        if (!this.type) return

        if (this.source === 'db') {
            let preloadData = {
                key_list: ['entry_id', 'uuid', 'start', 'end'],
                value_list: [this.orgID.toString(), this.uuID, this.start, this.end],
                dataset: this.orgID
            };
            let wpsDBInfo = await this._requestData("/workspace/dbload", preloadData)
            if (wpsDBInfo.Error) {
                console.warn(wpsDBInfo.Error)
                return
            }
            if (wpsDBInfo['id'].substring(0, 3) === 'wps') {
                /** update properties **/
                this.source = wpsDBInfo['id'].substring(0, 3);
                this.dbID = wpsDBInfo['id'].substring(3,);
                this.inputs = wpsDBInfo['inputs'];
                /** adjust html and sessionStorage **/
                let properties = {};
                for (const key of Object.keys(this)) {
                    properties[key] = this[key];
                }
                this.save(properties, true)
                this._createHtmlName()
                this._createHtmlButton()
                this._replaceHtmlButton()
            }
        }
    }

    _updateGeom(data) {
        this.geom = data["geom"];
    }
}
