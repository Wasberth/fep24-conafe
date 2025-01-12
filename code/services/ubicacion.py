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
    keys = data['claves']
    query = {'clave':{'$in':keys}}

    result = lugares.find(query)
    return jsonify(objectid_to_str({'result':list(result)}))

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
        print("Probando " + inicio['clave'])
        for final in algoiterable:
            if inicio['clave'] == final['clave'] or final['clave'] in revisados:
                continue
            print("con " + str(final['clave']))
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
    actualizar = len(list(rutas.find(query))) > 0
    insert_result = ""
    if actualizar:
        for i in poli:
            query = {'estado': estado, 'puntos': i['puntos']}
            operacion = {'$set':{'polilinea':i['polilinea']}}
            insert_result = rutas.update_one(query, operacion)
    else:
        insert_result = rutas.insert_many(poli)
    return jsonify({"state":str(insert_result)})

if __name__ == '__main__':
    from __args__ import parse_args
    args = parse_args()
    app.run(port=args.port, debug=args.debug)