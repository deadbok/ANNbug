'''
@since: 21 Jan 2012
@author: oblivion
'''
from ann import genetic
import logging
import log
import random

#Jan 21, 2012 version 0.1
#    Getting the basics straight.
VERSION = 0.1


def main():
    '''Main entry point.'''
    log.init_file_log(logging.DEBUG)
    log.init_console_log()

    log.logger.info("ANNbug V" + str(VERSION))

    brains = list()   
    log.logger.info("Creating initial brains...") 
    for i in range(20):
        log.logger.debug("Creating initial brain number: " + str(i))
        brains.append(genetic.Genetic(2, 1, 1, 3))

    for brain in brains:
        print(str(brain))

if __name__ == '__main__':
    main()
