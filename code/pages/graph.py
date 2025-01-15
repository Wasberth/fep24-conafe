from flask import Flask, render_template, jsonify
from datetime import datetime
from decos import route, nav
import requests
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

from mode_handler import get_url
from pages._error_ import ConafeException
from pages._check_level_ import restricted


CAPTACION_URL = get_url('captacion')

@route('/tallas')
@restricted('AA')
@nav('Estadísticas convocatoria pasada')
def registro_tallas():
    """Renderiza una gráfica de registro de tallas."""
    current_year = datetime.now().year - 1
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
        'graph.html', graphs=[graph1_json, graph2_json],
        playera_list=playera_list, pantalon_list=pantalon_list, calzado_list=calzado_list
    )

@route('/historico_tallas')
@restricted('AA')
@nav('Estadísticas históricas')
def registro_tallas_historico():
    """Realiza una regresión lineal para predecir el número de tallas en un año futuro y genera gráficos interactivos."""
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import LabelEncoder
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    from datetime import datetime
    import requests

    current_year = datetime.now().year

    try:
        response = requests.post(CAPTACION_URL + '/historico_tallas', json={'years': [current_year - i for i in range(1, 6)]})
        response.raise_for_status()
        microservice_data = response.json()
    except requests.RequestException as e:
        raise ConafeException(500, "Error comunicándose con el microservicio", str(e))

    # Convertir los datos a un DataFrame de Pandas
    df = pd.DataFrame(microservice_data['result'])

    # Validar que las columnas necesarias existan
    required_columns = {'playera', 'pantalon', 'calzado', 'convocatoria'}
    if not required_columns.issubset(df.columns):
        raise ConafeException(500, "Faltan columnas necesarias en los datos del microservicio")

    # Rellenar años faltantes con conteos de 0
    years = list(range(current_year - 5, current_year))  # Últimos 5 años
    conteos = []
    prendas = ['playera', 'pantalon', 'calzado']
    graphs = []
    label_encoders = {}

    prediccion = {}

    for prenda in prendas:
        # Codificar tallas categóricas a valores numéricos
        le = LabelEncoder()
        df[prenda] = le.fit_transform(df[prenda].astype(str))
        print(df[prenda])
        label_encoders[prenda] = le
        print(le.classes_)

        # Contar las tallas por año y rellenar años faltantes
        conteo = df.groupby(['convocatoria', prenda]).size().reset_index(name='cantidad')
        tallas_completas = pd.DataFrame([(year, talla) for year in years for talla in range(len(le.classes_))], columns=['convocatoria', prenda])
        print(tallas_completas)
        conteo = pd.merge(tallas_completas, conteo, on=['convocatoria', prenda], how='left').fillna(0)
        conteo['cantidad'] = conteo['cantidad'].astype(int)
        conteo['tipo'] = prenda.capitalize()
        conteos.append(conteo)

        print(conteo)

        fig = go.Figure()

        # Hacer las regresiones lineales por cada talla
        for talla in conteo[prenda].unique():
            # Seleccionar datos para la talla actual
            conteo_talla = conteo[conteo[prenda] == talla]

            X = conteo_talla['convocatoria'].values.reshape(-1, 1)
            y = conteo_talla['cantidad'].values

            # Crear y entrenar el modelo de regresión lineal
            model = LinearRegression()
            model.fit(X, y)

            # Obtener el texto de la talla
            talla_text = le.inverse_transform([talla])[0].upper()

            # Generar predicciones
            predicted_y = model.predict(X)
            next_year = model.predict(np.array([current_year]).reshape(-1, 1))

            # Agregar la prediccion del sig año
            if prenda not in prediccion.keys():
                prediccion[prenda] = []

            prediccion[prenda].append((talla_text, round(next_year[0])))

            # Agregar la línea de regresión
            fig.add_trace(go.Scatter(
                x=conteo_talla['convocatoria'],
                y=predicted_y,
                mode='lines',
                name=f'Regresión {prenda.capitalize()} {talla_text}'
            ))

            # Agregar los puntos reales
            fig.add_trace(go.Scatter(
                x=conteo_talla['convocatoria'],
                y=y,
                mode='markers',
                name=f'Datos reales {prenda.capitalize()} {talla_text}'
            ))

        # Configurar diseño de la gráfica
        fig.update_layout(
            title=f'Regresión Lineal: {prenda.capitalize()}',
            xaxis_title='Año de Convocatoria',
            yaxis_title='Cantidad de Solicitudes',
            template='plotly_white'
        )

        # Convertir la gráfica a JSON
        graphs.append(fig.to_json())

        print("=================================")

    # Concatenar los resultados de las tallas
    tallas_totales = pd.concat(conteos, ignore_index=True)

    # Revertir tallas codificadas a categóricas
    for prenda in prendas:
        tallas_totales.loc[tallas_totales['tipo'] == prenda.capitalize(), 'talla'] = label_encoders[prenda].inverse_transform(
            tallas_totales.loc[tallas_totales['tipo'] == prenda.capitalize(), prenda].astype(int)
        )

    # Crear una gráfica de barras para las tallas totales
    fig_barras = px.bar(
        tallas_totales,
        x='tipo',
        y='cantidad',
        color='talla',
        labels={'tipo': 'Tipo de Prenda', 'cantidad': 'Cantidad', 'talla': 'Talla'},
        title='Cantidad de Tallas por Tipo de Prenda'
    )

    # Convertir la gráfica de barras a JSON
    graph_barras_json = fig_barras.to_json()
    graphs.append(graph_barras_json)

    # Retornar el resultado al frontend
    return render_template(
        'graph.html',
        graphs=graphs,
        playera_list=prediccion['playera'],
        pantalon_list=prediccion['pantalon'],
        calzado_list=prediccion['calzado']
    )