"""Logger implementation."""

import logging
from typing import Optional

from qgis.core import Qgis, QgsMessageLog

from cgiqgispluginsandboxday.constants import PLUGIN_NAME

logger: Optional[logging.Logger] = None


class QgisLogHandler(logging.Handler):
    """Log handler emitting log event to QgsMessageLog."""

    def __init__(self, level: int = logging.DEBUG) -> None:
        """Initialize the handler."""
        logging.Handler.__init__(self, level=level)

    def emit(self, record: logging.LogRecord) -> None:
        """Emit the log record."""
        if record.levelno in (logging.ERROR, logging.CRITICAL):
            qgis_level = Qgis.MessageLevel.Critical
        elif record.levelno == logging.WARNING:
            qgis_level = Qgis.MessageLevel.Warning
        else:
            qgis_level = Qgis.MessageLevel.Info

        QgsMessageLog.logMessage(self.format(record), PLUGIN_NAME, qgis_level)


def remove_logger() -> None:
    """Remove the logger."""
    global logger

    if logger is not None:
        for handler in logger.handlers:
            if isinstance(handler, logging.FileHandler):
                handler.close()
            logger.removeHandler(handler)
        logger = None


def init_logger() -> logging.Logger:
    """Initialize the logger."""
    global logger

    if logger is not None:
        return logger

    logger = logging.getLogger(PLUGIN_NAME)

    # set the level
    logger.setLevel(logging.INFO)

    log_formatter = logging.Formatter(
        "%(filename)s:%(funcName)s():%(lineno)d : %(message)s",
        "%d.%m.%Y %H:%M:%S",
    )

    # add qgis logging
    qgis_handler = QgisLogHandler()
    qgis_handler.setFormatter(log_formatter)
    logger.addHandler(qgis_handler)

    logger.info("Plugin logging initialized")

    return logger


def get_logger() -> logging.Logger:
    """Get the logger."""
    if logger is None:
        return init_logger()

    return logger
