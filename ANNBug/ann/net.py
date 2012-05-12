'''
@since: 20 Jan 2012
@author: oblivion
'''
import layer
import connection
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
        self.hidden_layers = list()
        #List of all connections
        self.connections = list()
        #Create inputs and connection
        con = connection.Connection()
        self.connections.append(con)
        self.input_layer = layer.Layer(n_inputs, con)
        #Create hidden layer(s) and connections
        for _i in range(n_hidden_layers):
            con = connection.Connection()
            self.connections.append(con)
            self.hidden_layers.append(layer.Layer(n_neurons, con))
        #Create output layer and connection
        con = connection.Connection()
        self.connections.append(con)
        self.output_layer = layer.Layer(n_outputs, con)
        #Create inputs and outputs
        self.inputs = None
        self.outputs = None
        self.input_layer.output.add_receiver(self.hidden_layers[0])
        #Create connections for the hidden layers
        for i in range(len(self.hidden_layers)):
            if i != (len(self.hidden_layers) - 1):
                self.hidden_layers[i].output.add_receiver(self.hidden_layers[i])
        #Connect the output layer
        self.hidden_layers[-1].output.add_receiver(self.output_layer)

    def update(self, value):
        log.logger.debug('Updating net: ' + self.id)
        self.inputs = value
        self.input_layer.update(value)
        self.output = self.output_layer.output.value
        log.logger.debug('Output: ' + str(self.output))
