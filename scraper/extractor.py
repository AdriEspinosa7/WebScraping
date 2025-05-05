from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from utils.log_utils import log_error

def obtener_html(url, wait_for_table=False, timeout=15):
    """
    Abre la URL con Selenium en modo headless, espera a que cargue la página
    y devuelve el HTML.
    Si wait_for_table=True, espera hasta que aparezca un <table> o hasta timeout.
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        if wait_for_table:
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "table"))
            )
        else:
            time.sleep(8)
        html = driver.page_source
        return html
    except Exception as e:
        log_error(f"Error al obtener el HTML de {url}: {e}")
        return driver.page_source
    finally:
        driver.quit()






