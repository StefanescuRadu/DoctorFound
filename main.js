let map;

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: -34.397, lng: 150.644 },
        zoom: 8,
    });
}

initMap();

// https://developers.google.com/maps/documentation/javascript/overview#maps_map_simple-css