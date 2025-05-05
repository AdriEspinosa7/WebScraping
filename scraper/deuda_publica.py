import re
from bs4 import BeautifulSoup
from datetime import date
from scraper.extractor import obtener_html
from database.db_manager import insertar_datos_deuda_publica
from utils.log_utils import log_info, log_error

URL_DEUDA_PUBLICA = "https://www.bolsasymercados.es/bme-exchange/es/Mercados-y-Cotizaciones/Renta-Fija/Precios/AIAF-SEND-Deuda-Publica"

def parse_int(text):
    """
    Elimina separadores de miles (.) y posibles decimales,
    devolviendo sólo la parte entera.
    """
    txt = text.strip()
    # quitamos todo lo que no sea dígito o coma/punto
    txt = re.sub(r"[^\d.,]", "", txt)
    # si hay coma, la parte entera es antes de ella:
    if "," in txt:
        txt = txt.split(",")[0]
    # eliminamos puntos (miles)
    txt = txt.replace(".", "")
    try:
        return int(txt)
    except ValueError:
        return 0

def parse_float(text):
    """
    Interpreta correctamente:
      - Si hay punto y coma: punto = miles, coma = decimal.
      - Si sólo hay coma: coma = decimal.
      - Si sólo hay punto: punto = decimal (caso raro en esta web).
    """
    txt = text.strip()
    # limpiamos espacios y símbolos
    txt = re.sub(r"[^\d.,]", "", txt)
    if "." in txt and "," in txt:
        # formato español: 1.234,56 -> 1234.56
        txt = txt.replace(".", "").replace(",", ".")
    elif "," in txt:
        # formato con coma decimal: 1234,56 -> 1234.56
        txt = txt.replace(",", ".")
    # de lo contrario dejamos el punto decimal si existe
    try:
        return float(txt)
    except ValueError:
        return 0.0

def extraer_tabla_deuda_publica(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        tabla = soup.find("table")
        if not tabla:
            raise ValueError("No se encontró ninguna tabla en la página.")

        filas = tabla.find_all("tr")
        datos = []

        for fila in filas[1:]:
            celdas = fila.find_all("td")
            if len(celdas) != 13:
                continue

            descripcion     = celdas[0].get_text(strip=True)
            isin            = celdas[1].get_text(strip=True)

            compra_numero   = parse_int(celdas[2].get_text())
            compra_importe  = parse_float(celdas[3].get_text())
            compra_tir      = parse_float(celdas[4].get_text())
            compra_precio   = parse_float(celdas[5].get_text())

            venta_precio    = parse_float(celdas[6].get_text())
            venta_tir       = parse_float(celdas[7].get_text())
            venta_importe   = parse_float(celdas[8].get_text())
            venta_numero    = parse_int(celdas[9].get_text())

            ultimo_precio   = parse_float(celdas[10].get_text())
            ultimo_tir      = parse_float(celdas[11].get_text())
            importe_nominal = parse_float(celdas[12].get_text())

            datos.append({
                "descripcion":     descripcion,
                "isin":            isin,
                "compra_numero":   compra_numero,
                "compra_importe":  compra_importe,
                "compra_tir":      compra_tir,
                "compra_precio":   compra_precio,
                "venta_precio":    venta_precio,
                "venta_tir":       venta_tir,
                "venta_importe":   venta_importe,
                "venta_numero":    venta_numero,
                "ultimo_precio":   ultimo_precio,
                "ultimo_tir":      ultimo_tir,
                "importe_nominal": importe_nominal,
                "fecha_insercion": date.today()
            })

        return datos

    except Exception as e:
        log_error(f"Error al extraer la tabla de deuda pública: {e}")
        return []

def ejecutar_scraper_deuda_publica():
    log_info("Iniciando scraping de deuda pública (AIAF SEND)")
    html = obtener_html(URL_DEUDA_PUBLICA, wait_for_table=True)
    if not html:
        log_error("No se pudo obtener el HTML de la página de deuda pública.")
        return

    datos = extraer_tabla_deuda_publica(html)
    if datos:
        insertar_datos_deuda_publica(datos)
        log_info(f"Se han insertado {len(datos)} registros de deuda pública.")
    else:
        log_info("No se encontraron datos para insertar.")

if __name__ == "__main__":
    ejecutar_scraper_deuda_publica()







