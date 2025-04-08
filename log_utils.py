from datetime import datetime

# Ruta del archivo de log
LOG_FILE = "log.txt"

def log_info(mensaje):
    """Registra un mensaje informativo con marca de tiempo."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[INFO] {datetime.now()} - {mensaje}\n")

def log_error(mensaje):
    """Registra un mensaje de error con marca de tiempo."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[ERROR] {datetime.now()} - {mensaje}\n")
