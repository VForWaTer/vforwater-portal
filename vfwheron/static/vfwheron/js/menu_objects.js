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

menues.forEach(menuBuilder,jsMenu);

function menuBuilder(parent) {
    if (jsMenu[parent].total > 0) {  // check how many entries are in menu
        let parentHTML ="";
        for (let i = 1; i <= jsMenu[parent].total; i++) {  // build child menu
            let child = 'C'+i.toString();
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
        console.log('jsMenu[parent].name: ', jsMenu[parent].name)
        // document.getElementById("accordion").innerHTML +=
        //     "<button class='new_accord'>" + jsMenu[item].name + "</button>" +
        //     "<div class='panel'>" +
        //     "<div> "+childHTML+"</div>" +
        //     "</div>"
        //            "<button class='new_accord'>" + jsMenu[item].name + "</button>" +
            // "<div class='panel'>" +
            // "<div> "+childHTML+"</div>" +
            // "</div>"
    }
        // "ui-corner-top ui-accordion-header-collapsed ui-corner-all ui-state-default ui-accordion-icons'" +
        // "id='fm"+index+"' value="+jsMenu[item].chosen +">" + jsMenu[item].name + "

    // document.getElementById("jsMenu").innerHTML += "<h5 " +
    //     "class='respo-hover-blue nav ui-accordion-header " +
    //     "ui-corner-top ui-accordion-header-collapsed ui-corner-all ui-state-default ui-accordion-icons'" +
    //     "id='fm"+index+"' value="+jsMenu[item].chosen +">" + jsMenu[item].name + "</h5>"
    //
}

function childBuilder(child, shortChild, shortParent) {
    let childHTML = "";
    let itemHTML = "";
    let dDL = 8;  // dropDownLimit
    // console.log('child in childbuilder: ', shortChild)
    if (child.total > 1 && child.total <= dDL && !child.hasOwnProperty("type")) {
        itemHTML = itemBuilder(child, shortChild, shortParent);
        childHTML =
            "<h6 class='respo-hover-blue nav child "+shortParent+" "+shortChild+" childmenu'>" + child.name + "</h6>" +
            "<div id='" + child.name + "'>" +
                "<div> "+itemHTML+"" +
            "   </div>" +
            "</div>"
    }
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
    else if (child.hasOwnProperty("type")) {
        if (child.type === "slider") {
            itemHTML = sliderBuilder(child, shortChild, shortParent);
            childHTML=
            "<h6 class='respo-hover-blue nav child "+shortParent+" "+shortChild+"'>" + child.name+ "&emsp;<i>(" + child.total + ")</i>" + "</h6>" +
            "<div id='" + child.name + "'>" +
                "<div id='sliderwildcard'> "+itemHTML+
            " </div>" +
            "</div>"
        }
        else if (child.type === "date") {
            itemHTML = dateBuilder(child, shortChild, shortParent);
            childHTML = itemHTML
        }
    }
    else if (child.total === 1) {
        itemHTML = itemBuilder(child, shortChild, shortParent);
        childHTML =
            "<div id='"+child.name+"'>" +
                "<b> "+child.name +": </b>"+itemHTML+
            "</div>"
    }
    return childHTML
}

function dateBuilder(child, shortChild, shortParent) {
    let minD = child.selectable_min.toString();
    let maxD = child.selectable_max.toString();
    let itemHTML =
        "<p>Date: <input type='text' id='datepicker "+shortParent+" "+shortChild+"'></p>";

    $( function() {
      $( "#datepicker" ).datepicker();
    } );

    return itemHTML;
}

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

function itemBuilder(child, shortChild, shortParent) {
    let i, itemHTML = "";
    for (i = 1; i <= child.total; i++) {
        let shortItem = 'I'+ i.toString();
        let cItem = eval("child." + shortItem);
        // console.log('itemBuilder child:', child)
        // console.log(' + + + + kaljsgdlagafhg ', cItem, shortItem, shortChild, shortParent)
        // if (cItem.chosen){
        //     active = 'active'
        // } else {
        //     active = ''
        // }
        let listHTML =
            // "<div>" +
                // "<label class='container'>"+
                // "<input type='radio' checked='checked' name='radio'>" +
                "<a class='respo-hover-blue btn "+shortParent+" "+shortChild+" "+shortItem+"' " +
                    "onclick='buttonFunction(this,\""+ shortParent+"\",\""+ shortChild+"\",\""+ shortItem+"\")'>" +
                    cItem.name + "&emsp;" +"<i>(" + cItem.total + ")</i>"+
                "</a>";
            // "   </label>" +
            // "</div>";
        itemHTML = itemHTML + listHTML;
        // console.log('haha!: ', listHTML.getElementsByClassName("btn"))
    }
    return itemHTML
}

function checkBoxBuilder(child, shortChild, shortParent) {
    let cItem = eval("child.I");
    let listHTML =
        "<a class='respo-hover-blue'>" + cItem.name +
        "</a>";
//     <label class="container">One
//   <input type="checkbox" checked="checked">
//   <span class="checkmark"></span>
// </label>;
    return listHTML;
}


function dDMFunction(dropDownName) {
    document.getElementById(dropDownName).classList.toggle("show");
}

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

$(document).ready(function (){
    let handlesSlider =  document.getElementsByClassName('slider');
    for (let i = 0; i < handlesSlider.length; i++){
        let maxv = parseFloat(handlesSlider[i].attributes.maxv.value);
        let minv = parseFloat(handlesSlider[i].attributes.minv.value);
        noUiSlider.create(handlesSlider[i], {
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
//     for (var i = 0; i < handlesDate.length; i++) {
//         console.log('date: ', handlesDate[i])
//         console.log("document."+handlesDate[i].id+".datepicker()")
//         eval("document."+handlesDate[i].id+".datepicker()");
//         // $( "#handlesDate[i].name" ).datepicker();
//     }
//   } ;

function buttonFunction(item, shortParent, shortChild, shortItem) {
    let activeSibling = checkSiblings(item);
    selection = buildSelection(activeSibling, shortParent, shortChild, shortItem);
    sendSelectionToServer(selection);
}

function sendSelectionToServer(selection) {
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

function updateCounts(json) {
    let parent, child, item;
    console.log('BACK ONE ! : ', Object.keys(json))
    for (parent in json) {
        console.log('BACK json[parent] ! : ', parent, json[parent])
        child = '';
        for (child in json[parent]) {
            // console.log('bla ', json[parent][child])
            item = '';
            for (item in json[parent][child]) {
                // console.log('tem: ', item, json[parent][child][item]);
                newValue = json[parent][child][item];

                // searchClass = "."+parent+"."+ child+ "."+ item;
                searchClass = parent+" "+ child+ " "+ item;
                // searchClass = parent+" "+ child;
                // searchClass = parent;
                // console.log(searchClass);
                // itemHTML = eval("document.getElementsByClassName('"+searchClass+"')");
                // console.log(itemHTML[0].innerHTML);
                // console.log(itemHTML[0].innerHTML.replace(/<i>\((\d{1,})\)<\/i>/i, "HaHa"));
                itemHTML = eval("document.getElementsByClassName('"+searchClass+"')[0].innerHTML." +
                    "replace("+/<i>\((\d{1,})\)<\/i>/i+", '<i>("+newValue+")<\/i>')");
                eval("document.getElementsByClassName('"+searchClass+"')[0].innerHTML = itemHTML");
                // console.log(itemHTML.getElementsByTagName('I'));

                // console.log('Tag: ', itemHTML.getElementsByTagName("I"));
            }
        }
    }
}

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

function buildSelection(activeSibling, shortParent, shortChild, shortItem) {
    // getElementsByClassName should be faster than QuerySelectAll
    let nodeListC = eval("document.getElementsByClassName('child "+shortChild+" "+shortParent+"')");
    let nodeListP = eval("document.getElementsByClassName('parent "+shortParent+"')");
    // let nodeListC = document.querySelectorAll(".child."+shortChild+"."+shortParent);
    // let nodeListP = document.querySelectorAll(".parent."+shortParent);

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