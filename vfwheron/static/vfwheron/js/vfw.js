
// Create map layer
/*function create_map() {
		maplayer = new ol.layer.Tile({
		  source: new ol.source.OSM()
	});
	    mapview = new ol.View({
	    center: ol.proj.fromLonLat([11.8810049, 50.0836865]),
	    zoom: 6
	});
	    map_tar = document.getElementById("map");
	    map = new ol.Map({
	    renderer: 'canvas',
	    target: map_tar,
	    layers: [maplayer],
	    view: mapview
	});  
}*/

//Create own base layer
function create_map() {
		maplayer = new ol.layer.Tile({
		  source: new ol.source.OSM("Default", "/osm/${z}/${x}/${y}.png")
	});
	    mapview = new ol.View({
	    center: ol.proj.fromLonLat([11.8810049, 50.0836865]),
	    zoom: 6
	});
	    map_tar = document.getElementById("map");
	    map = new ol.Map({
	    renderer: 'canvas',
	    target: map_tar,
	    layers: [maplayer],
	    view: mapview
	});  
}

// Draw polygon
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

// Toggle between showing and hiding the sidenav, and add overlay effect
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

// Close the sidenav with the close button
function respo_close() {
	var mySidenav = document.getElementById("mySidenav");

	var overlayBg = document.getElementById("myOverlay");
	
    mySidenav.style.display = "none";
    overlayBg.style.display = "none";
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

// Search
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

// Select Data
function select_data() {
    var selectedData = document.getElementById("select_data").value;
    if (!document.getElementById(selectedData) && selectedData!=0){
    document.getElementById("workspace").innerHTML += "<li class='respo-padding' id='"+selectedData+"'><span class='respo-medium'>"+selectedData+"</span><a href='javascript:void(0)' onclick=this.parentElement.remove(); class='respo-hover-white respo-right'><i class='fa fa-remove fa-fw'></i></a><br></li>";
    }
}