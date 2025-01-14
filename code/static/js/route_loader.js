let campo_playera;
let campo_pantalon;
let campo_calzado;
let estado;
let formulario;
let rutas;
let alerta;
let cargando_general;
let chiste = 0;
let chiste_control;
let exito_chiste;
let iframe;
let boton_mostrar_mapa;
let lista_destinos;

document.addEventListener("DOMContentLoaded", function () {
    iframe = document.getElementById("map-frame");
    boton_mostrar_mapa = document.getElementById("boton_generador");
    estado = document.getElementById("estado_visible");
    formulario = document.getElementById("formulario_inventario");
    rutas = document.getElementById("visibiilidad_rutas");
    campo_playera = document.getElementById("campos_playera");
    campo_pantalon = document.getElementById("campos_pantalon");
    campo_calzado = document.getElementById("campos_calzado");
    alerta = document.getElementById('alerta_existencia');
    cargando_general = document.getElementById('cargar_general');
    chiste_control = document.getElementById('chistolongo');
    exito_chiste = document.getElementById('exito_chiste');
    lista_destinos = document.getElementById('lista_rutas');
    chiste_control.style.display = "none";
    exito_chiste.style.display = "none";
    chiste_control.addEventListener("click", (event) =>{
        manejar_chiste(estado.value);
    });
    cargar_inventario(estado.value);
    estado.addEventListener("change", (event) => {
        cargar_inventario(estado.value);
    });
    window.addEventListener("keydown", konami);
});

function vaciar(elemento){
    while(elemento.firstElementChild){
        elemento.firstElementChild.remove();
    }
}

async function manejar_chiste(estado_valor){
    chiste_control.style.display = "none";
    rutas.style.display =  "none";
    alerta.style.display =  "none";
    cargando_general.style.display = "flex";
    let repuesta = await fetch(urlUser_chiste, {
        method: "POST",
        body: estado_valor
    }).then(response => response.json()).then(data => {
        cargando_general.style.display = "none";
        if('error' in data){
            alerta.innerHTML = "No se pudieron generar rutas para ".concat(estado.value);
            alerta.style.display = "block";
        }else{
            exito_chiste.style.display = "block";
            rutas.style.display = "block";
        }
    }).catch(error => {
        cargando_general.style.display = "none";
        alerta.innerHTML = "Ups, intentelo mas tarde";
        alerta.style.display = "block";
    });
}

async function cargar_inventario(estado_valor){
    formulario.style.display = "none";
    iframe.style.display = "none";
    lista_destinos.innerHTML = "";
    boton_mostrar_mapa.style.display = "inline-block";
    rutas.style.display =  "none";
    alerta.style.display =  "none";
    exito_chiste.style.display = "none";
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
            alerta.innerHTML = "No hay que entregar algo en ".concat(estado.value);
            alerta.style.display = "block";
        }else{
            temp = "";
            for(i=0;i<data['playera'].length;i++){
                temp = temp.concat('<label for="pl-', data['playera'][i][0], '" class="col-sm-8 col-form-label">Talla ', data['playera'][i][0], '</label><div class="col-sm-4"><input id="pl-', data['playera'][i][0], '" type="number" value="', data['playera'][i][1], '" name="pl-', data['playera'][i][0], '" class="form-control"></div>');
            }
            campo_playera.innerHTML = temp;
            temp = "";
            for(i=0;i<data['pantalon'].length;i++){
                temp = temp.concat('<label for="pa-', data['pantalon'][i][0], '" class="col-sm-8 col-form-label">Talla ', data['pantalon'][i][0], '</label><div class="col-sm-4"><input id="pa-', data['pantalon'][i][0], '" type="number" value="', data['pantalon'][i][1], '" name="pa-', data['pantalon'][i][0], '" class="form-control"></div>');
            }
            campo_pantalon.innerHTML = temp;
            temp = "";
            for(i=0;i<data['calzado'].length;i++){
                temp = temp.concat('<label for="ca-', data['calzado'][i][0], '" class="col-sm-8 col-form-label">Talla ', data['calzado'][i][0], '</label><div class="col-sm-4"><input id="ca-', data['calzado'][i][0], '" type="number" value="', data['calzado'][i][1], '" name="ca-', data['calzado'][i][0], '" class="form-control"></div>');
            }
            campo_calzado.innerHTML = temp;
            formulario.style.display = "block";
            rutas.style.display = "block";
        }
    }).catch(error => {
        cargando_general.style.display = "none";
        alerta.innerHTML = "Ups, intentelo mas tarde";
        alerta.style.display = "block";
    });
}

