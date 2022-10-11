var marker;

function initMap() {
  var directionsService = new google.maps.DirectionsService();
  var DirectionsRenderer = new google.maps.DirectionsRenderer();

    map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: 0, lng: 0},
      zoom: 3,
      styles: [{
        featureType: 'poi',
        stylers: [{ visibility: 'off' }]  // Turn off points of interest.
      }, {
        featureType: 'transit.station',
        stylers: [{ visibility: 'off' }]  // Turn off bus stations, train stations, etc.
      }],
      disableDoubleClickZoom: true,
      streetViewControl: false,
      mapTypeControl: false,
      fullscreenControl: false
    });

    marker = new google.maps.Marker({
      map: map
    });
    
    marker.addListener('click', function() {
      infowindow.open(map, marker);
      $(".hide1").toggle();
    });
    
    DirectionsRenderer.setMap(map);

    // 路線相關設定
    var request = {
        origin: { lat: 25.034010, lng: 121.562428 },
        destination: { lat: 25.037906, lng: 121.549781 },
        travelMode: 'DRIVING'
    };

    // 繪製路線
    directionsService.route(request, function (result, status) {
        if (status == 'OK') {
            // 回傳路線上每個步驟的細節
            console.log(result.routes[0].legs[0].steps);
            DirectionsRenderer.setDirections(result);
        } else {
            console.log(status);
        }
    });
}


