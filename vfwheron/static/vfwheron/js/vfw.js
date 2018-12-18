//Change visibility of basiseinzugsgebiete with button
// function toggleLayer(layerName) {
//     if (layerName.getVisible() == true) {
//         layerName.setVisible(false);
//     } else {
//         layerName.setVisible(true);
//     }
// }
let draw, modify, selected_Id, selectedFeatures, vector;

function resetDraw() {
    selected_Id = [];
    selectedFeatures.clear();
    olmap.removeInteraction(draw);
    olmap.removeInteraction(modify);
    olmap.removeLayer(vector);
}

// Menu to draw polygon on map
function drawPolygon(shortParent, shortChild) {
    let div = document.getElementById('toggle_draw');
    console.log('in draw ploygon child, shortChild, shortParent: ', div, shortChild, shortParent)
    filterbox_open();
    // itemButtonFunction(item, shortParent, shortChild, shortItem)

    // olmap.removeInteraction(selectCluster);
    let collection = new ol.Collection();

    let source = new ol.source.Vector({
        wrapX: false,
        features: collection,
        useSpatialIndex: false
    });

    // create source layer
    vector = new ol.layer.Vector({
        source: source,
        style: new ol.style.Style({
            fill: new ol.style.Fill({
                color: 'rgba(255, 255, 255, 0.2)'
            }),
            stroke: new ol.style.Stroke({
                color: '#ff0040',
                width: 1
            }),
            /*  image: new ol.style.Circle({
                  radius: 5,
                  fill: new ol.style.Fill({
                      color: '#ff0040'
                  })
              })*/
        }),
        updateWhileAnimating: true, // optional, for instant visual feedback
        updateWhileInteracting: true // optional, for instant visual feedback
    });
    olmap.addLayer(vector);
    // olmap.getLayers().extend([vector]);

    let select = new ol.interaction.Select(
        /*{
        style: new ol.style.Style({
     /!*       stroke: new ol.style.Stroke({
                    color: 'green',
                    width: 2.5
                }),*!/
            fill: new ol.style.Fill({
                    color: 'rgba(255,0,0,0.1)'
                })
        }),
        }*/
    );
    olmap.addInteraction(select);

    draw = new ol.interaction.Draw({
        source: source,
        type: 'Polygon',
    });

    modify = new ol.interaction.Modify({
        // features: collection.getFeaturesCollection(),
        features: collection,
        // the SHIFT key must be pressed to delete vertices, so that new
        // vertices can be drawn at the same position of existing vertices
        deleteCondition: function (event) {
            return ol.events.condition.shiftKeyOnly(event) &&
                ol.events.condition.singleClick(event);
        }
    });

    // select interaction working on "double click"
    /*    let selectClick = new ol.interaction.Select({
            // condition: ol.events.condition.doubleClick,
            // multi: true
            // features: collection,
            layers: vector,
            style: new ol.style.Style({
                stroke: new ol.style.Stroke({
                    color: '#b9ff00',
                    width: 2
                }),
            }),
        });*/

    selectedFeatures = select.getFeatures();
    selected_Id = [];
    let sketch, listener, polygon;
    let append_str = wfsLayerName + '.';
    let features = hiddenLayer.getSource().getFeatures();

    /* Point features select/deselect as you move polygon.
        Deactivate select interaction. */
    modify.on('modifystart', function (event) {
        sketch = event.features;
        select.setActive(false);
        listener = event.features.getArray()[0].getGeometry().on('change', function (event) {
            // clear features so they deselect when polygon moves away
            selectedFeatures.clear();
            polygon = event.target;

            for (var i = 0; i < features.length; i++) {
                if (polygon.intersectsExtent(features[i].getGeometry().getExtent())) {
                    selectedFeatures.push(features[i]);
                }
            }
        });
    }, this);
    /* Reactivate select function */
    modify.on('modifyend', function (event) {
        sketch = null;
        delaySelectActivate();
        selectedFeatures.clear();
        selected_Id = [];
        polygon = event.features.getArray()[0].getGeometry();
        // let features = hiddenLayer.getSource().getFeatures();

        /* select features in polygon */
        let fLen = features.length;
        for (let i = 0; i < fLen; i++) {
            if (polygon.intersectsExtent(features[i].getGeometry().getExtent())) selectedFeatures.push(features[i]);
        }
        /* get id of selected features for menu */
        selectedFeatures.getArray().forEach(function (val) {
            selected_Id.push(parseInt(val.getId().replace(append_str, '')))
        });
        mapSelectFuntion(shortParent, shortChild, selected_Id);
    }, this);

    /* //////////// SUPPORTING FUNCTIONS */
    function delaySelectActivate() {
        setTimeout(function () {
            select.setActive(true)
        }, 300);
    }

    let drwst = document.getElementById('draw_polygon');
    drwst.addEventListener('click', function () {
        olmap.removeInteraction(modify);
        // olmap.removeInteraction(selectClick);
        olmap.addInteraction(draw);
        /* Deactivate select and delete any existing polygons.
            Only one polygon drawn at a time. */
    });
    draw.on('drawstart', function (event) {
        source.clear();
        select.setActive(false);

        sketch = event.feature;

        listener = sketch.getGeometry().on('change', function (event) {
            selectedFeatures.clear();
            polygon = event.target;
            let fLen = features.length;
            for (let i = 0; i < fLen; i++) {
                if (polygon.intersectsExtent(features[i].getGeometry().getExtent())) selectedFeatures.push(features[i]);
            }
        });
    }, this);

    draw.on('drawend', function () {
        selected_Id = [];
        // let writer = new ol.format.KML();
        // let geojsonStr = writer.writeFeatures(source.getFeatures());
        selectedFeatures.getArray().forEach(function (val) {
            selected_Id.push(parseInt(val.getId().replace(append_str, '')))
        });
        draw.finishDrawing();
        if (selected_Id.length > 0) {
            mapSelectFunction(shortParent, shortChild, selected_Id);
        }

    });


    let modst = document.getElementById('modify_polygon');
    modst.addEventListener('click', function () {
        // olmap.removeInteraction(selectCluster);
        olmap.removeInteraction(draw);
        // olmap.removeInteraction(selectClick);
        olmap.addInteraction(modify);
    });

    /*    let selst = document.getElementById('select_polygon');
        selst.addEventListener('click', function () {
            // olmap.removeInteraction(selectCluster);
            olmap.removeInteraction(draw);
            olmap.removeInteraction(modify);
            olmap.addInteraction(selectClick);
        });*/

    let delst = document.getElementById('' +
        'remove_polygon');
    delst.addEventListener('click', function () {
        // olmap.removeInteraction(selectCluster);
        // source.clear();
        source.clear();
        select.setActive(false);
        mapSelectFunction(shortParent, shortChild, []);
        resetDraw();
        /*    selectClick.getFeatures().on('add', function (feature) {
                source.removeFeature(feature.element);
                feature.target.remove(feature.element);
            });*/
    });

    let closst = document.getElementById('draw_close');
    closst.addEventListener('click', function () {
        olmap.removeInteraction(draw);
        olmap.removeInteraction(modify);
        // olmap.removeInteraction(selectClick);
        // olmap.addInteraction(selectCluster);
        filterbox_close()
    });
}

