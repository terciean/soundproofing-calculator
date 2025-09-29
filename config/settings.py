"""Application settings and configuration parameters."""

from pathlib import Path
import os

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# MongoDB settings
MONGODB_SETTINGS = {
    'host': 'localhost',
    'port': 27017,
    'db_name': 'soundproofing',
    'collections': {
        'solutions': ['wallsolutions', 'ceilingsolutions', 'floorsolutions'],
        'materials': 'materials',
        'profiles': 'profiles'
    }
}

# Cache settings
CACHE_SETTINGS = {
    'enabled': True,
    'default_timeout': 300,  # 5 minutes
    'type': 'simple'  # Options: 'simple', 'redis', 'memcached'
}

# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'app.log'),
            'mode': 'a',
        },
    },
    'loggers': {
        '': {  # Root logger
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        },
    }
}

# Application settings
APP_SETTINGS = {
    'debug': True,
    'testing': False,
    'secret_key': 'your-secret-key-here',  # Change in production
    'allowed_extensions': ['jpg', 'png', 'svg'],
    'max_content_length': 16 * 1024 * 1024  # 16MB max file size
}

# Solution configuration
SOLUTION_SETTINGS = {
    'default_dimensions': {
        'length': 1.0,
        'width': 1.0,
        'height': 1.0
    },
    'measurement_units': 'metric',  # Options: 'metric', 'imperial'
    'calculation_precision': 2
}

# Error handling settings
ERROR_SETTINGS = {
    'show_detailed_errors': True,  # Set to False in production
    'log_errors': True,
    'error_log_file': os.path.join(BASE_DIR, 'error.log')
}