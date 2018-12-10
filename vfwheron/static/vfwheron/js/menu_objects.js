// This function builds the whole menu structure. For interaction with Server the menus have a short class in the style:
// First top menu (Parent): P1
// First child: C1
// Second child: C2
// First Item: I1...

const jsMenu = JSON.parse(jsonMenu);
const menues = Object.keys(jsMenu);
let filterMenu;
let parent;
let selection = {};
console.log(jsMenu)

// TODO: To improve performance onclick try to build variables P1C1I1, P1C1T2,... here and assign an id to the
// TODO: respective value. In 'updateCounts' you can access the values then directly with the ID; But the following isn't working
// Predefine variables to assign IDs for the filter elements that will be changed on every filter selection:
// for (let p in jsMenu){
//     for (let m = 1; m <= jsMenu[p].total; m++) {
//         let c = 'C'+m.toString()
//         for (let n = 1; n <= jsMenu[p][c].total; n++) {
//             let i = 'I'+n.toString()
//             eval("let "+p+c+i)
//         }
//     }
// }

/* Loop through menues after load and build menu objects */
menues.forEach(menuBuilder);

/* build the parents of the menu*/
function menuBuilder(parent) {
    if (jsMenu[parent].total > 0) {  // check how many entries are in menu
        let parentHTML ="";
        let ctot = jsMenu[parent].total;
        for (let c = 1; c <= ctot; c++) {  // build child menu
            let child = 'C'+c.toString();
            let childHTML = childBuilder(jsMenu[parent][child], child, parent);
            // let childHTML = childBuilder(eval("jsMenu[parent]."+[child]), child, parent);
            // console.log('  *** ** *' + parentHTML)
            parentHTML += `<div id='subaccordion'> ${childHTML}   </div>`
        }
        filterMenu = document.getElementById("accordion").innerHTML +=
            `<h5 class='respo-hover-blue nav parent ${parent}'>${jsMenu[parent].name}</h5>
            <div id='${jsMenu[parent].name}'>${parentHTML}</div>`;
    }
}

/* build the childs of the menu / distinguishes the types of possible inputs*/
function childBuilder(child, shortChild, shortParent) {
    let childHTML = "";
    let itemHTML = "";
    let inputName = "";
    let dDL = 8;  // dropDownLimit; when there are more items then build dropdown menue instead of seperate items to click
/* build child with items for amount of items between 1 and dropDownLimit (dDL) */
    if (child.total > 1 && child.total <= dDL && !child.hasOwnProperty("type")) {
        itemHTML = itemBuilder(child, shortChild, shortParent);
        childHTML =
            `<h6 class='respo-hover-blue nav child ${shortParent} ${shortChild} childmenu'>${child.name}</h6>
            <div id='${child.name}'> ${itemHTML}</div>`
    }
/* build a dropdown list for childs with many items */
    else if (child.total > dDL && !child.hasOwnProperty("type")){
        itemHTML = itemBuilder(child, shortChild, shortParent);
        inputName = "Input"+child.name;
        childHTML =
            `<div class='dropdown'>
                <button onclick='dDMFunction("${child.name}")' 
                    class='filter-btn-block respo-hover-blue nav child ${shortParent} ${shortChild}'>${child.name}
                </button>
                <div id='${child.name}' class='dropdown-content'>
                    <input type='text' placeholder='Search...' 
                    id='${inputName}'onkeyup='dDMFilterFunction("${child.name}", 
                    "${inputName}")' >${itemHTML}
                </div>
            </div>`
    }
/* build special childs if type is defined */
    else if (child.hasOwnProperty("type")) {
/* build slider if type is slider */
        switch (child.type) {
            case "slider":
                if (child.selectable_min.toString() =='None' || child.selectable_max.toString()=='None'){break;}
                itemHTML = sliderBuilder(child, shortChild, shortParent);
                childHTML=
                    `<div id='${child.name}'>
                        <h6 class='respo-hover-blue child ${shortParent} ${shortChild}'>
                        </h6>${child.name}&emsp;<i class='count s'>(${child.total})</i>
                    <div id='sliderwildcard'>${itemHTML} </div></div>`;
                break;
            // }
/* build calender if type is date */
        // else if (child.type === "date") {
            case "date":
                itemHTML = dateBuilder(child, shortChild, shortParent);
                // childHTML = itemHTML
                childHTML =
                    `<div id='${child.name}'>
                        <h6 class='respo-hover-blue nav child ${shortParent} ${shortChild}'>
                        </h6>${child.name}&emsp;<i><div class='count d'>(${child.total})</div></i>${itemHTML}
                    </div>`;
                break;
        // }
/* build draw box if type is map */
        // else if (child.type === "draw") {
            case "draw":
                itemHTML = drawBuilder(child, shortChild, shortParent);
                childHTML=
                    `<div id='${child.name}'>
                        <h6 class='respo-hover-blue nav child ${shortParent} ${shortChild} count m${shortParent}'></h6>
                        ${child.name}&emsp;<i><div class='count'>(${child.total})</div></i>${itemHTML}
                    </div>`;
                break;
        }
    }
    else if (child.total === 1) {
        itemHTML = itemBuilder(child, shortChild, shortParent);
        childHTML =
            `<div id='${child.name}'><h6 class='respo-hover-blue child ${shortParent} ${shortChild}'></h6>
            ${child.name}: ${itemHTML}</div>`
    }
    return childHTML
}

/* Builds a calender to select dates*/
function dateBuilder(child, shortChild, shortParent) {
    let minD = child.selectable_min.toString();
    let maxD = child.selectable_max.toString();
    let itemHTML =
        "<div class='date'></div>" +
        "<p>Date: <input type='date' id='datepicker "+shortParent+" "+shortChild+"'></p>";

    // $( function() {
    //   $( "#datepicker" ).datepicker(
    //       console.log('Datepicker')
    //   );
    // } );

    return itemHTML;
}

/* Prepair location in web site to build there a slider to select num values after loading of web site */
function sliderBuilder(child, shortChild, shortParent) {
    return `<div class='slider ${shortParent} ${shortChild}' name='${child.name}' 
        minV='${ child.selectable_min.toString()}' maxv='${child.selectable_max.toString()}'></div>
        <div class="respo-row-padding">
            <div class="respo-half"><input id="slide-0${shortParent}${shortChild}" title="min-${child.name}" 
                class="respo-input respo-hover-blue" style="width: 80px;" placeholder="One" type="number"></div>
            <div class="respo-half"><input id="slide-1${shortParent}${shortChild}" title="max-${child.name}" 
                class="respo-input respo-hover-blue" style="width: 80px;" placeholder="two" type="number"></div>
        </div>`;  // respective field for min and max is accessed by 0 and 1 in id
}

