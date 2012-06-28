'''
Floating-point coded chromosome.

@since: Jun 24, 2012
@author: oblivion
'''
import chromosome
from copy import deepcopy
import random

class FloatChromo(chromosome.Chromosome):
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
        Randomise the chromosome with floating-point data.
        
        @param length: The number of floats in the chromosome.
        @type length: int
        '''
        def random_floats():
            _i = length
            self.data = list()
            while _i >= 0:
                self.data.append(random.uniform(-1, 1))
                _i -= 1

        #Validate the chromosome, if a validation function is present
        random_floats()
        if self.validate == None:
            while not self.validate():
                random_floats()
        return(self)

    def validate(self):
        '''
        Override this method, with code to check if the chromosome is valid.
        '''
        return(True)

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
        #New chromosome
        new_floats = list()
        #Run through the old values
        for _i in range(0, len(self.data)):
            dec = 1
            #Append the old value
            new_floats.append(self.data[_i])
            while dec > 0.000000001:
                if rate > random.uniform(0, 1):
                    new_floats[_i] += dec * random.uniform(-9, 9)
                dec /= 10
        self.data = new_floats
        return(self)
