from flask import Flask, render_template, jsonify
from datetime import datetime
from decos import route

@route('/')
def index_page():
    """Renderiza la página principal"""
    return render_template(f'index.html', stylesheets=['index', 'button'])