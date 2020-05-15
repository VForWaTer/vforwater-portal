//Toggle between showing and hiding the sidenav, and add overlay effect
function respo_open() {
    // Get the Sidenav
    var mySidenav = document.getElementById("mySidenav");

    // Get the DIV with overlay effect
    var overlayBg = document.getElementById("myOverlay");

    if (mySidenav.style.display === "block") {
        mySidenav.style.display = "none";
        overlayBg.style.display = "none";
    } else {
        mySidenav.style.display = "block";
        overlayBg.style.display = "block";
    }
}

//Close the sidenav with the close button
function respo_close() {
    var mySidenav = document.getElementById("mySidenav");

    var overlayBg = document.getElementById("myOverlay");

    mySidenav.style.display = "none";
    overlayBg.style.display = "none";
}

//Toggle between showing and hiding the sidemenu, and add overlay effect
function Sidemenu_open() {
    // Get the Sidemenu
    var mySidemenu = document.getElementById("mySidemenu");

    // Get the DIV with overlay effect
    var overlaymenu = document.getElementById("mySidemenuOverlay");

    if (mySidemenu.style.display === "block") {
        mySidemenu.style.display = "none";
        overlaymenu.style.display = "none";
    } else {
        mySidemenu.style.display = "block";
        overlaymenu.style.display = "block";
    }
}

//Close the sidemenu with the close button
function Sidemenu_close() {
    var mySidemenu = document.getElementById("mySidemenu");

    var overlaymenu = document.getElementById("mySidemenuOverlay");

    mySidemenu.style.display = "none";
    overlaymenu.style.display = "none";
}

// Get the User Selection in Workspace
// Button information is stored in an HTML object with Id 'workdata'
// it is stored as a string, so the following function transforms this string back to a dictionary
// TODO: workdata is maybe not needed anymore? Try to store information in sessionStorage
function show_data() {
    // Initiate creation of data Button in data and result store. When called from outside of 'Home' check if data is
    // already pickled. If not pickle it. (TODO: Should be monitored if a lot of data gets pickled but never used!)
    let workspaceData = JSON.parse(sessionStorage.getItem("dataBtn"));
    if (workspaceData) {// && "value" in workspaceData) {
        build_datastore_button(workspaceData);
        let path = window.location.pathname;
        if (path.includes('wps_gui')) {
            // check if datasets are pickled and update buttons
            preload_datastore_button(workspaceData);
    }
    }
    if (document.getElementById("workspace_results")) {  // check if user is on a page with workspace to built buttons
        let resultData = JSON.parse(sessionStorage.getItem("resultBtn"));
        if (resultData) {
            let html = "";
            $.each(resultData, function (btnName, value) {
                html += build_resultstore_button(btnName, value);
            });
            document.getElementById("workspace_results").innerHTML += html;
        }
    }
}

/**
 * If there is a selection from the Filtermenu preload it and store the pickle
 * @param workspaceData
 */
function preload_datastore_button(workspaceData) {
    // USE THIS UPPER PART WHEN YOU PREFER TO LOAD EACH DATASET SEPARATELY
    for (let dataset in workspaceData) {
        let preload = {};
        if (!workspaceData[dataset]['pickle']) {
            preload[dataset] = {type: workspaceData[dataset]['type'], start: workspaceData[dataset]['start'],
            end: workspaceData[dataset]['end']};
            $.ajax({
                url: DEMO_VAR + "/wps_gui/processview",
                // dataType: 'json',
                data: {
                    dbload: JSON.stringify(preload), 'csrfmiddlewaretoken': csrf_token,
                }, // data sent with post request
                success: (wpsDBInfo) => update_datastore_button(wpsDBInfo),
                error: function (wpsDBInfo) {
                    console.error('Error in preload of data. ', wpsDBInfo)
                }
            });
        }
    }
    // USE FOLLOWING CODE INSTEAD WHEN YOU PREFER TO UPDATE ALL DATASETS IN ONE REQUEST
    // let preload = {};
    // for (let dataset in workspaceData) {
    //     if (!workspaceData[dataset]['pickle']) {
    //         preload[dataset] = {type: workspaceData[dataset]['type'], start: workspaceData[dataset]['start'],
    //         end: workspaceData[dataset]['end']};
    //     }
    // }
    // if (Object.keys(preload).length == 0){}
    // else {
    //     // send request to preload datasets
    //     // TODO: might take a while. Check how to cancel if webpage changes
    //     // TODO: discuss if "load it all at once" is the best solution. (alternatives: each dataset or in chunks)
    //     $.ajax({
    //         url: DEMO_VAR + "/wps_gui/processview",
    //         // dataType: 'json',
    //         data: {
    //             dbload: JSON.stringify(preload), 'csrfmiddlewaretoken': csrf_token,
    //         }, // data sent with post request
    //         success: function (wpsDBInfo) {
    //             update_datastore_button(wpsDBInfo, 'pickle');
    //         },
    //         error: function (wpsDBInfo) {
    //             console.log('Error in preload of data. ', wpsDBInfo)
    //         }
    //     });
    // }
}

