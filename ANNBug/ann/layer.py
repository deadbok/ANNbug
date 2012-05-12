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
    def __init__(self, n_neurons, con):
        '''
        Constructor.

        @param n_neurons: Number of neurons in the layer.
        @type n_neurons: int
        @param n_inputs: Number of inputs per neuron.
        @type n_inputs: int
        '''
        log.logger.debug('Creating a neural net')
        self.id = str(uuid.uuid4())
        log.logger.debug('ID: ' + self.id)
        self.neurons = list()
        for i in range(n_neurons):
            self.neurons.append(neuron.Neuron())
            self.neurons[i].inputs = [0 for _j in range(n_neurons)]
        self.output = con

    def update(self, value):
        '''Update the output.'''
        log.logger.debug('Updating layer: ' + self.id)
        for n in self.neurons:
            n.inputs = value
            n.update()
        self.output.send([outp.output for outp in self.neurons])
