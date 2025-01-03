import os
import importlib.util
from flask import Flask, render_template
import inspect
from dotenv import load_dotenv
from pages._error_ import ConafeException
from werkzeug.exceptions import HTTPException
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ['secret_key']

nav_items = {}

def load_pages_and_register_routes(app: Flask, pages_folder: str = "pages"):
    """Carga las páginas de forma dinámica de la carpeta pages."""
    modules_path = os.path.join(os.path.dirname(__file__), pages_folder)
    
    for filename in os.listdir(modules_path):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]
            module_path = os.path.join(modules_path, filename)
            
            # Cargar páginas de forma dinámica
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Registrar páginas decoradas
            for attr_name in dir(module):
                if attr_name.startswith('__'):
                    continue

                attr = getattr(module, attr_name)
                if not inspect.isfunction(attr):
                    continue

                if hasattr(attr, "route") and hasattr(attr, "methods"):
                    app.route(attr.route, methods=attr.methods)(attr)
                
                access = ['public']
                if hasattr(attr, "restricted"):
                    access = attr.restricted

                if hasattr(attr, "nav"):
                    for person in access:
                        if person not in nav_items:
                            nav_items[person] = []
                        nav_items[person].append({'text': attr.nav, 'url': attr.route})

@app.route('/error')
def error():
    raise ConafeException(500, m="Error de prueba")

@app.context_processor
def inject_nav_items():
    """Inyecta los items de navegación en el contexto de Jinja."""
    return dict(nav_items=nav_items)

@app.errorhandler(Exception)
def page_not_found(e):
    if isinstance(e, ConafeException):
        return e.response()
    
    if isinstance(e, HTTPException):
        return render_template('error.html', description=str(e), code=e.code), e.code
    
    return render_template('error.html', description=str(e), code=500), 500

# Load modules and register routes
load_pages_and_register_routes(app)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
