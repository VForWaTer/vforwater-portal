function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text/html", ev.target.id);
}

function drop(ev) {
    ev.preventDefault();
    let droplet = ev.dataTransfer.getData("text/html");
    console.log('ev: ', ev)
    console.log('drop: ', droplet)

    // let droplet = document.createElement('canvas');
    // let dropletCopy = document.createElement('canvas');
    let dropletCopy = document.getElementById(droplet).cloneNode(true);
    // build new id for new element:
    if (sessionStorage.getItem("dz_count")) {
        sessionStorage.setItem("dz_count", JSON.parse(sessionStorage.getItem("dz_count")) + 1)
    } else {
        sessionStorage.setItem("dz_count", 1)
    }
    console.log('sessionStorage: ', sessionStorage.getItem("dz_count"))
    dropletCopy.id = "dz" + sessionStorage.getItem("dz_count");
    dropletCopy.classList.add('tool-btn');
    dropletCopy.style.left = ev.offsetX + "px";
    dropletCopy.style.top = ev.offsetY + "px";
    console.log('Copy: ', dropletCopy)
    // ev.dataTransfer.setDragImage(dropletCopy, ev.offsetX + "px", ev.offsetY + "px")
    ev.target.appendChild(dropletCopy);
    console.log('ev: ', ev)
}

// TODO: btn_id is not used yet, though it is needed to decide if an element has to be placed in the Dropozone on save:
//  if process_id == btn_id place btn in dropzone (on save)
function open_wpsprocess(service, process_id, btn_id) {
    wpsprocess(service, process_id, btn_id);
    /*
        let btn = document.getElementById(btn_id);
        console.log("btn: ", btn)
        console.log('data service: ', btn.dataset.service)
        console.log('data process: ', btn.dataset.process)
    */

    //let modal = document.getElementById("workModal");
    //modal.style.display = "block";
    console.log("service: ", service)
    console.log("identifier: ", process_id)
    console.log("btn_id: ", btn_id)
}

function wpsprocess(service, identifier, btn_id) {
    $.ajax({
        url: DEMO_VAR + "/wps_gui/processview",
        //url: DEMO_VAR+"/wps_gui/"+service+"/process",
        dataType: 'json',
        data: {
            processview: JSON.stringify({id: identifier, serv: service}),
            'csrfmiddlewaretoken': csrf_token,
        }, // data sent with the post request
        success: function (json) {
            build_modal(json, service, identifier, btn_id)
        },
    });
}

function dropAndSave() {
    console.log('lets store it')
}

function checkRequired(checkElement) {
    console.log('required: ', checkElement)
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
            console.log('requiredList[i].value: ', requiredList[i].value)
            if (!requiredList[i].value) {
                alert("Please fill all required fields that are marked with (*).");
                passed = false;
                break
            }
        }
    }
    return passed
}

// TODO: runProcess now works only on execution from modal. Ajdust to be usable from Dropzone too,
//  when you have the drop objects
function runProcess() {
    let inModal = document.getElementById('mod_in');
    let inputs = inModal.getElementsByTagName('input');
    console.log('+ inputs: ', inputs)
    var i;
    // var inDict = {};
    var inKey = [];
    var inValue = [];
    let loopLength = inputs.length;
    for (i = 0; i < loopLength; i++) {
        if (inputs[i].type == "radio") {
            if (inputs[i].checked == true) {
                // inDict[inputs[i].name] = inputs[i].value;
                inKey.push(inputs[i].name);
                inValue.push(inputs[i].value);
            }
        } else {
            // inDict[inputs[i].name] = inputs[i].value;
            inKey.push(inputs[i].name);
            inValue.push(inputs[i].value);
        }
    }
    let outModal = document.getElementById('mod_out');
    let outputs = outModal.getElementsByTagName('output');
    let outDict = {};
    loopLength = outputs.length;
    for (i = 0; i < loopLength; i++) {
        if (outputs[i].type == "radio") {
            if (outputs[i].checked == true) {
                outDict [outputs[i].name] = outputs[i].value;
            }
        } else {
            outDict [outputs[i].name] = outputs[i].value;
        }
    }

    let modhead = document.getElementById('mod_head');
    let wpsservice = modhead.dataset.service;
    let identifier = modhead.dataset.process;
    console.log('--- outDict : ', outDict)
    $.ajax({
        url: DEMO_VAR + "/wps_gui/processview",
        dataType: 'json',
        data: {
            processrun: JSON.stringify({id: identifier, serv: wpsservice, key_list: inKey, value_list: inValue}),
            'csrfmiddlewaretoken': csrf_token,
        }, // data sent with the post request
        success: function (json) {
            console.log(' + + + + ')
            console.log(' result: ', json)
            console.log(' result: ', json.execution_status)
            // build_modal(json, service, identifier, btn_id)
            // sessionStorage.removeItem("resultBtnList")
            if (json.execution_status == "ProcessSucceeded") {
                if (sessionStorage.getItem("resultBtnList")) {
                    let result_btns = JSON.parse(sessionStorage.getItem("resultBtnList"));
                    if (result_btns.includes(identifier)) {

                        console.log('---------- gibts schon: ', result_btns)
                    } else {
                        result_btns.push(identifier);
                        sessionStorage.setItem("resultBtnList", JSON.stringify(result_btns));
                        buildResultStoreButton(json);
                    }
                    // sessionStorage.setItem("resultBtnList", JSON.stringify(stored))
                } else {
                    sessionStorage.setItem("resultBtnList", JSON.stringify([identifier]));
                    buildResultStoreButton(json);
                }
            } else {
                alert('Error: Failed to execute your request.');
                console.log(json)
            }
        }
    });

}

