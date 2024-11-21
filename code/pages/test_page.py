from flask import Flask, render_template, jsonify
from datetime import datetime
from decos import route

@route('/test')
def test_page():
    """Renderiza la página principal"""
    return render_template(f'success.html', stylesheets=['success', 'button'])