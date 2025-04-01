import mysql.connector
from datetime import date

def guardar_datos(nombre, precio, variacion, porcentaje):
    """
    Guarda el nombre del índice, su precio, la variación en puntos
    y la variación porcentual en la base de datos MySQL.
    """
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",  # Cambia esto si tu usuario de MySQL es otro
            password="",  # Añade la contraseña si la tienes
            database="bolsa"
        )
        cursor = conexion.cursor()

        consulta = "INSERT INTO ibex35 (fecha, nombre, precio, variacion, porcentaje) VALUES (%s, %s, %s, %s, %s)"
        valores = (
            date.today(),
            nombre,
            float(precio.replace('.', '').replace(',', '.')),  # Convierte el precio a decimal
            variacion.replace(',', '.'),  # Mantiene el signo y corrige el formato
            porcentaje.replace(',', '.')  # Mantiene el signo y el %
        )

        cursor.execute(consulta, valores)
        conexion.commit()

        print("Datos guardados correctamente en MySQL.")

    except mysql.connector.Error as error:
        print(f"Error al guardar en MySQL: {error}")

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

