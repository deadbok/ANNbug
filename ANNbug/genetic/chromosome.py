'''
Chromosome.

@since: Jun 16, 2012
@author: oblivion
'''
import random

class Chromosome(object):
    '''
    Chromosome data class.
    '''
    def __init__(self, validate = None):
        '''
        Constructor
        '''
        self.fitness = 0
        self.bits = '0'
        self.validate = validate
        
    def randomize(self, length):
        '''
        Randomize the chromosome.
        
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
            while (False, '0') == self.validate(self): 
                random_bits()
        return(self)
    