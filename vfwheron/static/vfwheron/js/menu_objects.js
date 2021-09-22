// This function builds the whole menu structure. For interaction with Server the menus have a short class in the style:
// First top menu (Parent): P1
// First child: C1
// Second child: C2
// First Item: I1...

let parent;
let SELECTION = {};
let UNBLOCKED_IDS = JSON.parse(unblockedIds)
// let selectedIds = {
//     map: null,
//     filter: null,
//     set map(idList) {
//         this.map = idList;
//     },
//     get map() {
//         return this.map
//     },
//     set filter(idList) {
//         this.filter = idList;
//     },
//     get filter() {
//         return this.filter
//     },
//     updateFilterTable: function () {
//         return this.selected
//     }
// };


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

/**
 * Add onclick functionality to update selection on map while drawing.
 * @param {*[]|string} selected_Id
 */
function mapSelectFunction(selected_Id) {
    console.log('from mapSelectFunction: selected_Id: ', selected_Id)
    let activeSibling = (selected_Id.length > 0) ? true:false;
    let mapselection = buildSelection(activeSibling, shortParent, shortChild, selected_Id);
    if (!jQuery.isEmptyObject(SELECTION)) {
        showSelectionOnMap(SELECTION);
        getCountFromServer(mapselection);
    }
    else {
        selectedIds.quickMenu = null;
        showSelectionOnMap([]);
        getCountFromServer(mapselection);
    }
}

// TODO: When you decide to remove the wms map, use showAllPointsOnMap
function showAllPointsOnMap(){
   $.ajax({
       url: DEMO_VAR + "/home/menu",
       dataType: 'json',
       data: {
           all_datasets: 'True',
           'csrfmiddlewaretoken': csrf_token,
       }, // data sent with the post request
       })
       .done(function (json) {
       })

//    document.getElementById("workspace").innerHTML += "<li class='w3-padding' id='"+selectedData+"'><span class='w3-medium'>"+selectedData+"</span><a href='javascript:void(0)' onclick=this.parentElement.remove(); class='w3-hover-white w3-right'><i class='fa fa-remove fa-fw'></i></a><br></li>";
}

/* button to remove the selection in the filter menu, reset values on items, and show all points on map */
function reset_filter(){
    showSelectionOnMap([]);
    // TODO: store the initial numbers for each item and use it here instead of a new get request
    getCountFromServer({});

    selectedIds.resetIds()
    // reset draw menu:
    if (selectedFeatures !== undefined) {selectedFeatures.clear();}
    olmap.removeInteraction(draw);
    olmap.removeInteraction(modify);
    olmap.removeLayer(dataPointsVectorLayer);
    drawfilter_close();
    // resetDraw();  TODO: There is a function for the last five commands. Why is this not working?
    // clusterLayer.changed()
}

/** update objects on map according to filter results */
function updateMapSelection(json) {
    zoomToExt.extent = ol.proj.transformExtent(json['dataExt'], 'EPSG:4326', 'EPSG:3857');
    wfsLayerName = json['ID_layer'];
    selectedIds.quickMenu = json['IDs'];
    wfsPointSource.refresh();
}

/**
 * Checks if one of the siblings of the clicked item is active.
 * @param {object} item
 */
function checkSiblings(item) {
    if (item.classList.contains('activeI')) {
        item.classList.remove('activeI');
        return false;
    } else {
        // itemList = item.parentElement.getElementsByClassName("active");
        $(item).addClass('activeI').siblings().removeClass('activeI');
        // item.classList.add('active');
        return true;
    }
}
