from flask import render_template, request, redirect, url_for, session, jsonify, make_response
from decos import route, nav
import requests
import json
import folium

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


    cdmx = [-99.1332, 19.4326]
    # Crear un mapa centrado en el punto inicial
    mapa = folium.Map(location=cdmx[::-1], zoom_start=6)

    for obj in microservice_data["result"]:
        
        folium.Marker(
        location=[float(obj["latitud"]),float(obj["longitud"])],
        popup=folium.Popup(obj["sede"], parse_html=True, max_width=100),
        ).add_to(mapa)
        #print(microservice_data["result"][0]["clave"])
        #print(type(microservice_data["result"][0]["clave"]))
        
    mapa.save('templates/mapa_cct.html')
    return render_template('mapa_cct.html')