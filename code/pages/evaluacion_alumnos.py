from flask import render_template, request, redirect, url_for, session, jsonify, make_response
from decos import route, nav
import requests
import json

from mode_handler import get_url
from pages._check_level_ import restricted

@route('/evaluacion/alumnos')
@nav('Control Escolar/Calificar')
@restricted('ECA')
def evaluacion_alumnos():
    """Renderiza la página de evaluación de los alumnos"""
    return render_template(
        f'eval_alumnos.html',
        stylesheets=['success', 'button', 'verticalText'],
        scripts=['addEvaluationStudent']
    )