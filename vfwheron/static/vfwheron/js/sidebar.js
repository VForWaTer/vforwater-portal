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
    let workspaceData = JSON.parse(sessionStorage.getItem("dataBtn"));
    if (workspaceData) {// && "value" in workspaceData) {
        build_datastore_button(workspaceData);
    }
    if (document.getElementById("workspace_results")) {
        let resultData = JSON.parse(sessionStorage.getItem("resultBtnList"));
        if (resultData) {
            var html = "";
            resultData.forEach(function (btnName) {
                html += build_resultstore_button(btnName, sessionStorage.getItem(btnName));
            });
            document.getElementById("workspace_results").innerHTML += html;
        }
    }
}

// build buttons in workspace and store selection in clients sessionStorage
function build_datastore_button(json) {
    // if (json['workspaceData'] !== undefined) {
    //     $.each(json['workspaceData'], function (key, value) {
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
                '</span><span class="data '+value['type']+'"></span>' +
                '<a href="javascript:void(0)" onclick="remove_single_data(' + key + ')" ' +
                'class="respo-hover-white respo-right"><i class="fa fa-remove fa-fw"></i>' +
                '</a><br></li>';
            /*
            document.getElementById("workspace").innerHTML += '<li draggable="true" class="respo-padding" ' +
                'onmouseover="" style="cursor: pointer;"rese id="' + key + '" onclick="store_menu(' + key + ')" >' +
                '<span class="respo-medium" title="'+title+'">' + btnName + '</span><a href="javascript:void(0)"' +
                'onclick="remove_single_data('+key+')"; class="respo-hover-white respo-right">' +
                '<i class="fa fa-remove fa-fw"></i></a><br></li>' +
                '<div id="w3popup" class="w3popup"><span class="popuptext" id="pop' + key + '"></span></div>' +
        '<li class="task" data-id="1"><div class="task__content">Build An App</div><div class="task__actions">' +
        '</div></li>';*/
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
            // document.getElementById("id" + key).remove()
        }
    });
    // remove button from session
    sessionStorage.removeItem("dataBtn");
}

function remove_single_result(removeData) {
    // remove data from portal:
    document.getElementById(removeData).remove();
    sessionStorage.removeItem(removeData);
    // remove data from session:
    let workspaceData = JSON.parse(sessionStorage.getItem("resultBtnList"));
    let resultBtnListLen = workspaceData.length;
    if (resultBtnListLen <= 1) {
        remove_all_results()
    } else {
        for (let i = 0; i < resultBtnListLen; i++) {
            if (workspaceData[i] === removeData) {
                workspaceData.splice(i, 1);
                i--;
            }
        }
    }
    // TODO: only the name is deleted from the list. Also delete the respective content!
    // delete workspaceData[removeData];
    sessionStorage.setItem("resultBtnList", JSON.stringify(workspaceData))
}

function remove_all_results() {
    let workspaceData = JSON.parse(sessionStorage.getItem("resultBtnList"));
    for (let i in workspaceData) {
        sessionStorage.removeItem('"' + workspaceData[i] + '"');
        document.getElementById(workspaceData[i]).remove();
    }
    sessionStorage.removeItem("resultBtnList");
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
 * @param {HTMLElement} link The link that was clicked
 */

function show_data_info(properties) {
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


function menuItemListener(link) {
    let id = taskItemInContext.getAttribute("data-id");
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
                    show_data_info(properties);

                }
            });
            break;
        case "Plot":
            $.ajax({
                url: DEMO_VAR + "/vfwheron/menu",
                datatype: 'image/png;base64',
                data: {
                    preview: id,
                    'csrfmiddlewaretoken': csrf_token,
                }, // data sent with post
                success: function (result) {
                    content.innerHTML = '<div class="mod-header">' + result['get'] + '</div>';
                    popcloser.classList.remove('respo-hide');
                    positionPopup(popup);
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
                    // let blob = new Blob([data], {type: "application/octet-binary"});
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
                    // let blob = new Blob([json], {type: "text/csv;charset=utf-8"});
                    // saveAs(blob, taskItemInContext.getAttribute("btnName"));
                    let blob = new Blob([json], {type: "text/csv;charset=utf-8"});
                    saveAs(blob, taskItemInContext.getAttribute("btnName"));
                },
                complete: function () {
                    popup.classList.remove(popActive);
                }
            });
            break;
        case "DownloadDMD":
            break;
        case "Remove":
            remove_single_data(id);
            popup.classList.remove(popActive);
            break;
        case "ViewR":
            let result = JSON.parse(sessionStorage.getItem(id));
            let popUpText = '<thead><tr><th>&nbsp;</th></tr></thead>';
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
