import logging
from v2_one.utils.logger import setup_logger


def test_logger_setup():
    logger = setup_logger("test_logger")
    assert logger.name == "test_logger"
    assert logger.level == logging.INFO  # Default from env if not set
    assert len(logger.handlers) >= 1
