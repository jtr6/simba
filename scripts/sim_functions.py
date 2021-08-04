# File of simulation functions, called from run.py


import numpy as np
import matplotlib.pyplot as plt
import astropy.io.fits


class SimImage(astropy.io.fits.ImageHDU):
    def __init__(self, data, header, alma_config=1, sourceID=1, angle=1, exp_time=3600, nbbox=(0,90), thresholds=[5]):
        '''
        Fits storage with attributes
        -
        alma_config: the ALMA configuration file specified
        angle: angle of the observation (assuming 6 angle views of simulated sources)
        '''
        self.alma_config = alma_config
        self.angle = angle
        self.exp_time = exp_time
        self.ident = f'{sourceID}_o{angle}_c{alma_config}_exp{exp_time}'
        super().__init__(data, header, name=self.ident)
        self.beam_params = (self.header['BMAJ'], self.header['BMIN'], self.header['BPA'])
        self.noise = np.std(self.data[nbbox[0]:nbbox[1],nbbox[0]:nbbox[1]])
        self.clumps = (len(self.contours(thresholds).allsegs[-1]))

    
    def contours(self, thresholds):
        '''
        Measure contours in images, return some contour object
        Can adapt code from clumps.py to fit here
        Thresholds should be a list of however many thresholds are required for contours; default is 3, 6, 7 sigma
        '''
        contour_lines = plt.contour(self.data, [self.noise * t for t in thresholds], colors="white", linewidths=1)
        return contour_lines
    


class FittedImage:
    def __init__(self) -> None:
        pass
    def fit(self):
        '''
        Some fitting routine e.g. GALFIT to obtain galaxy parameters (clumps, radius, etc)
        '''
        raise NotImplementedError


class SimbaPlots:
    def __init__(self, sim_image, thresholds=[5,10,18]):
        self.data = sim_image.data
        self.contour = self.contour_plot(sim_image, sim_image.contours, thresholds)


    def panel_plot(self, images):
        '''
        Produce a panel plot of given images (images should be an array of image arrays?)
        '''
        raise NotImplementedError

    def contour_plot(self, image, contour_lines, thresholds):
        '''
        Make figure of contour plots for an indivdual image. Image should be a SimImage instance.
        '''
        plt.imshow(image.data)
        contour_lines(thresholds)
        plt.show()
        # plt.savefig("g{}_o{}_conf{}_contours_multi_new.png".format(image.name, image.angle, image.alma_config))







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
