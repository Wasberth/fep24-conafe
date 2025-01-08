##### **Historia de usuario 1: Panel de control de gráficas**

| Criterios/Fecha                                                                                   |     |
| ------------------------------------------------------------------------------------------------- | --- |
| Cuando el usuario da clic en la pestaña "panel de control", se le despliegan las gráficas         |     |
| Cuando el usuario ingresa la url manualmente, accede únicamente si ha iniciado la sesión como DPE |     |
|                                                                                                   |     |
##### **Historia de usuario 2: Llenado de convocatoria**

| Criterios/Fecha                                                                       | 21/11/2024 | 23/11/2024 | 30/12/2024 |
| ------------------------------------------------------------------------------------- | :--------: | ---------- | ---------- |
| El usuario ingresa los datos de campos obligatorios y sube el formulario sin problema |     x      | x          | x          |
| Si el usuario no ingresó un dato en un campo obligatorio, no permite subir los datos  |     x      | x          | x          |
| El usuario debe haber ingresado una CURP válida para poder subir los datos            |            |            | x          |
##### **Historia de usuario 3: Revisión de solicitudes**

| Criterios/Fecha                                                                                                                                                   | 21/11/2024 | 23/11/2024 | 16/12/2024 |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------: | :--------: | :--------: |
| Cuando el usuario le da clic al botón "revisar solicitudes", se despliega la lista de solicitudes.                                                                |            |            |     x      |
| Cuando el usuario le da clic al botón de "aceptar", la solicitud correspondiente es aceptada y se agrega "estado: aceptada" en su registro de la base de datos    |            |            |     x      |
| Cuando el usuario le da clic al botón de "rechazar", la solicitud correspondiente es rechazada y se agrega "estado: rechazada" en su registro de la base de datos |            |            |     x      |
| Cuando el usuario ingresa la url manualmente, accede únicamente si ha iniciado la sesión como COT                                                                 |     x      |     x      |     x      |
##### **Historia de usuario 4: Llenado de formulario para evaluación de figuras docentes**

| Criterios/Fecha                                                                                               | 15/12/2024 | 16/12/2024 |
| ------------------------------------------------------------------------------------------------------------- | ---------- | ---------- |
| Cuando el usuario le da clic al boton "Evaluar figuras docentes en capacitación", se le muestra el formulario |            | x          |
| El formulario sigue el formato que se especifica en el documento 6.1                                          | x          | x          |
| El formulario puede ser descargado cuando se está fuera de línea y cargado posteriormente.                    | x          | x          |
| Cuando el usuario ingresa la url manualmente, accede únicamente si ha iniciado la sesión como ECA             | x          | x          |
##### **Historia de usuario 5: Llenado de formulario para evaluación de figuras docentes**

| Criterios/Fecha                                                                                           | 23/11/2024 | 17/12/2024 |
| --------------------------------------------------------------------------------------------------------- | :--------: | ---------- |
| Cuando el usuario le da clic al boton "Evaluar figuras docentes en servicio", se le muestra el formulario |            | x          |
| El formulario sigue el formato que se especifica en el documento 6.2                                      |     x      | x          |
| El formulario puede ser descargado cuando se está fuera de línea y cargado posteriormente.                |            | x          |
| Cuando el usuario ingresa la url manualmente, accede únicamente si ha iniciado la sesión como ECA         |     x      | x          |
##### **Historia de usuario 6: Entrega de convenio**

| Criterios/Fecha                                                                                   | 02/01/2024 | 04/01/2025 |
| :------------------------------------------------------------------------------------------------ | :--------: | ---------- |
| El COT acepta al EC y se ve reflejado en la base de datos.                                        |     x      | x          |
| Cuando el usuario ingresa la url manualmente, accede únicamente si ha iniciado la sesión como COT |     x      | x          |

##### **Historia de usuario 7: Carga de archivo descargado**

| Criterios/Fecha                                                                                                                                          | 31/01/2024 | 03/01/2025 |
| -------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------: | ---------- |
| El sistema debe mandar automáticamente un registro a la base de datos y debe comportarse tal cual como si hubiese sido llenado en el formulario original |     x      | x          |
| El sistema debe cargar automáticamente cada formulario con éxito en cada una de las páginas correspondientes.                                            |            | x          |
##### **Historia de usuario 8:Visualización del estado de la convocatoria**

| Criterios/Fecha                                                           | 21/11/2024 | 15/12/2024 | 24/12/2024 |
| ------------------------------------------------------------------------- | ---------- | ---------- | ---------- |
| El sistema no permite la revisión de los datos si los campos no coinciden | x          | x          | x          |
| El sistema muestra correctamente el estado de su solicitud                |            |            | x          |
##### **Historia de usuario 9:Inicio de sesión**

