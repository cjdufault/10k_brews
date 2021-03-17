function showLocation(name, latitude, longitude, token){
    let location_map = L.map("location_map", {scrollWheelZoom: false}).setView([latitude, longitude], 12);

    L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=" + token, {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: "mapbox/streets-v11",
    tileSize: 512,
    zoomOffset: -1}).addTo(location_map);

    L.control.scale().addTo(location_map);

    let location = L.marker([latitude, longitude]).addTo(location_map);
    location.bindPopup(name);
}
