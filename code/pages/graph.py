from flask import Flask, render_template, jsonify
from datetime import datetime
from decos import route, nav
import requests
import pandas as pd
import plotly.express as px

from mode_handler import get_url
from pages._error_ import ConafeException
from pages._check_level_ import restricted

CAPTACION_URL = get_url('captacion')

@route('/tallas')
@restricted('AA')
@nav('Estadísticas convocatoria pasada')
def registro_tallas():
    """Renderiza una gráfica de registro de tallas."""
    current_year = datetime.now().year
    try:
        response = requests.post(CAPTACION_URL + '/tallas', json={'year': current_year})
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

    # Concatenar los resultados
    tallas_totales = pd.concat([tallas_playera, tallas_pantalon], ignore_index=True)

    # Crear la gráfica con Plotly Express
    fig1 = px.bar(
        tallas_totales,
        x='tipo',
        y='cantidad',
        color='talla',
        labels={'tipo': 'Tipo de Prenda', 'cantidad': 'Cantidad', 'talla': 'Talla'},
    )
    
    # Convertir la gráfica a JSON para enviar al frontend
    graph1_json = fig1.to_json()

    fig2 = px.bar(
        tallas_calzado,
        x='tipo',
        y='cantidad',
        color='talla',
        labels={'tipo': 'Tipo de Prenda', 'cantidad': 'Cantidad', 'talla': 'Talla'},
    )

    graph2_json = fig2.to_json()
    
    # Renderizar la plantilla HTML con la gráfica
    return render_template(
        'graph.html', graph1_json=graph1_json, graph2_json=graph2_json,
        playera_list=playera_list, pantalon_list=pantalon_list, calzado_list=calzado_list
    )