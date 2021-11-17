function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text/html", ev.target.id);
}

function drop(ev) {
    ev.preventDefault();
    let droplet = ev.dataTransfer.getData("text/html");

    // let droplet = document.createElement('canvas');
    // let dropletCopy = document.createElement('canvas');
    let dropletCopy = document.getElementById(droplet).cloneNode(true);
    // build new id for new element:
    if (sessionStorage.getItem("dz_count")) {
        sessionStorage.setItem("dz_count", JSON.parse(sessionStorage.getItem("dz_count")) + 1)
    } else {
        sessionStorage.setItem("dz_count", 1)
    }
    dropletCopy.id = "dz" + sessionStorage.getItem("dz_count");
    dropletCopy.classList.add('tool-btn');
    dropletCopy.style.left = ev.offsetX + "px";
    dropletCopy.style.top = ev.offsetY + "px";
    // ev.dataTransfer.setDragImage(dropletCopy, ev.offsetX + "px", ev.offsetY + "px")
    ev.target.appendChild(dropletCopy);
}

// TODO: btn_id is not used yet, though it is needed to decide if an element has to be placed in the Dropozone on save:
//  if process_id == btn_id place btn in dropzone (on save)
/**
 * Load metadata of a wps process.
 * The in- and outputs (and so on) of a tool are not loaded when page loads but on its first use.
 * Then stored in the sessionStorage for the next time the user wants to use this tool.
 *
 * @param {string} service - wps service as stored in database
 * @param {string} identifier - identifier of a wps process
 **/
function wpsprocess(service, identifier) {
    let tools = get_sessionStorage_tools(service)
    if (tools[service][identifier]) {
        build_modal(tools[service][identifier], service)
    } else {
        load_wpsprocess(service, identifier)
            .done(function (json) {
                build_modal(json, service)
                tools[service][identifier] = json
                sessionStorage.setItem('tools', JSON.stringify(tools))
            })
    }
}

/**
 * Actual function to load metadata of a wps process.
 *
 * @param {string} service - wps service as stored in database
 * @param {string} identifier - identifier of a wps process
 **/
function load_wpsprocess(service, identifier) {
    return $.ajax({
        url: DEMO_VAR + "/workspace/processview",
        //url: DEMO_VAR+"/wps_gui/"+service+"/process",
        dataType: 'json',
        async: false,
        data: {
            processview: JSON.stringify({id: identifier, serv: service}),
            'csrfmiddlewaretoken': csrf_token,
        }, /** data sent with the post request **/
    })
        .fail(function (e) {
            console.error('Failed: ', e)
        });
}

/**
 * Load metadata of a wps process.
 * in- and outputs and so on of a tool are not loaded when page loads but on its first use and stored in
 * the sessionStorage for the next time the user wants to use this tool
 * @param {string} service - wps service as stored in database
 * @param {string} identifier - identifier of a wps process
 * @return {obj} json - object of a wps process as saved in sessionStorage
 */
function get_wpsprocess(service, identifier) {
    let tools = get_sessionStorage_tools(service)
    if (tools[service][identifier]) {
        return tools[service][identifier]
    } else {
        load_wpsprocess(service, identifier)
            .done(function (json) {
                tools[service][identifier] = json
                sessionStorage.setItem('tools', JSON.stringify(tools))
                return json
            })
        /* .fail(function (e) {
             console.error('Failed: ', e)
         });*/
    }
}

function add_connection(sourcePort, targetPort) {
    // canvas.installEditPolicy(connection.connectionPolicy);
    // let box = new Box(
    //     box_param.name, box_param.orgid, box_param.type,
    //     box_param.inputs, box_param.outputs, source, service, boxID
    // )
    //
    // canvas.add(box.box, x, y);
    // console.log('toolbox getOutputPort(0): ', toolbox.getOutputPort(0))
    // console.log('toolbox getOutputPort(): ', toolbox.getOutputPort())
    console.log('canvas ports: ', canvas.getAllPorts())
    let connection = new draw2d.Connection({
        source: sourcePort,
        target: targetPort
    });
    // let connection = createConnection(dataport, toolport);
    // let connection = createConnection(start.getOutputPort(0),end.getInputPort(0));
    canvas.add(connection);

}

/**
 * create a dict with random coordinates on the dropzone ('dropdiv').
 * TODO: avoid overlap of boxes
 * @returns {{x: number, y: number}}
 */
function get_drop_coords() {
    let dropzone = document.getElementById('dropdiv');
    let dropzone_coords = dropzone.getBoundingClientRect();
    let x_pad = 0;
    let y_pad = 0;
    let x, y
    if (dropzone_coords.height > 100) {x_pad = 300};
    if (dropzone_coords.width > 300) {y_pad = 200};
    x = Math.floor((Math.random() * (dropzone_coords.width-x_pad))-x_pad + dropzone_coords.left);
    y = Math.floor((Math.random() * (dropzone_coords.height-y_pad))+y_pad/2 - dropzone_coords.top);
    return {'x': x, 'y': y}
}


/**
 * Collect data to drop element. (When Okay in Modal is pressed)
 * Check if any inputs or outputs are selected and drop resprective elements, too.
 *
 * @param {object} ev - object passed with drop event
 **/
function drop_on_click(ev) {
    /** Prepare and drop a tool button **/
    let tool_id, data_id, newbox, toolbox, databox, metadata, dataport, toolport;
    let coords = get_drop_coords();
    let modalData = prep_modal_data();
    newbox = drop_handler(modalData, coords['x'], coords['y'], modalData.id, 'toolbar', modalData.serv)
    tool_id = newbox.boxID;
    toolbox = newbox.box;

    /** Check if tool is connected with other elements to drop and get ports **/
    let box_types = ['array', 'iarray', 'varray', 'ndarray', '_2darray',
        'timeseries', 'vtimeseries', 'raster', 'vraster', 'idataframe', 'vdataframe',
        'time-dataframe', 'vtime-dataframe', 'html', 'plot', 'figure', 'image']
    for (let i in modalData.type_list) {
        if (box_types.includes(modalData.type_list[i]) && modalData.inId_list[i]) {
            metadata = JSON.parse(sessionStorage.getItem("dataBtn"))[modalData.inId_list[i]]
            newbox = drop_handler(metadata, coords['x']-40, coords['y']-40, 'sidebtn' + modalData.inId_list[i], 'workspace')
            tool_id = newbox.boxID;
            databox = newbox.box;
            dataport = databox.getOutputPort(0);
            // TODO: Not sure if ports have always the same order as in modal. Find better way to get right port.
            toolport = toolbox.getInputPort(parseInt(i));
            // add_connection(dataport, toolport);
        }
    }
}

/**
 * Check if an input (an Element of a wps) is required and if it is required check if the input has a value.
 *
 * @param {HTMLElement} checkElement Element to be checked if filled.
 */
function is_required(checkElement) {
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
    return passed
}

/**
 * Check if an input has a regex pattern and if input is correct.
 *
 * @param {HTMLElement} checkElement Element to be checked if filled.
 */
function check_pattern(checkElement) {
    /** check if an Element of a wps is required **/
    console.warn('TODO: Add pattern check where necessary.')
    return true
}


/**
 * Collect data from modal neeeded to run a processes.
 * @returns {{type_list: *[], serv: string, outputName: string, key_list: *[], inId_list: *[], id: string, value_list: *[]}}
 */
function prep_modal_data() {
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
    return {'id': identifier, 'serv': wpsservice, 'key_list': inKey, 'value_list': inValue,
        'type_list': inType, 'outputName': outputName, 'inId_list': inId}
}

