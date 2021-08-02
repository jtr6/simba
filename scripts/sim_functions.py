# File of simulation functions, called from run.py


import numpy as np

class SimImage:
    def __init__(self):
        self.image = ()
        self.header = ()
        self.dims = self.shape
    
    def contours(self):
        '''
        Measure contours in images, return some contour object

        '''
        raise NotImplementedError
    
    def fit(self):
        '''
        Some fitting routine e.g. GALFIT to obtain galaxy parameters (clumps, radius, etc)
        '''
        raise NotImplementedError



def configure_inputs():
    '''
    Take user input and produce config file for CASA
    '''
    raise NotImplementedError

def sim_alma():
    '''
    Run CASA simalma and clean functions on a given sky image for a given input configuration
    '''
    raise NotImplementedError
