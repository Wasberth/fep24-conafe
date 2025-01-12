let campo_playera;
let campo_pantalon;
let campo_calzado;
let estado;
let formulario;
let rutas;
let alerta;
let cargando_general;

document.addEventListener("DOMContentLoaded", function () {
    estado = document.getElementById("estado_visible");
    formulario = document.getElementById("formulario_inventario");
    rutas = document.getElementById("visibiilidad_rutas");
    campo_playera = document.getElementById("campos_playera");
    campo_pantalon = document.getElementById("campos_pantalon");
    campo_calzado = document.getElementById("campos_calzado");
    alerta = document.getElementById('alerta_existencia');
    cargando_general = document.getElementById('cargar_general');
    cargar_inventario(estado.value)
    estado.addEventListener("change", (event) => {
        cargar_inventario(estado.value)
    });
});

function vaciar(elemento){
    while(elemento.firstElementChild){
        elemento.firstElementChild.remove();
    }
}

async function cargar_inventario(estado_valor){
    formulario.style.display = "none";
    rutas.style.display =  "none";
    alerta.style.display =  "none";
    cargando_general.style.display = "flex";
    let respuesta = await fetch(urlUser_form, {
        method: "POST",
        body: estado_valor
    }).then(response => response.json()).then(data => {
        vaciar(campo_playera);
        vaciar(campo_pantalon);
        vaciar(campo_calzado);
        cargando_general.style.display = "none"
        if('error' in data){
            formulario.style.display = "none"
            rutas.style.display = "none"
            alerta.innerHTML = "No hay que entregar algo en ".concat(estado.value)
            alerta.style.display = "block"
        }else{
            temp = "";
            for(i=0;i<data['playera'].length;i++){
                temp = temp.concat('<label for="pa_', data['playera'][i][0], '" class="col-sm-8 col-form-label">Talla ', data['playera'][i][0], '</label><div class="col-sm-4"><input id="pa-', data['playera'][i][0], '" type="number" value="', data['playera'][i][1], '" name="pa-', data['playera'][i][0], '" class="form-control"></div>');
            }
            campo_playera.innerHTML = temp;
            temp = "";
            for(i=0;i<data['playera'].length;i++){
                temp = temp.concat('<label for="pa_', data['pantalon'][i][0], '" class="col-sm-8 col-form-label">Talla ', data['pantalon'][i][0], '</label><div class="col-sm-4"><input id="pa-', data['pantalon'][i][0], '" type="number" value="', data['pantalon'][i][1], '" name="pa-', data['pantalon'][i][0], '" class="form-control"></div>');
            }
            campo_pantalon.innerHTML = temp;
            temp = "";
            for(i=0;i<data['playera'].length;i++){
                temp = temp.concat('<label for="pa_', data['calzado'][i][0], '" class="col-sm-8 col-form-label">Talla ', data['calzado'][i][0], '</label><div class="col-sm-4"><input id="pa-', data['calzado'][i][0], '" type="number" value="', data['calzado'][i][1], '" name="pa-', data['calzado'][i][0], '" class="form-control"></div>');
            }
            campo_calzado.innerHTML = temp;
            formulario.style.display = "block"
            rutas.style.display = "block"
        }
    });
}

function procesar_mapa(){
    const iframe = document.getElementById("map-frame");
    const loader = document.getElementById("loader");
    const mapContainer = document.getElementById("map-container");
    const boton = document.getElementById("boton_generador");

    boton.remove();
    loader.style.display = "flex";
    let rutaiframe = urlUser.concat('?data={');
    for(let i = 0; i < formulario.length; i++){
    // for(let i = 0; i < 5; i++){
        if(formulario[i].nodeName == 'INPUT'){
            rutaiframe = rutaiframe.concat('"', formulario[i].name, '":', formulario[i].value, ",");
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