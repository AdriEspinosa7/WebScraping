from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def obtener_html(url):
    """
    Selenium para obtener el HTML de una página que carga contenido dinámico con JavaScript.
    """
    # Configurar Chrome en modo "headless" (sin abrir ventana)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")

    # Descargar y configurar ChromeDriver automáticamente
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)  # Abrir la URL
        time.sleep(5)  # Esperar a que la página cargue

        return driver.page_source  # Devolver el HTML de la página
    finally:
        driver.quit()  # Cerrar el navegador


