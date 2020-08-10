# https://stackoverflow.com/questions/19846332/python-threading-inside-a-class#19846691

import threading
import logging

def threaded(fn):
    def wrapper(*args, **kwargs):
        logging.debug('Creating new thread...')
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper