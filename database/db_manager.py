import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
from log_utils import log_info, log_error

# ========================
# Configuración de conexión
# ========================
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "bolsa"

# ========================
# Crear base de datos si no existe
# ========================
def crear_base_datos_si_no_existe():
    try:
        conexion = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conexion.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        log_info(f"✅ Base de datos '{DB_NAME}' verificada o creada.")
    except mysql.connector.Error as err:
        log_error(f"❌ Error al crear la base de datos: {err}")
    finally:
        cursor.close()
        conexion.close()

# ========================
# Conexión a la base de datos
# ========================
def conectar():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# ========================
# Crear tabla si no existe
# ========================
def crear_tabla_si_no_existe():
    conexion = conectar()
    cursor = conexion.cursor()

    crear_tabla_sql = """
    CREATE TABLE IF NOT EXISTS indices (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        precio DECIMAL(10, 2) NOT NULL,
        variacion VARCHAR(20) NOT NULL,
        porcentaje VARCHAR(20) NOT NULL,
        fecha_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """

    try:
        cursor.execute(crear_tabla_sql)
        conexion.commit()
        log_info("✅ Tabla 'indices' verificada o creada correctamente.")
    except Exception as e:
        log_error(f"❌ Error al crear/verificar la tabla 'indices': {e}")
    finally:
        cursor.close()
        conexion.close()

# ========================
# Verificar si ya existe un registro ese día
# ========================
def existe_registro(nombre):
    conexion = conectar()
    cursor = conexion.cursor()
    fecha_actual = datetime.now().date()  # Solo la fecha (sin hora)

    try:
        cursor.execute("""
            SELECT COUNT(*) FROM indices 
            WHERE nombre = %s AND DATE(fecha_hora) = %s
        """, (nombre, fecha_actual))
        resultado = cursor.fetchone()
        return resultado[0] > 0
    except mysql.connector.Error as error:
        log_error(f"❌ Error al verificar existencia en MySQL: {error}")
        return False
    finally:
        cursor.close()
        conexion.close()

# ========================
# Guardar datos
# ========================
def guardar_datos(nombre, precio, variacion, porcentaje, fecha_hora):
    if existe_registro(nombre):
        log_info(f"📛 Ya existe un registro para '{nombre}' en la fecha actual. No se insertó.")
        return

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        consulta = """
            INSERT INTO indices (nombre, precio, variacion, porcentaje, fecha_hora)
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (nombre, float(precio), variacion, porcentaje, fecha_hora)
        cursor.execute(consulta, valores)
        conexion.commit()
        log_info(f"📥 Guardado: {nombre} - {precio} - {variacion} - {porcentaje}")
    except mysql.connector.Error as error:
        log_error(f"❌ Error al guardar en MySQL: {error}")
    finally:
        cursor.close()
        conexion.close()

# ========================
# Inicialización
# ========================
crear_base_datos_si_no_existe()
crear_tabla_si_no_existe()