// TODO: runProcess now works only on execution from modal. Adjust to be usable from Dropzone too,
//  when you have the drop objects
// TODO: Improve code by using HTML Forms
function modal_run_process() {
    set_modalColor("dodgerblue");
    let modal_input = prep_modal_data();

    $.ajax({
        url: DEMO_VAR + "/workspace/processrun",
        data: {
            processrun: JSON.stringify(modal_input),
            'csrfmiddlewaretoken': csrf_token,
        }, /** data sent with post request **/
    })
        .done(function (json) {  /** Results are stored in the sessionStorage **/
            if (json.execution_status == "ProcessSucceeded") {
                let group = false;
                let groupName = ''
                let i = 0;
                let members = [];
                let directshowdatatypes = ['figure', 'string', 'html']

                json.wps = modal_input.id;
                json.inputs = {};
                $.each(modal_input.inKey, function (key, value) {
                    json.inputs[value] = modal_input.inValue[i];
                    i++;
                });
                set_modalColor("forestgreen");

                if (Object.keys(json.result).length > 1) {
                    group = true;
                    groupName = set_group_btn_name(modal_input.outputName, 'resultBtn');
                    // document.getElementById("workspace_results").innerHTML
                    //     += build_resultgroup_button(groupName);
                }

                for (let i in json.result) {
                    let btnName = set_result_btn_name(modal_input.outputName);
                    json.result[i].dropBtn.name = btnName;
                    let btnData = {
                        dbID: json.result[i].wpsID,
                        inputs: json.inputs,
                        name: btnName,
                        type: json.result[i].type,
                        outputs: json.result[i].data,
                        wps: json.wps,
                        source: "wps",
                        status: json.execution_status,
                        dropBtn: json.result[i].dropBtn,
                        group: groupName
                    }
                    add_resultbtn_to_sessionstore(btnName, btnData);
                    if (directshowdatatypes.includes(btnData.type)) {
                        add_resultbtn_to_modal(btnData)
                    }

                    if (group === false) {
                        document.getElementById("workspace_results").innerHTML
                            += build_resultstore_button(btnName, btnData);
                    } else {
                        members.push([btnName, btnData])
                    }
                }
                if (group === true) {
                    document.getElementById("workspace_results").innerHTML
                        += build_resultgroup_button(groupName, members);
                    add_groupaccordion_toggle()
                }
            } else if (json.execution_status == "Exception") {
                console.error('error in wps process')
                set_modalColor("firebrick");
                // alert('Error: Failed to execute your request.');
            } else if (json.execution_status == "error in wps process") {
                set_modalColor("firebrick");
                console.error('Error in wps process: ', json.error)
                // alert('Error: Failed to execute your request.');
            } else if (json.execution_status == "auth_error") {
                set_modalColor("firebrick");
                /** Use Timeout to ensure color changed before popup appears **/
                setTimeout(function () {
                    alert('Error: You are not allowed to run this process. Please Contact your Admin.');
                }, 5);
                console.error('Maybe you have to log in to run processes. ', json.execution_status)
            }
        })
        .fail(function (json) {
            set_modalColor("firebrick");
            console.error('Error, No success: ', json)
        });
}

// Not used yet
function run_wps(input_dict) {
    let modhead = document.getElementById('mod_head');
    let wpsservice = modhead.dataset.service;
    let identifier = modhead.dataset.process;

    $.ajax({
        url: DEMO_VAR + "/workspace/processrun",
        data: {
            processrun: JSON.stringify({
                id: identifier, serv: wpsservice,
                key_list: input_dict.keys(), value_list: input_dict.values()
            }),
            // processrun: JSON.stringify(input_dict),
            'csrfmiddlewaretoken': csrf_token,
        }, /** data sent with the post request **/
    })
        .done(function (json) {
            return json
        })
        .fail(function (json) {
            console.error('Error, No success: ', json)
            set_modalColor("firebrick");
        })
}


/**
 * Check if result data in sessionStorage exists, if yes check if name already exists, if yes add numger to name.
 *
 * @param {string} name
 */
