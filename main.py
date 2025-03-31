from scraper.extractor import obtener_html
from scraper.parser import extraer_datos
from scraper.db import guardar_datos

url = "https://es.investing.com/indices/spain-35"

html = obtener_html(url)

if html:
    nombre, precio = extraer_datos(html)
    print(f"Nombre del índice: {nombre}")
    print(f"Precio actual: {precio}")

    guardar_datos(nombre, precio)
else:
    print("No se pudo obtener el HTML de la página.")
