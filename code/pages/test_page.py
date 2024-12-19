from flask import Flask, render_template, jsonify, session
from datetime import datetime
from decos import route

@route('/test')
def test_page():
    """Renderiza la página principal"""
    return render_template(f'test.html')

@route('/check_my_level')
def level_page():
    """Imprime el nivel que tiene guardado en session"""
    return render_template(f'test.html', echo=session['nivel'])