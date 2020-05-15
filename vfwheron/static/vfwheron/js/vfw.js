let draw, modify, selectedFeatures, vector;
let selectedIdsMap = null;

function resetDraw() {
    selectedIdsMap = null;
    selectedFeatures.clear();
    olmap.removeInteraction(draw);
    olmap.removeInteraction(modify);
    olmap.removeLayer(vector);
}

// Menu to draw polygon on map
function drawPolygon(shortParent, shortChild) {
    filterbox_open();

    let collection = new ol.Collection();

    let source = new ol.source.Vector({
        wrapX: false,
        features: collection,
        useSpatialIndex: false,
        zindex: -100
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
        }),
        updateWhileAnimating: true, // optional, for instant visual feedback
        updateWhileInteracting: true // optional, for instant visual feedback
    });
    olmap.addLayer(vector);

    let select = new ol.interaction.Select(
    );
    olmap.addInteraction(select);

    draw = new ol.interaction.Draw({
        source: source,
        type: 'Polygon',
        stopClick: true
    });

    modify = new ol.interaction.Modify({
        features: collection,
        // the SHIFT key must be pressed to delete vertices, so that new
        // vertices can be drawn at the same position of existing vertices
        deleteCondition: function (event) {
            return ol.events.condition.shiftKeyOnly(event) &&
                ol.events.condition.singleClick(event);
        }
    });

    selectedFeatures = select.getFeatures();
    selectedIdsMap = null;
    let sketch, listener, polygon;
    let append_str = wfsLayerName + '.';
    let features = hiddenLayer.getSource().getFeatures();

    /* Point features select/deselect as you move polygon.
        Deactivate select interaction. */
    modify.on('modifystart', function (event) {
        sketch = event.features;
        // select.setActive(false);
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
        selectedIdsMap = null;
        polygon = event.features.getArray()[0].getGeometry();

        /* select features in polygon */
        let fLen = features.length;
        for (let i = 0; i < fLen; i++) {
            if (polygon.intersectsExtent(features[i].getGeometry().getExtent())) selectedFeatures.push(features[i]);
        }
        /* get id of selected features for menu */
        selectedFeatures.getArray().forEach(function (val) {
            selectedIdsMap.push(parseInt(val.getId().replace(append_str, '')))
        });
        mapSelectFuntion(shortParent, shortChild, selectedIdsMap);
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
        olmap.addInteraction(draw);
        /* Deactivate select and delete any existing polygons.
            Only one polygon drawn at a time. */
    });
    draw.on('drawstart', function (event) {
        source.clear();
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
        selectedIdsMap = [];
        selectedFeatures.getArray().forEach(function (val) {
            selectedIdsMap.push(parseInt(val.getId().replace(append_str, '')))
        });
        if (selectedIdsMap.length > 0) {
            mapSelectFunction(shortParent, shortChild, selectedIdsMap);
        }
        olmap.removeInteraction(draw);
        toggle_draw(document.getElementById("draw_polygon"))

    });


    let modst = document.getElementById('modify_polygon');
    modst.addEventListener('click', function () {
        olmap.removeInteraction(draw);
        olmap.addInteraction(modify);
    });

    let delst = document.getElementById('' +
        'remove_polygon');
    delst.addEventListener('click', function () {
        source.clear();
        select.setActive(false);
        mapSelectFunction(shortParent, shortChild, []);
        resetDraw();
    });

    let closst = document.getElementById('draw_close');
    closst.addEventListener('click', function () {
        olmap.removeInteraction(draw);
        olmap.removeInteraction(modify);
        filterbox_close()
    });
}

//Toggle between showing and hiding filterbox
function filterbox_open() {
    let filterbox = document.getElementById("filterbox");
    filterbox.style.display = "block";
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
        self.classList.remove('activeM');
        draw.finishDrawing();
    } else {
        for (s = 0; s < sLen; s++) {
            if (siblings[s].classList.contains('activeM')) siblings[s].classList.remove('activeM')
        }
        if (self.id !== siblings[sLen].id && self.id !== 'draw_close') self.classList.add('activeM')
    }
}

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

function moreInfoModal(id) {
    document.getElementById('mod_dat_inf').innerHTML = "";
    document.getElementById("mod_prev").innerHTML = "";
    document.getElementById("mod_prev").classList.add("loader");
    // TODO: If the first ajax finishes first there is an additional table id="popupTable". Check why and avoid it!
    $.ajax({
        url: DEMO_VAR + "/vfwheron/menu",
        dataType: 'json',
        data: {
            show_info: JSON.stringify([id]),
            'csrfmiddlewaretoken': csrf_token,
        }, // data sent with the post request
        success: function (properties) {
            let metaText = '<table>';
            // loop over "properties" dict with metadata, build columns
            for (let j in properties) {
                // TODO: compare with let values = eval('properties["' + j + '"]'); in buildPopupTextvfw why eval?
                metaText += '<tr><td><b>' + j + '</b></td><td>' + properties[j] + '</td></tr>';
            }
            document.getElementById('mod_dat_inf').innerHTML = metaText + '</table>';
            showDataInfo(properties);
        }
    });

    // load preview image parallel to metadata
    $.ajax({
        url: DEMO_VAR + "/vfwheron/menu",
        datatype: 'image/png;base64',
        // datatype: 'html',
        data: {
            preview: id,
            'csrfmiddlewaretoken': csrf_token,
        }, // data sent with the post request
    })
        .done(function (json) {
            document.getElementById("mod_prev").innerHTML = json.div; // add plot
            console.log('HTML: ', document.getElementById("mod_prev"))
            console.log('HTML: ', document.getElementById("mod_prev").innerHTML)
            // bokehPreviewScript is a global variable to set and remove the script of bokeh
            bokehPreviewScript = document.createElement('script');
            bokehPreviewScript.type = 'text/javascript';
            bokehPreviewScript.text = json.script;
            document.head.appendChild(bokehPreviewScript);
        })
        .fail(function (e) {
            console.log('fehler: ', e)
        })
        .always(function (json) {
            document.getElementById("mod_prev").classList.remove("loader");
        });
    let modal = document.getElementById("infoModal");
    modal.style.display = "block";
}

// send request to view to get info about selection; can be a single id or a list of ids
function workspace_dataset(id) {
    if (id !== 'null') {
        $.ajax({
            url: DEMO_VAR + "/vfwheron/menu",
            datatype: 'json',
            data: {
                workspaceData: id,
                'csrfmiddlewaretoken': csrf_token,
            }, // data sent with post request
            success: function (json) {
                if (sessionStorage.getItem("dataBtn")) {
                    console.log('json of menu: ', json)
                    let stored = JSON.parse(sessionStorage.getItem("dataBtn"));
                    $.each(json['workspaceData'], function (key, value) {
                        if (!stored[key]) stored[key] = value;
                    });
                    console.log('stored dataet: ', stored)
                    sessionStorage.setItem("dataBtn", JSON.stringify(stored))
                } else {
                    console.log('***** else: ', json['workspaceData'])
                    sessionStorage.setItem("dataBtn", JSON.stringify(json['workspaceData']));
                }
                // build buttons
                build_datastore_button(json['workspaceData']);
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
    })
        .done(function (json) {
            $.each(json, function (key, value) {
                // document.getElementById("preview_img").innerHTML = '<img src="data:image/svg,' + value; // Strobl svg
                document.getElementById("preview_img").innerHTML = value; // png
                document.getElementById("show_data_preview" + id.toString()).value = "Reload Preview"
            });
        })
        .fail(function (e) {
            console.log('fehler: ', e)
        })
}
