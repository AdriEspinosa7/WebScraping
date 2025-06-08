import time
import os
import csv
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from database.db_manager import guardar_datos
from utils.log_utils import log_info, log_error
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


class InvestingScraper:
    def __init__(self, csv_path="indices.csv"):
        self.csv_path = csv_path
        self.driver = self._crear_driver()
        self.indices = self._cargar_indices()

    def _crear_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)

    def _crear_csv_predeterminado(self):
        contenido_inicial = [
            {"nombre": "IBEX 35", "url": "https://es.investing.com/indices/spain-35"},
            {"nombre": "S&P 500", "url": "https://es.investing.com/indices/us-spx-500"},
            {"nombre": "NASDAQ 100", "url": "https://es.investing.com/indices/nq-100"},
            {"nombre": "DAX 40", "url": "https://es.investing.com/indices/germany-30"},
            {"nombre": "MSCI WORLD", "url": "https://es.investing.com/indices/msci-world"}
        ]
        try:
            with open(self.csv_path, mode="w", newline='', encoding="utf-8") as archivo:
                campos = ["nombre", "url"]
                writer = csv.DictWriter(archivo, fieldnames=campos)
                writer.writeheader()
                writer.writerows(contenido_inicial)
            log_info("📝 Se creó el archivo indices.csv con contenido predeterminado.")
        except Exception as e:
            log_error(f"❌ Error al crear indices.csv: {e}")
            raise

    def _cargar_indices(self):
        if not os.path.exists(self.csv_path):
            self._crear_csv_predeterminado()

        indices = {}
        try:
            with open(self.csv_path, mode="r", encoding="utf-8") as archivo_csv:
                lector = csv.DictReader(archivo_csv)
                for fila in lector:
                    nombre = fila.get("nombre")
                    url = fila.get("url")
                    if nombre and url:
                        indices[nombre.strip()] = url.strip()

            if not indices:
                raise ValueError("El archivo indices.csv está vacío o mal formateado.")
            return indices

        except Exception as e:
            log_error(f"❌ Error al leer indices.csv: {e}")
            raise


    def parsear_numero(self, texto):
        """
        Convierte textos numéricos en float, manejando formatos latino y anglosajón.
        """
        try:
            texto = texto.strip()

            # Patrón típico latino: 14.196,78 o 92.290.819
            if re.match(r"^\d{1,3}(\.\d{3})+,\d{2}$", texto) or re.match(r"^\d{1,3}(\.\d{3})+$", texto):
                texto_limpio = texto.replace('.', '').replace(',', '.')
                return float(texto_limpio)

            # Patrón típico anglosajón: 2,149,190.33 o 92,290,819
            if re.match(r"^\d{1,3}(,\d{3})+(\.\d+)?$", texto):
                texto_limpio = texto.replace(',', '')
                return float(texto_limpio)

            # Solo coma decimal: 123,45
            if re.match(r"^\d+,\d+$", texto):
                return float(texto.replace(',', '.'))

            # Solo punto decimal: 123.45
            return float(texto)
        except ValueError:
            log_error(f"❌ Error al convertir número: {texto}")
            raise

    def obtener_datos(self, url, reintentos=3):
        for intento in range(reintentos):
            try:
                self.driver.get(url)
                time.sleep(5)

                # Verificar el título del documento con BeautifulSoup
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                titulo = soup.title.string.strip().lower() if soup.title and soup.title.string else ""

                # Detectar errores reales según el título
                if any(e in titulo for e in ["404", "not found", "error", "access denied"]):
                    log_error(f"❌ Página con error detectado en el título: '{titulo}' -> {url}")
                    return None, None, None, None

                # Esperar a que aparezca el nombre del índice
                try:
                    nombre_element = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
                    )
                    nombre = nombre_element.text.strip()
                except TimeoutException:
                    log_error(f"❌ No se encontró el título <h1> en {url}.")
                    return None, None, None, None

                # Esperar a que aparezca el precio actual
                try:
                    price_element = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "span[data-test='instrument-price-last']"))
                    )
                    precio_bruto = price_element.text.strip()
                except TimeoutException:
                    log_error(f"❌ No se encontró el precio para {nombre}.")
                    return None, None, None, None

                # Obtener variación y porcentaje
                variacion_bruta = self.driver.find_element(By.CSS_SELECTOR,
                                                           "span[data-test='instrument-price-change']").text.strip()
                porcentaje_bruto = self.driver.find_element(By.CSS_SELECTOR,
                                                            "span[data-test='instrument-price-change-percent']").text.strip()

                precio = self.parsear_numero(precio_bruto)
                variacion = variacion_bruta.strip()
                porcentaje = porcentaje_bruto.strip()

                return nombre, precio, variacion, porcentaje

            except Exception as e:
                print(f"Error en intento {intento + 1}: {e}")
                time.sleep(2)

        return None, None, None, None


    def ejecutar(self):
        guardados = 0
        omitidos = 0
        fallidos = 0

        log_info("🚀 Inicio del scraping de índices bursátiles.")

        for indice, url in self.indices.items():
            print(f"Procesando {indice}...")
            nombre, precio, variacion, porcentaje = self.obtener_datos(url)

            if nombre and precio is not None:
                fecha_hora = datetime.now()
                resultado = guardar_datos(nombre, precio, variacion, porcentaje, fecha_hora)
                if resultado:
                    guardados += 1
                    print(f"✅ Guardado: {nombre}")
                else:
                    omitidos += 1
                    print(f"ℹ️ Omitido (duplicado): {nombre}")
            else:
                log_error(f"❌ Fallo al obtener datos de {indice}.")
                fallidos += 1

        self.driver.quit()
        log_info("🏁 Fin del scraping. Navegador cerrado.")

        print("\n📊 RESUMEN DE EJECUCIÓN:")
        print(f"✅ Índices guardados: {guardados}")
        print(f"ℹ️ Índices omitidos: {omitidos}")
        print(f"❌ Fallos: {fallidos}")

        log_info("📊 RESUMEN FINAL:")
        log_info(f"✅ Índices guardados: {guardados}")
        log_info(f"ℹ️ Índices omitidos: {omitidos}")
        log_info(f"❌ Fallos: {fallidos}")

# Función fuera de la clase para ejecutar el scraping de índices
def ejecutar_scraping_indices():
    try:
        scraper = InvestingScraper()
        scraper.ejecutar()
    except Exception as e:
        log_error(f"❌ Error al ejecutar el scraping de índices: {e}")

