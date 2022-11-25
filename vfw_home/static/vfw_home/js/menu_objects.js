// This function builds the whole menu structure. For interaction with Server the menus have a short class in the style:
vfw.map.UNBLOCKED_IDS = JSON.parse(unblockedIds)


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


// TODO: When you decide to remove the wms map, use showAllPointsOnMap
function showAllPointsOnMap(){
   $.ajax({
       url: vfw.var.DEMO_VAR + "/home/menu",
       dataType: 'json',
       data: {
           all_datasets: 'True',
           'csrfmiddlewaretoken': csrf_token,
       }, // data sent with the post request
       })
       .done(function (json) {
       })

}

/* button to remove the selection in the filter menu, reset values on items, and show all points on map */
function reset_filter(){
    showSelectionOnMap([]);
    // TODO: store the initial numbers for each item and use it here instead of a new get request
    getCountFromServer({});

    vfw.var.obj.selectedIds.resetIds()
    // reset draw menu:
    if (selectedFeatures !== undefined) {selectedFeatures.clear();}
    olmap.removeInteraction(draw);
    olmap.removeInteraction(modify);
    olmap.removeLayer(selectionLayer);
    drawfilter_close();
    // resetDraw();  TODO: There is a function for the last five commands. Why is this not working?
}

/** update objects on map according to filter results */
vfw.map.updateMapSelection = function (json) {
    vfw.map.control.zoomToExt.extent = ol.proj.transformExtent(json['dataExt'], 'EPSG:4326', 'EPSG:3857');
    vfw.map.vars.wfsLayerName = json['ID_layer'];
    vfw.var.obj.selectedIds.quickMenu = json['IDs'];
    vfw.map.source.wfsPointSource.refresh();
}
