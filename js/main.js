
async function getcords() {
    try {
        let response = await fetch('http://127.0.0.1:3000/maat/kaupungit/koordinaatit');

        if (!response.ok) {
            throw new Error('Failed to fetch joke');
        }
        let jsonData = await response.json();
        const naatit = jsonData.koordinaatit
        return(naatit)

    } catch (error) {
        console.error(error);
    }
}

async function getcities() {
    try {
        let response = await fetch('http://127.0.0.1:3000/maat/kaupungit');

        if (!response.ok) {
            throw new Error('Failed to fetch joke');
        }
        let jsonData = await response.json();
        const cities = jsonData.kaupungit
        return(cities)

    } catch (error) {
        console.error(error);
    }
}
function onClick(e) {
    var popup = e.target.getPopup();
    var content = popup.getContent();
    console.log(content);
    //alert("Lennatko " +content);
    if (confirm("Lento maksaa" + ", lennetaanko kaupinkiin " + content) == true) {
        console.log("Lennetaan")
    } else {
        console.log("Ei lenneta")
    }
}

    //console.log(this._popup);
    //alert(this.getLatLng());

let map = L.map('map').setView([60.1674881,24.9427473], 5);

        // Add the base tile layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);


        let cities = getcities() //haetaan kaupunkit
            .then(function (cities) {
                cities.forEach(
                    function (city){
                        var coords = city.slice(1) //leikataan ensimmäinen arvo(kaupungin nimi) pois
                        //console.log(coords)
                        let marker = L.marker(coords).addTo(map).on('dblclick', onClick);
                        marker.bindPopup(city[0]).openPopup();

                    })
            })


/* Toimii
        let naatit = getcords()
            .then(function (result) {
               result.forEach(
                   function (markerLocation){
                    let marker = L.marker(markerLocation).addTo(map);
                    marker.bindPopup("Coordinates: " + markerLocation).openPopup();
                    }
               )
            })
*/

function fly() {
       console.log("Painallus")
        }