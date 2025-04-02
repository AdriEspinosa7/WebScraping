from scraper.extractor import obtener_html
from scraper.parser import extraer_datos
from scraper.db import guardar_datos  # Asumiendo que guardar_datos ya está funcionando bien

indices = {
    "IBEX 35": "https://es.investing.com/indices/spain-35",
    "S&P 500": "https://es.investing.com/indices/us-spx-500",
    "NASDAQ 100": "https://es.investing.com/indices/nq-100",
    "DAX 40": "https://es.investing.com/indices/germany-30",
    "MSCI WORLD": "https://es.investing.com/indices/msci-world"
}

for nombre_indice, url in indices.items():
    print(f"Procesando {nombre_indice}...")
    html = obtener_html(url)
    if html:
        try:
            nombre, precio, variacion, porcentaje = extraer_datos(html, nombre_indice)
            # Aquí puedes convertir el precio a float si es necesario
            # Por ejemplo, quitar separadores y cambiar coma por punto:
            if precio != "No encontrado":
                precio_num = float(precio.replace('.', '').replace(',', '.'))
            else:
                precio_num = 0.0

            # Luego guarda los datos en la base de datos
            guardar_datos(nombre, precio_num, variacion, porcentaje)
        except Exception as e:
            print(f"Error al procesar {nombre_indice}: {e}")
    else:
        print(f"No se pudo obtener HTML para {nombre_indice}")


