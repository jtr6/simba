import numpy as np
from astropy.io import fits
import glob
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

cmap = matplotlib.cm.magma
cmap.set_bad(color='black')


# aless_imgs= sorted(glob.glob("../data/aless_imgs/ALESS*"))

# for img in aless_imgs:
# 	ID = img.split("_")[2]
# 	print fits.open(img).info()
# 	aless_img = fits.open(img)[0].data

# 	aless_img = np.reshape(aless_img, (2560, 2560))

# 	print aless_img.shape

# 	# fits_header = fits.open(img)[0].header
# 	# print fits_header


# 	# bmaj = fits_header['BMAJ']
# 	# bmin = fits_header['BMIN']
# 	# bpa  = fits_header['BPA']
# 	# pixscale = fits_header['CDELT2']
# 	# scale = len(cropped) * pixscale *3600

# 	plt.gca().tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)
# 	plt.imshow(np.sqrt(aless_img[1180:1380, 1180:1380]), cmap=cmap)
# 	# plt.savefig("../plots/ALESS_{}.png".format(ID))

# 	plt.show()


galaxies = [3,8,51,54,100,134,139]

for g in galaxies:
	comparison_imgs = sorted(glob.glob('../output_imgs/sim_m100_g{}*fullRes_10hr_conf7'.format(g) +'*pbcor*'))
	for img in comparison_imgs:
		ID = img.split("_")[4].split(".")[0]
		print ID
		sim_img = fits.open(img)[0].data
		sim_img = np.reshape(sim_img, (512, 512))
		print sim_img.shape
		plt.imshow(sim_img[156:356, 156:356], cmap=cmap)
		plt.gca().tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)
		plt.savefig("../plots/individual/g{}_{}_10hr_conf7.png".format(g, ID))

		# plt.show()		
