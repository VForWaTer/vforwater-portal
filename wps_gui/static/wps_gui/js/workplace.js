/*
 * Project Name: V-FOR-WaTer
 * Author: Marcus Strobl
 * Contributors:
 * License: MIT License
 */

/**
 * Load metadata of a wps process.
 * The in- and outputs (and so on) of a tool are not loaded when page loads but on its first use.
 * Then stored in the sessionStorage for the next time the user wants to use this tool.
 *
 * @param {string} service - wps service as stored in database
 * @param {string} identifier - identifier of a wps process
 * @param {string, list} inputs - ugly hack - from result store comes key-value pair, from workspace comes only a btnName
 **/
vfw.workspace.modal.open_wpsprocess = function (service, identifier, inputs = null) {
    const modal_values = vfw.session.get_workflow();
    const json = vfw.session.get_wpsprocess(service, identifier);
    vfw.workspace.modal.build_modal(json, service)
    /** Fill the tool with selection made to receive this result button */
    if (typeof inputs === 'string') {
        vfw.workspace.modal.setProcessValues(modal_values[inputs]['input_keys'], modal_values[inputs]['input_values'])
    } else if (Array.isArray(inputs)) {
        vfw.workspace.modal.setProcessValues(inputs[0], inputs[1])
    }
}

/**
 * Set the head content of a modal in the workspace modal. Add Title and abstract form the tool.
 *
 * @param {object} wpsInfo - The content as JSON to set the head of the modal.
 * @param {string} service - Might be needed later for running the process.
 */
vfw.workspace.modal.setHead = function (wpsInfo, service) {
    let modHeadElement = document.getElementById("mod_head");
    modHeadElement.innerHTML = wpsInfo.title;
    modHeadElement.dataset.service = service;
    modHeadElement.dataset.process = wpsInfo.id;
    modHeadElement = document.getElementById("mod_abs");
    if (wpsInfo.description) {
        newElement = wpsInfo.description;
    }
    modHeadElement.innerHTML = newElement;
}

/**
 * Load metadata of a wps process if not available.
 * The in- and outputs (and so on) of a tool are used from the normal tool if available.
 * @param {string} origin - depending on the source the sources to fill the input fields are different
 * @param {string} service - wps service as stored in database
 * @param {string} identifier - identifier of a wps process
 **/
vfw.workspace.modal.openBatchprocess = function (origin='modal', wpsInfo={}, service="",
                                                  identifier="", inputs = null, boxId=[]) {
    if (wpsInfo === {}) wpsInfo = vfw.session.get_wpsprocess(service, identifier)

    let sessionStoreData = getStorageOrDict("dataBtn");
    let resultData = getStorageOrDict("resultBtn");
    let workflowData = getStorageOrDict("workflow");

    let newElement = "";
    let modInElement = document.getElementById("mod_in");
    let modOutElement = document.getElementById("mod_out");
    let modFootElement = document.getElementById("modal-footer");

    if (!sessionStoreData) sessionStoreData = {}
    if (!resultData) resultData = {}
    if (!workflowData) {
        workflowData = {}
    } else {
        workflowData = workflowData[boxId]
    }

    /** create the heading of the modal */
    vfw.workspace.modal.setHead(wpsInfo, service)
    Object.entries(wpsInfo.inputs).forEach(function (entry_value, index) {
        newNode = vfw.html.createBatchInputElement(entry_value, resultData, sessionStoreData);
        if (typeof (newNode) === 'object') modInElement.appendChild(newNode)
    });
}

vfw.html.createBatchInputElement = function (entry_value, resultData, sessionStoreData) {
    console.log('batch input')
    console.log('entry_value: ', entry_value)
    console.log('resultData: ', resultData)
    console.log('sessionStoreData: ', sessionStoreData)
}

/**
 * Modal to change data of a port.
 *
 * @param {string} service - wps service as stored in database
 * @param {string} identifier - identifier of a wps process
 * @param {string} boxidentifier - identifier of the box in session storage
 * @param {string} index - ugly hack - from result store comes key-value pair, from workspace comes only a btnName
 * @param {string} inputtype - type of data
 * @param {string} porttype - distinguish 'input' or 'output' port
 **/
vfw.workspace.modal.open_port = function (service, identifier, boxidentifier, index, inputtype, porttype) {

    let btnObj = {};
    let workflowBoxes = vfw.session.get_workflow();
    let process = vfw.session.get_wpsprocess(service, identifier);
    if (porttype === 'output') {
        console.warn('No action for output ports is implemented yet.');
        return;
    } else {
        let input_key, input_value = "nothing selected yet";
        let popUpText = '<thead><tr><th>&nbsp;</th></tr></thead>';

        input_key = workflowBoxes[boxidentifier]['input_keys'][index];
        if (workflowBoxes[boxidentifier]['input_values']) {
            input_value = workflowBoxes[boxidentifier]['input_values'][index];
        }
        popUpText += '<tr><td><b>' + input_key + ':</b></td><td>' + input_value + '</td></tr>';
        vfw.workspace.modal.openResultModal(popUpText)

        btnObj = [process['dataInputs'][index]['identifier'], process['dataInputs'][index]]
    }
}

/**
 * Actual function to load metadata of a wps process.
 *
 * @param {string} service - wps service as stored in database
 * @param {string} identifier - identifier of a wps process
 **/
vfw.session.load_wpsprocess = function (service, identifier) {
    let processdata = {};
    $.when(
        $.ajax({
            url: vfw.var.DEMO_VAR + "/workspace/processview",
            dataType: 'json',
            async: false,
            data: {
                processview: JSON.stringify({id: identifier, serv: service}),
                'csrfmiddlewaretoken': vfw.var.csrf_token,
            }, /** data sent with the post request **/
        })
    )
        .done(function (json) {
            processdata = json
        })
        .fail(function (e) {
            console.error('Failed: ', e)
        });
    return processdata
}

/**
 * Load metadata of a wps process.
 * in- and outputs and so on of a tool are not loaded when page loads but on its first use and stored in
 * the sessionStorage for the next time the user wants to use this tool
 * @param {string} service - wps service as stored in database
 * @param {string} identifier - identifier of a wps process
 * @return {obj} json - object of a wps process as saved in sessionStorage
 */
vfw.session.get_wpsprocess = function (service, identifier) {
    let tools = vfw.session.get_tools(service)
    let tool_data = {};
    if (tools[service][identifier]) {
        tool_data = tools[service][identifier]
    } else {
        vfw.html.loaderOverlayOn()
        $.when(vfw.session.load_wpsprocess(service, identifier))
            .done(
                function (json) {
                    tools[service][identifier] = json
                    sessionStorage.setItem('tools', JSON.stringify(tools))
                    tool_data = json;
                    vfw.html.loaderOverlayOff();
                })
    }
    return tool_data
}

