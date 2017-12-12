//Create own base layer
function create_map() {
	var mapSource = new ol.source.XYZ({url: window.location.origin + "/osm/{z}/{x}/{y}.png"})
	
	var dataExt = JSON.parse(document.getElementById('dataExt').value); // bbox of available data
	var data_style = JSON.parse(document.getElementById('data_style').value);
    data_style = data_style['data_style']
// build the background map
	var mapLayer = new ol.layer.Tile({
		preload: Infinity,
		source: mapSource,
	});

	// get OSM in case local map is not loading:
	mapLayer.getSource().on('tileloaderror',function(event){
		source = new ol.source.OSM();
		mapLayer.setSource(source)
    });

	var mapView = new ol.View({
		center: ol.proj.fromLonLat([11.8810049, 50.0836865]),
		zoom: 6,
		maxZoom: 18,
        minZoom: 2
	});

    var wmsPointSource = new ol.source.TileWMS({
		url: 'https://vforwater-gis.scc.kit.edu/geoserver/wms',
		serverType:'geoserver',
		params: {
		    // LAYERS: 'CAOS:get_pointinfo',
		    LAYERS: 'CAOS:ID_as_identifier',
		    // LAYERS: 'CAOS:pointdata',
		    TILED: true,
		    //STYLES: 'CAOS:new_point',
           // STYLES: 'Light Blue Circle',
		    STYLES: data_style,
        },
        name: 'wmsPointSource'
	});
	var wmsPointLayer = new ol.layer.Tile({
		source: wmsPointSource,
	});

    var wfsPointSource = new ol.source.Vector({
      format: new ol.format.GeoJSON(),
      loader: function(extent, resolution, projection) {
         var proj = projection.getCode();
         var url = 'https://vforwater-gis.scc.kit.edu/geoserver/CAOS/wfs?service=WFS&version=2.0.0&' +
             'request=GetFeature&typename=CAOS:ID_as_identifier&outputFormat=application/json&srsname=EPSG:3857' +
             '&bbox=' + extent.join(',') + ',EPSG:3857';
         var xhr = new XMLHttpRequest();
         xhr.open('GET', url);
         var onError = function() {
           vectorSource.removeLoadedExtent(extent);
         }
         xhr.onerror = onError;
         xhr.onload = function() {
           if (xhr.status == 200) {
             vectorSource.addFeatures(
                 vectorSource.getFormat().readFeatures(xhr.responseText));
           } else {
             onError();
           }
         }
         xhr.send();
       },
       strategy: ol.loadingstrategy.bbox
     });
/*    var wfsPointSource = new ol.source.Vector({
        format: new ol.format.GeoJSON(),
        url: function(extent){return 'https://vforwater-gis.scc.kit.edu/geoserver/CAOS/ows?service=WFS&version=2.0.0' +
            '&request=GetFeature&typeName=CAOS:ID_as_identifier&outputFormat=application/json&srsname=EPSG:3857&' +
                        'bbox=' + extent.join(',') + ',EPSG:3857';},
        strategy: ol.loadingstrategy.tile(ol.tilegrid.createXYZ())
    })*/
    var wfsPointLayer = new ol.layer.Vector({
        source: wfsPointSource,
        renderMode: 'image',
        style: new ol.style.Style({
            image: new ol.style.Circle({
                radius: 6,
                fill: new ol.style.Fill({
                    color: 'blue'
                }),
                stroke: new ol.style.Stroke({
                    color: 'black',
                    width: 0.5
                })
            })
        })
    })


/*    var featureSource = new ol.source.Vector({
        features: (new ol.format.GeoJSON()).readFeatures('https://vforwater-gis.scc.kit.edu/geoserver/CAOS/ows?service=WFS&version=2.0.0' +
            '&request=GetFeature&typeName=CAOS:ID_as_identifier&outputFormat=application/json&srsname=EPSG:3857'
    )})*/
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

	var vectorSource = new ol.source.TileWMS({
		url: 'https://vforwater-gis.scc.kit.edu/geoserver/wms',
		params: {LAYERS: 'LUBW:vfwheron_basiseinzugsgebiet'},
		// visible: False,
	});
    var vectorLayer = new ol.layer.Tile({
		source: vectorSource,
	});

	var map_tar = document.getElementById("map");
	var map = new ol.Map({
		// renderer: 'canvas',
		overlays: [overlay],
		target: map_tar,
		// layers: [mapLayer, vectorLayer, wfsPointLayer], // *works only on the server
		layers: [mapLayer, vectorLayer, wmsPointLayer], // *use that one on your local machine
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
				tipLabel: 'Auf die verfügbaren Daten zoomen',
				extent: dataExt,
			}),
			],
        view: mapView//dataview
	});

/* function download_file(url) { // unused/deleteable
   window.location.assign(url);
 }*/
/* function httpGet(theUrl)
{
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
    }
    else
    {// code for IE6, IE5
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4 && xmlhttp.status==200)
        {
            return xmlhttp.responseText;
        }
    }
    xmlhttp.open("GET", theUrl, false );
    xmlhttp.send();
}*/
// get information about your data in a popup when you click on a data point in the map
	map.on('singleclick', showinfo);

    function showinfo(evt) {
        var pixel = map.getEventPixel(evt.originalEvent);
		var viewResolution = /** @type {number} */ (mapView.getResolution());
		var url = wmsPointSource.getGetFeatureInfoUrl(
			evt.coordinate, viewResolution, 'EPSG:3857',
			{'INFO_FORMAT': 'text/html'});
		// supported formats are [text/plain, text/html, application/vnd.ogc.gml]
        // console.log(evt.coordinate)
  /*      var features = map.getFeaturesAtPixel(evt.pixel);
        console.log(map.forEachLayerAtPixel(pixel));
        console.log(map.forEachLayerAtPixel(map.getEventPixel(evt.originalEvent)));
        if (!features) {
          // info.innerText = '';
          // info.style.opacity = 0;
          return;
        }*/
        // var properties = features[0].getProperties();
        // console.log(properties)
		if (url) {
			document.getElementById('popup-content').innerHTML =
			'<iframe seamless src=' + url + ' style="border: none; allowtransparency:true"></iframe>';
			overlay.setPosition(evt.coordinate);
		}
	};

/*comment the following in your development environment to avoid error messages*/
  map.on('pointermove', function(evt) {
    if (evt.dragging) {
      return;
    }
    var pixel = map.getEventPixel(evt.originalEvent);
    var hit = map.forEachLayerAtPixel(pixel, function (feature, layer) {
      return feature;
    }, null, function(layer){return layer === wfsPointLayer}
    );
    map.getTargetElement().style.cursor = hit ? 'pointer' : '';
  });

}
