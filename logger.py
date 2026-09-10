import logging
from unicodedata import name

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)

def get_logger(name):
    return logging.getLogger(name)