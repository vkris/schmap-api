import os, sys
sys.path.append(".")
import logging


def getLog():
    format_string = "%(asctime)s %(name)s [%(levelname)s]:%(message)s"
    level = 'INFO'
    logger = logging.getLogger('schmap_api')
    logger.setLevel(level)
    #lhandler = logging.FileHandler("schmap_api.log")
    lhandler = logging.StreamHandler()
    lhandler.setLevel(level)
    fm = logging.Formatter(format_string)
    lhandler.setFormatter(fm)
    logger.addHandler(lhandler)
    return logger

def client(username, password,output_dir=""):
    from schmap_api.client_api import SchmapAPIClient
    return SchmapAPIClient(username, password,"","",output_dir)

log = getLog()

