from flask import render_template, request, redirect, url_for, session, jsonify
from decos import route
import requests
import json

from mode_handler import get_url

CAPACITACION_URL = get_url('capacitacion')

@route('/evaluacion/capacitacion')
def evaluacion_capacitacion():
    """Renderiza la página de evaluación al educador comunitario en capacitacion (EC1)"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if session['nivel'] != "COT":
        return redirect(url_for('test_page'))

    return render_template(
        f'eval_capacitacion.html',
        stylesheets=['success', 'button'],
        scripts=['addEvaluationEC1']
    )

@route('/evaluacion/servicio')
def evaluacion_capacitacion_servicio():
    """Renderiza la página de evaluación al educador comunitario en servicio (EC1)"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if session['nivel'] != "COT":
        return redirect(url_for('test_page'))

    return render_template(
        f'eval_servicio.html',
        stylesheets=['success', 'button'],
        scripts=['addEvaluationInServiceEC1']
    )

