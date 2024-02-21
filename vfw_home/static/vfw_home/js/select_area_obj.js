/*
create new object with new vfw.datasets.DataObj(json)
*/
vfw.datasets.selectObj = class extends vfw.datasets.DataObj {

    constructor(data) {
        super(data);
        const defaultParams = {
            orgID: "",
            // source: "",
            abbr: "",
            name: "",
            unit: "",
            title: "",
            type: "polygon",   // datatype for combining datasets in workspace
            location: {},   // {type: string, coordinates: [lat, lon]
            source: "", //this.setSource(),
            sessionStorage: "",
        };
        this.htmlName = "";  // run createHtmlName to fill this
        this.title = "";
        this.url = window.location.pathname;

        Object.assign(this, {...defaultParams, ...data});

        this.storeKey = "dataBtn";
        this.btnPosition = "workspace";

    }

    htmlElementID() {
        return this.btnPosition + this.workID + this.orgID; // storeID;  // TODO: not sure what storeID should be or any other ID here...}
    }

    _buildHtmlGroup() {
        let html = `<div class="grouppanel content">${this.group}</div>`
    }

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
            `</span><span class="data ${this.type}"></span>` +
            `<a onclick=vfw.datasets.selectObjects['${this.orgID}'].removeData('${this.orgID}') ` +
            `class="w3-hover-white w3-right"><i class="fa fa-remove fa-fw"></i>` +
            `</a>` +
            `<a onclick=vfw.datasets.selectObjects['${this.orgID}'].showContextMenu('${this.orgID}') ` +
            `class="w3-hover-white w3-right"><i class="fa fa-caret-down fa-fw"></i>` +
            `</a><br></li>`;
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
    _createHtmlName() {
        this.htmlName = this.name;
        // this.htmlName = this.name + this.dbID;
    }

    removeData(removeData=this.orgID) {  // TODO: removeData var should be taken from this!
        /** remove data from portal: **/
        document.getElementById(this.htmlElementID()).remove();

        /** remove data from session: **/
        let workspaceData = JSON.parse(sessionStorage.getItem(this.storeKey));

        delete workspaceData[removeData];
        delete vfw.datasets.selectObjects[this.orgID];
        sessionStorage.setItem(this.storeKey, JSON.stringify(workspaceData))
        sessionStorageData = workspaceData  // is this already in use somewhere? Then add it also in Result Buttons
        vfw.map.func.resetDraw();
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

    _replaceHtmlButton() {
        let thisHtmlButton = document.getElementById(this.htmlElementID())
        $(thisHtmlButton).replaceWith(this._createHtmlButton());
    }

    update(data) {
        let properties = {};
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
}

