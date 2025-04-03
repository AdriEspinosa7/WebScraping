import mysql.connector
from datetime import date

def guardar_datos(nombre, precio, variacion, porcentaje):
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bolsa"
        )
        cursor = conexion.cursor()

        consulta = "INSERT INTO indices (fecha, nombre, precio, variacion, porcentaje) VALUES (%s, %s, %s, %s, %s)"
        valores = (date.today(), nombre, float(precio), variacion, porcentaje)

        print("Ejecutando consulta:", consulta)  # Para ver la consulta antes de ejecutarla
        cursor.execute(consulta, valores)
        conexion.commit()

        print(f"Datos guardados correctamente: {nombre} - {precio} - {variacion} - {porcentaje}")

    except mysql.connector.Error as error:
        print(f"❌ Error al guardar en MySQL: {error}")

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

