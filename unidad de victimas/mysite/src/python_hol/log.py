'''
Created on 18/11/2014

@author: afvenegas10
'''

import logging
from datetime import date

logging.basicConfig(
                    level=logging.DEBUG,
                    filename = 'C:/Users/andres/git/'+'web/mysite/log/'+'UndVictimas'+str(date.today())+'.log',
                    datefmt="%Y-%m-%d %H:%M:%S",
                    format='%(asctime)s.%(msecs)d %(levelname)s %(module)s - %(funcName)s: %(message)s') 

def error(msg):  
    logging.debug(msg)
    print msg

def info(msg):
    logging.error(msg)
    print msg