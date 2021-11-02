import numpy as np
from astropy.io import fits
import matplotlib
import matplotlib.pyplot as plt
cmap = matplotlib.cm.magma
cmap.set_bad(color='black')

plot_dir = "../plots/clumps/"



alma_configs = [1,2,3,4,5,6,7,8,9]
angles = [0,1,2,3,4,5] 
galaxies = [3,8,51,54,139,134,100]

clumps = []

for g in galaxies:
	for c in alma_configs:
		for angle in angles:
			obs_im_path = "../output_imgs/sim_m100_g{}_o{}.threshold0.01.ms.fullRes_1hr_conf{}.image.pbcor.fits".format(g,angle, c)
			obs = fits.open(obs_im_path)[0].data
			obs = obs.reshape((512, 512))[100:412, 100:412]


			noise = np.std(obs[0:90, 0:90])

			# print noise

			# print np.max(obs)

			plt.imshow(obs, cmap=cmap)
			contours = plt.contour(obs, [3*noise,6*noise,9*noise,12*noise], colors="white",linewidths=1)
			# print "-------------------------------------"
			print g, c
			# print contours.levels
			# print len(contours.allsegs[0])
			# print len(contours.allsegs[-1])

			clumps.append(len(contours.allsegs[-1]))
			# print "-------------------------------------"
			# plt.savefig(plot_dir + "g{}_o{}_conf{}_contours_multi.png".format(g,angle,c))
			plt.close()
			# plt.show()

clumps  = np.array(clumps).reshape(len(galaxies), len(alma_configs),  len(angles))

print clumps[0,6,0]
