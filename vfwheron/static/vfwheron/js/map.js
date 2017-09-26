//Create own base layer
function create_map() {
	mapsource = new ol.source.XYZ({url: window.location.origin + "/osm/{z}/{x}/{y}.png"})
	
	var dataExt = JSON.parse(document.getElementById('dataExt').value); // bbox of available data


// build the background map
	maplayer = new ol.layer.Tile({
		preload: Infinity,
		source: mapsource,
	});
	
	// get OSM in case local map is not loading:
	maplayer.getSource().on('tileloaderror',function(event){
		source = new ol.source.OSM();
		maplayer.setSource(source) 
    });
	
	mapview = new ol.View({
		center: ol.proj.fromLonLat([11.8810049, 50.0836865]),
		zoom: 6,
		maxZoom: 20,
	});


    pointsource = new ol.source.TileWMS({
		url: 'https://vforwater-gis.scc.kit.edu/geoserver/wms',
		params: {LAYERS: 'CAOS:lt_location'}
	});
	pointmap = new ol.layer.Tile({
		source: pointsource,
	});

	vectorSource = new ol.source.TileWMS({
		url: 'https://vforwater-gis.scc.kit.edu/geoserver/wms',
		params: {LAYERS: 'LUBW:vfwheron_basiseinzugsgebiet'}
	});
	vectormap = new ol.layer.Tile({
		source: vectorSource,
	});


	map_tar = document.getElementById("map");
	map = new ol.Map({
		renderer: 'canvas',
		target: map_tar,
		layers: [maplayer, vectormap, pointmap],
		controls: [
			new ol.control.Zoom(),
			new ol.control.Attribution(),
			new ol.control.ZoomSlider(),
			new ol.control.MousePosition({
				projection: 'EPSG:4326',
				coordinateFormat: function(coord) {
					return ol.coordinate.format(coord, ' {y}°N, {x}°E ', 4);}
			}),
			new ol.control.ScaleLine(),
			new ol.control.ZoomToExtent({ // zoom button
				label: 'Z',
				tipLabel: 'Zoom to your Data',
				extent: dataExt

			}),
			],
			view: mapview//dataview
	});
}
