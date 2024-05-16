var map = L.map('map', {
    center: [54.5260, 15.2551],
    zoom: 4,
    minZoom: 3,
    maxZoom: 7,
    maxBounds: [
        [35, -10],
        [70, 40]
    ]
});

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var airports = [
    { name: "Heathrow Airport", location: [51.4700, -0.4543] },
    { name: "Charles de Gaulle Airport", location: [49.0097, 2.5479] },
    { name: "Frankfurt Airport", location: [50.0379, 8.5622] },
    { name: "Madrid Barajas Airport", location: [40.4839, -3.5679] },
    { name: "Schiphol Airport", location: [52.3105, 4.7683] },
    { name: "Leonardo da Vinci–Fiumicino Airport", location: [41.8003, 12.2389] },
    { name: "Munich Airport", location: [48.3538, 11.7861] },
    { name: "Barcelona–El Prat Airport", location: [41.2974, 2.0833] },
    { name: "Gatwick Airport", location: [51.1537, -0.1821] },
    { name: "Lisbon Portela Airport", location: [38.7742, -9.1342] },
    { name: "Copenhagen Airport", location: [55.6181, 12.6561] },
    { name: "Vienna International Airport", location: [48.1103, 16.5697] },
    { name: "Stockholm Arlanda Airport", location: [59.6519, 17.9186] },
    { name: "Dublin Airport", location: [53.4213, -6.2701] },
    { name: "Zurich Airport", location: [47.4582, 8.5481] },
    { name: "Helsinki-Vantaa Airport", location: [60.3172, 24.9633] },
    { name: "Oslo Gardermoen Airport", location: [60.1939, 11.1004] },
    { name: "Brussels Airport", location: [50.9010, 4.4844] },
    { name: "Athens International Airport", location: [37.9364, 23.9475] },
    { name: "Warsaw Chopin Airport", location: [52.1657, 20.9670] }
];

airports.forEach(function(airport) {
    L.marker(airport.location).addTo(map)
        .bindPopup(airport.name);
});


function fly() {
    map.flyTo([48.8566, 2.3522], 6);
}

$(document).ready(function() {
    map.on('click', function(e) {
        var lat = e.latlng.lat;
        var lng = e.latlng.lng;
        $("#apiout").html(`Clicked at Latitude: ${lat}, Longitude: ${lng}`);
    });
});
