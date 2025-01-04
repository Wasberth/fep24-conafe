from flask import render_template, request, session, make_response
from decos import route, nav
import requests

from mode_handler import get_url
from pages._check_level_ import restricted
from pages._error_ import ConafeException

CAPTACION_URL = get_url('captacion')
UBICACION_URL = get_url('ubicacion')

@route('/carga_archivo')
@nav('Carga de archivo')
@restricted(['EC1', 'EC2', 'ECA'])
def json_loader():
    return render_template(
        f'carga_archivo.html',
        stylesheets=['dropZone'],
        scripts=['jsonLoader'],
    )