// This function builds the whole menu structure. For interaction with Server the menus have a short class in the style:
// First top menu (Parent): P1
// First child: C1
// Second child: C2
// First Item: I1...

const JSMENU = JSON.parse(jsonMenu);
const MENUS = Object.keys(JSMENU);
let FILTERMENU;
let parent;
let SELECTION = {};
let UNBLOCKED_IDS = JSON.parse(unblockedIds)


/* Loop through menus after load and build menu objects */
MENUS.forEach(menuBuilder);

/* build the parents of the menu*/
function menuBuilder(parent) {
    if (JSMENU[parent].total > 0) {  // check how many entries are in menu
        let parentHTML ="";
        let ctot = JSMENU[parent].total;
        for (let c = 1; c <= ctot; c++) {  // build child menu
            let child = 'C'+c.toString();
            let childHTML = _childBuilder(JSMENU[parent][child], child, parent);
            parentHTML += childHTML
        }
        FILTERMENU = document.getElementById("accordion").innerHTML +=
            `<h5 class='w3-hover-blue nav parent ${parent}'>${JSMENU[parent].name}</h5>
            <div id='${JSMENU[parent].name}'>${parentHTML}</div>`;
    }
}

/* build the childs of the menu / distinguishes the types of possible inputs*/
function _childBuilder(child, shortChild, shortParent) {
    let childHTML = "";
    let itemHTML = "";
    let inputName = "";
    let dDL = 8;  // dropDownLimit; when there are more items then build dropdown menu instead of separate items to click
/* build child with items for amount of items between 1 and dropDownLimit (dDL) */
    if (child.total > 1 && child.total <= dDL && !child.hasOwnProperty("type")) {
        itemHTML = itemBuilder(child, shortChild, shortParent);
        childHTML =
            `<h6 class='w3-hover-blue nav child ${shortParent} ${shortChild} childmenu'>${child.name}</h6>
            <div id='${child.name}'> ${itemHTML}</div>`
    }
/* build a dropdown list for childs with many items */
    else if (child.total > dDL && !child.hasOwnProperty("type")){
        itemHTML = itemBuilder(child, shortChild, shortParent);
        inputName = "Input"+child.name;
        childHTML =
            `<div class='dropdown'>
                <button onclick='dDMFunction("${child.name}")'
                    class='filter-btn-block w3-hover-blue nav child ${shortParent} ${shortChild}'>${child.name}
                </button>
                <div id='${child.name}' class='dropdown-content'>
                    <input type='text' placeholder='Search...'
                    id='${inputName}' onkeyup='dDMFilterFunction("${child.name}",
                    "${inputName}")' >${itemHTML}
                </div>
            </div>`
    }
    /* build special childs if type is defined */
    else if (child.hasOwnProperty("type")) {
        switch (child.type) {
            /* build three-way-button if type is boolean */
            case "bool":
                if (child.I1.total + child.I2.total == 0){break;}
                itemHTML = boolBuilder(child, shortChild, shortParent);
                childHTML =
                    `<div id='${child.name}'>
                        <h6 class='w3-hover-blue child ${shortParent} ${shortChild}'>
                        </h6>${child.name}&emsp;<i class='count s'>(${child.total})</i>
                    <div id='sliderwildcard'>${itemHTML} </div></div>`;
                break;
            /* build slider if type is slider */
            case "slider":
                if (child.selectable_min.toString() =='None' || child.selectable_max.toString()=='None'){break;}
                itemHTML = sliderBuilder(child, shortChild, shortParent);
                childHTML=
                    `<div id='${child.name}'>
                        <h6 class='w3-hover-blue child ${shortParent} ${shortChild}'>
                        </h6>${child.name}&emsp;<i class='count s'>(${child.total})</i>
                    <div id='sliderwildcard'>${itemHTML} </div></div>`;
                break;
            // }
            /* build calender if type is date */
            case "date":
                itemHTML = dateBuilder(child, shortChild, shortParent);
                // childHTML = itemHTML
                childHTML =
                    `<div id='${child.name}'>
                        <h6 class='w3-hover-blue nav child ${shortParent} ${shortChild}'>
                        </h6>${child.name}&emsp;<i><div class='count d'>(${child.total})</div></i>${itemHTML}
                    </div>`;
                break;
            // }
            /* build draw box if type is draw */
            case "draw":
                itemHTML = drawBuilder(child, shortChild, shortParent);
                childHTML=
                    `<div id='${child.name}'>
                        <h6 class='w3-hover-blue nav child ${shortParent} ${shortChild} count m${shortParent}'></h6>
                        ${child.name}&emsp;<i><div class='count'>(${child.total})</div></i>${itemHTML}
                    </div>`;
                return childHTML
                // break;
        }
    }
    else if (child.total === 1) {
        itemHTML = itemBuilder(child, shortChild, shortParent);
        childHTML =
            `<div id='${child.name}'><h6 class='w3-hover-blue child ${shortParent} ${shortChild}'></h6>
            ${child.name}: ${itemHTML}</div>`
    }
    return `<div id='subaccordion'> ${childHTML} </div>`
}

