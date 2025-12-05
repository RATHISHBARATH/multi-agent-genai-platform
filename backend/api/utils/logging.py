import logging, os
from pythonjsonlogger import jsonlogger

def get_structured_logger(name='autoscillab'):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(os.getenv('LOG_LEVEL', 'INFO'))
    return logger

logger = get_structured_logger()
