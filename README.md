# Proyecto CONAFE: Sistema de Geolocalización y Gestión Educativa

## Descripción del Proyecto

Este proyecto es una propuesta tecnológica desarrollada para **CONAFE** (Consejo Nacional de Fomento Educativo), una institución mexicana enfocada en proporcionar servicios educativos a comunidades marginadas y rurales. La herramienta tiene como objetivo principal la **gestión eficiente de recursos, capacitación, y ubicación geográfica** de centros educativos y docentes, mejorando la distribución de equipo y la planificación estratégica.

## Funcionamiento del Proyecto

### Archivo `.env`

El proyecto requiere un archivo `.env` en la carpeta `/code` para almacenar las configuraciones esenciales. Este archivo debe contener las siguientes variables:

- **uri**: URL de conexión a la base de datos MongoDB.
- **secret_key**: Una clave secreta para el cifrado de Flask (puede ser un string básico).
- **dev**: Debe estar configurado como `true` para un funcionamiento adecuado, ya que no se ha implementado un sistema de producción.

Además, las siguientes variables deben especificar los puertos correspondientes a cada microservicio:

- **main_dev**: Puerto del servicio principal.
- **captacion_dev**: Puerto del microservicio de captación.
- **autenticacion_dev**: Puerto del microservicio de autenticación.
- **aceptacion_dev**: Puerto del microservicio de aceptación.
- **capacitacion_dev**: Puerto del microservicio de capacitación.
- **ubicacion_dev**: Puerto del microservicio de ubicación.

### Estructura de Archivos

La estructura del proyecto es la siguiente:

```
/
├── README.md
├── Documentación sobre el proyecto
├── Notas Documentos/
│ ├── Funcionamiento de la CONAFE y manuales
├── code/
│ ├── main.py
│ ├── execute_all.py
│ ├── .env
│ ├── pages/
│ │ ├── Archivos Python para renderizar plantillas HTML con Flask
│ ├── services/
│ │ ├── Microservicios independientes (se pueden ejecutar directamente)
│ ├── static/
│ │ ├── Archivos JS, CSS e imágenes estáticas
│ ├── templates/
│ ├── Plantillas HTML y JS para renderizado dinámico
├── BD/
│ ├── Bases de datos en formato JSON
```

#### Archivos Clave

- **`main.py`**: Ejecuta el servicio principal que recopila las páginas y gestiona la aplicación web.
- **`execute_all.py`**: Ejecuta todos los microservicios y el servicio principal simultáneamente. Este archivo debe usarse para ejecutar el sistema completo de manera local.
- **`BD`**: Contiene los datos de la base de datos en formato JSON. La estructura debe organizarse de la siguiente manera:
  - Cada carpeta representa una base de datos de MongoDB.
  - Cada archivo dentro de una carpeta representa una colección.
  - Algunos archivos tienen un `2` al final del nombre para indicar que pertenecen a una segunda base de datos, la cual está incompleta.

### Ejecución Local

1. Asegúrate de configurar el archivo `.env` en la carpeta `/code`.
2. Ejecuta `execute_all.py` desde la carpeta `/code` para iniciar todos los microservicios y el servicio principal.
3. Accede a la interfaz web a través del puerto configurado para **main_dev**.

## Licencia

Este proyecto está protegido por derechos de autor. Para más información, consulta los términos de uso en los documentos del proyecto.
