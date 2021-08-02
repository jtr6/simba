import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from astropy.io import fits
plt.style.use("computer_modern.mplstyle")

# cmap = matplotlib.cm.magma
# cmap.set_bad(color='black')

plot_dir = "../plots/clumps/"

alma_configs = [1,2,3,4,5,6,7,8,9]


def gini_coefficient(array):
    """Calculate the Gini coefficient of a numpy array."""
    # based on bottom eq:
    # http://www.statsdirect.com/help/generatedimages/equations/equation154.svg
    # from:
    # http://www.statsdirect.com/help/default.htm#nonparametric_methods/gini.htm
    # All values are treated equally, arrays must be 1d:
    array = array.flatten()
    if np.amin(array) < 0:
        # Values cannot be negative:
        array -= np.amin(array)
    # Values cannot be 0:
    array += 0.0000001
    # Values must be sorted:
    array = np.sort(array)
    # Index per array element:
    index = np.arange(1,array.shape[0]+1)
    # Number of array elements:
    n = array.shape[0]
    # Gini coefficient:
    return ((np.sum((2 * index - n  - 1) * array)) / (n * np.sum(array)))


def beams(img, img_hdr):
	# Define area above 5 sigma
	noise = np.std(img[0:90, 0:90])
	img = img.flatten()
	source = img[img >3*noise]
	# count number of pixels
	pix = len(source)
	# divide by beam area -> beams/source	
	pixscale = img_hdr['CDELT2']
	bmaj = img_hdr['BMAJ'] / pixscale 
	bmin = img_hdr['BMIN'] / pixscale 
	beam_area = (np.pi/2.35482004503 ) * bmaj * bmin
	return pix/beam_area

def count_clumps(img, noise, dax, sigma=10):
	contours = dax.contour(img, [sigma*noise])
	n = len(contours.allsegs[0])
	print n
	return n



fig, ax = plt.subplots(7,6)
dfig, dax = plt.subplots(1,1)


alma_configs = [1,2,3,4,5,6,7,8,9]
angles = [0,1,2,3,4,5] 
galaxies = [3,8,51,54,139,134,100]


cmap = plt.get_cmap("viridis",11)

i=0
m=3
for g in galaxies:
	ax[i,0].set_ylabel("Galaxy {}              ".format(g), rotation=0)
	for a in angles:
		ax[0,a].set_title("Angle {}".format(a))
		beam_per_source = []
		gini = []
		clumps  = []
		beam_fwhm = []
		for c in alma_configs:
			img_path = "../output_imgs/sim_m100_g{}_o{}.threshold0.01.ms.fullRes_10hr_conf{}.image.pbcor.fits".format(g,a,c)

			img = fits.open(img_path)[0].data
			img = img.reshape((512, 512))[100:412, 100:412]
			img_hdr = fits.open(img_path)[0].header
			beam_per_source.append(beams(img, img_hdr))
			noise = np.std(img[0:90, 0:90])
			clumps.append(count_clumps(img, noise, dax, 5))

			img = img.flatten()
			source = img[img >3*noise]
			# gini_c = gini_coefficient(source)
			# gini.append(gini_c)
			# print img_hdr['BMAJ'], gini_c
			beam_fwhm.append(img_hdr['BMAJ'])
		# print a,i
		plot = ax[i,a].scatter(beam_fwhm, beam_per_source, c=clumps, cmap=cmap, vmin=1, vmax=11)
	i += 1
	print i

plt.close(dfig)
for k, ax in enumerate(fig.axes):
	ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)
	ax.set_xlim([0.000002, 0.0005])
	ax.set_xscale("log")

fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.1, 0.03, 0.8])
norm = matplotlib.colors.Normalize(vmin=1, vmax=11)


cbar = fig.colorbar(plot, cax=cbar_ax)
plt.clim=(0.5,11.5)
cbar.set_label("No. clumps > 5 $\sigma$")
cbar.set_ticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5])
# cbar.set_ticks([1,2,3,4,5,6,7,8,9,10,11])

cbar.set_ticklabels([1,2,3,4,5,6,7,8,9,10,11])
cbar.ax.tick_params(size=0)
cbar.outline.set_visible(False)
# plt.xlabel("log (beam FWHM)")
# plt.ylabel("No. beams/source")

fig.text(0.5,0.04, "log (beam FWHM)", ha="center", va="center")
fig.text(0.001,0.5, "No. beams/source", ha="center", va="center", rotation=90)

fig.savefig(plot_dir + "clumps_beamwidth_10hr.png", bbox_inches="tight")
plt.show(fig)
