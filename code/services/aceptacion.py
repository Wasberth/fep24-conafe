from flask import Flask, jsonify, request, make_response, render_template
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import bson
from bson.objectid import ObjectId
from bson.json_util import dumps
import os
from dotenv import load_dotenv

from __mongo_operations__ import objectid_to_str

load_dotenv()

app = Flask(__name__)

# Configurar la conexión a MongoDB
uri = os.environ['uri']
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['captacion']
convocatorias = db.formulario

# Configurar conexión con login
db2 = client['login']
usuarios = db2.credenciales

db3 = client['CCT']
estados = db3.estados_republica

@app.route('/lista_convocatoria', methods=['GET'])
def get_convocatoria_list():
    """Obtiene la lista de la convocatoria."""
    data = request.get_json()
    estado = estados.find_one({"COT": ObjectId(data['cot_id'])})
    print(estado)
    convocatorias_list = convocatorias.find({"estado":{"$exists": False}, "estado_republica": estado['estado']})
    return jsonify(objectid_to_str({"result":list(convocatorias_list)}))

@app.route('/convocatoria/aceptar_bd', methods=['POST'])
def aceptar_convocatoria_bd():
    resultado_convocatoria = request.get_json()
    usuario = resultado_convocatoria.get('usuario')
    
    #Actualizar estado de convocatoria
    convocatorias.update_one({'_id': ObjectId(usuario)}, {'$set': {'estado':'aceptada'}})

    #Agregar nuevo usuario
    insert_result = usuarios.insert_one(resultado_convocatoria)
    
    return jsonify({"id": str(insert_result.inserted_id)})

@app.route('/convocatoria/rechazar_bd', methods=['POST'])
def rechazar_convocatoria_bd():
    resultado_convocatoria = request.get_json()
    _id = resultado_convocatoria.get('_id')
    
    #Actualizar estado de convocatoria
    convocatorias.update_one({'_id': ObjectId(_id)}, {'$set': {'estado':'rechazada'}})
    
    return jsonify({"_id": _id})

    

if __name__ == '__main__':
    from __args__ import parse_args
    args = parse_args()
    app.run(port=args.port, debug=args.debug)