/* Builds a calender to select dates*/
function dateBuilder(child, shortChild, shortParent) {
    let minD = child.selectable_min.toString();
    let maxD = child.selectable_max.toString();
    let itemHTML =
        "<div class='date'></div>" +
        "<p>Date: <input type='date' id='datepicker "+shortParent+" "+shortChild+"'></p>";

    return itemHTML;
}

/* Build three connected radio buttons for false, true or no choice */
function boolBuilder(child, shortChild, shortParent) {
    let i, itemHTML = "";
    let shortItem, cItem;
    for (i = 1; i <= 2; i++) {
        shortItem = 'I'+ i.toString();
        cItem = child[shortItem];
        itemHTML += `<a class='w3-hover-blue btn ${shortParent} ${shortChild} ${shortItem}'
            onclick='itemButtonFunction(this,"${shortParent}","${shortChild}","${shortItem}")'>${cItem.name}&emsp;
            <i><span class='count'>(${cItem.total})</span></i>
            </a>`;
    }
    return itemHTML
  }

/* Prepare location in web site to build there a slider to select num values after loading of web site */
function sliderBuilder(child, shortChild, shortParent) {
    return `<div class='slider ${shortParent} ${shortChild}' name='${child.name}'
        minV='${ child.selectable_min.toString()}' maxv='${child.selectable_max.toString()}'></div>
        <div class="w3-row-padding">
            <div class="w3-half"><input id="slide-0${shortParent}${shortChild}" title="min-${child.name}"
                class="w3-input w3-hover-blue" style="width: 80px;" placeholder="One" type="number"></div>
            <div class="w3-half"><input id="slide-1${shortParent}${shortChild}" title="max-${child.name}"
                class="w3-input w3-hover-blue" style="width: 80px;" placeholder="two" type="number"></div>
        </div>`;  // respective field for min and max is accessed by 0 and 1 in id
}

/* build a button to open the draw menue */
function drawBuilder(child, shortChild, shortParent) {
    return `<a class='w3-hover-blue btn' onClick='drawPolygon("${shortParent}","${shortChild}","${child}")'
        id='toggle_draw' title='Click here to select from drawing'>Open draw menu</a>`;
}

/* build items to click on in the Filter Menu*/
function itemBuilder(child, shortChild, shortParent) {
    let i, itemHTML = "";
    let ctot = child.total;
    let shortItem, cItem;
    for (i = 1; i <= ctot; i++) {
        shortItem = 'I'+ i.toString();
        cItem = child[shortItem];
        itemHTML += `<a class='w3-hover-blue btn ${shortParent} ${shortChild} ${shortItem}'
            onclick='itemButtonFunction(this,"${shortParent}","${shortChild}","${shortItem}")'>${cItem.name}&emsp;
            <i><span class='count'>(${cItem.total})</span></i>
            </a>`;
    }
    return itemHTML
}

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

/* build sliders at the respective locations after the menu has loaded*/
$(document).ready(function (){
    let maxv, minv, input, input1, value;
    let handlesSlider =  document.getElementsByClassName('slider');
    [].slice.call(handlesSlider).forEach(function (slider) {
        maxv = parseFloat(slider.attributes.maxv.value);
        minv = parseFloat(slider.attributes.minv.value);
        noUiSlider.create(slider, {
            start: [minv, maxv],
            connect: true,
            range: {
                'min': [minv],
                'max': [maxv]
            },
        });
        slider.noUiSlider.on('update', function (values, handle) {
            input = document.getElementById('slide-'+handle+slider.classList[1]+slider.classList[2]);
            value = values[handle];
            input.value = values[handle];
        });
        input.addEventListener('change', function () {
            slider.noUiSlider.set([null, this.value])
        });
        input = document.getElementById('slide-0'+slider.classList[1]+slider.classList[2]);
        input.addEventListener('change', function () {
            slider.noUiSlider.set([this.value, null])
        });
    })
});

/**
 * Add onclick functionality to the items in the menu to update menu and show selection on map and table.
 * @param {Object} item
 * @param {string} shortParent
 * @param {string} shortChild
 * @param {string} shortItem
 */
