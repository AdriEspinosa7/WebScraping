from bs4 import BeautifulSoup


def extraer_datos(html, indice):
    """
    Extrae el nombre del índice, precio, variación y porcentaje usando los atributos data-test.
    Se espera que para IBEX 35 y otros índices con estructura similar se encuentren:
      - Precio: data-test="instrument-price-last"
      - Variación: data-test="instrument-price-change"
      - Porcentaje: data-test="instrument-price-change-percent"
    """
    soup = BeautifulSoup(html, 'html.parser')

    # Extraer el nombre (generalmente en <h1>)
    nombre_elemento = soup.find('h1')
    nombre = nombre_elemento.text.strip() if nombre_elemento else "No encontrado"

    # Extraer el precio
    precio_elemento = soup.find('span', {'data-test': 'instrument-price-last'})
    precio = precio_elemento.text.strip() if precio_elemento else "No encontrado"

    # Extraer la variación
    variacion_elemento = soup.find('span', {'data-test': 'instrument-price-change'})
    variacion = variacion_elemento.text.strip() if variacion_elemento else "No encontrado"

    # Extraer el porcentaje
    porcentaje_elemento = soup.find('span', {'data-test': 'instrument-price-change-percent'})
    porcentaje = porcentaje_elemento.text.strip() if porcentaje_elemento else "No encontrado"

    print(f"Nombre encontrado: {nombre}")
    print(f"Precio encontrado: {precio}")
    print(f"Variación encontrada: {variacion}")
    print(f"Porcentaje encontrado: {porcentaje}")

    return nombre, precio, variacion, porcentaje


