'''
Genetic algorithm test.
 
@since: Jun 16, 2012
@author: oblivion
'''
from genetic import chromosome
from genetic import algorithm
import copy

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

GENERATIONS = list()

class EquChromosome(chromosome.Chromosome):
    '''
    Chromosome for an equation.
    '''
    def __init__(self):
        '''
        Constructor.
        '''
        chromosome.Chromosome.__init__(self)

    def decode(self):
        '''
        Decode the chromosome to an equation.
        '''
        answer = ''
        #Run through each gene.
        gene_start = 0
        gene_end = 0
        operator = False
        for gene_end in range(4, len(self.bits), 4):
            gene = str(self.bits[gene_start:gene_end])
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

    def validate(self):
        '''
        Check if the chromosome is meaningful.
        '''
        answer = self.decode()
        try:
            eval(answer)
            ret = True
        except (SyntaxError, ZeroDivisionError):
            #The chromosome does not parse
            ret = False
        return(ret)

    def fitness(self, target):
        '''
        Get the fitness of the chromosome.
        '''
        if self.validate():
            equ = self.decode()
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

class EquPopulation(algorithm.Algorithm):
    '''
    Population to find an equation for an answer.
    '''
    def __init__(self):
        '''
        Constructor.
        '''
        algorithm.Algorithm.__init__(self, 80)
        _i = self.population_size
        while _i > 0:
            self.population.append(EquChromosome().randomise(self.chromosome_bits))
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


def main():
    '''
    Genetic test program.
    '''
    target = 10
    #Create initial population
    population = EquPopulation()
    population.mutation_rate = 0.001
    #Loop until an answer is found
    while not population.found:
        population.evolve(target)
        print('Generation: ' + str(population.generation) + ' = ' + population.best_fit.decode())
    print('Answer(s):')
    for answer in population.answers:
        print('    ' + answer.decode() + ' = ' + str(target))

if __name__ == '__main__':
    main()
