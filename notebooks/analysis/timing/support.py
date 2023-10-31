"""
SOME/IP support functions and variables.
"""

import logging


def create_logger(name: str):
    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter('[%(asctime)s][%(name)-14s][%(levelname)-8s] %(message)s')
    formatter.datefmt = '%H:%M:%S'
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)
    return logger
