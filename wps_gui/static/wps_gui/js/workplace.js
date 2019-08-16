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
        outputName = identifier;
    } else {
        outputName = outputs[0].value;
    }
    $.ajax({
        url: DEMO_VAR + "/wps_gui/processview",
        dataType: 'json',
        data: {
            processrun: JSON.stringify({id: identifier, serv: wpsservice, key_list: inKey, value_list: inValue}),
            'csrfmiddlewaretoken': csrf_token,
        }, // data sent with the post request
        success: function (json) { // Results are stored in the sessionStorage
            if (json.execution_status == "ProcessSucceeded") {
                color_modal("forestgreen");
                let btnName = set_result_btn_name(outputName);
                sessionStorage.setItem(btnName, JSON.stringify(json));
                add_to_resultstore_buttonlist(btnName);
                document.getElementById("workspace_results").innerHTML += build_resultstore_button(btnName, json);
            } else {
                color_modal("firebrick");
                alert('Error: Failed to execute your request.');
            }
        }
    });
}

function set_result_btn_name(name) {
    let newName;
    if (sessionStorage.getItem("resultBtnList")) {
        let result_btns = JSON.parse(sessionStorage.getItem("resultBtnList"));
        newName = name;
        if (result_btns.includes(name)) {
            var i = 0;
            while (result_btns.includes(newName)) {
                i++;
                newName = name + i
            }
        }
        result_btns.push(newName);
    } else {
        newName = [name];
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

function add_to_resultstore_buttonlist(btnName) {
    if (sessionStorage.getItem("resultBtnList")) {

        let result_btns = JSON.parse(sessionStorage.getItem("resultBtnList"));
        if (result_btns.includes(btnName)) {
            console.error('Error! Names should be unique!')
        }
        result_btns.push(btnName);
        // }
        sessionStorage.setItem("resultBtnList", JSON.stringify(result_btns));
    } else {
        sessionStorage.setItem("resultBtnList", JSON.stringify(btnName));
    }
    // return newBtnName;
}

//TODO: Urgent!!! Is it necessary that a result knows which function it came from and what the input parameters were?
function build_resultstore_button(btnName, json) {
    // let ident = json.processid;
    let title = json.processid;
    return '<li draggable="true" class="respo-padding task is-result" ' +
        'data-id="' + btnName + '" btnName="' + btnName + '" onmouseover="" style="cursor:pointer;" id="' + btnName + '">' +
        '<span class="respo-medium" title="' + title + '"><div class="task__content">' + btnName + '</div>' +
        '<div class="task__actions"></div></span>' +
        // '<span class="'+value['type']+'"></span>' +
        '<a href="javascript:void(0)"' +
        'onclick="remove_single_result(\'' + btnName + '\')" class="respo-hover-white">' +
        '<i class="fa fa-remove fa-fw"></i></a><br></li>';
}

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
    let storeData = JSON.parse(sessionStorage.getItem("dataBtn"));
    let opt = document.createElement("OPTION");
    let htmlSelect = document.createElement("SELECT");
    if (item.minOccurs === 1) htmlSelect.required = true;
    if (item.maxOccurs > 1) htmlSelect.multiple = true;
    htmlSelect.size = "3";
    htmlSelect.name = item.identifier;
    let optionGroup = document.createElement("OPTGROUP");
    optionGroup.label = "Data store";
    item.keywords.forEach(function (option) {
        Object.keys(storeData).forEach(function (singleData) {
            if (option == storeData[singleData].type) {
                opt.innerText = `${singleData} ${storeData[singleData].name} (${storeData[singleData].abbr} in ${storeData[singleData].unit})`;
                opt.value = singleData;
                optionGroup.appendChild(opt)
                opt = document.createElement("OPTION");
                }
            })
        });
    htmlSelect.appendChild(optionGroup);
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
                titleText = " " + item.title + " (*) : "
            } else {
                titleText = " " + item.title + ": "
            }
        }
        if (item.minOccurs === 1) inElement.required = true;
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
    if (typeof (newNode) === 'object') element.appendChild(newNode)
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