//Toggle between showing and hiding filterbox
function filterbox_open() {
    let filterbox = document.getElementById("filterbox");
    filterbox.style.display = "block";
    // document.getElementById("toggle_draw").className = 'active'
}

function filterbox_close() {
    let filterbox = document.getElementById("filterbox");
    filterbox.style.display = "none";
    // TODO: remove only if nothing selected
    // document.getElementById("toggle_draw").classList.remove('active')
}

// add toggle function for background of draw and modify button, and remove background by press on delete and close
function toggle_draw(self) {
    let siblings = document.getElementsByClassName('draw-hover');
    let s;
    let sLen = siblings.length - 1;  // avoid to toggle on the delete button
    if (self.classList.contains('activeM')) {
        self.classList.remove('activeM')
    } else {
        for (s = 0; s < sLen; s++) {
            if (siblings[s].classList.contains('activeM')) siblings[s].classList.remove('activeM')
        }
        if (self.id !== siblings[sLen].id && self.id !== 'draw_close') self.classList.add('activeM')
    }
}

//Toggle between showing and hiding select_catchment
/*function select_catchment_toggle() {
    let selcatchment = document.getElementById("select_catchment");

    if (selcatchment.style.display == "block") {
        selcatchment.style.display = "none";
    } else {
        selcatchment.style.display = "block";
    }
}*/

//Search
function search_close() {

    document.getElementById("search_box").outerHTML = "<a href='#' onclick='open_search()' id='srch_box' " +
        "class='respo-hover-white'><i class='fa fa-search fa-fw'></i>  Search</a>";
    document.getElementById("search_but").outerHTML = "<a id='srch_but' class='respo-hover-none'></a>";
    document.getElementById("search_close_but").outerHTML = "<a id='srch_close_but' class='respo-hover-none'></a>";
}

