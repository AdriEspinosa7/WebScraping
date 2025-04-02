import mysql.connector
from datetime import date

def guardar_datos(nombre, precio, variacion, porcentaje):
    """
    Guarda los datos en la base de datos MySQL.
    """
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

        cursor.execute(consulta, valores)
        conexion.commit()

        print(f"Datos guardados correctamente: {nombre} - {precio} - {variacion} - {porcentaje}")

    except mysql.connector.Error as error:
        print(f"❌ Error al guardar en MySQL: {error}")

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()


