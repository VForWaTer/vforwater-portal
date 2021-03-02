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
 * in- and outputs and so on of a tool are not loaded when page loads but on its first use and stored in
 * the sessionStorage for the next time the user wants to use this tool
 * @param {string} service - wps service as stored in database
 * @param {string} identifier - identifier of a wps process
 **/
function wpsprocess(service, identifier) {
    let tools = JSON.parse(sessionStorage.getItem('tools'))
    if (!tools) {
        tools = {}
    }
    if (!tools[service]) {
        tools[service] = {}
    }
    if (tools[service][identifier]) {
        build_modal(tools[service][identifier], service, identifier)
    } else {
        $.ajax({
            url: DEMO_VAR + "/workspace/processview",
            //url: DEMO_VAR+"/wps_gui/"+service+"/process",
            dataType: 'json',
            data: {
                processview: JSON.stringify({id: identifier, serv: service}),
                'csrfmiddlewaretoken': csrf_token,
            }, /** data sent with the post request **/
        })
            .done(function (json) {
                build_modal(json, service, identifier)
                tools[service][identifier] = json
                sessionStorage.setItem('tools', JSON.stringify(tools))
        })
            .fail(function (e) {
                console.log('Failed: ', e)
        });
    }
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
    let tools = JSON.parse(sessionStorage.getItem('tools'))
    if (!tools) {
        tools = {}
    }
    if (!tools[service]) {
        tools[service] = {}
    }
    if (tools[service][identifier]) {
        return tools[service][identifier]
    } else {
        $.ajax({
            url: DEMO_VAR + "/workspace/processview",
            //url: DEMO_VAR+"/wps_gui/"+service+"/process",
            dataType: 'json',
            data: {
                processview: JSON.stringify({id: identifier, serv: service}),
                'csrfmiddlewaretoken': csrf_token,
            }, // data sent with the post request
        })
            .done(function (json) {
                tools[service][identifier] = json
                sessionStorage.setItem('tools', JSON.stringify(tools))
                return json
        })
            .fail(function (e) {
                console.log('Failed: ', e)
        });
    }
}

function drop_and_save() {
    console.error('lets store it')
}

/**
 * Check if an input is required and if it is required check if the input has a value.
 *
 * @param {HTMLElement} checkElement Element to be checked if filled.
 */
