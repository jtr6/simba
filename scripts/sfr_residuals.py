import scipy
import numpy as np
from scipy.fftpack import ifftn
import matplotlib
import matplotlib.pyplot as plt
from astropy.io import fits
from scipy.ndimage import gaussian_filter, rotate
plt.style.use("computer_modern.mplstyle")

cmap = matplotlib.cm.magma
cmap.set_bad(color='black')

plot_dir = "../plots/SFR/"

alma_configs = [1,2,3,4,5,6,7,8,9]

for c in alma_configs:

	img = np.rot90(np.genfromtxt("../data/simba_physical_images/m100_sfr_g3_o0")[100:412, 100:412])
	obs_im_path = "../output_imgs/sim_m100_g3_o0.threshold0.01.ms.fullRes_1hr_conf{}.image.pbcor.fits".format(c)

	obs = fits.open(obs_im_path)[0].data
	obs = obs.reshape((512, 512))[100:412, 100:412]

	fits_header = fits.open(obs_im_path)[0].header

	## Convolution:

	pixscale = fits_header['CDELT2']

	bmaj = fits_header['BMAJ'] / pixscale 
	bmin = fits_header['BMIN'] / pixscale 
	bpa  = fits_header['BPA'] 
	beam_area = (np.pi/2.35482004503 ) * bmaj * bmin
	kpc2_per_pixel = 60./512.
	kpc2_per_beam = beam_area * kpc2_per_pixel

	bmaj = bmaj / 2.35482004503 		##FWHM to 1-sigma conversion factor
	bmin = bmin / 2.35482004503 		##FWHM to 1-sigma conversion factor

	print "max of obs:", np.max(obs)
	print "max of sfr:", np.max(img)

	img = img / kpc2_per_pixel

	filtered = rotate(img, bpa)
	filtered = gaussian_filter(filtered, [bmaj,bmin])
	filtered = rotate(filtered, 360-bpa)

	new_size = filtered.shape[0]
	dims = [int(new_size/2.) - 156, int(new_size/2.) + 156]
	filtered = filtered[dims[0]:dims[1],dims[0]:dims[1]]


	obs_sfr = (obs / kpc2_per_beam) * 190.531018941	#from calc_SFR - conversion factor for 1 mJy

	# residual = (obs/np.max(obs)) - (filtered/np.max(filtered))
	residual = (obs_sfr) - (filtered)
	print np.max(residual)
	vmin = 0
	vmax = np.sqrt(np.max(obs))

	print "max of obs_sfr:", np.max(obs_sfr)
	print "max of sfr_density:", np.max(filtered)

	fig, ax = plt.subplots(1,4)

	# ax[0].imshow(np.log10(img), cmap=cmap)
	ax[0].imshow(img, cmap=cmap)
	ax[0].set_title("SFR map", fontsize=12)
	# ax[1].imshow(np.sqrt(filtered), cmap=cmap)
	ax[1].imshow(filtered, cmap=cmap)
	ax[1].set_title("Smoothed map", fontsize=12)
	# ax[2].imshow(np.sqrt(obs), cmap=cmap)
	ax[2].imshow(obs_sfr, cmap=cmap)
	ax[2].set_title("Synthetic obs.", fontsize=12)
	ax[3].imshow((residual), cmap=cmap, vmin=0, vmax=1)
	ax[3].set_title("Residual", fontsize=12)
	for m, ax in enumerate(fig.axes):
		ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)
	plt.savefig(plot_dir + "smoothed_residual_conf{}.png".format(c),bbox_inches=0)
	plt.show()