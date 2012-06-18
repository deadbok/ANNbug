'''
@since: 20 Jan 2012
@author: oblivion
'''
import random
import log
import uuid
import math


class Neuron(object):
    '''Basic neuron.'''
    def __init__(self, n_inputs):
        '''
        Construct a neuron.

        @param n_inputs: Number of inputs.
        @type n_inputs: int. 
        '''
        log.logger.debug('Creating a neuron')
        self.id = str(uuid.uuid4())
        log.logger.debug('ID: ' + self.id)
        self.weights = None
        self.threshold = random.uniform(-1, 1)
        log.logger.debug('Treshold: ' + str(self.threshold))
        #Connections
        self.output = 0
        log.logger.debug('Creating ' + str(n_inputs) + ' inputs')
        self.inputs = list()
        for _i in range(n_inputs):
            self.inputs.append(0)
        self.generate_weights()
        
    def generate_weights(self):
        '''
        Generate the weights for the neuron.
        '''
        log.logger.debug('Creating weights')
        self.weights = list()
        for _i in range(len(self.inputs)):
            self.weights.append(random.uniform(-1, 1))    

    def get_activation(self):
        '''Get the activation value.'''
        log.logger.debug('Calculating activation value for: ' + self.id)
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
        self.output = self.sigmoid(a_val, 1)
#        self.output = a_val
        log.logger.debug('Output: ' + str(self.output))

    def sigmoid(self, activation, response):
        '''Sigmoid function to smooth out the output.'''
        return(1 / (1 + math.exp(-activation / response)))

        
