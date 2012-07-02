'''
Chromosome.

@since: Jun 16, 2012
@author: oblivion
'''
import log

class Chromosome(object):
    '''
    Chromosome base class.
    '''
    def __init__(self):
        '''
        Constructor
        '''
        log.logger.debug("Creating a chromosome.")
        self.data = None
        self.last_fit = None

    def randomise(self, length):
        '''
        Randomise the chromosome with binary data.
        
        @param length: The number of data in the chromosome.
        @type length: int
        '''
        return(None)

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
        return(None)

    def cross(self, other, rate):
        '''
        Cross this chromosome with another.
        
        @param other: The chromosome to cross this one with
        @type other: L{chromosome.Chromosome}
        @param rate: The crossover rate (0..1)
        @type rate: float    
        '''
        return(self)

    def mutate(self, rate):
        '''
        Mutate the chromosome.

        @param rate: The mutation rate (0..1)
        @type rate: float            
        '''
        return(self)
