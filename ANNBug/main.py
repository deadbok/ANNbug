'''
@since: 21 Jan 2012
@author: oblivion
'''
from ann import net
import logging
import log

#Jan 21, 2012 version 0.1
#    Getting the basics straight.
VERSION = 0.1


def main():
    '''Main entry point.'''
    log.init_file_log(logging.DEBUG)
    log.init_console_log()

    log.logger.info("ANNbug V" + str(VERSION))

    brain = net.Net(2, 1, 1, 3)
    brain.update([2, 2])

    print(str(brain))
    print(str(brain.output))

if __name__ == '__main__':
    main()
