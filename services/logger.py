import logging
from rich.logging import RichHandler

def setup_logger(name="GoMusic"):
    """Create a logger with rich handler."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    console_handler = RichHandler(rich_tracebacks=True)
    formatter = logging.Formatter("%(message)s")
    console_handler.setFormatter(formatter)
    
    if not logger.hasHandlers():
        logger.addHandler(console_handler)
    
    return logger

logger = setup_logger()
