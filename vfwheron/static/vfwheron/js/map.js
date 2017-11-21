//Create own base layer
function create_map() {
	mapSource = new ol.source.XYZ({url: window.location.origin + "/osm/{z}/{x}/{y}.png"})
	
	var dataExt = JSON.parse(document.getElementById('dataExt').value); // bbox of available data
/*    var sample_locations = document.getElementById('sample_locations').value;
    console.log(sample_locations);

// Build a vector layer:
    var image = new ol.style.Circle({
        radius: 5,
        fill: null,
        stroke: new ol.style.Stroke({color: 'blue', width: 1})
    });

    var styles = {
        'Point': new ol.style.Style({
          image: image
        }),
    }

    var styleFunction = function(feature) {
        return styles[feature.getGeometry().getType()];
      };

    var vectorSource = new ol.source.Vector({
        features: (new ol.format.GeoJSON()).readFeatures(sample_locations)
      });

    var vectorLayer = new ol.layer.Vector({
        source: vectorSource,
        style: styleFunction
      });*/

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


//	Access as wfs - not used now
/*		vectorSource = new ol.source.Vector({
              format: new ol.format.GeoJSON({defaultDataProjection:"ESPG:4326"}),
                url: function(extent) {
              return 'https://vforwater-gis.scc.kit.edu/geoserver/wfs?service=WFS&' +
              'version=2.0.0&request=GetFeature&typename=LUBW:vfwheron_basiseinzugsgebiet&' +
              'outputFormat=application/json&' +
              'bbox=' + extent.join(',') + ',EPSG:4326';
        },
        strategy: ol.loadingstrategy.bbox
                });

                  vectorMap = new ol.layer.Vector({
                  source: vectorSource,
                  style: new ol.style.Style({
                    stroke: new ol.style.Stroke({
                      color: 'rgba(0, 100, 255, 1.0)',
                      width: 1.5
                    })
                  })
                });
 */
    WMSpointSource = new ol.source.TileWMS({
		url: 'https://vforwater-gis.scc.kit.edu/geoserver/wms',
		serverType:'geoserver',
		params: {
		    LAYERS: 'CAOS:get_important_info',
//		    LAYERS: 'CAOS:get_important_info',
		    TILED: true,
		    STYLES: 'CAOS:new_point',
//		    STYLES: 'Light Blue Circle',
        },
        name: 'WMSpointSource'
	});
	pointMap = new ol.layer.Tile({
		source: WMSpointSource,
	});

/*  pointMap = new ol.layer.Vector({
        source: new ol.source.Cluster({
          distance: 40,
          source: new ol.source.Vector({
            url: 'https://vforwater-gis.scc.kit.edu/geoserver/kml',
            format: new ol.format.KML({
              extractStyles: true
            })
          })
        }),
//        style: styleFunction
      });*/
    /*WMSpointSource = new ol.source.Vector({
      format: new ol.format.GeoJSON({defaultDataProjection:"ESPG:4326"}),
        url: function(extent) {
      return 'https://vforwater-gis.scc.kit.edu/geoserver/ows?service=WFS&' +
      'version=1.0.0&request=GetFeature&typename=CAOS:lt_location&' +
      'outputFormat=text/javascript';
*//*      'outputFormat=application/json&' +
      'bbox=' + extent.join(',') + ',EPSG:2169';*//*
    },
    strategy: ol.loadingstrategy.bbox
            });

    pointMap = new ol.layer.Vector({
      source: WMSpointSource,
      style: new ol.style.Style({
        stroke: new ol.style.Stroke({
          color: 'rgba(0, 100, 255, 1.0)',
          width: 1.5
        })
      })
    });*/
/*    WMSpointSource = new ol.source.WFS({
//        url: 'http://vforwater-gis.scc.kit.edu/geoserver/CAOS/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=CAOS:lt_location&maxFeatures=50&outputFormat=text%2Fjavascript'
        url: 'https://vforwater-gis.scc.kit.edu/geoserver/wfs',
        params: {LAYERS: 'CAOS:lt_location'}
    });
    pointMap = new ol.source.Tile({
        source: WMSpointSource,
    })*/

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
    var url = WMSpointSource.getGetFeatureInfoUrl(
        evt.coordinate, viewResolution, 'EPSG:3857',
        {'INFO_FORMAT': 'text/html'});
    if (url) {
      document.getElementById('popup-content').innerHTML =
      '<iframe seamless src=' + url + '></iframe>';
      overlay.setPosition(evt.coordinate);
    }
  });

/*comment the following in your development environment to avoid error messages*/
  map.on('pointermove', function(evt) {
    if (evt.dragging) {
      return;
    }
    var pixel = map.getEventPixel(evt.originalEvent);
    var hit = map.forEachLayerAtPixel(pixel, function (feature, layer) {
      return feature;
    }, null, function(layer){return layer === pointMap}
    );
    map.getTargetElement().style.cursor = hit ? 'pointer' : '';
  });


}
