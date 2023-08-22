/*
create new object with new vfw.datasets.DataObj(json)
*/
vfw.datasets.DataObj = class {
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
        this.url = window.location.pathname;

        Object.assign(this, {...defaultParams, ...data});
        this.storeKey = Array.isArray(this.inputs) && this.inputs.length ? "resultBtn" : "dataBtn";

        this.#setTitle();
        this.#createHtmlName();
        this.#setSource();
        if (this.group.trim().length !== 0) {
            this.isGroupMember = true;
            this.#buildHtmlGroup()
        }
        this.#placeHtmlButton();
        this.save(data);
        // this.workID = "";
        if (this.url !== `/home/`) this.#preloadData()
    }

    #preloadData() {
        // ensure datasets without type will not be loaded (because there usually have no actual data)
        if (!this.type) return
        let preloadData = {};
        if (this.source === 'db') {
            preloadData = {
                key_list: ['entry_id', 'uuid', 'start', 'end'],
                value_list: [this.orgID.toString(), this.uuID, this.start, this.end],
                dataset: this.orgID
            };
            $.ajax({
                url: vfw.var.DEMO_VAR + "/workspace/dbload",
                // dataType: 'json',
                "timeout": 5000,
                data: {
                    dbload: JSON.stringify(preloadData), 'csrfmiddlewaretoken': vfw.var.csrf_token,
                }, /** data sent with post request **/
            })
        }
    }

    #buildHtmlGroup() {
        let html = `<div class="grouppanel content">${this.group}</div>`
    }

    #placeHtmlButton() {
        document.getElementById('workspace').innerHTML += this.#buildHtmlButton();
    }

    #buildHtmlButton() {
        // set where to place the button
        let btnPosition = "";
        let dragHtml = "";
        if (this.storeKey == "dataBtn") {
            btnPosition = "sidebtn";
        }

        if (this.url == '/workspace/') {
            dragHtml = 'draggable="true" ondragstart="dragstart_handler(event)"'
        }
        let elementID = btnPosition + this.workID; // storeID;  // TODO: not sure what storeID should be or any other ID here...
        return `<li ` + dragHtml + ` class="w3-padding task" data-sessionstore=${this.storeKey} ` +
            `data-orgid="${this.orgID}"` +
            `data-id="${this.orgID}" btnName="${this.htmlName}" onmouseover="" ` +
            `data-btnName="${this.htmlName}" style="cursor:pointer;" id="${elementID}${this.orgID}">` +
            `<span class="w3-medium" title="${this.title}">` +
            `<div class="task__content ${this.noData}">${this.htmlName}</div><div class="task__actions"></div>` +
            `</span><span class="data ${this.type}"></span>` +
            `<a onclick=vfw.datasets.dataObjects['${this.orgID}'].removeData('${this.orgID}') ` +
            `class="w3-hover-white w3-right"><i class="fa fa-remove fa-fw"></i>` +
            `</a><br></li>`;
    }

    #setSource() {
        if (this.source) {
            if (this.source.substring(0, 2) === 'db') {
                this.source = 'db'
                // storageEntry.source = wpsDBInfo['id'].substring(0, 3)
                // storageEntry.dbID = wpsDBInfo['id'].substring(3,)
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

    save(data) {
        let stored;
        data['inSessionStorage'] = true;
        if (sessionStorage.getItem(this.storeKey)) {
            stored = JSON.parse(sessionStorage.getItem(this.storeKey));
        }
        console.log('stored: ', stored)
        if (sessionStorage.getItem(this.storeKey)) {
            stored = JSON.parse(sessionStorage.getItem(this.storeKey));
            if (!stored[this.orgID]) stored[this.orgID] = data;
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
        var newName = this.htmlName;
        if (sessionStorage.getItem(this.storeKey)) {
            let result_btns = JSON.parse(sessionStorage.getItem(this.storeKey));
            var i = 0;
            while (Object.keys(result_btns).includes(newName)) {
                newName = name + i++;
            }
        }
        this.htmlName = newName;
    }

    #updateDataButton(wpsDBInfo) {
        let workspaceData = JSON.parse(sessionStorage.getItem("dataBtn"));
        // let workspaceData = sessionStorageData
        let datasetKey = wpsDBInfo['orgid']
        let storageEntry = workspaceData[datasetKey]
        let btnName = createBtnName(storageEntry['name'], storageEntry['abbr'],
            storageEntry['unit'], wpsDBInfo['id'].substring(3,))
        let title = `${storageEntry['name']} (${storageEntry['abbr']} in ${storageEntry['unit']})`;
        let button = document.getElementById('sidebtn' + wpsDBInfo['orgid'])

        if (wpsDBInfo['id'].substring(0, 3) == 'wps') {
            storageEntry.source = wpsDBInfo['id'].substring(0, 3)
            storageEntry.dbID = wpsDBInfo['id'].substring(3,)
            storageEntry.inputs = wpsDBInfo['inputs']
        }
        workspaceData[datasetKey] = storageEntry
        sessionStorage.setItem("dataBtn", JSON.stringify(workspaceData));
        sessionStorageData = workspaceData
    }

    removeData(removeData) {  // TODO: removeData var should be taken from this!
        /** remove data from portal: **/
        document.getElementById("sidebtn" + removeData).remove();
        // removeData.remove();  // could be used when the element where send directly

        /** remove data from session: **/
        let workspaceData = JSON.parse(sessionStorage.getItem(this.storeKey));

        delete workspaceData[removeData];
        sessionStorage.setItem(this.storeKey, JSON.stringify(workspaceData))
        sessionStorageData = workspaceData  // is this already in use somewhere? Then add it also in Result Buttons
    }

}

