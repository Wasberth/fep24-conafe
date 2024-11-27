import os
import importlib.util
from flask import Flask
import inspect
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ['secret_key']

def load_pages_and_register_routes(app, pages_folder="pages"):
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

# Load modules and register routes
load_pages_and_register_routes(app)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
