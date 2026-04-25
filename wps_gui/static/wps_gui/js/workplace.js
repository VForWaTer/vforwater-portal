/*
 * Project Name: V-FOR-WaTer
 * Author: Marcus Strobl
 * Contributors:
 * License: MIT License
 */

// TODO: box_types aren't used anymore, though one has to make sure there is no problem now with 2darray
// vfw.var.box_types = ['array', 'iarray', 'varray', 'ndarray', '_2darray',
//     'timeseries', 'vtimeseries', 'raster', 'vraster', 'idataframe', 'vdataframe',
//     'time-dataframe', 'vtime-dataframe', 'html', 'plot', 'figure', 'image']

// function allowDrop(ev) {
//     ev.preventDefault();
// }

// function drag(ev) {
//     ev.dataTransfer.setData("text/html", ev.target.id);
// }

// function drop(ev) {
//     console.log('_______ I dropped something')
//     ev.preventDefault();
//     let droplet = ev.dataTransfer.getData("text/html");
//
//     // let droplet = document.createElement('canvas');
//     // let dropletCopy = document.createElement('canvas');
//     let dropletCopy = document.getElementById(droplet).cloneNode(true);
//     // build new id for new element:
//     if (sessionStorage.getItem("dz_count")) {
//         sessionStorage.setItem("dz_count", JSON.parse(sessionStorage.getItem("dz_count")) + 1)
//     } else {
//         sessionStorage.setItem("dz_count", 1)
//     }
//     dropletCopy.id = "dz" + sessionStorage.getItem("dz_count");
//     dropletCopy.classList.add('tool-btn');
//     dropletCopy.style.left = ev.offsetX + "px";
//     dropletCopy.style.top = ev.offsetY + "px";
//     // ev.dataTransfer.setDragImage(dropletCopy, ev.offsetX + "px", ev.offsetY + "px")
//     ev.target.appendChild(dropletCopy);
// }

// TODO: btn_id is not used yet, though it is needed to decide if an element has to be placed in the Dropozone on save:
//  if process_id == btn_id place btn in dropzone (on save)
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
    // if (!vfw.obj.workModal) vfw.obj.workModal = new vfw.html.workModalObj();
    // vfw.obj.workModal(html, is_simple)
    const modal_values = get_workflow();
    const json = vfw.session.get_wpsprocess(service, identifier);
    // vfw.obj.workModal.build(json, service)
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
    // modHeadElement.innerHTML = newElement;
}

/**
 * Load metadata of a wps process if not available.
 * The in- and outputs (and so on) of a tool are used from the normal tool if available.
 * TODO: also a batch job should be stored somehow to make it available. Maybe through a grouping (button) of the results?
 * @param {string} origin - depending on the source the sources to fill the input fields are different
 * @param {string} service - wps service as stored in database
 * @param {string} identifier - identifier of a wps process
 **/
vfw.workspace.modal.openBatchprocess = function (origin='modal', wpsInfo={}, service="",
                                                  identifier="", inputs = null, boxId=[]) {
    //if (wpsInfo === {}) wpsInfo = vfw.session.get_wpsprocess(service, identifier)
    // const modal_values = vfw.session.get_workflow();

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

        // TODO: implement possibility not only to preview, but also to select data for port.
        //  Improve code of vfw.workspace.modal.build_radio and others to allow reuse of these functions
        btnObj = [process['dataInputs'][index]['identifier'], process['dataInputs'][index]]

        /** Fill the tool with selection made to receive this result button */
        // if (inputtype === 'string') {
        //
        //     vfw.workspace.modal.setInPortValue(process['dataInputs'][index]['identifier'], process['dataInputs'][index])
        //     // vfw.workspace.modal.setInPortValue(modal_values[boxidentifier]['input_keys'], modal_values[boxidentifier]['input_values'])
        //     // vfw.workspace.modal.setInPortValue(modal_values[inputs]['input_keys'], modal_values[inputs]['input_values'])
        // } else if (Array.isArray(inputs)) {
        //     vfw.workspace.modal.setInPortValue(inputs[0], inputs[1])
        // }
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
            //url: DEMO_VAR+"/wps_gui/"+service+"/process",
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
            // return e
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
        // vfw.html.popup.classList.add(popActive);
        vfw.html.loaderOverlayOn()
        $.when(vfw.session.load_wpsprocess(service, identifier))
            .done(
                function (json) {
                    tools[service][identifier] = json
                    sessionStorage.setItem('tools', JSON.stringify(tools))
                    tool_data = json;
                    // vfw.html.popup.classList.remove(popActive);
                    vfw.html.loaderOverlayOff();
                })
        /* .fail(function (e) {
             console.error('Failed: ', e)
         });*/
    }
    return tool_data
}

