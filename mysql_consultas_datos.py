import mysql.connector
from pyproj import Transformer
import mysql_conexion
import mysql_validaciones

# Función consulta delitos
def buscar_delitos_por_valor():
    # Solicitar al usuario el valor de búsqueda
    valor = input("Introduce el valor a buscar: ")

    try:
        conexion = mysql_conexion.crear_conexion_bd()
        cursor = conexion.cursor()

        # Consulta SQL para buscar delitos que coincidan con el valor proporcionado en cualquier campo
        consulta = '''
            SELECT * FROM delitos
            WHERE num_caso LIKE %s
            OR descripcion LIKE %s
            OR cuadra LIKE %s
            OR fecha LIKE %s
            OR latitud LIKE %s
            OR longitud LIKE %s
        '''

        # Agrega comodines para buscar coincidencias parciales
        valor_busqueda = '%' + valor + '%'

        # Ejecutar la consulta con el mismo valor de búsqueda aplicado a todos los campos
        cursor.execute(consulta, (valor_busqueda, valor_busqueda, valor_busqueda, valor_busqueda, valor_busqueda, valor_busqueda))

        # Obtener resultados de la consulta
        resultados = cursor.fetchall()

        # Imprimir los resultados
        if resultados:
            print("\nSe encontraron los siguientes delitos:")
            for resultado in resultados:
                print(f"""
                Número de caso: {resultado[1]}
                Descripción: {resultado[2]}
                Arrestado: {resultado[3]}
                Área comunitaria: {resultado[4]}
                Cuadra: {resultado[5]}
                Fecha: {resultado[6]}
                Latitud: {resultado[7]}
                Longitud: {resultado[8]}
                """)
        else:
            print("\nNo se encontraron delitos que coincidan con el valor proporcionado.\n")

    except mysql.connector.Error as error:
        print("\nError al conectar a la base de datos:", error)

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

# Función mostrar delitos
def mostrar_todos_los_delitos():
    try:
        conexion = mysql_conexion.crear_conexion_bd()
        cursor = conexion.cursor()

        # Consulta SQL para obtener todos los delitos
        consulta = '''
            SELECT * FROM delitos
        '''

        # Ejecutar la consulta
        cursor.execute(consulta)

        # Obtener resultados de la consulta
        resultados = cursor.fetchall()

        # Imprimir los resultados
        if resultados:
            print("Listado de todos los delitos:")
            for resultado in resultados:
                print(f"""
                Número de caso: {resultado[1]}
                Descripción: {resultado[2]}
                Arrestado: {resultado[3]}
                Área comunitaria: {resultado[4]}
                Cuadra: {resultado[5]}
                Fecha: {resultado[6]}
                Latitud: {resultado[7]}
                Longitud: {resultado[8]}
                """)
        else:
            print("\nNo se encontraron delitos en la base de datos.\n")

    except mysql.connector.Error as error:
        print("Error al conectar a la base de datos:", error)

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

# Función para editar un delito
def editar_delito():
    try:
        conexion = mysql_conexion.crear_conexion_bd()
        cursor = conexion.cursor()

        # Pedir al usuario el número de caso del delito a editar
        num_caso = input("Ingrese el número de caso del delito que desea editar: ")

        # Verificar si el delito existe en la base de datos
        consulta_existencia = "SELECT * FROM delitos WHERE num_caso = %s"
        cursor.execute(consulta_existencia, (num_caso,))
        delito = cursor.fetchone()

        if not delito:
            print("El delito con el número de caso especificado no existe.")
            return

        # Pedir al usuario el parámetro a editar
        print("Seleccione el parámetro que desea editar:")
        print("1. Descripción")
        print("2. Arrestado")
        print("3. Área comunitaria")
        print("4. Cuadra")
        print("5. Fecha")
        print("6. Latitud")
        print("7. Longitud")
        opcion = int(input("Ingrese el número correspondiente al parámetro: "))

        # Pedir al usuario el nuevo valor para el parámetro seleccionado
        if opcion == 2:  # Si se selecciona el parámetro "Arrestado"
            print("Ingrese el nuevo valor para el parámetro seleccionado: ")
            nuevo_valor = mysql_validaciones.criminal_arrestado()
            # Convertir el valor a un booleano apropiado
            #nuevo_valor = nuevo_valor == "true"
        elif opcion == 3:
            print("Ingrese el nuevo valor para el parámetro seleccionado: ")
            nuevo_valor = mysql_validaciones.elegir_area_comunitaria()
        elif opcion == 5:
            print("Ingrese el nuevo valor para el parámetro seleccionado: ")
            nuevo_valor = mysql_validaciones.validar_fecha()
        elif opcion == 6:
            print("Ingrese el nuevo valor para el parámetro seleccionado: ")
            nuevo_valor = mysql_validaciones.validar_float("Latitud")
        elif opcion == 7:
            print("Ingrese el nuevo valor para el parámetro seleccionado: ")
            nuevo_valor = mysql_validaciones.validar_float("Longitud")
        else:
            nuevo_valor = input("Ingrese el nuevo valor para el parámetro seleccionado: ")

        # Actualizar el delito en la base de datos según el parámetro seleccionado
        campos = ["descripcion", "arrestado", "area_comunitaria", "cuadra", "fecha", "latitud", "longitud"]
        campo_actualizar = campos[opcion - 1]

        consulta_actualizacion = f"UPDATE delitos SET {campo_actualizar} = %s WHERE num_caso = %s"
        cursor.execute(consulta_actualizacion, (nuevo_valor, num_caso))
        conexion.commit()

        print("El delito ha sido actualizado correctamente.")

    except mysql.connector.Error as error:
        print("Error al conectar a la base de datos:", error)

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

