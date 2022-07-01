import logging
import os
import sys
from logging import StreamHandler, getLogger

logger = getLogger("app")
logger.propagate = False
handler = StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('[%(levelname)s] %(pathname)s:%(lineno)d "%(message)s"'))
handler.setLevel(os.getenv("LOG_HANDLER_LEVEL", "DEBUG"))
logger.setLevel(os.getenv("LOG_LOGGER_LEVEL", "DEBUG"))
logger.addHandler(handler)
