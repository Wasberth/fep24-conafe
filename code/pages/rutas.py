from flask import render_template, request, redirect, url_for, session, jsonify, Response
from decos import route, nav
from mongo_objects._common_types_ import Estado_republica
import requests
import folium
import folium.plugins
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from mode_handler import get_url
from pages._check_level_ import restricted
from datetime import datetime
import pandas as pd
from pages._error_ import ConafeException
import json
import math
import pants
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

MAPA_URL = get_url('ubicacion')
CAPTACION_URL = get_url('captacion')
polilineas = []

@route("/generador_ruta")
@restricted('AA')
@nav('Generador de rutas')
def generacion_ruta():
    """Renderiza la pagina y formulario para generar rutas de distribucion."""
    return render_template('ruta.html', stylesheets=['index', 'route_loader'], scripts=['route_loader'])

@route('/actualizar_formulario', methods=["POST"])
def actualizar_formulario():
    """Entrega el inventario necesario para un estado"""
    # Quiero asumir que los faltantes son los del siguiente año, hay que poner mas registros cuando se pueda
    # Arreglen si es un entero o string pofavo
    current_year = "2024"
    estado = request.get_data().decode()
    try:
        response = requests.post(CAPTACION_URL + '/tallas_repartibles', json={'year': current_year, 'estado': estado})
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        raise ConafeException(500, "Error comunicándose con el microservicio", str(e))
    
    # Convertir los datos a un DataFrame de Pandas
    df = pd.DataFrame(microservice_data['result'])
    
    # Validar que las columnas necesarias existan
    required_columns = {'playera', 'pantalon', 'calzado'}
    if not required_columns.issubset(df.columns):
        return json.dumps({"error": "No hay registros para ese estado"})
    
    retorno = {}

    # Contar las repeticiones de cada talla por tipo de prenda
    tallas_playera = df['playera'].value_counts().reset_index()
    tallas_playera.columns = ['talla', 'cantidad']
    tallas_playera['tipo'] = 'Playera'

    retorno['playera'] = tallas_playera.values.tolist()

    tallas_pantalon = df['pantalon'].value_counts().reset_index()
    tallas_pantalon.columns = ['talla', 'cantidad']
    tallas_pantalon['tipo'] = 'Pantalón'

    retorno['pantalon'] = tallas_pantalon.values.tolist()

    tallas_calzado = df['calzado'].value_counts().reset_index()
    tallas_calzado.columns = ['talla', 'cantidad']
    tallas_calzado['tipo'] = 'Calzado'

    retorno['calzado'] = tallas_calzado.values.tolist()
    return json.dumps(retorno)

@route('/reobtener_polilineas', methods=['POST'])
def reobtener_polilineas():
    estado = request.get_data().decode()
    try:
        response = requests.post(MAPA_URL + '/generar_rutas', json={'estado': estado})
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        raise ConafeException(500, "Error comunicándose con el microservicio", str(e))
    if "error" in microservice_data.keys():
        return json.dumps({'error': microservice_data['error']})
    return json.dumps({'resultado': "Correcto"})