/**
 * create a dict with random coordinates on the dropzone ('dropdiv').
 * TODO: avoid overlap of boxes
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
            // console.log("'sidebtn' + modalData.inId_list[i]: ", 'sidebtn' + modalData.inId_list[i])
            // console.log('tool_id: ', tool_id)
            box_id = newbox.boxID;

            // TODO: The following should be part of another function
            workflow = vfw.session.get_workflow()
            // workflow[box_id].output_boxes = [tool_id];
            // workflow[tool_id].input_boxes[i] = box_id;
            workflow[box_id].output_ids = [tool_id];
            workflow[tool_id].input_ids[i] = box_id;
            sessionStorage.setItem('workflow', JSON.stringify(workflow))

            databox = newbox.box;
            dataport = databox.getOutputPort(0);
            // TODO: Not sure if ports have always the same order as in modal. Find better way to get right port.
            toolport = toolbox.getInputPort(parseInt(i));
            // add_connection(dataport, toolport);
        }
    }
    vfw.session.draw2d.setdata();
}

// TODO: avoid overlap!
/*function reduce_lap(x, y) {
    // console.log('ev: ', ev)
    // let box_param = vfw.workspace.workflow.process_drop_params(service, id)
    let dropzone = document.getElementById('dropdiv');
    // console.log('dropzone: ', dropzone.getBoundingClientRect())
    let dropzone_coords = dropzone.getBoundingClientRect()
    let dropzone_size = [dropzone_coords.width, dropzone_coords.height]
    let dropzone_offset = [dropzone_coords.left, dropzone_coords.top]
    let boxes = [];
    let box_dist = [];
    let box_row = [];
    let bx, by, i, j;

    let rectangles = document.getElementsByTagName("rect");
    // console.log('rectangles: ', rectangles)

    for (i of rectangles) {
        if (i.className.baseVal.startsWith("box")) {
            boxes.push(i)
            // console.log('i1: ', i)
            // console.log('i2: ', i.getBoundingClientRect())
            // console.log('i3: ', document.elementFromPoint(x, y))
        }
    }
    for (i of boxes) {
        console.log('boxes: ', boxes)
        box_row = [];
        for (j of boxes) {
            bx = i.getBoundingClientRect().x - j.getBoundingClientRect().x
            by = i.getBoundingClientRect().y - j.getBoundingClientRect().y
            box_row.push([bx, by, Math.sqrt((bx*bx)+(by*by))])
        }
        box_dist.push(box_row)
    }
    console.log('box_dixst: ', box_dist)
    // if ((a.left >= b.right || a.top >= b.bottom ||
    //     a.right <= b.left || a.bottom <= b.top):
    // {
    //     // no overlap
    // }
    // else
    // {
    //     // overlap
    // }

    // sessionStorage.setItem('box', JSON.stringify(box))
}*/

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
    /** TODO: check if an Element of a wps is required **/
    const inModal = document.getElementById('mod_in');
    const dropDInputs = inModal.getElementsByTagName('select');
    // const inputInputs = inModal.getElementsByTagName('input');
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
    let files = {};
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
                // valueList.push(dDInput[j].value)
                stored = JSON.parse(sessionStorage.getItem("dataBtn"))[dDInput[j].value]
                // TODO: take care how to handle the input. For now input comes only from db so the ID is directly add.
                //  Find solution for data sources that are not in the Entries table (i.e. results)
                valueList.push(parseInt(stored['dbID']))
                // valueList.push(stored['source'] + stored['dbID'])
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
            // TODO: Create a objects for tools and get there the info if selection should be in an array
            // if (dDInput[0].value.substring(0, 2) == 'db') {
            if (dDInput[0].value.split(",").length == 1) {
                stored = JSON.parse(sessionStorage.getItem("dataBtn"))[dDInput[0].value]
                if (stored.type !== "geometry") {
                    // TODO: take care how to handle the input. For now input comes only from db so the ID is directly add.
                    //  Find solution for data sources that are not in the Entries table (i.e. results)
                    let intValue = dropDInputs[i].multiple ? [parseInt(stored['dbID'])] : parseInt(stored['dbID']);
                    inValue.push(intValue);
                    // inValue.push(stored['source'] + stored['dbID']);
                } else {
                    let polygon = new ol.geom.Polygon(stored['geom']);
                    let geoJsonFormat = new ol.format.GeoJSON();
                    // TODO: Stop transforming EPSG:4326 as EPSG:3857 to EPSG:4236. TODO: Make sure which coordinates are given and transform only when needed.
                    // polygon.applyTransform(ol.proj.getTransform('EPSG:3857', 'EPSG:4326'));
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
                // TODO: What if I have another source than only dataBtn or dataGroup? Have to get this key somehow.
                let groupInValues = [];
                let groupInTypes = [];
                // Try to get wps ID for data
                for (let dataset of dDInput[0].value.split(",")) {
                    stored = JSON.parse(sessionStorage.getItem("dataBtn"))[dataset]
                    // TODO: take care how to handle the input. For now input comes only from db so the ID is directly add.
                    //  Find solution for data sources that are not in the Entries table (i.e. results)
                    groupInValues.push(parseInt(stored['dbID']))
                    // groupInValues.push(stored['source'] + stored['dbID'])
                    groupInTypes.push(stored['type']);
                }
                inValue.push(groupInValues)
                inType.push(groupInTypes);
                // inValue.push(dDInput[0].value.split(","));
                // inValue.push(dDInput[0].value);
                // inType.push(stored['type']);
                indict[dropDInputs[i].name] = dDInput[0].value.split(",");
            }
            inKey.push(dropDInputs[i].name);
            inId.push(dDInput[0].value);
        }
    }

    /** now check the other elements like radio buttons or checkboxes **/
    for (let i = 0; i < inputInputs.length; i++) {
        if (inputInputs[i].type == "file") {
            inKey.push(inputInputs[i].name);
            inValue.push(inputInputs[i].files.length ? inputInputs[i].files[0].name : "");
            inType.push('file');
            inId.push('');
            if (inputInputs[i].files.length) {
                files[inputInputs[i].name] = inputInputs[i].files[0];
                // indict[inputInputs[i].name] = inputInputs[i].files[0].name;
                indict[inputInputs[i].name] = "__uploaded__";
            } else {
                indict[inputInputs[i].name] = "";
            }
        } 
        else if (inputInputs[i].type == "radio") {
            if (inputInputs[i].checked == true) {
                inKey.push(inputInputs[i].name);
                inValue.push(inputInputs[i].value);
                inType.push('string');
                inId.push('');
                indict[inputInputs[i].name] = inputInputs[i].value;
                // indict[inputInputs[i].name] = dDInput[i].value;
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
        'in_type_list': inType, 'outputName': outputName, 'inId_list': inId, 'in_dict': indict, 'files': files,
    }
}

// TODO: runProcess now works only on execution from modal. Adjust to be usable from Dropzone too,
//  when you have the drop objects
// TODO: Improve code by using HTML Forms
// TODO: colors here need to be fixed for the modal -- Goutam
vfw.workspace.modal.runProcess = function () {
    //vfw.workspace.modal.setColor("dodgerblue");
    vfw.workspace.modal.setColor(modalColors['DEFAULT']);
    let modal_input = vfw.workspace.modal.prepData();
    let directshowdatatypes = ['figure', 'string', 'html', 'integer', 'float']
    let group = false;
    let groupName = ''
    let i = 0;
    let members = [];
    vfw.html.loaderOverlayOn();

    let formData = new FormData();

    formData.append("processrun", JSON.stringify({
        id: modal_input.id,
        serv: modal_input.serv,
        key_list: modal_input.key_list,
        value_list: modal_input.value_list,
        in_type_list: modal_input.in_type_list,
        outputName: modal_input.outputName,
        inId_list: modal_input.inId_list,
        in_dict: modal_input.in_dict
    }));

    formData.append("csrfmiddlewaretoken", vfw.var.csrf_token);
    if (modal_input.files) {
        Object.entries(modal_input.files).forEach(([key, file]) => {
            formData.append(key, file);
        });
    }

    $.ajax({
        url: vfw.var.DEMO_VAR + "/workspace/processrun",
        type: 'POST',
        data: formData,
        processData: false,   
        contentType: false   
    })
        .done(function (json) {  /** Results are stored in the sessionStorage **/
            vfw.html.loaderOverlayOff()
            console.log(json)
            /** Handle result according to the success/status of the process */
            if (json.status == "SUCCESS") {
                let btnName = '';
                let btnData = {};
                json.wps = modal_input.id;
                json.inputs = {};
                $.each(modal_input.key_list, function (key, value) {
                    json.inputs[value] = modal_input.value_list[i];
                    i++;
                });
                //vfw.workspace.modal.setColor("forestgreen");
                vfw.workspace.modal.setColor(modalColors['SUCCESS']);

                // if there is an html available for a result show it directly as result
                if ('report_html' in json) {
                    btnData['report_html'] = json.report_html;
                     // let iframe = '<iframe srcdoc="' + json.report_html + '"></iframe>'
                    // vfw.workspace.modal.openResultModal(iframe)
                    vfw.workspace.modal.openResultModal(json.report_html)
                    // vfw.html.loaderOverlayOff();
                }

                // if there are more then one result, than create a grouped button
                if (Object.keys(json.result).length > 1) {
                    group = true;
                    groupName = vfw.sidebar.set_group_btn_name(modal_input.outputName, 'resultBtn');
                    // document.getElementById("workspace_results").innerHTML
                    //     += vfw.workspace.buildResultGroupButton(groupName);
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
                //vfw.workspace.modal.setColor("firebrick");
                vfw.workspace.modal.setColor(modalColors['FAILED']);
            }
            else if (json.status == 'accepted' || json.status == 'running') {
                //vfw.workspace.modal.setColor("orange");
                vfw.workspace.modal.setColor(modalColors['ACCEPTED']);
                if (!json['orgID']) {
                    // create an id for the new object
                    const urlParts = json.outputs.path.split("/");
                    json['orgID'] = json.name + '_' + urlParts[urlParts.length -1];
                }

                // create object
                //vfw.datasets.resultObjects[json['orgID']] = new vfw.datasets.resultObj(json);
                vfw.datasets.resultObjects = { [json['orgID']]: new vfw.datasets.resultObj(json) };
                vfw.datasets.resultObjects[json['orgID']].job_details = json['job_details'];
                vfw.datasets.resultObjects[json['orgID']]._updateJobStatus(json['job_details']);
                console.log(vfw.datasets.resultObjects);

            }
            else if (json.status == 'successful') {
                vfw.workspace.modal.setColor(modalColors['SUCCESSFUL']);

                if (!json['orgID']) {
                    // create an id for the new object
                    const urlParts = json.outputs.path.split("/");
                    json['orgID'] = json.name + '_' + urlParts[urlParts.length -1];
                }

                vfw.datasets.resultObjects = { [json['orgID']]: new vfw.datasets.resultObj(json) };
            }
            else if (json.status == 'FINISHED') {
                alert('Finished neeeds implementation (Short running porcess)')
                //vfw.workspace.modal.setColor("green");
                vfw.workspace.modal.setColor(modalColors['SUCCESS']);
            }
            else if (json.execution_status == "error in wps process") {
                //vfw.workspace.modal.setColor("firebrick");
                vfw.workspace.modal.setColor(modalColors['FAILED']);
                console.error('Error in wps process: ', json.error)
                // alert('Error: Failed to execute your request.');
            }
            else if (json.execution_status == "auth_error") {
                //vfw.workspace.modal.setColor("firebrick");
                vfw.workspace.modal.setColor(modalColors['FAILED']);
                /** Use Timeout to ensure color changed before popup appears **/
                setTimeout(function () {
                    alert('Error: You are not allowed to run this process. Please Contact your Admin.');
                }, 5);
                console.error('Maybe you have to log in to run processes. ', json.execution_status)
            }
        })
        .fail(function (json) {
            vfw.html.loaderOverlayOff()
            //vfw.workspace.modal.setColor("firebrick");
            vfw.workspace.modal.setColor(modalColors['FAILED']);
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
    // '2020-10-31T14:10'
    // fetch(GEO_SERVER + '/wfs/' + vfw.var.DATA_LAYER_NAME + '/' + extent.join(',') + '/3857',
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
        url: vfw.var.DEMO_VAR + "/workspace/processrun",
        data: {
            processrun: JSON.stringify({
                id: identifier, serv: wpsservice,
                key_list: input_dict.keys(), value_list: input_dict.values()
            }),
            // processrun: JSON.stringify(input_dict),
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
/** 
vfw.workspace.modal.setColor = function (color) {
    let modalColor = document.getElementById("modal-header");
    modalColor.style.backgroundColor = color;
    modalColor = document.getElementById("modal-footer");
    modalColor.style.backgroundColor = color;
    document.getElementsByClassName("work_modal-output")[0].style.display = "none";
}
*/
const modalColors = {
    "DEFAULT": "bg-blue-600",
    "SUCCESSFUL": "bg-green-500",
    "ACCEPTED": "bg-yellow-600",
    "FAILED": "bg-red-500"
}

vfw.workspace.modal.setColor = function (color) {
    const modalHeader = document.getElementById("modal-header");
    const modalFooter = document.getElementById("modal-footer");

    // Remove all existing background color classes from modalColors
    Object.values(modalColors).forEach(bgColorClass => {
        modalHeader.classList.remove(bgColorClass);
        modalFooter.classList.remove(bgColorClass);
    });

    // Add the desired color class
    const newColorClass = modalColors[color] || modalColors["DEFAULT"]; // Fallback to "DEFAULT" if color not found
    modalHeader.classList.add(newColorClass);
    modalFooter.classList.add(newColorClass);

    // Hide the "view result" button
    document.getElementsByClassName("work_modal-output")[0].style.display = "none";
};
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
    // let radioNode = document.createElement("p");
    let nodeText = document.createTextNode(" " + option + " ");

    let inElement = document.createElement("INPUT");
    inElement.type = "radio";
    // inElement.setAttribute("type", "radio");
    inElement.value = option;
    inElement.id = 'mod_in_el_' + item.title;  // item.identifier;
    if (item.minOccurs === 1) inElement.required = true;

    inElement.name = entry_name;  // item.identifier;
    // inElement.title = item.description;  // item.identifier;
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
    // let radioNode = document.createElement("p");
    let nodeText = document.createTextNode(" " + option + " ");
    let inElement = document.createElement("input");
    inElement.type = "radio";
    // inElement.setAttribute("type", "radio");
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
    let acceptedDataTypes = DATATYPE.accepts([item.dataType])  // TODO: Whats wrong in this Class?
    // let acceptedDataTypes = DATATYPE.accepts([item.keywords[0]])

    // htmlSelect.id = item.identifier;
    htmlSelect.id = 'mod_in_el_' + item.identifier;  // item.id

    for (let i in sessionStoreData) {
        if (acceptedDataTypes.has(sessionStoreData[i].type)) {  // TODO: shouldn't this be 'hasOwnProperty'?
            aptStoreData[i] = sessionStoreData[i];
        }
        // TODO: groups are not properly handled yet
        if (sessionStoreData[i].hasOwnProperty('group')) {
            // aptGroupedData[i] = sessionStoreData[i];
        } else {
            // aptStoreData[i] = sessionStoreData[i];
        }
    }
    for (let i in resultData) if (acceptedDataTypes.has(resultData[i].type)) aptResultData[i] = resultData[i]
    for (let i in groupedData) {
        if (acceptedDataTypes.has(groupedData[i].type)) {  // TODO: shouldn't this be 'hasOwnProperty'?
            // aptGroupedData[i] = groupedData[i]
            // aptGroupedData[i] = groupedData[i]
        }
        // aptGroupedData[i] = groupedData[i]
    }
    // for (let i in sessionStoreData) if (item.keywords[0] == sessionStoreData[i].type) aptStoreData[i] = sessionStoreData[i];
    // for (let i in resultData) if (item.keywords[0] == resultData[i].type) aptResultData[i] = resultData[i]
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
            // opt.setAttribute('data-datatype', selectables[singleData].type);
    }

    Object.keys(selectables).forEach(function (singleData) {
        opt = document.createElement("OPTION");
        groupName = ''

        /** Check if a Button for a group, or a single button is needed */
        if (selectables[singleData].abbr && selectables[singleData].unit)
            // TODO: group needs to be implemented. To seperate one could start with the following line
            // !selectables[singleData].hasOwnProperty('group') &&  // is no group
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
            // opt.innerText = `${singleData}`;
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

    if (item.identifier === 'start_date' || item.identifier === 'end_date') {
        return document.createDocumentFragment();
        }
        
    // if ('minOccurs' in item) {  // outer if seems to be unused
    if (item.minOccurs == 0) {
        titleText = " " + item.title + ": "
    } else if (item.defaultValue) {
        titleText = " " + item.title + ": "
    } else if (item.required === true || item.minOccurs > 0) {
        // } else if (item.minOccurs > 0 && item.dataType != 'boolean') {
        titleText = " " + item.title + " (*) : ";
        inElement.required = true;
        // }
    } else {
        titleText = " " + item.title + ": "
    }

    /** check attributes/'keywords' from the process that are used to define which input element is used */
    // if (item.minOccurs === 1) inElement.required = true;
    nodeText = document.createTextNode(titleText);
    newNode.appendChild(nodeText);

        //Upload input support
    if ('keywords' in item && Array.isArray(item.keywords) && item.keywords.includes('upload')) {
        inElement = document.createElement("input");
        inElement.type = "file";
        inElement.id = 'mod_in_el_' + entry_name;
        inElement.name = entry_name;
        inElement.title = item.description || "";
        inElement.accept = ".csv,text/csv";
        if (item.minOccurs > 0) {
            inElement.required = true;
        }
        inElement.classList.add("sr-only");
        newNode.classList.add("flex", "items-center", "gap-3");

        const fileNameSpan = document.createElement("span");
        fileNameSpan.textContent = "No file chosen";
        fileNameSpan.classList.add("text-xs", "text-gray-400", "truncate", "max-w-[160px]");

        const label = document.createElement("label");
        label.htmlFor = inElement.id;
        label.classList.add(
            "flex", "items-center", "gap-3", "cursor-pointer"
        );

        const btn = document.createElement("span");
        const icon = document.createElement("i");
        icon.classList.add("fa-solid", "fa-upload");
        btn.appendChild(icon);
        btn.appendChild(document.createTextNode(" Choose file"));
        btn.classList.add(
            "inline-flex", "items-center", "gap-1.5",
            "px-4", "py-2", "text-xs", "font-semibold",
            "!bg-slate-700", "!text-white", "hover:!bg-slate-800",
            "transition-colors", "cursor-pointer"
        );

        inElement.addEventListener("change", () => {
            fileNameSpan.textContent = inElement.files.length > 0 ? inElement.files[0].name : "No file chosen";
        });

        label.appendChild(btn);
        label.appendChild(fileNameSpan);
        newNode.appendChild(inElement);
        newNode.appendChild(label);
        return newNode;
    }
    if ('allowedValues' in item && Array.isArray(item.allowedValues) && item.allowedValues.length > 1) {
        if ('maxOccurs' in item) {
            if (item.maxOccurs === 1) {
                // nodeText = "";
                item.allowedValues.forEach(function (option) {
                    vfw.workspace.modal.build_radio(item, entry_name, newNode, option)
                });
            }
        }
    } else if ('supportedValues' in item && Array.isArray(item.supportedValues) && item.supportedValues.length > 1) {
        if ('maxOccurs' in item) {
            if (item.maxOccurs === 1) {
                // nodeText = "";
                item.supportedValues.forEach(function (option) {
                    vfw.workspace.modal.build_radio(item, entry_name, newNode, option)
                });
                // inElement.setAttribute("type", "radio")
            }
        }
    } else if ("enum" in item.schema) {
        item.schema.enum.forEach(function (option) {
            vfw.workspace.modal.build_radio(item, entry_name, newNode, option)
        });
    } else if ('keywords' in item && item.keywords.includes('pattern')) {
        vfw.workspace.modal.build_regexText(item, entry_name, newNode)
    // } else if ('keywords' in item) {  // don't use this for geoapi;
    } else if (vfw.var.EXT_DATATYPES.includes(item.dataType)) {
        countDropDowns = vfw.workspace.modal.build_dropdown(item, newNode, countDropDowns)

        /** Set input element according to dataType */
    } else {
        inElement = document.createElement("INPUT");
        inElement.id = 'mod_in_el_' + entry_name;  // item.id;
        inElement.name = entry_name;  // item.identifier;
        inElement.title = item.description;  // item.identifier;
        inElement.setAttribute("list", item.title + '_list');  // item.identifier + '_list');
        inElement.classList.add("bg-gray-50", "border", "border-gray-300", "text-gray-900", "text-sm", "!mb-2", "p-1")

        // if (item.required === true) inElement.required = true;
        // if (item.minOccurs > 0 && item.dataType != 'boolean') inElement.required = true;
        switch (item.schema.type) {  // (item.dataType) {
            case 'string':
                inElement.type = "text";
                //inElement.className = "input"
                inElement.appendChild(vfw.workspace.modal.set_textfield_opt(item, resultData, sessionStoreData))
                if ("default" in item.schema) inElement.value = item.schema.default;
                if ('defaultValue' in item) inElement.value = item.defaultValue;  // old schema
                break;
            case 'boolean':
                inElement.type = "checkbox";

                if ("default" in item.schema && item.schema.default === true) {
                    inElement.checked = true;
                }
                // Fallback for older schema 
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
        // TODO: is this here the third time I set required = True? Test if necessary
        if (item.minOccurs > 0) {
            inElement.required = true
        } //else {inElement.required = false}
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
    // let availableInputs = get_available_inputs();
    // let wpsInfo = vfw.session.get_wpsprocess(service, identifier);

    /** Collect the data that is available for the tools. If key has no data an empty dict is returned.
     * @param {string} store - Which key of the Session Storage should be loaded
     */
    getStorageOrDict = function (store) {
        return sessionStorage.getItem(store) ? JSON.parse(sessionStorage.getItem(store)) : {};
    }
    let sessionStoreData = getStorageOrDict("dataBtn");
    let resultData = getStorageOrDict("resultBtn");
    let workflowData = getStorageOrDict("workflow");
    // let sessionStoreData = sessionStorage.getItem("dataBtn") ? JSON.parse(sessionStorage.getItem("dataBtn")) : {};
    // let resultData = JSON.parse(sessionStorage.getItem("resultBtn"));
    // let workflowData = JSON.parse(sessionStorage.getItem("workflow"));

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
    // modInElement = document.getElementById("mod_in");
    modInElement.innerHTML = "";
    let inElement = "", newNode = "", nodeText = "";
    let outElementIdList = [];

    /** Loop over input parameters and create an appropriate input element for each */
    // wpsInfo.dataInputs.forEach(function (item, index) {  // old wps used a list
    Object.entries(wpsInfo.inputs).forEach(function (entry_value, index) {
        newNode = vfw.html.createInputElement(entry_value, resultData, sessionStoreData);
        if (typeof (newNode) === 'object') modInElement.appendChild(newNode)
    });

    // TODO: build one output now. Decide how to handle several outputs
    /** outputs: **/
    document.getElementById("mod_out").innerHTML = "";

    nodeText = document.createElement("p");
    nodeText.appendChild(document.createTextNode(" Name for output in data store: "));

    newNode = document.createElement("div");
    newNode.appendChild(nodeText);
    let outElement = document.createElement("input");
    outElement.classList.add("bg-gray-50", "border", "border-gray-300", "text-gray-900", "text-sm", "!mb-2", "p-1")
    newNode.appendChild(outElement);
    if (typeof (newNode) === 'object') modOutElement.appendChild(newNode);
    let modal = document.getElementById("workModal");
    // modal.setAttribute("name", invoke_btn_id);
    modal.setAttribute("name", wpsInfo.identifier);
    //modal.style.display = "block";
    modal.classList.remove("hidden");
    modal.classList.add("flex");
    let currentModal = new vfw.workspace.modalObj(wpsInfo.identifier, outElementIdList);

    let batchBtn = modFootElement.getElementsByClassName("work_modal-createbatch")[0]
    batchBtn.addEventListener("click", function (evt) {
        vfw.workspace.modal.openBatchprocess('modal', wpsInfo, service);
    });
    // TODO: get right name for sessionstorage
    // sessionStorage.setItem("currentModal", JSON.stringify(currentModal));
    // console.log('+++: ', JSON.stringify(vfw.workspace.modalObj))
    // return modal;
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
    console.log("load just a test workflow.")
    // let workflow
    // sessionStorage.setItem('workflow', JSON.stringify(workflow))
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
    console.log('++++ + inputs: ', inputs)
    let has_inIds, has_inVals;
    let result = {'error': false, 'error_index': []}
    let testtool = JSON.parse(sessionStorage.getItem('tools'))[server][tool]
    testtool.dataInputs.forEach((testinput, i) => {
        if (testinput.required) {
            // console.log('____testinput: ', testinput)
            // console.log('____ inputs[1].inId_list: ', !inputs[1].inId_list)
            // console.log('____ !inputs[1].inId_list[i]: ', !inputs[1].inId_list[i])
            // console.log('____ inputs[1].inId_list && !inputs[1].inId_list[i]: ', inputs[1].inId_list && !inputs[1].inId_list[i])
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
    console.log('workflow: ', workflow)
    // let workflow = globalWorkflow.session_storage();
    let processTree = vfw.workspace.workflow.create_processTree(workflow);
    console.log('processTree: ', processTree)
    let processChain = vfw.workspace.workflow.create_ReverseProcessOrder(processTree).reverse();
    console.log('processChain: ', processChain)
    let preppedWorkflow = vfw.workspace.workflow.prep_wps_workflow(workflow, processChain);
    console.log('run preppedWorkflow: ', preppedWorkflow)
    Object.entries(preppedWorkflow).map((box) => {
        box_result = vfw.workspace.workflow.check_inputs(box[1].serv, box[1].id, box);
        if (box_result.error) {
            errors.push(box_result)
        }
    })
    console.log('errors:', errors)

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
    console.log('workflow: ', workflow)
    console.log('processChain: ', processChain)
    let preppedWorkflow = {};
    let outputName;

    for (let i of processChain) {
        outputName = workflow[i].output_ids.length === 0 ? workflow[i].name + "_" : workflow[i].name;
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
    /*    let goal = {
            id: "flowdurationcurve"
            inId_list: (3) ['db494', '', '']
            in_type_list: (3) ['timeseries', 'boolean', 'boolean']
            key_list: (3) ['ts-pickle', 'non-exceeding', 'log']
            outputName: "flowdurationcurve_"
            serv: "PyWPS_vforwater"
            value_list: (3) ['wps1047', false, true]
        }*/

    return preppedWorkflow;
}


/**
 * Remove boxes from Dropzone, from Sessionstorage and set workflow name to default name.
 */
vfw.workspace.workflow.clear_workflow = function () {
    vfw.draw2d.canvas.clear();
    // globalWorkflow.set_name();
    vfw.session.set_workflow_name()
    document.getElementById("workflow_name").value = gettext('my workflow')
    sessionStorage.setItem('workflow', JSON.stringify({'name': "my workflow"}))
    vfw.session.draw2d.setdata()
}


/**
 * Check in- and output of connected boxes and build the workflow as a tree.
 * @param {{}} workflow
 */
// function create_process_tree(workflow) {
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
            console.log('box: ', i, box)
            processList.push(box[0])
            /*if (workflow[box[1].input_boxes].source === 'toolbar') {

            }*/
            processDict[box[0]] = {children: box[1].input_ids};
            processDict[box[0]].parents = box[1].output_ids;
            // if (box[1].output_boxes.length == 0) {
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
            // TODO: This results in an error anyways. Fix it!
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
 * TODO: update for parallel function call
 * @param {dict} processDict
 * @param {number} depth
 * @param {dict} innerProcesses
 */
vfw.workspace.workflow.create_ReverseProcessOrder = function (processTree, depth = 0, innerProcesses = []) {
    for (let [boxName, deeperElements] of Object.entries(processTree)) {
        console.log('boxName: ', boxName)
        console.log('deeperElements: ', deeperElements)
        if (boxName) {
            innerProcesses.push(boxName);
            innerProcesses.concat(
                vfw.workspace.workflow.create_ReverseProcessOrder(deeperElements, depth += 1, innerProcesses)
            )
        }
    }
    return innerProcesses;
}

const previewState = {
    files: [],
    currentIndex: 0,
    dir: '',
};

vfw.workspace.modal.renderResult = function () {
    console.log("currentIndex: ", previewState.currentIndex);
    const container = document.getElementById("carouselContainer");
    container.innerHTML = "";

    const filePath = previewState.files[previewState.currentIndex];
    const filename = formatFileName(filePath);
    const extension = filePath.split('.').pop().toLowerCase();

    //Update Header
    document.getElementById("previewFileName").textContent = "Name: " + filename;
    document.getElementById("previewCounter").textContent =
        "("+ `${previewState.currentIndex + 1} / ${previewState.files.length}`+ ")";

    path = previewState.dir;
    const fullPath = `${path}/${filePath}`;
    const url = `/workspace/resultdisplay?path=${encodeURIComponent(fullPath)}`;

    if (["png", "jpg", "jpeg", "gif", "webp"].includes(extension)) {
        const img = document.createElement("img");
        img.src = url;
        img.className = "max-h-full max-w-full object-contain";
        container.appendChild(img);

    } else if (extension === "pdf") {
        const iframe = document.createElement("iframe");
        iframe.src = url;
        iframe.className = "w-full h-full";
        container.appendChild(iframe);
    }


    else if (extension === "html") {
        container.innerHTML = "";

        // Wrapper
        const wrapper = document.createElement("div");
        wrapper.style.position = "relative";
        wrapper.style.width = "100%";
        wrapper.style.height = "100%";

        // Loading message
        const loader = document.createElement("div");
        loader.innerHTML = "Loading evaluation report... please wait ⏳";
        loader.style.position = "absolute";
        loader.style.top = "50%";
        loader.style.left = "50%";
        loader.style.transform = "translate(-50%, -50%)";
        loader.style.fontSize = "18px";
        loader.style.color = "#444";

        // Optional: make it look nicer
        loader.style.background = "rgba(255,255,255,0.9)";
        loader.style.padding = "20px";
        loader.style.borderRadius = "10px";
        loader.style.boxShadow = "0 2px 10px rgba(0,0,0,0.1)";

        // Iframe
        const iframe = document.createElement("iframe");
        iframe.style.width = "100%";
        iframe.style.height = "100%";
        iframe.style.border = "0";


        iframe.onload = () => {
            setTimeout(() => {
                loader.style.transition = "opacity 0.4s ease";
                loader.style.opacity = "0";

                setTimeout(() => {
                    loader.style.display = "none";
                }, 100);
            }, 1000);
        };


        wrapper.appendChild(iframe);
        wrapper.appendChild(loader);
        container.appendChild(wrapper);

        // Fetch + write HTML
        fetch(url)
            .then(response => response.text())
            .then(html => {
                const iframeDoc = iframe.contentWindow.document;
                iframeDoc.open();
                iframeDoc.write(html);
                iframeDoc.close();
            })
            .catch(error => {
                console.error("Failed to load HTML report:", error);
                loader.innerHTML = "❌ Failed to load simulation report.";
            });
    }

}

function formatFileName(path) {
    const name = path
        .split(/[/\\]/).pop()
        .replace(/\.[^/.]+$/, "")             
        .replace(/[_-]+/g, " ");              

    return name.replace(/\b\w/g, c => c.toUpperCase());
}