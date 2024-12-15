import argparse

def parse_args():
    """Parsea los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(description="Iniciar el microservicio Flask.")
    parser.add_argument("--port", type=int, default=5003, help="El puerto en el que se ejecutará el servidor.")
    parser.add_argument("--debug", action="store_true", help="Habilitar el modo de depuración.")
    return parser.parse_args()