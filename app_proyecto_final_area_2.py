
from IPython.display import display # Importamos el siguiente componente del módulo display para poder representar correctamente el mapa dentro del menú creado.
import folium                       # Importamos la librería folium para representar un mapa de las comisarías y los delitos cometidos.
from datetime import datetime       # Importamos el módulo datetime de la librería datetime.
from pyproj import Transformer      # Importamos la clase Transformer de la librería pyproj.
import numpy as np                  # Importamos la librería numpy.
import math                         # Importamos la librería math.
import webbrowser
import os
from dotenv import load_dotenv
import pymongo
import mysql.connector
import mysql_insertar_datos
import mysql_consultas_datos
import mongodb_delincuencia


# Vvariables para el menú que controla los procesos.
proceso_delitos = 1
proceso_criminal = 2
proceso_comisarias = 3
proceso_hospitales = 4
proceso_areas_comunitarias = 5
proceso_mapa = 6
proceso_ordenar_delitos = 7
proceso_tiempo_entre_delitos = 8
proceso_comisarias_cercanas_a_delitos = 9
proceso_cerrar_app = 10

delitos_areas = []                          # Lista de los delitos según áreas.

sistema_referencia_origen = "EPSG:4326"     # Sistema geográfico.
sistema_referencia_destino = "EPSG:26916"   # Sistema proyectado.
transformer = Transformer.from_crs(sistema_referencia_origen, sistema_referencia_destino)   # Definimos la variable transformer para crear el objeto transformador.


# ------------------------------------- MENÚ Y CONTROLADOR DE PROCESOS DEL PROGRAMA -----------------------------
def controlador(par_proceso):
    proceso = par_proceso
    
    if proceso == proceso_delitos:
        opcion_orden = ""
        # Se ejecuta el bucle hasta que el usuario pulse una de las opciones disponibles
        while opcion_orden not in (1, 2, 3, 4):
            try:
                opcion_orden = int(input("\nElige una opción:\n\
- 1) Buscar delitos.\n\
- 2) Mostrar todos los delitos.\n\
- 3) Agregar delito.\n\
- 4) Editar delito.\n\
Introduce el número que corresponda con la opción escogida: "))
                if opcion_orden == 1:
                    mysql_consultas_datos.buscar_delitos_por_valor()
                elif opcion_orden == 2:
                    mysql_consultas_datos.mostrar_todos_los_delitos()
                elif opcion_orden == 3:
                    mysql_insertar_datos.agregar_delito()
                elif opcion_orden == 4:
                    mysql_consultas_datos.editar_delito()
            except: print("Has introducido una opción no válida.")

    elif proceso == proceso_criminal:
        opcion_orden = ""
        while opcion_orden not in range(1,7):
            try:
                opcion_orden = int(input("\nElige una opción:\n\
- 1) Buscar criminales entre fechas de nacimiento.\n\
- 2) Buscar Por delito.\n\
- 3) Buscar por estatura y peso.\n\
- 4) Mostrar lista con todos los criminales.\n\
- 5) Agregar un criminal.\n\
- 6) Editar un criminal.\n\
Introduce el número que corresponda con la opción escogida: "))
                if opcion_orden == 1:
                    mongodb_delincuencia.buscar_por_fecha()
                elif opcion_orden == 2:
                    mongodb_delincuencia.buscar_por_delito()
                elif opcion_orden == 3:
                    mongodb_delincuencia.buscar_por_estatura_peso()
                elif opcion_orden == 4:
                    mongodb_delincuencia.mostrar_todos_los_criminales()
                elif opcion_orden == 5:
                    mongodb_delincuencia.agregar_criminal()
                elif opcion_orden == 6:
                    mongodb_delincuencia.editar_criminal()
            except: print("Has introducido una opción no válida.")

    elif proceso == proceso_comisarias:
        opcion_orden = ""
        while opcion_orden not in (1, 2):
            try:
                opcion_orden = int(input("\nElige una opción:\n\
- 1) Mostrar todas las comisarias.\n\
- 2) Agregar una comisaria.\n\
Introduce el número que corresponda con la opción escogida: "))
                if opcion_orden == 1:
                    mysql_consultas_datos.mostrar_todas_las_comisarias()            
                elif opcion_orden == 2:
                    mysql_insertar_datos.agregar_comisaria()            
            except: print("Has introducido una opción no válida.")

    elif proceso == proceso_hospitales:
        opcion_orden = ""
        while opcion_orden not in (1, 2):
            try:
                opcion_orden = int(input("\nElige una opción:\n\
- 1) Mostrar todos los Hospitales.\n\
- 2) Agregar un Hospital.\n\
Introduce el número que corresponda con la opción escogida: "))
                if opcion_orden == 1:
                    mysql_consultas_datos.mostrar_todos_los_hospitales()          
                elif opcion_orden == 2:
                    mysql_insertar_datos.agregar_hospital()
            except: print("Has introducido un valor no válido.")

    elif proceso == proceso_areas_comunitarias:
        opcion_orden = ""
        while opcion_orden != 1:
            try:
                opcion_orden = int(input("\nElige una opción:\n\
- 1) Mostrar todas las Áreas Comunitarias.\n\
Introduce el número que corresponda con la opción escogida: "))
                if opcion_orden == 1:
                    mysql_consultas_datos.mostrar_areas_comunitarias()    
            except: print("Has introducido un valor no válido.")   

    elif proceso == proceso_mapa:
        ver_mapa()

    elif proceso == proceso_ordenar_delitos:
        opcion_orden = ""
        while opcion_orden not in (1, 2):
            try:
                opcion_orden = int(input("\n¿Cómo quieres ordenar los delitos?\n\
- 1) De más antiguo a más reciente.\n\
- 2) De más reciente a más antiguo.\n\
Introduce el número que corresponda con la opción escogida: "))
                if opcion_orden == 1:
                    mysql_consultas_datos.mostrar_delitos_asc()
                elif opcion_orden == 2:
                    mysql_consultas_datos.mostrar_delitos_desc()
            except: print("Has introducido un valor no válido.") 

    elif proceso == proceso_tiempo_entre_delitos:
        calcular_tiempo_entre_delitos()

    elif proceso == proceso_comisarias_cercanas_a_delitos:
        encontrar_comisaria_mas_cercana()

    elif proceso == proceso_cerrar_app:
        cerrar_sesion()

    else:
        print("Has introducido un valor no válido. Vuelve a intentarlo.")

