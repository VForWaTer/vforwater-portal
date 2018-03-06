var jsMenu = JSON.parse(jsonMenu)
var menues = Object.keys(jsMenu)
var filterMenu

menues.forEach(menuBuilder,jsMenu)

function menuBuilder(item, index) {
    if (jsMenu[item].total > 1) {  // check how many entries are in menu
        var parentHTML ="";
        var i;
        for (i = 1; i <= jsMenu[item].total; i++) {  // build child menu
            var child = eval("jsMenu[item]."+['child'+i.toString()])
            var childHTML = childBuilder(child)
            // console.log('  *** ** *' + itemHTML)
            parentHTML = parentHTML + childHTML
        }
        filterMenu = document.getElementById("accordion").innerHTML +=
            "<h5 class='respo-hover-blue nav'>" + jsMenu[item].name + "</h5>" +
            "<div id='" + jsMenu[item].name + "'>" +
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
            "<h6 class='respo-hover-blue nav'>" + child.name + "</h6>" +
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
            itemHTML = sliderDiv(child)
            childHTML=
            "<a >"+child.name+"</a>" +
                "<a> "+itemHTML +"</a>"
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
            "<div>" +
                "<b> "+child.name +": </b>"+itemHTML+"" +
            "</div>"
    }
    return childHTML
}

function dateBuilder(child) {
    console.log(child.name)
    var minD = child.selectable_min.toString();
    var maxD = child.selectable_max.toString();
    var itemHTML =
        // "<div class='slidecontainer'>" +
        // "<input type='range' min="+child.selectable_min+" max="+child.selectable_max+" min_value="+child.selectable_min+" class='slider' id='myRange'>" +
        // "</div>"
        "<p>Date: <input type='text' id='datepicker'></p>"

  $( function() {
    $( "#datepicker" ).datepicker();
  } );

    return itemHTML;
}

function sliderDiv(child) {
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
    // Append the option elements
    // var select = document.getElementById('input-select');
    // for ( var i = minV; i <= maxV; i++ ){
    //     var option = document.createElement("option");
    //     option.text = i;
		// option.value = i;
    //     select.appendChild(option);
    // };
    // // Initializing the slider
    // var html5Slider = document.getElementById('html5');
    // noUiSlider.create(html5Slider, {
    //     start: [ minV, maxV ],
    //     connect: true,
    //     range: {
    //         'min': minV,
    //         'max': maxV
    //     }
    // });

    // // Updating the <select> and <input>
    // var inputNumber = document.getElementById('input-number');
    // html5Slider.noUiSlider.on('update', function( values, handle ) {
    //     var value = values[handle];
    //     if ( handle ) {
    //         inputNumber.value = value;
    //     } else {
    //         select.value = Math.round(value);
    //     }
    // });
    // select.addEventListener('change', function(){
    //     html5Slider.noUiSlider.set([this.value, null]);
    // });
    // inputNumber.addEventListener('change', function(){
    //     html5Slider.noUiSlider.set([null, this.value]);
    // });


    // Two Textfields for numbers:
    // var itemHTML =
    //     "<div >(min/max: "+minV+"/"+maxV+")" +
    //     "<input type='number' name='price-min' id='price-min' value='"+minV+"' min='"+minV+"' max='"+maxV+"'>" +
    //     "<input type='number' name='price-max' id='price-max' value='"+maxV+"' min='"+minV+"' max='"+maxV+"'>" +
    //     "<input type='submit' data-inline='true' value='Submit'>"+
    //     "</div>"

    // TODO: find a working from-to slider
    // This builds only two separate sliders
    // var itemHTML =
    //     "<div class='container' data-role='rangeslider'>"+child.name+"" +
    //     "<div data-role='rangeslider'>" +
    //     "<label for='price-min'>Price:</label>" +
    //     "<input type='range' name='price-min' id='price-min' value='200' min='"+minV+"' max='"+maxV+"'>" +
    //     "<input type='range' name='price-max' id='price-max' value='800' min='"+minV+"' max='"+maxV+"'>" +
    //     "</div>" +
    //     "<input type='submit' data-inline='true' value='Submit'>"+
    //     "</div>"

    return itemHTML;
}

function itemBuilder(child) {
    var i, itemHTML = "";
    for (i = 1; i <= child.total; i++) {
        var cItem = eval("child.item" + i.toString());
        var listHTML =
            "<div>" +
                "<a value='" + child.item1 + "' class='respo-hover-blue'>" + cItem.name + "" +
                "</a>" +
            "</div>";
        itemHTML = itemHTML + listHTML;
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


$(document).ready(sliderBuilder);

function sliderBuilder(){
    var handlesSlider =  document.getElementsByClassName('slider');
    for (var i = 0; i < handlesSlider.length; i++){
        var maxv = parseInt(handlesSlider[i].attributes.maxv.value);
        var minv = parseInt(handlesSlider[i].attributes.minv.value);
        noUiSlider.create(handlesSlider[i], {
            start: [minv, maxv],
            tooltips:  true ,
            // behaviour: 'tap-drag',
            // connect: true,
            range: {
                'min': [ minv ],
                'max': [ maxv ]
            },
            pips: { // Show a scale with the slider
		mode: 'steps',
		stepped: true,
		density: 4
	}
        });

    }
}