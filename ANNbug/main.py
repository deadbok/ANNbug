'''
@since: 21 Jan 2012
@author: oblivion
'''
from genetic import floatchromo
from genetic import algorithm
from ann import net
import logging
import log
import copy
import profile

#Jan 21, 2012 version 0.1
#    Getting the basics straight.
VERSION = 0.1

#Store the generations of anns
GENERATIONS = list()

class AnnChromosome(floatchromo.FloatChromo):
    '''
    Chromosome for an ann.
    '''
    def __init__(self, n_inputs, n_outputs, n_hidden_layers, n_neurons):
        '''
        Constructor.
        '''
        floatchromo.FloatChromo.__init__(self)
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.n_hidden_layers = n_hidden_layers
        self.n_neurons = n_neurons
        self.net = None
        self.last_fit = None

    def decode(self):
        '''
        Decode the chromosome to an ann.
        '''
        if self.data == None:
            return(None)

        self.net = net.Net(self.n_inputs, self.n_outputs, self.n_hidden_layers, self.n_neurons)
        self.net.set_weights(self.data)
        return(self.net)

    def validate(self):
        '''
        Check if the chromosome is meaningful.
        '''
        if self.data == None:
            return(False)
        else:
            return(True)

    def fitness(self, inputs, target):
        '''
        Get the fitness of the chromosome.
        '''
        self.decode()
        self.net.update(inputs)
        #Both output and answer are equal, max fitness!
        if target == self.net.output:
            return(0)
        ret = 0
        for _i, o_val in enumerate(self.net.output):
            ret += target[_i] - o_val
        ret = ret / len(target)
        log.logger.debug("Fitness: " + str(ret))
        self.last_fit = ret
        return(ret)

class AnnPopulation(algorithm.Algorithm):
    '''
    Population of ANNs.
    '''
    def __init__(self, n_inputs, n_outputs, n_hidden_layers, n_neurons):
        '''
        Constructor.
        '''
        algorithm.Algorithm.__init__(self, 5)
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.n_hidden_layers = n_hidden_layers
        self.n_neurons = n_neurons
        self.n_genes = (self.n_inputs
                        + (self.n_hidden_layers * self.n_neurons
                           * self.n_inputs)
                        + self.n_outputs * self.n_neurons)
        _i = self.population_size
        while _i > 0:
            self.population.append(AnnChromosome(self.n_inputs,
                                                 self.n_outputs,
                                                 self.n_hidden_layers,
                                                 self.n_neurons).randomise(self.n_genes))
            _i -= 1
        #Original mutation rate
        self.original_mrate = 0
        #Factor to spike mutation
        self.mfactor = 1

    def evolve(self, training_set):
        '''
        Train the neural network, by evolving the weights.
        '''
        #Save generation
        GENERATIONS.append(copy.deepcopy(self))
        #Save original mutation rate
        self.original_mrate = self.mutation_rate
        #Spike the mutation when answers the same
        self.mutation_rate *= self.mfactor
        #Maybe randomise this, so that it is not the sucsession is learned
        _n = 0
        for ts in training_set:
            _n += 1
            log.logger.info('Traning set: ' + str(_n))
            target = ts[1]
            inputs = ts[0]
            algorithm.Algorithm.evolve(self, inputs, target)
            #If we have a useful number of generations
            if len(GENERATIONS) > 1:
                #Keep a count of generations in the following loop
                _i = 0
                #Look for answer that are the same as this one
                for gen in reversed(GENERATIONS):
                    if not gen.best_fit == None:
                        if gen.best_fit.decode() == self.best_fit.decode():
                            #Ramp up the multiplication factor
                            self.mfactor *= 32
                        else:
                            #As soon as we have a different answer, stop
                            #If the last best fit is different from the current
                            if _i == 0:
                                #Reset the multiplier
                                self.mfactor = 1
                            break
                    _i += 1
            #Reset mutation rate
            self.mutation_rate = self.original_mrate
        self.generation += 1


def main():
    '''
    Genetic test program.
    '''
    log.init_file_log(logging.DEBUG)
    log.init_console_log()

    log.logger.info("ANNbug V." + str(VERSION))

    training_set = list()
    training_set.append([[0, 0], [0]])
    training_set.append([[1, 0], [1]])
    training_set.append([[0, 1], [1]])
    training_set.append([[1, 1], [0]])

    #Create initial population
    population = AnnPopulation(2, 1, 1, 4)
    population.mutation_rate = 0.001
    #Loop until an answer is found
    while not population.generation > 5:
        population.evolve(training_set)
        log.logger.info('Generation: ' + str(population.generation)
                        + ' fitness: ' + str(population.best_fit.last_fit)
                        + '\n' + str(population.best_fit.decode()))
    print('Answer(s):')
    for answer in population.answers:
        print('    ' + str(answer.decode()))

profile.run('main()')

if __name__ == '__main__':
    main()
