import os
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scraper.parser import parsear_fila_bme
from database.db_manager import insertar_datos_empresa
from utils.log_utils import log_info, log_error


class BmeScraper:
    def __init__(self):
        self.driver = self._configurar_driver()
        self.empresas = self._leer_empresas_bme_csv()

    def _configurar_driver(self):
        opciones = Options()
        opciones.add_argument("--headless")
        opciones.add_argument("--no-sandbox")
        opciones.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(options=opciones)

    def _leer_empresas_bme_csv(self):
        # Se asume que el archivo CSV está en la raíz del proyecto (no dentro de scraper)
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
            log_info(f"Se cargaron {len(empresas)} empresas desde empresas_bme.csv")
            return empresas
        except Exception as e:
            log_error(f"❌ Error al leer empresas_bme.csv: {e}")
            return {}

    def _extraer_tabla(self, empresa, url):
        try:
            log_info(f"📄 Accediendo a la web de {empresa}: {url}")
            self.driver.get(url)

            tablas = WebDriverWait(self.driver, 15).until(
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
                return

            filas = tabla_deseada.find_elements(By.TAG_NAME, "tr")
            if len(filas) <= 1:
                log_info(f"⚠️ No se encontraron filas de datos para {empresa}")
                return

            filas_validas = 0
            for fila in filas[1:]:
                celdas = fila.find_elements(By.XPATH, ".//td | .//th")
                valores = [celda.text.strip() for celda in celdas]

                if len(valores) == 9:
                    datos = parsear_fila_bme(valores, empresa)

                    # Si todos los valores son vacíos o guiones, se ignora la fila
                    if all(valor in ("", "-") for valor in datos.values()):
                        log_info(f"⚠️ Fila ignorada para {empresa}, datos vacíos o nulos: {valores}")
                        continue

                    # Capturamos el resultado de la inserción
                    result = insertar_datos_empresa(datos)
                    if result:
                        filas_validas += 1
                        log_info(f"✅ Datos insertados para {empresa}, año {datos['anio']}")
                    # Si result es False, no se imprime nada aquí adicional, ya que la función
                    # en db_manager.py ya registra el duplicado.

                else:
                    log_info(f"⚠️ Fila con columnas inesperadas en {empresa}: {len(valores)} columnas")

            if filas_validas == 0:
                log_info(f"⚠️ Todas las filas fueron ignoradas para {empresa}")

        except TimeoutException:
            log_error(f"❌ Timeout: no se encontró la tabla para {empresa}")
        except NoSuchElementException as e:
            log_error(f"❌ No se pudo encontrar la tabla en la página de {empresa}: {e}")
        except Exception as e:
            log_error(f"❌ Error general al procesar {empresa}: {e}")

    def ejecutar(self):
        log_info("🚀 Iniciando scraping de empresas BME")

        if not self.empresas:
            log_error("❌ No se encontraron empresas válidas en el archivo CSV.")
            return

        for empresa, url in self.empresas.items():
            log_info(f"🔍 Iniciando scraping para {empresa}")
            self._extraer_tabla(empresa, url)

        self.driver.quit()
        log_info("✅ Scraping de empresas BME finalizado.")


def ejecutar_scraping_empresas_bme():
    scraper = BmeScraper()
    scraper.ejecutar()






















