var jsMenu = JSON.parse(jsonMenu)
var menues = Object.keys(jsMenu)
var filterMenu

menues.forEach(menuBuilder,jsMenu)

function menuBuilder(item, index) {
    if (jsMenu[item].total > 0) {  // check how many entries are in menu TODO: No Accordion when only one value
        var parentHTML ="";
        var i;
        for (i = 1; i <= jsMenu[item].total; i++) {  // build child menu
            var child = eval("jsMenu[item]."+['child'+i.toString()])
            var childHTML = childBuilder(child)
            // console.log('  *** ** *' + itemHTML)
            parentHTML = parentHTML + childHTML
        }
        filterMenu = document.getElementById("accordion").innerHTML +=
            "<h5 class='respo-hover-blue nav topmenu'>" + jsMenu[item].name + "</h5>" +
            "<div id='" + jsMenu[item].name + "'>" +
        // TODO: subaccordion works only in first menu. FIX IT!
                "<div id='subaccordion'> "+parentHTML+"" +
            "   </div>" +
            "</div>"
            // +"<div><a>HaHa!</a></div>";
        console.log('jsMenu[item].name: ', jsMenu[item].name)
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

function childBuilder(child) {
    var childHTML = "";
    var itemHTML = "";
    var dDL = 8;  // dropDownLimit

    if (child.total > 1 && child.total <= dDL && !child.hasOwnProperty("type")) {
        itemHTML = itemBuilder(child)
        childHTML =
            "<h6 class='respo-hover-blue nav childmenu'>" + child.name + "</h6>" +
            "<div id='" + child.name + "'>" +
                "<div> "+itemHTML+"" +
            "   </div>" +
            "</div>"
    }
    else if (child.total > dDL && !child.hasOwnProperty("type")){
        itemHTML = itemBuilder(child)
        inputName = "Input"+child.name
        childHTML =
            "<div class='dropdown'>" +
                "<button onclick='dDMFunction(\""+child.name+"\")' class='filter-btn-block respo-hover-blue nav'>"+child.name+"" +
                "</button>" +
                "<div id='" + child.name + "' class='dropdown-content'>" +
                    "<input type='text' placeholder='Search...' id = '"+inputName+"'" +
                        "onkeyup='dDMFilterFunction(\""+child.name+"\", \""+inputName+"\")' >" +
                    "<div> "+itemHTML+"" +
                    "</div>" +
                "</div>" +
            "</div>"
    }
    else if (child.hasOwnProperty("type")) {
        if (child.type == "slider") {
            itemHTML = sliderBuilder(child)
            childHTML=
            "<h6 class='respo-hover-blue nav'>" + child.name+ "&emsp;<i>(" + child.total + ")</i>" + "</h6>" +
            "<div id='" + child.name + "'>" +
                "<div id='sliderwildcard'> "+itemHTML+
            "   </div>" +
            "</div>"
        }
        else if (child.type == "date") {
            itemHTML = dateBuilder(child)
            childHTML = itemHTML
        }
    }
    else if (child.total == 1) {
        itemHTML = itemBuilder(child)
        // itemHTML = checkBoxBuilder(child)
        childHTML =
            "<div id='"+child.name+"'>" +
                "<b> "+child.name +": </b>"+itemHTML+
            "</div>"
    }
    return childHTML
}

function dateBuilder(child) {
    console.log('child.name: ', child.name)
    var minD = child.selectable_min.toString();
    var maxD = child.selectable_max.toString();
    var itemHTML =
        // "<p>"+child.name+"</p><input class='date' type='text' id='"+child.name+"'>"

        "<p>Date: <input type='text' id='datepicker'></p>"
    $( function() {
      $( "#datepicker" ).datepicker();
    } );

    return itemHTML;
}

function sliderBuilder(child) {
    console.log(child.name)
    var minV = child.selectable_min.toString();
    var maxV = child.selectable_max.toString();
    // onclick_slider(child.name,minV,maxV)

    // var handlesSlider = document.getElementById('slider-handles');
    // // var document.getElementById(child.name).addEventListener("click", function(){
    // // document.getElementById("demo").innerHTML = "Hello World";
    // // });
    //     console.log(handlesSlider)
    // var itemHTML =
    //     "<div class='container' data-role='rangeslider'>"+child.name+"" +
    //      // "<button onclick="+onclick_slider()+">Click me</button>"+
    //     "</div>"
    var itemHTML =
                // "<h6 class='respo-hover-blue nav'>" + child.name + "</h6>" +
            // "<button onclick='onclick_slider("+child.name+","+minV+","+maxV+")' class='filter-btn-block respo-hover-blue nav'>"+child.name+"</button>" +
        "<div class='slider' name='" + child.name + "' minV='"+minV+"' maxv='"+maxV+"'>" +
        "</div>"
    // Two Textfields for numbers:
    // var itemHTML =
    //     "<div >(min/max: "+minV+"/"+maxV+")" +
    //     "<input type='number' name='price-min' id='price-min' value='"+minV+"' min='"+minV+"' max='"+maxV+"'>" +
    //     "<input type='number' name='price-max' id='price-max' value='"+maxV+"' min='"+minV+"' max='"+maxV+"'>" +
    //     "<input type='submit' data-inline='true' value='Submit'>"+
    //     "</div>"

    return itemHTML;
}

function itemBuilder(child) {
    var i, active, itemHTML = "";
    // console.log('now me jsMenu[item].name: ', jsMenu[item].name)
    for (i = 1; i <= child.total; i++) {
        var cItem = eval("child.item" + i.toString());
        if (cItem.chosen){
            active = 'active'
        } else {
            active = ''
        }
        var listHTML =
            // "<div>" +
                // "<label class='container'>"+
                // "<input type='radio' checked='checked' name='radio'>" +
                "<a class='respo-hover-blue btn "+active+"' onclick='activateFunc(this)'>" + cItem.name + "&emsp;" +
            "       <i>(" + cItem.total + ")</i>"+
                "</a>"
            // "   </label>" +
            // "</div>";
        itemHTML = itemHTML + listHTML;
        // console.log('haha!: ', listHTML.getElementsByClassName("btn"))
    }
    return itemHTML
}

function checkBoxBuilder(child) {
    var cItem = eval("child.item");
    var listHTML =
        "<a class='respo-hover-blue'>" + cItem.name + "" +
        "</a>"
//     <label class="container">One
//   <input type="checkbox" checked="checked">
//   <span class="checkmark"></span>
// </label>;
    return itemHTML
}


function dDMFunction(dropDownName) {
    document.getElementById(dropDownName).classList.toggle("show");
}

function dDMFilterFunction(dropDownName, inputName) {
    var input, filter, ul, li, a, i;
    input = document.getElementById(inputName);
    filter = input.value.toUpperCase();
    div = document.getElementById(dropDownName);
    a = div.getElementsByTagName("a");
    for (i = 0; i < a.length; i++) {
        if (a[i].innerHTML.toUpperCase().indexOf(filter) > -1) {
            a[i].style.display = "";
        } else {
            a[i].style.display = "none";
        }
    }
}

$(document).ready(function (){
    var handlesSlider =  document.getElementsByClassName('slider');
    for (var i = 0; i < handlesSlider.length; i++){
        var maxv = parseFloat(handlesSlider[i].attributes.maxv.value);
        var minv = parseFloat(handlesSlider[i].attributes.minv.value);
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

function activateFunc(item) {
    if (item.classList.contains('active')) {
        item.classList.remove('active');
    } else {
        itemList = item.parentElement.getElementsByClassName("active")
        $(item).addClass('active').siblings().removeClass('active');
        // item.classList.add('active');
    }
}