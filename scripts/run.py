# Run.py

from functions.sim_functions import SimImage
from functions.plot_functions import SimbaPlots
from astropy.io import fits

baselines = [155.6, 272.6, 460.0, 704.1, 1124.3, 1813.1, 3696.9, 6855.1, 12644.8]


im_path = "../output_imgs/sim_m100_g100_o0.threshold0.01.ms.fullRes_10hr_conf5.image.pbcor.fits"
im = fits.open(im_path)
data = im[0].data.squeeze()
header = im[0].header

test = SimImage(data, header, 6, "G100", 0, 3000)
plots = SimbaPlots(test, thresholds = [3, 5, 10, 18])