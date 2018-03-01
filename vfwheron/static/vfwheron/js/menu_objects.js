var jsMenu = JSON.parse(jsonMenu)
var menues = Object.keys(jsMenu)

menues.forEach(menuBuilder,jsMenu)

function menuBuilder(item, index) {
    // console.log('jsMenu[item]: ', jsMenu[item])
    if (jsMenu[item].total > 1) {  // check how many entries are in menu
        // console.log('keys: ', Object.keys(jsMenu[item]))
        console.log('jsMenu[item].name :', jsMenu[item].name )
        var childHTML ="";
        var i;
        for (i = 1; i <= jsMenu[item].total; i++) {  // build child menu
            var child = eval("jsMenu[item]."+['child'+i.toString()])
            // console.log('childHTML1: ', childHTML)
            console.log('child.name: ', child.name)
            var itemHTML = childBuilder(child)
            childHTML = childHTML + itemHTML
            // console.log('itemHTML: ', itemHTML)
            // console.log('childHTML2: ', childHTML)
        }

        document.getElementById("accordion").innerHTML +=
            "<h5 class='respo-hover-blue nav'>" + jsMenu[item].name + "</h5>" +
            // "<div class='panel'>" +
            "<div id='" + jsMenu[item].name + "'>" +
            "<div id='subaccordion'> "+childHTML+"</div>" +
            "</div>"

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
    console.log(child.name)
    var childHTML = ""
    var itemHTML = ""
    console.log('child.name:', child.name);
    // console.log('child.total:', child.total > 0);

    if (child.total > 1 && !child.hasOwnProperty("type")) {
        // console.log('child.name: ', child.name)
        itemHTML = itemBuilder(child)
        childHTML =
            "<div class='respo-hover-blue nav'>" + child.name + "</div>" +
            "<div id='" + child.name + "'>" +
            "<div> "+itemHTML+"</div>" +
            "</div>"
            // "<div class='new_accord'>" + child.name + "</div>" +
            //         "<div id='subaccordion'>"+itemHTML+"</div>"
    }
    else if (child.total == 1 && !child.hasOwnProperty("type")){

    }
    else {
        childHTML = ''
    }
    return childHTML
}

//  TODO: HIER GEHTS WEITER
function itemBuilder(child) {
    console.log('child: ', child)
    console.log('child: ', child.total)
    var childHTML;
    var itemHTML = ""
    var i;
        for (i = 1; i <= child.total; i++) {
            if (!child.hasOwnProperty("type")) {
                var cItem = eval("child.item" + i.toString());
                // console.log('cItem works: ', cItem.name)
                var listHTML = "<div value='" + (i-1).toString() + "' class='respo-hover-blue'>" + cItem.name + "</div>";
                // console.log('itemHTML: ', itemHTML)
                itemHTML = itemHTML + listHTML;
            }
        }
    return itemHTML
}

// function buildSelectBox(child){
//     var itemHTML = "<div class='custom-select' style='width:200px;'>"+child.name+" <select class='select-box' >"
//     var i;
//         for (i = 1; i <= child.total; i++) {
//             if (!child.hasOwnProperty("type")) {
//                 var cItem = eval("child.item" + i.toString());
//                 // console.log('cItem works: ', cItem.name)
//                 var listHTML = "<option value='" + (i-1).toString() + "'>" + cItem.name + "</options>";
//                 itemHTML = itemHTML + listHTML;
//             }
//         }
//         itemHTML = itemHTML + " </select></div>"
//     return itemHTML
// }

// function buildSelectBox(child){
//     var itemHTML = "<div class='custom-select' style='width:200px;'>"+child.name+" <select class='select-box' >"
//     var i;
//         for (i = 1; i <= child.total; i++) {
//             if (!child.hasOwnProperty("type")) {
//                 var cItem = eval("child.item" + i.toString());
//                 // console.log('cItem works: ', cItem.name)
//                 var listHTML = "<option value='" + (i-1).toString() + "'>" + cItem.name + "</options>";
//                 itemHTML = itemHTML + listHTML;
//             }
//         }
//         itemHTML = itemHTML + " </select></div>"
//     return itemHTML
// }

function Menuitem(name, total_choices, type, child) {
    this.name = name;
    this.total_choices = total_choices;
    this.choices = total_choices;
    this.chosen = 0;
    // this.child = child_builder(child)

}

function Childitem(name, total_choices, type, child) {
    this.name = name
    this.type = type || 'default'
    this.total_choices = total_choices;
    this.choices = total_choices;
    this.chosen = 0;

}


// // *** accordion ***
// var acc = document.getElementsByClassName("new_accord");
// var i;
//
// for (i = 0; i < acc.length; i++) {
//   acc[i].addEventListener("click", function() {
//     this.classList.toggle("active");
//     var panel = this.nextElementSibling;
//     if (panel.style.maxHeight){
//       panel.style.maxHeight = null;
//     } else {
//       panel.style.maxHeight = panel.scrollHeight + "px";
//     }
//   });
// }


// $(document).ready(function (menuTitle) {
//     $('#accordion').accordion({
//         heightStyle: "content",
//         active: false,
//         collapsible: true,
// //  TODO - very low priority: icons don't work
//         icons: {
//             header: 'fa-plus-circle',
//             activeHeader: 'fa-minus-circle'
//         }
//     });
//
//     $("h5.respo-hover-blue.nav").click(function () { // two actions happen on click:
//
//         var menuValue = $(this).attr("value");
// // first action: open accordion
//         $('div #subaccordion').accordion({
//             heightStyle: "content",
//             active: false,
//             collapsible: true,
//             //  TODO - very low priority: icons don't work
//             icons: {
//                 header: 'fa-plus-circle',
//                 activeHeader: 'fa-minus-circle'
//             }
//         });
//     })
// });

// accordion without animation (check also css for changes!):
// for (i = 0; i < acc.length; i++) {
//     acc[i].addEventListener("click", function() {
//         /* Toggle between adding and removing the "active" class,
//         to highlight the button that controls the panel */
//         this.classList.toggle("active");
//
//         /* Toggle between hiding and showing the active panel */
//         var panel = this.nextElementSibling;
//         if (panel.style.display === "block") {
//             panel.style.display = "none";
//         } else {
//             panel.style.display = "block";
//         }
//     });
// }