function search_open() {
    if (!document.getElementById("search_box")) {
        let searchBox = document.getElementById("srch_box");
        searchBox.outerHTML = "<a class='respo-hover-none' style='height:103px' id='search_box'><input type='search' " +
            "value='' placeholder='Search ...' style='height:26px; font-size:70%;'></a>";

        let searchBut = document.getElementById("srch_but");
        searchBut.outerHTML = "<a href='#' class='respo-hover-white' style='height:103px' id='search_but' " +
            "onclick='search_close()'><i class='fa fa-search fa-fw'></i></a>";

        let closeBut = document.getElementById("srch_close_but");
        closeBut.outerHTML = "<a href='javascript:void(0)' class='respo-hover-white' style='height:103px' " +
            "id='search_close_but' onclick='search_close()'><i class='fa fa-remove fa-fw'></i></a>";
    }
}

// TODO: check if CSRF is properly implemented! vgl. https://godjango.com/18-basic-ajax/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        let nLen = name.length;
        let cLen = cookies.length;
        for (let i = 0; i < cLen; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, nLen + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(nLen + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// TODO: not used in this file. So from where comes the used token? Which one is better?
let csrf_token = getCookie('csrftoken');

//build menu on sidebar
$(document).ready(function (menuTitle) {
    $('#accordion').accordion({
        heightStyle: "content",
        active: false,
        collapsible: true,
    });

    $("h5.respo-hover-blue.nav").click(function () {
        // var menuValue = $(this).attr("value");
// open accordion
        $('div #subaccordion').accordion({
            heightStyle: "content",
            active: false,
            collapsible: true,
        });
    });
}); // end ready

// seems to be unused / delete with next commit
// Select Data / build elements, in workspace /
// function select_data(selectedData) {
//     $.ajax({
//         url: DEMO_VAR+"/vfwheron/menu",
//         datatype: 'json',
//         data: {
//             selection: selectedData[0],
//             submenu: selectedData[1],
//             'csrfmiddlewaretoken': csrf_token,
//         }, // data sent with the post request
//         success: function (json) {
//         },
//     });
// //    document.getElementById("workspace").innerHTML += "<li class='respo-padding' id='"+selectedData+"'><span class='respo-medium'>"+selectedData+"</span><a href='javascript:void(0)' onclick=this.parentElement.remove(); class='respo-hover-white respo-right'><i class='fa fa-remove fa-fw'></i></a><br></li>";
// }

// TODO: check if CSRF is properly implemented! vgl. https://godjango.com/18-basic-ajax/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        let cLen = cookies.length;
        let nLen = name.length;
        for (let i = 0; i < cLen; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, nLen + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(nLen + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// send request to view to get info about selection; can be a single id or a list of ids
function workspace_dataset(id) {
    if (id !== 'null') {
        console.log('in workspace_dataset', id)
        $.ajax({
            url: DEMO_VAR + "/vfwheron/menu",
            datatype: 'json',
            data: {
                workspaceData: id,
                'csrfmiddlewaretoken': csrf_token,
            }, // data sent with post request
            success: function (json) {
                console.log('in ajax of workspace_dataset', id)
                if (sessionStorage.getItem("btn")) {
                    let stored = JSON.parse(sessionStorage.getItem("btn"));
                    $.each(json['workspaceData'], function (key, value) {
                        if (!stored[key]) stored[key] = value;
                    });
                    sessionStorage.setItem("btn", JSON.stringify(stored))
                } else {
                    sessionStorage.setItem("btn", JSON.stringify(json['workspaceData']));
                    console.log('workspacedata: ', JSON.stringify(json['workspaceData']))
                }
                // push sessionStorage keys to html for Workspace
                let x = [];
                $.each(JSON.parse(sessionStorage.getItem("btn")), function (key) {
                    x.push(key)
                });
                document.getElementById("workdata").value = x;

                // build buttons
                workspace_button(json);
            } // function in sidebar.js
        });
    }
}

/* Send ID to server to build preview and add preview image to html */
function show_preview(id) {
    document.getElementById("show_data_preview" + id.toString()).value = "Loading Preview";
    $.ajax({
        url: DEMO_VAR + "/vfwheron/menu",
        datatype: 'image/png;base64',
        data: {
            preview: id,
            'csrfmiddlewaretoken': csrf_token,
        }, // data sent with the post request
        success: function (json) {
            $.each(json, function (key, value) {
                // document.getElementById("preview_img").innerHTML = '<img src="data:image/svg,' + value; // Strobl svg
                document.getElementById("preview_img").innerHTML = value; // png
                document.getElementById("show_data_preview" + id.toString()).value = "Reload Preview"
            });
        }
    });
}

function popupContentvfw(ids, page) {
    // TODO: CSS style überarbeiten
    // console.log(' + + + ++  ids: ', ids)
    if (typeof (ids) === 'string' && typeof(page) === 'undefined') {
        page = JSON.parse("[" + ids + "]").slice(-1);
        ids = JSON.parse("[" + ids + "]").slice(0, -1);
    }
    if (page != 'none') document.getElementById("pagi" + page).classList.add("loadspin");
    let popupTableBeforeMeta = '<table id="popupTable"><td>';
    // let popupTextStyle = '<style>table tr:nth-child(even)  {background-color: #c8ebee;}</style>';
    let popUpText = `${popupTableBeforeMeta}<style>table tr:nth-child(even) {background-color: #c8ebee;}</style><table id="metaTable">`;

    // request info from server
    $.ajax({
        url: DEMO_VAR + "/vfwheron/menu",
        dataType: 'json',
        data: {
            show_info: JSON.stringify(ids),
            'csrfmiddlewaretoken': csrf_token,
        }, // data sent with the post request
        success: function (json) {
            document.getElementById('popup-content').innerHTML = buildPopupTextvfw(json, popUpText);
            if (page != 'none') {
                document.getElementsByClassName("active")[0].classList.remove("active");
                document.getElementsByClassName("loadspin")[0].classList.remove("loadspin");
                document.getElementById("pagi" + page).classList.add("active");
            }
            console.log('finished', json, popUpText)
        }

    });

}

function buildPopupTextvfw(json, popUpText) {
    let properties = json.get;
    let vLen;
    let buttonId = [];
    let values;
    // loop over "properties" dict with metadata, build columns
    for (let j in properties) {
        values = properties[j];
        vLen = values.length;
        popUpText = popUpText + '<tr><td><b>' + j + '</b></td>';
        // loop over dict values and build rows
        for (let k = 0; k < vLen; k++) {
            popUpText += '<td>' + values[k] + '</td>';
            if (j.toLowerCase() == 'id') buttonId.push(values[k])
        }
        popUpText += '</tr>'
    }
    popUpText += '<tr><td><b></b></td>';
    // build buttons for each dataset
    for (let k = 0; k < vLen; k++) {
        popUpText += '<td><a><b><input id="show_data_preview' + buttonId[k].toString() + '" class="respo-btn-block" type="submit" ' +
            'onclick=\"show_preview(\'' + buttonId[k] + '\')\" value="Preview" data-toggle="tooltip" ' +
            'title="Attention! Loading the preview might take a while."></b></a>' +
            '<a><b><input class="respo-btn-block respo-btn-block:hover" type="submit" ' +
            'onclick=\"workspace_dataset(\'' + buttonId[k] + '\')\" value="Pass to datastore" data-toggle="tooltip" ' +
            'title="Put dataset to session datastore"></b></a></td>';
    }
    let popupTableAfterMeta = popUpText + '</table>';
    let img_preview = '</td><td><p id = "preview_img" ></p></td></table>';
    return popupTableAfterMeta + img_preview;
}

function buildPagivfw(idDict, page) {
    console.log('----------------------------')
    console.log('idDict, page: ', idDict, page)
    console.log('JSON.parse("[" + idDict + "]"): ', JSON.parse("[" + idDict + "]"))
    if (typeof (idDict) === 'string' && typeof(page) === 'undefined') {
        page = JSON.parse("[" + idDict + "]").slice(-1);
        idDict = JSON.parse("[" + idDict + "]").slice(0, -1);
    }
    for (let i = 1; i <= page; i++) {
        if (i == 1) {
            pagi = '<li id="pagi' + i + '" class="active"><a><input type="submit" id="popBtn" class="respo-btn-simple"' +
                'onclick=\"popupContentvfw(\'' + idDict[i] + ',' + i + '\')\" value="' + i + '"></a></li>';
        } else {
            pagi = pagi + '<li id="pagi' + i + '"><a><input type="submit" class="respo-btn-simple"' +
                'onclick=\"popupContentvfw(\'' + idDict[i] + ',' + i + '\')\" value="' + i + '"></a></li>';
        }
    }
}

// // another accordion/ didn't work for me (Marcus)
// var acc = document.getElementsByClassName("new_accord");
// var i;
//
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

