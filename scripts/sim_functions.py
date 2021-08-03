# File of simulation functions, called from run.py


import numpy as np
import matplotlib.pyplot as plt
import astropy.io

class astropy.io.fits.ImageHDU:
    def __init__(self, *args, **kwargs): pass

class SimImage(astropy.io.fits.ImageHDU):
    def __init__(self, name, alma_config, angle, exp_time, beam_params, *args, **kwargs):
        self.name = name
        self.image = self.data.reshape((512, 512))[100:412, 100:412]
        self.alma_config = alma_config
        self.angle = angle
        self.exp_time = exp_time
        self.beam_params = beam_params
        self.noise = np.std(self.image[0:90, 0:90])

    
    def contours(self, thresholds=[3,5,7]):
        '''
        Measure contours in images, return some contour object
        Can adapt code from clumps.py to fit here
        Thresholds should be a list of however many thresholds are required for contours; default is 3, 6, 7 sigma
        '''
        contour_lines = plt.contour(self.image, [self.noise * t for t in thresholds], colors="white", linewidths=1)
        self.clumps = (len(contour_lines.allsegs[-1]))
        return contour_lines
    
    def fit(self):
        '''
        Some fitting routine e.g. GALFIT to obtain galaxy parameters (clumps, radius, etc)
        '''
        raise NotImplementedError


class SimbaPlots:

    def contour_plot(self, image, contour_lines):
        '''
        Make figure of contour plots for an indivdual image. Image should be a SimImage instance.
        '''
        plt.imshow(image.image)
        contour_lines()
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
