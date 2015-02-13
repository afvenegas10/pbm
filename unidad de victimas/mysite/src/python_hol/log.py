'''
Created on 18/11/2014

@author: afvenegas10
'''

import logging
from datetime import date


logging.basicConfig(
                    level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S",
                    filename = "C:/Apache24/logs/UndVictimas/"+"UndVictimas"+str(date.today())+".log"
                    )

def error(msg):  
    logging.debug(msg)
    print msg

def info(msg):
    logging.error(msg)
    print msg