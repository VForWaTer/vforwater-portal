//Create own base layer
function create_map() {
	mapsource = new ol.source.XYZ({url: window.location.origin + "/osm/{z}/{x}/{y}.png"})
	
	var dataExt = JSON.parse(document.getElementById('dataExt').value); // bbox of available data

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

                  vectormap = new ol.layer.Vector({
                  source: vectorSource,
                  style: new ol.style.Style({
                    stroke: new ol.style.Stroke({
                      color: 'rgba(0, 100, 255, 1.0)',
                      width: 1.5
                    })
                  })
                });
 */
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
		layers: [maplayer, vectormap],
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
