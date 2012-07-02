'''
@since: 20 Jan 2012
@author: oblivion
'''
import neuron
import log
import uuid


class Layer(object):
    '''
    A layer in the neural net.
    '''
    def __init__(self, n_neurons, n_inputs):
        '''
        Constructor.

        @param n_neurons: Number of neurons in the layer.
        @type n_neurons: int
        @param n_inputs: Number of inputs per neuron.
        @type n_inputs: int
        '''
        log.logger.debug('Creating a neural layer')
        self.id = str(uuid.uuid4())
        log.logger.debug('ID: ' + self.id)
        self.neurons = list()
        for i in range(n_neurons):
            self.neurons.append(neuron.Neuron(n_inputs))
            self.neurons[i].inputs = [0 for _j in range(n_neurons)]
        self.inputs = list()
        self.outputs = list()

    def update(self):
        '''Update the output.'''
        log.logger.debug('Updating layer: ' + self.id)
        self.outputs = list()
        for n in self.neurons:
            n.inputs = self.inputs
            self.outputs.append(n.output)

class InputLayer(object):
    '''
    A layer in the neural net.
    '''
    def __init__(self, n_inputs):
        '''
        Constructor.

        @param n_inputs: Number of inputs per neuron.
        @type n_inputs: int
        '''
        log.logger.debug('Creating a neural input layer')
        self.id = str(uuid.uuid4())
        log.logger.debug('ID: ' + self.id)
        self.neurons = list()
        for i in range(n_inputs):
            self.neurons.append(neuron.Neuron(1))
            self.neurons[i].inputs = [0]
        self.inputs = list()
        self.outputs = list()

    def update(self):
        '''Update the output.'''
        log.logger.debug('Updating layer: ' + self.id)
        self.outputs = list()
        for _i, n in enumerate(self.neurons):
            n.inputs = [self.inputs[_i]]
            self.outputs.append(n.output)
