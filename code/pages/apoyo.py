from flask import render_template
from decos import route, nav

from pages._check_level_ import restricted

@route('/apoyo')
@nav('Apoyo/Solicitud')
@restricted(['EC1', 'EC2', 'ECA'])
def apoyo_estudios():
    return render_template(f'apoyo.html', stylesheets=['button'])