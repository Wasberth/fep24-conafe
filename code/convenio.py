from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime
import random
import string
from docx import Document
import secrets
from mongo_objects.cct import CCT

load_dotenv()
uri = os.environ['uri']
client = MongoClient(uri)
db = client['captacion']
formulario_collection = db['formulario']


db = client['CCT']
cct_collection = db['cct']


COTs = {
    "AGUASCALIENTES": "Álvaro de Ávila Aguilar",
    "BAJA CALIFORNIA": "Juan Gálvez Lugo",
    "BAJA CALIFORNIA SUR": "José Jesús Flores Castro",
    "CAMPECHE": "María Guadalupe Sarlat Ancona",
    "CHIAPAS": "Ernesto Pérez Bautista",
    "CHIHUAHUA": "Lorenza Botello Montañez",
    "COAHUILA": "Alcira de Jesús Vásquez Corral",
    "COLIMA": "Luis Alberto Araoz Ubaldo",
    "DURANGO": "María del Pilar Espino",
    "ESTADO DE MEXICO": "Berenice Olmos Sánchez",
    "GUANAJUATO": "Giovana Battaglia Velazquez",
    "GUERRERO": "José Enrique Pérez Franco",
    "HIDALGO": "Joel Guerrero Juárez",
    "JALISCO": "Lilia Dalila López Salmorán",
    "MICHOACAN": "Genoveva Pérez Vieyra",
    "MORELOS": "Araceli Castillo Macías",
    "NAYARIT": "Adán Rivera Ramos",
    "NUEVO LEON": "Martha Idalia Garza González",
    "OAXACA": "Alejandra Brito Rodríguez",
    "PUEBLA": "Cutberto Cantoran Espinosa",
    "QUERETARO": "Alejandra Torres Martínez",
    "QUINTANA ROO": "Nancy Paola Chávez Arias",
    "SAN LUIS POTOSI": "César Vázquez Jiménez",
    "SINALOA": "Anatolio Lugo Félix",
    "SONORA": "Elena Ramírez Madueña",
    "TABASCO": "Gabino de la Torre Ochoa",
    "TAMAULIPAS": "Roberto Villarreal Danwing",
    "TLAXCALA": "Rocío Reyes Sánchez",
    "VERACRUZ": "Antonio Rubén Viveros Álvarez",
    "YUCATAN": "Daniel Flores Albornoz",
    "ZACATECAS": "Rito Longoria Castrejón"
}

def generar_cadena_aleatoria(longitud=255):
    caracteres = string.ascii_letters + string.digits  # Letras y números
    cadena_aleatoria = ''.join(random.choices(caracteres, k=longitud))
    return cadena_aleatoria


def obtener_todos_los_cct():
    cct_data_list = cct_collection.find({}, {"_id": 0, "clave": 1, "nombre": 1, "municipio": 1, "comunidad": 1, "sede": 1, "estado": 1})
    cct_list = [CCT(**cct_data) for cct_data in cct_data_list]
    return cct_list

def obtener_todos_los_datos():
    projection = {
        "_id": 0,
        "nombre": 1,
        "apellido1": 1,
        "apellido2": 1,
        "estado_republica": 1,
        "genero": 1,
        "direccion": 1,
        "situacion_educativa": 1,
        "fecha_nacimiento": 1
    }
    return formulario_collection.find({}, projection)

def calcular_edad(fecha_nacimiento):
    try:
        fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
    except ValueError:
        try:
            fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%d/%m/%Y")
        except ValueError:
            raise ValueError(f"Formato de fecha no reconocido: {fecha_nacimiento}")
    fecha_actual = datetime.now()
    edad = fecha_actual.year - fecha_nacimiento.year
    if (fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1
    return edad

def generar_cadena_aleatoria(longitud=15):
    caracteres = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))


cct_list = obtener_todos_los_cct()



