from flask import Flask, render_template, jsonify
from datetime import datetime
from decos import route

@route('/registro_concluido')
def registro_concluido_page():
    """Renderiza la página principal"""
    return render_template(f'success.html', stylesheets=['success', 'button'])