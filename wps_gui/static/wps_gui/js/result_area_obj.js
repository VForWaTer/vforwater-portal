/**
create new object with new vfw.datasets.resultObjects[json['orgID']] = new vfw.datasets.resultObj(json)
The object is mainly copied from data_obj.js, and many functions can be carefully removed.
*/
vfw.datasets.resultObj = class {

    storedTool = "";
    htmlName = "";
    id = "";
    btnData = {};
    orgID = "";
    url = window.location.pathname;
    title = "";

    dbID = "";
    inputs = "";
    input_keys = "";
    input_values = "";
    name = "";
    type = "";
    outputs = "";
    wps = "";
    status = "";
    dropBtn = "";
    group = "";
    sessionStorage = "";
    btnPosition = "";
    htmlElementID = "";

    constructor(data) {
        const defaultParams = {
            // source: "",
            // type: "geometry",   // datatype for combining datasets in workspace
            source: "wps", //this.setSource(),
            storeKey: "resultBtn",
            btnPosition: "workspace_results"  // ID of html element to add the button
            }

        Object.assign(this, {...defaultParams, ...data});
        console.log('this: ', this)
        this._createHtmlName();
        console.log('this. name : ', this.name)
        console.log('this. orgID : ', this.orgID)
        this.htmlElementID = this.btnPosition + this.orgID;

        // this.storeKey = "resultBtn";
        // this.btnPosition = "workspace";
        this._adaptOrgID();

        this._setTitle();
        this._setSource();
        if (this.group.trim().length !== 0) {
            this.isGroupMember = true;
            this._buildHtmlGroup()
        }
        this._placeHtmlButton();
        this.save();
    }

    download(element=this.orgID) {  // TODO: removeData var should be taken from this!
        /** remove data from session: **/
        const workspaceData = JSON.parse(sessionStorage.getItem(this.storeKey));
        const jsonBlob = new Blob([JSON.stringify(this.gjson)], {type: 'application/json'});
        const url = URL.createObjectURL(jsonBlob);
        const link = document.createElement('a');
        link.href = url;

        // if the element name has the ending '.json' use it, else add '.json' to the name
        link.download = workspaceData[element]['name'].slice(-5) === '.json' ? workspaceData[element]['name'] :
            workspaceData[element]['name'] + '.json';

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    filterData(element=this.orgID) {  // TODO: removeData var should be taken from this!
        vfw.map.func.renderCatchment(this.gjson, 'json')
        vfw.html.getQuickSelection({'draw': vfw.map.func.getSelectionEdgeCoords()});
    }

    removeData(removeData=this.orgID) {  // TODO: removeData var should be taken from this!
        /** remove data from portal: **/
        document.getElementById(this.htmlElementID).remove();

        /** remove data from session: **/
        let workspaceData = JSON.parse(sessionStorage.getItem(this.storeKey));

        delete workspaceData[removeData];
        delete vfw.datasets.resultObjects[this.orgID];
        sessionStorage.setItem(this.storeKey, JSON.stringify(workspaceData))
        sessionStorageData = workspaceData  // is this already in use somewhere? Then add it also in Result Buttons
    }

    /**
     * Send request to django if there is an update on the process.
     * If yes, update object (with sessionstorage and html)
     */
    refresh() {  // TODO: removeData var should be taken from this!

        $.ajax({
            url: vfw.var.DEMO_VAR + '/workspace/processstate',
            data: {'processid': this.id,
                'csrfmiddlewaretoken': vfw.var.csrf_token,
            }
        })
            .done(result => {
                if (result.status !== this.status) {
                    this.status = result.status;
                    this.update(result);
                }
            })
            .fail(error => {
                console.warn('failed getting data from server: ', error)
        })

    }

    /** save info to build object in session Storage
     * @param {Object} data - The data to be stored. Default is the whole object.
     * **/
    save(data = this, update = false) {
        let stored;
        let newID = this.orgID
        data['inSessionStorage'] = true;
        if (sessionStorage.getItem(this.storeKey)) {
            stored = JSON.parse(sessionStorage.getItem(this.storeKey));
            if (update || !stored[newID]) {
                stored[newID] = data;
            }
            sessionStorage.setItem(this.storeKey, JSON.stringify(stored))
            sessionStorageData = stored;
        } else {
            let sessionEntry = {};
            sessionEntry[newID] = data;
            sessionStorage.setItem(this.storeKey, JSON.stringify(sessionEntry));
            sessionStorageData = data
        }
    }

    load() {
        console.log('this.storeKey: ', this.storeKey)
        return sessionStorage.getItem(this.storeKey);
    }

    /** Several functions to fill and show a context menu
     * - actually its a more user friendly  dropdown instead of a context menu -
     * **/
    showContextMenu() {
        // TODO: used modal instead of context => rename and remove unnecessary code like action in createContextMenu
        let htmlElements = `<ul class="context-menu__items">${this._createContextMenu(this.orgID)}</ul>`
        console.log('htmlElements: ', htmlElements)

        vfw.sidebar.html.contextModal.open(htmlElements)
    }

    /**
     * Update the html and geometry data of an object.
     * @param {Object} data - The updated data to be applied.
     */
    update(data) {
        let properties = {}; //= this.load();
        for (const key of Object.keys(this)) {
            properties[key] = this[key];
        }
        properties['geom'] = data;
        this.save(properties, true)
        this._createHtmlName()
        this._createHtmlButton()
        this._replaceHtmlButton()
        // this.geom = data["geom"];
    }

       /**
     * Generate a new ID by appending a number to the given ID,
     * if the given name already exists in the result button list of the sessionStorage.
     */
    _adaptOrgID() {
        let existingObj = {};
        let newID = this.orgID;
        if (sessionStorage.getItem(this.storeKey)) {
            existingObj = JSON.parse(sessionStorage.getItem(this.storeKey));
            if (Object.keys(existingObj).includes(newID)) {
                var i = 0;
                while (Object.keys(existingObj).includes(newID)) {
                    newID = `${this.orgID}_${i++}`;
                }
            }
        }
        this.orgID = newID;
        return newID;
    }

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

    const itemParams = {
        // set parameters: action, iconClass, name, function
        "geometry": [
            ["DownloadJSON", "fa-download", gettext("Download data"), "download"],
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
            `onclick=vfw.datasets.resultObjects['${orgID}'].${func}('${orgID}') > ` +
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

    _createHtmlButton() {
        /** set where to place the button **/
        let dragHtml = "";
        let stateIndicator = "";
        if (this.url === '/workspace/') {
            dragHtml = 'draggable="true" ondragstart="dragstart_handler(event)"'
        }
        if (this.status === "ACCEPTED" || this.status === "CREATED") {  // add refresh button if not finished
            stateIndicator = `<a onclick=vfw.datasets.resultObjects[\'${this.orgID}\'].refresh() ` +
                `class="w3-hover-white"><i class="process-state fa fa-refresh process-${this.status}"></i>`
        } else {
            stateIndicator = `<i class="process-state process-${this.status}"></i>`
        }
        return `<li ` + dragHtml + ` class="w3-padding task" data-sessionstore=${this.storeKey} ` +
            `data-orgid="${this.orgID}"` +
            `data-id="${this.orgID}" btnName="${this.htmlName}" onmouseover="" ` +  // TODO: remove btnName - but might be used when dropped in dropzone...
            `data-btnName="${this.htmlName}" style="cursor:pointer;" id="${this.htmlElementID}">` +
            `<span class="w3-medium" title="${this.title}">` +
            `<div class="task__content ${this.noData}">${this.htmlName}</div><div class="task__actions"></div>` +
            `</span><span class="data ${this.type}"></span>${stateIndicator}` +
            `<a onclick=vfw.datasets.resultObjects['${this.orgID}'].removeData('${this.orgID}') ` +
            `class="w3-hover-white w3-right"><i class="fa fa-remove fa-fw"></i>` +
            `</a>` +
            `<a onclick=vfw.datasets.resultObjects['${this.orgID}'].showContextMenu('${this.orgID}') ` +
            `class="w3-hover-white w3-right"><i class="fa fa-caret-down fa-fw"></i>` +
            `</a><br></li>`;
    }

    /** Create a name for buttons according to the length of the name string */
    _createHtmlName() {
        const nameLength = 21;
        console.log('this.name: ', this.name)
        const vnLen = this.name.length;
        if (vnLen <= nameLength) this.htmlName = this.name
        else if (vnLen > nameLength) this.htmlName = this.name.substring(0, nameLength)
    }

    _placeHtmlButton() {
        document.getElementById(this.btnPosition).innerHTML += this._createHtmlButton();
    }

    _replaceHtmlButton() {
        let thisHtmlButton = document.getElementById(this.htmlElementID)
        $(thisHtmlButton).replaceWith(this._createHtmlButton());
    }

    async _requestData(url, data) {
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
        this.title = `${this.name}`;
    }

    // TODO: not used, keep to improve actually used update function
    async _update() {
        /** ensure datasets without type will not be loaded (because usually they have no actual data) **/
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

    // groupName = vfw.sidebar.set_group_btn_name(modal_input.outputName, 'resultBtn');
}

