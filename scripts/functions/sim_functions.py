# File of simulation functions, called from run.py


import numpy as np
import matplotlib.pyplot as plt
import astropy.io.fits


class SimImage(astropy.io.fits.ImageHDU):
    def __init__(self, data, header, alma_config=1, sourceID=1, angle=1, exp_time=3600, nbbox=(0,90), thresholds=[5]):
        '''
        Fits storage with attributes
        '''
        self.alma_config = alma_config
        self.angle = angle
        self.exp_time = exp_time
        self.ident = f'{sourceID}_o{angle}_c{alma_config}_exp{exp_time}'
        super().__init__(data, header, name=self.ident)
        self.beam_params = (self.header['BMAJ'], self.header['BMIN'], self.header['BPA'])
        self.noise = np.std(self.data[nbbox[0]:nbbox[1],nbbox[0]:nbbox[1]])
        self.clumps = (len(self.contours(thresholds).allsegs[-1]))
        self.pixel_scale = self.header['CDELT2']

    
    def contours(self, thresholds):
        '''
        Measure contours in images, return some contour object
        Code adapted from clumps.py
        Thresholds should be a list of however many thresholds are required for contours; default is 3, 6, 7 sigma
        '''
        contour_lines = plt.contour(self.data, [self.noise * t for t in thresholds], colors="white", linewidths=1)
        return contour_lines
    


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
