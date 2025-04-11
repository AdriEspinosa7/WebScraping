from bs4 import BeautifulSoup
import re
from datetime import datetime

def extraer_datos(html, indice):
    """
    Extrae el nombre del índice, precio, variación y porcentaje desde Investing.com.
    Utiliza los atributos data-test esperados en la estructura del HTML.
    Devuelve una tupla con nombre, precio, variación y porcentaje.
    """
    soup = BeautifulSoup(html, 'html.parser')

    # Extraer el nombre del índice (normalmente en un <h1>)
    nombre_elemento = soup.find('h1')
    nombre = nombre_elemento.text.strip() if nombre_elemento else "No encontrado"

    # Extraer el precio actual del índice
    precio_elemento = soup.find('span', {'data-test': 'instrument-price-last'})
    precio = precio_elemento.text.strip() if precio_elemento else "No encontrado"

    # Extraer la variación absoluta
    variacion_elemento = soup.find('span', {'data-test': 'instrument-price-change'})
    variacion = variacion_elemento.text.strip() if variacion_elemento else "No encontrado"

    # Extraer la variación porcentual
    porcentaje_elemento = soup.find('span', {'data-test': 'instrument-price-change-percent'})
    porcentaje = porcentaje_elemento.text.strip() if porcentaje_elemento else "No encontrado"

    print(f"Nombre encontrado: {nombre}")
    print(f"Precio encontrado: {precio}")
    print(f"Variación encontrada: {variacion}")
    print(f"Porcentaje encontrado: {porcentaje}")

    return nombre, precio, variacion, porcentaje


def limpiar_anio_bme(anio_raw):
    """
    Extrae el año como entero desde un string tipo '2025 (hasta el 08/4)'.
    Devuelve una tupla: (año, fecha_sin_hora) para guardar en la base de datos.
    """
    match = re.match(r"(\d{4})(?:.*?(\d{1,2})/(\d{1,2}))?", anio_raw)
    if match:
        anio = int(match.group(1))
        if match.group(2) and match.group(3):
            dia = int(match.group(2))
            mes = int(match.group(3))
            fecha_extraccion = datetime(anio, mes, dia).date()  # ✅ devolvemos solo la fecha
        else:
            fecha_extraccion = datetime(anio, 12, 31).date()
        return anio, fecha_extraccion
    else:
        return None, None


def parsear_fila_bme(fila_elementos, empresa):
    """
    Parsea una fila de datos anuales de una empresa BME.
    Devuelve un diccionario con los datos ya normalizados para guardar en la base de datos.
    """
    anio_raw = fila_elementos[0]
    anio, fecha_extraccion = limpiar_anio_bme(anio_raw)

    # Limpieza de valores: quita puntos de miles y convierte comas a puntos decimales
    def normalizar(valor):
        return valor.replace(".", "").replace(",", ".") if valor else None

    return {
        "empresa": empresa,
        "anio": anio,
        "capitalizacion": normalizar(fila_elementos[1]),
        "num_acciones": normalizar(fila_elementos[2]),
        "precio_cierre": normalizar(fila_elementos[3]),
        "ultimo_precio": normalizar(fila_elementos[4]),
        "precio_max": normalizar(fila_elementos[5]),
        "precio_min": normalizar(fila_elementos[6]),
        "volumen": normalizar(fila_elementos[7]),
        "efectivo": normalizar(fila_elementos[8]),
        "fecha_registro": fecha_extraccion  # ✅ solo la fecha (sin hora)
    }




import re
from datetime import datetime

def limpiar_anio_bme(anio_raw):
    """
    Extrae el año como entero desde el formato '2025 (hasta el 08/4)'.
    Si no hay fecha adicional, se asume el 31 de diciembre.
    """
    match = re.match(r"(\d{4})(?:.*?(\d{1,2})/(\d{1,2}))?", anio_raw)
    if match:
        anio = int(match.group(1))
        if match.group(2) and match.group(3):
            dia = int(match.group(2))
            mes = int(match.group(3))
            fecha_extraccion = datetime(anio, mes, dia)
        else:
            fecha_extraccion = datetime(anio, 12, 31)  # valor por defecto si no hay fecha
        return anio, fecha_extraccion
    else:
        return None, None

def parsear_fila_bme(fila_elementos, empresa):
    """
    Recibe una lista de textos (una fila de la tabla BME) y devuelve un dict listo para guardar en la BD.
    """
    anio_raw = fila_elementos[0]
    anio, fecha_extraccion = limpiar_anio_bme(anio_raw)

    # Eliminamos puntos de miles y cambiamos comas por puntos decimales
    def normalizar(valor):
        return valor.replace(".", "").replace(",", ".") if valor else None

    return {
        "empresa": empresa,
        "anio": anio,
        "capitalizacion": normalizar(fila_elementos[1]),
        "num_acciones": normalizar(fila_elementos[2]),
        "precio_cierre": normalizar(fila_elementos[3]),
        "ultimo_precio": normalizar(fila_elementos[4]),
        "precio_max": normalizar(fila_elementos[5]),
        "precio_min": normalizar(fila_elementos[6]),
        "volumen": normalizar(fila_elementos[7]),
        "efectivo": normalizar(fila_elementos[8]),
        "fecha_registro": fecha_extraccion  # ✅ corregido aquí
    }



