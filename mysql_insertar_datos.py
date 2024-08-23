import mysql.connector
from datetime import datetime
import mysql_conexion
import mysql_validaciones


# Datos simulados para áreas comunitarias
areas_comunitarias_data = [
    ('Albany Park', 2023, 51361, 34350.45, 32.1, 9.4, 33.3, 19.3, 5.9),
    ('Archer Heights', 2023, 13142, 29550.78, 61.2, 2.3, 31.6, 2.8, 1.3),
    ('Auburn Gresham', 2023, 48567, 26500.60, 95.5, 1.2, 2.8, 0.3, 0.2),
    ('New City', 2023, 32894, 32000.20, 50.3, 46.8, 1.5, 1.2, 0.2),
    ('Near North Side', 2023, 75628, 72000.40, 20.2, 45.6, 30.8, 2.9, 0.5),
    ('Lower West Side', 2023, 24569, 31000.80, 65.7, 6.5, 24.8, 2.0, 0.5),
    ('Loop', 2023, 10345, 95000.70, 15.3, 60.5, 20.0, 3.5, 0.7),
    ('Oakland', 2023, 8790, 42000.90, 25.6, 70.3, 2.8, 1.0, 0.3),
    ('Lincoln Park', 2023, 64521, 62000.10, 10.2, 80.5, 7.8, 1.3, 0.2),
    ('Uptown', 2023, 49876, 39000.50, 15.8, 50.4, 30.5, 3.1, 0.2)
]

# Datos simulados para comisarías
comisarias_data = [
    ('Comisaría Central', 1, '123 Main St', '312-555-1234', 41.8781, -87.6298),  
    ('Comisaría Norte', 2, '456 Elm St', '312-555-5678', 41.8837, -87.6303),
    ('Comisaría Sur', 3, '789 Oak St', '312-555-9012', 41.8994, -87.6245),  
    ('Comisaría Oeste', 4, '101 Pine St', '312-555-3456', 41.8947, -87.6321)  
    # Agrega más datos simulados según sea necesario
]

# Datos simulados para hospitales
hospitales_data = [
    ('Hospital General', 3, '789 Oak St', '312-555-9012', 41.8917, -87.6076),  
    ('Hospital Pediátrico', 4, '901 Pine St', '312-555-3456', 41.8784, -87.6245),    
    # Agrega más datos simulados según sea necesario
]

# Datos simulados para delitos
delitos_data = [
    ('HY411595', 'Tráfico de drogas', True, 2, '035XX W BARRY AVE', '2015-09-05 13:30:00', 41.9384, -87.7000),  
    ('HY411435', 'Robo en casa', False, 7, '082XX S LOOMIS BLVD', '2015-09-06 10:55:00', 41.7444, -87.6576),  
    ('HY411648', 'Maltrato doméstico', False, 6, '043XX S WOOD ST', '2015-09-07 13:30:00', 41.8151, -87.6700),  
    ('HY411649', 'Robo a mano armada', True, 1, '500 Block of N Michigan Ave', '2015-09-08 13:30:00', 41.8914, -87.6243),  
    ('HY411650', 'Robo de vehículo', False, 10, '700 Block of W 19th St', '2015-09-09 13:30:00', 41.8551, -87.6657),  
    ('HY411651', 'Asalto', True, 5, '200 E Randolph St', '2015-09-10 13:30:00', 41.8841, -87.6215),  
    ('HY411652', 'Hurto', False, 4, '100 N State St', '2015-09-11 13:30:00', 41.8837, -87.6279),  
    ('HY411653', 'Atraco', True, 8, '2301 S Lake Shore Dr', '2015-09-12 13:30:00', 41.8535, -87.6096),  
    ('HY411654', 'Robo de Identidad', False, 3, '800 N Kedzie Ave', '2015-09-13 13:30:00', 41.8959, -87.7065),  
    ('HY411655', 'Fraude', True, 9, '1500 N Clybourn Ave', '2015-09-14 13:30:00', 41.9094, -87.6557),
    ('HY411656', 'Robo de vehículo', False, 10, '4800 N Broadway', '2015-09-15 13:30:00', 41.9698, -87.6596)    
    # Agrega más datos simulados según sea necesario
]

