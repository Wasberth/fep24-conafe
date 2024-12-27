from flask import Flask, render_template, jsonify, session
from datetime import datetime
from decos import route

from pages._card_ import *

@route('/test')
def test_page():
    """Renderiza la página principal"""
    return render_template(f'test.html')

@route('/check_my_level')
def level_page():
    """Imprime el nivel que tiene guardado en session"""
    return render_template(f'test.html', echo=session['nivel'])

@route('/test_card')
def test_card():
    datos = {
        "_id": {
            "$oid": "676df8fb2bfa6512bee1c75d"
        },
        "curp": "3",
        "nombre": "Billy",
        "apellido": "Lennon",
        "direccion": "uk",
        "num-exterior": "1",
        "num-interior": "",
        "codigo-postal": "2",
        "fecha_nacimiento": "2000-11-11",
        "genero": "masculino",
        "nacionalidad": "mexicano",
        "playera": "c",
        "pantalon": "c",
        "calzado": "26.5",
        "banco": "Banca Afirme",
        "cuenta_bancaria": "",
        "clabe": "",
        "email": "example@hotmail.com",
        "telefono_fijo": "",
        "telefono_movil": "",
        "nivel_educativo": "superior",
        "situacion_educativa": "trunca",
        "lengua": "false"
    }
    
    return render_template('cartas.html', cards=[Card.card_from_dict(CONVOCATORIA_TEMPLATE, **datos).my_dict()])