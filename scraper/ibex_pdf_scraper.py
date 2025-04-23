import os
import re
import tempfile
import requests
from datetime import datetime
import platform
import zipfile

import fitz           # PyMuPDF
import pdfplumber     # pip install pdfplumber
# OCR fallback:
try:
    from pdf2image import convert_from_path  # pip install pdf2image
    import pytesseract                       # pip install pytesseract
except ImportError:
    convert_from_path = None
    pytesseract = None

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
        self.poppler_path = self._configurar_poppler()
        self._configurar_tesseract()

    def _configurar_poppler(self) -> str:
        if platform.system() != "Windows":
            return None
        base = os.path.join(os.getcwd(), "poppler")
        zip_path = os.path.join(self.extras_dir, "poppler.zip")
        if not os.path.isdir(base) or not any(
            f.lower().endswith(".exe")
            for _, _, files in os.walk(base)
            for f in files
        ):
            if not os.path.isfile(zip_path):
                log_error("❌ No se encontró 'poppler.zip' en extras/.")
                return None
            try:
                with zipfile.ZipFile(zip_path, "r") as z:
                    z.extractall(base)
                log_info("🧩 Poppler descomprimido automáticamente.")
            except Exception as e:
                log_error(f"❌ Error al descomprimir poppler.zip: {e}")
                return None
        for root, _, files in os.walk(base):
            if "pdftoppm.exe" in files:
                log_info(f"🔧 Poppler configurado en: {root}")
                return root
        log_error("❌ Poppler descomprimido pero faltan binarios.")
        return None

    def _configurar_tesseract(self):
        if platform.system() != "Windows" or pytesseract is None:
            return
        base = os.path.join(os.getcwd(), "tesseract")
        zip_path = os.path.join(self.extras_dir, "tesseract.zip")
        if not any(
                f.lower() == "tesseract.exe"
                for _, _, files in os.walk(base)
                for f in files
        ):
            if not os.path.isfile(zip_path):
                log_error("❌ No se encontró 'tesseract.zip' en extras/. OCR no funcionará.")
                return
            try:
                with zipfile.ZipFile(zip_path, "r") as z:
                    z.extractall(base)
                log_info("🧠 Tesseract descomprimido automáticamente.")
            except Exception as e:
                log_error(f"❌ Error al descomprimir tesseract.zip: {e}")
                return

        for root, _, files in os.walk(base):
            if "tesseract.exe" in files:
                exe = os.path.join(root, "tesseract.exe")
                pytesseract.pytesseract.tesseract_cmd = exe
                tessdata_dir = os.path.join(os.path.dirname(exe), "tessdata")
                os.environ["TESSDATA_PREFIX"] = os.path.dirname(tessdata_dir)
                if not os.path.exists(os.path.join(tessdata_dir, "spa.traineddata")):
                    log_error("❌ Falta 'spa.traineddata' en tessdata.")
                else:
                    log_info(f"🔍 Tesseract configurado en: {exe}")
                return
        log_error("❌ Tesseract descomprimido pero no se encontró tesseract.exe.")

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

    def _extraer_texto_ocr(self, pdf_path: str) -> str:
        try:
            imgs = convert_from_path(pdf_path,
                                     dpi=300,
                                     poppler_path=self.poppler_path)
            texto = ""
            for img in imgs:
                texto += pytesseract.image_to_string(img, lang="spa") + "\n"
            return texto
        except Exception as e:
            log_error(f"❌ Error en OCR del PDF: {e}")
            return ""

    def _limpiar_lineas(self, texto: str) -> list[str]:
        marcador = "Composición del índice IBEX 35"
        idx = texto.find(marcador)
        if idx >= 0:
            texto = texto[idx + len(marcador):]
        return [l.strip() for l in texto.splitlines() if l.strip()]

    def _parsear_lineas(self, lines: list[str], pdf_path: str) -> list[dict]:
        filas = []
        for l in lines:
            match = re.match(
                r"^([A-Z]{2,5})\s+(.+?)\s+([\d\.]+)\s+(?:-?([\d\.]*))?\s+([\d\.]+)\s+(\d{2,3})$",
                l
            )
            if match:
                simbolo, nombre, tit, mod, comp, coef = match.groups()
                filas.append({
                    "simbolo": simbolo,
                    "nombre": nombre.strip(),
                    "titulos_antes": tit.replace(".", ""),
                    "estatus": None,
                    "modificaciones": "" if not mod else mod.replace(".", ""),
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
        flat = " ".join(bloque.split())
        partes = re.split(r'(?<=\d)\s+(?=[A-Z]{2,5}\s)', flat)
        PAT = re.compile(
            r"^([A-Z]{2,5})\s+"
            r"(.+?)\s+"
            r"([\d\.]+)\s+"
            r"(-[\d\.]+|[\d\.]+|-)\s+"
            r"([\d\.]+)\s+"
            r"(\d{1,3})$"
        )
        filas = []
        for p in partes:
            texto = p.strip()
            m = PAT.match(texto)
            if not m:
                log_info(f"⚠️ No coincide parte: {texto}")
                continue
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
        if filas:
            log_info(f"📊 (_parsear_bloque) Se extrajeron {len(filas)} filas de la tabla.")
        return filas

    def extraer_tabla(self, pdf_path: str) -> list[dict]:
        texto = self._extraer_texto_fitz(pdf_path)
        marcadores = [
            "Composición del índice IBEX 35® a partir",
            "Composición del índice IBEX 35 a partir",
            "Composición del índice IBEX 35",
        ]
        bloque = None
        for marcador in marcadores:
            pos = texto.find(marcador)
            if pos >= 0:
                bloque = texto[pos + len(marcador):]
                break
        if bloque:
            datos = self._parsear_bloque(bloque, pdf_path)
            if datos:
                return datos
        else:
            log_error("❌ No se encontró ningún marcador reconocible en el PDF.")
        datos_pdfplumber = self._extraer_con_pdfplumber(pdf_path)
        if datos_pdfplumber:
            return datos_pdfplumber
        if convert_from_path:
            texto_ocr = self._extraer_texto_ocr(pdf_path)
            return self._parsear_bloque(texto_ocr, pdf_path)
        return []

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
                if simbolo.upper() == "IBEX":
                    log_info(f"⚠️ Fila de sección ignorada: {d}")
                    continue
                if not simbolo or not nombre:
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





















