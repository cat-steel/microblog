import logging

def log():
    logger = logging.getLogger()
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler('app\\log\\test.log')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s---%(levelname)s---%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger