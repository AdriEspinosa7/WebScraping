import os
import csv
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from database.db_manager import guardar_datos
from log_utils import log_info, log_error
from scraper.bme_scraper import ejecutar_scraping_empresas_bme

# ===============================
# Configuración del Navegador
# ===============================
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# ===============================
# Crear archivo CSV si no existe
# ===============================
def crear_csv_predeterminado(ruta_csv):
    contenido_inicial = [
        {"nombre": "IBEX 35", "url": "https://es.investing.com/indices/spain-35"},
        {"nombre": "S&P 500", "url": "https://es.investing.com/indices/us-spx-500"},
        {"nombre": "NASDAQ 100", "url": "https://es.investing.com/indices/nq-100"},
        {"nombre": "DAX 40", "url": "https://es.investing.com/indices/germany-30"},
        {"nombre": "MSCI WORLD", "url": "https://es.investing.com/indices/msci-world"}
    ]
    try:
        with open(ruta_csv, mode="w", newline='', encoding="utf-8") as archivo:
            campos = ["nombre", "url"]
            writer = csv.DictWriter(archivo, fieldnames=campos)
            writer.writeheader()
            writer.writerows(contenido_inicial)
        log_info("📝 Se creó el archivo indices.csv con contenido predeterminado.")
        print("Se ha creado indices.csv con contenido de ejemplo.")
    except Exception as e:
        log_error(f"❌ Error al crear indices.csv: {e}")
        print(f"No se pudo crear indices.csv: {e}")
        exit(1)

# ===============================
# Leer índices desde indices.csv
# ===============================
indices = {}
csv_path = os.path.join(os.path.dirname(__file__), "indices.csv")

if not os.path.exists(csv_path):
    crear_csv_predeterminado(csv_path)

try:
    with open(csv_path, mode="r", encoding="utf-8") as archivo_csv:
        lector = csv.DictReader(archivo_csv)
        for fila in lector:
            nombre = fila.get("nombre")
            url = fila.get("url")
            if nombre and url:
                indices[nombre.strip()] = url.strip()

    if not indices:
        log_error("❌ El archivo indices.csv está vacío o mal formateado.")
        print("El archivo indices.csv no tiene índices válidos. Terminando el programa.")
        exit(1)

except Exception as e:
    log_error(f"❌ Error al leer indices.csv: {e}")
    print(f"No se pudo leer el archivo indices.csv: {e}")
    exit(1)

# ===============================
# Función para Extraer Datos
# ===============================
def obtener_datos(url, reintentos=3):
    for intento in range(reintentos):
        try:
            driver.get(url)
            time.sleep(5)  # Espera estática: podría sustituirse por espera explícita si fallara

            nombre = driver.find_element(By.CSS_SELECTOR, "h1").text.strip()
            precio_text = driver.find_element(By.CSS_SELECTOR, "span[data-test='instrument-price-last']").text.strip()
            variacion = driver.find_element(By.CSS_SELECTOR, "span[data-test='instrument-price-change']").text.strip()
            porcentaje = driver.find_element(By.CSS_SELECTOR, "span[data-test='instrument-price-change-percent']").text.strip()

            precio_num = float(precio_text.replace(".", "").replace(",", "."))  # Adaptación al formato europeo

            return nombre, precio_num, variacion, porcentaje

        except Exception as e:
            print(f"Error en intento {intento + 1} para {url}: {e}")
            time.sleep(2)

    print(f"No se pudo obtener datos después de varios intentos para {url}.")
    return None, None, None, None

# ===============================
# Procesamiento de los Índices
# ===============================
guardados = 0
omitidos = 0
fallidos = 0

log_info("🚀 Inicio del proceso de scraping de índices bursátiles.")

for indice, url in indices.items():
    print(f"Procesando {indice}...")
    nombre, precio, variacion, porcentaje = obtener_datos(url)

    if nombre and precio is not None:
        print(f"{indice}: {nombre} - {precio} - {variacion} - {porcentaje}")
        fecha_hora = datetime.now()

        resultado = guardar_datos(nombre, precio, variacion, porcentaje, fecha_hora)
        if resultado:
            guardados += 1
            print(f"✅ Datos guardados para {nombre}.")
        else:
            omitidos += 1
            print(f"ℹ️ Ya existía un registro para {nombre} hoy. Se omitió.")
    else:
        log_error(f"❌ No se pudieron obtener datos para {indice}.")
        fallidos += 1

driver.quit()
log_info("🏁 Fin del proceso de scraping. Navegador cerrado.")

# ===============================
# Resumen Final
# ===============================
print("\n📊 RESUMEN DE EJECUCIÓN:")
print(f"✅ Índices guardados: {guardados}")
print(f"ℹ️ Índices omitidos (ya estaban en la BD): {omitidos}")
print(f"❌ Fallos al obtener datos: {fallidos}")

log_info("📊 RESUMEN FINAL:")
log_info(f"✅ Índices guardados: {guardados}")
log_info(f"ℹ️ Índices omitidos (ya estaban en la BD): {omitidos}")
log_info(f"❌ Fallos al obtener datos: {fallidos}")

# ===============================
# Scraping de empresas BME
# ===============================
ejecutar_scraping_empresas_bme()













