# Functions for making the plots for the SIMBA project
# Also includes the generic functions clean_axes, and uniform_figsize. 
# (need to implement these in the above plotting functions too)

from functions.sim_functions import SimImage
import matplotlib.pyplot as plt
import numpy as np

class SimbaPlots(SimImage):
    def __init__(self, image, thresholds=[5,10,18]):
        '''
        Class to deal with all the required plots.
        Image should be a SimImage instance
        '''
        super().__init__(image.data, image.header)
        self.image = image
        self.contour = self.contour_plot(self.image, self.image.contours, thresholds)
        self.beam = self.plot_beam(self.image.beam_params, self.image.pixel_scale)

    def contour_plot(self, image, contour_lines, thresholds):
        '''
        Make figure of contour plots for an individual image. Image should be a SimImage instance.
        '''
        plt.imshow(image.data)
        contour_lines(thresholds)
        # plt.show()
        plt.close()

    def plot_beam(self, beam_params, pixscale, x = 400, y = 400):
        '''
        Returns mpatches ellipse object from beam params, in pixels, ready to plot
        '''
        from astropy.coordinates import Angle
        import matplotlib.patches as mpatches
        bmaj, bmin, bpa = beam_params
        bpa = Angle(bpa, "radian")
        bmaj = bmaj / pixscale
        bmin = bmin / pixscale
        beam_ellipse = mpatches.Ellipse((x, y), 2*bmaj, 2*bmin, bpa.degree, edgecolor='white',facecolor='none')
        return beam_ellipse

    def resize_im():
        '''
        Resize images as they go to higher resolution, to make plot better
        '''
        raise NotImplementedError
    
def panel_plot(images,configs,angles):
    '''
    Produce a panel plot of given images (images should be an array of SimbaPlot objects?)
    '''
    if images.shape != (len(angles), len(configs)):
        raise ValueError('The image block has incorrect dimensions, should be of form [angles, configs]')
    fig, axes = plt.subplots(len(angles), len(configs))
    for c in configs:
        print("config {}".format(c))
        # axes[0,c].set_title(baselines[c])  # Need to decide where to store baselines?!
        for a in angles:
            print("----angle {}".format(a))
            image = images[a-1,c-1]
            print("----------on axis {}".format((a, c)))
            axes[a-1,c-1].imshow(image.image.data)
            print("Here is some of the imshow data:", image.image.data[:30])
        beam = image.beam
        axes[a-1,c-1].add_patch(beam)

    for ax in fig.axes:
        ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)
    plt.tight_layout(w_pad=0.2)
    plt.axis('off')
    # plt.savefig(plot_dir + "all_angles_g{}_1hr.png".format(g), bbox_inches=0)
    plt.show()
    # plt.close()

    # raise NotImplementedError

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