| Criterios/Fecha                                                                                                            | 05/12/2024 | 10/12/2024 | 13/12/2024 |
| -------------------------------------------------------------------------------------------------------------------------- | :--------: | ---------- | ---------- |
| El sistema permite acceso al usuario, y se asegura de que sólo tenga acceso a sus módulos correspondientes.                |     x      | x          | x          |
| Además, si existe una sesión aparte donde el usuario esté loggeado, hay que denegar el acceso, o invalidar la otra sesión. |            |            | x          |
##### **Historia de usuario 10: Visualización de Convenio**


| Criterios/Fecha                                                                                               | 30/12/2024 | 04/01/2025 |
| ------------------------------------------------------------------------------------------------------------- | :--------: | ---------- |
| El usuario accede a la sección de "Convenio" y se muestra el convenio                                         |            | x          |
| Cuando el usuario ingresa la url manualmente, accede únicamente si ha iniciado la sesión como EC1, EC2 y ECA. |     x      | x          |
##### **Historia de usuario 11: Visualización de los educadores comunitarios**

| Criterios/Fecha                                                                                                                                                                       | 02/01/2025 | 07/01/2025 |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ---------- |
| Cuando el usuario da clic en la sección "Educadores", se despliega una lista de los educadores. Bajo cada educador, se tiene un histórico de cada una de las evaluaciones realizadas. | x          | x          |
| En caso de no tener evaluaciones realizadas, no se muestra nada                                                                                                                       |            | x          |

##### **Historia de usuario 12: Visualización de datos de registro EC**

| Criterios/Fecha                                                                                         |     |
| ------------------------------------------------------------------------------------------------------- | --- |
| Cuando el usuario da clic en la sección "Información", se despliega una lista de botones de descarga.   |     |
| Cada uno de los botones de descarga permite descargar lo correspondiente a cada uno                     |     |
| Cuando el usuario ingresa la url manualmente, accede únicamente si ha iniciado la sesión como EC1 o EC2 |     |

##### **Historia de usuario 13: Calificar Alumnos**
| Criterios/Fecha                                                                                   | 19/12/2024 | 26/12/2024 | 02/01/2025 |
| ------------------------------------------------------------------------------------------------- | :--------: | ---------- | ---------- |
| Cuando el usuario le da clic al boton "Evaluar alumnos", se le muestra el formulario              |            |            | x          |
| El formulario sigue el formato que se especifica en el documento 6.5                              |            | x          | x          |
| El formulario puede ser descargado cuando se está fuera de línea y cargado posteriormente.        |            | x          | x          |
| Cuando el usuario ingresa la url manualmente, accede únicamente si ha iniciado la sesión como EC2 |     x      |            | x          |
##### **Historia de usuario 14: Alta de Alumnos**
| Criterios/Fecha                                                                                         | 28/12/2024 | 02/01/2025 |
| ------------------------------------------------------------------------------------------------------- | :--------: | ---------- |
| Cuando el usuario ingresa a la sección "Control Escolar / Alta", se le muestra el formulario            |            | x          |
| El formulario sigue el formato que se especifica en el documento 6.12                                   |     x      | x          |
| El formulario puede ser descargado cuando se está fuera de línea y cargado posteriormente.              |            |            |
| El alta del (los) alumno(s) se ve reflejada en la lista del EC2 en el grupo correspondiente             |     x      | x          |
| Cuando el usuario ingresa la url manualmente, accede únicamente si ha iniciado la sesión como EC2 o ECA |            | x          |
##### **Historia de usuario 15: Baja de Alumnos**

| Criterios/Fecha                                                                                         | 04/01/2025 | 06/01/2025 |
| ------------------------------------------------------------------------------------------------------- | :--------: | ---------- |
| Cuando el usuario ingresa a la sección "Control Escolar / Baja", se le muestra el formulario            |            | x          |
| El formulario sigue el formato que se especifica en el documento 6.7                                    |     x      | x          |
| El formulario puede ser descargado cuando se está fuera de línea y cargado posteriormente.              |            |            |
| La baja del (los) alumno(s) se ve reflejada en la lista del EC2 en el grupo correspondiente             |     x      | x          |
| Cuando el usuario ingresa la url manualmente, accede únicamente si ha iniciado la sesión como EC2 o ECA |            | x          |
##### **Historia de usuario 16: Solicitud Apoyo Servicios

| Criterios/Fecha                                                                                                                      | 05/01/2025 |
| ------------------------------------------------------------------------------------------------------------------------------------ | :--------: |
| Cuando el COT ingresa un monto, se hace un registro en los apoyos económicos, y es visible dentro de la visualización de los apoyos. |     x      |
##### **Historia de usuario 17: Solicitud Apoyo Estudios

