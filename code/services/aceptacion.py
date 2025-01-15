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
grupos =db.grupo

# Configurar conexión con login
db2 = client['login']
usuarios = db2.credenciales

db3 = client['CCT']
estados = db3.estados_republica

@app.route('/lista_convocatoria', methods=['GET'])
def get_convocatoria_list():
    """Obtiene la lista de la convocatoria."""
    data = request.get_json()
    estado = estados.find_one({"cot": data['cot_id']})
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

@app.route('/convenio/aceptar_bd', methods=['POST'])
def aceptar_convenio_bd():
    resultado = request.get_json()
    folio = resultado.get('folio')
    beneficiario = resultado.get('beneficiario')
    clave = resultado.get('clave')
    grado = resultado.get('grado')
    estado = resultado.get('estado')
    monto_apoyo_convenio = resultado.get('monto_apoyo_convenio')

    info_antes = grupos.find_one({'ec': folio})
    grado_antes = info_antes['grado']
    clave_antes = info_antes['cct']
    #Actualizar estado de convocatoria
    if estado == 'convenio':
        if grado != grado_antes or clave != clave_antes:
            dicc = {'preescolar1': '1', 'preescolar2': '2', 'preescolar3': '3', 'primaria': 'P', 'secundaria': 'S'}
            dicc2= {1:'A', 2:'B',3:'C', 4:'D',5:'E', 6:'F',7:'G', 8:'H',9:'I', 10:'J',11:'K', 12:'L',13:'M', 14:'N',15:'O', 16:'P',17:'Q', 18:'R',19:'S', 20:'T',21:'U', 22:'V',23:'X', 24:'Y',25:'Z'}
            grupos_cct = list(grupos.find({'cct': clave, 'grado': grado}))
            if len(grupos_cct) == 0:
                nuevo_grupo = f"{dicc[grado]}A"
                print("grupo len 0: ", nuevo_grupo)
                print(type(nuevo_grupo))
                grupos.update_one({'ec': folio}, {'$set': {'nombre': nuevo_grupo, 'grado': grado, 'cct': clave}})
            else:
                tam =len(grupos_cct) + 1
                nuevo_grupo = f"{dicc[grado]}{dicc2[tam]}"
                print("grupo len +: ", nuevo_grupo)
                print(type(nuevo_grupo))
                grupos.update_one({'ec': folio}, {'$set': {'nombre': nuevo_grupo, 'grado': grado, 'cct': clave}})
           
        convocatorias.update_one({'folio': folio}, {'$set': {'beneficiario': beneficiario, 'sede': clave, 'monto_apoyo_convenio': float(monto_apoyo_convenio), 'estado': estado, 'grado': grado, 'uniforme': False, 'firma': True}})
        
    if estado == 'apoyo':
        convocatorias.update_one({'folio': folio}, {'$set': {'beneficiario': beneficiario, 'sede': clave, 'monto_apoyo_convenio': float(monto_apoyo_convenio), 'estado': estado, 'grado': grado, 'uniforme': False, 'firma': True}})
        grupos.delete_one({'ec': folio})
    
    return jsonify({"msg": "Se ha actualizado con éxito!"})


@app.route('/convocatoria/rechazar_bd', methods=['POST'])
def rechazar_convocatoria_bd():
    resultado_convocatoria = request.get_json()
    _id = resultado_convocatoria.get('_id')
    
    #Actualizar estado de convocatoria
    convocatorias.update_one({'_id': ObjectId(_id)}, {'$set': {'estado':'rechazada'}})
    
    return jsonify({"_id": _id})

@app.route('/convocatoria/documentos_necesarios', methods=['GET'])
def documentos_necesarios():
    """Obtiene la lista de la convocatoria."""
    data = request.get_json()
    documento = convocatorias.find_one({"_id": ObjectId(data['_id'])})
    return jsonify({"doc":documento["documentos_necesarios"]})

@app.route('/aceptar_apoyo_bd', methods=['POST'])
def aceptar_apoyo_bd():
    data = request.get_json()
    folio = data["folio"]

    #Actualizar estado de apoyo
    convocatorias.update_one({'folio': folio}, {'$set': {'estado_apoyo': "aceptada"}})

    return jsonify({"msg": "Se ha actualizado con éxito!"})

@app.route('/rechazar_apoyo_bd', methods=['POST'])
def rechazar_apoyo_bd():
    data = request.get_json()
    folio = data["folio"]

    #Actualizar estado de apoyo
    convocatorias.update_one({'folio': folio}, {'$set': {'estado_apoyo': "rechazada"}})

    return jsonify({"msg": "Se ha actualizado con éxito!"})

@app.route('/apoyo/documentos_necesarios', methods=['GET'])
def apoyo_documentos_necesarios():
    """Obtiene los documento del apoyo."""
    data = request.get_json()
    documento = convocatorias.find_one({"folio": data["folio"]})
    return jsonify({"doc":documento["documentos_apoyo"]})


if __name__ == '__main__':
    from __args__ import parse_args
    args = parse_args()
    app.run(port=args.port, debug=args.debug)