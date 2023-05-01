# Contiene las configuraciones para inicializar
# logger
# cuando se llame
# loggin.getLogger(LOGGER_NAMNE)
# obtendra la misma instancia a traves de la aplicacion

import logging
import sys
from logging.handlers import TimedRotatingFileHandler

LOG_FILE = "app_logs.log"
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s- %(module)s - %(funcName)s - %(lineno)d - %(message)s'
LOGGER_NAME = "app"


def init() -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    # handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    # Escribe en archivo
    logger.addHandler(__get_file_handler())


def __get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    return file_handler