| Criterios/Fecha                                                                                                                                                                                     | 26/12/2024 | 27/12/2024 | 29/12/2024 | 05/01/2025 |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------: | :--------: | :--------: | :--------: |
| Cuando el usuario ingresa a la sección "Control Escolar / Baja", se le muestra el formulario                                                                                                        |     x      |            |            |     x      |
| El formulario sigue el formato que se especifica en el documento 6.7                                                                                                                                |     x      |            |            |     x      |
| El formulario puede ser descargado cuando se está fuera de línea y cargado posteriormente.                                                                                                          |     x      |            |     x      |     x      |
| La baja del (los) alumno(s) se ve reflejada en la lista del EC2 en el grupo correspondiente                                                                                                         |     x      |            |            |     x      |
| Cuando el usuario ingresa la URL manualmente, accede únicamente si ha iniciado la sesión como EC2 o ECA                                                                                             |            |     x      |            |     x      |
| Cuando el usuario ingresa a la sección "Apoyos/Solicitud", se le muestra el formulario                                                                                                              |            |     x      |            |     x      |
| El formulario permite la carga de archivos                                                                                                                                                          |            |            |            |     x      |
| Una vez solicitado el apoyo, en vez de cargar el formulario, se muestra un mensaje de que sólo se puede pedir un apoyo económico por ciclo escolar, y muestra un link que manda a Apoyos/Peticiones |            |     x      |     x      |     x      |
| Cuando el usuario ingresa la URL manualmente, accede únicamente si ha iniciado la sesión como EC1, EC2 o ECA                                                                                        |            |            |     x      |     x      |
##### **Historia de usuario 18: Revisión de los apoyos económicos

| Criterios/Fecha                                                                                                    | 26/12/2024 | 27/12/2024 | 29/12/2024 | 05/01/2025 |
| ------------------------------------------------------------------------------------------------------------------ | :--------: | :--------: | :--------: | :--------: |
| Cuando el usuario ingresa a la sección "Apoyos/Peticiones", se le muestra los apoyos económicos que se solicitaron |            |            |     x      |     x      |
| Cuando el usuario ingresa la URL manualmente, accede únicamente si ha iniciado la sesión como EC1, EC2 o ECA       |     x      |     x      |            |     x      |
##### **Historia de usuario 19: Aceptación de Apoyo Económico

| Criterios/Fecha                                                                                                                        | 02/01/2024 | 04/01/2024 | 07/01/2024 |
| -------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ---------- | ---------- |
| Cuando la CIDAP inicia sesión, automáticamente lo manda a la sección de apoyos económicos                                              | x          | x          | x          |
| Cuando se acepta / rechaza la solicitud, se muestra en la base de datos y el solicitante puede ver este cambio realizado en su cuenta. |            | x          | x          |
| En caso de ingresar la URL manualmente, sólo se le permite el acceso a la CIDAP                                                        |            |            | x          |

##### **Historia de usuario 20: GIS

| Criterios/Fecha                                                                                            | 26/12/2024 | 28/12/2024 |
| ---------------------------------------------------------------------------------------------------------- | :--------: | ---------- |
| El mapa es visible para todos, no está bloqueado detrás de inicio de sesión para mantener la transparencia |            | x          |



##### **Historia de usuario 21: GIS con detalles de CCT**

| Criterios/Fecha                                                                                          | 29/12/2024 | 30/12/2024 |
| -------------------------------------------------------------------------------------------------------- | :--------: | :--------: |
| El mapa es visible                                                                                       |     x      |     x      |
| Se puede visualizar la información de los CCT de forma correcta                                          |     x      |     x      |
| Muestra los detalles correctos, y cualquier cambio se ve reflejado en esta página después de refrescarla |     x      |     x      |
| En caso de ingresar la URL manualmente, sólo se le permite el acceso al DEP.                             |     x      |     x      |
##### **Historia de usuario 22: GIS para distribución de tallas**

| Criterios/Fecha                                                                                                                   | 30/12/2025 | 07/01/2025 |
| --------------------------------------------------------------------------------------------------------------------------------- | :--------: | ---------- |
| El administrador de almacenes puede iniciar sesión y se le muestra la página correspondiente.                                     |            | x          |
| Se muestra correctamente la cantidad de prendas necesarias según lo especificado                                                  |     x      | x          |
| El algoritmo de clusterización identifica correctamente los grupos de CCT's                                                       |            | x          |
| El algoritmo de distribución identifica una ruta que incluya todos los CCT's de cada grupo, y la ruta se puede mostrar al usuario |            | x          |
| En caso de ingresar la URL manualmente, sólo se le permite el acceso al administrador de almacenes.                               |     x      | x          |

##### **Historia de usuario 23: Registro de tallas anteriores

| Criterios/Fecha                                                                                     | 29/01/2028 | 02/01/2024 | 03/01/2025 |
| --------------------------------------------------------------------------------------------------- | :--------: | ---------- | ---------- |
| El administrador de almacenes puede iniciar sesión y acceder a la sección "Estadísticas Históricas" |            |            | x          |
| Las gráficas y las cantidades se muestran de forma correcta                                         |            | x          | x          |
| La página web puede ser impresa correctamente                                                       |            | x          | x          |
| En caso de ingresar la URL manualmente, sólo se le permite el acceso al administrador de almacenes  |     x      | x          | x          |