def generar_contrato(datos):

    dia = datetime.now().day
    mes = datetime.now().month
    ano = datetime.now().year
   
    for i in datos:
        nombre = i["nombre"]
        apellido1 = i["apellido1"]
        apellido2 = i.get("apellido2", "")

        genero = i["genero"]

        if genero == "Male":
            genero = "EL"
        elif genero == "Female":
            genero = "LA"
        elif genero == "Other":
            genero = "EL/LA"
       
        direccion = i["direccion"]
        situacion_educativa = i["situacion_educativa"]
        fecha_nacimiento = i.get("fecha_nacimiento")
        estado_republica = i.get("estado_republica")
        if not fecha_nacimiento:
            print(f"Documento sin fecha_nacimiento: {i}")
            continue
        edad = calcular_edad(fecha_nacimiento)
        cadena = generar_cadena_aleatoria()
        doc = Document()

        registro = next((cct for cct in cct_list if cct.estado.upper() == estado_republica.upper()), None)
        if registro:
            persona = COTs.get(registro.estado.upper(), "No se encontró información")
            sede = registro.sede
      
        else:
            print(f"No se encontró información para el estado {estado_republica}")

        
        cadena1 = generar_cadena_aleatoria()
        cadena2 = generar_cadena_aleatoria()

    

        
        texto = f'''CONVENIO DE CONCERTACIÓN VOLUNTARIA PARA FORMALIZAR LA PARTICIPACIÓN DEL ASPIRANTE A EDUCADOR 
                COMUNITARIO EN LA ETAPA DE FORMACIÓN Y/O COMO DENTRO DEL SISTEMA DE FORMACIÓN EN LA PRÁCTICA EDUCATIVA COMUNITARIA Y EL  OTORGAMIENTO DE APOYOS ECONÓMICOS, QUE CELEBRAN POR UNA PARTE EL CONSEJO NACIONAL DE FOMENTO EDUCATIVO “EL CONAFE”, REPRESENTADO EN ESTE ACTO POR EL DIRECTOR DE OPERACIÓN TERRITORIAL, EL MTRO. JUAN MARTÍN MARTÍNEZ BECERRA, AUXILIADO PARA EL CUMPLIMIENTO DEL PRESENTE INSTRUMENTO POR EL (LA) COORDINADOR (A) TERRITORIAL PARA EL SERVICIO EDUCATIVO DEL CONAFE, EL (LA) C. {persona}, EN EL ESTADO DE {estado_republica} Y POR LA OTRA EL (LA) C.{nombre} {apellido1} {apellido2}, A QUIEN SE DENOMINARÁ EN LO SUBSECUENTE {genero} ASPIRANTE, A QUIENES DE FORMA CONJUNTA SE LES DENOMINARÁ “LAS PARTES”, AL TENOR DE LAS DECLARACIONES Y CLÁUSULAS SIGUIENTES: 
                D E C L A R A C I O N E S I. DE “EL CONAFE”: 
                I.1.- Que es un Organismo Descentralizado creado por el Ejecutivo Federal, que tiene por objeto el fomento educativo a través de la prestación de servicios de educación inicial y básica con Equidad Educativa e Inclusión Social a la población infantil de cero a tres años once meses y niñas, niños y adolescentes hasta los 16 años de edad, que habitan en localidades preferentemente rurales e indígenas que registran altos y muy altos niveles de marginación y/o rezago social, bajo el modelo de Educación Comunitaria, de conformidad con el Decreto que lo rige publicado en el Diario Oficial de la Federación el 18 de marzo de 2016.  
                
                I.2.- Que es representado en este acto por su Director de Operación Territorial, con fundamento en lo establecido en los artículos, 5 fracción III, inciso c), 15, 16 fracción IV, 21 fracciones III, VIII, IX y XLVIII del Estatuto Orgánico de “EL CONAFE”, así como del Acuerdo por el que se reforman, adicionan y derogan diversas disposiciones del citado  Estatuto, publicados en el Diario Oficial de la Federación el 29 de noviembre del 2016 y el 19 de julio del 2019, respectivamente, en relación con el contenido del instrumento notarial número 122,005 (ciento veintidós mil cinco), del Libro 2,992 (dos mil novecientos noventa y dos), de fecha 20 de mayo de 2021, protocolizado por el Lic. Rafael Arturo Coello Santos, Titular de la Notaría número 30 de la Ciudad de México, el cual contiene, entre otros, poder general para pleitos y cobranzas, así como para actos de administración a su favor. 
                
                I.3.- Que el Director de Operación Territorial se auxiliará del (de la) Coordinador (a) Territorial para el Servicio Educativo de “EL CONAFE” en el estado de {estado_republica} para el cumplimiento del objeto del presente  convenio, así como para el seguimiento y supervisión de las obligaciones a cargo de {genero} ASPIRANTE, de conformidad con el artículo 21 fracciones V y VI del 
                Acuerdo por el que se reforman, adicionan y derogan diversas disposiciones del Estatuto Orgánico del Consejo Nacional de Fomento Educativo publicado en el Diario Oficial de la Federación el diecinueve de julio de dos mil diecinueve. 
                
                I.	4.- Que para los efectos de este convenio señala como domicilios para oír y recibir todo tipo de notificaciones y documentos el ubicado en Avenida Universidad, Número 1200, Colonia Xoco, Alcaldía Benito Juárez, Código Postal 03330, Ciudad de México; y/o {sede}
                
                
                
                
                II.	DE  {genero} ASPIRANTE  : 
                
                II.1.- Que es de nacionalidad mexicana, con estudios de {situacion_educativa}, que cuenta con {edad} años de edad y señala como domicilio para oír y recibir todo tipo de notificaciones y documentos el ubicado en {direccion}. 
                II.2.- Que es su deseo y voluntad colaborar temporalmente con “EL CONAFE”, incorporándose al Sistema de Formación en la Práctica Educativa Comunitaria y brindar atención educativa en la comunidad que “EL CONAFE” le asigne.  
                Conforme a las declaraciones que anteceden, se establecen las siguientes cláusulas:  
                C	L Á U S U L A S 
                PRIMERA. - DEL OBJETO. Formalizar la participación de concertación voluntaria de {genero} ASPIRANTE en su etapa de formación dentro del Sistema de Formación en la Práctica Educativa Comunitaria que brinda “EL CONAFE” durante el ciclo escolar 2022-2023 para desarrollar la práctica educativa basada en la pedagogía de la relación tutora y la metodología para la reflexión sobre las prácticas de crianza, así como  normar el otorgamiento de apoyos económicos. 
                
                SEGUNDA. - DEL PROCESO DE FORMACIÓN. Las partes convienen que este proceso formativo se regirá de conformidad con las siguientes obligaciones: 
                De “EL (LA) ASPIRANTE”  
                a) Participar en la formación inicial o extemporáneo que imparta “EL CONAFE” previo a la práctica educativa. 
                De {genero} ASPIRANTE: 
                a) Participar en la formación inicial y permanente que imparta “EL CONAFE” previo y durante el ciclo escolar correspondiente atendiendo a los tiempos y contenidos establecidos por la Coordinación Territorial para el Servicio Educativo del CONAFE en la entidad federativa.  
                De “EL CONAFE”: 
                a)	Podrá entregar a {genero} ASPIRANTE y/o a un apoyo económico durante la etapa de formación inicial intensiva el cual debe  ser utilizado para los gastos de traslado, alimentación y hospedaje. El monto del apoyo económico dependerá las tarifas autorizadas por la Comisión de Interna de Administración y Programación (CIDAP) y de acuerdo a la disponibilidad presupuestal mismas que serán comunicadas por la Dirección de Educación Comunitaria para el Bienestar y estarán expresadas en los Lineamientos Generales del Sistema de Formación en la Práctica Educativa Comunitaria.   
                b)	“EL CONAFE” determinará al finalizar la formación inicial si {genero} ASPIRANTE está en condiciones de desarrollar la práctica educativa como para el ciclo escolar 2024-2025. 
                De “LAS PARTES”: 
                a) Atender las funciones y responsabilidades descritas en los Lineamientos Generales del Sistema de Formación en la Práctica Educativa Comunitaria. 
                
                TERCERA. – DE LA PRÁCTICA EDUCATIVA COMUNITARIA. “LAS PARTES” convienen que la práctica educativa comunitaria se regirá de conformidad con lo siguiente: De {genero} ASPIRANTE: 
                a)	Desarrollar la práctica educativa de la relación tutora y de la metodología para la reflexión sobre las prácticas de crianza, dedicando tiempo de atención pedagógica en los días y horarios acordados con la APEC, con base al calendario vigente y de acuerdo a lo establecido en los Lineamientos Generales del Sistema de Formación en la Práctica Educativa Comunitaria. 
                
                b)	Realizar la práctica educativa en uno o más servicios educativos que se brinden en una comunidad, o realizando funciones de acompañamiento a una microrregión o región, así como promover el aprendizaje durante toda la vida de jóvenes y adultos.  
                
                c)	Brindar un trato amable, respetuoso y digno que garantice la integridad física y emocional de los estudiantes que son atendidos en los servicios educativo de “EL CONAFE”, respetando los derechos humanos de personas gestantes, los bebés, las niñas, niños, adolescentes, jóvenes y de los integrantes demás integrantes de la comunidad; y en general, con toda persona que tenga relación con motivo de la práctica educativa comunitaria.  
                
                De “EL CONAFE”: 
                a) Derivado de alguna contingencia que suceda en el país (sismo, inundación, pandemia, o cualquier situación que impida el curso normal de la operación), “EL CONAFE” informará las acciones emergentes a implementarse para que se cumpla la labor educativa en la que se ven inmersos los (las) Educadores (as) Comunitarios (as). 
                De “LAS PARTES”: 
                a) Atender las funciones y responsabilidades descritas en los Lineamientos Generales del Sistema de Formación en la Práctica Educativa Comunitaria. 
                
                CUARTA. - DE LOS APOYOS ECONÓMICOS.  
                “EL CONAFE” entregará a {genero} ASPIRANTE un apoyo económico mensual, por la cantidad de $3100.00 (TRES MIL CIEN PESOS 00/100 M. N.) durante el tiempo de permanencia en la práctica educativa comunitaria, de acuerdo a los periodos del ciclo escolar establecidos en los Lineamiento Generales del Sistema de Formación en la Práctica Educativa Comunitaria. 
                a)	Las cuotas del apoyo económico serán diferentes por tipo de figura (EC, ECA o ECAR) y nivel educativo (Inicial, preescolar, primaria o secundaria) conforme lo aprobado por la Comisión Interna de Administración y Programación (CIDAP) y en los Lineamientos Generales del Sistema de Formación en la Práctica Educativa Comunitaria. 
                b)	En los casos donde “EL (LA) EDUCADOR (A) COMUNITARIO” atienda los niveles de inicial y preescolar, se tomará como monto del apoyo económico el correspondiente a este último nivel.  
                c)	En las localidades donde “EL (LA) EDUCADOR (A) COMUNITARIO” sea foráneo y pernocte, la comunidad le brindará alimentación y hospedaje como se establece en el convenio que formaliza la participación de la APEC en la Educación Comunitaria para el Bienestar.  
                
                
                QUINTA – DE LOS APOYOS ECONÓMICOS PARALELOS.  
                “EL CONAFE” podrá otorgar a {genero} ASPIRANTE apoyos paralelos de acuerdo a los criterios de asignación establecidos en los Lineamientos Generales del Sistema de Formación en la Práctica Educativa Comunitaria, para los siguientes fines:  
                a)	La continuación de estudios durante o posterior a la práctica educativa en instituciones públicas o privadas con Reconocimiento de Validez Oficial de Estudios (RVOE) o con clave del centro de trabajo, de acuerdo a lo establecido en los Lineamientos vigentes.  
                b)	Conectividad móvil para apoyar las funciones académicas. 
                c)	Transportación, alimentación y hospedaje para asistir a las reuniones de formación en las microrregiones, de acuerdo a lo establecido en el calendario de formación. 
                d)	Al concluir la práctica educativa comunitaria, “EL CONAFE” continuará proporcionando a los (las) ex educadores (as) comunitarios (as) espacios de formación para favorecer su participación en las comunidades de aprendizaje.  
                e)	Apoyo económico de fin de año sujeto a la disposición presupuestal. 
                f)	Otorgar un apoyo económico para la atención médico-quirúrgica, farmacéutica y hospitalaria en caso de accidente, enfermedad o incapacidad total permanente hasta por la cantidad que determine “EL CONAFE”, durante la etapa de formación inicial, la práctica educativa comunitaria y como beneficiario para la continuación de estudios. 
                g)	En caso de fallecimiento, para la entrega del apoyo autorizado para esta situación, {genero} ASPIRANTE designa como su(s) beneficiario(s) a: 
                ____________________________________________________________________________________, quien(es) es (son) mayor(es) de edad, mismo(s) que será(n) reconocido(s) con ese carácter por “EL CONAFE” hasta en tanto aquél/aquélla no realice nueva designación. Este apoyo se otorgará también durante la práctica educativa comunitaria y como beneficiario para la continuidad de estudios. 
                h)	Otorgamiento de vestuario de identificación institucional. 
                i)	Acompañamiento académico y técnico pedagógico por parte de la Coordinación Territorial para el Servicio Educativo del CONAFE en la Entidad Federativa.  
                
                SEXTA. - DE LA RESCISIÓN. Ambas partes convienen en que “EL CONAFE” tendrá la facultad de rescindir el presente convenio mediante notificación por escrito del (de la) Coordinador (a) Territorial para el Servicio Educativo en la Entidad Federativa, previa solicitud expresa que presenten el (la) Presidente de la APEC o el personal de la propia Coordinación Territorial sin necesidad de declaración judicial, cuando {genero} ASPIRANTE incurra en alguno de los supuestos: 
                a)	Incumpla con las obligaciones inherentes a la formación o a la práctica educativa comunitaria.  
                b)	Realice acciones que entorpezcan las actividades durante la formación o la práctica educativa comunitaria.  
                c)	Incurra en faltas de honradez 
                d)	Tenga cinco inasistencias injustificadas durante el proceso de formación y/o la práctica educativa comunitaria.  
                e)	Incurra en actos de violencia en contra de los miembros de la comunidad, personal del CONAFE o de cualquier persona con la que tenga relación con motivo del convenio y/o cualquier delito tipificado por el fuero común y/ o federal. 
                f)	Cuando se haya dictado en su contra una sentencia definitiva de tipo penal o administrativa.  
                g)	Realice actos que pongan en riesgo la integridad física y emocional de los estudiantes.  
                h)	Realice actos de proselitismos políticos o religioso durante su estancia en la sede de formación o la práctica educativa comunitaria 
                
                SÉPTIMA. - DE LA TERMINACIÓN ANTICIPADA. “EL CONAFE” podrá dar por terminado anticipadamente el presente convenio, sin responsabilidad cuando concurran razones de interés general. “LAS PARTES” convienen que se entenderá como causa de interés general, orden púbico, y disposición legal, la instrucción, directiva, pronunciamiento de cualquier autoridad competente, así como del comunicado del Ejecutivo Federal en materia de austeridad, fortalecimiento, salud pública, reducción presupuestal que restrinja el gasto, entre otras, que impacten a “EL CONAFE”.  
                
                OCTAVA. - MARCO LEGAL. Las partes manifiestan que suscriben el presente convenio con fundamento en los artículos, 37, 38 y 39 de la Ley de Planeación en relación de los convenios de concertación; artículos 31 y 32 de la Ley General de Educación y 7o. y 8o. del Reglamento para la Educación Comunitaria, por lo que no constituye relación laboral alguna. En consecuencia, cualquier controversia la resolverán de común acuerdo. 
                
                NOVENA. - VIGENCIA.   
                a)	La vigencia del presente convenio se inicia a partir de la fecha de su firma y por el ciclo escolar 2022-2023, pudiendo ser ampliada mediante modificación por escrito a la misma. 
                b)	“LAS PARTES” expresan estar de acuerdo que la suscripción del presente convenio de ninguna manera presupone el vínculo o relación laboral entre “EL CONAFE” y {genero} ASPIRANTE en virtud de que se busca garantizar el acceso a la educación establecido en el Artículo 3º de la Constitución Política de los Estados Unidos Mexicanos.  
                
                DECIMA. - FIRMA ELECTRÓNICA 
                A través de la firma electrónica del presente convenio, acepto la utilización de los datos de validación electrónica (firma) que “EL CONAFE” disponga para la autenticación a través de medios digitales 
                
                Leídas las cláusulas del presente convenio por ambas partes y enteradas de su contenido y alcance legal, reconocen que no existen en el mismo, vicios de voluntad, por lo que firman de conformidad al margen y al calce, en dos tantos, conservando un original para cada una de las partes, en {estado_republica},  a {dia} de {mes} del {ano}.  
                
                POR EL CONAFE 
                MTRO. JUAN MARTÍN MARTÍNEZ BECERRA DIRECTOR DE OPERACIÓN TERRITORIAL. 
                FIRMA ELECTRÓNICA 
                {cadena1}
                
                
                POR “EL CONAFE” 
                EL(LA) COORDINADOR(A) TERRITORIAL PARA EL SERVICIO EDUCATIVO DEL CONAFE EN EL ESTADO DE {estado_republica}
                FIRMA ELECTRÓNICA 
                {cadena2}
                
                
                
                
                {genero} ASPIRANTE

                FIRMA ELECTRÓNICA 
                '''
 # Tu texto completo aquí
        doc.add_paragraph(texto)
        doc.save(f"contrato_{nombre}_{cadena}.docx")



# Ejecución principal
datos = obtener_todos_los_datos()
generar_contrato(datos)