# Función para el menú.
def main():
    try:
        continuar = True
        while continuar:
            proceso = int(input("\n¡Hola Agente! ¿Con que información desea trabajar?\n\
\n1) Delitos.\n\
2) Criminales.\n\
3) Comisarias.\n\
4) Hospitales.\n\
5) Áreas comunitarias.\n\
6) Ver mapa de delitos y comisarias.\n\
7) Mostrar y ordenar los delitos existentes.\n\
8) Calcular el tiempo entre delitos.\n\
9) Comprobar cuál es la comisaría más cercana a cada delito.\n\
10) Cerrar sesión.\n\
\nIntroduce el número que corresponda con la opción escogida: "))
            controlador(proceso)

            if proceso == 10:
                continuar = False
            else:
                respuesta = ""
                while respuesta not in ("si", "sí", "no"):
                    respuesta = input("¿Desea hacer algo más? (SI/NO): ").strip().lower()
                if respuesta == 'no':
                    continuar = False

        print("\n¡Hasta pronto! ¡Qué tenga un buen día!")
        
    except: print("Has introducido un valor no válido. La aplicación se ha cerrado.")

# Función para cerrar la sesión del programa.
def cerrar_sesion():
    print("Ha cerrado la sesión correctamente.")

# ------------------------------------------ FUNCIONES PARA EL CONTROLADOR -------------------------------------------


