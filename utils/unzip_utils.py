import os
import zipfile

def descomprimir_si_no_existe(archivo_zip, carpeta_destino):
    if not os.path.exists(carpeta_destino):
        print(f"🔧 Descomprimiendo {archivo_zip}...")
        with zipfile.ZipFile(archivo_zip, 'r') as zip_ref:
            zip_ref.extractall(carpeta_destino)
        print(f"✅ Descomprimido en {carpeta_destino}")
    else:
        print(f"📦 {carpeta_destino} ya existe. No se descomprime.")
