/*
 * Project Name: V-FOR-WaTer
 * Author: Marcus Strobl
 * Contributors: Safa Bouguezzi
 * License: MIT License
 */

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
    job_details = {};

    constructor(data) {
        const defaultParams = {
            // source: "",
            // type: "geometry",   // datatype for combining datasets in workspace
            source: "wps", //this.setSource(),
            storeKey: "resultBtn",
            btnPosition: "workspace_results",  // ID of html element to add the button
            btnPosition2: "new_result_store"
            }

        Object.assign(this, {...defaultParams, ...data});
        this._createHtmlName();
        this.htmlElementID = this.btnPosition + this.orgID;

        // this.storeKey = "resultBtn";
        // this.btnPosition = "workspace";

        this._setTitle();
        this._setSource();
        if (this.group.trim().length !== 0) {
            this.isGroupMember = true;
            this._buildHtmlGroup()
        }
        //this._placeHtmlButton();
        //this._placeNewResultStore();
        //console.log("Reached constructor")
        this.save();

        if (this.status == "accepted" || this.status == "running") {
            this.startPolling();
        }
    }

    startPolling(interval = 5000, maxAttempts = 25) {
        let attempts = 0;

        const startTime = new Date(); // Record the start time
        const durationElement = document.getElementById('job_duration'); // Get the duration element
    
        // Function to update the duration in the HTML
        const updateDuration = () => {
            const currentTime = new Date();
            const elapsedTime = Math.floor((currentTime - startTime) / 1000); // Calculate elapsed time in seconds
            const minutes = Math.floor(elapsedTime / 60);
            const seconds = elapsedTime % 60;
            durationElement.textContent = `${minutes}m ${seconds}s`; // Update the duration text
        };

        const durationInterval = setInterval(updateDuration, 1000);

        const poll = () => {
            if (attempts >= maxAttempts) {
                console.warn('Max polling attempts reached.');
                clearInterval(durationInterval); // Stop updating duration
                return;
            }

            attempts++;
            const url = `${vfw.var.DEMO_VAR}/workspace/jobstatus`;

            // Make a POST request using fetch
            fetch(url, {
                    method: 'POST', // Specify the HTTP method as POST
                    headers: {
                        'Content-Type': 'application/json', // Set the content type to JSON
                        'X-CSRFToken': vfw.var.csrf_token // Include CSRF token if required
                    },
                    body: JSON.stringify({ job_id: this.id }) // Send the job_id in the request body
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log(`Polling attempt ${attempts}:`, data);

                    if (data.status !== this.status) {
                        this.status = data.status;
    
                        // Update the result store in the HTML
                        //this._replaceHtmlButton();
                        //this._placeNewResultStore();
    
                        // Stop polling if the job is finished or failed
                        if (this.status === "successful" || this.status === "failed" || this.status === "dismissed") {
                            console.log(`Job ${this.id} completed with status: ${this.status}`);
                            this.job_details = data;
                            console.log(this.job_details)
                            //this.populateResultCard();
                            this._updateJobStatus(this.job_details);
                            clearInterval(durationInterval); // Stop updating duration
                            return;
                        }
                    }
    
                    // Continue polling if the job is not finished or failed
                    setTimeout(poll, interval);
                })
                .catch(error => {
                    console.error('Polling error:', error);
                    clearInterval(durationInterval); // Stop updating duration
                });
        }
        // Start the initial polling
        poll();
    }

    showDownloadModal() {
        const modal = document.getElementById("fileListModal");
        const fileList = document.getElementById("fileList");
        
        fileList.innerHTML = "";

        const files = this.job_details.results['plots'];
        const path = this.job_details.dir;

        files.forEach((filePath) => {
            const fullPath = `${path}/${filePath}`;
            const fileName = filePath.split('/').pop();
            const listItem = document.createElement("li");

            listItem.innerHTML = `
            <li class="flex items-center justify-between bg-gray-50 hover:bg-gray-100 px-5 py-4 rounded-xl transition">

            <div class="flex items-center gap-4">
                <i class="fa-solid fa-file text-blue-600 text-lg"></i>
                <span class="text-gray-800 font-medium text-lg">
                ${fileName}
                </span>
            </div>

            <button 
            onclick="openPdfFromBackend('${fullPath}')"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition flex items-center gap-2">
                <i class="fa-solid fa-download text-sm"></i>
                Download
            </button>

            </li>
            `;
            fileList.appendChild(listItem);
        });

        // Show the modal
        modal.classList.remove("hidden");
    }

    showPreviewModal() {
        document.getElementById("previewModal").classList.remove("hidden");
        let resultFiles = this.job_details.results['plots'];
        
        previewState.currentIndex = 0;
        previewState.files = resultFiles;
        previewState.dir = this.job_details.dir;
        vfw.workspace.modal.renderResult();

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


    downloadzip = function() {
        /** download results from server in one zip file **/

        const orgID = this.orgID;
        //const resultData = JSON.parse(sessionStorage.getItem("resultBtn"))[orgID].outputs.results[0].json;
        const resultData = this.job_details.results;
        const path = resultData.dir;
        const directoryName = path.split("/").pop();
        console.log("Directory-", path, resultData);

        $.ajax({
            url: "/workspace/resultdownload",
            type: 'GET',
            data: { zip: orgID, path: path },
            xhrFields: {
                responseType: 'blob'  // Important for handling binary data
            },
            success: function(blob) {
                const downloadUrl = window.URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = downloadUrl;
                a.download = directoryName + ".zip";
                document.body.appendChild(a);
                a.click();
                a.remove();
            },
            error: function(error) {
                console.error('Download failed:', error);
                alert('Failed to download the file. Please try again.');
            },
            complete: function() {
                console.log("Download attempt completed.");
            }
        });
    }


    /** remove data from webpage and from session, but user data is relaoded when user refreshes page **/
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

    /** remove data from webpage, session and DB. TODO: remove data from geoapi db and disk **/
    deleteFromDB() {
        $.ajax({
            url: vfw.var.DEMO_VAR + '/workspace/deleteresult',
            data: {'processid': this.id,
                'csrfmiddlewaretoken': vfw.var.csrf_token,
            }
        })
            .done(result => {
                console.log('+++ result: ', result)
                if ('done' in result) this.removeData(this.orgID)
                else if ('message' in result && result['message'] == 'delete') this.removeData(this.orgID)
            })
            .fail(error => {
                console.warn('failed to remove data from server: ', error)
                this.removeData(this.orgID);
        })
    }

    /**
     * Send request to django if there is an update on the process.
     * If yes, update object (with sessionstorage and html)
     */
    refresh(element) {  // TODO: removeData var should be taken from this!
        if (element !== null && typeof element === 'object' && !Array.isArray(element)) {
            element.classList.add('rotate');
        } else {
            vfw.html.loaderOverlayOn();
        }

        $.ajax({
            url: vfw.var.DEMO_VAR + '/workspace/processstate',
            data: {'processid': this.id,
                'csrfmiddlewaretoken': vfw.var.csrf_token,
            }
        })
            .done(result => {
                if (result.status !== this.status) {
                    this.status = result.status;
                    this.outputs.results = result.results;
                    this.update(result);
                } else if (result.hasOwnProperty('error')) {
                    this.status = "ERROR"
                    this.update(result);
                }
            })
            .fail(error => {
                // console.log('error: ', error)
                // console.log('result error: ', result)
                this.status = error.status;
                this.update(error);
                console.warn('failed getting data from server: ', error)
            })
            .always(bla => {
                if (element !== null && typeof element === 'object' && !Array.isArray(element)) {
                    element.classList.remove('rotate');
                } else {
                    vfw.html.loaderOverlayOff();
                }
            })

    }
    /**
     * Send request to django if there is an update on the process.
     * If yes, update object (with sessionstorage and html)
     */
    reopen() {
        const service = "pygeoapi_vforwater"  // TODO: Change this when we have more then 1 GeoAPI Server!!!
        vfw.workspace.modal.open_wpsprocess(service,
            this.title, [Object.keys(this.inputs), Object.values(this.inputs)]);
    }

    /** save info of object in session Storage
     * @param {Object} data - The data to be stored. Default is the whole object.
     * @param {boolean} update - Set if an object is updated (true) or a new was created (default=false).
     * **/
    save(data = this, update = false) {
        let stored;
        let newID = this.orgID
        data['inSessionStorage'] = true;
        /** Replace the entire object instead of appending 
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
        */
        let sessionEntry = {};
        sessionEntry[newID] = data;  // Create a new entry with only the current data
        sessionStorage.setItem(this.storeKey, JSON.stringify(sessionEntry));
        sessionStorageData = sessionEntry;  // Update the local variable
    }

    /**
     * Displays the results as a table in a modal dialog.
     *
     * @description This method loads the results and displays them as a table in a modal dialog.
     * First checks if the "resultModalObject" exists in the "vfw.var.obj", if not
     * creates a new instance of "vfw.html.resultModalObj" and assigns it to "vfw.var.obj.resultModalObject".
     * Then, it iterates over the resonclick="openPdfFromBackend('${fullPath}')"ults, appends them in the html variable, and adds it to the "resultModalObject".
     * 
     */

    
    showAsTable() {

        if (!Object.prototype.hasOwnProperty(vfw.var.obj, 'resultModalObject'))
            vfw.var.obj.resultModalObject = new vfw.html.resultModalObj();
    
        let html = "";
        const results = this.load().outputs.results;
    
        function backendFileUrl(p) {
            return "/workspace/resultdisplay?path=" + encodeURIComponent(p);
        }
    
        results.forEach(function (item) {
    
            const resultjson = item.json;
            const path = resultjson.dir;
            const plotFiles  = resultjson.plots || [];
            const imageFiles = resultjson.preview_images || [];
    
            // -------------------------
            // ALWAYS DEFINE itemHtml FIRST
            // -------------------------
            let itemHtml = item.html || "";   // <-- FIXES undefined.replace()
    
            // -------------------------
            // 1) Replace PDF <li> items
            // -------------------------
            plotFiles.forEach(function(filename) {
                if (!filename.endsWith(".pdf")) return;
    
                const fullPath = `${path}/${filename}`;
                const esc = filename.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    
                const liRegex = new RegExp(`<li\\s*>\\s*${esc}\\s*<\\/li>`, 'g');
    
                itemHtml = itemHtml.replace(
                    liRegex,
                    `
                    <li>
                        <a href="javascript:void(0)"
                           onclick="openPdfFromBackend('${fullPath}')"
                           style="display:flex;align-items:center;gap:8px;">
                           <i class="fa-solid fa-magnifying-glass" style="font-size:18px;"></i>
                           <span>Preview ${filename}</span>
                        </a>
                    </li>`
                );
            });
    
            // -------------------------
            // 2) Insert image gallery container
            // -------------------------
            itemHtml = itemHtml.replace(
                /<td[^>]*>\s*preview_images\s*<\/td>\s*<td[^>]*>/,
                `<td class="label-cell">preview_images</td>
                 <td class="image-cell">
                 <div class="image-gallery">`
            );
    
            // -------------------------
            // 3) Replace image <li> with image cards
            // -------------------------
            imageFiles.forEach(function(filename) {
                const full = `${path}/${filename}`;
                const fileUrl = backendFileUrl(full);
                const esc = filename.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    
                const liRegex = new RegExp(`<li\\s*>\\s*${esc}\\s*<\\/li>`, 'g');
    
                itemHtml = itemHtml.replace(
                    liRegex,
                    `
                    <div class="image-card" onclick="openPdfFromBackend('${full}')">
                        <img src="${fileUrl}" alt="${filename}">
                        <div class="image-title">${filename.replace('plots/', '')}</div>
                    </div>`
                );
            });
    
            // Close gallery container safely
            itemHtml = itemHtml.replace(
                /(image-gallery[^>]*>[\s\S]*?)<\/td>\s*<\/tr>/,
                "$1</div></td></tr>"
            );
    
            // -------------------------
            // 4) Enforce table + colgroup
            // -------------------------
            itemHtml = itemHtml.replace(
                /<table\b[^>]*>/,
                `<table class="styled-table">
                   <colgroup>
                     <col style="width:22%">
                     <col style="width:78%">
                   </colgroup>`
            );
    
            // -------------------------
            // 5) Scroll-wrap long cells
            // -------------------------
            itemHtml = itemHtml.replace(
                /<td>([\s\S]*?)<\/td>/g,
                function(match, content) {
    
                    if (content.includes("scroll-cell")) return match;
    
                    const textOnly = content.replace(/<[^>]*>/g, "").trim();
    
                    if (textOnly.length > 400) {
                        return `<td><div class="scroll-cell">${content}</div></td>`;
                    }
    
                    return match;
                }
            );
    

            // -------------------------
            html += itemHtml;
        });



        //        previewButtons += `
                 
        //            <a href="javascript:void(0)" onclick="openPdfFromBackend('${fullPath}')" style="display: flex; align-items: center; gap: 8px;">
        //              <i class="fa-solid fa-magnifying-glass" style="font-size: 18px;" title="Preview ${filename}"></i>
        //              <span>Preview ${filename}</span>
        //            </a>
                
        //        `;
        //      }
        //    });
           
         

        //    let item_2 = item.html.replace(
        //     /<li>\.\/(.*?)<\/li>/g,
        //     previewButtons
        //   );
          
        //   item_2 = item_2.replace(
        //     /<table\b[^>]*>/,
        //     '<table class="styled-table">'
        //   );
         
        //    html += item_2
        // });



        //console.log(html)
        vfw.var.obj.resultModalObject.addContent(html);
        //console.log(vfw.var.obj.resultModalObject);
        vfw.var.obj.resultModalObject.open()
          
    }

    /** Retrieves the value from the session storage as JSON, associated with the storekey.
     * @returns {string | null} The stored value, or null if no value is found.
     */
    load() {
        return JSON.parse(sessionStorage.getItem(this.storeKey))[this.orgID];
    }

    /** Several functions to fill and show a context menu
     * - actually its a more user friendly  dropdown instead of a context menu -
     * **/
    showContextMenu() {
        // TODO: used modal instead of context => rename and remove unnecessary code like action in createContextMenu
        let htmlElements = `<ul class="context-menu__items">${this._createContextMenu(this.orgID)}</ul>`
        //console.log('htmlElements: ', htmlElements)

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

    _buildHtmlGroup() {
        let html = `<div class="grouppanel content">${this.group}</div>`
    }

    /**
     * Create a context menu for the given dataset according to its datatype, processing state and if user is logged in.
     *
     * @param {string} orgID - The ID of the organization.
     * @return {string} - The HTML elements of the context menu.
     */
    _createContextMenu(orgID = this.orgID) {
        let htmlElements = "";
        let loggedInParams = [];

        // standard (default) parameters that are used in any case
        const defaultParams = [
            ["DeleteDataSet", "fa-eraser", gettext("Remove completely"), "deleteFromDB"],
            ["ReOpenProcess", "fa-window-maximize", gettext("Reopen Tool"), "reopen"]
        ]
        // little difference if user is logged in or not.
        if (vfw.var.USER_IS_AUTHENTICATED) {
            loggedInParams = [
                ["RemoveDataSet", "fa-trash", gettext("Remove in browser"), "removeData"],
            ].concat(defaultParams)
        } else {loggedInParams = [].concat(defaultParams)}

        // parameters specific for processing state
        const itemParams = {
            /** set parameters: action (still used?), iconClass, name in html, function to call */
            "FINISHED": [
                ["ShowResult", "fa-table", gettext("Show result as table"), "showAsTable"],
                ["DownloadJSON", "fa-download", gettext("Download result"), "download"],
                ["DownloadZIP", "fa-download", gettext("Download result (.zip)"), "downloadzip"],

            ].concat(loggedInParams),
            "ERROR": [  // TODO: How to delete from GeoAPI DB?
                // ["DeleteDataSet", "fa-eraser", gettext("Delete completely"), "deleteFromDB"]
            ].concat(loggedInParams),
            "CREATED": [  // only accessed if none of the others!
                ["RefreshDataSet", "fa-refresh", gettext("Refresh result"), "refresh"],
            ].concat(loggedInParams)
        }

    /** Build a html button for the context menu */
    function createMenuItem(action, iconClass, name, func) {
        htmlElements += `<li class="context-menu__item"> ` +
            `<a class="context-menu__link" data-action=${action} ` +
            `onclick=vfw.datasets.resultObjects['${orgID}'].${func}('${orgID}') > ` +
            `<i class="fa ${iconClass}"></i> ${name}</a>` +
            `</li>`
    }

    /**  */
    if (this.status === "FINISHED" || this.status === "ERROR") {
        itemParams[this.status].forEach((value) => createMenuItem(...value))
    } else {
        itemParams["CREATED"].forEach((value) => createMenuItem(...value))
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
            stateIndicator = `<a onclick=vfw.datasets.resultObjects[\'${this.orgID}\'].refresh(this) ` +
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

    _createNewResultStore() {
        // Create the first row with the object name and status
        const row1 = `
            <div class="flex justify-between items-center p-2 border-b border-gray-300">
                <span class="font-medium text-gray-800">${this.htmlName}</span>
                <span class="text-sm font-medium px-2 py-1 rounded ${
                    this.status === "successful" ? "bg-green-500 text-white" :
                    this.status === "accepted" || this.status === "running" ? "bg-yellow-500 text-white" :
                    "bg-red-500 text-white"
                }">
                    ${this.status}
                </span>
            </div>
        `;
    
        // Create the second row with the context menu options
        const contextMenuOptions = this._createContextMenu(this.orgID)
            .split("</li>")
            .filter(option => option.trim() !== "")
            .map(option => `<div class="p-2">${option}</div>`)
            .join("");
    
        const row2 = `
            <div class="flex flex-wrap gap-2 p-2">
                ${contextMenuOptions}
            </div>
        `;
    
        // Combine the rows into a single card
        return `
            <div class="bg-white shadow-md rounded mb-4 border border-gray-300">
                ${row1}
                ${row2}
            </div>
        `;
    }

    /** Create a name for buttons according to the length of the name string */
    _createHtmlName() {
        const nameLength = 21;
        //console.log('this.name: ', this.name)
        const vnLen = this.name.length;
        if (vnLen <= nameLength) this.htmlName = this.name
        else if (vnLen > nameLength) this.htmlName = this.name.substring(0, nameLength)
    }

    _placeHtmlButton() {
        document.getElementById(this.btnPosition).innerHTML += this._createHtmlButton();
    }

    _placeNewResultStore() {
        document.getElementById(this.btnPosition2).innerHTML = this._createNewResultStore();
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

    preview() {
        console.log('preview clicked');
    }

    populateResultCard() {
        if (this.status === "successful" || this.status === "failed") {
           document.getElementById('jobid').textContent = this.id;
           document.getElementById('start_time').textContent = '26.01.2026';
           document.getElementById('end_time').textContent = '26.01.2026 Later';
           document.getElementById('duration').textContent = '20s';

           document.getElementById('download_result').href = this.download();
           document.getElementById('download_zip_result').href = this.downloadzip();
           document.getElementById('show_as_table_result').href = this.showAsTable();
           document.getElementById('preview_result').href = this.preview();

        }

    }

    // Create function to set the values in the job card based on the job status
    _updateJobStatus(job_details) {
        if (job_details.status === "successful") {
            // Set the values for successful job
            document.getElementById('job_status_title').textContent = 'Successful';
            document.getElementById('job_status_desc').textContent = 'Job finished successfully';
            document.getElementById('job_status_icon').className = 'fa-solid fa-circle-check text-emerald-600';

            //Populate job details in the card
            document.getElementById('job_name').textContent = job_details.process_id;
            document.getElementById('job_id').textContent = job_details.identifier;
            document.getElementById('job_start_time').textContent = job_details.created;
            document.getElementById('job_end_time').textContent = job_details.finished;
            document.getElementById('job_duration').textContent = job_details.duration;

            let successBox = document.getElementById('success_box');
            let failureBox = document.getElementById('failure_box');

            successBox.classList.remove('hidden');
            successBox.classList.add('visible');
            
            failureBox.classList.remove('visible');
            failureBox.classList.add('hidden');

            const downloadZipElement = document.getElementById("download_zip_result");
            downloadZipElement.onclick = () => this.downloadzip();

            const downloadElement = document.getElementById("download_result");
            downloadElement.onclick = () => this.showDownloadModal();

            const previewElement = document.getElementById("preview_result");
            previewElement.onclick = () => this.showPreviewModal();
        }
        else if (job_details.status == "accepted") {
            document.getElementById('job_status_title').textContent = 'Running';
            document.getElementById('job_status_desc').textContent = 'Job accepted and running';
            document.getElementById('job_status_icon').className = 'fa-solid fa-clock text-yellow-600';

            //Populate job details in the card
            document.getElementById('job_name').textContent = job_details.process_id;
            document.getElementById('job_id').textContent = job_details.identifier;
            document.getElementById('job_start_time').textContent = job_details.created;
            document.getElementById('job_end_time').textContent = job_details.finished;

            let successBox = document.getElementById('success_box');
            let failureBox = document.getElementById('failure_box');

            successBox.classList.remove('visible');
            successBox.classList.add('hidden');
            
            failureBox.classList.remove('visible');
            failureBox.classList.add('hidden');
        }
        else if (job_details.status == "failed") {
            document.getElementById('job_status_title').textContent = 'Failed';
            document.getElementById('job_status_desc').textContent = 'Execution unsuccessful';
            document.getElementById('job_status_icon').className = 'fa-solid fa-clock text-red-600';

            let successBox = document.getElementById('success_box');
            let failureBox = document.getElementById('failure_box');
            
            successBox.classList.remove('visible');
            successBox.classList.add('hidden');
            
            failureBox.classList.remove('hidden');
            failureBox.classList.add('visible');

            failureBox.textContent = "Error Description:" + job_details.results["code"];  
                   
        }

    }

    // groupName = vfw.sidebar.set_group_btn_name(modal_input.outputName, 'resultBtn');
}

