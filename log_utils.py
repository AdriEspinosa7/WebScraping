import logging

def configurar_logger():
    """
    Configura el logger principal del proyecto para escribir en 'log.txt'.
    Asegura que no se añadan múltiples handlers si ya hay uno configurado.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.FileHandler('log.txt', encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

# Configurar logger al importar el módulo
configurar_logger()

# Funciones auxiliares para registrar mensajes
def log_info(mensaje):
    logging.info(mensaje)

def log_error(mensaje):
    logging.error(mensaje)






