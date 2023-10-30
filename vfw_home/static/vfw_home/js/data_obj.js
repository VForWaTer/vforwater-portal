/*
create new object with new vfw.datasets.DataObj(json)
*/
vfw.datasets.DataObj = class {
    orgID;
    uuID;
    workID;
    abbr;
    name;
    unit;
    title;
    type;
    start;
    end;
    inputs;
    outputs;
    location;
    isGroupMember;
    group;
    source;

    constructor(data) {
        const defaultParams = {
            orgID: "",
            uuID: "",
            workID: "",
            // source: "",
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

        // if (Array.isArray(this.inputs) && this.inputs.length) {
        if (this.isResult) {
            this.storeKey = "resultBtn";
            this.btnPosition = "";
        } else {
            this.storeKey = "dataBtn";
            this.btnPosition = "workspace";
            // this.btnPosition = "sidebtn";
        }

        this.#setTitle();
        this.#createHtmlName();
        this.#setSource();
        if (this.group.trim().length !== 0) {
            this.isGroupMember = true;
            this.#buildHtmlGroup()
        }
        this.#placeHtmlButton();
        this.save(data);
        if (this.url !== `/home/`) {
            this.#update()
        }
    }

    htmlElementID() {
        return this.btnPosition + this.workID + this.orgID; // storeID;  // TODO: not sure what storeID should be or any other ID here...}
    }

    #buildHtmlGroup() {
        let html = `<div class="grouppanel content">${this.group}</div>`
    }

    #placeHtmlButton() {
        document.getElementById(this.btnPosition).innerHTML += this.#createHtmlButton();
    }

    #createHtmlButton() {
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
            `</span><span class="data ${this.type}"></span>` +
            `<a onclick=vfw.datasets.dataObjects['${this.orgID}'].removeData('${this.orgID}') ` +
            `class="w3-hover-white w3-right"><i class="fa fa-remove fa-fw"></i>` +
            `</a>` +
            `<a onclick=vfw.datasets.dataObjects['${this.orgID}'].showContextMenu('${this.orgID}') ` +
            `class="w3-hover-white w3-right"><i class="fa fa-caret-down fa-fw"></i>` +
            `</a><br></li>`;
    }

    #setSource() {
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

    #setTitle() {
        if (this.type == null) {
            this.noData = "noDataBtn";
            this.title = "Internal error. No data available for this metadata record.";
        } else {
            this.title = `${this.name} (${this.abbr} in ${this.unit})`;
        }
    }

    save(data, update = false) {
        let stored;
        data['inSessionStorage'] = true;
        if (sessionStorage.getItem(this.storeKey)) {
            stored = JSON.parse(sessionStorage.getItem(this.storeKey));
        }
        if (sessionStorage.getItem(this.storeKey)) {
            stored = JSON.parse(sessionStorage.getItem(this.storeKey));
            if (update || !stored[this.orgID]) {
                stored[this.orgID] = data;
            }
            sessionStorage.setItem(this.storeKey, JSON.stringify(stored))
            sessionStorageData = stored;
        } else {
            let sessionEntry = {};
            sessionEntry[this.orgID] = data;
            sessionStorage.setItem(this.storeKey, JSON.stringify(sessionEntry));
            sessionStorageData = data
        }
    }

    // groupName = vfw.sidebar.set_group_btn_name(modal_input.outputName, 'resultBtn');

    /**
     * Create a name for buttons according to the length of the name string
     */
    #createHtmlName() {
        let vnLen = this.name.length;
        if (vnLen + this.abbr.length + this.unit.length <= 13) {
            this.htmlName = this.name + '(' + this.abbr + ' in ' + this.unit + ') - ' + this.dbID;
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

    removeData(removeData=this.orgID) {  // TODO: removeData var should be taken from this!
        /** remove data from portal: **/
        document.getElementById(this.htmlElementID()).remove();

        /** remove data from session: **/
        let workspaceData = JSON.parse(sessionStorage.getItem(this.storeKey));

        delete workspaceData[this.orgID];
        sessionStorage.setItem(this.storeKey, JSON.stringify(workspaceData))
        sessionStorageData = workspaceData  // is this already in use somewhere? Then add it also in Result Buttons
    }

    async #requestData(url, data) {
        let preloadData = {};
        return new Promise((resolve, reject) => {
                $.ajax({
                    url: vfw.var.DEMO_VAR + url,
                    // dataType: 'json',
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

    async #update() {
        /** ensure datasets without type will not be loaded (because usually they have no actual data) **/
        if (!this.type) return

        if (this.source === 'db') {
            let preloadData = {
                key_list: ['entry_id', 'uuid', 'start', 'end'],
                value_list: [this.orgID.toString(), this.uuID, this.start, this.end],
                dataset: this.orgID
            };
            let wpsDBInfo = await this.#requestData("/workspace/dbload", preloadData)
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
                this.#createHtmlName()
                this.#createHtmlButton()
                this.#replaceHtmlButton()
            }
        }
    }

    #replaceHtmlButton() {
        let thisHtmlButton = document.getElementById(this.htmlElementID())
        $(thisHtmlButton).replaceWith(this.#createHtmlButton());
    }

    /** Several functions to fill and show a context menu
     * - actually its a more user friendly  dropdown instead of a context menu -
     * **/
    showContextMenu() {
        console.log('...reached')
        // TODO: used modal instead of context => rename and remove unnecessary code like action in createContextMenu
        let htmlElements = this.#createContextMenu(this.orgID)
        vfw.workspace.modal.openResultModal(htmlElements, true)

    }

    getPlot() {
        console.log('getPlot: ')
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
                place_html_with_js("mod_result", requestResult)
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

    #createContextMenu(orgID) {
        let htmlElements = ""
        let itemParams = {
            "timeseries": [
                ["Plot", "fa-eye", gettext("Plot data"), "getPlot"],
                ["Downloadxml", "fa-download", gettext("Download metadata") + " (.xml)"],
                ["Downloadcsv", "fa-download", gettext("Download data") + " (.csv)"],
                ["Downloadshp", "fa-download", gettext("Download data") + " (.shp)"],
                ["RemoveDataSet", "fa-eraser", gettext("Remove dataset")]
            ]}

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

        itemParams[this.type].forEach((value) => createMenuItem(...value))

        return htmlElements

    }
    #loadPlot() {
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

}

