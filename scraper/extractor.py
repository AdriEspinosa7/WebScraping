from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def obtener_html(url):
    """
    Abre la URL con Selenium en modo headless, espera a que cargue la página y devuelve el HTML.
    """
    options = Options()
    options.add_argument("--headless")       # Modo sin interfaz gráfica
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Iniciar el WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        # Esperar 5-10 segundos para que se cargue todo el contenido dinámico
        time.sleep(8)
        html = driver.page_source
        return html
    except Exception as e:
        print(f"Error al obtener el HTML: {e}")
        return None
    finally:
        driver.quit()





