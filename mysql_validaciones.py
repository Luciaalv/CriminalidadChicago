import mysql_conexion
from datetime import datetime
import re

# Función para saber si un registro existe ya en la base de datos
def comprobar_existencia_registro(tabla, columna, valor):
    try:
        conexion = mysql_conexion.crear_conexion_bd()
        cursor = conexion.cursor()
        #Consulta que devuelve el número de delitos existentes con el mismo valor
        query = f'SELECT COUNT(*) FROM `{tabla}` WHERE `{columna}` = "{valor}"';
        cursor.execute(query)
        #Recuperamos el resultado de la consulta
        total = cursor.fetchone()[0]
        conexion.close()
        #Si ya hay algún resultado en la bd, se retorna True. De lo contrario, False.
        if total > 0:
            return True
        else: return False
    except: print("Se ha producido un error al recuperar información de la base de datos.")

    
# Función para comprobar si hay registros ya introducidos en la tabla x de la base de datos
def tabla_vacia(tabla):
    try:
        conexion = mysql_conexion.crear_conexion_bd()
        cursor = conexion.cursor()
        #Consulta que devuelve el número de registros existentes en la base de datos
        query = f'SELECT COUNT(*) FROM {tabla}'
        cursor.execute(query)
        #Recuperamos el resultado de la consulta
        total = cursor.fetchone()[0]
        conexion.close()
        #Si no hay ningún resultado en la bd, se retorna True. De lo contrario, False.
        if total < 1:
            return True
        else: return False
    except: print("Se ha producido un error al recuperar información de la base de datos.")


# Función para comprobar que el valor introducido en los campos latitud y longitud es numérico
def validar_float(dato):
    while True:
        try:
            valor = float(input(f"{dato}: "))
            return valor
        except: print("Debes introducir un número válido.")

# Función para comprobar que se introduce la fecha en el formato adecuado
def validar_fecha():
    while True:
        try:
            fecha = input("Fecha (YYYY-MM-DD HH:MM:SS): ")
            if fecha == datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S'):
                return fecha
        except: print("Debes introducir la fecha en el formato especificado.")

# Función para comprobar que se introduce el teléfono en el formato adecuado
def validar_telefono():
    regex = re.compile('[0-9]{9}')
    while True:
        try:
            telefono = input("Teléfono: ")
            if regex.match(telefono):
                return telefono
            else: raise TypeError
        except: print("Debes introducir un número de teléfono válido de 9 cifras.")

# Función para cambiar a int el valor introducido por el usuario en el campo de arrestado
def criminal_arrestado():
    valor = ""
    while valor not in ("true", "false"):
        valor = input("¿Arrestado? (True/False): ").strip().lower()
    if valor == 'true':
        return True
    else: return False


# Función para imprimir las opciones de áreas comunitarias y pedir al usuario que elija una
def elegir_area_comunitaria():
    try:
        conexion = mysql_conexion.crear_conexion_bd()
        cursor = conexion.cursor()
        #Consulta que devuelve los datos del área solicitada
        query = f'SELECT id_area_comunitaria, nombre FROM areas_comunitarias'
        cursor.execute(query)
        #Mostramos los nombres y las ids de las áreas y pedimos id al usuario
        if tabla_vacia("areas_comunitarias") == False:
            n_area = ""
            indices = []
            print("Áreas comunitarias: ")
            for area in cursor:
                print(f"{area[0]}: {area[1]}")
                indices.append(area[0])
            #Si el usuario pulsa una tecla incorrecta, vuelve a pedir el número
            while n_area not in indices:
                try:
                    n_area = int(input("Introduce el número del área elegida: "))
                except:
                    print("Debes elegir un número.")
            conexion.close()
            return n_area
        else: print("No hay áreas comunitarias en la base de datos. Añade una para seleccionarla.")
    except: print("Se ha producido un error al elegir el área comunitaria.")