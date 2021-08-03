import numpy as np
import scipy 
from astropy.modeling import models, fitting
from astropy.io import fits
import matplotlib.pyplot as plt
import warnings


test_img = fits.open("/home/jo/Pictures/gal.fits")[0].data


p_init = models.Sersic2D()
fit_p = fitting.LevMarLSQFitter()

with warnings.catch_warnings():
    # Ignore model linearity warning from the fitter
    warnings.simplefilter('ignore')
    p = fit_p(p_init, test_img)

plt.figure(figsize=(8, 2.5))
plt.subplot(1, 3, 1)
plt.imshow(test_img, origin='lower', interpolation='nearest', vmin=-1e4, vmax=5e4)
plt.title("Data")
plt.subplot(1, 3, 2)
plt.imshow(p(test_img), origin='lower', interpolation='nearest', vmin=-1e4,
           vmax=5e4)
plt.title("Model")
plt.subplot(1, 3, 3)
plt.imshow(z - p(x, y), origin='lower', interpolation='nearest', vmin=-1e4,
           vmax=5e4)
plt.title("Residual")