/**
 * create a dict with random coordinates on the dropzone ('dropdiv').
 * @returns {{x: number, y: number}}
 */
vfw.workspace.get_drop_coords = function () {
    let dropzone = document.getElementById('dropdiv');
    let dropzone_coords = dropzone.getBoundingClientRect();
    let x_pad = 0;
    let y_pad = 0;
    let x, y
    if (dropzone_coords.height > 100) {
        x_pad = 300
    };
    if (dropzone_coords.width > 300) {
        y_pad = 200
    };
    x = Math.floor((Math.random() * (dropzone_coords.width - x_pad)) - x_pad + dropzone_coords.left);
    y = Math.floor((Math.random() * (dropzone_coords.height - y_pad)) + y_pad / 2 - dropzone_coords.top);
    return {'x': x, 'y': y}
}


/**
 * Collect data to drop element. (When 'Drop' in Modal is pressed)
 * Check if any inputs or outputs are selected and drop resprective elements, too.
 *
 * @param {object} ev - object passed with drop event
 **/
vfw.workspace.drop_on_click = function (ev) {
    /** Prepare and drop a tool button **/
    let data_id, tool_id, box_id, newbox, toolbox, databox, metadata, dataport, toolport, params, workflow;
    let coords = vfw.workspace.get_drop_coords();
    let modalData = vfw.workspace.modal.prepData();
    newbox = vfw.workspace.drop_handler(modalData, coords['x'], coords['y'], modalData.id, 'toolbar', modalData.serv)
    tool_id = newbox.boxID;
    toolbox = newbox.box;

    /** Check if tool is connected with other elements to drop and get ports **/
    for (let i in modalData.in_type_list) {
        if (vfw.var.DATATYPES.includes(modalData.in_type_list[i]) && modalData.inId_list[i]) {
            metadata = JSON.parse(sessionStorage.getItem("dataBtn"))[modalData.inId_list[i]]
            newbox = vfw.workspace.drop_handler(metadata, coords['x'] - 40, coords['y'] - 40, 'sidebtn' + modalData.inId_list[i], 'workspace')
            box_id = newbox.boxID;

            workflow = vfw.session.get_workflow()
            workflow[box_id].output_ids = [tool_id];
            workflow[tool_id].input_ids[i] = box_id;
            sessionStorage.setItem('workflow', JSON.stringify(workflow))

            databox = newbox.box;
            dataport = databox.getOutputPort(0);
            toolport = toolbox.getInputPort(parseInt(i));
        }
    }
    vfw.session.draw2d.setdata();
}

/**
 * Check if an input (an Element of a wps) is required and if it is required check if the input has a value.
 *
 * @param {HTMLElement} checkElement Element to be checked if filled.
 */
vfw.workspace.is_required = function (checkElement) {
    var passed = true;
    let requiredList = checkElement.querySelectorAll("[required]");
    let loopLength = requiredList.length;
    let radioName = "";
    let checkedRadioName = "";
    for (let i = 0; i < loopLength; i++) {
        if (requiredList[i].type === 'radio') {
            radioName = requiredList[i].name;
            if (checkedRadioName !== radioName) {
                if ($('input[name=' + radioName + ']:checked').length > 0) {
                    checkedRadioName = radioName;
                } else {
                    alert("Please fill all required fields that are marked with (*).");
                    passed = false;
                    break
                }
            }
        } else {
            if (!requiredList[i].value) {
                alert("Please fill all required fields that are marked with (*).");
                passed = false;
                break
            }
        }
    }
    return passed;
}

/**
 * Check if an input has a regex pattern and if input is correct.
 *
 * @param {HTMLElement} checkElement Element to be checked if filled.
 */
vfw.workspace.checkPattern = function (checkElement) {
    const inModal = document.getElementById('mod_in');
    const dropDInputs = inModal.getElementsByTagName('select');
    let dDInput, stored;
    /** first loop over each dropdown in input, then over values in dropdown (if something is selected) **/
    for (let i = 0; i < dropDInputs.length; i++) {
        dDInput = dropDInputs[i].selectedOptions;
        if (dDInput.length > 0) {
            stored = JSON.parse(sessionStorage.getItem("dataBtn"))[dDInput[0].value];
            if (stored.type == "geometry") {
                let geoJsonFormat = new ol.format.GeoJSON();
                let geoJsonPolygon = geoJsonFormat.writeGeometry(new ol.geom.Polygon(stored['geom']))
                if (!vfw.util.isValidGeoJson(JSON.parse(geoJsonPolygon))) {
                    console.warn("Not a valid GeoJSON")
                    return false
                } else if (!vfw.util.isValidPolygon(JSON.parse(geoJsonPolygon))) {
                    console.warn("Not a valid Polygon")
                    return false
                }
            }
        }
    }
    return true
}

/**
 * Collect data from modal neeeded to run a process.
 * @returns {{in_type_list: *[], serv: string, outputName: string, key_list: *[], inId_list: *[], id: string, value_list: *[]}}
 */
