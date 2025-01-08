from flask import render_template, request, redirect, url_for, session, jsonify, Response
from decos import route, nav
from mongo_objects._common_types_ import Estado_republica
import requests
import folium
import folium.plugins
import math
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pants
from mode_handler import get_url
from pages._check_level_ import restricted
from datetime import datetime
import pandas as pd
from pages._error_ import ConafeException
import json

MAPA_URL = get_url('ubicacion')
CAPTACION_URL = get_url('captacion')

@route("/generador_ruta")
@restricted('AA')
@nav('Generador de rutas')
def generacion_ruta():
    """Renderiza la pagina y formulario para generar rutas de distribucion."""
    # Quiero asumir que los faltantes son los del siguiente año, hay que poner mas registros cuando se pueda
    # Arreglen si es un entero o string pofavo
    current_year = "2024"
    try:
        response = requests.post(CAPTACION_URL + '/tallas_repartibles', json={'year': current_year})
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        raise ConafeException(500, "Error comunicándose con el microservicio", str(e))
    
    # Convertir los datos a un DataFrame de Pandas
    df = pd.DataFrame(microservice_data['result'])
    
    # Validar que las columnas necesarias existan
    required_columns = {'playera', 'pantalon', 'calzado'}
    if not required_columns.issubset(df.columns):
        raise ConafeException(500, "Faltan columnas necesarias en los datos del microservicio")
    
    # Contar las repeticiones de cada talla por tipo de prenda
    tallas_playera = df['playera'].value_counts().reset_index()
    tallas_playera.columns = ['talla', 'cantidad']
    tallas_playera['tipo'] = 'Playera'

    playera_list = tallas_playera.values.tolist()

    tallas_pantalon = df['pantalon'].value_counts().reset_index()
    tallas_pantalon.columns = ['talla', 'cantidad']
    tallas_pantalon['tipo'] = 'Pantalón'

    pantalon_list = tallas_pantalon.values.tolist()

    tallas_calzado = df['calzado'].value_counts().reset_index()
    tallas_calzado.columns = ['talla', 'cantidad']
    tallas_calzado['tipo'] = 'Calzado'

    calzado_list = tallas_calzado.values.tolist()

    # Renderizar la plantilla HTML
    return render_template('ruta.html', playera_list=playera_list, pantalon_list=pantalon_list, calzado_list=calzado_list, stylesheets=['index', 'route_loader'], scripts=['route_loader'])

