

async function getapi() {
    try {
        // Fetch data using the Fetch API
        let response = await fetch('http://127.0.0.1:3000/maat/kaupungit/koordinaatit');

        // Check if response is ok
        if (!response.ok) {
            throw new Error('Failed to fetch joke');
        }
        let jsonData = await response.json();

        console.log(jsonData);
        return(jsonData)

    } catch (error) {
        console.error(error);
    }
}

getapi();