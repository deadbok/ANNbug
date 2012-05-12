'''
@since: 20 Jan 2012
@author: oblivion
'''
import random
import log
import uuid
import cmath


class Neuron(object):
    '''Basic neuron.'''
    def __init__(self):
        '''
        Construct a neuron.

        @param n_inputs: Number of inputs.
        '''
        log.logger.debug('Creating a neuron')
        self.id = str(uuid.uuid4())
        log.logger.debug('ID: ' + self.id)
        self.weights = None
        self.threshold = random.uniform(-1, 1)
        log.logger.debug('Treshold: ' + str(self.threshold))
        #Connections
        self.output = 0
        self.inputs = list()

    def get_activation(self):
        '''Get the activation value.'''
        log.logger.debug('Calculating activation value for: ' + self.id)
        if self.weights == None:
            log.logger.debug('Creating ' + str(len(self.inputs)) + ' weights')
            self.weights = list()
            for i in range(len(self.inputs)):
                self.weights.append(random.uniform(-1, 1))
        ret = 0
        for i in range(len(self.inputs)):
            ret += self.inputs[i] * self.weights[i]
        log.logger.debug('Activation value: ' + str(ret))
        return(ret)

    def update(self):
        '''Update the output.'''
        log.logger.debug('Updating neuron: ' + self.id)
        log.logger.debug('Inputs: ' + str(self.inputs))
        a_val = self.get_activation()
        a_val -= self.threshold
#        if a_val > 0:
#            self.output = 1
#        else:
#            self.output = 0
        self.output = self.sigmoid(a_val, 1)
        log.logger.debug('Output: ' + str(self.output))

    def sigmoid(self, activation, response):
        '''Sigmoid function to smooth ou the output.'''
        return(1 / (1 + cmath.exp(-activation / response)))
    
    def adjust(self, ratio):
        
