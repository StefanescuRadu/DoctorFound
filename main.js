let map;
let position ;
function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: -34.397, lng: 150.644 },
        zoom: 15,
    });
}
function getLocation() {
    if (navigator.geolocation) {
       position = navigator.geolocation.getCurrentPosition(showPosition);
       console.log(position);
    } else {
        console.log("Geolocation is not supported by this browser.") ;
    }
}

function showPosition(position) {
    console.log("Latitude: " + position.coords.latitude +
        "Longitude: " + position.coords.longitude)
}
initMap();

// https://developers.google.com/maps/documentation/javascript/overview#maps_map_simple-css