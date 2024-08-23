import mysql.connector
import mysql_conexion

# Creación base de datos
""" conexion = mysql.connector.connect(host = "localhost", user = "root", password = "")
cursor = conexion.cursor()
cursor.execute("CREATE DATABASE chicago_safety_data;")  """


# FUNCIÓN PARA CREAR TABLAS
def crear_tablas():
    conexion = mysql_conexion.crear_conexion_bd()
    cursor = conexion.cursor()

    # Tabla 'areas_comunitarias' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS areas_comunitarias (
            id_area_comunitaria INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            año YEAR NOT NULL,
            poblacion INT,
            ingresos FLOAT,
            latinos FLOAT,
            negros FLOAT,
            blancos FLOAT,
            asiaticos FLOAT,
            otros FLOAT
        );
    ''')

    # Create 'comisarias' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comisarias (
            id_comisaria INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            area_comunitaria INT,
            direccion VARCHAR(255),
            telefono VARCHAR(20),
            latitud FLOAT,
            longitud FLOAT,
            FOREIGN KEY (area_comunitaria) REFERENCES areas_comunitarias(id_area_comunitaria)
        );
    ''')

    # Create 'hospitales' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hospitales (
            id_hospital INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            area_comunitaria INT,
            direccion VARCHAR(255),
            telefono VARCHAR(20),
            latitud FLOAT,
            longitud FLOAT,
            FOREIGN KEY (area_comunitaria) REFERENCES areas_comunitarias(id_area_comunitaria)
        );
    ''')

    # Create 'delitos' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS delitos (
            id_delito INT AUTO_INCREMENT PRIMARY KEY,
            num_caso VARCHAR(255) NOT NULL,
            descripcion TEXT,
            arrestado BOOLEAN,
            area_comunitaria INT,
            cuadra VARCHAR(255),
            fecha DATETIME,
            latitud FLOAT,
            longitud FLOAT,
            FOREIGN KEY (area_comunitaria) REFERENCES areas_comunitarias(id_area_comunitaria)
        );
    ''')

    conexion.commit()
    cursor.close()
    conexion.close()

if __name__ == "__main__":
   crear_tablas()