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
function wpsprocess(service, identifier, invoke_btn_id) {
    $.ajax({
        url: DEMO_VAR + "/wps_gui/processview",
        //url: DEMO_VAR+"/wps_gui/"+service+"/process",
        dataType: 'json',
        data: {
            processview: JSON.stringify({id: identifier, serv: service}),
            'csrfmiddlewaretoken': csrf_token,
        }, // data sent with the post request
        success: function (json) {
            build_modal(json, service, identifier, invoke_btn_id)
        },
    });
}

function drop_and_save() {
    console.exception('lets store it')
}

function check_required(checkElement) {
    // check if an Element of a wps is required
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
function modal_run_process() {
    color_modal("dodgerblue");
    var inKey = [];
    var inValue = [];
    // let workModal = document.getElementById('workModal');
    let inModal = document.getElementById('mod_in');
    let radioInputs = inModal.getElementsByTagName('input');
    let dropDInputs = inModal.getElementsByTagName('select');

    for (let i = 0; i < dropDInputs.length; i++) {
        for (let j = 0; j < dropDInputs[i].length; j++) {
            if (dropDInputs[i][j].selected) {
                inKey.push(dropDInputs[i].name);
                inValue.push(dropDInputs[i][j].value);
            }
        }
    }

    for (let i = 0; i < radioInputs.length; i++) {
        if (radioInputs[i].type == "radio") {
            if (radioInputs[i].checked == true) {
                // inDict[inputs[i].name] = inputs[i].value;
                inKey.push(radioInputs[i].name);
                inValue.push(radioInputs[i].value);
            }
        } else {
            // inDict[inputs[i].name] = inputs[i].value;
            inKey.push(radioInputs[i].name);
            inValue.push(radioInputs[i].value);
        }
    }

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
        url: DEMO_VAR + "/wps_gui/processview",
        data: {
            processrun: JSON.stringify({id: identifier, serv: wpsservice, key_list: inKey, value_list: inValue}),
            'csrfmiddlewaretoken': csrf_token,
        }, // data sent with the post request
        success: function (json) { // Results are stored in the sessionStorage
            if (json.execution_status == "ProcessSucceeded") {
                json.wps = identifier;
                json.inputs = {};
                $.each(inKey, function (key, value){ json.inputs[value] = inValue;});
                color_modal("forestgreen");
                let btnName = set_result_btn_name(outputName);
                add_resultbtn_to_sessionstore(btnName, json);
                document.getElementById("workspace_results").innerHTML += build_resultstore_button(btnName, json);
            } else if (json.execution_status == "Exception") {
                color_modal("firebrick");
                // alert('Error: Failed to execute your request.');
            } else if (json.execution_status == "auth_error") {
                color_modal("firebrick");
                // Use Timeout to ensure color changed before popup appears
                setTimeout(function () {
                    alert('Error: You are not allowed to run this process. Please Contact your Admin.');
                }, 5);
                console.log('Maybe you have to log in to run processes. ', json.execution_status)
            }
        },
        error: function (json) {
            color_modal("firebrick");
            console.log('Error: ', json)
        }
    });
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

// A Object with names and values from the input object / not used yet
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
    result_btns[btnName] = {type: json.type, wps: json.wps, inputs: json.inputs, wpsid: json.wpsid, status: json.execution_status};
    sessionStorage.setItem("resultBtn", JSON.stringify(result_btns));
}