@route('/mapa_ruta')
def mapa_ruta():
    """Obtiene la lista de CCT's, los agrupa en rutas y genera una ruta optima para la distribucion."""
    # Obtener los datos del microservicio
    formulario = json.loads(request.args.get('data'))
    estado = request.args.get('estado')
    request_data = {'estado': estado}
    try:
        response = requests.post(MAPA_URL + '/get_coordenadas', json=request_data)
        response.raise_for_status() # Lanza una excepción si ocurre un error HTTP
        microservice_data_map = response.json() # Obtiene el JSON del microservicio
        claves = []
        for doc in microservice_data_map['result']:
            claves.append(doc['clave'])
        request_data = {'claves': claves, 'tallas': formulario}
        response = requests.post(CAPTACION_URL + '/get_distribucion', json=request_data)
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data_cap = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        return jsonify({"error": "Error comunicándose con el microservicio", "details": str(e)}), 500
    
    # Central de abastos
    cdmx = (microservice_data_map['central']['longitud'], microservice_data_map['central']['latitud'])
    central = (microservice_data_map['delegacion']['longitud'], microservice_data_map['delegacion']['latitud'])
    # Crear un mapa centrado en el punto inicial y se agrega la central de abastos
    mapa = folium.Map(location=cdmx[::-1], zoom_start=5)
    folium.Marker(location=cdmx[::-1], popup="Ciudad de México\nDirección: "+str(microservice_data_map['central']['direccion']), icon=folium.Icon(color="green")).add_to(mapa)
    folium.Marker(location=central[::-1], popup="Delegacion de "+str(microservice_data_map['delegacion']['estado'])+"\nDirección: "+str(microservice_data_map['delegacion']['direccion']), icon=folium.Icon(color="green")).add_to(mapa)

    #Se itera a través de cada CCT y pone las coordenadas de cada uno en una lista para procesar
    coordenadas = []
    datos_ccts = []
    for dict in microservice_data_map["result"]:
        if dict['clave'] in microservice_data_cap['claves']:
            end = (float(dict["longitud"]), float(dict["latitud"]))
            coordenadas.append(end)
            datos_ccts.append(dict)
    
    #Se genera un diccionario con las rutas entre cada CCT
    poli = {}
    for dict in microservice_data_map['rutas']:
        poli[dict['puntos']] = dict['polilinea']

    #Poner la ruta de CDMX a la central de abastos
    llave = str(central[0])+","+str(central[1])+"/"+str(cdmx[0])+","+str(cdmx[1])
    route_coords = poli[llave]
    folium.PolyLine(
            locations=[coord[::-1] for coord in route_coords],  # Invertimos [lon, lat] a [lat, lon]
            color="green",
            weight=5,
            opacity=0.8
        ).add_to(mapa)

    #Se obtienen las listas de cada ruta
    rutas_optimas = optimizar_ruta(coordenadas, central, poli)
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
            for dict in datos_ccts:
                if end[0] == float(dict["longitud"]) and end[1] == float(dict["latitud"]):
                    folium.Marker(location=end[::-1], 
                            popup=f"Nombre: {dict['nombre']}\nEstado: {dict['estado']}\nMunicipio: {dict['municipio']}\nComunidad: {dict['comunidad']}\nSede: {dict['sede']}\nRegión: {dict['region']}", 
                            icon=folium.Icon(color=colors[i])).add_to(mapa)

            llave = str(start[0])+","+str(start[1])+"/"+str(end[0])+","+str(end[1])
            if llave not in poli.keys():
                llave = str(end[0])+","+str(end[1])+"/"+str(start[0])+","+str(start[1])
            route_coords = poli[llave]
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

def sum_dists(a, b, poli):
    llave = str(a[0])+","+str(a[1])+"/"+str(b[0])+","+str(b[1])
    if llave not in poli.keys():
        llave = str(b[0])+","+str(b[1])+"/"+str(a[0])+","+str(a[1])
    sum = 0
    usando = poli[llave]
    for i in range(len(usando)-1):
        sum = sum + dist_euclidiana(usando[i], usando[i+1])
    return sum

def optimizar_ruta(ccts, centro, poli):
    """
    Obtiene una serie de coordenadas por las que se tiene que pasar, un centro donde debe originar y terminar cada ruta.
    Primero crea grupos de cercania de cada punto y genera una ruta por cada uno, de ahi optimiza cada ruta y devuelve una lista conteniendo listas ordenadas de los puntos de cada ruta.
    """
    # Obtener la mejor cantidad de grupos.
    coordenadas = []
    ccts_minimos = 20
    if ccts_minimos > len(ccts):
        ccts.append(centro)
        coordenadas.append(ccts)
    else:
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
            for m in grafo.nodes:
                for n in grafo.nodes:
                    a, b = grafo.data(m), grafo.data(n)
                    if a != b:
                        grafo.edges[m, n].length = sum_dists(a,b, poli)
            solucionador = pants.Solver()
            solucion = solucionador.solve(grafo)
            camino = solucion.path
            tmp = []
            for j in camino:
                tmp.append([(j.start[0], j.start[1]), (j.end[0], j.end[1])])
            nodos_optimos.append(tmp)
    return nodos_optimos