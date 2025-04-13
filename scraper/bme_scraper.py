import os
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database.db_manager import insertar_datos_empresa
from scraper.parser import parsear_fila_bme
from log_utils import log_info, log_error


def configurar_driver():
    opciones = Options()
    opciones.add_argument("--headless")
    opciones.add_argument("--no-sandbox")
    opciones.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=opciones)


def leer_empresas_bme_csv():
    ruta_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "empresas_bme.csv")
    empresas = {}
    try:
        with open(ruta_csv, mode="r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                nombre = fila.get("nombre")
                url = fila.get("url")
                if nombre and url:
                    empresas[nombre.strip()] = url.strip()
        return empresas
    except Exception as e:
        log_error(f"❌ Error al leer empresas_bme.csv: {e}")
        print(f"❌ Error al leer empresas_bme.csv: {e}")
        return {}


def extraer_tabla_bme(driver, url, empresa):
    try:
        log_info(f"📄 Accediendo a la web de {empresa}: {url}")
        print(f"📄 Accediendo a la web de {empresa}...")
        driver.get(url)

        tablas = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="table-responsive"]/table'))
        )

        tabla_deseada = None
        for t in tablas:
            cabecera = t.find_elements(By.TAG_NAME, "th")
            if len(cabecera) == 9:
                tabla_deseada = t
                break

        if not tabla_deseada:
            log_error(f"❌ No se encontró una tabla con 9 columnas para {empresa}")
            print(f"❌ No se encontró una tabla con 9 columnas para {empresa}")
            return

        filas = tabla_deseada.find_elements(By.TAG_NAME, "tr")
        if len(filas) <= 1:
            log_info(f"⚠️ No se encontraron filas de datos para {empresa}")
            print(f"⚠️ No se encontraron filas de datos para {empresa}")
            return

        filas_validas = 0

        for fila in filas[1:]:
            celdas = fila.find_elements(By.XPATH, ".//td | .//th")
            valores = [celda.text.strip() for celda in celdas]

            if len(valores) == 9:
                datos = parsear_fila_bme(valores, empresa)

                if all(valor in ("", "-") for valor in datos.values()):
                    log_info(f"⚠️ Fila ignorada para {empresa}, datos vacíos o nulos: {valores}")
                    print(f"⚠️ Fila ignorada para {empresa}, datos vacíos o nulos")
                    continue

                insertar_datos_empresa(datos)
                filas_validas += 1
                log_info(f"✅ Datos insertados para {empresa}, año {datos['anio']}")
            else:
                log_info(f"⚠️ Fila con columnas inesperadas en {empresa}: {len(valores)} columnas")
                print(f"⚠️ Fila con columnas inesperadas en {empresa}: {len(valores)} columnas")

        if filas_validas == 0:
            log_info(f"⚠️ Todas las filas fueron ignoradas para {empresa}")
            print(f"⚠️ Todas las filas fueron ignoradas para {empresa}")

    except TimeoutException:
        mensaje = f"❌ Timeout: no se encontró la tabla para {empresa}"
        log_error(mensaje)
        print(mensaje)
    except NoSuchElementException as e:
        mensaje = f"❌ No se pudo encontrar la tabla en la página de {empresa}: {e}"
        log_error(mensaje)
        print(mensaje)
    except Exception as e:
        mensaje = f"❌ Error general al procesar {empresa}: {e}"
        log_error(mensaje)
        print(mensaje)



def ejecutar_scraping_empresas_bme():
    empresas = leer_empresas_bme_csv()

    log_info("🚀 Iniciando scraping de empresas BME")
    print("🚀 Iniciando scraping de empresas BME...")

    if not empresas:
        print("❌ No se encontraron empresas válidas en el archivo CSV.")
        return

    driver = configurar_driver()

    for empresa, url in empresas.items():
        log_info(f"🔍 Iniciando scraping para {empresa}")
        print(f"🔍 Iniciando scraping para {empresa}")
        extraer_tabla_bme(driver, url, empresa)

    driver.quit()
    log_info("✅ Scraping de empresas BME finalizado.")
    print("✅ Scraping de empresas BME finalizado.")


if __name__ == "__main__":
    ejecutar_scraping_empresas_bme()















