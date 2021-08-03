# File of simulation functions, called from run.py


import numpy as np
import matplotlib.pyplot as plt

class SimImage:
    def __init__(self):
        self.name = ()
        self.image = ()
        self.header = ()
        self.alma_config = ()
        self.angle = ()
        self.exp_time = ()
        self.beam_params = ()
        self.noise = np.std(self.image[0:90, 0:90])

    
    def contours(self):
        '''
        Measure contours in images, return some contour object
        Can adapt code from clumps.py to fit here
        '''
        noise = self.noise
        plt.imshow(self.image)
        contour_lines = plt.contour(self.image, [3*noise,5*noise,7*noise,10*noise, 15*noise], colors="white", linewidths=1)
        plt.savefig("g{}_o{}_conf{}_contours_multi_new.png".format(self.name, self.angle, self.alma_config))
        c = (len(contour_lines.allsegs[-1]))
        return c
    
    def fit(self):
        '''
        Some fitting routine e.g. GALFIT to obtain galaxy parameters (clumps, radius, etc)
        '''
        raise NotImplementedError


class SimbaPlots:

    def contour_plot(self, image, contours):
        '''
        Make figure of contour plots for an indivdual image. Image should be a SimImage instance.
        '''
        plt.imshow(image.image)
        plt.savefig("g{}_o{}_conf{}_contours_multi_new.png".format(image.name, image.angle, image.alma_config))







def configure_inputs():
    '''
    Take user input and produce config file for CASA
    This is a work in progress: need to fix up but can aim to run all analysis on existing images first
    '''
    import config
    return config

def sim_alma():
    '''
    Run CASA simalma and clean functions on a given sky image for a given input configuration
    This is a work in progress: need to fix up but can aim to run all analysis on existing images first
    '''
    raise NotImplementedError
