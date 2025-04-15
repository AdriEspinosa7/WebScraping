import os
import tempfile
import requests
import fitz  # PyMuPDF
import re
from datetime import datetime
from log_utils import log_info, log_error
from database.db_manager import insertar_datos_composicion


class IbexPDFScraper:
    def __init__(self, pdf_url=None):
        # URL predeterminada; cámbiala si es necesario
        self.pdf_url = pdf_url or "https://www.bolsasymercados.es/bme-exchange/docs/Indices/Avisos/esp/gestorindice/Aviso_Gestor_Indices_02-25.pdf"

    def descargar_pdf(self):
        """
        Descarga el PDF y lo guarda en un archivo temporal.
        Devuelve la ruta del archivo descargado o None en caso de error.
        """
        try:
            response = requests.get(self.pdf_url)
            if response.status_code == 200:
                tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                tmp_file.write(response.content)
                tmp_file.close()
                log_info(f"📥 PDF descargado correctamente: {self.pdf_url}")
                return tmp_file.name
            else:
                log_error(f"❌ Error al descargar PDF, código de estado: {response.status_code}")
                return None
        except Exception as e:
            log_error(f"❌ Excepción al descargar PDF: {e}")
            return None

    def extraer_tabla(self, pdf_path):
        """
        Abre el PDF, extrae el texto completo y busca la sección con la tabla de composición.
        Se espera que la sección comience con la línea que contenga:
        "Composición del índice IBEX 35® a partir"
        Devuelve una lista de diccionarios (cada uno representa una fila) o una lista vacía si no se encuentran datos.
        """
        try:
            # Abrir PDF
            doc = fitz.open(pdf_path)
            texto = ""
            # Concatenamos el texto de todas las páginas (puedes ajustar si solo es la primera)
            for page in doc:
                texto += page.get_text("text") + "\n"
            doc.close()

            # Buscamos el marcador (ajusta el patrón si es necesario)
            marcador = "Composición del índice IBEX 35® a partir"
            pos = texto.find(marcador)
            if pos == -1:
                log_error("❌ No se encontró el marcador 'Composición del índice IBEX 35® a partir' en el PDF.")
                return []

            # Extraer el bloque de texto que sigue al marcador
            bloque = texto[pos + len(marcador):].strip()

            # Como en el PDF la tabla se muestra en varias líneas, separamos en líneas
            lineas = [line.strip() for line in bloque.splitlines() if line.strip()]
            if not lineas:
                log_error("❌ No se encontraron líneas después del marcador en el PDF.")
                return []

            # Aquí puedes imprimir el bloque para depuración (comentado):
            # print("DEBUG - Texto extraído:\n", bloque)

            # Suponemos que las filas de la tabla comienzan inmediatamente y que cada fila tiene al menos 7 columnas.
            datos_tabla = []
            for linea in lineas:
                # Separamos por dos o más espacios
                columnas = re.split(r'\s{2,}', linea)
                # Validamos que tengamos al menos 7 columnas
                if len(columnas) < 7:
                    continue
                # Si hay más de 7 columnas, unimos las extras en la última columna
                if len(columnas) > 7:
                    columnas = columnas[:6] + [' '.join(columnas[6:])]
                # Creamos el diccionario para esta fila
                fila = {
                    "simbolo": columnas[0],
                    "nombre": columnas[1],
                    "titulos_antes": columnas[2],
                    "estatus": columnas[3],
                    "modificaciones": columnas[4],
                    "comp": columnas[5],
                    "porcentaje_coef_ff": columnas[6],
                    "fecha_registro": datetime.now().date()  # Solo la fecha
                }
                datos_tabla.append(fila)

            log_info(f"Se extrajeron {len(datos_tabla)} filas de la tabla del PDF.")
            return datos_tabla
        except Exception as e:
            log_error(f"❌ Error al extraer la tabla del PDF: {e}")
            return []

    def ejecutar(self):
        """
        Ejecuta todo el proceso: descarga el PDF, extrae la tabla y guarda los datos en la base de datos.
        Elimina el archivo temporal al finalizar.
        """
        log_info("🚀 Iniciando scraping de PDF del IBEX 35")
        pdf_path = self.descargar_pdf()
        if not pdf_path:
            log_error("❌ Falló la descarga del PDF; abortando scraping.")
            return

        datos = self.extraer_tabla(pdf_path)
        if not datos:
            log_error("❌ No se extrajeron datos de la tabla del PDF.")
        else:
            for dato in datos:
                result = insertar_datos_composicion(dato)
                if result:
                    log_info(f"📥 Insertado/actualizado: {dato['simbolo']} - {dato['nombre']}")
                else:
                    log_info(f"📛 Registro duplicado o error para: {dato['simbolo']} - {dato['nombre']}")

        try:
            os.remove(pdf_path)
            log_info("🗑️ Archivo PDF temporal eliminado.")
        except Exception as e:
            log_error(f"❌ Error al eliminar el PDF temporal: {e}")

        log_info("✅ Scraping de PDFs de IBEX 35 completado.")


# Función para ejecutar el scraper desde la línea de comandos
def ejecutar_scraping_pdf():
    scraper = IbexPDFScraper()
    scraper.ejecutar()


if __name__ == "__main__":
    ejecutar_scraping_pdf()




