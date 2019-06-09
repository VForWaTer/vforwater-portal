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
        console.log('bla: ', json)
        build_modal(json)
        },
    });
}

function build_modal(wpsInfo) {
    console.log('wpsInfo: ', wpsInfo)
    // console.log('wpsInfo[title]: ', wpsInfo[title])
    let element = document.getElementById("mod_head");
    let newElement = "";
    element.innerHTML = wpsInfo.title;
    element = document.getElementById("mod_abs");
    if (wpsInfo.abstract) {
        newElement = wpsInfo.abstract;
    } else {newElement = ""}
    element.innerHTML = newElement;

    element = document.getElementById("mod_in");
    console.log('input: ', wpsInfo.dataInputs)
    console.log('input: ', wpsInfo.dataInputs.length)
    console.log('element: ', element)
    let inElement = "";
    wpsInfo.dataInputs.forEach(function (item){
        inElement = document.createElement("input");
        console.log('item: ', item)
        if (item.dataType.includes('string')){

            console.log('string')
            inElement.setAttribute("type", "text");;
            //inElement.className = "input"

            console.log('1: ', typeof (inElement))
            console.log('1: ', item.title)
            //inElement.insertBefore(document.createTextNode(item.title), inElement.childNodes);
            console.log('2: ', inElement)
            //inElement.setAttribute("type", "text");
            console.log('3: ', inElement)
            console.log('3 element.childNodes[0]: ', element.parentNode)
            //element.insertBefore(inElement, element.parentNode)

        }
        if (item.minOccurs > 0) {inElement.required = true} //else {inElement.required = false}
        element.appendChild(inElement)
        console.log('inElement: ', inElement)
    })

    // if ()
    console.log('Element: ', element)
    //element.innerHTML = inElement;

    let modal = document.getElementById("workModal");
    modal.style.display = "block";



/*

 $("input[name=delete_id]").val(deleteVal);

$('.openmodal').click(function () {
  var deleteVal = $(this).attr('data-val');
  console.log(deleteVal)

    $('#myDeleteModal').modal({
        show: true
    });

    $("input[name=delete_id]").val(deleteVal);

});*/
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
