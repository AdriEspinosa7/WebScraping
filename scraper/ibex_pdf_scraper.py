import os
import re
import tempfile
import requests
from datetime import datetime

import fitz           # PyMuPDF
import pdfplumber     # pip install pdfplumber

from scraper.ocr_utils import configurar_ocr, extraer_texto_ocr
from log_utils import log_info, log_error
from database.db_manager import insertar_datos_composicion


class IbexPDFScraper:
    def __init__(self,
                 pdf_url: str = None,
                 extras_dir: str = None):
        self.pdf_url = pdf_url or (
            "https://www.bolsasymercados.es/"
            "bme-exchange/docs/Indices/Avisos/esp/gestorindice/"
            "Aviso_Gestor_Indices_02-25.pdf"
        )
        # localizamos extras/ como carpeta hermana de scraper/
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.extras_dir = extras_dir or os.path.join(base_dir, "extras")
        # atributo para nombre real de PDF
        self.pdf_name = None
        self.poppler_path = configurar_ocr(extras_dir=self.extras_dir)

    def descargar_pdf(self) -> str:
        try:
            r = requests.get(self.pdf_url, timeout=20)
            if r.status_code != 200:
                log_error(f"❌ Error al descargar PDF: HTTP {r.status_code}")
                return ""
            # Extraer nombre real del PDF (cabecera o URL)
            cd = r.headers.get('content-disposition', '')
            filename = None
            if cd:
                m = re.search(r"filename\*?=\"?([^;\"]+)\"?", cd)
                if m:
                    filename = m.group(1)
            if not filename:
                filename = os.path.basename(self.pdf_url)
            self.pdf_name = filename
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            tmp.write(r.content)
            tmp.close()
            log_info(f"📥 PDF descargado: {self.pdf_url} -> {filename}")
            return tmp.name
        except Exception as e:
            log_error(f"❌ Excepción descargando PDF: {e}")
            return ""

    def _extraer_con_pdfplumber(self, pdf_path: str) -> list[dict]:
        filas = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    for table in tables:
                        if not table or len(table) < 2:
                            continue
                        header = [str(h).strip() if h else "" for h in table[0]]
                        if any("Simb" in h for h in header):
                            for row in table[1:]:
                                if len(row) < 7:
                                    continue
                                sim, name, antes, est, mod, comp, coef = row[:7]
                                filas.append({
                                    "simbolo": sim.strip() if sim else "",
                                    "nombre": name.strip() if name else "",
                                    "titulos_antes": (antes.replace(".", "").replace(",", ".").strip()
                                                      if antes else ""),
                                    "estatus": None if est in ("-", "", None) else est.strip(),
                                    "modificaciones": "" if mod in ("-", "", None)
                                    else mod.replace(".", "").replace(",", ".").strip(),
                                    "comp": (comp.replace(".", "").replace(",", ".").strip()
                                             if comp else ""),
                                    "coef_ff": coef.strip() if coef else "",
                                    "fecha_insercion": datetime.now().date(),
                                    "nombre_pdf": self.pdf_name
                                })
            log_info(f"📊 Se extrajeron {len(filas)} filas con pdfplumber.")
        except Exception as e:
            log_error(f"❌ Error con pdfplumber: {e}")
        return filas

    def _extraer_texto_fitz(self, pdf_path: str) -> str:
        try:
            doc = fitz.open(pdf_path)
            txt = "".join(page.get_text("text") + "\n" for page in doc)
            doc.close()
            return txt
        except Exception as e:
            log_error(f"❌ Error abriendo PDF en PyMuPDF: {e}")
            return ""

    def _limpiar_lineas(self, texto: str) -> list[str]:
        marcador = "Composición del índice IBEX 35"
        idx = texto.find(marcador)
        if idx >= 0:
            texto = texto[idx + len(marcador):]
        return [l.strip() for l in texto.splitlines() if l.strip()]

    def _parsear_lineas(self, lines: list[str], pdf_path: str) -> list[dict]:
        filas = []
        PAT = re.compile(
            r"^([A-Z]{2,5})\s+"  # símbolo
            r"(.+?)\s+"  # nombre (mínimo espacio)
            r"([\d\.]+)\s+"  # títulos antes
            r"(-[\d\.]+|[\d\.]+|-)\s+"  # modificaciones (número o guion)
            r"([\d\.]+)\s+"  # comp
            r"(\d{1,3})$"  # coef_ff
        )
        for l in lines:
            m = PAT.match(l)
            if m:
                simbolo, nombre, tit, mod, comp, coef = m.groups()
                filas.append({
                    "simbolo": simbolo,
                    "nombre": nombre.strip(),
                    "titulos_antes": tit.replace(".", ""),
                    "estatus": None,
                    "modificaciones": "" if mod == "-" else mod.replace(".", ""),
                    "comp": comp.replace(".", ""),
                    "coef_ff": coef,
                    "fecha_insercion": datetime.now().date(),
                    "nombre_pdf": self.pdf_name
                })
            else:
                log_info(f"⚠️ Línea ignorada por no coincidir: {l}")
        if filas:
            log_info(f"📊 (_parsear_lineas) Se extrajeron {len(filas)} filas de la tabla.")
        return filas

    def _parsear_bloque(self, bloque: str, pdf_path: str) -> list[dict]:
        PAT = re.compile(
            r"(?:%Coef\s+)?(?:FF\s+)?([A-Z]{2,5})\s+"  # símbolo, ignorando posibles prefijos como '%Coef FF'
            r"([A-Z][A-Z\s\.\-&]{2,})\s+"  # nombre en mayúsculas con espacios o puntos
            r"([\d.]+)\s+"  # títulos antes
            r"(-?[\d.]+|-)\s+"  # modificaciones
            r"([\d.]+)\s+"  # composición
            r"(\d{1,3})\b"  # coeficiente
        )

        flat = " ".join(bloque.split())
        matches = PAT.findall(flat)

        filas = []
        for m in matches:
            s, nombre, tit, mod, comp, coef = m

            # ⛔ Ignorar líneas tipo 'IBEX ENERGÍA'
            if s.upper().startswith("IBEX"):
                continue

            filas.append({
                "simbolo": s.strip(),
                "nombre": nombre.strip(),
                "titulos_antes": tit.replace(".", ""),
                "estatus": None,
                "modificaciones": "" if mod in ("-", "–", "−") else mod.replace(".", ""),
                "comp": comp.replace(".", ""),
                "coef_ff": coef.strip(),
                "fecha_insercion": datetime.now().date(),
                "nombre_pdf": self.pdf_name
            })

        if filas:
            log_info(f"📊 (_parsear_bloque) Se extrajeron {len(filas)} filas de la tabla.")
        return filas


    def extraer_tabla(self, pdf_path: str) -> list[dict]:
        """
        Extrae la tabla del IBEX 35® desde el PDF dado.
        Utiliza primero fitz (PyMuPDF); si falla, intenta con pdfplumber; si todo falla, intenta OCR.
        """
        # 1) Extraer texto con fitz
        texto = self._extraer_texto_fitz(pdf_path)
        flat = " ".join(texto.split())

        # Buscar bloque desde el primer patrón completo de fila detectado
        match = re.search(
            r"[A-Z]{2,5}\s+[\w\.\s&\-ÁÉÍÓÚÑÜ]+?\s+[\d\.]+\s+(?:-[\d\.]+|[\d\.]+|-)\s+[\d\.]+\s+\d{1,3}",
            flat
        )
        if match:
            bloque = flat[match.start():]
            datos = self._parsear_bloque(bloque, pdf_path)
            datos = self._limpiar_datos(datos)
            if datos and len(datos) == 35:
                log_info("✅ Datos extraídos usando PyMuPDF (fitz).")
                return datos

        # 2) Si no ha funcionado, usar pdfplumber
        datos_pdfplumber = self._extraer_con_pdfplumber(pdf_path)
        datos_pdfplumber = self._limpiar_datos(datos_pdfplumber)
        if datos_pdfplumber and len(datos_pdfplumber) == 35:
            log_info("✅ Datos extraídos usando pdfplumber.")
            return datos_pdfplumber

        # 3) Si sigue sin funcionar, OCR (si disponible)
        texto_ocr = extraer_texto_ocr(pdf_path, self.poppler_path)
        if texto_ocr:
            datos_ocr = self._parsear_bloque(texto_ocr, pdf_path)
            datos_ocr = self._limpiar_datos(datos_ocr)
            if datos_ocr and len(datos_ocr) == 35:
                log_info("✅ Datos extraídos usando OCR (Tesseract).")
                return datos_ocr

        # 4) Si todo falla, devolver lista vacía
        return []

    def _limpiar_datos(self, datos: list[dict]) -> list[dict]:
        """
        Limpia los datos eliminando entradas no válidas y dejando exactamente las 35 empresas.
        """
        # Filtrar entradas que empiecen por 'IBEX' o estén corruptas
        datos_filtrados = [
            d for d in datos
            if d.get("simbolo")
               and d.get("nombre")
               and not d["simbolo"].startswith("IBEX")
        ]

        # Eliminar duplicados por símbolo
        simbolos_vistos = set()
        datos_unicos = []
        for d in datos_filtrados:
            s = d["simbolo"]
            if s not in simbolos_vistos:
                simbolos_vistos.add(s)
                datos_unicos.append(d)

        # Ordenar alfabéticamente por símbolo
        datos_ordenados = sorted(datos_unicos, key=lambda x: x["simbolo"])

        return datos_ordenados

    def ejecutar(self):
        log_info("🚀 Iniciando scraping de PDF del IBEX 35")
        pdf_path = self.descargar_pdf()
        if not pdf_path:
            log_error("❌ No se descargó el PDF; abortando.")
            return

        datos = self.extraer_tabla(pdf_path)
        if not datos:
            log_error("❌ No se extrajeron datos del PDF.")
        else:
            for d in datos:
                simbolo = d.get("simbolo", "").strip()
                nombre = d.get("nombre", "").strip()
                coef = d.get("coef_ff", "").strip()

                # En lugar de filtrar por 'IBEX', filtramos por ausencia de datos clave
                if not simbolo or not nombre or not coef:
                    log_info(f"⚠️ Fila ignorada por falta de datos clave: {d}")
                    continue

                ok = insertar_datos_composicion(d)
                tag = "📥" if ok else "📛"
                log_info(f"{tag} {simbolo} – {nombre}")

        try:
            os.remove(pdf_path)
            log_info("🗑️ PDF temporal eliminado.")
        except Exception as e:
            log_error(f"❌ No se pudo eliminar temporal: {e}")

        log_info("✅ Scraping de PDFs de IBEX 35 completado.")

def ejecutar_scraping_pdf():
    IbexPDFScraper().ejecutar()

if __name__ == "__main__":
    ejecutar_scraping_pdf()





















