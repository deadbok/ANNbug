'''
Genetic algorithm

@since: Jun 18, 2012
@author: oblivion
'''
import random

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

    def roulette(self, target):
        '''
        Select an entity "randomly" favouring best fit.
        '''
        #Find total fitness
        total_fitness = 0
        for entity in self.population:
            total_fitness += entity.fitness(target)
        fitness = 0
        #Find a random fitness to aim for
        target_fitness = random.uniform(0, total_fitness)
        #Keep adding the fitness of each entity until the target fitness is reached
        for entity in self.population:
            fitness += entity.fitness(target)
            if fitness >= target_fitness:
                return(entity)
        #As a last resort, return the last entity
        return(entity)

    def evolve(self, target):
        '''
        Override this method with code to evolve one generation.
        '''
        self.found = False
        self.answers = list()
        best_fit = 0
        for entity in self.population:
            #Save the best chromosome
            if best_fit < entity.fitness(target):
                best_fit = entity.fitness(target)
                self.best_fit = entity
            #Check for solution
            if entity.fitness(target) > 1.0:
                self.found = True
                self.answers.append(entity)
        #If no answer is found, create a new generation
        if not self.found:
            self.generation += 1
            new_pop = list()
            while len(new_pop) < len(self.population):
                #Find a parent
                first_parent = self.roulette(target)
                #Cross with a second
                child = first_parent.cross(self.roulette(target), self.crossover_rate)
                #Mutate
                child.mutate(self.mutation_rate)
                #If fitness is 0 it is not worth the trouble evolving it
                if child.fitness(target) > 0:
                    new_pop.append(child)
            #Replace population with next generation
            self.population = new_pop
