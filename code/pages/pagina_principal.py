from flask import Flask, render_template, url_for, session, redirect
from datetime import datetime
from decos import route

@route('/')
def index_page():
    """Renderiza la página principal"""
    if session and session.get('nivel', False):
        return redirect(url_for('wellcome'))

    return render_template(f'index.html', stylesheets=['index', 'button'])