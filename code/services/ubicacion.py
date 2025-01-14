from flask import Flask, jsonify, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from __mongo_operations__ import objectid_to_str
import bson
import os
from dotenv import load_dotenv
import requests
load_dotenv()

app = Flask(__name__)

uri = os.environ['uri']
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['CCT']

lugares = db['cct']
estados = db['estados_republica']
rutas = db['rutas']
delegaciones_estatales = db['delegaciones_estatales']

@app.route('/lista_lugares', methods=['GET']) 
def get_lugares():
    """Obtiene la lista de CCT."""
    # Checar si se envió un estado
    data = request.get_json(silent=True)
    query = {}
    if data is not None and 'estado' in data:
        query = {"estado": data['estado']}

    lugares_list = lugares.find(query)
    return jsonify(objectid_to_str({"result":list(lugares_list)}))

@app.route('/lista_lugares_estado', methods=['GET']) 
def get_lugares_estado():
    """Obtiene la lista de CCT por estado."""
    data = request.get_json()['estado']
    lugares_list = lugares.find({"estado": data})
    return jsonify(objectid_to_str({"result":list(lugares_list)}))

@app.route('/cot_estado', methods=['GET']) 
def get_estado_por_folio():
    """Obtiene el estado del COT"""
    data = request.get_json()['cot']
    estado = estados.find({"cot": data})
    return jsonify(objectid_to_str({"result":list(estado)}))

@app.route('/get_coordenadas', methods=['POST'])
def get_coordenadas():
    """Obtiene las coordenadas de los CCT's con respecto a su clave"""
    data = request.get_json()
    estado = data['estado']

    query = {'estado':estado}
    result = lugares.find(query)

    query = {'estado': estado}
    resulta2 = delegaciones_estatales.find_one(query)
    
    resulta4 = rutas.find(query)

    query = {'estado': "CIUDAD DE MEXICO"}
    resulta3 = delegaciones_estatales.find_one(query)

    return jsonify(objectid_to_str({'result':list(result), 'delegacion':resulta2, 'central': resulta3, 'rutas': list(resulta4)}))

@app.route('/generar_rutas', methods=['POST'])
def generar_rutas():
    """Genear las polilineas que representan las rutas entre todos los CCT's de un estado"""
    data = request.get_json()
    estado = str(data['estado']).upper()
    query = {'estado': estado}

    result = lugares.find(query)
    algoiterable = []
    for doc in result:
        algoiterable.append(doc)
    if len(algoiterable) == 0:
        return jsonify({"error": "No hay ccts en ese estado"})
    result = delegaciones_estatales.find(query)
    for doc in result:
        doc['clave'] = "DELDES"
        algoiterable.append(doc)
    poli = []
    revisados = []
    for inicio in algoiterable:
        for final in algoiterable:
            if inicio['clave'] == final['clave'] or final['clave'] in revisados:
                continue
            route_coords = [[inicio['longitud'], inicio['latitud']], [final['longitud'], final['latitud']]]
            ruta_exacta = 1
            try:
                osrm_url = "http://router.project-osrm.org/route/v1/driving/"+str(inicio['longitud'])+","+str(inicio['latitud'])+";"+str(final['longitud'])+","+str(final['latitud'])+"?geometries=geojson"
                response = requests.get(osrm_url).json()
                # Extraer las coordenadas de la ruta
                if 'routes' in response.keys():
                    route_coords = response['routes'][0]['geometry']['coordinates']
            except requests.RequestException as e:
                ruta_exacta = 0
            id = str(inicio['longitud'])+","+str(inicio['latitud'])+"/"+str(final['longitud'])+","+str(final['latitud'])
            temp = {}
            temp['puntos'] = id
            temp['polilinea'] = route_coords
            temp['estado'] = estado
            poli.append(temp)
        revisados.append(inicio['clave'])
    borrar = len(list(rutas.find(query))) > 0
    insert_result = ""
    if borrar:
        query = {'estado': estado}
        delete_result = rutas.delete_many(query)
    insert_result = rutas.insert_many(poli)
    return jsonify({"state":str(insert_result)})

@app.route('/script_dev', methods=['POST'])
def script_dev():
    """Genear las polilineas que representan las rutas entre todos los CCT's de un estado"""
    data = request.get_json()
    estado = str(data['estado']).upper()
    algoiterable = []
    result = delegaciones_estatales.find()
    centro = {}
    for doc in result:
        if doc['estado'] == "CIUDAD DE MEXICO":
            centro = doc
        else:
            algoiterable.append(doc)
    if len(algoiterable) == 0:
        return jsonify({"error": "No hay ccts en ese estado"})
    poli = []
    for inicio in algoiterable:
        route_coords = [[inicio['longitud'], inicio['latitud']], [centro['longitud'], centro['latitud']]]
        ruta_exacta = 1
        try:
            osrm_url = "http://router.project-osrm.org/route/v1/driving/"+str(inicio['longitud'])+","+str(inicio['latitud'])+";"+str(centro['longitud'])+","+str(centro['latitud'])+"?geometries=geojson"
            response = requests.get(osrm_url).json()
            # Extraer las coordenadas de la ruta
            if 'routes' in response.keys():
                route_coords = response['routes'][0]['geometry']['coordinates']
        except requests.RequestException as e:
            ruta_exacta = 0
        id = str(inicio['longitud'])+","+str(inicio['latitud'])+"/"+str(centro['longitud'])+","+str(centro['latitud'])
        temp = {}
        temp['puntos'] = id
        temp['polilinea'] = route_coords
        temp['estado'] = inicio['estado']
        temp['central'] = True
        poli.append(temp)
    query = {'central': True}
    borrar = len(list(rutas.find(query))) > 0
    insert_result = ""
    if borrar:
        query = {'estado': estado}
        delete_result = rutas.delete_many(query)
    insert_result = rutas.insert_many(poli)
    return jsonify({"state":str(insert_result)})

if __name__ == '__main__':
    from __args__ import parse_args
    args = parse_args()
    app.run(port=args.port, debug=args.debug)