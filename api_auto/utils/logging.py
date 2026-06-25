import logging

def get_logger():
    logger = logging.getLogger(__name__)
    return logger

logger = get_logger()