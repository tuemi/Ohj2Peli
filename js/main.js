//Lähetetään dataa pythoniin
// POST
function sendlocation(e)   {
    fetch('http://127.0.0.1:3000/location', {

        // Declare what type of data we're sending
        headers: {
        'Content-Type': 'application/json'
        },

        // Specify the method
        method: 'POST',

        // A JSON payload
        body: JSON.stringify({
            "cords": e
        })
    }).then(function (response) { // At this point, Flask has printed our JSON
        return response.text();
    }).then(function (text) {

        console.log('POST location: ');

        // Should be 'OK' if everything was successful
        console.log(text);
    });
}

async function getcords() {
    try {
        let response = await fetch('http://127.0.0.1:3000/maat/kaupungit/koordinaatit');

        if (!response.ok) {
            throw new Error('Failed to fetch');
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
            throw new Error('Failed to fetch');
        }
        let jsonData = await response.json();
        const cities = jsonData.kaupungit
        return(cities)

    } catch (error) {
        console.error(error);
    }
}


function fly() {
    sendlocation([60.2, 20.33])
}
//fly()



async function getstartcity() {
    try {
        let response = await fetch('http://127.0.0.1:3000/maat/aloitus');

        if (!response.ok) {
            throw new Error('Failed to fetch');
        }
        let jsonData = await response.json();
        const startcity = jsonData.kaupungit
        return(startcity)

    } catch (error) {
        console.error(error);
    }
}

function onClick(e) {
    let popup = e.target.getPopup();
    let content = popup.getContent();
     console.log(content);
    let coords = e.latlng;
    console.log(coords)
    //alert("Lennatko " +content);
    if (confirm("Lento maksaa xxx \u20AC" + ", lennetaanko kaupinkiin " + content) == true) {
        console.log("Lennetaan "+coords)

        circle1 = addcurrent(coords)
        // lähetä apilla uusi kaupunki
    } else {
        console.log("Ei lenneta")
    }
}

    //console.log(this._popup);
    //alert(this.getLatLng());

let map = L.map('map').setView([60.1674881,24.9427473], 4);

        // Add the base tile layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);


        let cities = getcities() //haetaan kaupungit
            .then(function (cities) {
                cities.forEach(
                    function (city){
                        let coords = city.slice(1) //leikataan ensimmäinen arvo(kaupungin nimi) pois
                        //console.log(coords)
                        let marker = L.marker(coords).addTo(map).on('dblclick', onClick);
                        marker.bindPopup(city[0]).openPopup();
                    })
            })

        let city = getstartcity() //haetaan aloituskaupunki
            .then(function (cities) {
                cities.forEach(
                    function (city){
                        let coords = city.slice(1) //leikataan ensimmäinen arvo(kaupungin nimi) pois
                        console.log(coords)
                        circle1 = addstartlocation(coords)
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



function fly() {
       console.log("Painallus")
        }

*/


function addstartlocation(e){
    //console.log("Lisätään nykyinen sijainti")
    console.log("Alkupiste lisätty")
    let circle1 = L.circle(e, {
        color: 'blue',
        fillColor: '#f03',
        fillOpacity: 0.5,
        radius: 50000
    }).addTo(map);
    map.flyTo(e, 8);
    return(circle1)
}

function addcurrent(e){
    //console.log("Lisätään nykyinen sijainti")
    poista()
    let circle1 = L.circle(e, {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.5,
        radius: 50000
    }).addTo(map);
    map.flyTo(e, 6);
    sendlocation([e])

    return(circle1)
}

function poista() {
    console.log("Edellinen poistettu")
    return map.removeLayer(circle1)
}