function update_datastore_button(wpsDBInfo){
    let workspaceData = JSON.parse(sessionStorage.getItem("dataBtn"));
    $.each(wpsDBInfo, function (keyID, value) {
        if (workspaceData[keyID] && workspaceData[keyID]['wpsID']) {
            workspaceData[keyID]['pickle'] = 1;
            workspaceData[keyID]['wpsID'] = value['wps_id'];
            workspaceData[keyID]['type'] = value['datatype'];
            // workspaceData[keyID]['type'] = workspaceData[keyID]['type'] + ", "+ newClass;
            document.getElementById("id" + keyID).getElementsByClassName("data")[0].classList.add(value['datatype']);
        }
    });
    sessionStorage.setItem("dataBtn", JSON.stringify(workspaceData));
}

// build buttons in workspace and store selection in clients sessionStorage
function build_datastore_button(json) {
    let html = "";
    $.each(json, function (key, value) {
        let btnName;
        let vnLen = value['name'].length;
        if (vnLen + value['abbr'].length + value['unit'].length <= 13) {
            btnName = `${value['name']} (${value['abbr']} in ${value['unit']}) - ${key}`;
        } else if (vnLen + value['abbr'].length <= 15) {
            btnName = `${value['name']} (${value['abbr']}) - ${key}`;
        } else if (vnLen <= 17) {
            btnName = `${value['name']} - ${key}`;
        } else {
            btnName = `${value['abbr']} in ${value['unit']} - ${key}`;
        }
        let title = `${value['name']} (${value['abbr']} in ${value['unit']})`;
        // check if buttons already exist before creating a new one:
        if (document.getElementById("id" + key) === null) {
            html += '<li draggable="true" class="respo-padding task" ' +
                'data-id="' + key + '" btnName="' + btnName + '" onmouseover="" style="cursor:pointer;" id="id' + key + '">' +
                '<span class="respo-medium" title="' + title + '">' +
                '<div class="task__content">' + btnName + '</div><div class="task__actions"></div>' +
                '</span><span class="data ' + value['type'] + '"></span>' +
                '<a href="javascript:void(0)" onclick="remove_single_data(' + key + ')" ' +
                'class="respo-hover-white respo-right"><i class="fa fa-remove fa-fw"></i>' +
                '</a><br></li>';
        }
    });
    document.getElementById('workspace').innerHTML += html
    // }
}

// Remove data / elements from workspace
function remove_single_data(removeData) {
    // remove data from portal:
    document.getElementById("id" + removeData).remove();
    // remove data from session:
    let workspaceData = JSON.parse(sessionStorage.getItem("dataBtn"));
    delete workspaceData[removeData];
    sessionStorage.setItem("dataBtn", JSON.stringify(workspaceData))
}

function remove_all_datasets() {
    // remove button from portal
    $.each(JSON.parse(sessionStorage.getItem("dataBtn")), function (key, value) {
        if ("name" in value) {
            remove_single_data(parseInt(key));
        }
    });
    // remove button from session
    sessionStorage.removeItem("dataBtn");
}

// code for context menu from https://www.sitepoint.com/building-custom-right-click-context-menu-javascript/
// MIT license

// (function() {

"use strict";
//
// H E L P E R    F U N C T I O N S

/**
 * Function to check if we clicked inside an element with a particular class
 * name.
 *
 * @param {Object} e The event
 * @param {String} className The class name to check against
 * @return {Boolean}
 */
function clickInsideElement(e, className) {
    var el = e.srcElement || e.target;

    if (el.classList.contains(className)) {
        return el;
    } else {
        while (el = el.parentNode) {
            if (el.classList && el.classList.contains(className)) return el;
        }
    }

    return false;
}

/**
 * Get's exact position of event.
 *
 * @param {Object} e The event passed in
 * @return {Object} Returns the x and y position
 */