// A Object with names and values from the input object
function modalObj(processId, processInput, processOutput) {
    this.processId = processId;
    this.processInput = processInput;
    this.processOutput = processOutput;
}

function buildResultStoreButton(json) {
    let ident = json.processid;
    console.log('ident: ', ident)
    let btnName = json.processid;
    let title = json.processid;
    console.log('workspace: ', document.getElementById("workspace_results"))
    document.getElementById("workspace_results").innerHTML += '<li draggable="true" class="respo-padding task" ' +
        'data-id="' + ident + '" btnName="' + btnName + '" onmouseover="" style="cursor:pointer;" id="' + ident + '">' +
        '<span class="respo-medium" title="' + title + '"><div class="task__content">' + btnName + '</div>' +
        '<div class="task__actions"></div></span><a href="javascript:void(0)"' +
        'onclick="remove_single_result(\'' + ident + '\')"; class="respo-hover-white respo-right">' +
        '<i class="fa fa-remove fa-fw"></i></a><br></li>';
}

function build_modal(wpsInfo, service, identifier, btn_id) {
    // sessionStorage.setItem("processModal", wpsInfo);
    // console.log(' wpsInfo: ', wpsInfo)
    // console.log(' btn_id: ', btn_id)
    // console.log('wpsInfo[title]: ', wpsInfo[title])
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
            if (item.minOccurs > 0) {
                titleText = " " + item.title + " (*) : "
            } else {
                titleText = " " + item.title + ": "
            }
        }
        if (item.minOccurs === 1) {
            inElement.required = true;
        }
        nodeText = document.createTextNode(titleText);
        newNode.appendChild(nodeText);
        if ('allowedValues' in item && Array.isArray(item.allowedValues) && item.allowedValues.length > 1) {
            if ('maxOccurs' in item) {
                if (item.maxOccurs === 1) {
                    let radioNode = "";
                    nodeText = "";
                    item.allowedValues.forEach(function (option) {
                        radioNode = document.createElement("p");
                        nodeText = document.createTextNode(" " + option + " ");
                        inElement = document.createElement("input");
                        inElement.type = "radio";
                        // inElement.setAttribute("type", "radio");
                        inElement.value = option;
                        inElement.id = item.identifier;
                        inElementIdList.push(item.identifier);
                        if (item.minOccurs === 1) {
                            inElement.required = true;
                        }

                        inElement.name = item.identifier;
                        if ('defaultValue' in item) {
                            if (item.defaultValue == option) {
                                inElement.checked = true;
                            }
                        }
                        newNode.appendChild(inElement);
                        newNode.appendChild(nodeText);
                    });
                }
            }
        } else if ('supportedValues' in item && Array.isArray(item.supportedValues) && item.supportedValues.length > 1) {
            if ('maxOccurs' in item) {
                if (item.maxOccurs === 1) {
                    let radioNode = "";
                    nodeText = "";
                    item.supportedValues.forEach(function (option) {
                        radioNode = document.createElement("p");
                        nodeText = document.createTextNode(" " + option + " ");
                        inElement = document.createElement("input");
                        inElement.type = "radio";
                        // inElement.setAttribute("type", "radio");
                        inElement.value = option;
                        inElement.id = item.identifier;
                        inElementIdList.push(item.identifier);
                        inElement.name = item.identifier;
                        if (item.minOccurs === 1) {
                            inElement.required = true;
                        }
                        if ('defaultValue' in item) {
                            if (item.defaultValue == option) {
                                inElement.checked = true;
                            }
                        }
                        newNode.appendChild(inElement);
                        newNode.appendChild(nodeText);
                    });
                    // inElement.setAttribute("type", "radio")
                }
            }
        } else {
            inElement = document.createElement("input");
            inElement.id = item.identifier;
            inElementIdList.push(item.identifier);
            inElement.name = item.identifier;
            if (item.minOccurs === 1) {
                inElement.required = true;
            }
            switch (item.dataType) {
                case 'string':
                    inElement.type = "text";
                    //inElement.className = "input"
                    if ('defaultValue' in item) {
                        inElement.value = item.defaultValue;
                    }
                    break;
                case 'boolean':
                    inElement.type = "checkbox";
                    if ('defaultValue' in item && item.defaultValue == true) {
                        inElement.checked = true;
                    }
                    break;
                case 'float':
                    inElement.type = "number";
                    inElement.step = "0.000001";
                    if ('defaultValue' in item) {
                        inElement.value = item.defaultValue;
                    }
                    break;
                case 'integer':
                    inElement.type = "number";
                    if ('defaultValue' in item) {
                        inElement.value = item.defaultValue;
                    }
                    break;
                case 'ComplexData':
                    inElement.type = "text";
                    console.log('you have to handle complesdata properly');
                    if ('defaultValue' in item) {
                        if ('mimeType' in item.defaultValue) {
                            inElement.value = item.defaultValue.mimeType;
                        }
                    }
                    break;
                case 'BoundingBoxData':
                    console.log('you have to handle BoundingBoxData properly');
                    if ('defaultValue' in item) {
                        inElement.value = item.defaultValue;
                    }
                    break;
                default:
                    console.log('+++++++++++++++++++++++')
                    console.log(' new dataType')
            }
            if (item.minOccurs > 0) {
                inElement.required = true
            } //else {inElement.required = false}
            newNode.appendChild(inElement);
        }
        //$("p").append("<b>Appended text</b>");
        //$("div").append(inElement);
        if (typeof (newNode) === 'object') {
            element.appendChild(newNode)
        }
    });

    // TODO: build one output now. Decide how to handle several outputs
    console.log('seesionStorage: ', sessionStorage.getItem("processModal"))
    //outputs:
    console.log('outputs: ', wpsInfo.processOutputs)
    console.log('outputs: ', wpsInfo.processOutputs.length)
    console.log('outputs: ', wpsInfo.processOutputs[0])
    document.getElementById("mod_out").innerHTML = "";

    element = document.getElementById("mod_out");

    nodeText = document.createElement("p");
    nodeText.appendChild(document.createTextNode(" Name for output in data store: "));

    newNode = document.createElement("div");
    newNode.appendChild(nodeText);
    let outElement = document.createElement("input");
    newNode.appendChild(outElement);
    if (typeof (newNode) === 'object') {
        element.appendChild(newNode)
    }
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
    modal.style.display = "block";
    let currentModal = new modalObj(identifier, inElementIdList, outElementIdList);
    // TODO: get right name for sessionstorage
    // sessionStorage.setItem("currentModal", JSON.stringify(currentModal));
    // console.log('+++: ', JSON.stringify(modalObj))

    // element.innerHTML = wpsInfo.title;
}

/*
function drop(ev) {
  ev.preventDefault();
  var data=ev.dataTransfer.getData("text/html");
  /!* If you use DOM manipulation functions, their default behaviour it not to
     copy but to alter and move elements. By appending a ".cloneNode(true)",
     you will not move the original element, but create a copy. *!/
  var nodeCopy = document.getElementById(data).cloneNode(true);
  nodeCopy.id = "newId"; /!* We cannot use the same ID *!/
  ev.target.appendChild(nodeCopy);
}*/
