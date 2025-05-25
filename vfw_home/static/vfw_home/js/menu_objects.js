/*
 * Project Name: V-FOR-WaTer
 * Author: Marcus Strobl
 * Contributors:
 * License: MIT License
 */


/* Drop Down Menu Button Function to toggle what is shown in it*/
function dDMFunction(dropDownName) {
    document.getElementById(dropDownName).classList.toggle("show");
}

/* Drop Down Menu Filter Function - Search functionality */
function dDMFilterFunction(dropDownName, inputName) {
    let input = document.getElementById(inputName);
    let filter = input.value.toUpperCase();
    let div = document.getElementById(dropDownName);
    let a = div.getElementsByTagName("a");
    let aLen = a.length;
    for (let i = 0; i < aLen; i++) {
        a[i].style.display = a[i].innerHTML.toUpperCase().indexOf(filter) > -1 ? "" : "none";
    }
}

function showAllPointsOnMap(){
   $.ajax({
       url: vfw.var.DEMO_VAR + "/home/menu",
       dataType: 'json',
       data: {
           all_datasets: 'True',
           'csrfmiddlewaretoken': vfw.var.csrf_token,
       }, // data sent with the post request
       })
       .done(function (json) {
       })

}

/** update objects on map according to filter results */
vfw.map.updateMapSelection = function (json) {
    /** the following code makes only sense on /home/. */
    if (window.location.pathname == `/home/`) {
        vfw.map.control.zoomToExt.extent = ol.proj.transformExtent(json['dataExt'], 'EPSG:4326', 'EPSG:3857');
        vfw.var.DATA_LAYER_NAME = json['ID_layer'];
        vfw.var.AREAL_DATA_LAYER_NAME = json['areal_ID_layer'];
        vfw.var.obj.selectedIds.quickMenu = json['IDs'];
        console.log('update map')
        vfw.map.source.wfsPointSource.refresh();
        vfw.map.source.wfsArealSource.refresh();
    }
}
