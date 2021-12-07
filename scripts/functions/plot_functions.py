# Functions for making the plots for the SIMBA project
# Also includes the generic functions clean_axes, and uniform_figsize. 
# (need to implement these in the above plotting functions too)

from functions.sim_functions import SimImage
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import astropy
cmap = cm.magma
cmap.set_bad(color='black')


def fits_to_simba_image(file_path, alma_config=1, sourceID=1, angle=1, exp_time=3600,nbbox=(0,90), plot_dir="../plots", save_img=False, save_contours=False, thresholds=[5,10,18]):
    file = astropy.io.fits.open(file_path)
    data = file[0].data.squeeze()
    header = file[0].header
    sim_image = SimbaPlots(data, header, alma_config, sourceID, angle, exp_time, nbbox, plot_dir, save_img, save_contours, thresholds)
    return sim_image


class SimbaPlots(astropy.io.fits.ImageHDU):
    def __init__(self, data, header, alma_config=1, sourceID=1, angle=1, exp_time=3600, nbbox=(0,90), plot_dir="../plots", save_img=True, save_contours=False, thresholds=[5,10,18]):
        '''
        Class that has fits storage with attributes & plots
        self.clumps returns how many clumps there are about 5 sigma
        '''
        self.ident = f'{sourceID}_o{angle}_c{alma_config}_exp{exp_time}'
        super().__init__(data, header, name=self.ident)
        self.plot_dir = plot_dir
        self.alma_config = alma_config
        self.angle = angle
        self.exp_time = exp_time
        self.pixel_scale = self.header['CDELT2']
        self.beam_params = (self.header['BMAJ'], self.header['BMIN'], self.header['BPA'])
        self.limits = self.resize_limits()
        self.cutout = self.data[self.limits[0]:self.limits[1], self.limits[0]:self.limits[1]]
        self.beam = self.plot_beam(self.beam_params, self.pixel_scale)
        self.noise = np.std(self.data[nbbox[0]:nbbox[1],nbbox[0]:nbbox[1]])
        self.contour = self.contours(save_contours, thresholds)
        self.plot = self.plot_single(save_img)
        self.clumps = (len(self.contours(save_contours, thresholds=[5]).allsegs[-1]))


    def contours(self, save_contours, thresholds):
        '''
        Measure contours in images, return some contour object.
        Optionally, make figure of contour plots for an individual image. Image should be a SimImage instance.
        '''
        contour_lines = plt.contour(self.cutout, [self.noise * t for t in thresholds], colors="white", linewidths=1)
        if save_contours:
            plt.imshow(self.cutout, cmap=cmap)
            plt.savefig(self.plot_dir + "/individual_plots/contours/{}.png".format(self.ident), format="png")
            plt.close()
        else:
            plt.close()
        return contour_lines

    def plot_beam(self, beam_params, pixscale):
        '''
        Returns mpatches ellipse object from beam params, in pixels, ready to plot
        '''
        from astropy.coordinates import Angle
        import matplotlib.patches as mpatches
        bmaj, bmin, bpa = beam_params
        bpa = Angle(bpa, "radian")
        bmaj = bmaj / pixscale
        bmin = bmin / pixscale
        x = y = 0.9 * self.limits[1]
        beam_ellipse = mpatches.Ellipse((x, y), 2*bmaj, 2*bmin, bpa.degree, edgecolor='white',facecolor='none')
        return beam_ellipse
    
    def plot_single(self, save, show=False):
        plt.imshow(self.data, cmap=cmap)
        plt.gca().set_xlim(self.limits[0], self.limits[1])
        plt.gca().set_ylim(self.limits[0], self.limits[1])
        if show:
            plt.show()
        if save:
            plt.savefig(self.plot_dir + "/individual_plots/{}.png".format(self.ident), format="png")
            plt.close()
        else:
            plt.close()

    def resize_limits(self):
        centre = len(self.data)/2
        size = 8 * self.beam_params[0] / self.pixel_scale
        size_min = int(centre - size)
        size_max = int(centre + size)
        if size >= len(self.data)/2:
            return (0, len(self.data))
        else:
            return (size_min, size_max)


    
def panel_plot(images,configs,angles,save=False,plot_dir="../../plots",g=1,exp=1):
    '''
    Produce a panel plot of given images (images should be an array of SimbaPlot objects?)
    '''
    if images.shape != (len(angles), len(configs)):
        raise ValueError('The image block has incorrect dimensions, should be of form [angles, configs]')
    fig, axes = plt.subplots(len(angles), len(configs))
    for c in configs:
        axes[0,c-1].set_title(images[1,c-1].alma_config)
        for a in angles:
            image = images[a,c-1]
            axes[a,c-1].imshow(image.cutout, cmap=cmap)
        beam = image.beam
        axes[a,c-1].add_patch(beam)

    for ax in fig.axes:
        ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)
    plt.tight_layout(w_pad=0.2)
    plt.axis('off')
    if save:
        plt.savefig(plot_dir + "/all_angles_g{}_{}hr.png".format(g, exp), bbox_inches=0)
        plt.close()
    else:
        plt.show()


def clean_axes(ax):
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)
    # ax.spines['left'].set_color(colour_main)
    # ax.spines['bottom'].set_color(colour_main)
    ax.tick_params(direction='out', width=1.5)

def uniform_figsize(fig, small=True):
    fig = plt.gcf()
    if small == True:
        # mpl.rcParams["font.size"] = 9
        fig.set_size_inches(4, 4)
    else:
        # mpl.rcParams["font.size"] = 9
        fig.set_size_inches(8, 5)