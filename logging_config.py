# logging_config.py

import logging
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(name)s: %(message)s",
        },
    },
    "handlers": {
        "file_handler": {
            "class": "logging.FileHandler",
            "filename": "operations.log",
            "formatter": "default",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["file_handler", "console"]
    },
}