# Función para listar comisarias
def mostrar_todas_las_comisarias():
    try:
        conexion = mysql_conexion.crear_conexion_bd()
        cursor = conexion.cursor()

        # Consulta SQL para seleccionar todas las comisarías
        consulta = "SELECT * FROM comisarias"
        cursor.execute(consulta)

        # Obtener todas las filas de resultados
        comisarias = cursor.fetchall()

        if not comisarias:
            print("No hay comisarías registradas en la base de datos.")
        else:
            # Imprimir información de todas las comisarías
            print("Lista de Comisarías:")
            for comisaria in comisarias:
                print(f"""
                Nombre: {comisaria[1]}
                Área Comunitaria: {comisaria[2]}
                Dirección: {comisaria[3]}
                Teléfono: {comisaria[4]}
                Latitud: {comisaria[5]}
                Longitud: {comisaria[6]}
                """)
               

    except mysql.connector.Error as error:
        print("Error al conectar a la base de datos:", error)

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
   
# Función para listar hospitales
def mostrar_todos_los_hospitales():
    try:
        conexion = mysql_conexion.crear_conexion_bd()
        cursor = conexion.cursor()

        # Consulta SQL para seleccionar todos los hospitales
        consulta = "SELECT * FROM hospitales"
        cursor.execute(consulta)

        # Obtener todas las filas de resultados
        hospitales = cursor.fetchall()

        if not hospitales:
            print("No hay hospitales registrados en la base de datos.")
        else:
            # Imprimir información de todos los hospitales
            print("Lista de Hospitales:")
            for hospital in hospitales:
                print(f"""
                Nombre: {hospital[1]}
                Área Comunitaria: {hospital[2]}
                Dirección: {hospital[3]}
                Teléfono: {hospital[4]}
                Latitud: {hospital[5]}
                Longitud: {hospital[6]}
                """)               

    except mysql.connector.Error as error:
        print("Error al conectar a la base de datos:", error)

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

# Función para listar todas las áreas comunitarias
def mostrar_areas_comunitarias():
    try:
        conexion = mysql_conexion.crear_conexion_bd()
        cursor = conexion.cursor()

        # Consulta SQL para seleccionar todas las áreas comunitarias
        consulta = "SELECT * FROM areas_comunitarias"
        cursor.execute(consulta)

        # Obtener todas las filas de resultados
        areas_comunitarias = cursor.fetchall()

        if not areas_comunitarias:
            print("No hay áreas comunitarias registradas en la base de datos.")
        else:
            # Imprimir información de todas las áreas comunitarias
            print("Lista de Áreas Comunitarias:")
            for area_comunitaria in areas_comunitarias:
                print(f"""
                Nombre: {area_comunitaria[1]}
                AÑo: {area_comunitaria[2]}
                Pobalción: {area_comunitaria[3]}
                Ingresos: {area_comunitaria[4]}
                Latinos: {area_comunitaria[5]}
                Negros: {area_comunitaria[6]}
                Blancos: {area_comunitaria[6]}
                Asiáticos: {area_comunitaria[6]}
                Otros: {area_comunitaria[6]}
                """)                

    except mysql.connector.Error as error:
        print("Error al conectar a la base de datos:", error)

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

# Función para buscar coordenadas comisarias
def coordenadas_comisarias():
    ubicaciones_comisarias = []
    
    try:
        conexion = mysql_conexion.crear_conexion_bd()
        cursor = conexion.cursor()

        # Consulta SQL para seleccionar todas las comisarías
        consulta = "SELECT nombre, latitud, longitud FROM comisarias"
        cursor.execute(consulta)

        # Obtener todas las filas de resultados
        comisarias = cursor.fetchall()

        if not comisarias:
            print("No hay comisarías registradas en la base de datos.")
        else:
            # Obtener ubicaciones de todas las comisarías
            for comisaria in comisarias:
                nombre, latitud, longitud = comisaria
                ubicaciones_comisarias.append((float(latitud), float(longitud), nombre))

    except mysql.connector.Error as error:
        print("Error al conectar a la base de datos:", error)

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
    
    return ubicaciones_comisarias

