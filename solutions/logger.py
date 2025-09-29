import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create logger instance
logger = logging.getLogger('soundproofing')
logger.setLevel(logging.INFO)

# Add console handler if you want to see logs in terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Add file handler for persistent logs
try:
    log_file = os.path.join(logs_dir, f'soundproofing_{datetime.now().strftime("%Y%m%d")}.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)  # More detailed logging to file
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
except Exception as e:
    logger.warning(f"Could not create log file: {e}")

def get_logger():
    """Get the configured logger instance.
    
    Returns:
        logging.Logger: The configured logger instance for the soundproofing application.
    """
    return logger

# Define convenience methods for common logging patterns
def log_error(message: str, exc: Exception = None):
    """Log an error message with optional exception details."""
    if exc:
        logger.error(f"{message}: {str(exc)}")
    else:
        logger.error(message)

def log_warning(message: str):
    """Log a warning message."""
    logger.warning(message)

def log_info(message: str):
    """Log an info message."""
    logger.info(message)

def log_debug(message: str):
    """Log a debug message."""
    logger.debug(message) 