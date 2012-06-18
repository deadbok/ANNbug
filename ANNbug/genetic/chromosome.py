'''
Chromosome.

@since: Jun 16, 2012
@author: oblivion
'''

from copy import deepcopy
import random

class Chromosome(object):
    '''
    Chromosome base class.
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.bits = '0'

    def randomise(self, length):
        '''
        Randomise the chromosome.
        
        @param length: The number of bits in the chromosome.
        @type length: int
        '''
        def random_bits():
            _i = length - 1
            self.bits = ''
            while _i > 0:
                self.bits += str(random.randint(0, 1))
                _i -= 1

        if self.validate == None:
            random_bits()
        else:
            random_bits()
            while not self.validate():
                random_bits()
        return(self)

    def validate(self):
        '''
        Override this method, with code to check if the chromosome is valid.
        '''
        return(True)

    def decode(self):
        '''
        Override this method with code to decode the chromosome.
        '''
        return('')

    def fitness(self, target):
        '''
        Override this method with code to calculate the fitness of the chromosome.
        
        @param target: The target value.
        @type target: int
        '''
    def cross(self, other, rate):
        '''
        Cross this chromosome with another.
        
        @param other: The chromosome to cross this one with
        @type other: L{chromosome.Chromosome}
        @param rate: The crossover rate (0..1)
        @type rate: float    
        '''
        #Only cross according to crossover rate
        if rate < random.uniform(0, 1):
            #Get a random point from where to inherit genes from other
            cross_index = random.randint(0, len(self.bits))
            #Create a child as a copy of self
            child = deepcopy(self)
            #Cross the chromosomes
            child.bits = self.bits[0:cross_index] + other.bits[cross_index:]
            return(child)
        #Return self, if we are not to cross this chromosome
        return(self)

    def mutate(self, rate):
        '''
        Mutate the chromosome.

        @param rate: The mutation rate (0..1)
        @type rate: float            
        '''
        new_bits = ''
        for _i in range(0, len(self.bits)):
            if rate > random.uniform(0, 1):
                if self.bits[_i] == '0':
                    new_bits += '1'
                else:
                    new_bits += '0'
            else:
                new_bits += self.bits[_i]
        self.bits = new_bits
        return(self)
