const box_types = ['array', 'iarray', 'varray', 'ndarray', '_2darray',
    'timeseries', 'vtimeseries', 'raster', 'vraster', 'idataframe', 'vdataframe',
    'time-dataframe', 'vtime-dataframe', 'html', 'plot', 'figure', 'image']

/**
 * Load metadata of a wps process.
 * The in- and outputs (and so on) of a tool are not loaded when page loads but on its first use.
 * Then stored in the sessionStorage for the next time the user wants to use this tool.
 *
 * @param {string} service - wps service as stored in database
 * @param {string} identifier - identifier of a wps process
 * @param {string, list} inputs - ugly hack - from result store comes key-value pair, from workspace comes only a btnName
 **/
vfw.workspace.modal.open_wpsprocess = function (service, identifier, inputs) {
    let modal_values = vfw.session.get_workflow();
    let json = vfw.session.get_wpsprocess(service, identifier);
    vfw.workspace.modal.build_modal(json, service)
    /** Fill the tool with selection made to receive this result button */
    if (typeof inputs === 'string') {
        vfw.workspace.modal.setProcessValues(modal_values[inputs]['input_keys'], modal_values[inputs]['input_values'])
    } else if (Array.isArray(inputs)) {
        vfw.workspace.modal.setProcessValues(inputs[0], inputs[1])
    }
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

    let modal_values = vfw.session.get_workflow();
    let json = vfw.session.get_wpsprocess(service, boxidentifier);
    /** Fill the tool with selection made to receive this result button */
    if (typeof inputs === 'string') {
        vfw.workspace.modal.setPortValue(modal_values[inputs]['input_keys'], modal_values[inputs]['input_values'])
    } else if (Array.isArray(inputs)) {
        vfw.workspace.modal.setPortValue(inputs[0], inputs[1])
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
                'csrfmiddlewaretoken': csrf_token,
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
        vfw.html.popup.classList.add(popActive);
        positionPopup(vfw.html.popup);
        $.when(vfw.session.load_wpsprocess(service, identifier))
            .done(
                function (json) {
                    tools[service][identifier] = json
                    sessionStorage.setItem('tools', JSON.stringify(tools))
                    tool_data = json;
                    vfw.html.popup.classList.remove(popActive);
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
 * Collect data to drop element. (When 'Okay' in Modal is pressed)
 * Check if any inputs or outputs are selected and drop resprective elements, too.
 *
 * @param {object} ev - object passed with drop event
 **/
vfw.workspace.drop_on_click = function (ev) {
    /** Prepare and drop a tool button **/
    let data_id, tool_id, box_id, newbox, toolbox, databox, metadata, dataport, toolport, params, workflow;
    let coords = vfw.workspace.get_drop_coords();
    let modalData = vfw.workspace.modal.prep_data();
    newbox = vfw.workspace.drop_handler(modalData, coords['x'], coords['y'], modalData.id, 'toolbar', modalData.serv)
    tool_id = newbox.boxID;
    toolbox = newbox.box;

    /** Check if tool is connected with other elements to drop and get ports **/
    for (let i in modalData.in_type_list) {
        if (box_types.includes(modalData.in_type_list[i]) && modalData.inId_list[i]) {
            console.log('droped on click: ', i)
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
vfw.workspace.check_pattern = function (checkElement) {
    /** check if an Element of a wps is required **/
    console.warn('TODO: Add pattern check where necessary.')
    return true
}


/**
 * Collect data from modal neeeded to run a process.
 * @returns {{in_type_list: *[], serv: string, outputName: string, key_list: *[], inId_list: *[], id: string, value_list: *[]}}
 */
vfw.workspace.modal.prep_data = function () {
    /** collect inputs **/
    var inKey = [];
    var inValue = [];
    var inType = [];
    var inId = [];
    let dDInput = 0;
    let inModal = document.getElementById('mod_in');
    let inputInputs = inModal.getElementsByTagName('input');
    let dropDInputs = inModal.getElementsByTagName('select');
    let valueList = [];
    let typeList = [];
    let inIdList = [];
    let stored;

    /** first loop over each dropdown in input, then over values in dropdown **/
    for (let i = 0; i < dropDInputs.length; i++) {
        dDInput = dropDInputs[i].selectedOptions;

        /** if many dropdowns **/
        if (dDInput.length > 1) {
            for (let j = 0; j < dDInput.length; j++) {
                // valueList.push(dDInput[j].value)
                stored = JSON.parse(sessionStorage.getItem("dataBtn"))[dDInput[j].value]
                valueList.push(stored['source'] + stored['dbID'])
                typeList.push(stored['type']);
                inIdList.push(dDInput[j].value);
            }
            inValue.push(valueList);
            inKey.push(dropDInputs[i].name);
            inType.push(typeList);
            inId.push(inIdList);

            /** else if one dropdown **/
        } else {
            if (dDInput[0].value.substring(0, 2) == 'db') {
                stored = JSON.parse(sessionStorage.getItem("dataBtn"))[dDInput[0].value]
                inValue.push(stored['source'] + stored['dbID']);
                inType.push(stored['type']);
            } else {
                inValue.push(dDInput[0].value);
                inType.push(stored['type']);
            }
            inKey.push(dropDInputs[i].name);
            inId.push(dDInput[0].value);
        }
    }
    for (let i = 0; i < inputInputs.length; i++) {
        if (inputInputs[i].type == "radio") {
            if (inputInputs[i].checked == true) {
                inKey.push(inputInputs[i].name);
                inValue.push(inputInputs[i].value);
                inType.push('string');
                inId.push('');
            }
        } else if (inputInputs[i].type == "checkbox") {
            inKey.push(inputInputs[i].name);
            if (inputInputs[i].checked == true) {
                inValue.push(true);
                inType.push('boolean');
                inId.push('');
            } else {
                inValue.push(false);
                inType.push('boolean');
                inId.push('');
            }
        } else {
            inKey.push(inputInputs[i].name);
            inValue.push(inputInputs[i].value);
            inType.push('');
            inId.push('');
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
        'in_type_list': inType, 'outputName': outputName, 'inId_list': inId
    }
}

vfw.workspace.modal.run_process = function () {
    vfw.workspace.modal.set_Color("dodgerblue");
    let modal_input = vfw.workspace.modal.prep_data();
    let directshowdatatypes = ['figure', 'string', 'html', 'integer', 'float']
    let group = false;
    let groupName = ''
    let i = 0;
    let members = [];

    $.ajax({
        url: vfw.var.DEMO_VAR + "/workspace/processrun",
        data: {
            processrun: JSON.stringify(modal_input),
            'csrfmiddlewaretoken': csrf_token,
        }, /** data sent with post request **/
    })
        .done(function (json) {  /** Results are stored in the sessionStorage **/
            if (json.execution_status == "ProcessSucceeded") {
                json.wps = modal_input.id;
                json.inputs = {};
                $.each(modal_input.inKey, function (key, value) {
                    json.inputs[value] = modal_input.inValue[i];
                    i++;
                });
                vfw.workspace.modal.set_Color("forestgreen");

                if (Object.keys(json.result).length > 1) {
                    group = true;
                    groupName = vfw.sidebar.set_group_btn_name(modal_input.outputName, 'resultBtn');
                }

                for (let i in json.result) {
                    let btnName = vfw.sidebar.set_result_btn_name(modal_input.outputName);
                    json.result[i].dropBtn.name = btnName;
                    let btnData = {
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
                            += vfw.workspace.build_resultstore_button(btnName, btnData);
                    } else {
                        members.push([btnName, btnData])
                    }
                }
                if (group === true) {
                    document.getElementById("workspace_results").innerHTML
                        += vfw.workspace.build_resultgroup_button(groupName, members);
                    vfw.sidebar.add_groupaccordion_toggle()
                }
            } else if (json.execution_status == "Exception") {
                console.error('error in wps process')
                vfw.workspace.modal.set_Color("firebrick");
            } else if (json.execution_status == "error in wps process") {
                vfw.workspace.modal.set_Color("firebrick");
                console.error('Error in wps process: ', json.error)
            } else if (json.execution_status == "auth_error") {
                vfw.workspace.modal.set_Color("firebrick");
                /** Use Timeout to ensure color changed before popup appears **/
                setTimeout(function () {
                    alert('Error: You are not allowed to run this process. Please Contact your Admin.');
                }, 5);
                console.error('Maybe you have to log in to run processes. ', json.execution_status)
            }
        })
        .fail(function (json) {
            vfw.workspace.modal.set_Color("firebrick");
            console.error('Error, No success: ', json)
        });
}

/**
 * View result directly on top of tool window
 * @param json
 */
vfw.workspace.view_result = function (json) {
    if (json.type == 'figure' || json.type == 'string' || json.type == 'integer') {
        document.getElementById("mod_result").innerHTML = json.outputs; // add plot
    }
    let rModal = document.getElementById("resultModal");
    rModal.style.display = "block";
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
            'csrfmiddlewaretoken': csrf_token,
        }, /** data sent with the post request **/
    })
        .done(function (json) {
            return json
        })
        .fail(function (json) {
            console.error('Error, No success: ', json)
            vfw.workspace.modal.set_Color("firebrick");
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
vfw.workspace.modal.set_Color = function (color) {
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
vfw.workspace.build_resultstore_button = function (name, json) {
    let title = json.wps + "\n" + JSON.stringify(json.inputs).slice(1, -1).replace(/"/g, "'");
    return '<li draggable="true" ondragstart="dragstart_handler(event)" ' +
        'class="w3-padding task is-result" data-sessionStore="resultBtn" ' +
        'data-id="' + json.source + json.dbID + '" btnName="' + name + '" onmouseover="" style="cursor:pointer;" ' +
        'data-btnName="' + name + '" id="' + name + '">' +
        '<span class="w3-medium" title="' + title + '">' +
        '<div class="task__content">' + name + '</div><div class="task__actions"></div>' +
        '</span><span class="' + json['type'] + '"></span>' +
        '<a href="javascript:void(0)" onclick="vfw.session.remove_single_result(\'' + name + '\')" class="w3-hover-white">' +
        '<i class="fa fa-remove fa-fw"></i></a><br></li>';
}

/**
 * Build a button in the result store. Base button for a group of results
 * data-id is used to find results on server,  id is used for the remove button
 *
 * @param  {string} name name for the group button
 * @return {string} HTML Code for the group button
 **/
vfw.workspace.build_resultgroup_button = function (groupname, members) {
    let mhtml = ''
    let ghtml = '<li draggable="true" ondragstart="dragstart_handler(event)" ' +
        'class="w3-padding task is-result-group groupaccordion" data-sessionStore="resultBtn"' +
        '" btnName="' + groupname + '" onmouseover="" style="cursor:pointer;" ' +
        'data-btnName="' + groupname + '" id="' + groupname + '"><span class="w3-medium">' +
        '<div class="task__content">' + groupname + '</div><div class="task__actions"></div></span>' +
        '<span class=""></span>' +
        '<a href="javascript:void(0)" onclick="vfw.session.remove_group_result(\'' + groupname + '\')" class="w3-hover-white">' +
        '<i class="fa fa-remove fa-fw"></i></a><br></li>';

    members.forEach(function (singlemember) {
        mhtml += vfw.workspace.build_resultstore_button(singlemember[0], singlemember[1]);
    })
    ghtml += '<div class="grouppanel">' + mhtml + '</div>'
    return ghtml
}

vfw.session.remove_single_result = function (removeData) {
    document.getElementById(removeData).remove();
    let workspaceData = JSON.parse(sessionStorage.getItem("resultBtn"));
    delete workspaceData[removeData];
    sessionStorage.setItem("resultBtn", JSON.stringify(workspaceData))
}

vfw.session.remove_group_result = function (removeData) {
    let workspaceData = JSON.parse(sessionStorage.getItem("resultBtn"));
    $.each(workspaceData, function (i) {
        if (workspaceData[i].group === removeData) {
            vfw.session.remove_single_result(i)
        }
    })
    document.getElementById(removeData).remove();
}

vfw.session.remove_all_results = function () {
    let groupSet = new Set();
    /** remove button from portal **/
    $.each(JSON.parse(sessionStorage.getItem("resultBtn")), function (key, value) {
        groupSet.add(value.group)
        vfw.session.remove_single_result(key);
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
 * @param {string} newNode - The new HTML Element where the checkbox will be added
 */
vfw.workspace.modal.build_regexText = function (item, newNode) {
    inElement = document.createElement("INPUT");
    inElement.id = item.identifier;
    inElement.name = item.identifier;
    inElement.setAttribute("pattern", item.keywords[1]);
    inElement.type = "text";
    if ('defaultValue' in item) {
        inElement.value = item.defaultValue;
    }
    if ('abstract' in item) {
        inElement.title = item.abstract;
    }
    newNode.appendChild(inElement);
}

/**
 * @param {json} item - input information loaded from Session Storage
 * @param {string} newNode - The new HTML Element where the checkbox will be added
 * @param {string} option - String with predefined value from wps process
 */
vfw.workspace.modal.build_radio = function (item, newNode, option) {
    let nodeText = document.createTextNode(" " + option + " ");
    let inElement = document.createElement("INPUT");
    inElement.type = "radio";
    inElement.value = option;
    inElement.id = item.identifier;
    if (item.minOccurs === 1) inElement.required = true;

    inElement.name = item.identifier;
    if ('defaultValue' in item) {
        if (item.defaultValue == option) inElement.checked = true;
    }
    newNode.appendChild(inElement);
    newNode.appendChild(nodeText);
}

/**
 * @param {json} item - input information loaded from Session Storage
 * @param {HTMLElement} newNode - The new HTML Element where the checkbox will be added
 * @param {string} option - String with predefined value from wps process
 */
vfw.workspace.modal.build_checkbox = function (item, newNode, option) {
    let nodeText = document.createTextNode(" " + option + " ");
    let inElement = document.createElement("input");
    inElement.type = "radio";
    inElement.value = option;
    inElement.id = item.identifier;
    if (item.minOccurs === 1) inElement.required = true;

    inElement.name = item.identifier;
    if ('defaultValue' in item) {
        if (item.defaultValue == option) inElement.checked = true;
    }
    newNode.appendChild(inElement);
    newNode.appendChild(nodeText);
}

/**
 * Function is called when the input should be a dataset.
 *
 * @param {json} item - description of wps input.
 * @param {HTMLParagraphElement} newNode
 * @param {number} countDropDowns
 */
vfw.workspace.modal.build_dropdown = function (item, newNode, countDropDowns) {
    let htmlSelect = document.createElement("SELECT");
    let sessionStoreData = JSON.parse(sessionStorage.getItem("dataBtn"));
    let resultData = JSON.parse(sessionStorage.getItem("resultBtn"));
    let boxLen = 0;
    let aptStoreData = {};
    let aptResultData = {};
    let acceptedDataTypes = DATATYPE.accepts([item.keywords[0]])

    htmlSelect.id = item.identifier;

    for (let i in sessionStoreData) if (acceptedDataTypes.has(sessionStoreData[i].type)) {
        aptStoreData[i] = sessionStoreData[i];
    }
    for (let i in resultData) if (acceptedDataTypes.has(resultData[i].type)) aptResultData[i] = resultData[i]
    boxLen = Object.keys(aptResultData).length + Object.keys(aptStoreData).length;
    if (item.minOccurs > 1) htmlSelect.required = true;

    /** check if input data is available; only build dropdown if there is data to select from **/
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
        if (storeData !== null) {
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
        if (item.maxOccurs > 1 || item.minOccurs > 1) {
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
 * @param {Object} item - Data description from the wps process.
 * @param {HTMLElement} optionGroup - HTML group Element. Different groups to seperate Data and Results in dropdown
 * @param {Object} sidebarData - The relevant elements from the sessionStorage
 */
vfw.workspace.modal.build_dropdown_opt = function (item, optionGroup, sidebarData) {
    let opt;
    Object.keys(sidebarData).forEach(function (singleData) {
        opt = document.createElement("OPTION");
        if (sidebarData[singleData].abbr && sidebarData[singleData].unit) {
            opt.innerText = `${singleData} ${sidebarData[singleData].name} (${sidebarData[singleData].abbr}
            in ${sidebarData[singleData].unit})`;
        } else {
            opt.innerText = `${singleData}`;
        }
        opt.value = sidebarData[singleData].wpsID ? 'wpsID' + (sidebarData[singleData].wpsID) : singleData;
        if (item.keywords.length == 1) opt.selected = true;
        optionGroup.appendChild(opt);
    })
    return optionGroup
}

/**
 * Build modal (popup) for a selected wps tool.
 *
 * @param {object} wpsInfo - Complete description from the process
 * @param {string} service - which wps server
 */
vfw.workspace.modal.build_modal = function (wpsInfo, service, values = [], boxId = []) {
    let sessionStoreData = JSON.parse(sessionStorage.getItem("dataBtn"));
    let resultData = JSON.parse(sessionStorage.getItem("resultBtn"));
    let workflowData = JSON.parse(sessionStorage.getItem("workflow"));
    let element = document.getElementById("mod_head");
    let newElement = "";

    if (!sessionStoreData) sessionStoreData = {}
    if (!resultData) resultData = {}
    if (!workflowData) {
        workflowData = {}
    } else {
        workflowData = workflowData[boxId]
    }
    element.innerHTML = wpsInfo.title;
    element.dataset.service = service;
    element.dataset.process = wpsInfo.identifier;
    element = document.getElementById("mod_abs");
    if (wpsInfo.abstract) {
        newElement = wpsInfo.abstract;
    }
    element.innerHTML = newElement;

    /** inputs: **/
    element = document.getElementById("mod_in");
    element.innerHTML = "";
    let inElement = "", newNode = "", nodeText = "";
    let outElementIdList = [];
    let countDropDowns = 0;

    wpsInfo.dataInputs.forEach(function (item, index) {
        newNode = document.createElement("p");

        /** Set title of Input and set the 'required' flag if necessary **/
        let titleText = "";
        if (item.minOccurs == 0) {
            titleText = " " + item.title + ": "
        } else if (item.defaultValue) {
            titleText = " " + item.title + ": "
        } else if (item.required === true) {
            titleText = " " + item.title + " (*) : ";
            inElement.required = true;
        } else {
            titleText = " " + item.title + ": "
        }

        nodeText = document.createTextNode(titleText);
        newNode.appendChild(nodeText);
        if ('allowedValues' in item && Array.isArray(item.allowedValues) && item.allowedValues.length > 1) {
            if ('maxOccurs' in item) {
                if (item.maxOccurs === 1) {
                    // nodeText = "";
                    item.allowedValues.forEach(function (option) {
                        vfw.workspace.modal.build_radio(item, newNode, option)
                    });
                }
            }
        } else if ('supportedValues' in item && Array.isArray(item.supportedValues) && item.supportedValues.length > 1) {
            if ('maxOccurs' in item) {
                if (item.maxOccurs === 1) {
                    item.supportedValues.forEach(function (option) {
                        vfw.workspace.modal.build_radio(item, newNode, option)
                    });
                }
            }
        } else if ('keywords' in item && item.keywords.includes('pattern')) {
            vfw.workspace.modal.build_regexText(item, newNode)
        } else if ('keywords' in item) {
            countDropDowns = vfw.workspace.modal.build_dropdown(item, newNode, countDropDowns)

            /** Set input element according to dataType */
        } else {
            inElement = document.createElement("INPUT");
            inElement.id = item.identifier;
            inElement.name = item.identifier;
            inElement.setAttribute("list", item.identifier + '_list');

            switch (item.dataType) {
                case 'string':
                    inElement.type = "text";
                    inElement.appendChild(vfw.workspace.modal.set_textfield_opt(item, resultData, sessionStoreData))
                    if ('defaultValue' in item) {
                        inElement.value = item.defaultValue;
                    }
                    break;
                case 'boolean':
                    inElement.type = "checkbox";
                    if ('defaultValue' in item && item.defaultValue == true) inElement.checked = true;
                    break;
                case 'dateTime':
                    inElement.type = "datetime-local";
                    inElement.appendChild(vfw.workspace.modal.set_textfield_opt(item, resultData, sessionStoreData))
                    if ('defaultValue' in item) inElement.value = item.defaultValue;
                    break;
                case 'float':
                    inElement.type = "number";
                    inElement.step = "0.000001";
                    inElement.appendChild(vfw.workspace.modal.set_textfield_opt(item, resultData, sessionStoreData))
                    if ('defaultValue' in item) inElement.value = item.defaultValue;
                    break;
                case 'integer':
                    inElement.type = "number";
                    inElement.appendChild(vfw.workspace.modal.set_textfield_opt(item, resultData, sessionStoreData))
                    if ('defaultValue' in item) inElement.value = item.defaultValue;
                    break;
                case 'positiveInteger':
                    inElement.type = "number";
                    inElement.min = "0";
                    inElement.appendChild(vfw.workspace.modal.set_textfield_opt(item, resultData, sessionStoreData))
                    if ('defaultValue' in item) inElement.value = item.defaultValue;
                    break;
                case 'ComplexData':
                    inElement.type = "text";
                    if ('defaultValue' in item) {
                        if ('mimeType' in item.defaultValue) inElement.value = item.defaultValue.mimeType;
                    }
                    break;
                case 'BoundingBoxData':
                    console.error('you have to handle BoundingBoxData properly');
                    if ('defaultValue' in item) inElement.value = item.defaultValue;
                    break;
                default:
                    console.error(' new dataType: ', item.dataType)
            }
            if (item.minOccurs > 0) {
                inElement.required = true
            newNode.appendChild(inElement);
        }
        if (typeof (newNode) === 'object') element.appendChild(newNode)
    });

    /** outputs: **/
    document.getElementById("mod_out").innerHTML = "";

    element = document.getElementById("mod_out");

    nodeText = document.createElement("p");
    nodeText.appendChild(document.createTextNode(" Name for output in data store: "));

    newNode = document.createElement("div");
    newNode.appendChild(nodeText);
    let outElement = document.createElement("input");
    newNode.appendChild(outElement);
    if (typeof (newNode) === 'object') element.appendChild(newNode);
    let modal = document.getElementById("workModal");
    modal.setAttribute("name", wpsInfo.identifier);
    modal.style.display = "block";
    let currentModal = new vfw.workspace.modalObj(wpsInfo.identifier, outElementIdList);
}

/**
 * Create DATALIST to add a dropdown to a text box
 *
 * @param {object} item
 * @param {object} resultData
 * @param {object} sessionStoreData
 */
vfw.workspace.modal.set_textfield_opt = function (item, resultData, sessionStoreData) {
    let inDatalist = "";
    let type = item.dataType;
    inDatalist = document.createElement("DATALIST");
    inDatalist.setAttribute("id", item.identifier + '_list');
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
            'csrfmiddlewaretoken': csrf_token,
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
        console.log('i: ', i)
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
    canvas.clear();
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

    // get processes of workflow
    Object.entries(workflow).forEach(function (box, i) {
        if (box[1].source === 'toolbar') {
            console.log('box: ', i, box)
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
            console.log('+ i: ', i)
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
