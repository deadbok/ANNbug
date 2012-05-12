'''
@since: 21 Jan 2012
@author: oblivion
'''


class Connection(object):
    '''
    Class to connect neurons.
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.value = 0
        self.receivers = list()

    def send(self, value):
        '''Send a value to a receiver.'''
        self.value = value
        for receiver in self.receivers:
            receiver.update(value)

    def add_receiver(self, receiver):
        '''Add a receiver'''
        self.receivers.append(receiver)
