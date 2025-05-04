import logging
from pathlib import Path

def configurar_logger():
    """
    Configura el logger para escribir en 'log.txt' en la raíz del proyecto,
    sin importar desde qué subcarpeta se ejecute el script.
    Elimina cualquier handler existente para evitar duplicados.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Eliminar handlers previos (si los hubiera)
    for handler in list(logger.handlers):
        logger.removeHandler(handler)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

    # Carpeta raíz del proyecto (subimos desde utils/)
    proyecto_raiz = Path(__file__).resolve().parent.parent
    ruta_log = proyecto_raiz / "log.txt"

    # Crear handler de archivo
    file_handler = logging.FileHandler(ruta_log, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Crear handler de consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Evitar propagación a handlers superiores
    logger.propagate = False

    return logger

# Configurar logger al importar el módulo
logger = configurar_logger()

# Funciones auxiliares

def log_info(mensaje):
    logger.info(mensaje)

def log_error(mensaje):
    logger.error(mensaje)














