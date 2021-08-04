import scipy
import numpy as np
from scipy.fftpack import ifftn
import matplotlib
import matplotlib.pyplot as plt
from astropy.io import fits
from scipy.ndimage import gaussian_filter, rotate
plt.style.use("computer_modern.mplstyle")
import sep

cmap = matplotlib.cm.magma
cmap.set_bad(color='black')

plot_dir = "../plots/SFR/"

alma_configs = [1,2,3,4,5,6,7,8,9]

for c in alma_configs:
	obs_im_path = "../output_imgs/sim_m100_g3_o0.threshold0.01.ms.fullRes_1hr_conf{}.image.pbcor.fits".format(c)
	obs = fits.open(obs_im_path)[0].data
	obs = obs.reshape((512, 512))[100:412, 100:412]
	bkg = sep.Background(obs)
	thresh = 1.5 * bkg.globalrms
	objects = sep.extract(obs, thresh)
	print objects
	# size = sep.flux_radius(obs, objects[0][x], objects[0][y],  )