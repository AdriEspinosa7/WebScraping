import os
import platform
import zipfile
import tempfile
from log_utils import log_info, log_error

# OCR requerimientos
try:
    from pdf2image import convert_from_path
    import pytesseract
except ImportError:
    convert_from_path = None
    pytesseract = None


def configurar_ocr(poppler_path=None, extras_dir="extras"):
    """
    Configura Tesseract y verifica/extrae Poppler si es necesario (solo en Windows).
    Devuelve la ruta a Poppler si se encuentra/configura correctamente.
    """
    poppler_dir = None
    if platform.system() == "Windows":
        poppler_dir = _configurar_poppler(extras_dir)
        _configurar_tesseract(extras_dir)
    return poppler_dir


def _configurar_poppler(extras_dir):
    base = os.path.abspath("poppler")
    zip_path = os.path.join(extras_dir, "poppler.zip")
    if not os.path.isdir(base) or not any(
        f.lower().endswith(".exe")
        for _, _, files in os.walk(base)
        for f in files
    ):
        if not os.path.exists(zip_path):
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


def _configurar_tesseract(extras_dir):
    if platform.system() != "Windows" or pytesseract is None:
        return
    base = os.path.abspath("tesseract")
    zip_path = os.path.join(extras_dir, "tesseract.zip")

    if not os.path.exists(os.path.join(base, "tesseract.exe")):
        if not os.path.exists(zip_path):
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


def extraer_texto_ocr(pdf_path, poppler_path):
    """
    Extrae texto del PDF usando OCR (Tesseract) si está disponible.
    """
    if convert_from_path is None or pytesseract is None:
        log_error("❌ OCR no disponible (falta pdf2image o pytesseract).")
        return ""

    try:
        imgs = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)
        texto = ""
        for img in imgs:
            texto += pytesseract.image_to_string(img, lang="spa") + "\n"
        return texto
    except Exception as e:
        log_error(f"❌ Error en OCR del PDF: {e}")
        return ""
