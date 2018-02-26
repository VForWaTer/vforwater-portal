//Change visibility of basiseinzugsgebiete with button
function toggleLayer(layerName) {
    if (layerName.getVisible() == true) {
        layerName.setVisible(false);
    } else {
        layerName.setVisible(true);
    }
}

//Draw polygon
function draw_polygon() {
    var collection = new ol.Collection();

    var source = new ol.source.Vector({
        wrapX: false,
        features: collection,
        useSpatialIndex: false
    });

    // Source layer
    var vector = new ol.layer.Vector({
        source: source,
        style: new ol.style.Style({
            fill: new ol.style.Fill({
                color: 'rgba(255, 255, 255, 0.2)'
            }),
            stroke: new ol.style.Stroke({
                color: '#ff0040',
                width: 2
            }),
            image: new ol.style.Circle({
                radius: 7,
                fill: new ol.style.Fill({
                    color: '#ff0040'
                })
            })
        }),
        updateWhileAnimating: true, // optional, for instant visual feedback
        updateWhileInteracting: true // optional, for instant visual feedback
    });

    map.addLayer(vector);

    var draw = new ol.interaction.Draw({
        source: source,
        type: 'Polygon',
    });

    var modify = new ol.interaction.Modify({
        features: collection,
        // the SHIFT key must be pressed to delete vertices, so
        // that new vertices can be drawn at the same position
        // of existing vertices
        deleteCondition: function (event) {
            return ol.events.condition.shiftKeyOnly(event) &&
                ol.events.condition.singleClick(event);
        }
    });

    // select interaction working on "double click"
    var selectClick = new ol.interaction.Select({
        condition: ol.events.condition.doubleClick,
        multi: true
    });

    var drwst = document.getElementById('draw_polygon');
    drwst.addEventListener('click', function () {
        map.removeInteraction(modify);
        map.removeInteraction(selectClick);
        map.addInteraction(draw);
        draw.on('drawend', function () {
            var writer = new ol.format.KML();
            var geojsonStr = writer.writeFeatures(source.getFeatures());
            document.getElementById("workspace").innerHTML += "<li class='respo-padding' id='p'><span " +
                "class='respo-medium'>" + geojsonStr + "</span><a href='javascript:void(0)' " +
                "onclick=this.parentElement.remove(); class='respo-hover-white respo-right'><i " +
                "class='fa fa-remove fa-fw'></i></a><br></li>";
        });
    });

    var modst = document.getElementById('modify_polygon');
    modst.addEventListener('click', function () {
        map.removeInteraction(draw);
        map.removeInteraction(selectClick);
        map.addInteraction(modify);
    });

    var selst = document.getElementById('select_polygon');
    selst.addEventListener('click', function () {
        map.removeInteraction(draw);
        map.removeInteraction(modify);
        map.addInteraction(selectClick);
    });

    var delst = document.getElementById('remove_polygon');
    delst.addEventListener('click', function () {
        map.removeInteraction(draw);
        map.removeInteraction(modify);
        selectClick.getFeatures().on('add', function (feature) {
            source.removeFeature(feature.element);
            feature.target.remove(feature.element);
        });
    });

    var closst = document.getElementById('draw_close');
    closst.addEventListener('click', function () {
        map.removeInteraction(draw);
        map.removeInteraction(modify);
        map.removeInteraction(selectClick);
    });
}

//Toggle between showing and hiding filterbox
function filterbox_open() {
    var filterbox = document.getElementById("filterbox");
    filterbox.style.display = "block";
}

function filterbox_close() {
    var filterbox = document.getElementById("filterbox");
    filterbox.style.display = "none";
}

//Toggle between showing and hiding select_catchment
function select_catchment_toggle() {
    var selcatchment = document.getElementById("select_catchment");

    if (selcatchment.style.display == "block") {
        selcatchment.style.display = "none";
    } else {
        selcatchment.style.display = "block";
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
        var searchBox = document.getElementById("srch_box");
        searchBox.outerHTML = "<a class='respo-hover-none' style='height:103px' id='search_box'><input type='search' " +
            "value='' placeholder='Search ...' style='height:26px; font-size:70%;'></a>";

        var searchBut = document.getElementById("srch_but");
        searchBut.outerHTML = "<a href='#' class='respo-hover-white' style='height:103px' id='search_but' " +
            "onclick='search_close()'><i class='fa fa-search fa-fw'></i></a>";

        var closeBut = document.getElementById("srch_close_but");
        closeBut.outerHTML = "<a href='javascript:void(0)' class='respo-hover-white' style='height:103px' " +
            "id='search_close_but' onclick='search_close()'><i class='fa fa-remove fa-fw'></i></a>";
    }
}

// TODO: check if CSRF is properly implemented! vgl. https://godjango.com/18-basic-ajax/
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// TODO: not used in this file. So from where comes the used token? Which one is better?
var csrf_token = getCookie('csrftoken');


