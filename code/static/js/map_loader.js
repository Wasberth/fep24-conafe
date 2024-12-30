document.addEventListener("DOMContentLoaded", function () {
    const iframe = document.getElementById("map-frame");
    const loader = document.getElementById("loader");
    const mapContainer = document.getElementById("map-container");

    // Mostrar el loader mientras el iframe se carga
    iframe.onload = function () {
        loader.style.display = "none";
        mapContainer.style.display = "block";
    };
});