# Functions for making the plots for the SIMBA project
# Also includes the generic functions clean_axes, and uniform_figsize. 
# (need to implement these in the above plotting functions too)

import matplotlib.pyplot as plt
import numpy as np

class SimbaPlots:
    def __init__(self, image, thresholds=[5,10,18]):
        '''
        Class to deal with all the required plots.
        Image should be a SimImage instance
        '''
        self.image = image
        self.contour = self.contour_plot(self.image, self.image.contours, thresholds)
        # self.panel = self.panel_plot(images)
        # self.beam = self.plot_beam(self.image.beam_params, self.image.pixel_scale)

    def contour_plot(self, image, contour_lines, thresholds):
        '''
        Make figure of contour plots for an individual image. Image should be a SimImage instance.
        '''
        plt.imshow(image.data)
        contour_lines(thresholds)
        plt.show()
        # plt.savefig("g{}_o{}_conf{}_contours_multi_new.png".format(image.name, image.angle, image.alma_config))

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

    def panel_plot(self, image_block):
        '''
        Produce a panel plot of given images (images should be an array of image arrays?)
        '''
        angles = len(images[0])
        configs = len(images[1])
        fig, axes = plt.subplots(angles, configs)
        for c in configs:
            # axes[0,c].set_title(baselines[c])  # Need to decide where to store baselines?!
            for a in angles:
                image = images[a,c]
                axes[a,c] = plt.imshow(np.sqrt(image.data))
            beam = image.beam()
            axes[5,c].add_patch(beam)

        for ax in fig.axes:
            ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)
        plt.tight_layout(w_pad=0.2)
        plt.axis('off')
        # plt.savefig(plot_dir + "all_angles_g{}_1hr.png".format(g), bbox_inches=0)
        plt.show()

        raise NotImplementedError

    def resize_im():
        '''
        Resize images as they go to higher resolution, to make plot better
        '''
        raise NotImplementedError



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