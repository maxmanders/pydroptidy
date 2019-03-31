import logging.config

from pydroptidy import settings


def setup_logging():
    logging.config.dictConfig(settings.LOGGING)
