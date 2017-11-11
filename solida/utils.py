import logging
import os
import shutil
import subprocess
import sys

LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


def a_logger(name, level="WARNING", filename=None, mode="a"):
    log_format = '%(asctime)s|%(levelname)-8s|%(name)s |%(message)s'
    log_datefmt = '%Y-%m-%d %H:%M:%S'
    logger = logging.getLogger(name)
    if not isinstance(level, int):
        try:
            level = getattr(logging, level)
        except AttributeError:
            raise ValueError("unsupported literal log level: %s" % level)
        logger.setLevel(level)
    if filename:
        handler = logging.FileHandler(filename, mode=mode)
    else:
        handler = logging.StreamHandler()
    formatter = logging.Formatter(log_format, datefmt=log_datefmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def path_exists(path, logger, force=True):
    def file_missing(path, logger, force):
        if force:
            logger.error("path - {} - doesn't exists".format(path))
            sys.exit()
        return False

    return True if os.path.exists(os.path.expanduser(path)) else file_missing(
        path,
        logger,
        force)


def ensure_dir(path, force=False):
    try:
        if force and os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise


# https://stackoverflow.com/questions/11210104/check-if-a-program-exists-from-a-python-script/11210902#11210902
def is_tool(name):
    try:
        devnull = open(os.devnull, 'w')
        subprocess.Popen([name], stdout=devnull, stderr=devnull).communicate()
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            return False
    return True

