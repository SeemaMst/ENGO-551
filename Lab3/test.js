function start_marking(geojson_data){

    
    var json_date= geojson_data;
    if (json_date.features.length==0){
        alert("No building permits for this date range.");
        return;
    }
    // console.log(typeof json_date)
    // console.log("json data"+json_date);
    // L.geoJSON(json_date.features,{onEachFeature: onEachFeature}).addTo(mymap)
    var oms = new OverlappingMarkerSpiderfier(mymap);
    var popup = new L.Popup();
    oms.addListener('click', function(marker) {
    popup.setContent(marker.desc);
    popup.setLatLng(marker.getLatLng());
    mymap.openPopup(popup);
    });
    oms.addListener('spiderfy', function(markers) {
        mymap.closePopup();
    });
    

    var markers = L.markerClusterGroup();
    for (i=0; i<json_date.features.length;i++){
        // console.log("json data geometry:"+json_date.features[i].geometry.coordinates);
        // console.log("json data properties issueddate:"+json_date.features[i].properties.issueddate);
        var datum=json_date.features[i];
        var loc = new L.LatLng(datum.geometry.coordinates[1], datum.geometry.coordinates[0]);
        var marker = new L.Marker(loc);
        var popcontent="issueddate: "+datum.properties.issueddate+"<br>"+
                        "workclassgroup: "+datum.properties.workclassgroup+"<br>"+
                        "contractorname: "+datum.properties.contractorname+"<br>"+
                        "communityname: "+datum.properties.communityname+"<br>"+
                        "originaladdress: "+datum.properties.originaladdress;
        marker.desc = popcontent;//popcontent
        // mymap.addLayer(marker);
        oms.addMarker(marker);

        markers.addLayer(marker);
        mymap.addLayer(markers);

    }
}