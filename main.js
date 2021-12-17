
let directionsService = new google.maps.DirectionsService()
let directionsRenderer = new google.maps.DirectionsRenderer();
let autocomplete = new google.maps.places.Autocomplete(
    document.getElementById("autocomplete"),
    {
        types: ['establishment'],
        componentRestrictions: {'country':['AU']},
        fields: ['place_id','geometry','name']
    });

function initMap() {


    var mapOptions = {
        zoom:7,
        center: {lat:44.439211,lng:26.112343}
    }
    var map = new google.maps.Map(document.getElementById('map'), mapOptions);
    directionsRenderer.setMap(map);
    directionsRenderer.setPanel(document.getElementById('directionsPanel'));
}

function calcRoute() {

    var start = document.getElementById('start').value;
    var end = document.getElementById('end').value;
    var request = {
        origin:start,
        destination:end,
        travelMode: 'DRIVING'
    };
    directionsService.route(request, function(response, status) {
        if (status == 'OK') {
            directionsRenderer.setDirections(response);
        }
    });
}
initMap()
// https://developers.google.com/maps/documentation/javascript/overview#maps_map_simple-css
