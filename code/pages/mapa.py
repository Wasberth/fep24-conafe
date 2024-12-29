from flask import render_template, request, redirect, url_for, session, jsonify, make_response
from decos import route, nav
from mongo_objects._common_types_ import Estado_republica
import requests
import json
import folium
import folium.plugins

from mode_handler import get_url

MAPA_URL = get_url('ubicacion')


@route('/mapa')
@nav('Mapa de CCT')
def mapa():
    """Renderiza la página donde se muestra el mapa."""
    return render_template('mapa.html')

@route('/mapa_visualizado')
def mapa_visualizado():

    # Obtener los datos del microservicio
    try:
        response = requests.get(MAPA_URL + '/lista_lugares')
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        return jsonify({"error": "Error comunicándose con el microservicio", "details": str(e)}), 500


    inicio = [23.108028, -101.639617]
    # Crear un mapa centrado en el punto inicial y grupos de puntos
    mapa = folium.Map(location=inicio, zoom_start=5)
    mcg = folium.FeatureGroup(name="CCTs")
    mapa.add_child(mcg)

    #Se itera a través de cada estado y se agregan los puntos a su estado
    for estado in Estado_republica:
        grupo = estado
        grupo = folium.plugins.FeatureGroupSubGroup(mcg, estado)
        mapa.add_child(grupo)
        
        for dict in microservice_data["result"]:
            if (dict["estado"].title()) == estado:
                folium.Marker(
                location=[float(dict["latitud"]),float(dict["longitud"])],
            popup=folium.Popup(f"Nombre: {dict['nombre']}\nEstado: {dict['estado']}\nMunicipio: {dict['municipio']}\nComunidad: {dict['comunidad']}\nSede: {dict['sede']}\nRegión: {dict['region']}", parse_html=True, max_width=100, lazy=True)).add_to(grupo)
    
    folium.LayerControl(collapsed=False).add_to(mapa)    
    mapa.save('templates/mapa_cct.html')
    return render_template('mapa_cct.html')