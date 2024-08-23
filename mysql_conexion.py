import mysql.connector

# Función para conectar con la base de datos
def crear_conexion_bd():
    try: 
        conexion=mysql.connector.connect(
        user='root',
        password='',
        host='localhost',
        database='chicago_safety_data',
        port='3306')
        return conexion
    except: print("Se ha producido un error al establecer conexión con la base de datos.")