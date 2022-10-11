var config = {
  apiKey: "AIzaSyBANw2_glWqCwXYeXmzIcyoXXJNA_fJ_Z0",
  authDomain: "webhw-1556367726853.firebaseapp.com",
  databaseURL: "https://webhw-1556367726853.firebaseio.com",
  projectId: "webhw-1556367726853",
  storageBucket: "webhw-1556367726853.appspot.com",
  messagingSenderId: "435267733785",
  appId: "1:435267733785:web:e714df50fd660e46fb1d88"
};

firebase.initializeApp(config);
var database = firebase.database();

database.ref("/gogobike_location").on('value', function(snapshot){
      updata_marker(snapshot.val().lat, snapshot.val().lng)
});

function updata_marker(lat, lng){
    var latLng = new google.maps.LatLng(lat, lng)
    marker.setPosition(latLng);
    map.setZoom(20);
    map.panTo(latLng);
}
