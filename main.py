from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from database.db_manager import guardar_datos  # Asegúrate de que esto está correctamente importado
import time
from webdriver_manager.chrome import ChromeDriverManager

# ===============================
# Configuración del Navegador
# ===============================
chrome_options = Options()
chrome_options.add_argument("--headless")  # Modo sin interfaz gráfica
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Inicializa ChromeDriver usando WebDriver Manager (se descarga la versión adecuada)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)


# ===============================
# Función para Extraer Datos
# ===============================
def obtener_datos(url, reintentos=3):
    """
    Extrae el nombre, precio, variación y porcentaje de cambio de un índice dado su URL.
    Usa los selectores basados en atributos 'data-test' que funcionaban previamente.
    Reintenta hasta 'reintentos' veces en caso de fallo.
    """
    for intento in range(reintentos):
        try:
            driver.get(url)
            # Espera para que se cargue el contenido dinámico
            time.sleep(5)

            # Extraer datos usando los selectores que funcionaban para IBEX 35
            nombre = driver.find_element(By.CSS_SELECTOR, "h1").text.strip()
            precio_text = driver.find_element(By.CSS_SELECTOR, "span[data-test='instrument-price-last']").text.strip()
            variacion = driver.find_element(By.CSS_SELECTOR, "span[data-test='instrument-price-change']").text.strip()
            porcentaje = driver.find_element(By.CSS_SELECTOR,
                                             "span[data-test='instrument-price-change-percent']").text.strip()

            # Conversión del precio: quitar puntos como separador de miles y reemplazar coma decimal
            precio_num = float(precio_text.replace(".", "").replace(",", "."))

            return nombre, precio_num, variacion, porcentaje
        except Exception as e:
            print(f"Error en intento {intento + 1} para {url}: {e}")
            time.sleep(2)
    print(f"No se pudo obtener datos después de varios intentos para {url}.")
    return None, None, None, None


# ===============================
# Diccionario de Índices
# ===============================
indices = {
    "IBEX 35": "https://es.investing.com/indices/spain-35",
    "S&P 500": "https://es.investing.com/indices/us-spx-500",
    "NASDAQ 100": "https://es.investing.com/indices/nq-100",
    "DAX 40": "https://es.investing.com/indices/germany-30",
    "MSCI WORLD": "https://es.investing.com/indices/msci-world"
}

# ===============================
# Proceso de Extracción para Todos los Índices
# ===============================
for indice, url in indices.items():
    print(f"Procesando {indice}...")
    nombre, precio, variacion, porcentaje = obtener_datos(url)
    if nombre is not None and precio is not None:
        print(f"{indice}: {nombre} - {precio} - {variacion} - {porcentaje}")
        # Ahora llamamos a guardar_datos para guardar los datos extraídos
        guardar_datos(nombre, precio, variacion, porcentaje)  # Añadir esta línea
    else:
        print(f"No se pudieron obtener datos para {indice}")

# Cerrar el navegador al finalizar
driver.quit()






