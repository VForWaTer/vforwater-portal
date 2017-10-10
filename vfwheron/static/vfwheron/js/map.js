//Create own base layer
function create_map() {
	mapSource = new ol.source.XYZ({url: window.location.origin + "/osm/{z}/{x}/{y}.png"})
	
	var dataExt = JSON.parse(document.getElementById('dataExt').value); // bbox of available data

// build the background map
	mapLayer = new ol.layer.Tile({
		preload: Infinity,
		source: mapSource,
	});

	// get OSM in case local map is not loading:
	mapLayer.getSource().on('tileloaderror',function(event){
		source = new ol.source.OSM();
		mapLayer.setSource(source)
    });

	mapView = new ol.View({
		center: ol.proj.fromLonLat([11.8810049, 50.0836865]),
		zoom: 6,
		maxZoom: 18,
	});


    pointSource = new ol.source.TileWMS({
		url: 'https://vforwater-gis.scc.kit.edu/geoserver/wms',
		serverType:'geoserver',
		params: {
		    LAYERS: 'CAOS:lt_location',
		    TILED: true,
		    STYLES: 'Light Blue Circle',
        }
	});
	pointMap = new ol.layer.Tile({
		source: pointSource,
	});

// Elements that make up the popup.
  var container = document.getElementById('popup');
  var content = document.getElementById('popup-content');
  var closer = document.getElementById('popup-closer');

// Create an overlay to anchor the popup to the map.
  var overlay = new ol.Overlay(/** @type {olx.OverlayOptions} */ ({
    element: container,
    autoPan: true,
    autoPanAnimation: {
      duration: 250
    }
  }));

  /** * Add a click handler to hide the popup. * @return {boolean} Don't follow the href. */
  closer.onclick = function() {
    overlay.setPosition(undefined);
    closer.blur();
    return false;
  };


	vectorSource = new ol.source.TileWMS({
		url: 'https://vforwater-gis.scc.kit.edu/geoserver/wms',
		params: {LAYERS: 'LUBW:vfwheron_basiseinzugsgebiet'}
	});

	vectorMap = new ol.layer.Tile({
		source: vectorSource,
	});

	map_tar = document.getElementById("map");
	map = new ol.Map({
		renderer: 'canvas',
		overlays: [overlay],
		target: map_tar,
		layers: [mapLayer, vectorMap, pointMap],
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
        view: mapView//dataview
	});


// get information about your data in a popup when you click on a data point in the map
  map.on('singleclick', function(evt) {
    var viewResolution = /** @type {number} */ (mapView.getResolution());
    var url = pointSource.getGetFeatureInfoUrl(
        evt.coordinate, viewResolution, 'EPSG:3857',
        {'INFO_FORMAT': 'text/html'});
    if (url) {
      document.getElementById('popup-content').innerHTML =
      '<iframe seamless src=' + url + '></iframe>';
      overlay.setPosition(evt.coordinate);
    }
  });


}
