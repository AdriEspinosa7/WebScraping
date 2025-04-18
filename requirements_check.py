import subprocess
import sys

# Lista de paquetes PyPI requeridos
requisitos = [
    "selenium",
    "beautifulsoup4",
    "pymupdf",
    "mysql-connector-python",
    "requests",
    "pdfplumber",
    "pdf2image",
    "pytesseract"
]

def instalar_paquete(paquete):
    """
    Verifica si el módulo correspondiente está importable, y si no,
    lo instala vía pip.
    """
    print(f"📦 Verificando {paquete}...")
    # Mapear nombre de paquete → nombre de módulo para __import__
    nombre_modulo = {
        "beautifulsoup4": "bs4",
        "mysql-connector-python": "mysql.connector",
        "pymupdf": "fitz"
    }.get(paquete, paquete)

    try:
        __import__(nombre_modulo)
        print(f"✅ {paquete} ya está instalado.")
    except ImportError:
        print(f"❌ {paquete} no está instalado. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", paquete])
        print(f"✅ {paquete} instalado correctamente.")

def main():
    print("🔍 Verificando dependencias del proyecto...\n")
    for paquete in requisitos:
        instalar_paquete(paquete)
    print("\n✅ Todas las dependencias están listas.")

if __name__ == "__main__":
    main()

