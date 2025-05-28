import mysql.connector
from datetime import datetime
from utils.log_utils import log_info, log_error
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

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
# Guardar datos de deuda pública
# ========================
def insertar_datos_deuda_publica(lista_datos):
    conexion = None
    cursor = None
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        consulta = """
            INSERT INTO deuda_publica (
                descripcion, isin,
                compra_numero, compra_importe, compra_tir, compra_precio,
                venta_precio, venta_tir, venta_importe, venta_numero,
                ultimo_precio, ultimo_tir, importe_nominal,
                fecha_insercion
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                compra_numero = VALUES(compra_numero),
                compra_importe = VALUES(compra_importe),
                compra_tir = VALUES(compra_tir),
                compra_precio = VALUES(compra_precio),
                venta_precio = VALUES(venta_precio),
                venta_tir = VALUES(venta_tir),
                venta_importe = VALUES(venta_importe),
                venta_numero = VALUES(venta_numero),
                ultimo_precio = VALUES(ultimo_precio),
                ultimo_tir = VALUES(ultimo_tir),
                importe_nominal = VALUES(importe_nominal),
                descripcion = VALUES(descripcion)
        """

        for fila in lista_datos:
            cursor.execute(consulta, (
                fila["descripcion"],
                fila["isin"],
                fila["compra_numero"],
                fila["compra_importe"],
                fila["compra_tir"],
                fila["compra_precio"],
                fila["venta_precio"],
                fila["venta_tir"],
                fila["venta_importe"],
                fila["venta_numero"],
                fila["ultimo_precio"],
                fila["ultimo_tir"],
                fila["importe_nominal"],
                fila["fecha_insercion"]
            ))

        conexion.commit()
        log_info(f"📥 {len(lista_datos)} registros de deuda pública insertados correctamente.")
    except Exception as e:
        log_error(f"❌ Error al insertar datos de deuda pública en la base de datos: {e}")
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

def crear_tabla_deuda_publica_si_no_existe():
    conexion = conectar()
    cursor = conexion.cursor()

    crear_tabla_sql = """
    CREATE TABLE IF NOT EXISTS deuda_publica (
        id INT AUTO_INCREMENT PRIMARY KEY,
        descripcion VARCHAR(255),
        isin VARCHAR(50),
        compra_numero VARCHAR(50),
        compra_importe VARCHAR(50),
        compra_tir VARCHAR(50),
        compra_precio VARCHAR(50),
        venta_precio VARCHAR(50),
        venta_tir VARCHAR(50),
        venta_importe VARCHAR(50),
        venta_numero VARCHAR(50),
        ultimo_precio VARCHAR(50),
        ultimo_tir VARCHAR(50),
        importe_nominal VARCHAR(50),
        fecha_insercion DATE NOT NULL,
        UNIQUE KEY unique_isin_fecha (isin, fecha_insercion)
    );
    """

    try:
        cursor.execute(crear_tabla_sql)
        conexion.commit()
        log_info("✅ Tabla 'deuda_publica' verificada o creada correctamente.")
    except Exception as e:
        log_error(f"❌ Error al crear/verificar la tabla 'deuda_publica': {e}")
    finally:
        cursor.close()
        conexion.close()

def crear_tabla_composicion_ibex35_si_no_existe():
    conexion = conectar()
    cursor = conexion.cursor()

    crear_tabla_sql = """
    CREATE TABLE IF NOT EXISTS composicion_ibex35 (
        id INT AUTO_INCREMENT PRIMARY KEY,
        simbolo VARCHAR(20),
        nombre VARCHAR(255),
        titulos_antes VARCHAR(100),
        estatus VARCHAR(100),
        modificaciones VARCHAR(100),
        comp VARCHAR(100),
        coef_ff VARCHAR(100),
        fecha_insercion DATE NOT NULL,
        nombre_pdf VARCHAR(255),
        UNIQUE KEY unique_simbolo_fecha (simbolo, fecha_insercion)
    );
    """

    try:
        cursor.execute(crear_tabla_sql)
        conexion.commit()
        log_info("✅ Tabla 'composicion_ibex35' verificada o creada correctamente.")
    except Exception as e:
        log_error(f"❌ Error al crear/verificar la tabla 'composicion_ibex35': {e}")
    finally:
        cursor.close()
        conexion.close()

def crear_tabla_datos_empresas_si_no_existe():
    conexion = conectar()
    cursor = conexion.cursor()

    crear_tabla_sql = """
    CREATE TABLE IF NOT EXISTS datos_empresas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        empresa VARCHAR(255),
        anio INT,
        capitalizacion DECIMAL(20, 2),
        num_acciones BIGINT,
        precio_cierre DECIMAL(10, 2),
        ultimo_precio DECIMAL(10, 2),
        precio_max DECIMAL(10, 2),
        precio_min DECIMAL(10, 2),
        volumen BIGINT,
        efectivo DECIMAL(20, 2),
        fecha_registro DATE NOT NULL,
        UNIQUE KEY unique_empresa_anio (empresa, anio)
    );
    """

    try:
        cursor.execute(crear_tabla_sql)
        conexion.commit()
        log_info("✅ Tabla 'datos_empresas' verificada o creada correctamente.")
    except Exception as e:
        log_error(f"❌ Error al crear/verificar la tabla 'datos_empresas': {e}")
    finally:
        cursor.close()
        conexion.close()


# ========================
# Inicialización al importar módulo
# ========================
crear_base_datos_si_no_existe()
crear_tabla_si_no_existe()
crear_tabla_datos_empresas_si_no_existe()
crear_tabla_composicion_ibex35_si_no_existe()
crear_tabla_deuda_publica_si_no_existe()