//TODO: Urgent!!! Is it necessary that a result knows which function it came from and what the input parameters were?
function build_resultstore_button(name, json) {
    let title = json.wps + "\n" + JSON.stringify(json.inputs).slice(1, -1).replace(/"/g, "'");
    return '<li draggable="true" class="respo-padding task is-result" ' +
        'data-id="' + name + '" btnName="' + name + '" onmouseover="" style="cursor:pointer;" id="id' + name + '">' +
        '<span class="respo-medium" title="' + title + '"><div class="task__content">' + name + '</div>' +
        '<div class="task__actions"></div></span>' +
        '<span class="'+json['type']+'"></span>' +
        '<a href="javascript:void(0)"' +
        'onclick="remove_single_result(\'' + name + '\')" class="respo-hover-white">' +
        '<i class="fa fa-remove fa-fw"></i></a><br></li>';
}


function remove_single_result(removeData) {
    document.getElementById("id" + removeData).remove();
    let workspaceData = JSON.parse(sessionStorage.getItem("resultBtn"));
    delete workspaceData[removeData];
    sessionStorage.setItem("resultBtn", JSON.stringify(workspaceData))
}

function remove_all_results() {
    // remove button from portal
    $.each(JSON.parse(sessionStorage.getItem("resultBtn")), function (key) { remove_single_result(key); });
    // remove button from session
    sessionStorage.removeItem("resultBtn");
}

// function remove_all_results() {
//     let workspaceData = JSON.parse(sessionStorage.getItem("resultBtnList"));
//     for (let i in workspaceData) {
//         sessionStorage.removeItem('"' + workspaceData[i] + '"');
//         document.getElementById(workspaceData[i]).remove();
//     }
//     sessionStorage.removeItem("resultBtnList");
// }

function build_modal_radio(inElementIdList, item, newNode, option) {
    // let radioNode = document.createElement("p");
    let nodeText = document.createTextNode(" " + option + " ");
    let inElement = document.createElement("input");
    inElement.type = "radio";
    // inElement.setAttribute("type", "radio");
    inElement.value = option;
    inElement.id = item.identifier;
    inElementIdList.push(item.identifier);
    if (item.minOccurs === 1) inElement.required = true;

    inElement.name = item.identifier;
    if ('defaultValue' in item) {
        if (item.defaultValue == option) inElement.checked = true;
    }
    newNode.appendChild(inElement);
    newNode.appendChild(nodeText);
}

function build_modal_dropdown(inElementIdList, item, newNode) {
    let htmlSelect = document.createElement("SELECT");
    let storeData = JSON.parse(sessionStorage.getItem("dataBtn"));
    if (storeData !== null) {
        let opt = document.createElement("OPTION");
        if (item.minOccurs === 1) htmlSelect.required = true;
        if (item.maxOccurs > 1) htmlSelect.multiple = true;
        htmlSelect.size = "3";
        htmlSelect.name = item.identifier;
        let optionGroup = document.createElement("OPTGROUP");
        optionGroup.label = "Data store";
        item.keywords.forEach(function (option) {
            Object.keys(storeData).forEach(function (singleData) {
                console.log('storeData[singleData].type: ', storeData[singleData].type)
                console.log('option: ', option)
                if (storeData[singleData].type.includes(option)) {
                    opt.innerText = `${singleData} ${storeData[singleData].name} (${storeData[singleData].abbr} in ${storeData[singleData].unit})`;
                    opt.value = singleData;
                    if (item.keywords.length == 1) opt.selected = true;
                    optionGroup.appendChild(opt);
                    opt = document.createElement("OPTION");
                }
            })
        });
        htmlSelect.appendChild(optionGroup);
    } else {
        htmlSelect = document.createElement("DIV");
        if (item.minOccurs === 1) htmlSelect.required = true;
        if (item.defaultValue) {
            htmlSelect.innerText = 'Without selected datasets the default ' + item.defaultValue + ' value is used.'
        } else {
            htmlSelect.innerText = 'Please first select a dataset from the filter menu.'
        }
    }
    newNode.appendChild(htmlSelect);
}

function get_available_inputs() {
    let available_elements = {};
    available_elements['workspace'] = document.getElementById('workspace').getElementsByClassName('task');
    available_elements['results'] = document.getElementById('workspace_results').getElementsByClassName('task');
    available_elements['toolbar'] = document.getElementById('toolbar').getElementsByClassName('process');
    Object.keys(available_elements).forEach(function (key) {
        if (available_elements[key].length == 0) delete available_elements[key]
    });
    // console.log('available_elements: ', available_elements);
    return available_elements
}

function build_modal(wpsInfo, service, identifier, invoke_btn_id) {
    // console.log('wpsInfo: ', wpsInfo)
    let availableInputs = get_available_inputs();
    // console.log('availableInputs: ', availableInputs)
    // sessionStorage.setItem("processModal", wpsInfo);
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
    //inputs:
    document.getElementById("mod_in").innerHTML = "";
    let inElement = "", newNode = "", nodeText = "";
    let outElementIdList = [], inElementIdList = [];

    wpsInfo.dataInputs.forEach(function (item) {
        element = document.getElementById("mod_in");
        newNode = document.createElement("p");
        let titleText = "";
        if ('minOccurs' in item) {
            if (item.minOccurs > 0 && item.dataType != 'boolean') {
                titleText = " " + item.title + " (*) : ";
                inElement.required = true;
            } else {
                titleText = " " + item.title + ": "
            }
        }
        // if (item.minOccurs === 1) inElement.required = true;
        nodeText = document.createTextNode(titleText);
        newNode.appendChild(nodeText);
        if ('allowedValues' in item && Array.isArray(item.allowedValues) && item.allowedValues.length > 1) {
            if ('maxOccurs' in item) {
                if (item.maxOccurs === 1) {
                    // nodeText = "";
                    item.allowedValues.forEach(function (option) {
                        build_modal_radio(inElementIdList, item, newNode, option)
                    });
                }
            }
        } else if ('supportedValues' in item && Array.isArray(item.supportedValues) && item.supportedValues.length > 1) {
            if ('maxOccurs' in item) {
                if (item.maxOccurs === 1) {
                    // nodeText = "";
                    item.supportedValues.forEach(function (option) {
                        build_modal_radio(inElementIdList, item, newNode, option)
                    });
                    // inElement.setAttribute("type", "radio")
                }
            }
        } else if ('keywords' in item) {
            build_modal_dropdown(inElementIdList, item, newNode)
        } else {
            inElement = document.createElement("input");
            inElement.id = item.identifier;
            inElementIdList.push(item.identifier);
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
                case 'float':
                    inElement.type = "number";
                    inElement.step = "0.000001";
                    if ('defaultValue' in item) inElement.value = item.defaultValue;
                    break;
                case 'integer':
                    inElement.type = "number";
                    if ('defaultValue' in item) inElement.value = item.defaultValue;
                    break;
                case 'ComplexData':
                    inElement.type = "text";
                    if ('defaultValue' in item) {
                        if ('mimeType' in item.defaultValue) inElement.value = item.defaultValue.mimeType;
                    }
                    break;
                case 'BoundingBoxData':
                    console.exception('you have to handle BoundingBoxData properly');
                    if ('defaultValue' in item) inElement.value = item.defaultValue;
                    break;
                default:
                    console.exception(' new dataType')
            }
            if (item.minOccurs > 0) {
                inElement.required = true
            } //else {inElement.required = false}
            newNode.appendChild(inElement);
        }
        //$("p").append("<b>Appended text</b>");
        //$("div").append(inElement);
        if (typeof (newNode) === 'object') element.appendChild(newNode)
    });

    // TODO: build one output now. Decide how to handle several outputs
    //outputs:
    document.getElementById("mod_out").innerHTML = "";

    element = document.getElementById("mod_out");

    nodeText = document.createElement("p");
    nodeText.appendChild(document.createTextNode(" Name for output in data store: "));

    newNode = document.createElement("div");
    newNode.appendChild(nodeText);
    let outElement = document.createElement("input");
    newNode.appendChild(outElement);
    if (typeof (newNode) === 'object') element.appendChild(newNode);
    /*let outElement = "";
    newNode = "";
    nodeText = "";

    wpsInfo.processOutputs.forEach(function (item) {
        element = document.getElementById("mod_out");

        nodeText = document.createElement("p");
        nodeText.appendChild(document.createTextNode(" Name for " + item.title + ": "));

        newNode = document.createElement("div");
        newNode.appendChild(nodeText);


        outElement = document.createElement("input");
        // inElement.className = "input";
        outElement.id = item.identifier;
        outElementIdList.push(item.identifier);
        outElement.name = item.identifier;
        outElement.type = "text";
        outElement.value = item.identifier;
        newNode.appendChild(outElement);

        nodeText = document.createElement("p");
        let mimeText = "";
        if (item.defaultValue && item.defaultValue.mimeType) {
            mimeText = " (" + item.defaultValue.mimeType + ")"
        }
        nodeText.appendChild(document.createTextNode(" Type of Output: " + item.dataType + mimeText));
        newNode.appendChild(nodeText);
        //$("div").append(inElement);
        if (typeof (newNode) === 'object') {
            element.appendChild(newNode)
        }
    });*/

    //element.innerHTML = inElement;
    let modal = document.getElementById("workModal");
    modal.setAttribute("name", invoke_btn_id);
    modal.style.display = "block";
    let currentModal = new modalObj(identifier, inElementIdList, outElementIdList);
    // TODO: get right name for sessionstorage
    // sessionStorage.setItem("currentModal", JSON.stringify(currentModal));
    // console.log('+++: ', JSON.stringify(modalObj))

    // element.innerHTML = wpsInfo.title;
}
