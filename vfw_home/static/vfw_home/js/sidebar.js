/*
 * Project Name: V-FOR-WaTer
 * Author: Marcus Strobl
 * Contributors:
 * License: MIT License
 */

/** Toggle between showing and hiding the sidenav, and add overlay effect **/
vfw.sidebar.w3_Open = function () {
    // Get the Sidenav
    let mySidenav = document.getElementById("mySidenav");
    // Get the DIV with overlay effect
    let overlayBg = document.getElementById("myOverlay");

    if (mySidenav.style.display === "block") {
        mySidenav.style.display = "none";
        overlayBg.style.display = "none";
    } else {
        mySidenav.style.display = "block";
        overlayBg.style.display = "block";
    }
}

/** Close the sidenav with the close button **/
vfw.sidebar.w3_Close = function () {
    let mySidenav = document.getElementById("mySidenav");
    let overlayBg = document.getElementById("myOverlay");

    mySidenav.style.display = "none";
    overlayBg.style.display = "none";
}

/** Toggle between showing and hiding the sidemenu, and add overlay effect **/
vfw.sidebar.sidemenuOpen = function () {
    // Get the Sidemenu
    let mySidemenu = document.getElementById("mySidemenu");
    // Get the DIV with overlay effect
    let overlaymenu = document.getElementById("mySidemenuOverlay");

    if (mySidemenu.style.display === "block") {
        mySidemenu.style.display = "none";
        overlaymenu.style.display = "none";
    } else {
        mySidemenu.style.display = "block";
        overlaymenu.style.display = "block";
    }
}

/** Close the sidemenu with the close button **/
vfw.sidebar.sidemenuClose = function () {
    let mySidemenu = document.getElementById("mySidemenu");
    let overlaymenu = document.getElementById("mySidemenuOverlay");

    mySidemenu.style.display = "none";
    overlaymenu.style.display = "none";
}

/**
 * Get the User Selection in Workspace
 * Button information is stored in an HTML object with Id 'workdata'
 * it is stored as a string, so the following function transforms this string back to a dictionary
 */
// TODO: workdata is maybe not needed anymore? Try to store information in sessionStorage
vfw.sidebar.showData = function () {
    /** Initiate creation of data Button in data and result store.  **/
    const dataStoreData = JSON.parse(sessionStorage.getItem("dataBtn"));
    if (dataStoreData) {  // && "value" in workspaceData) {
        $.each(dataStoreData, function (k) {
            if (!(dataStoreData[k].hasOwnProperty('type') && dataStoreData[k]['type'] === 'geometry')) {
                vfw.datasets.dataObjects[k] = new vfw.datasets.DataObj(dataStoreData[k], false);
            } else {
                vfw.datasets.selectObjects[k] = new vfw.datasets.selectObj(dataStoreData[k], false);
            }
        });
    }

    /** build result objects only on /workspace/ */
    let resultStoreData;
    if (window.location.pathname === '/workspace/') {
        resultStoreData = JSON.parse(sessionStorage.getItem("resultBtn"));
    } else {
        resultStoreData = null;
    }
    /** collect  results data from session storage, create objects from it and check status if not finished or error */
    if (resultStoreData) {  // && "value" in workspaceData) {
        $.each(resultStoreData, function (k) {
            vfw.datasets.resultObjects[k] = new vfw.datasets.resultObj(resultStoreData[k]);
            if (vfw.datasets.resultObjects[k]['status'] === "ACCEPTED"
                || vfw.datasets.resultObjects[k]['status'] === "CREATED")
                vfw.datasets.resultObjects[k].refresh()
        });
    }
    // (TODO: Old version. Maybe reuse later to group data
    // if (document.getElementById("workspace_results")) {  // check if user is on a page with workspace to built buttons
    //     const resultData = JSON.parse(sessionStorage.getItem("resultBtn"));
    //     let groups = {};
    //     if (resultData) {
    //         let html = "";
    //         let ghtml = "";
    //         let mhtml = "";
    //         $.each(resultData, function (btnName, value) {
    //             if (!value.group) {
    //                 html += vfw.workspace.buildResultStoreButton(btnName, value);
    //             } else {
    //                 if (!(value.group in groups)) {
    //                     groups[value.group] = [];
    //                 }
    //                 groups[value.group].push([btnName, value])
    //             }
    //         });
    //         $.each(groups, function (groupname, members) {
    //             mhtml = "";
    //             ghtml = "";
    //             members.forEach(function (singlemember) {
    //                 return mhtml += vfw.workspace.buildResultStoreButton(singlemember[0], singlemember[1]);
    //             })
    //             html += vfw.workspace.buildResultGroupButton(groupname, members)
    //             // ghtml += '<div class="grouppanel">' + mhtml + '</div>'
    //             // html += ghtml
    //         })
    //         // ghtml += build_resultgroup_button(value.group)
    //         document.getElementById("workspace_results").innerHTML += html;
    //
    //         vfw.sidebar.addGroupaccordionToggle()
    //     }
    // }
}

