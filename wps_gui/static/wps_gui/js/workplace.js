function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text/html", ev.target.id);
}

function drop(ev) {
    ev.preventDefault();
    let droplet= ev.dataTransfer.getData("text/html");
    console.log('ev: ', ev)
    console.log('drop: ', droplet)

    // let droplet = document.createElement('canvas');
    // let dropletCopy = document.createElement('canvas');
    let dropletCopy = document.getElementById(droplet).cloneNode(true);
    // build new id for new element:
    if (sessionStorage.getItem("dz_count")){
        sessionStorage.setItem("dz_count", JSON.parse(sessionStorage.getItem("dz_count"))+1)
    } else {
        sessionStorage.setItem("dz_count", 1)
    }
    console.log('sessionStorage: ', sessionStorage.getItem("dz_count"))
    dropletCopy.id = "dz"+sessionStorage.getItem("dz_count");
    dropletCopy.classList.add('tool-btn');
    dropletCopy.style.left = ev.offsetX + "px";
    dropletCopy.style.top = ev.offsetY + "px";
    console.log('Copy: ', dropletCopy)
    // ev.dataTransfer.setDragImage(dropletCopy, ev.offsetX + "px", ev.offsetY + "px")
    ev.target.appendChild(dropletCopy);
    console.log('ev: ', ev)
}

function open_wpsprocess(service, identifier) {
    wpsprocess(service, identifier)
    //let modal = document.getElementById("workModal");
    //modal.style.display = "block";
    console.log("service: ", service)
    console.log("identifier: ", identifier)
}

function wpsprocess(service, identifier) {
    $.ajax({
    url: DEMO_VAR+"/wps_gui/processview",
    //url: DEMO_VAR+"/wps_gui/"+service+"/process",
    dataType   : 'json',
    data: {
        processview: JSON.stringify({id: identifier, serv: service}),
        'csrfmiddlewaretoken': csrf_token,
    }, // data sent with the post request
    success: function (json) {
        build_modal(json)
        },
    });
}

function saveInput() {
    console.log('lets store it')
}

function build_modal(wpsInfo) {
    console.log(' wpsInfo: ', wpsInfo)
    // console.log('wpsInfo[title]: ', wpsInfo[title])
    let element = document.getElementById("mod_head");
    let newElement = "";
    element.innerHTML = wpsInfo.title;
    element = document.getElementById("mod_abs");
    if (wpsInfo.abstract) {newElement = wpsInfo.abstract;
    } else {newElement = ""}
    element.innerHTML = newElement;

    //inputs:
    document.getElementById("mod_in").innerHTML = "";
    let inElement = "";
    let newNode, nodeText = "";

    wpsInfo.dataInputs.forEach(function (item){
        element = document.getElementById("mod_in");
        newNode = document.createElement("p");
        nodeText = document.createTextNode(" " + item.title + ": ");
        newNode.appendChild(nodeText);
        if ('allowedValues' in item && Array.isArray(item.allowedValues) && item.allowedValues.length > 1){
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
                        inElement.name = item.identifier;
                        if (item.minOccurs === 1) {inElement.required = true;}
                        if ('defaultValue' in item) {
                            if (item.defaultValue == option) {inElement.checked = true;}}
                        newNode.appendChild(inElement);
                        newNode.appendChild(nodeText);
                    });
                }
            }
        } else if ('supportedValues' in item  && Array.isArray(item.supportedValues) && item.supportedValues.length > 1){
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
                        inElement.name = item.identifier;
                        if (item.minOccurs === 1) {inElement.required = true;}
                        if ('defaultValue' in item) {
                            if (item.defaultValue == option) {inElement.checked = true;}}
                        newNode.appendChild(inElement);
                        newNode.appendChild(nodeText);
                    });
                    // inElement.setAttribute("type", "radio")
                }
            }
        } else {
            inElement = document.createElement("input");
            inElement.id = item.identifier;
            inElement.name = item.identifier;
            switch (item.dataType) {
                case 'string':
                    inElement.type = "text";
                    //inElement.className = "input"
                    if ('defaultValue' in item) {inElement.value = item.defaultValue;}
                    break;
                case 'boolean':
                    inElement.type = "checkbox";
                    if ('defaultValue' in item && item.defaultValue == true) {inElement.checked = true;}
                    break;
                case 'float':
                    inElement.type =  "number";
                    inElement.step = "0.000001";
                    if ('defaultValue' in item) {inElement.value = item.defaultValue;}
                    break;
                case 'integer':
                    inElement.type =  "number";
                    if ('defaultValue' in item) {inElement.value = item.defaultValue;}
                    break;
                case 'ComplexData':
                    inElement.type = "text";
                    console.log('you have to handle complesdata properly');
                    if ('defaultValue' in item) {
                        if ('mimeType' in item.defaultValue) {
                            inElement.value = item.defaultValue.mimeType;}}
                    break;
                case 'BoundingBoxData':
                    console.log('you have to handle BoundingBoxData properly');
                    if ('defaultValue' in item) {inElement.value = item.defaultValue;}
                    break;
                default:
                    console.log('+++++++++++++++++++++++')
                    console.log(' new dataType')
            }
            if (item.minOccurs > 0) {inElement.required = true} //else {inElement.required = false}
            newNode.appendChild(inElement);
        }
        //$("p").append("<b>Appended text</b>");
        //$("div").append(inElement);
        if (typeof (newNode) === 'object') {element.appendChild(newNode)}
    });

    //outputs:
    console.log('outputs: ', wpsInfo.processOutputs)
    console.log('outputs: ', wpsInfo.processOutputs.length)
    console.log('outputs: ', wpsInfo.processOutputs[0])
    document.getElementById("mod_out").innerHTML = "";
    let outElement = "";
    newNode, nodeText = "";

    wpsInfo.processOutputs.forEach(function (item){
        element = document.getElementById("mod_out");

        nodeText = document.createElement("p");
        nodeText.appendChild(document.createTextNode(" Name for " + item.title + ": "));

        newNode = document.createElement("div");
        newNode.appendChild(nodeText);



        outElement = document.createElement("input");
        // inElement.className = "input";
        outElement.id = item.identifier;
        outElement.name = item.identifier;
        outElement.type = "text";
        outElement.value = item.identifier;
        newNode.appendChild(outElement);

        nodeText = document.createElement("p");
        let mimeText ="";
        if (item.defaultValue && item.defaultValue.mimeType){mimeText = " (" +item.defaultValue.mimeType+ ")"}
        nodeText.appendChild(document.createTextNode(" Type of Output: " + item.dataType + mimeText));
        newNode.appendChild(nodeText);
        //$("div").append(inElement);
        if (typeof (newNode) === 'object') {element.appendChild(newNode)}
    });

    //element.innerHTML = inElement;
    let modal = document.getElementById("workModal");
    modal.style.display = "block";

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
