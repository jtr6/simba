import numpy as np
from astropy.io import fits
import glob
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from astropy.modeling.models import Ellipse2D
from astropy.coordinates import Angle
from custom_cmaps import twilight
from plotting_fns import *
plt.style.use("computer_modern.mplstyle")
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar, AnchoredEllipse


# cmap = twilight()
cmap = matplotlib.cm.magma
cmap.set_bad(color='black')

plot_dir = "../plots/"

def fits_show(fits_file):

	img = fits.open(fits_file)[0].data

	print img.shape

	img = img.reshape((512, 512))

	# plt.imshow(np.log(img),cmap="viridis")
	plt.imshow(img,cmap="viridis")
	plt.colorbar()
	plt.show()

def panel_ims(obs_files, gas_files, dust_files, submm_files, sfr_files, stellar_files):
	for i in range(6):
		print i

		obs_im = fits.open(obs_files[i])[0].data
		obs_im = obs_im.reshape((512, 512))

		stellar_im = np.log10(np.genfromtxt(stellar_files[i]))
		gas_im     = np.log10(np.genfromtxt(gas_files[i]))
		dust_im    = np.log10(np.genfromtxt(dust_files[i]))
		submm_im   = np.log10(np.genfromtxt(submm_files[i]))
		sfr_im     = np.log10(np.genfromtxt(sfr_files[i]))

		print stellar_files[i]
		print submm_files[i]
		print obs_files[i]

		fig,axes = plt.subplots(3,2)
		ax = axes.ravel()
		im0 = ax[0].imshow(obs_im, cmap="viridis")
		plt.colorbar(im0, ax=ax[0])
		im1 = ax[1].imshow(gas_im, cmap = "cividis")
		plt.colorbar(im1, ax=ax[1])
		im2 = ax[2].imshow(dust_im, cmap=cmap)
		plt.colorbar(im2, ax=ax[2])
		im3 = ax[3].imshow(stellar_im, cmap="afmhot")
		plt.colorbar(im3, ax=ax[3])
		im4 = ax[4].imshow(sfr_im, cmap=cmap)
		plt.colorbar(im4, ax=ax[4])
		im5 = ax[5].imshow(submm_im)
		plt.colorbar(im5, ax=ax[5])
		plt.show()

def angles(obs_files, config):
	fig,axes = plt.subplots(3,2)
	ax = axes.ravel()

	for i in range(6):
		print(obs_files[i])
		obs_im = fits.open(obs_files[i])[0].data
		obs_im = obs_im.reshape((512, 512))
		im1 = ax[i].imshow(obs_im, cmap="viridis")
	for k, ax in enumerate(fig.axes):
		ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)
	plt.tight_layout(w_pad=0.2)
	plt.axis('off')
	plt.savefig(plot_dir + "all_angles_conf{}.png".format(config), bbox_inches=0)
	plt.show()

def plot_beam(bmaj, bmin, bpa, pixscale, x = 400, y = 400):
	bpa = Angle(bpa, "radian")
	bmaj = bmaj / pixscale
	bmin = bmin / pixscale
	e2 = mpatches.Ellipse((x, y), 2*bmaj, 2*bmin, bpa.degree, edgecolor='white',facecolor='none')
	# e2 = AnchoredEllipse(axes[k,j].transData, 2*bmaj, 2*bmin, bpa.degree, loc='lower right', pad=0.5, borderpad=0.4, frameon=False, edgecolor='white',facecolor='none')

	return e2



stellar_files = sorted(glob.glob('../data/simba_physical_images/*stellar*'))
submm_files   = sorted(glob.glob('../data/simba_physical_images/*850*'))
sfr_files     = sorted(glob.glob('../data/simba_physical_images/*sfr*'))
gas_files     = sorted(glob.glob('../data/simba_physical_images/*gas*'))
dust_files    = sorted(glob.glob('../data/simba_physical_images/*dust*'))

# all_obs_files     = sorted(glob.glob('../output_imgs/sim_m100_g54*pbcor*'))


def resize_im(obs_im, j):
	if j < 3:
		pos = 400
		return obs_im, pos
	elif 3 <= j <= 5:
		cropped = obs_im[106:406, 106:406]
		pos = 250
		return cropped, pos
	elif 5 < j:
		cropped = obs_im[186:326, 186:326]
		pos = 120
		return cropped, pos

galaxies = [3,8,51,54,100,134,139]

baselines = [155.6, 272.6, 460.0, 704.1, 1124.3, 1813.1, 3696.9, 6855.1, 12644.8]

for g in galaxies:
	fig, axes = plt.subplots(6,9)
	for j in range(9):
		# print g
		# print j
		obs_files = sorted(glob.glob('../output_imgs/sim_m100_g{}*fullRes_1hr_conf'.format(g)+ str(j+1) +'*pbcor*'))
		axes[0,j].set_title(baselines[j])
		# print obs_files
		for k in range(6):
			obs_im = fits.open(obs_files[k])[0].data
			# print obs_files[k]
			# print "+==========+"
			fits_header = fits.open(obs_files[k])[0].header
			bmaj = fits_header['BMAJ']
			bmin = fits_header['BMIN']
			bpa  = fits_header['BPA']
			pixscale = fits_header['CDELT2']
			obs_im = obs_im.reshape((512, 512))
			cropped, pos = resize_im(obs_im, j)
			scale = len(cropped) * pixscale *3600
			# print scale
			im1 = axes[k,j].imshow(np.sqrt(cropped), cmap=cmap)
		beam = plot_beam(bmaj, bmin, bpa, pixscale, x = pos, y = pos)
		axes[5,j].add_patch(beam)
		bar = AnchoredSizeBar(axes[k,j].transData, 100, " ", 1, color="white", frameon=False, borderpad=0.3)
		axes[0,j].add_artist(bar)

	for m, ax in enumerate(fig.axes):
		ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)
	plt.tight_layout(w_pad=0.2)
	plt.axis('off')
	plt.savefig(plot_dir + "all_angles_g{}_1hr.png".format(g), bbox_inches=0)
	plt.show()	

	# print obs_files
	# angles(obs_files, j)
	# fits_show(obs_files[i])

# panel_ims(obs_files, gas_files, dust_files, submm_files, sfr_files, stellar_files)