function itemButtonFunction(item, shortParent, shortChild, shortItem) {
    let activeSibling = checkSiblings(item);
    SELECTION = buildSelection(activeSibling, shortParent, shortChild, shortItem);
    if (!jQuery.isEmptyObject(SELECTION)) {
        showSelectionOnMap(SELECTION);
        getCountFromServer(SELECTION);
    }
    else {
        selectedIds.quickMenu = null;
        showSelectionOnMap([]);
        getCountFromServer(SELECTION);
    }
}
/**
 * Add onclick functionality to update selection on map while drawing.
 * @param {string} shortParent
 * @param {string} shortChild
 * @param {*[]|string} selected_Id
 */
function mapSelectFunction(shortParent, shortChild, selected_Id) {
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
    $('#accordion').accordion({
        heightStyle: "content",
        active: false,
        collapsible: true,
    });
    while (document.getElementsByClassName('activeP')[0]) {
        document.getElementsByClassName('activeP')[0].classList.remove('activeP');
    }
    while (document.getElementsByClassName('activeC')[0]) {
        document.getElementsByClassName('activeC')[0].classList.remove('activeC');
    }
    while (document.getElementsByClassName('activeI')[0]) {
        document.getElementsByClassName('activeI')[0].classList.remove('activeI');
    }
    showSelectionOnMap([]);
    // TODO: store the initial numbers for each item and use it here instead of a new get request
    getCountFromServer({});

    selectedIds.resetIds()
    // reset draw menu:
    if (selectedFeatures !== undefined) {selectedFeatures.clear();}
    olmap.removeInteraction(draw);
    olmap.removeInteraction(modify);
    olmap.removeLayer(vector);
    filterbox_close();
}

/* send json Object with selection (i.e. P6:{C1:I1}) to server and receive IDs of selection for wfs */
function showSelectionOnMap(selection) {
    $.ajax({
        url: DEMO_VAR + "/home/filter_map_selection",
        dataType: 'json',
        data: {
            filter_map_selection: JSON.stringify(selection),
            'csrfmiddlewaretoken': csrf_token,
        }, // data sent with the post request
    })
        .done(function (json) {
            zoomToExt.extent = ol.proj.transformExtent(json['dataExt'], 'EPSG:4326', 'EPSG:3857');
            wfsLayerName = json['ID_layer'];
            selectedIds.quickMenu = json['IDs'];
            wfsPointSource.refresh();
    })
        .fail(function (e) {
            console.warn('Cannot update your map: ', e)
        })
}

/* send json Object with selection to server and get int(in a json) with amount of items back */
async function getCountFromServer(selection) {
    $.ajax({
        url: DEMO_VAR + "/home/filter_selection",
        dataType: 'json',
        data: {
            filter_selection: JSON.stringify(selection),
            'csrfmiddlewaretoken': csrf_token,
        }, // data sent with the post request
    })
        .done(function (json) {
            _updateCounts(json);
    });
}

/* updates the numbers for each item */
function _updateCounts(json) {
    let parent, child, item, itemHTML, jpc;
    for (parent in json) {
        child = '';
        for (child in json[parent]) {
            item = '';
            jpc = json[parent][child];
            for (item in jpc) {
                itemHTML = document.getElementsByClassName(`${parent} ${child} ${item}`);
                itemHTML[0].getElementsByClassName('count')[0].innerHTML = "("+jpc[item]+")";
                if (jpc[item] == '0'){
                    itemHTML[0].classList.add('w3-disabled')
                }
                else if (itemHTML[0].classList.contains('w3-disabled')) {
                    itemHTML[0].classList.remove('w3-disabled')
                }
            }
            if (item == '' && typeof(jpc) == 'number') {
                document.getElementsByClassName(`${parent} ${child} count`)[0].nextElementSibling.innerHTML = `(${jpc})`
            }
        }
    }
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
        $(item).addClass('activeI').siblings().removeClass('activeI');
        return true;
    }
}

/**
 * Checks if selected item is already activated, toggles the item as well as child and parent.
 * @param {boolean} activeSibling
 * @param {string} shortParent
 * @param {string} shortChild
 * @param {string} shortItem
 */
function buildSelection(activeSibling, shortParent, shortChild, shortItem, type) {
    // getElementsByClassName should be faster than QuerySelectAll
    let nodeListC = document.getElementsByClassName(`child ${shortChild} ${shortParent}`);
    let nodeListP = document.getElementsByClassName(`parent ${shortParent}`);
    if (activeSibling) {
        try {
            SELECTION[shortParent][shortChild]= shortItem;
        } catch (TypeError) {
            SELECTION[shortParent] = {[shortChild]: shortItem};
        }
        nodeListC[0].classList.add("activeC");
        nodeListP[0].classList.add("activeP");
    }
    else {
        nodeListC[0].classList.remove("activeC");
        delete SELECTION[shortParent][shortChild];
        if (jQuery.isEmptyObject(SELECTION[shortParent])) {
            nodeListP[0].classList.remove("activeP");
            delete SELECTION[shortParent]
        }
    }
    return SELECTION;
}
