import os as _os

LOG_LEVEL = _os.getenv("LOG_LEVEL", "INFO")
LOG_LEVEL_VENDOR = {"propagate": True, "level": "INFO"}


LOGGING = {
    "version": 1,
    "formatters": {
        "simple": {
            "format": "[%(asctime)s.%(msecs)03d] [%(levelname)s] %(module)s: %(message)s",
            "datefmt": "%Y/%m/%d %H:%M:%S",
        }
    },
    "handlers": {
        "stderr": {
            "level": LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "simple",
        }
    },
    "root": {"handlers": ["stderr"], "level": LOG_LEVEL},
    "loggers": {"dropbox": LOG_LEVEL_VENDOR, "urllib3": LOG_LEVEL_VENDOR},
}

UPLOADS_FOLDER = "/Camera Uploads"