vfw.workspace.modal.prepData = function () {
    /** collect inputs **/
    const inModal = document.getElementById('mod_in');
    const dropDInputs = inModal.getElementsByTagName('select');
    const inputInputs = inModal.getElementsByTagName('input');
    var inKey = [];
    var inValue = [];
    let indict = {};  // pywps needed a set. For geoapi processes we can use a dict. TODO: delete set if not needed.
    var inType = [];
    var inId = [];
    let dDInput = 0;
    let valueList = [];
    let typeList = [];
    let inIdList = [];
    let stored;

    /** first loop over each dropdown in input, then over values in dropdown **/
    for (let i = 0; i < dropDInputs.length; i++) {
        dDInput = dropDInputs[i].selectedOptions;
        valueList = [];
        typeList = [];
        inIdList = [];

        /** if many inputs in dropdown **/
        if (dDInput.length > 1) {
            for (let j = 0; j < dDInput.length; j++) {
                stored = JSON.parse(sessionStorage.getItem("dataBtn"))[dDInput[j].value]
                valueList.push(parseInt(stored['dbID']))
                typeList.push(stored['type']);
                inIdList.push(dDInput[j].value);
            }
            inValue.push(valueList);
            inKey.push(dropDInputs[i].name);
            inType.push(typeList);
            inId.push(inIdList);
            indict[dropDInputs[i].name] = valueList;

        /** else if one input element in dropdown **/
        } else if (dDInput.length == 1) {
            if (dDInput[0].value.split(",").length == 1) {
                stored = JSON.parse(sessionStorage.getItem("dataBtn"))[dDInput[0].value]
                if (stored.type !== "geometry") {
                    let intValue = dropDInputs[i].multiple ? [parseInt(stored['dbID'])] : parseInt(stored['dbID']);
                    inValue.push(intValue);
                } else {
                    let polygon = new ol.geom.Polygon(stored['geom']);
                    let geoJsonFormat = new ol.format.GeoJSON();
                    const geoJsonPolygon = {
                        "type": "Feature",
                        "geometry":geoJsonFormat.writeGeometry(polygon),
                        "properties": {"name":stored['name'],"orgID":stored['orgID']}
                    };
                    inValue.push(geoJsonPolygon);
                }
                inType.push(stored['type']);
                indict[dropDInputs[i].name] = stored['source'] + stored['dbID'];
            } else {
                let groupInValues = [];
                let groupInTypes = [];
                // Try to get wps ID for data
                for (let dataset of dDInput[0].value.split(",")) {
                    stored = JSON.parse(sessionStorage.getItem("dataBtn"))[dataset]
                    groupInValues.push(parseInt(stored['dbID']))
                    groupInTypes.push(stored['type']);
                }
                inValue.push(groupInValues)
                inType.push(groupInTypes);
                indict[dropDInputs[i].name] = dDInput[0].value.split(",");
            }
            inKey.push(dropDInputs[i].name);
            inId.push(dDInput[0].value);
        }
    }

    /** now check the other elements like radio buttons or checkboxes **/
    for (let i = 0; i < inputInputs.length; i++) {
        if (inputInputs[i].type == "radio") {
            if (inputInputs[i].checked == true) {
                inKey.push(inputInputs[i].name);
                inValue.push(inputInputs[i].value);
                inType.push('string');
                inId.push('');
                indict[inputInputs[i].name] = inputInputs[i].value;
            }
        } else if (inputInputs[i].type == "checkbox") {
            inKey.push(inputInputs[i].name);
            if (inputInputs[i].checked == true) {
                inValue.push(true);
                inType.push('boolean');
                inId.push('');
                indict[inputInputs[i].name] = true;
            } else {
                inValue.push(false);
                inType.push('boolean');
                inId.push('');
                indict[inputInputs[i].name] = false;
            }
        } else if (inputInputs[i].type == "datetime-local") {
            const datetime = dayjs.tz(inputInputs[i].value, 'Europe/Berlin');
            inKey.push(inputInputs[i].name);
            inValue.push(datetime.format());
            inType.push('');
            inId.push('');
            indict[inputInputs[i].name] = datetime.format();
        } else {
            inKey.push(inputInputs[i].name);
            inValue.push(inputInputs[i].value);
            inType.push('');
            inId.push('');
            indict[inputInputs[i].name] = inputInputs[i].value;
        }
    }

    /** collect outputs **/
    let outModal = document.getElementById('mod_out');
    let outputs = outModal.getElementsByTagName('input');
    let outDict = {};
    for (let i = 0; i < outputs.length; i++) {
        if (outputs[i].type == "radio") {
            if (outputs[i].checked == true) {
                outDict[outputs[i].name] = outputs[i].value;
            }
        } else {
            outDict[outputs[i].name] = outputs[i].value;
        }
    }

    /** find respective process **/
    let modhead = document.getElementById('mod_head');
    let wpsservice = modhead.dataset.service;
    let identifier = modhead.dataset.process;

    let outputName;
    if (outputs[0].value === "") {
        outputName = identifier + "_";
    } else {
        outputName = outputs[0].value;
    }
    return {
        'id': identifier, 'serv': wpsservice, 'key_list': inKey, 'value_list': inValue,
        'in_type_list': inType, 'outputName': outputName, 'inId_list': inId, 'in_dict': indict,
    }
}

vfw.workspace.modal.runProcess = function () {
    vfw.workspace.modal.setColor("dodgerblue");
    let modal_input = vfw.workspace.modal.prepData();
    let directshowdatatypes = ['figure', 'string', 'html', 'integer', 'float']
    let group = false;
    let groupName = ''
    let i = 0;
    let members = [];
    vfw.html.loaderOverlayOn();

    $.ajax({
        url: vfw.var.DEMO_VAR + "/workspace/processrun",
        type: 'POST',
        data: {
            processrun: JSON.stringify(modal_input),
            'csrfmiddlewaretoken': vfw.var.csrf_token,
        }, /** data sent with post request **/
    })
        .done(function (json) {  /** Results are stored in the sessionStorage **/
            vfw.html.loaderOverlayOff()
            /** Handle result according to the success/status of the process */
            if (json.execution_status == 200 || json.execution_status == "ProcessSucceeded") {
                let btnName = '';
                let btnData = {};
                json.wps = modal_input.id;
                json.inputs = {};
                $.each(modal_input.inKey, function (key, value) {
                    json.inputs[value] = modal_input.inValue[i];
                    i++;
                });
                vfw.workspace.modal.setColor("forestgreen");

                // if there is an html available for a result show it directly as result
                if ('report_html' in json) {
                    btnData['report_html'] = json.report_html;
                    vfw.workspace.modal.openResultModal(json.report_html)
                }

                // if there are more then one result, than create a grouped button
                if (Object.keys(json.result).length > 1) {
                    group = true;
                    groupName = vfw.sidebar.set_group_btn_name(modal_input.outputName, 'resultBtn');
                }

                for (let i in json.result) {
                    btnName = vfw.sidebar.set_result_btn_name(modal_input.outputName);
                    json.result[i].dropBtn['name'] = btnName;
                    btnData = {
                        dbID: json.result[i].wpsID,
                        inputs: json.inputs,
                        input_keys: modal_input.key_list,
                        input_values: modal_input.value_list,
                        name: btnName,
                        type: json.result[i].type,
                        outputs: json.result[i].data,
                        wps: json.wps,
                        source: "wps",
                        status: json.execution_status,
                        dropBtn: json.result[i].dropBtn,
                        group: groupName
                    }
                    vfw.session.add_resultbtn(btnName, btnData);
                    if (directshowdatatypes.includes(btnData.type)) {
                        vfw.workspace.modal.add_resultbtn(btnData)
                        vfw.workspace.view_result(btnData)
                    }

                    if (group === false) {
                        document.getElementById("workspace_results").innerHTML
                            += vfw.workspace.buildResultStoreButton(btnName, btnData);
                    } else {
                        members.push([btnName, btnData])
                    }
                }

                if (group === true) {
                    document.getElementById("workspace_results").innerHTML
                        += vfw.workspace.buildResultGroupButton(groupName, members);
                    vfw.sidebar.addGroupaccordionToggle()
                }
            }
            else if (json.status == 'ERROR') {
                console.error('error in wps process')
                vfw.workspace.modal.setColor("firebrick");
            }
            else if (json.status == 'CREATED' || json.status == 'ACCEPTED') {
                vfw.workspace.modal.setColor("orange");
                if (!json['orgID']) {
                    // create an id for the new object
                    const urlParts = json.outputs.path.split("/");
                    json['orgID'] = json.name + '_' + urlParts[urlParts.length -1];
                }

                // create object
                vfw.datasets.resultObjects[json['orgID']] = new vfw.datasets.resultObj(json);

            }
            else if (json.status == 'FINISHED') {
                alert('Finished neeeds implementation (Short running porcess)')
                vfw.workspace.modal.setColor("green");
            }
            else if (json.execution_status == "error in wps process") {
                vfw.workspace.modal.setColor("firebrick");
                console.error('Error in wps process: ', json.error)
                // alert('Error: Failed to execute your request.');
            }
            else if (json.execution_status == "auth_error") {
                vfw.workspace.modal.setColor("firebrick");
                /** Use Timeout to ensure color changed before popup appears **/
                setTimeout(function () {
                    alert('Error: You are not allowed to run this process. Please Contact your Admin.');
                }, 5);
                console.error('Maybe you have to log in to run processes. ', json.execution_status)
            }
        })
        .fail(function (json) {
            vfw.html.loaderOverlayOff()
            vfw.workspace.modal.setColor("firebrick");
            console.error('Error, No success: ', json)
        })
        // .always(vfw.html.loaderOverlayOff());
}