function getPosition(e) {
    var posx = 0;
    var posy = 0;

    if (!e) var e = window.event;

    if (e.pageX || e.pageY) {
        posx = e.pageX;
        posy = e.pageY;
    } else if (e.clientX || e.clientY) {
        posx = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
        posy = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
    }

    return {
        x: posx,
        y: posy
    }
}

//
// C O R E    F U N C T I O N S
//

/**
 * Variables.
 */
var contextMenuClassName = "context-menu";
var contextMenuItemClassName = "context-menu__item";
var contextMenuLinkClassName = "context-menu__link";
var contextMenuActive = "context-menu--active";
var contextResultActive = "context-result--active";

var taskItemClassName = "task";
var taskItemInContext;

var clickCoords;
var clickCoordsX;
var clickCoordsY;

var menu = document.querySelector("#context-menu");
var resultMenu = document.querySelector("#context-result");
let popup = document.querySelector("#loader-popup");
let content = document.querySelector('#pop-content-side');
let popText = document.querySelector('#popupText');
let popcloser = document.querySelector('#pop-closer');
let popActive = "mod-popup--active";
let popInActive = "mod-popup--inactive";

var menuState = 0;
var menuWidth;
var menuHeight;
var resultMenuWidth;
var resultMenuHeight;
var menuPosition;
var menuPositionX;
var menuPositionY;

var windowWidth;
var windowHeight;

/**
 * Initialise our application's code.
 */
function init() {
    contextListener();
    clickListener();
    keyupListener();
    resizeListener();
}

/**
 * Listens for contextmenu events.
 */
function contextListener() {
    document.addEventListener("contextmenu", function (e) {
        taskItemInContext = clickInsideElement(e, taskItemClassName);
        let chooseContext;
        if (taskItemInContext) {
            if (taskItemInContext.classList.contains('is-result')) chooseContext = 'is-result';
            e.preventDefault();
            toggleMenuOn(chooseContext);
            positionMenu(e);
        } else {
            taskItemInContext = null;
            toggleMenuOff();
        }
    });
}

/**
 * Listens for click events.
 */
function clickListener() {
    document.addEventListener("click", function (e) {
        let clickeElIsLink = clickInsideElement(e, contextMenuLinkClassName);
        if (clickeElIsLink) {
            e.preventDefault();
            menuItemListener(clickeElIsLink);
        } else {
            let button = e.which || e.button;
            if (button === 1) toggleMenuOff();
        }
    });
}

/**
 * Listens for keyup events.
 */
function keyupListener() {
    window.onkeyup = function (e) {
        if (e.keyCode === 27) toggleMenuOff();
    }
}

/**
 * Window resize event listener
 */
function resizeListener() {
    window.onresize = function (e) {
        toggleMenuOff();
    };
}

/**
 * Turns the custom context menu on.
 */
function toggleMenuOn(chooseContext) {
    toggleMenuOff(chooseContext);
    if (menuState !== 1) {
        menuState = 1;
        if (chooseContext == "is-result") {
            resultMenu.classList.add(contextResultActive);
        } else {
            menu.classList.add(contextMenuActive);
        }
    }
}

/**
 * Turns the custom context menu off.
 */
function toggleMenuOff(chooseContext) {
    if (menuState !== 0) {
        menuState = 0;
        if (resultMenu) resultMenu.classList.remove(contextResultActive);
        menu.classList.remove(contextMenuActive);
    }
}

/**
 * Positions the menu properly.
 *
 * @param {Object} e The event
 */
function positionMenu(e) {
    clickCoords = getPosition(e);
    clickCoordsX = clickCoords.x;
    clickCoordsY = clickCoords.y;

    menuWidth = menu.offsetWidth + 4;
    menuHeight = menu.offsetHeight + 4;

    windowWidth = window.innerWidth;
    windowHeight = window.innerHeight;

    menu.style.left = ((windowWidth - clickCoordsX) < menuWidth) ? `${windowWidth - menuWidth}px` : `${clickCoordsX}px`;
    menu.style.top = ((windowHeight - clickCoordsY) < menuHeight) ? `${windowHeight - menuHeight}px` : `${clickCoordsY}px`;

    if (resultMenu) {
    resultMenuWidth = resultMenu.offsetWidth + 4;
    resultMenuHeight = resultMenu.offsetHeight + 4;

    resultMenu.style.left = ((windowWidth - clickCoordsX) < resultMenuWidth) ? `${windowWidth - resultMenuWidth}px` : `${clickCoordsX}px`;
    resultMenu.style.top = ((windowHeight - clickCoordsY) < resultMenuHeight) ? `${windowHeight - resultMenuHeight}px` : `${clickCoordsY}px`;
    }
}