//build menu on sidebar
$(document).ready(function (menuTitle) {
    $('#accordion').accordion({
        heightStyle: "content",
        active: false,
        collapsible: true,
//  TODO - very low priority: icons don't work
        icons: {
            header: 'fa-plus-circle',
            activeHeader: 'fa-minus-circle'
        }
    });

    $("h5.respo-hover-blue.nav").click(function () { // two actions happen on click:

        var menuValue = $(this).attr("value");
// first action: open accordion
        $('div #subaccordion').accordion({
            heightStyle: "content",
            active: false,
            collapsible: true,
            //  TODO - very low priority: icons don't work
            icons: {
                header: 'fa-plus-circle',
                activeHeader: 'fa-minus-circle'
            }
        });
// second action: request menu values
        $.ajax({
            url: DEMO_VAR+"/vfwheron/menu",
            datatype: 'json',
            data: {
                menu: menuValue,

                'csrfmiddlewaretoken': csrf_token,
            }, // data sent with the post request
            success: function (json) {
                $.each(json, function (key1, value1) { // loop over top level menu z.B. key1 = Geologie
                    //                    var newMenuButton = ('#'+key1)
                    var newHTML = '';
                    var newMenu = '';
                    $.each(value1, function (key2, value2) { // loop over sub menu z.B. key2 = Sandstone
                        if (key2 != 'null') {
                            var selectedData = "['" + key2 + "', '" + key1 + "']"
//                            var selectedData = "'"+ key2 +"'"
//                            console.log('value 2 ist: ', value2[1])
                            var bool = ''
                            if (value2[0]) {
                                bool = 'checked'
                            }
                            newHTML = '<input type="checkbox" class="respo-check respo-hover-blue" id="' + key2 + '" ' +
                                bool + '  onclick="select_data(' + selectedData + ')"> ' + key2 + ' <i>(' + value2[1] +
                                ')</i></input><br>';
                        } else {
                            newHTML = '<a>keine Auswahl verfügbar</a>';
                        }
                        newMenu = newMenu + newHTML;
                    });
                    $('#' + key1).html(newMenu);
                });
            },
        });
    });
}); // end ready

// Select Data / build elements, in workspace
function select_data(selectedData) {
    $.ajax({
        url: DEMO_VAR+"/vfwheron/menu",
        datatype: 'json',
        data: {
            selection: selectedData[0],
            submenu: selectedData[1],
            'csrfmiddlewaretoken': csrf_token,
        }, // data sent with the post request
        success: function (json) {
        },
    });
//    document.getElementById("workspace").innerHTML += "<li class='respo-padding' id='"+selectedData+"'><span class='respo-medium'>"+selectedData+"</span><a href='javascript:void(0)' onclick=this.parentElement.remove(); class='respo-hover-white respo-right'><i class='fa fa-remove fa-fw'></i></a><br></li>";
}

// TODO: check if CSRF is properly implemented! vgl. https://godjango.com/18-basic-ajax/
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function onclick_show_datasets_func() {
    $.ajax({
        url: DEMO_VAR+"/vfwheron/menu",
        datatype: 'json',
        data: {
            onclick_show_datasets: 'True',
            'csrfmiddlewaretoken': csrf_token,
        }, // data sent with post request
        success: function (json) {
            // console.log('onclick_show_datasets_func: ', json)
            $.each(json, function (key, value) {
                if (key == "results") {
                    /*document.getElementById("workspace").innerHTML += "<li class='respo-padding' id='" + key + "'>" +
                        "<span class='respo-medium'>You got " + value + " Datasets</span><a href='javascript:void(0)'" +
                        "onclick=this.parentElement.remove(); class='respo-hover-white respo-right'><i " +
                        "class='fa fa-remove fa-fw'></i></a><br></li>";*/
                } else if (key == "data_style") {
                    selectedIds = value
                    wfsPointLayer.changed()
                }
            })
        }
    });
}

function workspace_dataset(id) {
    $.ajax({
        url: DEMO_VAR+"/vfwheron/menu",
        datatype: 'json',
        data: {
            workspaceData: id,
            'csrfmiddlewaretoken': csrf_token,
        }, // data sent with the post request
        success: function(json) {workspace_button(json)} // function in sidebar.js
    });/*
    document.getElementById("workspace").innerHTML += "<li class='respo-padding' id='" + id + "'>" +
        "<span class='respo-medium' data-toggle=\"tooltip\" title="+metaTable+">You got Dataset #" + id + " </span><a href='javascript:void(0)'" +
        "onclick=this.parentElement.remove(); class='respo-hover-white respo-right'><i " +
        "class='fa fa-remove fa-fw'></i></a><br></li>";
*/
}

function show_preview(id) {
    document.getElementById("show_data_preview").value = "Loading Preview"
    $.ajax({
        url: DEMO_VAR+"/vfwheron/menu",
        datatype: 'image/png;base64',
        data: {
            preview: id,
            'csrfmiddlewaretoken': csrf_token,
        }, // data sent with the post request
        success: function(json) {
            // console.log('back from preview', json)
            $.each(json, function (key, value) {
                // document.getElementById("preview_img").innerHTML = '<img src="data:image/svg,' + value; // Strobl svg
                document.getElementById("preview_img").innerHTML = value; // Mälicke  png
                document.getElementById("show_data_preview").value = "Load Preview again"
            });
        }
    });
}
