import mysql.connector
from datetime import date

def guardar_datos(nombre, precio):
    """
    Guarda el nombre del índice y su precio en la base de datos MySQL.
    """
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",  # Mi nombre de usuario
            password="",  # No tengo contraseña
            database="bolsa"
        )
        cursor = conexion.cursor()

        consulta = "INSERT INTO ibex35 (fecha, nombre, precio) VALUES (%s, %s, %s)"
        valores = (date.today(), nombre, float(precio.replace('.', '').replace(',', '.')))

        cursor.execute(consulta, valores)
        conexion.commit()

        print("Datos guardados correctamente en MySQL.")

    except mysql.connector.Error as error:
        print(f"Error al guardar en MySQL: {error}")

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