/**
 * Positions the popup properly.
 *
 * @param {Object} e The event
 */
// TODO: Why is the position only sometimes correctly updated?
function positionPopup(window) {
    let popupWidth = window.offsetWidth + 4;
    let popupHeight = window.offsetHeight + 4;
    window.style.left = ((windowWidth - clickCoordsX) < popupWidth) ? `${windowWidth - popupWidth}px` : `${clickCoordsX}px`;
    window.style.top = ((windowHeight - clickCoordsY) < popupHeight) ? `${windowHeight - popupHeight}px` : `${clickCoordsY}px`;
}

/**
 * Dummy action function that logs an action when a menu item link is clicked
 *
 * @param {???} properties
 */
function showDataInfo(properties) {
    let popUpText = '<thead><tr><th>&nbsp;</th></tr></thead>';
    // loop over "properties" dict with metadata, build columns
    for (let j in properties) {
        // TODO: compare with let values = eval('properties["' + j + '"]'); in buildPopupTextvfw why eval?
        popUpText += '<tr><td><b>' + j + '</b></td><td>' + properties[j] + '</td></tr>';
    }
    content.innerHTML = '<div class="mod-header"><table><td><style>table tr:nth-child(even) ' +
        '{background-color: #c8ebee;}</style><table>' + popUpText + '</table></div>';
    popcloser.classList.remove('respo-hide');
    positionPopup(popup);
}

// TODO: Fill Tool with previous values
function setModalValues(btnName, btnValues) {
    let inModal = document.getElementById('mod_in');
    let radioInputs = inModal.getElementsByTagName('input');
    let dropDInputs = inModal.getElementsByTagName('select');
    /** first loop over each dropdown in input, then over values in dropdown **/
    // for (let i = 0; i < dropDInputs.length; i++) {
    //
    //         // dDInput = dropDInputs[i].selectedOptions;
    //     //     console.log('dDInput: ', dDInput)
    //     //     if (dDInput.length > 1) {
    //     //         for (let j = 0; j < dDInput.length; j++) {
    //     //             valueList.push(dDInput[j].value)
    //     //         }
    //     //         inValue.push(valueList);
    //     //         inKey.push(dropDInputs[i].name);
    //     //     } else {
    //     //         inKey.push(dropDInputs[i].name);
    //     //         inValue.push(dDInput[0].value);
    //     // }
    // }

}

/**
 * Provide actions for the right click menues for data and result buttons, and load the respective data from the server.
 *
 * @param (html) link HTML Code of the clicked link
 */