/**
 * View result directly on top of tool window
 * @param json
 */
vfw.workspace.view_result = function (json) {
    if (json.type == 'figure' || json.type == 'string' || json.type == 'integer') {
        document.getElementById("mod_result").innerHTML = json.outputs; // add plot
    }
    vfw.html.resultModal.style.display = "block";
    vfw.html.popup.classList.remove(popActive);
    modalToggleSize.style.display = "none";
}


// Not used yet
function run_wps(input_dict) {
    let modhead = document.getElementById('mod_head');
    let wpsservice = modhead.dataset.service;
    let identifier = modhead.dataset.process;
    $.ajax({
        url: vfw.var.DEMO_VAR + "/workspace/processrun",
        data: {
            processrun: JSON.stringify({
                id: identifier, serv: wpsservice,
                key_list: input_dict.keys(), value_list: input_dict.values()
            }),
            'csrfmiddlewaretoken': vfw.var.csrf_token,
        }, /** data sent with the post request **/
    })
        .done(function (json) {
            return json
        })
        .fail(function (json) {
            console.error('Error, No success: ', json)
            vfw.workspace.modal.setColor("firebrick");
        })
}


/**
 * Check if result data in sessionStorage exists, if yes check if name already exists, if yes add numger to name.
 *
 * @param {string} name
 */