# Función para insertar datos en las tablas
def insertar_datos():
    try:
        conexion = mysql_conexion.crear_conexion_bd()
        cursor = conexion.cursor()

        # Insertar datos en areas_comunitarias
        cursor.executemany('''
            INSERT INTO areas_comunitarias (nombre, año, poblacion, ingresos, latinos, negros, blancos, asiaticos, otros)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', areas_comunitarias_data)

        # Insertar datos en comisarias
        cursor.executemany('''
            INSERT INTO comisarias (nombre, area_comunitaria, direccion, telefono, latitud, longitud)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', comisarias_data)

        # Insertar datos en hospitales
        cursor.executemany('''
            INSERT INTO hospitales (nombre, area_comunitaria, direccion, telefono, latitud, longitud)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', hospitales_data)

        # Insertar datos en delitos
        cursor.executemany('''
            INSERT INTO delitos (num_caso, descripcion, arrestado, area_comunitaria, cuadra, fecha, latitud, longitud)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', delitos_data)

        conexion.commit()
        cursor.close()
        conexion.close()
        print("Datos agregados a la base de datos.")

    except: print("No se han podido insertar los datos.")


# ------------------------------------- FUNCIONES PARA INSRTAR DATOS POR USUARIO ----------------------------- #

""" # Desactivada Función para insertar Area comunitaria
def insertar_area_comunitaria():
    # Solicitar datos al usuario
    nombre = input("Nombre del área comunitaria: ")
    año = input("Año: ")
    poblacion = input("Población: ")
    ingresos = input("Ingresos medios: ")
    latinos = input("Índice de personas latinas: ")
    negros = input("Índice de personas negras: ")
    blancos = input("Índice de personas blancas: ")
    asiaticos = input("Índice de personas asiáticas: ")
    otros = input("Índice de personas de otra raza: ")

    # Conectar a la base de datos
    conexion = mysql_conexion.crear_conexion_bd()
    cursor = conexion.cursor()

    # Insertar los datos en la tabla areas_comunitarias
    cursor.execute('''
        INSERT INTO areas_comunitarias (nombre, año, poblacion, ingresos, latinos, negros, blancos, asiaticos, otros)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (nombre, año, poblacion, ingresos, latinos, negros, blancos, asiaticos, otros))

    # Confirmar cambios y cerrar la conexión
    conexion.commit()
    cursor.close()
    conexion.close() """

#Función para insertar Comisaria
def agregar_comisaria():
    try:
        # Solicitar datos al usuario
        nombre = input("Nombre de la Comisaria: ")
        if mysql_validaciones.comprobar_existencia_registro("comisarias","nombre", nombre) == True:
            print("Esta comisaría ya está en la base de datos.")
            return
        area_comunitaria = mysql_validaciones.elegir_area_comunitaria()
        direccion = input("Dirección: ")
        telefono = mysql_validaciones.validar_telefono()
        latitud = mysql_validaciones.validar_float("Latitud")
        longitud = mysql_validaciones.validar_float("Longitud")

        # Conectar a la base de datos
        conexion = mysql_conexion.crear_conexion_bd()
        cursor = conexion.cursor()

        # Insertar los datos en la tabla comisarias
        cursor.execute('''
            INSERT INTO comisarias (nombre, area_comunitaria, direccion, telefono, latitud, longitud)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (nombre, area_comunitaria, direccion, telefono, latitud, longitud))

        # Confirmar cambios y cerrar la conexión
        conexion.commit()
        cursor.close()
        conexion.close()
        print("Nueva comisaría agregada a la base de datos.")

    except: print("No se ha podido insertar la comisaría.")

#Función para insertar Hospital
def agregar_hospital():
    try:
        # Solicitar datos al usuario
        nombre = input("Nombre del hospital: ")
        if mysql_validaciones.comprobar_existencia_registro("hospitales","nombre", nombre) == True:
            print("Este hospital ya está en la base de datos.")
            return
        area_comunitaria = mysql_validaciones.elegir_area_comunitaria()
        direccion = input("Dirección: ")
        telefono = mysql_validaciones.validar_telefono()
        latitud = mysql_validaciones.validar_float("Latitud")
        longitud = mysql_validaciones.validar_float("Longitud")

        # Conectar a la base de datos
        conexion = mysql_conexion.crear_conexion_bd()
        cursor = conexion.cursor()

        # Insertar los datos en la tabla hospitales
        cursor.execute('''
            INSERT INTO hospitales (nombre, area_comunitaria, direccion, telefono, latitud, longitud)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (nombre, area_comunitaria, direccion, telefono, latitud, longitud))

        # Confirmar cambios y cerrar la conexión
        conexion.commit()
        cursor.close()
        conexion.close()
        print("Nuevo hospital agregado a la base de datos.")

    except: print("No se ha podido insertar el hospital.")

#Función para insertar Delito
def agregar_delito():
    try:
        # Solicitar datos al usuario
        num_caso = input("Número caso: ")
        if mysql_validaciones.comprobar_existencia_registro("delitos","num_caso", num_caso) == True:
            print("Este delito ya está en la base de datos.")
            return
        descripcion = input("Descripción: ")
        arrestado = mysql_validaciones.criminal_arrestado()
        area_comunitaria = mysql_validaciones.elegir_area_comunitaria()
        cuadra = input("Cuadra: ")
        fecha_str = mysql_validaciones.validar_fecha()
        latitud = mysql_validaciones.validar_float("Latitud")
        longitud = mysql_validaciones.validar_float("Longitud")

        # Convertir la cadena de fecha a un objeto datetime
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')

        # Conectar a la base de datos
        conexion = mysql_conexion.crear_conexion_bd()
        cursor = conexion.cursor()

        # Insertar los datos en la tabla delitos
        cursor.execute('''
            INSERT INTO delitos (num_caso, descripcion, arrestado, area_comunitaria, cuadra, fecha, latitud, longitud)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (num_caso, descripcion, arrestado, area_comunitaria, cuadra, fecha, latitud, longitud))

        # Confirmar cambios y cerrar la conexión
        conexion.commit()
        cursor.close()
        conexion.close()
        print("Nuevo delito agregado a la base de datos.")

    except: print("No se ha podido insertar el delito.")


if __name__ == "__main__":
    insertar_datos()