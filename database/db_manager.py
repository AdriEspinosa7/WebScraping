import mysql.connector
from datetime import datetime
from utils.log_utils import log_info, log_error

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
# Crear tabla 'indices' si no existe
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
# Verificar si ya existe un registro ese día para un índice concreto
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
# Guardar datos de un índice bursátil
# ========================
def guardar_datos(nombre, precio, variacion, porcentaje, fecha_hora):
    if existe_registro(nombre):
        log_info(f"📛 Ya existe un registro para '{nombre}' en la fecha actual. No se insertó.")
        return False

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
        return True
    except mysql.connector.Error as error:
        log_error(f"❌ Error al guardar en MySQL: {error}")
        return False
    finally:
        cursor.close()
        conexion.close()

# ========================
# Guardar datos anuales de empresas cotizadas (BME)
# ========================
def insertar_datos_empresa(datos):
    conexion = conectar()
    cursor = conexion.cursor()

    # Verificación previa: evitar duplicados exactos
    consulta_check = """
        SELECT COUNT(*) FROM datos_empresas WHERE 
            empresa = %s AND anio = %s AND capitalizacion = %s AND num_acciones = %s AND 
            precio_cierre = %s AND ultimo_precio = %s AND precio_max = %s AND precio_min = %s AND 
            volumen = %s AND efectivo = %s
    """
    valores_check = (
        datos["empresa"], datos["anio"], datos["capitalizacion"], datos["num_acciones"],
        datos["precio_cierre"], datos["ultimo_precio"], datos["precio_max"], datos["precio_min"],
        datos["volumen"], datos["efectivo"]
    )

    try:
        cursor.execute(consulta_check, valores_check)
        if cursor.fetchone()[0] > 0:
            log_info(f"📛 Registro duplicado: {datos['empresa']} - {datos['anio']}. No se insertó.")
            return False

        consulta = """
            INSERT INTO datos_empresas (
                empresa, anio, capitalizacion, num_acciones,
                precio_cierre, ultimo_precio, precio_max,
                precio_min, volumen, efectivo, fecha_registro
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                capitalizacion = VALUES(capitalizacion),
                num_acciones = VALUES(num_acciones),
                precio_cierre = VALUES(precio_cierre),
                ultimo_precio = VALUES(ultimo_precio),
                precio_max = VALUES(precio_max),
                precio_min = VALUES(precio_min),
                volumen = VALUES(volumen),
                efectivo = VALUES(efectivo)
        """

        valores = (
            datos["empresa"], datos["anio"], datos["capitalizacion"], datos["num_acciones"],
            datos["precio_cierre"], datos["ultimo_precio"], datos["precio_max"],
            datos["precio_min"], datos["volumen"], datos["efectivo"], datos["fecha_registro"]
        )

        cursor.execute(consulta, valores)
        conexion.commit()
        log_info(f"📥 Insertado/actualizado: {datos['empresa']} - {datos['anio']}")
        return True

    except mysql.connector.Error as error:
        log_error(f"❌ Error al insertar datos de empresa: {error}")
        return False

    finally:
        cursor.close()
        conexion.close()

# ========================
# Guardar datos de composición del IBEX 35
# ========================
def insertar_datos_composicion(datos):
    """
    Inserta o actualiza la composición del IBEX 35,
    guardando también el nombre del PDF fuente para evitar duplicados.
    """
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        consulta = """
            INSERT INTO composicion_ibex35 (
                simbolo, nombre, titulos_antes, estatus,
                modificaciones, comp, coef_ff, fecha_insercion,
                nombre_pdf
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            ON DUPLICATE KEY UPDATE
              titulos_antes  = VALUES(titulos_antes),
              estatus        = VALUES(estatus),
              modificaciones = VALUES(modificaciones),
              comp           = VALUES(comp),
              coef_ff        = VALUES(coef_ff),
              -- si vuelve a procesar el mismo PDF, volvemos a escribirlo
              nombre_pdf     = VALUES(nombre_pdf)
        """
        valores = (
            datos.get("simbolo", ""),
            datos.get("nombre", ""),
            datos.get("titulos_antes", ""),
            datos.get("estatus", ""),
            datos.get("modificaciones", ""),
            datos.get("comp", ""),
            datos.get("coef_ff", ""),
            datos.get("fecha_insercion", ""),
            datos.get("nombre_pdf", "")
        )
        cursor.execute(consulta, valores)
        conexion.commit()
        log_info(f"📥 Insertado/actualizado: {datos.get('simbolo', '')} – {datos.get('nombre', '')} (PDF: {datos.get('nombre_pdf')})")
        return True
    except mysql.connector.Error as error:
        log_error(f"❌ Error al insertar datos de composición: {error}")
        return False
    finally:
        cursor.close()
        conexion.close()


# ========================
# Inicialización al importar módulo
# ========================
crear_base_datos_si_no_existe()
crear_tabla_si_no_existe()












