from bs4 import BeautifulSoup

def extraer_datos(html):
    """
    Analiza el HTML y extrae el nombre del índice y su precio actual.
    """
    soup = BeautifulSoup(html, 'html.parser')

    # Extraer el nombre del índice
    nombre_elemento = soup.find('h1')
    nombre = nombre_elemento.text.strip() if nombre_elemento else 'Nombre no encontrado'

    # Extraer el precio actual
    precio_elemento = soup.find('div', class_='ml-3 table-cell w-[75px] max-w-[75px] flex-none overflow-hidden whitespace-nowrap text-right text-xs font-normal leading-4 text-[#181C21] rtl:text-right')
    precio = precio_elemento.text.strip() if precio_elemento else 'Precio no encontrado'

    return nombre, precio
