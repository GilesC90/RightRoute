

async function initMap() {
    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer();
    const map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 47.480195, lng: -122.20392 },
        zoom: 18
    });

    directionsRenderer.setMap(map);
    directionsRenderer.setPanel(document.getElementById("sidebar"));

    

    const onChangeHandler = function () {
        calculateAndDisplayRoute(directionsService, directionsRenderer);
    };

    document.getElementById("start").addEventListener("change", onChangeHandler);
    document.getElementById("end").addEventListener("change", onChangeHandler);
    }

    function calculateAndDisplayRoute(directionsService, directionsRenderer) {
        directionsService
            .route({
                origin: {
                    query: document.getElementById("start").value,
                },
                destination: {
                    query: document.getElementById("end").value,
                },
                travelMode: google.maps.TravelMode.WALKING,
                unitSystem: google.maps.UnitSystem.IMPERIAL,
                })
                .then((response) => {
                    directionsRenderer.setDirections(response);
                    console.log(response.routes[0].overview_polyline)
                    document.querySelector("input#path").value=response.routes[0].overview_polyline;

                    var myForm = document.querySelector('form');
                    myForm.onsubmit = function(e){
                        e.preventDefault();
                        const formData = {
                            "name" : myForm.querySelector('#name').value,
                            "distance" : myForm.querySelector('#distance').value,
                            "path" : response.routes[0].overview_polyline
                        }
                        fetch("http://localhost:5000/route/create", { method :'POST', body : JSON.stringify(formData), headers:{"Content-Type":"application/json"}})
                            .then( response => response.json() )
                            .then( data => console.log(data) )
                    }
                });
    }





// 25b8e1b87e749dc7 map id