                                                 
import logging
from os import path
logging.basicConfig(filename="log.log", filemode='a', format="\n\n%(asctime)s   %(levelname)s: %(message)s\n")

def logger(msg, mode='warning'):
    if mode == 'warning':
        logging.warning(msg, exc_info=False)
    elif mode == 'exception':
        logging.exception(msg, exc_info=True)
    elif mode == 'info':
        logging.info(msg)

def etc(msg):
    filename = "search.log"
    if path.exists(filename) == True:
        f = open(filename, "a")
    else:
        f = open(filename, "x")
        f.close()
        f = open(filename, "w")
    f.write(msg)
    f.close()