# Función para buscar coordenadas de delitos
def coordenadas_delitos():
    ubicaciones_delitos = []

    try:
        conexion = mysql_conexion.crear_conexion_bd()
        cursor = conexion.cursor()

        # Consulta SQL para obtener todos los delitos
        consulta = '''
            SELECT num_caso, latitud, longitud FROM delitos
        '''
        cursor.execute(consulta)

        # Obtener resultados de la consulta
        delitos = cursor.fetchall()

        if delitos:
            for delito in delitos:
                num_caso, latitud, longitud = delito
                if latitud and longitud:  # Verificar que latitud y longitud no sean nulos
                    ubicaciones_delitos.append((float(latitud), float(longitud), num_caso))

    except mysql.connector.Error as error:
        print("Error al conectar a la base de datos:", error)

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

    return ubicaciones_delitos

# Función para ordenar delitos de manera ascendente
def mostrar_delitos_asc():
    try:
        conexion = mysql_conexion.crear_conexion_bd()
        cursor = conexion.cursor()

        # Consulta SQL para obtener todos los delitos ordenados por fecha de manera ascendente
        consulta = '''
            SELECT * FROM delitos
            ORDER BY fecha ASC
        '''

        # Ejecutar la consulta
        cursor.execute(consulta)

        # Obtener resultados de la consulta
        resultados = cursor.fetchall()

        # Imprimir los resultados
        if resultados:
            print("Listado de todos los delitos ordenados por fecha de manera ascendente:")
            for resultado in resultados:
                print(f"""
                Número de caso: {resultado[1]}
                Descripción: {resultado[2]}
                Arrestado: {resultado[3]}
                Área comunitaria: {resultado[4]}
                Cuadra: {resultado[5]}
                Fecha: {resultado[6]}
                Latitud: {resultado[7]}
                Longitud: {resultado[8]}
                """)
        else:
            print("\nNo se encontraron delitos en la base de datos.\n")

    except mysql.connector.Error as error:
        print("Error al conectar a la base de datos:", error)

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

# Función para ordenar delitos de manera descendente
def mostrar_delitos_desc():
    try:
        conexion = mysql_conexion.crear_conexion_bd()
        cursor = conexion.cursor()

        # Consulta SQL para obtener todos los delitos ordenados por fecha de manera ascendente
        consulta = '''
            SELECT * FROM delitos
            ORDER BY fecha DESC
        '''

        # Ejecutar la consulta
        cursor.execute(consulta)

        # Obtener resultados de la consulta
        resultados = cursor.fetchall()

        # Imprimir los resultados
        if resultados:
            print("Listado de todos los delitos ordenados por fecha de manera ascendente:")
            for resultado in resultados:
                print(f"""
                Número de caso: {resultado[1]}
                Descripción: {resultado[2]}
                Arrestado: {resultado[3]}
                Área comunitaria: {resultado[4]}
                Cuadra: {resultado[5]}
                Fecha: {resultado[6]}
                Latitud: {resultado[7]}
                Longitud: {resultado[8]}
                """)
        else:
            print("\nNo se encontraron delitos en la base de datos.\n")

    except mysql.connector.Error as error:
        print("Error al conectar a la base de datos:", error)

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

# Función para devolver orden asc para calculo tiempo entre delitos
def delitos_asc_retorno():
    try:
        conexion = mysql_conexion.crear_conexion_bd()
        cursor = conexion.cursor()

        # Consulta SQL para obtener todos los delitos ordenados por fecha de manera ascendente
        consulta = '''
            SELECT * FROM delitos
            ORDER BY fecha ASC
        '''

        # Ejecutar la consulta
        cursor.execute(consulta)

        # Obtener resultados de la consulta
        resultados = cursor.fetchall()

        # Lista para almacenar los resultados como diccionarios
        lista_delitos = []

        # Verificar si se encontraron resultados
        if resultados:
            for resultado in resultados:
                # Crear un diccionario para cada delito
                delito = {
                    "Núm. caso": resultado[1],
                    "Descripción": resultado[2],
                    "Arrestado": resultado[3],
                    "Área comunitaria": resultado[4],
                    "Cuadra": resultado[5],
                    "Fecha": resultado[6],
                    "Latitud": resultado[7],
                    "Longitud": resultado[8]
                }
                lista_delitos.append(delito)

        return lista_delitos

    except mysql.connector.Error as error:
        print("Error al conectar a la base de datos:", error)
        return []

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()



#if __name__ == "__main__":
    #editar_delito()
    #buscar_delitos_por_valor()
    #coordenadas_delitos()
    