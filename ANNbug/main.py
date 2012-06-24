'''
@since: 21 Jan 2012
@author: oblivion
'''
from genetic import chromosome
from genetic import algorithm
from ann import net
import logging
import log
import random
import copy

#Jan 21, 2012 version 0.1
#    Getting the basics straight.
VERSION = 0.1

#Store the generations of anns
GENERATIONS = list()

class AnnChromosome(chromosome.Chromosome):
    '''
    Chromosome for an ann.
    '''
    def __init__(self, n_inputs, n_outputs, n_hidden_layers, n_neurons):
        '''
        Constructor.
        '''
        chromosome.Chromosome.__init__(self)
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.n_hidden_layers = n_hidden_layers
        self.n_neurons = n_neurons
        self.net = None

    def decode(self):
        '''
        Decode the chromosome to an ann.
        '''
        if self.data == None:
            return(None)

        self.net = net.Net(self.n_inputs, self.n_outputs, self.n_hidden_layers, self.n_neurons)
        self.net.set_weights(self.data)


    def validate(self):
        '''
        Check if the chromosome is meaningful.
        '''
        if self.data == None:
            return(False)
        else:
            return(True)

    def fitness(self, target):
        '''
        Get the fitness of the chromosome.
        '''
        #Both output and answer are equal, max fitness!
        if target == self.net.output:
            return(0)
        ret = 0
        for _i, o_val in enumerate(self.net.output):
            ret += target[_i] - o_val
        ret = ret / len(target)
        log.logger.debug("Fitness: " + str(ret))
        return(ret)

class AnnPopulation(algorithm.Algorithm):
    '''
    Population of ANNs.
    '''
    def __init__(self, n_inputs, n_outputs, n_hidden_layers, n_neurons):
        '''
        Constructor.
        '''
        algorithm.Algorithm.__init__(self)
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.n_hidden_layers = n_hidden_layers
        self.n_neurons = n_neurons
        self.n_genes = self.n_inputs + (self.n_hidden_layers * self.n_neurons) + self.n_outputs
        _i = self.population_size
        while _i > 0:
            self.population.append(AnnChromosome(self.n_inputs,
                                                 self.n_outputs,
                                                 self.n_hidden_layers,
                                                 self.n_neurons).randomise_floats(self.n_genes))
            _i -= 1
        #Original mutation rate
        self.original_mrate = 0
        #Factor to spike mutation
        self.mfactor = 1

    def evolve(self, target):
        #Save generation
        GENERATIONS.append(copy.deepcopy(self))
        #Save original mutation rate
        self.original_mrate = self.mutation_rate
        #Spike the mutation when answers the same
        self.mutation_rate *= self.mfactor
        algorithm.Algorithm.evolve(self, target)
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


def select_brains(brains, result):
    '''
    Select two brains from a list of brains, based on roulette selection.
    
    @param brains: A list of brains to chose from.
    @type brains: list 
    '''
    log.logger.debug('Selecting brains.')
    min_fitness = 1001
    max_fitness = -1001
    for brain in brains:
        fitness = brain.fitness(result)
        if fitness < min_fitness:
            min_fitness = fitness
        if fitness > max_fitness:
            max_fitness = fitness
    log.logger.debug("Lowest fitness of all brains: " + str(min_fitness))
    log.logger.debug("Highest fitness of all brains: " + str(max_fitness))

    def roll():
        '''
        Select a brain.
        '''
        target_fitness = random.uniform(min_fitness, max_fitness)
        _i = -1
        fitness = 0
        if target_fitness < 0:
            total_fitness = min_fitness
            while total_fitness < target_fitness:
                _i += 1
                fitness = brains[_i].fitness(result)
                if fitness < 0:
                    total_fitness -= fitness
        elif target_fitness > 0:
            total_fitness = max_fitness
            while total_fitness > target_fitness:
                _i += 1
                fitness = brains[_i].fitness(result)
                if fitness > 0:
                    total_fitness -= fitness
        return(brains[_i])

    ret = list()
    ret.append(roll())
    ret.append(roll())
    for brain in ret:
        log.logger.debug('Selected brain has a fitness of: ' + str(brain.fitness(result)))
    return(ret)

def mutate(chromosome, mutation_rate):
    '''
    Mutate a chromosome.
    '''
    for _i in range(len(chromosome) - 1):
        if random.uniform(0, 1) < mutation_rate:
            chromosome[_i] += random.uniform(-1, 1)
    return(chromosome)

def child(pair, crossover_rate, mut_rate):
    '''
    Have a child.
    '''
    ret = copy.deepcopy(pair[0])
    if crossover_rate > random.uniform(0, 1):
        split = random.randint(1, len(pair[0].chromosome) - 1)
        childchromo = list()
        childchromo.extend(pair[0].chromosome[0:split])
        childchromo.extend(pair[1].chromosome[split:])
        log.logger.debug('A child is born: ' + str(childchromo))
        ret.change(childchromo)

    ret.change(mutate(ret.chromosome, mut_rate))
    return(ret)

def train(brains, training_set, cross_rate, mut_rate):
    '''
    Train a list of genetic networks.
    
    @param brains: A list of brains to train.
    @type brains: list
    @param training_set: A list of training inputs, and outputs
    @type training_set: list
    '''
    generation = 0
    best_fit = 1001
    while best_fit != 0:
        best_fit = 1001
        best_output = None
        for brain in brains:
            fitness = 0
            abs_fitness = 0
            output = list()
            #Run through the training set
            for ts in training_set:
                log.logger.debug('New training set: ' + str(ts))
                #This is vector math. Should code this as a distance.
                inputs = ts[0]
                result = ts[1]
                brain.update(inputs)
                fitness += brain.fitness(result)
                abs_fitness += abs(brain.fitness(result))
                output.append(brain.net.output)
            fitness = fitness / len(training_set)
            abs_fitness = abs_fitness / len(training_set)
            log.logger.debug('Fitness ' + str(fitness) + '. Absolute fitness '
                             + str(abs_fitness))
            #if fitness is closer to zero       
            if abs(best_fit) > abs(abs_fitness):
                best_fit = abs_fitness
                best_output = output
        log.logger.info("Best fit generation " + str(generation)
                        + ": " + str(best_fit) + " output " + str(best_output))
        nextgen = list()
        while len(nextgen) < len(brains):
            pair = select_brains(brains, result)
            log.logger.debug("Pairing brains with " + str(pair[0].fitness(result))
                            + " and " + str(pair[1].fitness(result)) + " in fitness score")
            nextgen.append(child(pair, cross_rate, mut_rate))
        brains = nextgen
        generation += 1


def main():
    '''Main entry point.'''
    log.init_file_log(logging.INFO)
    log.init_console_log()

    log.logger.info("ANNbug V" + str(VERSION))

    brains = list()
    log.logger.info("Creating initial brains...")
    for i in range(100):
        log.logger.debug("Creating initial brain number: " + str(i))
        brains.append(genetic.Genetic(2, 1, 1, 4))

    training_set = list()
    training_set.append([[0, 0], [0]])
    training_set.append([[1, 0], [1]])
    training_set.append([[0, 1], [1]])
    training_set.append([[1, 1], [0]])

    train(brains, training_set, 0.75, 0.005)


if __name__ == '__main__':
    main()
