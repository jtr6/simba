# Run.py

from functions.sim_functions import SimImage, fits_to_sim_image
from functions.plot_functions import fits_to_simba_image, SimbaPlots, panel_plot
from astropy.io import fits
import numpy as np


baselines = [155.6, 272.6, 460.0, 704.1, 1124.3, 1813.1, 3696.9, 6855.1, 12644.8]

## Now try for a series of files:
configs = [1,2,3,4,5,6,7,8,9]
angles  = [0,1,2,3,4,5]

image_list = []

for angle in angles:
    all_configs = []
    for config in configs:
        file = f'../output_imgs/sim_m100_g8_o{angle}.threshold0.01.ms.fullRes_10hr_conf{config}.image.pbcor.fits'
        image = fits_to_simba_image(file, alma_config=config, sourceID="g8", angle=angle, exp_time=36000, plot_dir="../plots", save_img=False, save_contours=False, thresholds=[3,5,10,18])
        image.contours(save_contours=True,  thresholds=[5,10,18])
        image.plot_single(save=True)
        image.psf(save=True)
        # print(image.clumps)
        all_configs.append(image)
    image_list.append(all_configs)

image_block = np.array(image_list)


panel_plot(image_block, configs, angles, save=True, plot_dir="../plots/panel_plots",g=8, exp=10)