function menuItemListener(link) {
    console.log('link: ', link)
    let wpsToOpen = "";
    let service = {};
    let id = taskItemInContext.getAttribute("data-id");
    let btnName = taskItemInContext.getAttribute('btnname');

    console.log('id: ', id)
    let result = JSON.parse(sessionStorage.getItem('resultBtn'));
    content.innerHTML = '<div id="loader" class="loader"></div>';
    popup.classList.add(popActive);
    popText.classList.remove(popInActive);
    positionPopup(popup);

    switch (link.getAttribute("data-action")) {

        case "View":
            $.ajax({
                url: DEMO_VAR + "/vfwheron/menu",
                dataType: 'json',
                data: {
                    show_info: JSON.stringify([id]),
                    'csrfmiddlewaretoken': csrf_token,
                }, // data sent with the post request
                success: function (properties) {
                    showDataInfo(properties);

                }
            });
            break;
        case "Downloadcsv":
            $.ajax({
                url: DEMO_VAR + "/vfwheron/datasetdownload",
                datatype: 'json',
                data: {
                    csv: id,
                }, // data sent with post request
                success: function (json) {
                    let blob = new Blob([json], {type: "text/csv;charset=utf-8"});
                    saveAs(blob, taskItemInContext.getAttribute("btnName") + ".csv");
                },
                complete: function () {
                    popup.classList.remove(popActive);
                }
            });
            break;
        case "Downloadshp":
            $.ajax({
                url: DEMO_VAR + "/vfwheron/datasetdownload",
                datatype: 'json',
                method: 'GET',
                xhrFields: {
                    responseType: 'blob'
                },
                data: {
                    shp: id,
                }, // data sent with post request
                success: function (data) {
                    let blob = new File([data], {type: "application/octet-stream"});
                    saveAs(blob, String(taskItemInContext.getAttribute("btnName")) + ".zip");
                },
                complete: function () {
                    popup.classList.remove(popActive);
                }
            });
            break;
        case "Downloadxml":
            $.ajax({
                url: DEMO_VAR + "/vfwheron/datasetdownload",
                datatype: 'json',
                data: {
                    xml: id,
                }, // data sent with post request
                success: function (json) {
                    let blob = new Blob([json], {type: "text/csv;charset=utf-8"});
                    saveAs(blob, taskItemInContext.getAttribute("btnName"));
                },
                complete: function () {
                    popup.classList.remove(popActive);
                }
            });
            break;
        case "OpenTool":
            /** Re-open the tool */
            wpsToOpen = result[btnName].wps;
            service = document.getElementById(wpsToOpen).getAttribute("data-service");
            wpsprocess(service, wpsToOpen)
            /** Fill the tool with selection made to receive this result button */
            setModalValues(btnName, JSON.parse(sessionStorage['resultBtn'])[btnName])
            popup.classList.remove(popActive);
            break;
        case "DownloadDMD":
            console.error('Not implemented yet')
            break;
        case "Remove":
            remove_single_data(id);
            popup.classList.remove(popActive);
            break;
        case "ViewResult":
            let popUpText = '<thead><tr><th>&nbsp;</th></tr></thead>';
            console.log('+ result: ', result)
            console.log('+ id: ', id)
            for (let j in result) {
                if (result[j]) {
                if (!(result[j] instanceof Object)) {
                    popUpText += '<tr><td><b>' + j + '</b></td><td>' + result[j] + '</td></tr>';
                    } else {
                        let len_k = result[j].length;
                        for (let k in result[j]) {
                            let name_j = len_k > 1 ? j + ' ' + k + 1 : j;
                            popUpText += '<tr><td><b>' + name_j + '</b></td><td>' + result[j][k] + '</td></tr>';
                        }
                    }
                }
            }
            content.innerHTML = '<div class="mod-header"><table><td><style>table tr:nth-child(even) ' +
                '{background-color: #c8ebee;}</style><table>' + popUpText + '</table></div>';
            popcloser.classList.remove('respo-hide');
            positionPopup(popup);
            break;
        case "Plot":
            $.ajax({
                url: DEMO_VAR + "/vfwheron/menu",
                datatype: 'json',
                data: {
                    preview: id,
                    'csrfmiddlewaretoken': csrf_token,
                }, // data sent with post
                success: function (requestResult) {
                    console.log('got a result: ', requestResult)
                    if ('html' in requestResult) {
                        document.getElementById("mod_result").innerHTML = requestResult.html; // add plot
                    } else {  // plot from bokeh
                        document.getElementById("mod_result").innerHTML = requestResult.div; // add plot
                        bokehResultScript = document.createElement('script');
                        bokehResultScript.type = 'text/javascript';
                        bokehResultScript.text = requestResult.script;
                        document.head.appendChild(bokehResultScript);
                    }
                    let rModal = document.getElementById("resultModal");
                    rModal.style.display = "block";
                },
                complete: function () {
                    popup.classList.remove(popActive);
                }
            });
            break;
        case "DownloadR":
            let blob = new Blob([sessionStorage.getItem(id)], {type: "text/csv;charset=utf-8"});
            saveAs(blob, taskItemInContext.getAttribute("btnName") + ".csv");
            popup.classList.remove(popActive);
            break;
        case "RemoveR":
            remove_single_result(id);
            popup.classList.remove(popActive);
            break;
        default:
            console.error('Error! There is no function defined for "' + link.getAttribute("data-action") + '".')

    }
    popText.classList.add(popInActive);
    toggleMenuOff();
}

/** * Add a click handler to hide the popup. * @return {boolean} Don't follow the href. */
popcloser.onclick = function () {
    // metaData_Overlay.setPosition(undefined);
    // popcloser.blur();
    popup.classList.remove(popActive);
    return false;
};

/** make the popup dragable: */
$(function () {
    $(popup).draggable({
        handle: ".mod-header"
    });
    // $('#loader-popup').resizable();

});

// TODO: remove popup when clicking outside of popup
/*
window.onclick = function(event) {
    console.log(' - + click + - : ', event)
    console.log(' - + click + - target: ', event.target)
    console.log(' - + click + - parentNode: ', event.parentNode)
    if (event.target == popup) {
        console.log('click inside')
        // popup.style.display = "none";
        popup.classList.remove(popActive);
    }
};
*/

/**
 * Run the app.
 */
init();
// })();