/**
 * add accordion function to group button
 */
vfw.sidebar.addGroupaccordionToggle = function () {
    const acc = document.getElementsByClassName("groupaccordion");
    let panel;
    for (let i of acc) {
        i.addEventListener("click", function () {
            this.classList.toggle("active");
            panel = this.nextElementSibling;
            panel.style.display = (panel.style.display === "block") ? "none" : "block";
        });
    }
}

/**
 * Adds a data store button to the sidebar. Used when user uploads a dataset or presses save button in draw menu.
 * @param {object} file - In case of an uploaded geometry one can pass the whole object. Yet used is only file.name
 */
vfw.sidebar.addSelectStoreButton = function (file={}, source="userUpload") {
    /** Data needed to create a Button in the datastore */
    const objData = {
        "name": "Select Area", "type": "geometry", "geom": vfw.filter.coords, "isGroupMember": false,
        "orgID": "selectArea" + Math.floor(Math.random() * 1000000).toString()
    }
    objData['name'] = 'name' in file ? file.name : "user upload";
    objData['source'] = source;
    console.log('objData: ', objData)

    /** Use the latest upload for filtering, If ID exists already loop sessionStore and change ID until we found a
     * new ID */ // TODO: We don't update, we store all => new ID (in case the random generator gave two time the same number)
    if (vfw.datasets.selectObjects.hasOwnProperty(objData['orgID'])) {
        let newID = objData['orgID'];
        let i = 0;
        while (vfw.datasets.selectObjects.hasOwnProperty(newID)) {
            newID = `${objData['orgID']}_${i++}`;
        }
        objData.orgID = newID;
        objData.name = `${objData.name} (${i})`;
    }
    vfw.datasets.selectObjects[objData['orgID']] = new vfw.datasets.selectObj(objData);
}


/** Remove data / elements from workspace **/
// vfw.session.removeSingleData = function (removeData) {
//     console.log('removeData: ', removeData)
//     console.log('document.getElementById("sidebtn' + removeData + '"): ', document.getElementById("sidebtn" + removeData))
//     /** remove data from portal: **/
//     document.getElementById("sidebtn" + removeData).remove();
//     // removeData.remove();  // could be used when the element where send directly
//
//     /** remove data from session: **/
//     let workspaceData = JSON.parse(sessionStorage.getItem("dataBtn"));
//
//     delete workspaceData[removeData];
//     sessionStorage.setItem("dataBtn", JSON.stringify(workspaceData))
//     sessionStorageData = workspaceData  // is this already in use somewhere? Then add it also in Result Buttons
// }

vfw.session.removeGroupData = function (removeData) {
    /** remove button from portal **/
    const storedData = JSON.parse(sessionStorage.getItem("dataBtn"))
    $.each(storedData, function (i) {
        if (storedData[i].group === removeData) {
            // vfw.session.removeSingleData(i);
            vfw.datasets.dataObjects[i].removeData(i)
            // document.getElementById("id" + key).remove()
        }
    });
    document.getElementById(removeData).remove();
}