function generar_destino(nombre, direccion, cantidad){
    elemento_lista = '<div class="list-group-item list-group-item-action"><div class="d-flex w-100 justify-content-between"><h4 class="mb-3">Destino: ';
    if(cantidad == 0){
        nombre = "Delegación ".concat(nombre);
    }
    elemento_lista = elemento_lista.concat(nombre, '</h4>');
    if(cantidad > 0){
        elemento_lista = elemento_lista.concat('<h4>Entregar <b>', cantidad, '</b> uniformes</h4>');
    }
    elemento_lista = elemento_lista.concat('</div><p class="mb-1">Direccion: ', direccion, '</p></div>');
    return elemento_lista;
}

async function marcar_completada(claves, i) {
    let anuncio = document.getElementById('marcar_exito_'.concat(i))
    vaciar(anuncio)
    enviar = JSON.stringify(claves)
    let respuesta = await fetch(urlUser_completar, {
        method: "POST",
        body: enviar
    }).then(response => response.json()).then(data => {
        anuncio.innerHTML = '<h1 class="text-center"><span class="badge text-bg-success">Operacion exitosa</span></h1>'
    }).catch(error => {
        anuncio.innerHTML = '<h1 class="text-center"><span class="badge text-bg-warning">Ups, intentelo más tarde</span></h1>'
    });
}

async function renderizar_mapa(url) {
    const mapContainer = document.getElementById("map-container");
    let respuesta = await fetch(url, {method: "GET"}).then(response => response.json()).then(data => {
        mapContainer.style.display = "block";
        for (let i = 0; i < data['lista'].length; i++) {
            const ruta_datos = data['lista'][i];
            
            lista_general = '<h2 class="text-center fw-bold">Ruta '.concat((i+1), '</h2><div class="list-group p-1">');
            for (let j = 0; j < ruta_datos.length; j++) {
                const parada = ruta_datos[j];
                lista_general = lista_general.concat(generar_destino(parada['nombre'], parada['direccion'], parada['cantidad']));
            }
            lista_general = lista_general.concat('<div class="d-flex justify-content-center p-3" id="marcar_exito_',i,'"><button class="btn btn-primary btn-lg" id="marcar_',i,'">Marcar completadas todas las entregas de la ruta ', (i+1),'</button></div></div>');
        }
        lista_destinos.innerHTML = lista_general;

        for (let i = 0; i < data['mapa'].length; i++) {
            let boton = document.getElementById('marcar_'.concat(i));
            boton.addEventListener("click", (event) => {
                marcar_completada(data['mapa'][i], i);
            });
        }

        rutaiframe = urlUser_render.concat('?ruta=', JSON.stringify(data['mapa']), '&estado=', estado.value);
        console.log(rutaiframe)
        iframe.setAttribute('src',rutaiframe);

        // Mostrar el loader mientras el iframe se carga
        iframe.onload = function () {
            loader.style.display = "none";
            iframe.style.display = "inline-block";
        };
    }).catch(error => {
        loader.style.display = "none";
        alerta.innerHTML = "Ups, intentelo mas tarde";
        alerta.style.display = "block";
    });
}

function procesar_mapa(){
    const loader = document.getElementById("loader");

    boton_mostrar_mapa.style.display = "none";
    loader.style.display = "flex";
    let rutaiframe = urlUser.concat('?estado=', estado.value,'&data={');
    for(let i = 0; i < formulario.length; i++){
        if(formulario[i].nodeName == 'INPUT'){
            rutaiframe = rutaiframe.concat('"', formulario[i].name, '":', formulario[i].value, ",");
        }
    }
    rutaiframe = rutaiframe.slice(0, -1);
    rutaiframe = rutaiframe.concat("}");
    renderizar_mapa(rutaiframe);
}

function konami(event){
    if(event.key == "ArrowUp" && (chiste == 0 || chiste == 1)){
        chiste++;
    }else if(event.key == "ArrowDown" && (chiste == 2 || chiste == 3)){
        chiste++;
    }else if(event.key == "ArrowLeft" && (chiste == 4 || chiste == 6)){
        chiste++;
    }else if(event.key == "ArrowRight" && (chiste == 5 || chiste == 7)){
        chiste++;
    }else if(event.key == "b" && chiste == 8){
        chiste++;
    }else if(event.key == "a" && chiste == 9){
        chiste++;
    }else if(event.key == "Enter" && chiste == 10){
        chiste_control.style.display = "flex";
        alerta.style.display = "none";
        exito_chiste.style.display = "none";
    }else{
        chiste == 0;
    }
}