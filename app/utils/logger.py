import logging
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG_DIR = os.path.join(ROOT_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger():   
    logger = logging.getLogger(__name__)
    
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        "{asctime} - {name} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    file_handler = logging.FileHandler(os.path.join(LOG_DIR, "app.log"))
    console_handler = logging.StreamHandler()
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    file_handler.setLevel(logging.DEBUG)
    console_handler.setLevel(logging.DEBUG)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger()