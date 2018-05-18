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
        for (let c = 1; c <= jsMenu[parent].total; c++) {  // build child menu
            let child = 'C'+c.toString();
            let childHTML = childBuilder(eval("jsMenu[parent]."+[child]), child, parent);
            // console.log('  *** ** *' + parentHTML)
            parentHTML = parentHTML + childHTML
        }
        filterMenu = document.getElementById("accordion").innerHTML +=
            "<h5 class='respo-hover-blue nav parent "+parent+"'>" + jsMenu[parent].name + "</h5>" +
            "<div id='" + jsMenu[parent].name + "'>" +
                "<div id='subaccordion'> "+parentHTML+"" +
            "   </div>" +
            "</div>";
    }
}

/* build the childs of the menu / distinguishes the types of possible inputs*/
function childBuilder(child, shortChild, shortParent) {
    let childHTML = "";
    let itemHTML = "";
    let inputName = "";
    let dDL = 8;  // dropDownLimit
/* build child with items for amount of items between 1 and dropDownLimit (dDL) */
    if (child.total > 1 && child.total <= dDL && !child.hasOwnProperty("type")) {
        itemHTML = itemBuilder(child, shortChild, shortParent);
        childHTML =
            "<h6 class='respo-hover-blue nav child "+shortParent+" "+shortChild+" childmenu'>" + child.name + "</h6>" +
            "<div id='" + child.name + "'>" +
                "<div> "+itemHTML+"" +
            "   </div>" +
            "</div>"
    }
/* build a dropdown list for childs with many items */
    else if (child.total > dDL && !child.hasOwnProperty("type")){
        itemHTML = itemBuilder(child, shortChild, shortParent);
        inputName = "Input"+child.name;
        childHTML =
            "<div class='dropdown'>" +
                "<button onclick='dDMFunction(\""+child.name+"\")' class='filter-btn-block respo-hover-blue nav child "+
                shortParent+" "+shortChild+"'>" + child.name + "</button>" +
                "<div id='" + child.name + "' class='dropdown-content'>" +
                    "<input type='text' placeholder='Search...' id = '"+inputName+"'" +
                        "onkeyup='dDMFilterFunction(\""+child.name+"\", \""+inputName+"\")' >" +
                    "<div> "+itemHTML+"" +
                    "</div>" +
                "</div>" +
            "</div>"
    }
/* build special childs if type is defined */
    else if (child.hasOwnProperty("type")) {
        /* build slider if type is slider */
        if (child.type === "slider") {
            itemHTML = sliderBuilder(child, shortChild, shortParent);
            childHTML=
            "<h6 class='respo-hover-blue nav child "+shortParent+" "+shortChild+"'>" + child.name+ "&emsp;<i><div class='count s'>(" + child.total + ")</div></i></h6>" +
            "<div id='" + child.name + "'>" +
                "<div id='sliderwildcard'> "+itemHTML+
            " </div>" +
            "</div>"
        }
/* build calender if type is date */
        else if (child.type === "date") {
            itemHTML = dateBuilder(child, shortChild, shortParent);
            // childHTML = itemHTML
            childHTML =
            "<h6 class='respo-hover-blue nav child "+shortParent+" "+shortChild+"'>" + child.name+ "&emsp;<i><div class='count d'>(" + child.total + ")</div></i></h6>" +
            "<div id='" + child.name + "'>" +
                "<div> "+itemHTML+
                // "<div id='datewildcard'> "+itemHTML+
            " </div>" +
            "</div>"
        }
    }
    else if (child.total === 1) {
        itemHTML = itemBuilder(child, shortChild, shortParent);
        childHTML =
            "<div id='"+child.name+"'>" +
            "<h6 class='respo-hover-blue child "+shortParent+" "+shortChild+"'></h6>" +
                ""+child.name +": "+itemHTML+
            "</div>"
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
    let minV = child.selectable_min.toString();
    let maxV = child.selectable_max.toString();

    // var handlesSlider = document.getElementById('slider-handles');
    // // var document.getElementById(child.name).addEventListener("click", function(){
    // // document.getElementById("demo").innerHTML = "Hello World";
    // // });
    //     console.log(handlesSlider)
    // var itemHTML =
    //     "<div class='container' data-role='rangeslider'>"+child.name+"" +
    //      // "<button onclick="+onclick_slider()+">Click me</button>"+
    //     "</div>"
    return `<div class='slider ${shortParent} ${shortChild}' name='${child.name}' minV='${minV}' maxv='${maxV}'></div>`;
    // Two Textfields for numbers:
    // var itemHTML =
    //     "<div >(min/max: "+minV+"/"+maxV+")" +
    //     "<input type='number' name='price-min' id='price-min' value='"+minV+"' min='"+minV+"' max='"+maxV+"'>" +
    //     "<input type='number' name='price-max' id='price-max' value='"+maxV+"' min='"+minV+"' max='"+maxV+"'>" +
    //     "<input type='submit' data-inline='true' value='Submit'>"+
    //     "</div>"

}

/* build items to click on in the Filter Menu*/
function itemBuilder(child, shortChild, shortParent) {
    let i, itemHTML = "";
    for (i = 1; i <= child.total; i++) {
        let shortItem = 'I'+ i.toString();
        let cItem = eval("child." + shortItem);
        let listHTML =
                "<a class='respo-hover-blue btn "+shortParent+" "+shortChild+" "+shortItem+"' " +
                    "onclick='itemButtonFunction(this,\""+ shortParent+"\",\""+ shortChild+"\",\""+ shortItem+"\")'>" +
                    cItem.name + "&emsp;" +"<i><div class='count'>(" + cItem.total + ")</div></i>"+
                "</a>";
        itemHTML = itemHTML + listHTML;
    }
    return itemHTML
}

/* Drop Down Menu Button Function to toggle what is shown in it*/
function dDMFunction(dropDownName) {
    document.getElementById(dropDownName).classList.toggle("show");
}

/* Drop Down Menu Filter Function - Search functionality */
function dDMFilterFunction(dropDownName, inputName) {
    let input, filter, div, a;
    input = document.getElementById(inputName);
    filter = input.value.toUpperCase();
    div = document.getElementById(dropDownName);
    a = div.getElementsByTagName("a");
    for (let i = 0; i < a.length; i++) {
        if (a[i].innerHTML.toUpperCase().indexOf(filter) > -1) {
            a[i].style.display = "";
        } else {
            a[i].style.display = "none";
        }
    }
}

/* build sliders at the respective locations after the menu has loaded*/
$(document).ready(function (){
    let handlesSlider =  document.getElementsByClassName('slider');
    for (let s = 0; s < handlesSlider.length; s++){
        let maxv = parseFloat(handlesSlider[s].attributes.maxv.value);
        let minv = parseFloat(handlesSlider[s].attributes.minv.value);
        noUiSlider.create(handlesSlider[s], {
            start: [minv, maxv],
            tooltips:  true ,
            // behaviour: 'tap-drag',
            // connect: true,
            range: {
                'min': [ minv ],
                'max': [ maxv ]
            },
            // pips: { // Show a scale with the slider
		// mode: 'steps',
		// stepped: true,
		// density: 4
	// }
        });

    }
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
        wfsPointLayer.changed()
        // showAllPointsOnMap();
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
           console.log('response of showAllPointsOnMap: ', json)
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
    wfsPointLayer.changed()
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
            selectedIds = json['all_filters'];
            wfsPointLayer.changed()
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
    let parent, child, item;
    for (parent in json) {
        child = '';
        for (child in json[parent]) {
            item = '';
            for (item in json[parent][child]) {
                itemHTML = eval("document.getElementsByClassName('"+parent+" "+ child+ " "+ item+"')");
                itemHTML[0].getElementsByClassName('count')[0].innerHTML = "("+json[parent][child][item]+")"
                if (json[parent][child][item] == '0'){
                // console.log('candidate for a "disable" option? itemHTML[0]', itemHTML[0], json[parent][child][item])
                //  respo-disabled classList.add
                    itemHTML[0].classList.add('respo-disabled')
                }
                else if (itemHTML[0].classList.contains('respo-disabled')) {
                    itemHTML[0].classList.remove('respo-disabled')
                }
            }
        }
    }
}

/* checks if one of the siblings of the clicked item is active */
function checkSiblings(item) {
    let activeSibling;
    if (item.classList.contains('activeI')) {
        item.classList.remove('activeI');
        activeSibling = false;
    } else {
        // itemList = item.parentElement.getElementsByClassName("active");
        $(item).addClass('activeI').siblings().removeClass('activeI');
        // item.classList.add('active');
        activeSibling = true;
    }
    return activeSibling;
}

/* checks if selected item is already activated, toggles the item as well as child and parent */
function buildSelection(activeSibling, shortParent, shortChild, shortItem) {
    // getElementsByClassName should be faster than QuerySelectAll
    let nodeListC = eval("document.getElementsByClassName('child "+shortChild+" "+shortParent+"')");
    let nodeListP = eval("document.getElementsByClassName('parent "+shortParent+"')");

    if (activeSibling) {
        try {
            eval('selection.' + shortParent + '.' + shortChild + ' = shortItem');
        } catch (TypeError) {
            selection[shortParent] = {[shortChild]: shortItem};
        }
        nodeListC[0].classList += " activeC";
        nodeListP[0].classList += " activeP";
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
