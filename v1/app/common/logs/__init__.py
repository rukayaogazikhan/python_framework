#!/usr/bin/env python3.6
import logging
import os
from logging.handlers import RotatingFileHandler
import os


def rotational_logger(log_name):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    handler = RotatingFileHandler(log_name + '.log', maxBytes=10*1024*1024, backupCount=5)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

project_name = os.path.basename(os.path.abspath(os.path.join(os.getcwd(), '../../../', os.pardir)))
logger = rotational_logger(os.path.join(os.path.dirname(__file__), '../../logs', project_name))