'''
Genetic algorithms to evolve the network.

hgh@since: Jun 3, 2012
@author: oblivion
'''
import net


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
        #Chromosome
        self.chromosome = self.net.get_weights()

    def __str__(self):
        '''
        Return the chromosome as a string.
        '''
        return(str(self.chromosome))

    def fitness(self, answer):
        '''
        Return the fitness of the chromosome, by comparing the
        output with the right answer.
        
        @param answer: The expected output of the network.
        @type answer: object
        '''
        #Both output and answer are equal, max fitness!
        fitness = 0
        if answer == self.net.output:
            return(1000)
        ret = 0
        for _i, o_val in enumerate(self.net.output):
            if answer[_i] == o_val:
                ret += 1000
            elif answer[_i] == 0:
                fitness = 1 / abs(o_val)
            else:
                fitness = 1 / abs(answer[_i] - o_val)
            ret += fitness
        ret = ret / len(answer)
        return(ret)

    def update(self, value):
        self.net.update(value)

    def change(self, chromosome):
        '''
        Change the chromosome of the net.
        '''
        self.net.set_weights(chromosome)
