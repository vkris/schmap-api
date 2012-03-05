import os, sys
sys.path.append(".")
import logging

format_string = "%(asctime)s %(name)s [%(levelname)s]:%(message)s"
level = 'INFO'
logger = logging.getLogger('schmap_api')
logger.setLevel(level)
lhandler = logging.FileHandler("schmap_api.log")
lhandler.setLevel(level)
fm = logging.Formatter(format_string)
lhandler.setFormatter(fm)
logger.addHandler(lhandler)
log = logger
