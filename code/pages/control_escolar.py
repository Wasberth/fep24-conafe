from flask import render_template
from decos import route, nav

from pages._check_level_ import restricted

@route('/alumno/alta')
@nav('Control Escolar/Altas')
@restricted(['EC2', 'ECA'])
def alta_alumno():
    return render_template(
        f'alta_alumno.html',
        stylesheets=['button'],
        scripts=['addStudent']
    )