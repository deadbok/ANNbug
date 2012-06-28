'''
Binary coded chromosome.

@since: Jun 24, 2012
@author: oblivion
'''

import chromosome
import random
from copy import deepcopy

class BinChromo(chromosome.Chromosome):
    '''
    Chromosome base class.
    '''
    def __init__(self):
        '''
        Constructor
        '''
        chromosome.Chromosome.__init__(self)

    def randomise(self, length):
        '''
        Randomise the chromosome with binary data.
        
        @param length: The number of bits in the chromosome.
        @type length: int
        '''
        def random_bits():
            _i = length - 1
            self.data = ''
            while _i > 0:
                self.data += str(random.randint(0, 1))
                _i -= 1

        #Validate the chromosome, if a validation function is present
        random_bits()
        if not self.validate == None:
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
        
        @return: Return a decoded chromosome, of the object type it represents or None
        '''
        return(None)

    def fitness(self, target):
        '''
        Override this method with code to calculate the fitness of the chromosome.
        
        @param target: The target value.
        @type target: int
        '''
        pass

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
            cross_index = random.randint(0, len(self.data))
            #Create a child as a copy of self
            child = deepcopy(self)
            #Cross the chromosomes
            child.data = self.data[0:cross_index] + other.data[cross_index:]
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
        for _i in range(0, len(self.data)):
            if rate > random.uniform(0, 1):
                if self.data[_i] == '0':
                    new_bits += '1'
                else:
                    new_bits += '0'
            else:
                new_bits += self.data[_i]
        self.data = new_bits
        return(self)
