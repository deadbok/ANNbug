'''
@since: 21 Jan 2012
@author: oblivion
'''
from ann import genetic
import logging
import log
import random
import copy

#Jan 21, 2012 version 0.1
#    Getting the basics straight.
VERSION = 0.1

def select_brains(brains, result):
    '''
    Select two brains from a list of brains, based on roulette selection.
    
    @param brains: A list of brains to chose from.
    @type brains: list 
    '''
    log.logger.debug('Selecting brains.')
    min_fitness = 999999999999
    for brain in brains:
        fitness = brain.fitness(result)
        if fitness < min_fitness:
            min_fitness = fitness
    log.logger.debug("Worst fitness of all brains: " + str(min_fitness))

    total_fitness = 0
    for brain in brains:
        total_fitness += brain.fitness(result)
    log.logger.debug("Total fitness of all brains: " + str(total_fitness))

    def roll():
        '''
        Select a brain.
        '''
        target_fitness = random.uniform(0, total_fitness)
        _i = -1
        fitness = 0
        while fitness < target_fitness:
            _i += 1
            fitness += brains[_i].fitness(result)
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
    if crossover_rate < random.uniform(0, 1):
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
    best_fit = 0
    while best_fit < 1000:
        best_fit = 0
        for brain in brains:
            fitness = 0
            output = list()
            #Run through the training set
            for ts in training_set:
                log.logger.debug('New training set: ' + str(ts))
                inputs = ts[0]
                result = ts[1]
                brain.update(inputs)
                fitness += brain.fitness(result)
                output.append(brain.net.output)
            fitness = fitness / len(ts)
            if best_fit < fitness:
                best_fit = fitness
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

    train(brains, training_set, 0.90, 0.05)


if __name__ == '__main__':
    main()
