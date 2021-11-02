# Run.py

from functions.sim_functions import SimImage, fits_to_sim_image
from functions.plot_functions import SimbaPlots, panel_plot
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
        file = f'../output_imgs/sim_m100_g8_o{angle}.threshold0.01.ms.fullRes_1hr_conf{config}.image.pbcor.fits'
        image = fits_to_sim_image(file)
        plots = SimbaPlots(image, thresholds = [3, 5, 10, 18])
        all_configs.append(plots)
    image_list.append(all_configs)

image_block = np.array(image_list)


panel_plot(image_block, configs, angles)