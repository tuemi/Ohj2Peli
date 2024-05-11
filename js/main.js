
// Initialize the map


async function getapi() {
    try {
        // Fetch data using the Fetch API
        let response = await fetch('http://127.0.0.1:3000/maat/kaupungit/koordinaatit');

        // Check if response is ok
        if (!response.ok) {
            throw new Error('Failed to fetch joke');
        }
        let jsonData = await response.json();
        const naatit = jsonData.koordinaatit
        //naatit.forEach(function (sijainti){console.log((sijainti))})
        //console.log(naatit)
        //console.log(jsonData.koordinaatit);
        return(naatit)

    } catch (error) {
        console.error(error);
    }
}


//document.getElementById("apiout").innerText = getapi()

let map = L.map('map').setView([51.505, -0.09], 5);

        // Add the base tile layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);


    /* Array of marker coordinates
        let markers = [
            [59.9133301, 10.7389701],
            [39.6112768, 6.129799],
            [51.49, -0.08]
        ];
       */
        console.log(getapi())
        let markers = [

        ];

        // Add markers to the map
        markers.forEach(function(markerLocation) {
            let marker = L.marker(markerLocation).addTo(map);
            marker.bindPopup("Coordinates: " + markerLocation).openPopup();
        });