function check_required(checkElement) {
    /** check if an Element of a wps is required **/
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

// TODO: runProcess now works only on execution from modal. Adjust to be usable from Dropzone too,
//  when you have the drop objects
// TODO: Improve code by using HTML Forms
function modal_run_process() {
    color_modal("dodgerblue");

    /** collect inputs **/
    var inKey = [];
    var inValue = [];
    var inType = [];
    let dDInput = 0;
    let inModal = document.getElementById('mod_in');
    let inputInputs = inModal.getElementsByTagName('input');
    let dropDInputs = inModal.getElementsByTagName('select');
    let valueList = [];
    let typeList = [];
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
            }
            inValue.push(valueList);
            inKey.push(dropDInputs[i].name);
            inType.push(typeList);

        /** else if one dropdowns **/
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
        }
    }
    for (let i = 0; i < inputInputs.length; i++) {
        if (inputInputs[i].type == "radio") {
            if (inputInputs[i].checked == true) {
                inKey.push(inputInputs[i].name);
                inValue.push(inputInputs[i].value);
                inType.push('string');
            }
        } else if (inputInputs[i].type == "checkbox") {
            inKey.push(inputInputs[i].name);
            if (inputInputs[i].checked == true) {
                inValue.push(true);
                inType.push('boolean');
            } else {
                inValue.push(false);
                inType.push('boolean');
            }
        } else {
            inKey.push(inputInputs[i].name);
            inValue.push(inputInputs[i].value);
            inType.push('');
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

    $.ajax({
        url: DEMO_VAR + "/workspace/processrun",
        data: {
            processrun: JSON.stringify({id: identifier, serv: wpsservice,
                key_list: inKey, value_list: inValue, type_list: inType}),
            'csrfmiddlewaretoken': csrf_token,
        }, /** data sent with the post request **/
    })
        .done(function (json) {  /** Results are stored in the sessionStorage **/
            if (json.execution_status == "ProcessSucceeded") {
                json.wps = identifier;
                json.inputs = {};
                let i = 0;
                $.each(inKey, function (key, value) {
                    json.inputs[value] = inValue[i];
                    i++;
                });
                color_modal("forestgreen");

                for (let i in json.result) {
                    let btnName = set_result_btn_name(outputName);
                    json.result[i].dropBtn.name = btnName;
                    let btnData = {
                        type: json.result[i].type,
                        wpsID: json.result[i].wpsID,
                        wps: json.wps,
                        inputs: json.inputs,
                        status: json.execution_status,
                        dropBtn: json.result[i].dropBtn
                    }
                    add_resultbtn_to_sessionstore(btnName, btnData);
                    document.getElementById("workspace_results").innerHTML += build_resultstore_button(btnName, btnData);
                }
            } else if (json.execution_status == "Exception") {
                console.error('error in wps process')
                color_modal("firebrick");
                // alert('Error: Failed to execute your request.');
            } else if (json.execution_status == "error in wps process") {
                color_modal("firebrick");
                console.error('Error in wps process: ', json.error)
                // alert('Error: Failed to execute your request.');
            } else if (json.execution_status == "auth_error") {
                color_modal("firebrick");
                /** Use Timeout to ensure color changed before popup appears **/
                setTimeout(function () {
                    alert('Error: You are not allowed to run this process. Please Contact your Admin.');
                }, 5);
                console.error('Maybe you have to log in to run processes. ', json.execution_status)
            }
        })
        .fail(function (json) {
            color_modal("firebrick");
            console.error('Error, No success: ', json)
    });
}

function run_wps(input_dict) {
    let modhead = document.getElementById('mod_head');
    let wpsservice = modhead.dataset.service;
    let identifier = modhead.dataset.process;
    // '2020-10-31T14:10'
    // fetch(GEO_SERVER + '/wfs/' + wfsLayerName + '/' + extent.join(',') + '/3857',
    //             // {body: {'csrfmiddlewaretoken': csrf_token},  body is only for post!
    //             // credentials: 'same-origin'}
    //             )
    //             .then(function (response) {
    //                 wfsPointSource.addFeatures(wfsPointSource.getFormat().readFeatures(response));
    //             })
    //             .catch(function (error) {
    //                 console.log('Error in building vector wfsPointSource: ', error);
    //                 wfsPointSource.removeLoadedExtent(extent);
    //             })
    $.ajax({
        url: DEMO_VAR + "/workspace/processrun",
        data: {
            processrun: JSON.stringify({id: identifier, serv: wpsservice,
                key_list: input_dict.keys(), value_list: input_dict.values()}),
            // processrun: JSON.stringify(input_dict),
            'csrfmiddlewaretoken': csrf_token,
        }, /** data sent with the post request **/
    })
        .done (function (json) {
            return json
        })
        .fail (function (json) {
            console.error('Error, No success: ', json)
            color_modal("firebrick");
        })
}

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

function color_modal(color) {
    let modalColor = document.getElementById("modal-header");
    modalColor.style.backgroundColor = color;
    modalColor = document.getElementById("modal-footer");
    modalColor.style.backgroundColor = color;
}

/** A Object with names and values from the input object / not used yet **/
function modalObj(processId, processInput, processOutput) {
    this.processId = processId;
    this.processInput = processInput;
    this.processOutput = processOutput;
}

function add_resultbtn_to_sessionstore(btnName, json) {
    let result_btns = {};
    if (sessionStorage.getItem("resultBtn")) {
        result_btns = JSON.parse(sessionStorage.getItem("resultBtn"));
        if (Object.keys(result_btns).includes(btnName)) {
            console.error('Error! Names should be unique! Problem with race conditions?')
        }
    }
    result_btns[btnName] = {
        type: json.type,
        wps: json.wps,
        inputs: json.inputs,
        wpsID: json.wpsID,
        status: json.execution_status,
        dropBtn: json.dropBtn
    };
    sessionStorage.setItem("resultBtn", JSON.stringify(result_btns));
}

//TODO: Urgent!!! Is it necessary that a result knows which function it came from and what the input parameters were?
/**
 * Build a button in the result store.
 * data-id is used to find results on server
 * id is used for the remove button
 * @param  {string} name name for the button
 * @param  {obj} json Object holding all necessary info about result
 * @return {string} HTML Code for the button
 **/
function build_resultstore_button(name, json) {
    let title = json.wps + "\n" + JSON.stringify(json.inputs).slice(1, -1).replace(/"/g, "'");
    return '<li draggable="true" ondragstart="dragstart_handler(event)" class="w3-padding task is-result" ' +
        'data-id="wps' + json.wpsID + '" btnName="' + name + '" onmouseover="" style="cursor:pointer;" ' +
        'id="' + name + '"><span class="w3-medium" title="' + title + '">' +
        '<div class="task__content">' + name + '</div><div class="task__actions"></div></span>' +
        '<span class="' + json['type'] + '"></span>' +
        '<a href="javascript:void(0)" onclick="remove_single_result(\'' + name + '\')" class="w3-hover-white">' +
        '<i class="fa fa-remove fa-fw"></i></a><br></li>';
}

function remove_single_result(removeData) {
    document.getElementById(removeData).remove();
    let workspaceData = JSON.parse(sessionStorage.getItem("resultBtn"));
    delete workspaceData[removeData];
    sessionStorage.setItem("resultBtn", JSON.stringify(workspaceData))
}

function remove_all_results() {
    /** remove button from portal **/
    $.each(JSON.parse(sessionStorage.getItem("resultBtn")), function (key) {
        remove_single_result(key);
    });

    /** remove button from session **/
    sessionStorage.removeItem("resultBtn");
}

function build_modal_radio(item, newNode, option) {
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
        htmlSelect.size = (boxLen > 3) ? "5":(boxLen + 2).toString();
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

function build_modal(wpsInfo, service, identifier) {
    // let availableInputs = get_available_inputs();
    let element = document.getElementById("mod_head");
    let newElement = "";
    element.innerHTML = wpsInfo.title;
    element.dataset.service = service;
    element.dataset.process = identifier;
    element = document.getElementById("mod_abs");
    if (wpsInfo.abstract) {
        newElement = wpsInfo.abstract;
    } else {
        newElement = ""
    }

    element.innerHTML = newElement;

    /** inputs: **/
    document.getElementById("mod_in").innerHTML = "";
    let inElement = "", newNode = "", nodeText = "";
    let outElementIdList = [];
    let countDropDowns = 0;

    wpsInfo.dataInputs.forEach(function (item) {
        element = document.getElementById("mod_in");
        newNode = document.createElement("p");

        /** Set title of Input and set the 'required' flag if necessary **/
        let titleText = "";
        if ('minOccurs' in item) {
            if (item.minOccurs == 0) {
                titleText = " " + item.title + ": "
            } else if (item.defaultValue) {
                titleText = " " + item.title + ": "
            } else if (item.minOccurs > 0 && item.dataType != 'boolean') {
                titleText = " " + item.title + " (*) : ";
                inElement.required = true;
            }
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
        } else if ('keywords' in item) {
            countDropDowns = build_modal_dropdown(item, newNode, countDropDowns)
        } else {
            inElement = document.createElement("input");
            inElement.id = item.identifier;
            inElement.name = item.identifier;
            if (item.minOccurs > 0 && item.dataType != 'boolean') inElement.required = true;
            switch (item.dataType) {
                case 'string':
                    inElement.type = "text";
                    //inElement.className = "input"
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
                    if ('defaultValue' in item) inElement.value = item.defaultValue;
                    break;
                case 'float':
                    inElement.type = "number";
                    inElement.step = "0.000001";
                    if ('defaultValue' in item) inElement.value = item.defaultValue;
                    break;
                case 'integer':
                    inElement.type = "number";
                    if ('defaultValue' in item) inElement.value = item.defaultValue;
                    break;
                case 'positiveInteger':
                    inElement.type = "number";
                    inElement.min = "0";
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
    modal.setAttribute("name", identifier);
    modal.style.display = "block";
    let currentModal = new modalObj(identifier, outElementIdList);
    // TODO: get right name for sessionstorage
    // sessionStorage.setItem("currentModal", JSON.stringify(currentModal));
    // console.log('+++: ', JSON.stringify(modalObj))
}

function load_workflow() {
    console.log("load isn't implemented yet.")
    console.log("load just a test workflow.")
    let workflow
    sessionStorage.setItem('workflow', JSON.stringify(workflow))
}

function save_workflow() {
    console.log("save isn't implemented yet: ",
        JSON.parse(document.getElementById('is_authenticated').value))
}

function run_workflow() {
    console.log("run isn't implemented yet.")
}

function clear_workflow() {
    console.log("clear isn't implemented yet.")
}
