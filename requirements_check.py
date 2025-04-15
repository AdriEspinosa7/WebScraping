import subprocess
import sys

# Lista de módulos requeridos
requisitos = [
    "selenium",
    "beautifulsoup4",
    "pymupdf",
    "mysql-connector-python",
    "requests"
]

def instalar_paquete(paquete):
    print(f"📦 Verificando {paquete}...")
    try:
        __import__(paquete.split("-")[0])  # para importar el módulo base
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
