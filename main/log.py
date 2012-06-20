import logging

DEBUG = logging.DEBUG
INFO = logging.INFO

class Log(object):
    def __init__(self, filename = 'logfile.log'):
        self.filename = filename

    def ini(self):

        # create a logger
        logg = logging.getLogger('Main')
        logg.setLevel(logging.DEBUG)

        # create a handler and set level
        logg_ch = logging.StreamHandler()
        logg_fh = logging.FileHandler(self.filename, mode='a', encoding=None, delay=False)
        logg_ch.setLevel(logging.INFO)
        logg_fh.setLevel(logging.DEBUG)

        # crate a formatter and add it to the handler
        # [HH:MM:SS AM][LEVEL] Message string
        logg_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%I:%M:%S')
        logg_ch.setFormatter(logg_formatter)
        logg_fh.setFormatter(logg_formatter)

        # add ch to logger
        logg.addHandler(logg_ch) #console handler at level INFO
        logg.addHandler(logg_fh) #file handler at level DEBUG for more detail

        return logg

logg = Log('spaced.log')
logg = logg.ini()