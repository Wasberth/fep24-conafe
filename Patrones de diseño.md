## Gateway API
Los microservicios se van a través de un orquestrador que será el que le pide a cada microservicio los datos. La comunicación se hará a través de archivos JSON

## Database per Service
Cada microservicio debe tener una única base de datos, y no se deben comunicar los microservicios con bases de datos que no les pertenece. Cualquier comunicación necesaria se hará en el orquestrador

## Formato del código
Para asegurar la mantenibilidad del código, el mismo debe tener las siguientes características:
- **Nombres de Variables:** Los nombres de variables deben ser significativos y en snake_case, en caso que no sea entendible, se agrega un comentario antes del primer uso de la variable donde explique el significado / uso de la variable
- **Documentación con docstrings:** Las funciones, clases y métodos deben contener un docstring de documentación en formato reStructuredTex. Ejemplo:

```python
def create_user(username, password):
	"""
	Crear un nuevo usuario en el sistema.
	:param str username: El nombre del usuario.
	:param str password: La contraseña del usuario.
	:returns: Un mensaje de confirmación de éxito o fallo
	:rtype: str
	"""
	
	pass
```

## Estructura de archivos
Para asegurar que todos los archivos se mantengan en orden y no haya problemas de administración, se deben seguir las siguientes pautas para la ubicación de los archivos:
- Todo lo que tenga que ver con la parte web, se debe incluir en la carpeta public, además, los archivos js, css e imágenes deben estar en las carpetas public/js, public/css y public/img respectivamente
- Todos los microservicios deben estar en un archivo propio de python en la carpeta services. Cada uno debe exponer la variable app correspondiente a su servicio a ofrecer ya configurado
- Cualquier función del orquestrador debe estar en un archivo correspondiente a su categoría en la carpeta modules que después se importará en el archivo index.py. Además, cada función que requiera un acceso por petición (get o post), se necesita decorar con el decorador de @route. Ejemplo:

```python
@route("/module1/hello", methods=["GET"])
def hello_world():
	"""Example route returning a simple JSON response."""
	return jsonify({"message": "Hello from Module 1"})
```
- 