function set_result_btn_name(name) {
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
function set_group_btn_name(name, storage) {
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
function set_modalColor(color) {
    let modalColor = document.getElementById("modal-header");
    modalColor.style.backgroundColor = color;
    modalColor = document.getElementById("modal-footer");
    modalColor.style.backgroundColor = color;
    document.getElementsByClassName("work_modal-output")[0].style.display = "none";
}

/**
 *  A Object with names and values from the input object / not used yet
 *  */
function modalObj(processId, processInput, processOutput) {
    this.processId = processId;
    this.processInput = processInput;
    this.processOutput = processOutput;
}


/**
 * Show hidden button in modal to enable quick preview of results.
 *
 * @param {{outputs, inputs: (*|{}), dbID: *, name: (*|string), dropBtn, wps: string, source: string, type, status: *, group: string}} json
 */
function add_resultbtn_to_modal(json) {
    let wspan_out = document.getElementsByClassName("work_modal-output")[0];
    wspan_out.style.display = "block";
    wspan_out.onclick = () => {
        if (json.type == 'figure' || json.type == 'string') {
            document.getElementById("mod_result").innerHTML = json.outputs; // add plot
        }
        let rModal = document.getElementById("resultModal");
        rModal.style.display = "block";
        popup.classList.remove(popActive);
        modalToggleSize.style.display = "none";
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
function add_resultbtn_to_sessionstore(btnName, json) {
    let result_btns = {};
    if (sessionStorage.getItem("resultBtn")) {
        result_btns = JSON.parse(sessionStorage.getItem("resultBtn"));
        if (Object.keys(result_btns).includes(btnName)) {
            console.error('Error! Names should be unique! Problem with race conditions?')
        }
    }
    result_btns[btnName] = json
    /*{
        type: json.type,
        wps: json.wps,
        inputs: json.inputs,
        wpsID: json.wpsID,
        status: json.execution_status,
        dropBtn: json.dropBtn
    };*/
    sessionStorage.setItem("resultBtn", JSON.stringify(result_btns));
}

//TODO: Is it necessary that a result knows which function it came from and what the input parameters were?
/**
 * Build a button in the result store.
 * data-id is used to find results on server, id is used for the remove button
 *
 * @param  {string} name - name for the button
 * @param  {obj} json - Object holding all necessary info about result
 * @return {string} - HTML Code for the button
 **/
function build_resultstore_button(name, json) {
    let title = json.wps + "\n" + JSON.stringify(json.inputs).slice(1, -1).replace(/"/g, "'");
    return '<li draggable="true" ondragstart="dragstart_handler(event)" ' +
        'class="w3-padding task is-result" data-sessionStore="resultBtn" ' +
        'data-id="' + json.source + json.dbID + '" btnName="' + name + '" onmouseover="" style="cursor:pointer;" ' +
        'id="' + name + '">' +
        '<span class="w3-medium" title="' + title + '">' +
        '<div class="task__content">' + name + '</div><div class="task__actions"></div>' +
        '</span><span class="' + json['type'] + '"></span>' +
        '<a href="javascript:void(0)" onclick="remove_single_result(\'' + name + '\')" class="w3-hover-white">' +
        '<i class="fa fa-remove fa-fw"></i></a><br></li>';
}

/**
 * Build a button in the result store. Base button for a group of results
 * data-id is used to find results on server,  id is used for the remove button
 *
 * @param  {string} name name for the group button
 * @return {string} HTML Code for the group button
 **/
function build_resultgroup_button(groupname, members) {
    let mhtml = ''
    let ghtml = '<li draggable="true" ondragstart="dragstart_handler(event)" ' +
        'class="w3-padding task is-result-group groupaccordion" data-sessionStore="resultBtn"' +
        '" btnName="' + groupname + '" onmouseover="" style="cursor:pointer;" ' +
        'id="' + groupname + '"><span class="w3-medium">' +
        '<div class="task__content">' + groupname + '</div><div class="task__actions"></div></span>' +
        '<span class=""></span>' +
        '<a href="javascript:void(0)" onclick="remove_group_result(\'' + groupname + '\')" class="w3-hover-white">' +
        '<i class="fa fa-remove fa-fw"></i></a><br></li>';

    members.forEach(function (singlemember) {
        mhtml += build_resultstore_button(singlemember[0], singlemember[1]);
    })
    ghtml += '<div class="grouppanel">' + mhtml + '</div>'
    return ghtml
}

function remove_single_result(removeData) {
    document.getElementById(removeData).remove();
    let workspaceData = JSON.parse(sessionStorage.getItem("resultBtn"));
    delete workspaceData[removeData];
    sessionStorage.setItem("resultBtn", JSON.stringify(workspaceData))
}

function remove_group_result(removeData) {
    let workspaceData = JSON.parse(sessionStorage.getItem("resultBtn"));
    $.each(workspaceData, function (i) {
        if (workspaceData[i].group === removeData) {
            remove_single_result(i)
        }
    })
    document.getElementById(removeData).remove();
}

function remove_all_results() {
    let groupSet = new Set();
    /** remove button from portal **/
    $.each(JSON.parse(sessionStorage.getItem("resultBtn")), function (key, value) {
        groupSet.add(value.group)
        remove_single_result(key);
    });

    /** remove result data from session **/
    sessionStorage.removeItem("resultBtn");

    /** remove group buttons from portal **/
    groupSet.forEach(function (i) {
        document.getElementById(i).remove();
    })
}

/**
 * @param {json} item - input information loaded from Session Storage
 * @param {string} newNode - The new HTML Element where the checkbox will be added
 */
function build_modal_regexText(item, newNode) {
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
function build_modal_radio(item, newNode, option) {
    // let radioNode = document.createElement("p");
    let nodeText = document.createTextNode(" " + option + " ");
    let inElement = document.createElement("INPUT");
    inElement.type = "radio";
    // inElement.setAttribute("type", "radio");
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
function build_modal_checkbox(item, newNode, option) {
    // let radioNode = document.createElement("p");
    let nodeText = document.createTextNode(" " + option + " ");
    let inElement = document.createElement("input");
    inElement.type = "radio";
    // inElement.setAttribute("type", "radio");
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
function build_modal_dropdown(item, newNode, countDropDowns) {
    let htmlSelect = document.createElement("SELECT");
    let sessionStoreData = JSON.parse(sessionStorage.getItem("dataBtn"));
    let resultData = JSON.parse(sessionStorage.getItem("resultBtn"));
    let boxLen = 0;
    let aptStoreData = {};
    let aptResultData = {};
    let acceptedDataTypes = DATATYPE.accepts([item.keywords[0]])

    for (let i in sessionStoreData) if (acceptedDataTypes.has(sessionStoreData[i].type)) {
        aptStoreData[i] = sessionStoreData[i];
    }
    for (let i in resultData) if (acceptedDataTypes.has(resultData[i].type)) aptResultData[i] = resultData[i]
    // for (let i in sessionStoreData) if (item.keywords[0] == sessionStoreData[i].type) aptStoreData[i] = sessionStoreData[i];
    // for (let i in resultData) if (item.keywords[0] == resultData[i].type) aptResultData[i] = resultData[i]
    boxLen = Object.keys(aptResultData).length + Object.keys(aptStoreData).length;
    // if (item.minOccurs === 1) htmlSelect.required = true; // Why did I first use === 1 ???
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
            optionGroup = build_dropdown_opt(item, optionGroup, aptStoreData);
            htmlSelect.appendChild(optionGroup);
        }
        if (resultData !== null) {
            let optionGroup = document.createElement("OPTGROUP");
            optionGroup.label = "Result store";
            optionGroup = build_dropdown_opt(item, optionGroup, aptResultData);
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
function build_dropdown_opt(item, optionGroup, sidebarData) {
    // let opt = document.createElement("OPTION");
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
        // opt.setAttribute('data-datatype', sidebarData[singleData].type);
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
function build_modal(wpsInfo, service) {
    // let availableInputs = get_available_inputs();
    // let wpsInfo = get_wpsprocess(service, identifier);
    let sessionStoreData = JSON.parse(sessionStorage.getItem("dataBtn"));
    let resultData = JSON.parse(sessionStorage.getItem("resultBtn"));
    let element = document.getElementById("mod_head");
    let newElement = "";

    if (!sessionStoreData) {
        sessionStoreData = {}
    }
    if (!resultData) {
        resultData = {}
    }

    element.innerHTML = wpsInfo.title;
    element.dataset.service = service;
    element.dataset.process = wpsInfo.identifier;
    element = document.getElementById("mod_abs");
    if (wpsInfo.abstract) {
        newElement = wpsInfo.abstract;
        // } else {
        //     newElement = ""
    }
    element.innerHTML = newElement;

    /** inputs: **/
    // TODO: Is reuse of element in new context okay? Fix if not.
    element = document.getElementById("mod_in");
    element.innerHTML = "";
    let inElement = "", newNode = "", nodeText = "";
    let outElementIdList = [];
    let countDropDowns = 0;

    wpsInfo.dataInputs.forEach(function (item) {
        newNode = document.createElement("p");

        /** Set title of Input and set the 'required' flag if necessary **/
        let titleText = "";
        // if ('minOccurs' in item) {  // outer if seems to be unused
        if (item.minOccurs == 0) {
            titleText = " " + item.title + ": "
        } else if (item.defaultValue) {
            titleText = " " + item.title + ": "
        } else if (item.minOccurs > 0 && item.dataType != 'boolean') {
            titleText = " " + item.title + " (*) : ";
            inElement.required = true;
            // }
        } else {
            titleText = " " + item.title + ": "
        }

        // if (item.minOccurs === 1) inElement.required = true;
        nodeText = document.createTextNode(titleText);
        newNode.appendChild(nodeText);
        if ('allowedValues' in item && Array.isArray(item.allowedValues) && item.allowedValues.length > 1) {
            if ('maxOccurs' in item) {
                if (item.maxOccurs === 1) {
                    // nodeText = "";
                    item.allowedValues.forEach(function (option) {
                        build_modal_radio(item, newNode, option)
                    });
                }
            }
        } else if ('supportedValues' in item && Array.isArray(item.supportedValues) && item.supportedValues.length > 1) {
            if ('maxOccurs' in item) {
                if (item.maxOccurs === 1) {
                    // nodeText = "";
                    item.supportedValues.forEach(function (option) {
                        build_modal_radio(item, newNode, option)
                    });
                    // inElement.setAttribute("type", "radio")
                }
            }
        } else if ('keywords' in item && item.keywords.includes('pattern')) {
            build_modal_regexText(item, newNode)
        } else if ('keywords' in item) {
            countDropDowns = build_modal_dropdown(item, newNode, countDropDowns)

            /** Set input element according to dataType */
        } else {
            inElement = document.createElement("INPUT");
            inElement.id = item.identifier;
            inElement.name = item.identifier;
            inElement.setAttribute("list", item.identifier + '_list');

            if (item.minOccurs > 0 && item.dataType != 'boolean') inElement.required = true;
            switch (item.dataType) {
                case 'string':
                    inElement.type = "text";
                    //inElement.className = "input"
                    inElement.appendChild(set_textfield_opt(item, resultData, sessionStoreData))
                    if ('defaultValue' in item) {
                        inElement.value = item.defaultValue;
                    }
                    // if ('defaultValue' in item) inElement.value = item.defaultValue;
                    break;
                case 'boolean':
                    inElement.type = "checkbox";
                    if ('defaultValue' in item && item.defaultValue == true) inElement.checked = true;
                    break;
                case 'dateTime':
                    inElement.type = "datetime-local";
                    inElement.appendChild(set_textfield_opt(item, resultData, sessionStoreData))
                    if ('defaultValue' in item) inElement.value = item.defaultValue;
                    break;
                case 'float':
                    inElement.type = "number";
                    inElement.step = "0.000001";
                    inElement.appendChild(set_textfield_opt(item, resultData, sessionStoreData))
                    if ('defaultValue' in item) inElement.value = item.defaultValue;
                    break;
                case 'integer':
                    inElement.type = "number";
                    inElement.appendChild(set_textfield_opt(item, resultData, sessionStoreData))
                    if ('defaultValue' in item) inElement.value = item.defaultValue;
                    break;
                case 'positiveInteger':
                    inElement.type = "number";
                    inElement.min = "0";
                    inElement.appendChild(set_textfield_opt(item, resultData, sessionStoreData))
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
            } //else {inElement.required = false}
            newNode.appendChild(inElement);
        }
        if (typeof (newNode) === 'object') element.appendChild(newNode)
    });

    // TODO: build one output now. Decide how to handle several outputs
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
    // modal.setAttribute("name", invoke_btn_id);
    modal.setAttribute("name", wpsInfo.identifier);
    modal.style.display = "block";
    let currentModal = new modalObj(wpsInfo.identifier, outElementIdList);
    // TODO: get right name for sessionstorage
    // sessionStorage.setItem("currentModal", JSON.stringify(currentModal));
    // console.log('+++: ', JSON.stringify(modalObj))
}

/**
 * Create DATALIST to add a dropdown to a text box
 *
 * @param {object} item
 * @param {object} resultData
 * @param {object} sessionStoreData
 */
function set_textfield_opt(item, resultData, sessionStoreData) {
    let inDatalist = "";
    let type = item.dataType;
    inDatalist = document.createElement("DATALIST");
    inDatalist.setAttribute("id", item.identifier + '_list');
    let optElement = "";
    Object.entries(resultData).forEach(function (dataset) {
        if (dataset[1].type === type) {
            optElement = document.createElement("OPTION");
            optElement.setAttribute("value", dataset[1].outputs);
            optElement.innerText = dataset[1].name;
            inDatalist.appendChild(optElement);

        }
    })
    return inDatalist
}

function load_workflow() {
    alert("Load is not implemented yet.")
    console.log("load just a test workflow.")
    // let workflow
    // sessionStorage.setItem('workflow', JSON.stringify(workflow))
}

function save_workflow() {
    alert("Save is not implemented yet.")
    console.log("save isn't implemented yet: ",
        JSON.parse(document.getElementById('is_authenticated').value))
}

function run_workflow() {
    let workflow = JSON.parse(sessionStorage.getItem('workflow'))
    if (Object.keys(workflow).length <= 1) {
        alert(gettext("Please Load or Create a workflow to run first."))
        return;
    }
    let processList = [];
    let processDict = {};
    let processTree = {};
    let endNode = [];

    // get processes of workflow
    Object.entries(workflow).map(function (i) {
        if (i[1].source === 'toolbar') {
            // processList.push(i[0])
            processDict[i[0]] = {children: i[1].input_ids};
            processDict[i[0]].parents = i[1].output_ids;
            if (typeof i[1].output_ids === "undefined") {
                endNode.push(i[0])
            }
        }
    })
    if (endNode.length > 1) {
        alert(gettext("Your workflow is supposed to end in a single process."))
        return;
    }
    /**
     * create tree of processes
     * @param {string} ID
     * @param {dictionary} parent
     * @param {dictionary} processDict
     * @param {array} processList
     */
    function createTree(ID, parent, processDict, processList) {
        if (!processList.includes(ID)) {
            processList.push(ID);
        } else {
            // TODO: This results in an error anyways. Fix it!
            alert(gettext("At least one process is used more than once. This could result in an infinite loop and is forbidden (yet)."))
            console.warn('Please check box with id: ', ID)
        }
        let tree = {};
        for (let i of processDict[ID].children) {
            tree[i] = typeof processDict[i].children != "undefined" ? createTree(i, tree, processDict, processList) : {}
        }
        return tree;
    }
    processTree[endNode] = {};
    processTree[endNode] = createTree(endNode, processTree[endNode], processDict, processList);
    console.log('processTree: ', processTree)

    console.log("run isn't implemented yet.")
}

/**
 * Remove boxes from Dropzone, from Sessionstorage and set workflow name to default name.
 */
function clear_workflow() {
    canvas.clear();
    set_sessionStorage_workflow_name()
    document.getElementById("workflow_name").value = gettext('my workflow')
}
