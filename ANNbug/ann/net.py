'''
@since: 20 Jan 2012
@author: oblivion
'''
import layer
import log
import uuid


class Net(object):
    '''
    A neural network.
    '''
    def __init__(self, n_inputs, n_outputs, n_hidden_layers, n_neurons):
        '''
        Constructor.

        @param n_hidden_layers: Number of hidden layers.
        @type n_hidden_layers: int
        @param n_inputs: Numper of inputs.
        @type n_inputs: int
        @param n_outputs: Numper of outputs.
        @type n_outputs: int
        @param n_neurons: Number of neurons in the hidden layer(s).
        @type n_neurons: int
        '''
        log.logger.debug('Creating a neural net')
        self.id = str(uuid.uuid4())
        log.logger.debug('ID: ' + self.id)
        self.layers = list()
        #Input layer
        self.layers.append(layer.Layer(n_inputs, n_inputs))
        #Create first hidden layer
        self.layers.append(layer.Layer(n_neurons, n_inputs))
        #Create following hidden layer(s)
        for _i in range(2, n_hidden_layers):
            self.layers.append(layer.Layer(n_neurons, n_neurons))
        #Create output layer and connection
        self.layers.append(layer.Layer(n_outputs, n_neurons))
        #Create inputs and outputs
        self.inputs = None
        self.output = None

    def update(self, value):
        log.logger.debug('Updating net: ' + self.id)
        self.inputs = value
        #Set inputs in the input layer
        self.layers[0].inputs = value
        #Update all layers
        last_output = value
        for net_layer in self.layers:
            net_layer.inputs = last_output
            net_layer.update()
            last_output = net_layer.outputs
            
        self.output = last_output
        log.logger.debug('Output: ' + str(self.output))

    def neuron_count(self):
        '''
        Get the number of neurons in the network.
        '''
        #Count neurons in each layer
        ret = 0
        for n_layer in self.layers:
            ret += len(n_layer.neurons)
        return(ret)