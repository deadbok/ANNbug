'''
Genetic algorithm

@since: Jun 18, 2012
@author: oblivion
'''
import random
import log

class Algorithm(object):
    '''
    Genetic algorithm base class.
    '''
    def __init__(self, population_size=200, chromosome_bits=300):
        '''
        Constructor
        
        @param population_size: Number of chromosomes in each generation.
        @type population_size: int
        @param chromosome_bits: Number of bits in each chromosome.
        @type chromosome_bits: int
        '''
#TODO: Change bits to genes
        #Init a population
        log.logger.debug("Creating a genetic population.")
        self.population_size = population_size
        self.chromosome_bits = chromosome_bits
        self.population = list()
        self.generations = list()
        #Default crossover rate
        self.crossover_rate = 0.75
        #Default mutation rate
        self.mutation_rate = 0.001
        #Keep track of generations
        self.generation = 0
        #Do we have a solution
        self.found = False
        #Save answers
        self.answers = list()
        #Or best fit
        self.best_fit = None

    def roulette(self, inputs, target):
        '''
        Select an entity "randomly" favouring best fit.
        '''
        log.logger.debug("Doing roulette selection.")
        #Find total fitness
        total_fitness = 0
        for entity in self.population:
            total_fitness += abs(entity.fitness(inputs, target))
        fitness = 0
        #Find a random fitness to aim for
        target_fitness = random.uniform(0, total_fitness)
        #Keep adding the fitness of each entity until the target fitness is reached
        for entity in self.population:
            fitness += abs(entity.fitness(inputs, target))
            if fitness >= target_fitness:
                log.logger.debug("Selected chromosome:" + str(entity.data))
                return(entity)
        #As a last resort, return the last entity
        return(entity)

    def evolve(self, inputs, target):
        '''
        Override this method with code to evolve one generation.
        '''
        log.logger.debug("Evolving population")
        self.found = False
        self.answers = list()
        best_fit_neg = -9999
        best_fit_pos = 9999
        #Run through the population
        _n = 0
        for entity in self.population:
            _n += 1
            log.logger.info('Brain: ' + str(_n))
            #Save the best chromosome
            fitness = entity.fitness(inputs, target)
            if fitness < 0:
                #Negative best fit
                if best_fit_neg < fitness:
                    best_fit_neg = fitness
            else:
                #Positive best fit
                if best_fit_pos > fitness:
                    best_fit_pos = fitness
            #Save overall best fit
            if self.best_fit == None:
                self.best_fit = entity
            else:
                if abs(self.best_fit.fitness(inputs, target)) > fitness:
                    self.best_fit = entity
            #Check for solution
            if fitness == 0:
                self.found = True
                self.answers.append(entity)
                log.logger.debug('Solution found: ' + entity.net.id)
        #If no answer is found, create a new generation
        _n = 0
        if not self.found:
            new_pop = list()
            while len(new_pop) < len(self.population):
                _n += 1
                log.logger.info('Child: ' + str(_n))
                #Find a parent
                first_parent = self.roulette(inputs, target)
                #Cross with a second
                child = first_parent.cross(self.roulette(inputs, target), self.crossover_rate)
                #Mutate
                child.mutate(self.mutation_rate)
                #If fitness is 0 it is not worth the trouble evolving it
                #if child.fitness(inputs, target) > 0:
                new_pop.append(child)
            #Replace population with next generation
            self.population = new_pop
