from scraper.extractor import obtener_html
from scraper.parser import extraer_datos
from scraper.db import guardar_datos  # Importación correcta

# URL de la página del IBEX 35 en Investing.com
url = "https://es.investing.com/indices/spain-35"

# Obtener HTML de la página
html = obtener_html(url)

# Extraer datos si el HTML se ha obtenido correctamente
if html:
    nombre, precio, variacion, porcentaje = extraer_datos(html)
    print(f"Nombre del índice: {nombre}")
    print(f"Precio actual: {precio}")
    print(f"Variación en puntos: {variacion}")
    print(f"Variación porcentual: {porcentaje}")

    # Guardar en MySQL
    guardar_datos(nombre, precio, variacion, porcentaje)
else:
    print("No se pudo obtener el HTML de la página.")

