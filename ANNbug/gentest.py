'''
Genetic algorithm test.
 
@since: Jun 16, 2012
@author: oblivion
'''
from genetic import chromosome
import random

GENES = {'0000': '0',
         '0001': '1',
         '0010': '2',
         '0011': '3',
         '0100': '4',
         '0101': '5',
         '0110': '6',
         '0111': '7',
         '1000': '8',
         '1001': '9',
         '1010': '+',
         '1011': '-',
         '1100': '*',
         '1101': '/',
         '1110': ' '}

def decode(chromo):
    '''
    Decode the chromosoe to an equation.
    '''
    answer = ''
    #Run through each gene.
    gene_start = 0
    gene_end = 0
    operator = False
    for gene_end in range(4, len(chromo.bits), 4):
        gene = str(chromo.bits[gene_start:gene_end])
        try:
            #Add the value of the gene
            gene_value = GENES[gene]
            #Ignore operator following operator
            if operator:
                if gene_value in ['+', '-', '*', '/', ' ']:
                    pass
                else:
                    operator = False
                    answer += gene_value
            elif gene_value in ['+', '-', '*', '/']:
                operator = True
                answer += gene_value
            elif gene_value == ' ':
                return(answer)
            else:
                operator = False
                answer += gene_value
            #move the start forward
            gene_start = gene_end
        except KeyError:
            #Ignore non-existing keys
            gene_value = ''
            #move the start forward
            gene_start = gene_end
    return(answer)

def validate(chromo):
    '''
    Check if the chromosome is meaningful.
    '''
    answer = decode(chromo)
    try:
        eval(answer)
        ret = True
    except (SyntaxError, ZeroDivisionError):
        #The chromosome does not parse
        ret = False
    return(ret)

def get_fitness(chromo, target, max_length):
    '''
    Get the fitness of the chromosome.
    '''
    if chromo.validate(chromo):
        equ = decode(chromo)
        equ = 'float(' + equ + ')'
        answer = eval(equ)
        #Zero my be a really bad answer, but give good results
        if answer == 0:
            if not target == 0:
                return(0)
        ret = 0
        if not answer == target:
            try:
                ret = 1.0 / (abs(target - answer) + 1.0)
            except ZeroDivisionError:
                ret = 1.0
            #Make the result count 2/3
        else:
            try:
                ret = 1.0
                ret += 1.0 / (len(equ))
            except ZeroDivisionError:
                pass
        return(ret)
    else:
        return(0)

def roulette(population):
    '''
    Select an entity "randomly" favouring best fit.
    '''
    #Find total fitness
    total_fitness = 0
    for entity in population:
        total_fitness += entity.fitness

    fitness = 0
    #Find a random fitness to aim for
    target_fitness = random.uniform(0, total_fitness)
    for entity in population:
        fitness += entity.fitness
        if fitness >= target_fitness:
            return(entity)
    return(entity)

def cross(first_parent, second_parent, crossover_rate):
    '''
    Cross to chromosomes.
    '''
    if crossover_rate < random.uniform(0, 1):
        cross_index = random.randint(0, len(first_parent.bits))
        child = chromosome.Chromosome(validate)
        child.bits = first_parent.bits[0:cross_index] + second_parent.bits[cross_index:]
        return(child)
    return(first_parent)

def mutate(chromo, rate):
    '''
    Mutate the chromosome.
    '''
    new_bits = ''
    for _i in range(0, len(chromo.bits)):
        if rate > random.uniform(0, 1):
            if chromo.bits[_i] == '0':
                new_bits += '1'
            else:
                new_bits += '0'
        else:
            new_bits += chromo.bits[_i]
    chromo.bits = new_bits
    return(chromo)

def main():
    '''
    Genetic test program.
    '''
    target = 10
    #Create initial population
    n_pop = 200
    n_bits = 300
    population = list()
    _i = n_pop
    while _i > 0:
        population.append(chromosome.Chromosome(validate).randomize(n_bits))
        _i -= 1

    #Loop until an answer is found
    found = False
    generation = 0
    while not found:
        generation += 1
        total_fitness = 0
        best_fit = 0
        for entity in population:
            entity.fitness = get_fitness(entity, target, n_bits / 4)
            total_fitness += entity.fitness
            if best_fit < entity.fitness:
                best_fit = entity.fitness
            if entity.fitness > 1.0:
                found = True
                ret = decode(entity)
                print(ret + " = " + str(eval(ret)))

        print("Generation: " + str(generation)
              + " total fitness: " + str(total_fitness)
              + " best fitness: " + str(best_fit))
        if not found:
            new_pop = list()
            while len(new_pop) < len(population):
                first_parent = roulette(population)
                second_parent = roulette(population)
                child = cross(first_parent, second_parent, 0.75)
                child = mutate(child, 0.005)
                if get_fitness(child, target, n_bits / 4) > 0:
                    new_pop.append(child)
            population = new_pop

if __name__ == '__main__':
    main()
