'''
Genetic algorithms to evolve the network.

hgh@since: Jun 3, 2012
@author: oblivion
'''
import net
import random


class Genetic(object):
    '''
    Genetic representation of the network.
    '''

    def __init__(self, n_inputs, n_outputs, n_hidden_layers, n_neurons):
        '''
        Constructor
        '''
        self.chromosome = list()
        self.net = net.Net(n_inputs, n_outputs, n_hidden_layers, n_neurons) 
        #Assign random weights for to each neuron
        #Input layer
        for neuron in self.net.layers[0].neurons:
            for i in range(n_inputs):
                if neuron.weights == None:
                    neuron.weights= list()
                neuron.weights.append(random.uniform(-1, 1))
        #Hidden layers
        for layer in self.net.layers[1:-1]:
            for neuron in layer.neurons:
                for i in range(n_neurons):
                    if neuron.weights == None:
                        neuron.weights= list()
                    neuron.weights.append(random.uniform(-1, 1))
        #Output layers
        for neuron in self.net.layers[-1].neurons:
            for i in range(n_outputs):
                if neuron.weights == None:
                    neuron.weights = list()
                neuron.weights.append(random.uniform(-1, 1))
        #Chromosome
        for layer in self.net.layers:
            for neuron in layer.neurons:
                for weight in neuron.weights:
                    self.chromosome.append(weight)
                    
    def change(self, chromosome):
        self.chromsome = chromosome
        #Create network according to DNA
        #Count inputs
        n_inputs = len(chromosome[0][0])
        #Count outputs
        n_outputs = len(chromosome[-1][0])
        #Count hidden layers
        n_hidden_layers = len(chromosome) - 2
        #Count neurons in the hidden layers
        n_neurons = len(chromosome[1])
        #Create the net
        self.net = net.Net(n_inputs, n_outputs, n_hidden_layers, n_neurons)
        
        for i, c_layer in enumerate(chromosome):
            for j, c_neuron in enumerate(c_layer.neurons):
                c_neuron.weights = chromosome[i][j]
                
    def __str__(self):
        '''
        Return the chromosome as a string.
        '''
        return(str(self.chromosome))
        