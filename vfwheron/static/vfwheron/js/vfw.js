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
		deleteCondition: function(event) {
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
	drwst.addEventListener('click', function(){ 
		map.removeInteraction(modify);
		map.removeInteraction(selectClick);
		map.addInteraction(draw);
		draw.on('drawend', function (){
			var writer = new ol.format.KML();
			var geojsonStr = writer.writeFeatures(source.getFeatures());
			document.getElementById("workspace").innerHTML += "<li class='respo-padding' id='p'><span class='respo-medium'>"+geojsonStr+"</span><a href='javascript:void(0)' onclick=this.parentElement.remove(); class='respo-hover-white respo-right'><i class='fa fa-remove fa-fw'></i></a><br></li>";
		});
	});

	var modst = document.getElementById('modify_polygon');
	modst.addEventListener('click', function(){ 
		map.removeInteraction(draw);
		map.removeInteraction(selectClick);
		map.addInteraction(modify);
	});

	var selst = document.getElementById('select_polygon');
	selst.addEventListener('click', function(){ 
		map.removeInteraction(draw);
		map.removeInteraction(modify);
		map.addInteraction(selectClick);
	});

	var delst = document.getElementById('remove_polygon');
	delst.addEventListener('click', function(){  
		map.removeInteraction(draw);
		map.removeInteraction(modify);
		selectClick.getFeatures().on('add', function(feature){
			source.removeFeature(feature.element);
			feature.target.remove(feature.element);
		});
	});

	var closst = document.getElementById('draw_close');
	closst.addEventListener('click', function(){ 
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
function search_close(){

	document.getElementById("search_box").outerHTML = "<a href='#' onclick='open_search()' id='srch_box' class='respo-hover-white'><i class='fa fa-search fa-fw'></i>  Search</a>";
	document.getElementById("search_but").outerHTML = "<a id='srch_but' class='respo-hover-none'></a>";
	document.getElementById("search_close_but").outerHTML = "<a id='srch_close_but' class='respo-hover-none'></a>";
}

function search_open(){
	if (!document.getElementById("search_box")){
		var searchBox = document.getElementById("srch_box");
		searchBox.outerHTML = "<a class='respo-hover-none' style='height:103px' id='search_box'><input type='search' value='' placeholder='Search ...' style='height:26px; font-size:70%;'></a>";

		var searchBut = document.getElementById("srch_but");
		searchBut.outerHTML = "<a href='#' class='respo-hover-white' style='height:103px' id='search_but' onclick='search_close()'><i class='fa fa-search fa-fw'></i></a>";

		var closeBut = document.getElementById("srch_close_but");
		closeBut.outerHTML = "<a href='javascript:void(0)' class='respo-hover-white' style='height:103px' id='search_close_but' onclick='search_close()'><i class='fa fa-remove fa-fw'></i></a>";
	}
}

//Select Data
function select_data() {
	var selectedData = document.getElementById("select_data").value;
	if (!document.getElementById(selectedData) && selectedData!=0){
		document.getElementById("workspace").innerHTML += "<li class='respo-padding' id='"+selectedData+"'><span class='respo-medium'>"+selectedData+"</span><a href='javascript:void(0)' onclick=this.parentElement.remove(); class='respo-hover-white respo-right'><i class='fa fa-remove fa-fw'></i></a><br></li>";
	}
}

function get_submenu() {
    var selectedMenu = document.getElementById("menu").value;
	if (!document.getElementById(selectedMenu) && selectedMenu!=0){
		document.getElementById("select_menu").innerHTML += "<li class='respo-padding' id='"+selectedMenu+"'><span class='respo-medium'>"+selectedMenu+"</span><a href='javascript:void(0)' onclick=this.parentElement.remove(); class='respo-hover-white respo-right'><i class='fa fa-remove fa-fw'></i></a><br></li>";
	}
}

function firstfilter() {
    location.href = "http://www.cnn.com";
}

//function dropdown(menuTitle) {
//    var actionVariable =  '"vfwheron:home"';
////    var menuID = document.getElementById(menuTitle);
////    document.getElementById(menuTitle).addEventListener("click", function () {
////  menuID.submit();
////});
//    var ajaxMenu = "\"#"+menuTitle+"\"";
//    $(ajaxMenu).bind('click', function(){
////    alert(ajaxMenu);
////    $("#Besitzer").click(function(){
////    alert(menuTitle);
//////        console.log( $(this).val() );
////        return false;
////    });
//
//    document.getElementById(menuTitle).classList.toggle("show");
//    });
//}

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
var csrftoken = getCookie('csrftoken');


$(document).ready(function(menuTitle) {
  $('#accordion').accordion({
    active: false,
    collapsible: true,
    icons: {
        header: 'fa-plus-circle',
        activeHeader: 'fa-minus-circle'
    }
  });
    $("h5.respo-hover-blue.nav").click(function () {
    var menuValue = $(this).attr("value");
//    $('.filter_submenu').html('').load(
//    url_home+"?menu=" + menuValue,)
////    "{% url url_home %}?menu=" + menuValue,)
        $.ajax({
            url: url_home,
            datatype: 'json',
    //        type : "POST",
            data: {
                    menu: menuValue ,
                    'csrfmiddlewaretoken': csrf_token,
            }, // data sent with the post request
            success : function(json) {
    //            alert(JSON.stringify(json));
    //            alert({json});
                console.log(json); // log the returned json to the console
                console.log("success"); // another sanity check
    //            $("h6").html( '{% for value4 in key2 %} <h8 id="{{ value3 }}" >json</h8>')
    //            $.each(json, function(i, val) {
    //                $(id="value").empty().append(
    //                    $('<a>').addClass('respo-hover-aqua ').text(i),
    //                    $('<a>').addClass('respo-hover-amber').text(val)
//                    )
    //            });
    },
    });
    });
 //   url:
//    $.post({
//    });
//    $.ajax('vfwheron:home', href, subMenu);
//    };
}); // end ready
//TODO: Aufruf dieser Funktion fehlt beim click
function update_menu(menu_values){
alert('bin da')
    console.log(menu_values)
    $('.vfwheron/filter_submenu.html').html('').load(
    "{% url 'vfwheron:update_menu' %}?menu="+menu_values
    )
}
//function subMenu(data){
//    newHTML = <p>New Value + data</p>;
//    $('menu').html(newHTML)
//}

/*
$('#post-form').on('submit', function(dropdown){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    create_post();
});
*/


// Close dropdown if the user clicks outside of it
//window.onclick = function(event) {
//  if (!event.target.matches('.respo-dropdown-click')) {
//
//    var dropdowns = document.getElementsByClassName("dropdown-content");
//    var i;
//    for (i = 0; i < dropdowns.length; i++) {
//      var openDropdown = dropdowns[i];
//      if (openDropdown.classList.contains('show')) {
//        openDropdown.classList.remove('show');
//      }
//    }
//  }
//}