vfw.session.removeAllDatasets = function () {
    /** remove button from portal **/
    const storedData = JSON.parse(sessionStorage.getItem("dataBtn"))
    $.each(storedData, function (key, value) {
        if (vfw.datasets.dataObjects[key]) vfw.datasets.dataObjects[key].removeData(key)
        else if (vfw.datasets.selectObjects[key]) vfw.datasets.selectObjects[key].removeData(key)
    });
}

// code for context menu from https://www.sitepoint.com/building-custom-right-click-context-menu-javascript/
// MIT license

// (function() {

"use strict";
//
// H E L P E R    F U N C T I O N S

/**
 * Function to check if we clicked inside an element with a particular class name.
 *
 * @param {Object} e The event
 * @param {String} className The class name to check against
 * @return {Boolean}
 */
vfw.sidebar.clickInsideElement = function (e, className) {
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
// TODO: THIS!!!!
vfw.util.getEventPosition = function (e) {
    var posx = 0;
    var posy = 0;

    if (!e) var e = window["event"];

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
 * Global Variables for popup.
 */
// var contextMenuClassName = "context-menu";
// var contextMenuItemClassName = "context-menu__item";
// var contextMenuLinkClassName = "context-menu__link";
var contextMenuActive = "context-menu--active";
var contextResultActive = "context-result--active";
document.querySelector
var taskItemClassName = "task";
// var taskItemInContext;
vfw.var.taskItemInContext = null;

vfw.html.contextMenu = document.querySelector("#context-menu");  // get element with id context-menu
// var vfw.html.contextMenu = document.querySelector("#context-menu");
var resultMenu = document.querySelector("#context-result");
vfw.html.popup = document.querySelector("#loader-popup");  // needed in sidebar "Plot data"
vfw.html.popup_content = document.querySelector('#pop-content-side');
let popText = document.querySelector('#popupText');
let popClose = document.querySelector('#pop-closer');
let popActive = "mod-popup--active";
let popInActive = "mod-popup--inactive";

var menuState = 0;
var menuWidth;
var menuHeight;
var resultMenuWidth;
var resultMenuHeight;

var windowWidth;
var windowHeight;

/**
 * Initialise our application's code.
 */
vfw.init = function() {
    vfw.init.contextListener();
    vfw.init.clickListener();
    vfw.init.keyupListener();
    vfw.init.resizeListener();
}

/**
 * Listens for contextmenu events.
 */
vfw.init.contextListener = function () {
    document.addEventListener("contextmenu", function (e) {
        vfw.var.taskItemInContext = vfw.sidebar.clickInsideElement(e, taskItemClassName);
        // console.log('vfw.var.taskItemInContext.dataset.sessionstore: ', vfw.var.taskItemInContext.dataset.sessionstore)

        let chooseContext;
        let btndata;
        if (vfw.var.taskItemInContext && !vfw.var.taskItemInContext.classList.contains("groupaccordion")) {
            if (vfw.var.taskItemInContext.classList.contains('is-result')) {
                chooseContext = 'is-result';
                btndata = JSON.parse(sessionStorage.getItem("resultBtn"))[vfw.var.taskItemInContext.dataset.btnname]
            } else {
                btndata = JSON.parse(sessionStorage.getItem("dataBtn"))[vfw.var.taskItemInContext.dataset.orgid]
            }
            e.preventDefault();
            vfw.html.toggleMenuOn(chooseContext, vfw.var.taskItemInContext.dataset, btndata);
            vfw.sidebar.positionMenu(e);
        } else {
            vfw.var.taskItemInContext = null;
            toggleMenuOff();
        }
    });
}

/**
 * Listens for click events.
 */
vfw.init.clickListener = function () {
    document.addEventListener("click", function (e) {
        const clickeElIsLink = vfw.sidebar.clickInsideElement(e, "context-menu__link");
        if (clickeElIsLink) {
            e.preventDefault();
            menuItemListener(clickeElIsLink);
        } else {
            let button = e.which || e.button;
            if (button === 1) toggleMenuOff();  // 1 == left button; 3 == right button
        }
    });
}

/**
 * Listens for keyup events.
 */
vfw.init.keyupListener = function () {
    window.onkeyup = function (e) {
        if (e.keyCode === 27) {
            // close everything when ESC was pressed
            toggleMenuOff()
            try {
                vfw.html.infoModal.close()
            } catch {}
            try {
                vfw.map.closeMapModal()
            } catch {}
            try {
                vfw.html.resultModal.close()
            } catch {}
        }
    }
}

/**
 * Window resize event listener
 */
vfw.init.resizeListener = function () {
    window.onresize = function (e) {
        toggleMenuOff();
    };
}

/**
 * Toggle in the contextmenu the option to show a plot.
 *
 * @param {Element} menunode
 * @param {Element} btndata
 */
function togglePlotContext(menunode, btndata) {
    let plotables = ["figure", "timeseries"]

    if (plotables.includes(btndata.type)) {
        menunode.querySelector(".context-menu-plot").parentNode.style.display = "block";
    } else {
        menunode.querySelector(".context-menu-plot").parentNode.style.display = "none";
    }
}

/**
 * Turns the custom context menu on.
 */
vfw.html.toggleMenuOn = function (chooseContext, data, btndata) {
    toggleMenuOff(chooseContext);
    if (menuState !== 1) {
        menuState = 1;
        if (chooseContext == "is-result") {
            resultMenu.classList.add(contextResultActive);
            togglePlotContext(resultMenu, btndata)
        } else {
            vfw.html.contextMenu.classList.add(contextMenuActive);
            togglePlotContext(vfw.html.contextMenu, btndata)
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
        vfw.html.contextMenu.classList.remove(contextMenuActive);
    }
}

/**
 * Positions the right click (context) menu properly.
 *
 * @param {Object} e The event
 */
vfw.sidebar.positionMenu = function (e) {
    console.log('e: ', e)
    vfw.html.mouse.clickCoords = vfw.util.getEventPosition(e);

    menuWidth = vfw.html.contextMenu.offsetWidth + 4;
    menuHeight = vfw.html.contextMenu.offsetHeight + 4;

    windowWidth = window.innerWidth;
    windowHeight = window.innerHeight;

    vfw.html.contextMenu.style.left = ((windowWidth - vfw.html.mouse.clickCoords.x) < menuWidth) ? `${windowWidth - menuWidth}px` : `${vfw.html.mouse.clickCoords.x}px`;
    vfw.html.contextMenu.style.top = ((windowHeight - vfw.html.mouse.clickCoords.y) < menuHeight) ? `${windowHeight - menuHeight}px` : `${vfw.html.mouse.clickCoords.y}px`;

    if (resultMenu) {
        resultMenuWidth = resultMenu.offsetWidth + 4;
        resultMenuHeight = resultMenu.offsetHeight + 4;

        resultMenu.style.left = ((windowWidth - vfw.html.mouse.clickCoords.x) < resultMenuWidth) ? `${windowWidth - resultMenuWidth}px` : `${vfw.html.mouse.clickCoords.x}px`;
        resultMenu.style.top = ((windowHeight - vfw.html.mouse.clickCoords.y) < resultMenuHeight) ? `${windowHeight - resultMenuHeight}px` : `${vfw.html.mouse.clickCoords.y}px`;
    }
}

/**
 * Dummy action function that logs an action when a menu item link is clicked
 *
 * @param {dict} properties
 */
vfw.workspace.modal.showDataInfo = function (properties) {
    // TODO: This function changes the style of the table used instead of the map. (To the Style I is supposed to be.
    //  Why only after this function and not without. What is this function doing?)
    let popUpText = '<thead><tr><th>&nbsp;</th></tr></thead>';
    // loop over "properties" dict with metadata, build columns
    for (let j in properties) {
        // TODO: compare with let values = eval('properties["' + j + '"]'); in buildPopupTextvfw why eval?
        popUpText += '<tr><td><b>' + j + '</b></td><td>' + properties[j] + '</td></tr>';
    }
    vfw.workspace.modal.openResultModal(popUpText);
    // document.getElementById("mod_result").innerHTML = '<div class="mod-header"><table><td><style>table tr:nth-child(even) ' +
    //     '{background-color: #c8ebee;}</style><table>' + popUpText + '</table></div>';; // add table
    // vfw.html.resultModal.style.display = "block";
}


/**
 * Add innerHTML to the result modal and open it. As standard the html code is part of a table.
 * As an alternative one can also add just the html without table for is_simple = true.
 *
 * @param {string} html
 * @param {boolean} js_simple
 */
vfw.workspace.modal.openResultModal = function (html, is_simple=false) {
    if (is_simple) {
        document.getElementById("mod_result").innerHTML = html;
    } else {
        document.getElementById("mod_result").innerHTML = '<div class="mod-header"><table><td><style>table tr:nth-child(even) ' +
        '{background-color: #c8ebee;}</style><table>' + html + '</table></div>'; // add table
    }
    vfw.html.resultModal.style.display = "block";
}


vfw.workspace.modal.setInPortValue = function (btnKey, btnValues) {
    let entry_value = [btnKey, btnValues]


    let btnName = vfw.var.taskItemInContext.getAttribute('btnname');
    let store = vfw.var.taskItemInContext.getAttribute('data-sessionstore');
    let item = JSON.parse(sessionStorage.getItem(store))[btnName];
    if (!item) {
        btnName = vfw.var.taskItemInContext.getAttribute('data-orgid');
        item = JSON.parse(sessionStorage.getItem(store))[btnName];
    }

    let resultData = JSON.parse(sessionStorage.getItem("resultBtn"));
    let workflowData = JSON.parse(sessionStorage.getItem("workflow"));
    let sessionStoreData = JSON.parse(sessionStorage.getItem("dataBtn"));
    let htmlelement = vfw.html.createInputElement(btnValues, resultData, sessionStoreData)
}


/**
 * Fill a process modal with values from a result.
 *
 * @param {list} btnKeys names of input fields
 * @param {list} btnValues values for the input fields
 */
vfw.workspace.modal.setProcessValues = function (btnKeys, btnValues) {  // TODO: Need source data or result
    // for (let i = 0; i < btnName.length; i++) {  // use this loop for older browsers
    //     document.getElementById(btnName[i].identifier).value = btnValues[btnName[i].identifier]
    // }
    let htmlElement = {};
    let workmodal = document.getElementById('workModal');
    let datastore = JSON.parse(sessionStorage['dataBtn']);
    let resultstore = JSON.parse(sessionStorage['resultBtn']);

    // loop values of result to insert them in the respective field
    let loopLength = 0;
    if (btnValues) {
        loopLength = btnValues.length
    }
    for (let i = 0; i < loopLength; i++) {

        htmlElement = document.getElementById('mod_in_el_' + btnKeys[i]);
        if (htmlElement.type == "checkbox") {
            htmlElement.checked = btnValues[i];
        } else if (htmlElement.type == "select-one") {
            let resultstore_selection;
            // name/id stored in result is not given in modal, so loop datastore for the right name/id
            for (let j in datastore) {
                if ((resultstore[j].source + resultstore[j].dbID) == btnValues[i]) {
                    resultstore_selection = j;
                    break;
                }
            }
            // if right name(id is found loop html element to find this element to pre-select it
            for (const [key, value] of Object.entries(htmlElement.options)) {
                if (htmlElement.options[key].value == resultstore_selection) {
                    htmlElement.options[key].selected = 'true';
                    break;
                }
            }
        } else {
            htmlElement.value = btnValues[i];
        }
    }

    /** first loop over each dropdown in input, then over values in dropdown **/
    // for (let i = 0; i < dropDInputs.length; i++) {
    //
    //         // dDInput = dropDInputs[i].selectedOptions;
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
 * Provide actions for the right click menus for data and result buttons, and load the respective data from the server.
 * Gets accessed on click in right click menu
 *
 * @param {html} link - HTML Element of the clicked link
 */
function menuItemListener(link) {
    if (!vfw.var.taskItemInContext) return;

    let wpsToOpen = "";
    let service = {};
    let id = vfw.var.taskItemInContext.getAttribute("data-id");
    let btnName = vfw.var.taskItemInContext.getAttribute('btnname');
    let store = vfw.var.taskItemInContext.getAttribute('data-sessionstore');
    console.log('**** store: ****: ', store)
    let item = JSON.parse(sessionStorage.getItem(store))[btnName];
    if (!item) {
        btnName = vfw.var.taskItemInContext.getAttribute('data-orgid');
        item = JSON.parse(sessionStorage.getItem(store))[btnName];
    }
    let result = JSON.parse(sessionStorage.getItem('resultBtn'));
    vfw.html.loaderOverlayOn();

    switch (link.getAttribute("data-action")) {

        case "View":
            $.ajax({
                url: vfw.var.DEMO_VAR + "/home/show_info",
                dataType: 'json',
                data: {
                    show_info: id,
                    'csrfmiddlewaretoken': vfw.var.csrf_token,
                }, // data sent with the post request
            })
                .done(function (properties) {
                    vfw.workspace.modal.showDataInfo(properties['table']);
                    if (properties['warning'] !== '') {
                        console.warn(properties['warning']);
                    }
                })
                .fail(function (failed) {
                    console.error('Failed to load any metadata for dataset ', id)
                })
                .always(function () {
                    vfw.html.loaderOverlayOff();
                })
            break;
        case "Downloadcsv":
            $.ajax({
                url: vfw.var.DEMO_VAR + "/home/datasetdownload",
                datatype: 'json',
                data: {
                    csv: id,
                }, // data sent with post request
            })
                .done(function (json) {
                    let blob = new Blob([json], {type: "text/csv;charset=utf-8"});
                    saveAs(blob, vfw.var.taskItemInContext.getAttribute("btnName") + ".csv");
                })
                .always(function () {
                    // vfw.html.popup.classList.remove(popActive);
                    vfw.html.loaderOverlayOff();
                });
            break;
        case "Downloadshp":
            $.ajax({
                url: vfw.var.DEMO_VAR + "/home/datasetdownload",
                datatype: 'json',
                method: 'GET',
                xhrFields: {
                    responseType: 'blob'
                },
                data: {
                    shp: id,
                }, // data sent with post request
            })
                .done(function (data) {
                    let blob = new File([data], {type: "application/octet-stream"});
                    // let blob = new Blob([data], {type: "application/octet-binary"});
                    saveAs(blob, String(vfw.var.taskItemInContext.getAttribute("btnName")) + ".zip");
                })
                .always(function () {
                    // vfw.html.popup.classList.remove(popActive);
                    vfw.html.loaderOverlayOff();
                });
            break;
        case "Downloadxml":
            $.ajax({
                url: vfw.var.DEMO_VAR + "/home/datasetdownload",
                datatype: 'json',
                data: {
                    xml: id,
                }, // data sent with post request
            })
                .done(function (json) {
                    // let blob = new Blob([json], {type: "text/csv;charset=utf-8"});
                    // saveAs(blob, vfw.var.taskItemInContext.getAttribute("btnName"));
                    // let blob = new Blob([json], {type: "text/csv;charset=utf-8"});
                    // console.log('blob: ', blob)
                    vfw.workspace.modal.openResultModal(json)
                    // saveAs(blob, vfw.var.taskItemInContext.getAttribute("btnName"));
                })
                .fail(function (failed) {
                    console.error('Failed to load metadata: ', failed)
                })
                .always(function () {
                    // vfw.html.popup.classList.remove(popActive);
                    vfw.html.loaderOverlayOff();
                });
            break;
        case "OpenTool":
            // TODO: Store different tools when input changes!
            /** Re-open the tool */
            wpsToOpen = result[btnName].wps;
            service = document.getElementById(wpsToOpen).getAttribute("data-service");
            vfw.workspace.modal.open_wpsprocess(service, wpsToOpen, [item.input_keys, item.input_values]);
            /** Fill the tool with selection made to receive this result button */
            /*vfw.workspace.modal.setProcessValues(
                JSON.parse(sessionStorage['tools'])[service][wpsToOpen]['dataInputs'],
                // JSON.parse(sessionStorage['resultBtn'])[btnName]['inputs']
                item.input_keys, item.input_values
            )*/
            // vfw.html.popup.classList.remove(popActive);
            vfw.html.loaderOverlayOff();
            break;
        case "DownloadDMD":
            console.error('Not implemented yet')
            break;
        case "Remove":
            // vfw.session.removeSingleData(id);
            if (id in vfw.datasets.dataObjects) vfw.datasets.dataObjects[id].removeData(id);
            else console.warn('Remove is not correctly implemented.')
            // vfw.html.popup.classList.remove(popActive);
            vfw.html.loaderOverlayOff();
            break;
        case "ViewHTML":
            console.log('item: ', item)
            vfw.workspace.modal.openResultModal(item.report_html)
            vfw.html.loaderOverlayOff();
            break;
        case "ViewResult":
            let popUpText = '<thead><tr><th>&nbsp;</th></tr></thead>';
            if (!(result[btnName] instanceof Object)) {
                popUpText += '<tr><td><b>${btnName}</b></td><td>${result[btnName]}</td></tr>';
            } else {
                popUpText += '<tr><td><b>' + 'result name' + '</b></td><td>' + result[btnName]['name'] + '</td></tr>';
                for (let j in result[btnName]['input_values']) {
                    popUpText += '<tr><td><b>' + 'input' + '</b></td><td>' + result[btnName]['input_values'][j] + '</td></tr>';
                }
                popUpText += '<tr><td><b>' + 'output' + '</b></td><td>' + result[btnName]['outputs'] + '</td></tr>';
                popUpText += '<tr><td><b>' + 'output type' + '</b></td><td>' + result[btnName]['type'] + '</td></tr>';
                // let len_k = result[btnName].length;
                // for (let k in result[btnName]) {
                //     console.log('k: ', k)
                //     let name_j = len_k > 1 ? btnName + ' ' + k + 1 : btnName;
                //     popUpText += '<tr><td><b>' + name_j + '</b></td><td>' + result[btnName][k] + '</td></tr>';
                // }
            }
            // use the following for grouped buttons (maybe?)
            // for (let j in result) {
            //     console.log('j: ', j)
            //     if (result[j]) {
            //         console.log('result[j]: ', result[j])
            //         if (!(result[j] instanceof Object)) {
            //             popUpText += '<tr><td><b>' + j + '</b></td><td>' + result[j] + '</td></tr>';
            //         } else {
            //             let len_k = result[j].length;
            //             for (let k in result[j]) {
            //                 let name_j = len_k > 1 ? j + ' ' + k + 1 : j;
            //                 popUpText += '<tr><td><b>' + name_j + '</b></td><td>' + result[j][k] + '</td></tr>';
            //             }
            //         }
            //     }
            // }
            // vfw.html.popup_content.innerHTML = '<div class="mod-header"><table><td><style>table tr:nth-child(even) ' +
            //     '{background-color: #c8ebee;}</style><table>' + popUpText + '</table></div>';
            // popClose.classList.remove('w3-hide');
            vfw.workspace.modal.openResultModal(popUpText)
            // document.getElementById("mod_result").innerHTML = '<div class="mod-header"><table><td><style>table tr:nth-child(even) ' +
            //     '{background-color: #c8ebee;}</style><table>' + popUpText + '</table></div>';
            // vfw.html.resultModal.style.display = "block";
            vfw.html.loaderOverlayOff();
            break;
        case "Plot":
            console.log('item: ', item)
            console.log('id: ', id)
            let urlParams = new URLSearchParams(window.location.search);
            let startdate, enddate;
            let date = urlParams.getAll('date');

            if ($.isEmptyObject(date)) {
                startdate = 'None'
                enddate = 'None'
            } else {
                startdate = date[0].toString();
                enddate = date[1].toString();
            }
            if (item.type == 'figure') {
                // document.getElementById("pop-content-side").innerHTML = item.outputs; // add plot
                vfw.workspace.modal.openResultModal(item.outputs, true)
                // document.getElementById("mod_result").innerHTML = item.outputs; // add plot
                // vfw.html.resultModal.style.display = "block";
                // vfw.html.popup.classList.remove(popActive);
                vfw.html.loaderOverlayOff();
                modalToggleSize.style.display = "none";
                // modalToggleSize.hidden = true;
            }
                // TODO: Add Names on lines in Plot needs modification in wps or another database entry
                // let allBtns = JSON.parse(sessionStorage['resultBtn'])
                // let inputs = allBtns[btnName].inputs
                // let btnNames = []
                // $.each(inputs, function (key, value) {
                //     if (typeof value === "object"){
                //         for (let singleValue of value){
                //             $.each(allBtns, function(key, value) {
                //                 if (String(value.wpsID) == singleValue.substr(5)) {
                //                     btnNames.push(key)
                //                 }
                //             })
                //         }
                //     }
            // })

            else {
                // get bokeh plot from django
                $.ajax({
                    url: vfw.var.DEMO_VAR + "/home/previewplot",
                    datatype: 'json',
                    data: {
                        preview: id,
                        'csrfmiddlewaretoken': vfw.var.csrf_token,
                        startdate: startdate,
                        enddate: enddate,
                    }, // data sent with post
                })
                    .done(function (requestResult) {
                        // content.innerHTML = '<div class="mod-header">' + 'result' + '</div>';
                        // content.innerHTML = result.div;
                        console.log('make a previewplot')
                        if ('html' in requestResult) {
                            document.getElementById("mod_result").innerHTML = requestResult.html; // add plot
                        } else {  // plot from bokeh
                            // sessionStorage['Bokeh'] = 'true';
                            vfw.var.obj.bokehImage = requestResult;
                            vfw.html.place_html_with_js("mod_result", requestResult)
                        }
                        // popClose.classList.remove('w3-hide');
                        vfw.html.resultModal.style.display = "block";
                    })
                    .fail(function (e) {
                        console.error('Fehler: ', e)
                    })
                    .always(function () {
                        // vfw.html.popup.classList.remove(popActive);
                        vfw.html.loaderOverlayOff();
                    })
            }
            break;
        case "DownloadR":
            let blob = new Blob([sessionStorage.getItem(id)], {type: "text/csv;charset=utf-8"});
            saveAs(blob, vfw.var.taskItemInContext.getAttribute("btnName") + ".csv");
            // vfw.html.popup.classList.remove(popActive);
            vfw.html.loaderOverlayOff();
            break;
        case "RemoveR":
            vfw.session.removeSingleResult(id);
            // vfw.html.popup.classList.remove(popActive);
            vfw.html.loaderOverlayOff();
            break;
        default:
            console.error('Error! There is no function defined for "' + link.getAttribute("data-action") + '".')
            vfw.html.loaderOverlayOff();

    }
    // popText.classList.add(popInActive);
    toggleMenuOff();
}

// /** * Add a click handler to hide the popup. * @return {boolean} Don't follow the href. */
// popClose.onclick = function () {
//     // metaData_Overlay.setPosition(undefined);
//     // popClose.blur();
//     vfw.html.popup.classList.remove(popActive);
//     return false;
// };

/** make the popup dragable: */
$(function () {
    $(vfw.html.popup).draggable({
        handle: ".mod-header"
    });
    // $('#loader-popup').resizable();

});

// TODO: remove popup when clicking outside of popup
/*
window.onclick = function(event) {
    if (event.target == popup) {
        // popup.style.display = "none";
        popup.classList.remove(popActive);
    }
};
*/

/**
 * Run the app.
 */
vfw.init();
// })();