@route('/mapa_ruta')
def mapa_ruta():
    """Obtiene la lista de CCT's, los agrupa en rutas y genera una ruta optima para la distribucion."""
    # Obtener los datos del microservicio
    formulario = json.loads(request.args.get('data'))
    try:
        response = requests.post(CAPTACION_URL + '/get_distribucion', json=formulario)
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
        response = requests.post(CAPTACION_URL + '/get_coordenadas', json=microservice_data)
        response.raise_for_status() # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json() # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        return jsonify({"error": "Error comunicándose con el microservicio", "details": str(e)}), 500

    # Central de abastos (?)
    start = (-101.639617, 23.108028)
    # Crear un mapa centrado en el punto inicial
    mapa = folium.Map(location=start[::-1], zoom_start=5)
    folium.Marker(location=start[::-1], popup="Ciudad de México", icon=folium.Icon(color="green")).add_to(mapa)

    #Se itera a través de cada CCT y pone las coordenadas de cada uno en una lista para procesar
    coordenadas = []
    for dict in microservice_data["result"]:
        end = (float(dict["longitud"]), float(dict["latitud"]))
        coordenadas.append(end)
    
    #Se obtienen las listas de cada ruta
    rutas_optimas = optimizar_ruta(coordenadas, start)
    colors = [
        'red',
        'blue',
        'orange',
        'purple',
        'pink',
        'gray',
        'beige',
        'black',
        'darkpurple',
        'darkblue',
        'darkgreen',
        'darkred',
        'cadetblue',
        'lightgreen',
        'lightgray',
        'lightblue',
        'lightred'
        ]
    for i in range(len(rutas_optimas)):
        for escala in rutas_optimas[i]:
            # Puntos de inicio y fin (lat, lon)
            start = [float(escala[0][0]), float(escala[0][1])]
            end = [float(escala[1][0]), float(escala[1][1])]
            for dict in microservice_data["result"]:
                if end[0] == float(dict["longitud"]) and end[1] == float(dict["latitud"]):
                    folium.Marker(location=end[::-1], 
                            popup=f"Nombre: {dict['nombre']}\nEstado: {dict['estado']}\nMunicipio: {dict['municipio']}\nComunidad: {dict['comunidad']}\nSede: {dict['sede']}\nRegión: {dict['region']}", 
                            icon=folium.Icon(color=colors[i])).add_to(mapa)

            # Llamar a la API de OSRM para calcular la ruta
            osrm_url = "http://router.project-osrm.org/route/v1/driving/"+str(start[0])+","+str(start[1])+";"+str(end[0])+","+str(end[1])+"?geometries=geojson"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
                "Accept-Encoding": "*",
                "Connection": "keep-alive"
            }
            route_coords = [start, end]
            ruta_exacta = 1
            try:
                response = requests.get(osrm_url, headers=headers).json()
                # Extraer las coordenadas de la ruta
                if 'routes' in response.keys():
                    route_coords = response['routes'][0]['geometry']['coordinates']
            except requests.RequestException as e:
                ruta_exacta = 0
            # Agregar ruta al mapa
            folium.PolyLine(
                    locations=[coord[::-1] for coord in route_coords],  # Invertimos [lon, lat] a [lat, lon]
                    color=colors[i],
                    weight=5,
                    opacity=0.8
                ).add_to(mapa)
            start = end

    # Guardar el mapa en HTML
    return Response(mapa._repr_html_(), content_type='text/html')

def dist_euclidiana(a, b):
    """Una funcion para definir la distancia entre cada nodo, el cual es necesario para la optimizacion."""
    return math.sqrt(pow(a[1] - b[1], 2) + pow(a[0] - b[0], 2))

def optimizar_ruta(ccts, centro):
    """
    Obtiene una serie de coordenadas por las que se tiene que pasar, un centro donde debe originar y terminar cada ruta.
    Primero crea grupos de cercania de cada punto y genera una ruta por cada uno, de ahi optimiza cada ruta y devuelve una lista conteniendo listas ordenadas de los puntos de cada ruta.
    """
    # Obtener la mejor cantidad de grupos.
    rutas_maximas = 10
    mejor = 0
    mejor_grupos = 1
    for i in range(2, min(len(ccts), rutas_maximas)):
        clustering = KMeans(n_clusters=i)
        clustering.fit(ccts)
        actual = silhouette_score(ccts, clustering.labels_, metric="euclidean")
        if actual > mejor:
            mejor = actual
            mejor_grupos = i

    # Obtener cada grupo y ponerlos en una lista.
    clustering = KMeans(n_clusters=mejor_grupos)
    clustering.fit(ccts)
    etiquetas = clustering.labels_
    coordenadas = []
    for i in range(mejor_grupos):
        temp = []
        temp.append(centro)
        for j in range(len(etiquetas)):
            if i == etiquetas[j]:
                temp.append(ccts[j])
        coordenadas.append(temp)
    
    # Optimizar una ruta por cada grupo.
    nodos_optimos = []
    for i in coordenadas:
        if len(i) > 2:
            grafo = pants.World(i, dist_euclidiana)
            solucionador = pants.Solver()
            solucion = solucionador.solve(grafo)
            camino = solucion.path
            tmp = []
            for j in camino:
                tmp.append([(j.start[0], j.start[1]), (j.end[0], j.end[1])])
            nodos_optimos.append(tmp)
    return nodos_optimos