# Función para establecer las coordenadas para el mapa.
def ver_mapa():
    # Creamos un mapa centrado en una ubicación por defecto
    mapa = folium.Map()

    # Obtenemos las ubicaciones de las comisarías desde la base de datos.
    ubicaciones_comisarias = mysql_consultas_datos.coordenadas_comisarias()

    # Obtenemos las ubicaciones de los delitos desde la base de datos.
    ubicaciones_delitos = mysql_consultas_datos.coordenadas_delitos()

    # Llamamos a la función para agregar marcadores de comisarías al mapa.
    marcador_comisarias(mapa, ubicaciones_comisarias)

    # Llamamos a la función para agregar marcadores de delitos al mapa.
    marcador_delitos(mapa, ubicaciones_delitos)

    # Creamos un mapa centrado en todas las ubicaciones.
    todas_ubicaciones = ubicaciones_comisarias + ubicaciones_delitos
    if todas_ubicaciones:
        mapa.fit_bounds([ubicacion[:2] for ubicacion in todas_ubicaciones])

    # Guardamos el mapa como un archivo HTML
    mapa_html = "mapa_delitos_comisarias.html"
    mapa.save(mapa_html)

    # Abrir automáticamente el archivo en el navegador web predeterminado
    print("Aquí tienes el mapa con las comisarías y delitos existentes: ")
    webbrowser.open(os.path.abspath(mapa_html))

    print("Mira la página que se abrió en tu navegador")

def marcador_comisarias(mapa, ubicaciones):
    for ubicacion in ubicaciones:
        lat, lon, nombre = ubicacion
        folium.Marker(
            location=[lat, lon],
            popup=nombre,
            icon=folium.Icon(color='blue')
        ).add_to(mapa)


def marcador_delitos(mapa, ubicaciones):
    for ubicacion in ubicaciones:
        lat, lon, texto = ubicacion
        folium.Marker(
            location=[lat, lon],
            popup=texto,
            icon=folium.Icon(color='red')
        ).add_to(mapa)


# Función para calcular el tiempo entre delitos.
def calcular_tiempo_entre_delitos():
    # Ordenar los delitos por fecha de forma ascendente.
    delitos_ordenados = mysql_consultas_datos.delitos_asc_retorno()

    # Verificar si se obtuvieron resultados
    if not delitos_ordenados:
        print("No se encontraron delitos para calcular el tiempo entre ellos.")
        return
    
    # Guardar la primera fecha para determinar si es str o datetime.
    primera_fecha = delitos_ordenados[0]["Fecha"]

    # Calcular la diferencia de tiempo entre delitos consecutivos.
    print("Tiempo entre delitos consecutivos: \n")
    for i in range(1, len(delitos_ordenados)):
        if type(primera_fecha) is str:
            # Si las fechas son cadenas, convertirlas a objetos datetime.
            fecha_actual = datetime.strptime(delitos_ordenados[i]["Fecha"], "%Y-%m-%d %H:%M:%S")
            fecha_anterior = datetime.strptime(delitos_ordenados[i - 1]["Fecha"], "%Y-%m-%d %H:%M:%S")
        else:
            # Si las fechas ya son objetos datetime, usarlas directamente.
            fecha_actual = delitos_ordenados[i]["Fecha"]
            fecha_anterior = delitos_ordenados[i - 1]["Fecha"]

        # Calcular la diferencia de tiempo entre las fechas.
        diferencia = fecha_actual - fecha_anterior
        tiempo_en_minutos = diferencia.total_seconds() / 60
        num_caso_actual = delitos_ordenados[i]["Núm. caso"]
        num_caso_anterior = delitos_ordenados[i - 1]["Núm. caso"]
        print(f"El tiempo entre el caso número {num_caso_anterior} y el caso número {num_caso_actual} es de {tiempo_en_minutos:.1f} minutos \n")


