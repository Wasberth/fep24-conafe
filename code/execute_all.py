import os
import subprocess
from dotenv import load_dotenv

from main import app

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def load_services():
    """
    Carga todos los archivos Python de la carpeta "services" y abre nuevos procesos CMD
    para hostear las aplicaciones Flask con debug=True si corresponde.
    """
    # Directorio de servicios
    services_dir = "services"

    if not os.path.isdir(services_dir):
        print(f"El directorio {services_dir} no existe.")
        return

    # Iterar sobre los archivos en la carpeta "services"
    for filename in os.listdir(services_dir):
        if filename.endswith(".py"):
            service_name = filename[:-3]  # Nombre del archivo sin la extensión .py

            # Buscar en el .env la variable "<filename>_dev"
            port = os.getenv(f"{service_name}_dev")
            if port:
                try:
                    port = int(port)

                    # Comando para ejecutar el servicio en un nuevo proceso CMD
                    service_path = os.path.join(services_dir, filename)
                    command = [
                        "python", service_path,
                        "--port", str(port),
                        "--debug"
                    ]

                    subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)
                    print(f"Servicio {service_name} iniciado en el puerto {port} con debug=True en una nueva ventana CMD.")

                except ValueError:
                    print(f"El valor de {service_name}_dev debe ser un número entero representando el puerto.")
                except Exception as e:
                    print(f"Error al cargar el servicio {service_name}: {e}")

def run_main():
    """
    Ejecuta el main que incluye todas las páginas web
    """
    port = int(os.getenv(f"main_dev"))
    app.run(debug=True, port=int(port))

if __name__ == "__main__":
    from mode_handler import is_dev_mode

    if is_dev_mode():
        print("Modo desarrollo activado.")
        load_services()
        run_main()
    else:
        print("Modo desarrollo desactivado.")