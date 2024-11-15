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
	Create a new user in the system.
	:param str username: The username for the new user.
	:param str password: The password for the new user.
	:returns: A confirmation message indicating the success of user creation.
	:rtype: str
	"""
	
	pass
```