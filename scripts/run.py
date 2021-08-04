# Run.py

from functions.sim_functions import SimImage, fits_to_sim_image
from functions.plot_functions import SimbaPlots
from astropy.io import fits
import glob


baselines = [155.6, 272.6, 460.0, 704.1, 1124.3, 1813.1, 3696.9, 6855.1, 12644.8]

## Now try for a series of files:
configs = [1,2,3]
angles  = [1,2,3,4]

image_block = []

for config in configs:
    for angle in angles:
        file = f'../output_imgs/sim_m100_g8_o{angle}.threshold0.01.ms.fullRes_1hr_conf{config}.image.pbcor.fits'
        image = fits_to_sim_image(file)
        plots = SimbaPlots(image, thresholds = [3, 5, 10, 18])
        image_block.append(image)
        