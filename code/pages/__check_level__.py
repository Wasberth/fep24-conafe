from flask import redirect, url_for, session

def check_level(level):
    """
    Verifica que el nivel sea el correcto, de lo contrario, lo redirige a una página compartida
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if session['nivel'] != "level":
        # TODO: Diseñar una página que tenga los vínculos únicos de cada usuario
        return redirect(url_for('test_page'))