# Función para transformar las coordenadas delitos de sistema geográfico al sistema proyectado.
def convertir_coordenadas_delitos():
    delitos_transformados = []
    ubicaciones_delitos = mysql_consultas_datos.coordenadas_delitos()

    sistema_referencia_origen = "EPSG:4326"     # Sistema geográfico.
    sistema_referencia_destino = "EPSG:26916"   # Sistema proyectado.
    transformer = Transformer.from_crs(sistema_referencia_origen, sistema_referencia_destino)

    for delito in ubicaciones_delitos:
        latitud, longitud, num_caso = delito    
        
        #Trasnformar coordenadas
        x, y = transformer.transform(latitud, longitud)

        delito_transformado = {
            "Num. caso": num_caso,
            "Coordenadas geográficas": {
                "Latitud": latitud,
                "Longitud": longitud
            },
            "Coordenadas proyectadas": {
                "X": x,
                "Y": y
            }
        }

        delitos_transformados.append(delito_transformado)

    return delitos_transformados

# Función que transforma las coordenadas comisarias de sistema geográficas a coordenadas proyectadas.
def convertir_coordenadas_comisarias():
    comisarias_transformadas = []
    ubicaciones_comisarias = mysql_consultas_datos.coordenadas_comisarias()
    
    sistema_referencia_origen = "EPSG:4326"     # Sistema geográfico.
    sistema_referencia_destino = "EPSG:26916"   # Sistema proyectado.
    transformer = Transformer.from_crs(sistema_referencia_origen, sistema_referencia_destino)

    for comisaria in ubicaciones_comisarias:
        latitud, longitud, nombre = comisaria
              
        # Transformar las coordenadas
        x, y = transformer.transform(latitud, longitud)
        
        # Crear el diccionario transformado
        comisaria_transformada = {
            "Nombre del Distrito": nombre,
            "Coordenadas geográficas": {
                "Latitud": latitud,
                "Longitud": longitud
            },
            "Coordenadas proyectadas": {
                "X": x,
                "Y": y
            }
        }
        
        # Agregar el diccionario transformado a la lista
        comisarias_transformadas.append(comisaria_transformada)
    
    
    return comisarias_transformadas

# Función para calcular la distancia entre dos puntos.
def calcular_distancia(punto1, punto2):
    return np.sqrt((punto1['X'] - punto2['X'])**2 + (punto1['Y'] - punto2['Y'])**2)

# Función para ncontrar la comisaría más cercana a cada delito y guardar esa comisaria en la información del delito.
def encontrar_comisaria_mas_cercana():
    delitos_transformados = convertir_coordenadas_delitos()
    comisarias_transformadas = convertir_coordenadas_comisarias()
    resultados = []

    for delito in delitos_transformados:
        coordenadas_delito = delito['Coordenadas proyectadas']
        distancia_minima = float('inf')
        comisaria_cercana = None

        for comisaria in comisarias_transformadas:
            coordenadas_comisaria = comisaria['Coordenadas proyectadas']
            distancia = calcular_distancia(coordenadas_delito, coordenadas_comisaria)

            if distancia < distancia_minima:
                distancia_minima = distancia
                comisaria_cercana = comisaria

        if distancia_minima < 1000:
            distancia = f"{distancia_minima:.2f} metros"
        else:
            distancia = f"{distancia_minima / 1000:.2f} kilómetros"

        resultados.append({
            "Num. caso": delito["Num. caso"],
            "Coordenadas geográficas": delito["Coordenadas geográficas"],
            "Coordenadas proyectadas": delito["Coordenadas proyectadas"],
            "Comisaria más cercana": comisaria_cercana["Nombre del Distrito"],
            "Distancia a la comisaria más cercana": distancia
        })

    # Mostramos los delitos y la comisaría más cercana
    for delito in resultados:
        print(f"Núm. caso del delito: {delito['Num. caso']}")
        print(f" - Comisaría más cercana al delito: {delito['Comisaria más cercana']}")
        print(f" - Distancia entre el delito cometido y la comisaría: {delito['Distancia a la comisaria más cercana']}")

# ---------------------------------------- LLAMAMOS A MAIN -------------------------------------------

# LLamamos a main. La función main() la hemos definido para establecer un menú con el que pueda interactuar el usuario "Agente de Policía".
main()

# ---------------------------------------- FIN DEL PROGRAMA -------------------------------------------