vfw.sidebar.set_result_btn_name = function (name) {
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

/**
 * Check if result data in sessionStorage exists, if yes check if name already exists, if yes add numger to name.
 *
 * @param {string} name
 * @param {string} storage
 */
vfw.sidebar.set_group_btn_name = function (name, storage) {
    let groupSet = new Set();
    let groupName = name + "__group";
    /** check if Storage exists. If yes get it **/
    if (sessionStorage.getItem(storage)) {
        let btns = JSON.parse(sessionStorage.getItem(storage));
        for (let i in btns) {
            if (btns[i].group.includes(name)) {
                groupSet.add(btns[i].group)
            }
        }
        if (groupSet.size > 0) {
            groupName = name + "__group" + groupSet.size
        }
    }
    return groupName
}

/**
 * Set color of header and footer of wps tool modal.
 * On change of color also remove 'view result' button.
 *
 * @param {string} color
 */
vfw.workspace.modal.setColor = function (color) {
    let modalColor = document.getElementById("modal-header");
    modalColor.style.backgroundColor = color;
    modalColor = document.getElementById("modal-footer");
    modalColor.style.backgroundColor = color;
    document.getElementsByClassName("work_modal-output")[0].style.display = "none";
}

/**
 *  A Object with names and values from the input object / not used yet
 *  */
vfw.workspace.modalObj = function (processId, processInput, processOutput) {
    this.processId = processId;
    this.processInput = processInput;
    this.processOutput = processOutput;
}


/**
 * Show hidden button in modal to enable quick preview of results.
 *
 * @param {{outputs, inputs: (*|{}), dbID: *, name: (*|string), dropBtn, wps: string, source: string, type, status: *, group: string}} json
 */
vfw.workspace.modal.add_resultbtn = function (json) {
    let wspan_out = document.getElementsByClassName("work_modal-output")[0];
    wspan_out.style.display = "block";
    wspan_out.onclick = () => {
        vfw.workspace.view_result(json)
    };
}

function set_preview_content(json) {

}

/**
 * Add information of a result for a result button to the sessionStorage.
 *
 * @param {string} btnName - name for button
 * @param {object} json - content stored for button
 */
vfw.session.add_resultbtn = function (btnName, json) {
    let result_btns = {};
    if (sessionStorage.getItem("resultBtn")) {
        result_btns = JSON.parse(sessionStorage.getItem("resultBtn"));
        if (Object.keys(result_btns).includes(btnName)) {
            console.error('Error! Names should be unique! Problem with race conditions?')
        }
    }
    result_btns[btnName] = json
    sessionStorage.setItem("resultBtn", JSON.stringify(result_btns));
}

/**
 * Build a button in the result store.
 * data-id is used to find results on server, id is used for the remove button
 *
 * @param  {string} name - name for the button
 * @param  {obj} json - Object holding all necessary info about result
 * @return {string} - HTML Code for the button
 **/
vfw.workspace.buildResultStoreButton = function (name, json) {
    let title = json.wps + "\n" + JSON.stringify(json.inputs).slice(1, -1).replace(/"/g, "'");
    return '<li draggable="true" ondragstart="dragstart_handler(event)" ' +
        'class="w3-padding task is-result" data-sessionStore="resultBtn" ' +
        'data-id="' + json.source + json.dbID + '" btnName="' + name + '" onmouseover="" style="cursor:pointer;" ' +
        'data-btnName="' + name + '" id="' + name + '">' +
        '<span class="w3-medium" title="' + title + '">' +
        '<div class="task__content">' + name + '</div><div class="task__actions"></div>' +
        '</span><span class="' + json['type'] + '"></span>' +
        '<a href="javascript:void(0)" onclick="vfw.session.removeSingleResult(\'' + name + '\')" class="w3-hover-white">' +
        '<i class="fa fa-remove fa-fw"></i></a><br></li>';
}

/**
 * Build a button in the result store. Base button for a group of results
 * data-id is used to find results on server,  id is used for the remove button
 *
 * @param  {string} name name for the group button
 * @return {string} HTML Code for the group button
 **/
vfw.workspace.buildResultGroupButton = function (groupname, members) {
    let mhtml = ''
    let ghtml = '<li draggable="true" ondragstart="dragstart_handler(event)" ' +
        'class="w3-padding task is-result-group groupaccordion" data-sessionStore="resultBtn"' +
        '" btnName="' + groupname + '" onmouseover="" style="cursor:pointer;" ' +
        'data-btnName="' + groupname + '" id="' + groupname + '"><span class="w3-medium">' +
        '<div class="task__content">' + groupname + '</div><div class="task__actions"></div></span>' +
        '<span class=""></span>' +
        '<a href="javascript:void(0)" onclick="vfw.session.removeGroupResult(\'' + groupname + '\')" class="w3-hover-white">' +
        '<i class="fa fa-remove fa-fw"></i></a><br></li>';

    members.forEach(function (singlemember) {
        mhtml += vfw.workspace.buildResultStoreButton(singlemember[0], singlemember[1]);
    })
    ghtml += '<div class="grouppanel">' + mhtml + '</div>'
    return ghtml
}

/** Remove element from html and update session Storage */
vfw.session.removeSingleResult = function (removeData) {
    document.getElementById(removeData).remove();
    let workspaceData = JSON.parse(sessionStorage.getItem("resultBtn"));
    delete workspaceData[removeData];
    sessionStorage.setItem("resultBtn", JSON.stringify(workspaceData))
}

vfw.session.removeGroupResult = function (removeData) {
    let workspaceData = JSON.parse(sessionStorage.getItem("resultBtn"));
    $.each(workspaceData, function (i) {
        if (workspaceData[i].group === removeData) {
            vfw.session.removeSingleResult(i)
        }
    })
    document.getElementById(removeData).remove();
}

/** Loop over all datasets of the element to select from and remove each individually */
vfw.session.removeAllResults = function () {
    let groupSet = new Set();
    /** remove button from portal **/
    $.each(JSON.parse(sessionStorage.getItem("resultBtn")), function (key, value) {
        groupSet.add(value.group)
        const delete_id = 'htmlElementID' in value ? value['htmlElementID'] : key;
        vfw.session.removeSingleResult(delete_id);
    });

    /** remove result data from session **/
    sessionStorage.removeItem("resultBtn");

    /** remove group buttons from portal **/
    if (groupSet[0] !== undefined) {
        groupSet.forEach(function (i) {
            document.getElementById(i).remove();
        })
    }
}

/**
 * @param {json} item - input information loaded from Session Storage
 * @param {string} entry_name - Name for the element (important! That name is also send to server!)
 * @param {string} newNode - The new HTML Element where the checkbox will be added
 */
vfw.workspace.modal.build_regexText = function (item, entry_name, newNode) {
    inElement = document.createElement("INPUT");
    inElement.id = 'mod_in_el_' + item.title;  // item.identifier;
    inElement.name = entry_name;  // item.identifier;
    inElement.setAttribute("pattern", item.keywords[1]);
    inElement.type = "text";
    if ('defaultValue' in item) {
        inElement.value = item.defaultValue;
    }
    if ('description' in item) {
        inElement.title = item.description;
    }
    newNode.appendChild(inElement);
}

/**
 * @param {json} item - input information loaded from Session Storage
 * @param {string} entry_name - Name for the element (important! That name is also send to server!)
 * @param {string} newNode - The new HTML Element where the checkbox will be added
 * @param {string} option - String with predefined value from wps process
 */
vfw.workspace.modal.build_radio = function (item, entry_name, newNode, option) {
    let nodeText = document.createTextNode(" " + option + " ");
    let inElement = document.createElement("INPUT");
    inElement.type = "radio";
    inElement.value = option;
    inElement.id = 'mod_in_el_' + item.title;  // item.identifier;
    if (item.minOccurs === 1) inElement.required = true;

    inElement.name = entry_name;  // item.identifier;
    if ("default" in item.schema) if (item.schema.default == option) inElement.checked = true;  // TODO!

    newNode.appendChild(inElement);
    newNode.appendChild(nodeText);
}

/**
 * @param {json} item - input information loaded from Session Storage
 * @param {string} entry_name - Name for the element (important! That name is also send to server!)
 * @param {HTMLElement} newNode - The new HTML Element where the checkbox will be added
 * @param {string} option - String with predefined value from wps process
 */
vfw.workspace.modal.build_checkbox = function (item, entry_name, newNode, option) {
    let nodeText = document.createTextNode(" " + option + " ");
    let inElement = document.createElement("input");
    inElement.type = "radio";
    inElement.value = option;
    inElement.id = item.identifier;
    if (item.minOccurs === 1) inElement.required = true;

    inElement.name = entry_name;
    if ("default" in item.schema) {
        if (item.schema.default == option) inElement.checked = true;  // TODO!
    }
    newNode.appendChild(inElement);
    newNode.appendChild(nodeText);
}


/**
 * Function is called when the input should be a dataset and builds a dropdown menu for the workspace modal.
 *
 * @param {json} item - description of wps input.
 * @param {HTMLParagraphElement} newNode
 * @param {number} countDropDowns - count all dropdowns in tool for naming and accessing the different menues
 */
vfw.workspace.modal.build_dropdown = function (item, newNode, countDropDowns) {

    const sessionStoreData = JSON.parse(sessionStorage.getItem("dataBtn"));
    const resultData = JSON.parse(sessionStorage.getItem("resultBtn"));
    const groupedData = JSON.parse(sessionStorage.getItem("dataGroup"));
    let htmlSelect = document.createElement("SELECT");
    let boxLen = 0;
    let aptStoreData = {};
    let aptResultData = {};
    let aptGroupedData = {};
    let acceptedDataTypes = DATATYPE.accepts([item.dataType])

    // htmlSelect.id = item.identifier;
    htmlSelect.id = 'mod_in_el_' + item.identifier;  // item.id

    for (let i in sessionStoreData) {
        if (acceptedDataTypes.has(sessionStoreData[i].type)) {
            aptStoreData[i] = sessionStoreData[i];
        }
        if (sessionStoreData[i].hasOwnProperty('group')) {
            // aptGroupedData[i] = sessionStoreData[i];
        } else {
            // aptStoreData[i] = sessionStoreData[i];
        }
    }
    for (let i in resultData) if (acceptedDataTypes.has(resultData[i].type)) aptResultData[i] = resultData[i]
    for (let i in groupedData) {
        if (acceptedDataTypes.has(groupedData[i].type)) {
            // aptGroupedData[i] = groupedData[i]
        }
        // aptGroupedData[i] = groupedData[i]
    }
    boxLen = Object.keys(aptResultData).length + Object.keys(aptStoreData).length + Object.keys(aptGroupedData).length;
    // if (item.minOccurs === 1) htmlSelect.required = true; // Why did I first use === 1 ???
    if (item.minOccurs >= 1) htmlSelect.required = true;

    /** check if input data is available; only build dropdown if there is data to select from (boxlen > 0) **/
    if (boxLen == 0) {
        htmlSelect = document.createElement("DIV");
        if (item.defaultValue) {
            htmlSelect.innerText = 'Without selected datasets the default ' + item.defaultValue + ' value is used.'
        } else {
            htmlSelect.innerText = 'No suitable dataset found.\nPlease first process or select a dataset from the filter menu.'
        }
    } else {
        htmlSelect.size = (boxLen > 3) ? "5" : (boxLen + 2).toString();
        htmlSelect.name = item.identifier;
        if (aptGroupedData !== null && Object.keys(aptGroupedData).length) {
            let optionGroup = document.createElement("OPTGROUP");
            optionGroup.label = "Data groups";
            optionGroup = vfw.workspace.modal.build_dropdown_opt(item, optionGroup, aptGroupedData);
            htmlSelect.appendChild(optionGroup);
        }
        if (aptStoreData !== null && Object.keys(aptStoreData).length) {
            let optionGroup = document.createElement("OPTGROUP");
            optionGroup.label = "Data store";
            optionGroup = vfw.workspace.modal.build_dropdown_opt(item, optionGroup, aptStoreData);
            htmlSelect.appendChild(optionGroup);
        }
        if (resultData !== null) {
            let optionGroup = document.createElement("OPTGROUP");
            optionGroup.label = "Result store";
            optionGroup = vfw.workspace.modal.build_dropdown_opt(item, optionGroup, aptResultData);
            htmlSelect.appendChild(optionGroup);
        }
        if (!item.maxOccurs == 1 || item.minOccurs > 1) {
            htmlSelect.multiple = true;
        }
        /** If more then one option is needed to select, show a second box with selection **/
    }
    newNode.appendChild(htmlSelect);
    return countDropDowns;
}

/**
 * Collect elements for a dropdown HTMLElement.
 *
 * @param {Object} processAttribute - Data description from the wps process.
 * @param {HTMLElement} optionGroup - HTML group Element. Different groups to seperate Data and Results in dropdown
 * @param {Object} selectables - The relevant elements from the sessionStorage
 */
vfw.workspace.modal.build_dropdown_opt = function (processAttribute, optionGroup, selectables) {
    // let opt = document.createElement("OPTION");
    let opt;
    let optGroupDict = {};
    let groupName = '';
    const groups = new Set([]);

    /**
     * Add a value to a the button or update the value for a group button
     * @param {Object} selectables
     * @param {number} singleData
     */
    function chooseDataID (selectables, singleData) {
        let value
        if (selectables[singleData].wpsID) {
            value = 'wpsID' + (selectables[singleData].wpsID);
        } else {
            value = singleData;
        }
        return value;
    }

    Object.keys(selectables).forEach(function (singleData) {
        opt = document.createElement("OPTION");
        groupName = ''

        /** Check if a Button for a group, or a single button is needed */
        if (selectables[singleData].abbr && selectables[singleData].unit)
            {  // but has unit and abbriviation
            opt.innerText = `${singleData} ${selectables[singleData].name} (${selectables[singleData].abbr}
            in ${selectables[singleData].unit})`;  // create String
            opt.value = chooseDataID(selectables, singleData);
        } else if (selectables[singleData].hasOwnProperty('group') &&  // is group
            !groups.has(selectables[singleData]['group'])) {  // but seen the first time

            groupName = selectables[singleData]['group']
            // Here the group element is build
            groups.add(groupName)
            opt.innerText = `${groupName}`;
            optGroupDict[groupName] = {'opt': {}};
            optGroupDict[groupName]['opt'] = opt;
            optGroupDict[groupName]['value'] = [chooseDataID(selectables, singleData)];
            return
        } else if (!groups.has(selectables[singleData]['group'])) {  // is no group

            opt.innerText = `${selectables[singleData]['name']}`;
            opt.value = chooseDataID(selectables, singleData);
            opt.name = selectables[singleData]['name']
        } else if (selectables[singleData].hasOwnProperty('group') &&  // is group,
            groups.has(selectables[singleData]['group'])) {  // but seen before, so add more values to an existing button

            optGroupDict[selectables[singleData]['group']]['value'].push(chooseDataID(selectables, singleData))
            return
        } else {
            console.warn('New case. Fix this')
            return;
        }

        if ('keywords' in processAttribute && processAttribute.keywords.length == 1) opt.selected = true;
        optionGroup.appendChild(opt);
    })
    Object.keys(optGroupDict).forEach(function (group) {
        optGroupDict[group]['opt'].value = optGroupDict[group]['value'];
        optionGroup.appendChild(optGroupDict[group]['opt']);
    })
    return optionGroup
}

/** Create an input element according to the expected type of the inputdata */
vfw.html.createInputElement = function (input_tool_description, resultData, sessionStoreData) {
    let inElement = "", newNode = "", nodeText = "";
    let item = input_tool_description[1];
    let entry_name = input_tool_description[0];
    let countDropDowns = 0;
    newNode = document.createElement("p");

    /** Set title of Input and set the 'required' flag if necessary **/
    let titleText = "";
    if (item.minOccurs == 0) {
        titleText = " " + item.title + ": "
    } else if (item.defaultValue) {
        titleText = " " + item.title + ": "
    } else if (item.required === true) {
        // } else if (item.minOccurs > 0 && item.dataType != 'boolean') {
        titleText = " " + item.title + " (*) : ";
        inElement.required = true;
    } else {
        titleText = " " + item.title + ": "
    }

    /** check attributes/'keywords' from the process that are used to define which input element is used */
    nodeText = document.createTextNode(titleText);
    newNode.appendChild(nodeText);
    if ('allowedValues' in item && Array.isArray(item.allowedValues) && item.allowedValues.length > 1) {
        if ('maxOccurs' in item) {
            if (item.maxOccurs === 1) {
                item.allowedValues.forEach(function (option) {
                    vfw.workspace.modal.build_radio(item, entry_name, newNode, option)
                });
            }
        }
    } else if ('supportedValues' in item && Array.isArray(item.supportedValues) && item.supportedValues.length > 1) {
        if ('maxOccurs' in item) {
            if (item.maxOccurs === 1) {
                item.supportedValues.forEach(function (option) {
                    vfw.workspace.modal.build_radio(item, entry_name, newNode, option)
                });
            }
        }
    } else if ("enum" in item.schema) {
        item.schema.enum.forEach(function (option) {
            vfw.workspace.modal.build_radio(item, entry_name, newNode, option)
        });
    } else if ('keywords' in item && item.keywords.includes('pattern')) {
        vfw.workspace.modal.build_regexText(item, entry_name, newNode)
    } else if (vfw.var.EXT_DATATYPES.includes(item.dataType)) {
        countDropDowns = vfw.workspace.modal.build_dropdown(item, newNode, countDropDowns)

        /** Set input element according to dataType */
    } else {
        inElement = document.createElement("INPUT");
        inElement.id = 'mod_in_el_' + item.identifier;  // item.id;
        inElement.name = entry_name;  // item.identifier;
        inElement.title = item.description;  // item.identifier;
        inElement.setAttribute("list", item.title + '_list');  // item.identifier + '_list');

        switch (item.schema.type) {  // (item.dataType) {
            case 'string':
                inElement.type = "text";
                inElement.appendChild(vfw.workspace.modal.set_textfield_opt(item, resultData, sessionStoreData))
                if ("default" in item.schema) inElement.value = item.schema.default;
                if ('defaultValue' in item) inElement.value = item.defaultValue;  // old schema
                break;
            case 'boolean':
                inElement.type = "checkbox";

                if ("default" in item.schema && item.schema.default === true) {
                    inElement.checked = true;
                }
                else if ('defaultValue' in item && item.defaultValue === true) {
                    inElement.checked = true;
                }
                break;
            case 'dateTime':
                inElement.type = "datetime-local";
                inElement.appendChild(vfw.workspace.modal.set_textfield_opt(item, resultData, sessionStoreData))
                if ("default" in item.schema) inElement.value = item.schema.default;
                if ('defaultValue' in item) inElement.value = item.defaultValue;  // old schema
                break;
            case 'float':
                inElement.type = "number";
                inElement.step = "0.000001";
                inElement.appendChild(vfw.workspace.modal.set_textfield_opt(item, resultData, sessionStoreData))
                if ("default" in item.schema) inElement.value = item.schema.default;
                if ('defaultValue' in item) inElement.value = item.defaultValue;  // old schema
                break;
            case 'integer':
                inElement.type = "number";
                inElement.appendChild(vfw.workspace.modal.set_textfield_opt(item, resultData, sessionStoreData))
                if ("default" in item.schema) inElement.value = item.schema.default;
                if ('defaultValue' in item) inElement.value = item.defaultValue;  // old schema
                break;
            case 'number':
                inElement.type = "number";
                if (item.schema.format  == "float") inElement.step = "0.000001";
                inElement.appendChild(vfw.workspace.modal.set_textfield_opt(item, resultData, sessionStoreData))
                if ("minimum" in item.schema) inElement.min = item.schema.minimum;
                if ("maximum" in item.schema) inElement.max = item.schema.maximum;
                if ("default" in item.schema) inElement.value = item.schema.default;
                if ('defaultValue' in item) inElement.value = item.defaultValue;  // old schema
                break;
            case 'positiveInteger':
                inElement.type = "number";
                inElement.min = "0";
                inElement.appendChild(vfw.workspace.modal.set_textfield_opt(item, resultData, sessionStoreData))
                if ("default" in item.schema) inElement.value = item.schema.default;
                if ('defaultValue' in item) inElement.value = item.defaultValue;  // old schema
                break;
            case 'ComplexData':
                inElement.type = "text";
                if ('defaultValue' in item) {
                    if ('mimeType' in item.defaultValue) inElement.value = item.defaultValue.mimeType;
                }
                break;
            case 'BoundingBoxData':
                console.warn('you have to handle BoundingBoxData properly');
                if ('defaultValue' in item) inElement.value = item.defaultValue;
                break;
            default:
                console.warn(' new dataType: ', item.schema)  // item.dataType)
        }
        if (item.minOccurs > 0) {
            inElement.required = true
        }
        newNode.appendChild(inElement);
    }
    return newNode;
}

/**
 * Build modal (popup) for a selected wps tool.
 *
 * @param {object} wpsInfo - Complete description from the process
 * @param {string} service - which wps server
 */
vfw.workspace.modal.build_modal = function (wpsInfo, service, values = [], boxId = []) {

    /** Collect the data that is available for the tools. If key has no data an empty dict is returned.
     * @param {string} store - Which key of the Session Storage should be loaded
     */
    getStorageOrDict = function (store) {
        return sessionStorage.getItem(store) ? JSON.parse(sessionStorage.getItem(store)) : {};
    }
    let sessionStoreData = getStorageOrDict("dataBtn");
    let resultData = getStorageOrDict("resultBtn");
    let workflowData = getStorageOrDict("workflow");

    let newElement = "";
    let modInElement = document.getElementById("mod_in");
    let modOutElement = document.getElementById("mod_out");
    let modFootElement = document.getElementById("modal-footer");

    if (!sessionStoreData) sessionStoreData = {}
    if (!resultData) resultData = {}
    if (!workflowData) {
        workflowData = {}
    } else {
        workflowData = workflowData[boxId]
    }

    /** create the heading of the modal */
    vfw.workspace.modal.setHead(wpsInfo, service)

    /** inputs: **/
    modInElement.innerHTML = "";
    let inElement = "", newNode = "", nodeText = "";
    let outElementIdList = [];

    /** Loop over input parameters and create an appropriate input element for each */
    Object.entries(wpsInfo.inputs).forEach(function (entry_value, index) {
        newNode = vfw.html.createInputElement(entry_value, resultData, sessionStoreData);
        if (typeof (newNode) === 'object') modInElement.appendChild(newNode)
    });

    /** outputs: **/
    document.getElementById("mod_out").innerHTML = "";

    nodeText = document.createElement("p");
    nodeText.appendChild(document.createTextNode(" Name for output in data store: "));

    newNode = document.createElement("div");
    newNode.appendChild(nodeText);
    let outElement = document.createElement("input");
    newNode.appendChild(outElement);
    if (typeof (newNode) === 'object') modOutElement.appendChild(newNode);
    let modal = document.getElementById("workModal");
    modal.setAttribute("name", wpsInfo.identifier);
    modal.style.display = "block";
    let currentModal = new vfw.workspace.modalObj(wpsInfo.identifier, outElementIdList);

    let batchBtn = modFootElement.getElementsByClassName("work_modal-createbatch")[0]
    batchBtn.addEventListener("click", function (evt) {
        vfw.workspace.modal.openBatchprocess('modal', wpsInfo, service);
    });
}

/**
 * Create DATALIST to add a dropdown to a text box
 *
 * @param {object} item
 * @param {object} resultData
 * @param {object} sessionStoreData
 */
vfw.workspace.modal.set_textfield_opt = function (item, resultData, sessionStoreData) {
    const type = item.dataType;
    let inDatalist = "";
    inDatalist = document.createElement("DATALIST");
    inDatalist.setAttribute("id", 'mod_in_el_' + item.title + '_list');  // item.identifier + '_list');
    let optElement = "";
    Object.entries(resultData).forEach((dataset) => {
        if (dataset[1].type === type) {
            optElement = document.createElement("OPTION");
            optElement.setAttribute("value", dataset[1].outputs);
            optElement.innerText = dataset[1].name;
            inDatalist.appendChild(optElement);

        }
    })
    return inDatalist;
}

vfw.workspace.workflow.load = function () {
    alert("Load is not implemented yet.")
}

vfw.workspace.workflow.save = function () {
    alert("Save is not implemented yet.")
    console.log("save isn't implemented yet: ",
        JSON.parse(document.getElementById('is_authenticated').value))
}


/**
 * check if all required values of a tool have a value or id assigned to.
 *
 * @param {string} server - name of wps server
 * @param {string} tool - id/name of tool on wps server
 * @param {object} inputs - data for the tool to process
 */
vfw.workspace.workflow.check_inputs = function (server, tool, inputs) {
    let has_inIds, has_inVals;
    let result = {'error': false, 'error_index': []}
    let testtool = JSON.parse(sessionStorage.getItem('tools'))[server][tool]
    testtool.dataInputs.forEach((testinput, i) => {
        if (testinput.required) {
            has_inIds = inputs[1].inId_list && inputs[1].inId_list[i];
            has_inVals = inputs[1].value_list && inputs[1].value_list[i];
            if (!has_inIds && !has_inVals) {
                result.error = true;
                result.error_index.push({[inputs[0]]: i});
            }
        }
    })
    return result;
}


vfw.workspace.workflow.run = function () {
    let errors = [];
    let box_result;
    let workflow = vfw.session.get_workflow();
    let processTree = vfw.workspace.workflow.create_processTree(workflow);
    let processChain = vfw.workspace.workflow.create_ReverseProcessOrder(processTree).reverse();
    let preppedWorkflow = vfw.workspace.workflow.prep_wps_workflow(workflow, processChain);
    Object.entries(preppedWorkflow).map((box) => {
        box_result = vfw.workspace.workflow.check_inputs(box[1].serv, box[1].id, box);
        if (box_result.error) {
            errors.push(box_result)
        }
    })

    $.ajax({
        url: vfw.var.DEMO_VAR + "/workspace/workflowrun",
        data: {
            processrun: JSON.stringify({'workflow': preppedWorkflow, 'chain': processChain}),
            'csrfmiddlewaretoken': vfw.var.csrf_token,
        }, /** data sent with post request **/
    })
        .done(function (result) {
            console.log('result: ', result)
        })
    console.log("run isn't implemented yet.")
}

vfw.workspace.workflow.prep_wps_workflow = function (workflow, processChain) {
    let preppedWorkflow = {};
    let outputName;

    for (let i of processChain) {
        outputName = workflow[i].output_ids === [] ? workflow[i].name + "_" : workflow[i].name;
        preppedWorkflow[i] = {
            id: workflow[i].orgid,
            inId_list: workflow[i].input_ids,
            in_type_list: workflow[i].inputs,
            key_list: workflow[i].input_keys,
            in_box_list: workflow[i].input_boxes,
            output_Name: outputName,
            serv: workflow[i].service,
            value_list: workflow[i].input_values,
        }
    }
    return preppedWorkflow;
}


/**
 * Remove boxes from Dropzone, from Sessionstorage and set workflow name to default name.
 */
vfw.workspace.workflow.clear_workflow = function () {
    vfw.draw2d.canvas.clear();
    vfw.session.set_workflow_name()
    document.getElementById("workflow_name").value = gettext('my workflow')
    sessionStorage.setItem('workflow', JSON.stringify({'name': "my workflow"}))
    vfw.session.draw2d.setdata()
}


/**
 * Check in- and output of connected boxes and build the workflow as a tree.
 * @param {{}} workflow
 */
vfw.workspace.workflow.create_processTree = function (workflow) {
    if (Object.keys(workflow).length <= 1) {
        alert(gettext("Please Load or Create a workflow to run first."))
        return;
    }
    let processList = [];
    let processDict = {};
    let processTree = {};
    let endNode = [];
    let orderedProcesses = [];
    let boxIndex = 0;

    // get processes of workflow
    Object.entries(workflow).forEach(function (box, i) {
        if (box[1].source === 'toolbar') {
            processList.push(box[0])
            processDict[box[0]] = {children: box[1].input_ids};
            processDict[box[0]].parents = box[1].output_ids;
            if (!box[1].output_ids && box[1].output_boxes.length == 0) {
                endNode.push(box[0])
            }
        }
    })
    if (endNode.length > 1) {
        alert(gettext("Your workflow is supposed to end in a single process."))
        return;
    }

    /**
     * create tree of processes. Send ID of the last process in the chain
     * @param {string} ID - endnote
     * @param {dictionary} processDict - dict of all process
     * @param {array} processList - list of all processes
     */
    function _createTree(ID, processDict, processList, allProcesses) {
        if (!processList.includes(ID)) {
            processList.push(ID);
        } else {
            alert(gettext("At least one process is used more than once. This could result in an infinite loop and is forbidden (yet)."))
            console.warn('Please check box with id: ', ID)
        }
        let tree = {};
        for (let i of processDict[ID].children) {
            tree[i] = allProcesses.includes(i) && typeof processDict[i].children != "undefined" ? _createTree(i, processDict, processList, allProcesses) : {};
        }
        return tree;
    }

    processTree[endNode] = {};
    processTree[endNode] = _createTree(endNode[0], processDict, [], processList);
    return processTree;
}


/**
 * Create a list of processes from a process tree in the reverse order they are supposed to run.
 * @param {dict} processDict
 * @param {number} depth
 * @param {dict} innerProcesses
 */
vfw.workspace.workflow.create_ReverseProcessOrder = function (processTree, depth = 0, innerProcesses = []) {
    for (let [boxName, deeperElements] of Object.entries(processTree)) {
        if (boxName) {
            innerProcesses.push(boxName);
            innerProcesses.concat(
                vfw.workspace.workflow.create_ReverseProcessOrder(deeperElements, depth += 1, innerProcesses)
            )
        }
    }
    return innerProcesses;
}
