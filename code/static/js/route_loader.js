function procesar_mapa(){
    const iframe = document.getElementById("map-frame");
    const loader = document.getElementById("loader");
    const mapContainer = document.getElementById("map-container");
    const boton = document.getElementById("boton_generador");
    const inputs = document.getElementById("formulario_inventario").elements;

    boton.remove();
    loader.style.display = "flex";
    let rutaiframe = urlUser.concat('?data={');
    for(let i = 0; i < inputs.length; i++){
    // for(let i = 0; i < 5; i++){
        if(inputs[i].nodeName == 'INPUT'){
            rutaiframe = rutaiframe.concat('"', inputs[i].name, '":', inputs[i].value, ",");
        }
    }
    rutaiframe = rutaiframe.slice(0, -1);
    rutaiframe = rutaiframe.concat("}");
    console.log(rutaiframe)
    iframe.setAttribute('src',rutaiframe);

    // Mostrar el loader mientras el iframe se carga
    iframe.onload = function () {
        loader.style.display = "none";
        mapContainer.style.display = "block";
    };
}