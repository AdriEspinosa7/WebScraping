import logging

def configurar_logger():
    """
    Configura el logger principal del proyecto para escribir en 'log.txt'
    y mostrar los mensajes también por consola.
    Asegura que no se añadan múltiples handlers si ya hay uno configurado.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

        # Handler para archivo
        file_handler = logging.FileHandler('log.txt', encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

# Configurar logger al importar el módulo
configurar_logger()

# Funciones auxiliares para registrar mensajes
def log_info(mensaje):
    logging.info(mensaje)

def log_error(mensaje):
    logging.error(mensaje)







