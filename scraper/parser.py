from bs4 import BeautifulSoup

def extraer_datos(html):
    """
    Analiza el HTML y extrae el nombre del índice, su precio actual,
    la variación en puntos y la variación en porcentaje.
    """
    soup = BeautifulSoup(html, 'html.parser')

    # Extraer el nombre del índice
    nombre_elemento = soup.find('h1')
    nombre = nombre_elemento.text.strip() if nombre_elemento else 'Nombre no encontrado'

    # Extraer el precio actual
    precio_elemento = soup.find('span', {'data-test': 'instrument-price-last'})
    precio = precio_elemento.text.strip() if precio_elemento else 'Precio no encontrado'

    # Extraer la variación en puntos (manteniendo el signo)
    variacion_elemento = soup.find('span', {'data-test': 'instrument-price-change'})
    variacion = variacion_elemento.text.strip() if variacion_elemento else 'Variación no encontrada'

    # Extraer la variación en porcentaje (manteniendo el signo y el símbolo %)
    porcentaje_elemento = soup.find('span', {'data-test': 'instrument-price-change-percent'})
    porcentaje = porcentaje_elemento.text.strip() if porcentaje_elemento else 'Porcentaje no encontrado'

    return nombre, precio, variacion, porcentaje


