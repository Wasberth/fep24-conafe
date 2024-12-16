from flask import render_template, request, redirect, url_for, session, jsonify
from decos import route
import requests
import json

from mode_handler import get_url

CAPACITACION_URL = get_url('capacitacion')

@route('/evaluacion/capacitacion')
def evaluacion_capacitacion():
    """Renderiza la página de evaluación al educador comunitario en capacitacion (EC1)"""
    return render_template(
        f'eval_capacitacion.html',
        stylesheets=['success', 'button'],
        scripts=['addEvaluationEC1']
    )