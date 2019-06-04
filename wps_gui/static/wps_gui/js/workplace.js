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
    dropletCopy.id = "dz"+sessionStorage.getItem("dz_count");
    dropletCopy.classList.add('tool-btn');
    dropletCopy.style.left = ev.offsetX + "px";
    dropletCopy.style.top = ev.offsetY + "px";
    // ev.dataTransfer.setDragImage(dropletCopy, ev.offsetX + "px", ev.offsetY + "px")
    ev.target.appendChild(dropletCopy);
}

function wpsprocess(service, identifier) {
    console.log("service: ", service)
    console.log("identifier: ", identifier)
     $.ajax({
        url: DEMO_VAR+"/wps_gui/processview",
        //url: DEMO_VAR+"/wps_gui/"+service+"/process",
        dataType   : 'json',
        data: {
            processview: JSON.stringify({id: identifier, serv: service}),
            'csrfmiddlewaretoken': csrf_token,
        }, // data sent with the post request
        success: function (json) {
            console.log('wpsprocess')
            console.log(json)
            //updateCounts(json);
        },
    });
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
