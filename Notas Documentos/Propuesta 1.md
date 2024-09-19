#propuesta #unfinished

## Objetivo principal
Implementar un sistema web para la petición de creación, seguimiento de las localizaciones educativas y su control de recursos y personal educativo de la CONAFE

## Objetivos específicos

#### Servicio de creación y su seguimiento de localidades 
[[MDP Microplaneacion.pdf#page=28]]
- Permitir a operativo de la [[JIAL]] el registro de la ubicación asociada a la [[petición de servicios educativos]] de nivel preescolar, primaria y secundaria
- Permitir a un operativo de la JIAL asignar a una [[investigador de campo]] una lista de localidades a investigar
- Permitir al investigador de campo el llenado del [[MDP Microplaneacion.pdf#page=32\|formato de factibilidad]] de una localidad como servicio educativo
- Permitir a la JIAL aceptar o rechazar los formatos de factibilidad y firmarlos digitalmente
- Permitir a [[Cordinador Territorial\|CT]] recibir la lista de localidades nuevas para [[Programación Detallada Anual|PRODET]]
- Permitir al CT marcar el inicio y la finalización de la construcción de la localidad
- Permitir al CT marcar la ubicación por mes de las localidades en condición de circo por [[Lineamientos Formación.pdf#page=31\|las responsabilidades del educador comunitario]]

#### Servicio de personal educativo
Los datos del personal educativo están en 
- Permitir al operativo de la JIAL registrar los [[Lineamientos Formación.pdf#page=21\|datos]] del personal educativo, y la fecha de terminación de convenio
- Proporcionar al operativo de la JIAL una lista de localizaciones como sugerencia a las que se puede asignar el personal educativo por persona
- Proporcionar al opérativo de la JIAL asigna el personal educativo a cada localidad
- Permitir al [[profesor de acompañamiento]] la carga del seguimiento del personal educativo
- Permitir al CT recibir los reportes del profesor de acompañamiento para el seguimiento del personal educativo
- Permitir a CT la modificación del estado del personal educativo
- Permitir a CT la renovación del convenio del personal educativo

## Recursos
- API tipo MAPS para ubicar las localizaciones
- Firma digital basada en RSA
- Implementación de KNN para la generación de sugerencia de centro educativo para personal educativo
- Base de datos relacional con MySQL