/* build a button to open the draw menue */
function drawBuilder(child, shortChild, shortParent) {
    return `<a class='respo-hover-blue btn' onClick='drawPolygon("${shortParent}","${shortChild}","${child}")' 
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
        itemHTML += `<a class='respo-hover-blue btn ${shortParent} ${shortChild} ${shortItem}' 
            onclick='itemButtonFunction(this,"${shortParent}","${shortChild}","${shortItem}")'>${cItem.name}&emsp;
            <i><div class='count'>(${cItem.total})</div></i>
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
            // tooltips: true,
            // tooltips: [true, wNumb({decimals: 0})],
            // behaviour: 'tap-drag',
            connect: true,
            range: {
                'min': [minv],
                'max': [maxv]
            },
            // pips: { // Show a scale with the slider
            // mode: 'steps',
            // stepped: true,
            // density: 4
            // }
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

// $(document).ready(addDatePicker);
// function addDatePicker() {
//     var handlesDate =  document.getElementsByClassName('date');
//     console.log('handlesDate: ', handlesDate)
//     for (let d = 0; d < handlesDate.length; d++) {
//         console.log('date: ', handlesDate[d])
//         console.log("document."+handlesDate[d].id+".datepicker()")
//         eval("document."+handlesDate[d].id+".datepicker()");
//         // $( "#handlesDate[i].name" ).datepicker();
//     }
//   } ;

/* Add onclick functionality to the items in the menu to update menu and show selection on map */
function itemButtonFunction(item, shortParent, shortChild, shortItem) {
    let activeSibling = checkSiblings(item);
    selection = buildSelection(activeSibling, shortParent, shortChild, shortItem);
    if (!jQuery.isEmptyObject(selection)) {
        showSelectionOnMap(selection);
        getCountFromServer(selection);
    }
    else {
        selectedIds = null;
        showSelectionOnMap(0);
        getCountFromServer(selection);
        // clusterLayer.changed()
        // showAllPointsOnMap();
    }
}
/* Add onclick functionality to the items in the menu to update menu and show selection on map */
function mapSelectFunction(shortParent, shortChild, selected_Id) {
    let activeSibling = (selected_Id.length > 0) ? true:false;
    let mapselection = buildSelection(activeSibling, shortParent, shortChild, selected_Id);
    if (!jQuery.isEmptyObject(selection)) {
        showSelectionOnMap(selection);
        getCountFromServer(mapselection);
    }
    else {
        selectedIds = null;
        showSelectionOnMap(0);
        getCountFromServer(mapselection);
    }
}

// TODO: When you decide to remove the wms map, use showAllPointsOnMap
function showAllPointsOnMap(){
   $.ajax({
       url: DEMO_VAR + "/vfwheron/menu",
       dataType: 'json',
       data: {
           all_datasets: 'True',
           'csrfmiddlewaretoken': csrf_token,
       }, // data sent with the post request
       success: function (json) {
       },
   });
//    document.getElementById("workspace").innerHTML += "<li class='respo-padding' id='"+selectedData+"'><span class='respo-medium'>"+selectedData+"</span><a href='javascript:void(0)' onclick=this.parentElement.remove(); class='respo-hover-white respo-right'><i class='fa fa-remove fa-fw'></i></a><br></li>";
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
    selectedIds = null;
    showSelectionOnMap(0);
    // TODO: store the inicial numbers for each item and use it here instead of a new get request
    getCountFromServer({});
    // reset draw menu:
    selected_Id = [];
    selectedFeatures.clear();
    olmap.removeInteraction(draw);
    olmap.removeInteraction(modify);
    olmap.removeLayer(vector);
    // clusterLayer.changed()
}

/* send json Object with selection (i.e. P6:{C1:I1}) to server and receive IDs of selection for wfs */
function showSelectionOnMap(selection) {
    $.ajax({
        url: DEMO_VAR + "/vfwheron/menu",
        dataType: 'json',
        data: {
            filter_selection_map: JSON.stringify(selection),
            'csrfmiddlewaretoken': csrf_token,
        }, // data sent with the post request
        success: function (json) {
            zoomToExt.extent = json['dataExt'];
            wfsLayerName = json['ID_layer'];
            selectedIds = json['IDs'];
            wfsPointSource.clear();
            // document.getElementById()
            // clusterLayer.changed()
        },
    });
//    document.getElementById("workspace").innerHTML += "<li class='respo-padding' id='"+selectedData+"'><span class='respo-medium'>"+selectedData+"</span><a href='javascript:void(0)' onclick=this.parentElement.remove(); class='respo-hover-white respo-right'><i class='fa fa-remove fa-fw'></i></a><br></li>";
}

/* send json Object with selection to server and get int(in a json) with amount of items back */
function getCountFromServer(selection) {
    $.ajax({
        url: DEMO_VAR+"/vfwheron/menu",
        dataType   : 'json',
        data: {
            filter_selection: JSON.stringify(selection),
            'csrfmiddlewaretoken': csrf_token,
        }, // data sent with the post request
        success: function (json) {
            updateCounts(json);
        },
    });
//    document.getElementById("workspace").innerHTML += "<li class='respo-padding' id='"+selectedData+"'><span class='respo-medium'>"+selectedData+"</span><a href='javascript:void(0)' onclick=this.parentElement.remove(); class='respo-hover-white respo-right'><i class='fa fa-remove fa-fw'></i></a><br></li>";
}

/* updates the numbers for each item */
function updateCounts(json) {
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
                    itemHTML[0].classList.add('respo-disabled')
                }
                else if (itemHTML[0].classList.contains('respo-disabled')) {
                    itemHTML[0].classList.remove('respo-disabled')
                }
            }
            if (item == '' && typeof(jpc) == 'number') {
                document.getElementsByClassName(`${parent} ${child} count`)[0].nextElementSibling.innerHTML = `(${jpc})`
            }
        }
    }
}

/* checks if one of the siblings of the clicked item is active */
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

/* checks if selected item is already activated, toggles the item as well as child and parent */
function buildSelection(activeSibling, shortParent, shortChild, shortItem, type) {
    // getElementsByClassName should be faster than QuerySelectAll
    let nodeListC = document.getElementsByClassName(`child ${shortChild} ${shortParent}`);
    let nodeListP = document.getElementsByClassName(`parent ${shortParent}`);
    if (activeSibling) {
        try {
            selection[shortParent][shortChild]= shortItem;
        } catch (TypeError) {
            selection[shortParent] = {[shortChild]: shortItem};
        }
        nodeListC[0].classList.add("activeC");
        nodeListP[0].classList.add("activeP");
    }
    else {
        nodeListC[0].classList.remove("activeC");
        delete selection[shortParent][shortChild];
        if (jQuery.isEmptyObject(selection[shortParent])) {
            nodeListP[0].classList.remove("activeP");
            delete selection[shortParent]
        }
    }
    return selection;
}

// implented in vfw.js
function many_datasets() {
    workspace_dataset(JSON.stringify(selectedIds))
}

