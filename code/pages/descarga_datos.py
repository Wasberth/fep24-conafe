from flask import render_template, session, send_file
from decos import route, nav
import requests
import pandas as pd
import io


from mode_handler import get_url
from pages._check_level_ import restricted
from pages._card_ import Card, CONVOCATORIA_TEMPLATE, mapear_datos_convocatoria
from pages._error_ import ConafeException

CAPTACION_URL = get_url('captacion')
AUTENTICACION_URL = get_url('autenticacion')
ACEPTACION_URL = get_url('aceptacion')
CAPACITACION_URL = get_url('capacitacion')

@route('/informacion')
@nav('Información')
@restricted(['EC2', 'EC1'])
def informacion():
    """Renderiza los botones."""
    return render_template('informacion.html', stylesheets=['button'])

@route('/descargar_informacion')
def descargar_informacion():
    """Renderiza los botones."""
    # Obtener los datos del microservicio
    try:
        response = requests.post(CAPTACION_URL + '/buscar_integrante', json={'folio': session['folio']})
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        raise ConafeException(500, "Error comunicándose con el microservicio", str(e))
        
    microservice_data = microservice_data["result"]

    convocatorias = mapear_datos_convocatoria(microservice_data)

    df = pd.DataFrame(convocatorias)
    # Guardar el DataFrame en un objeto BytesIO
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Datos')
    output.seek(0)
    
    return send_file(
        output,
        as_attachment=True,
        download_name='información.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@route('/descargar_evaluaciones')
def descargar_evaluaciones():
    """Renderiza los botones."""
    try:
        response = requests.post(CAPACITACION_URL + '/get_evaluaciones', json={'folio': session['folio']})
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        microservice_data = response.json()  # Obtiene el JSON del microservicio
    except requests.RequestException as e:
        raise ConafeException(500, "Error comunicándose con el microservicio", str(e))
        
    microservice_data = microservice_data["result"]

    convocatorias = microservice_data

    df = pd.DataFrame(convocatorias)
    # Guardar el DataFrame en un objeto BytesIO
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Datos')
    output.seek(0)
    
    return send_file(
        output,
        as_attachment=True,
        download_name='evaluaciones.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )