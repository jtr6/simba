import numpy as np

import scipy.constants
from scipy.stats import truncnorm
from astropy.cosmology import WMAP9 as cosmo
import astropy.units as u
import scipy.integrate as integrate
import matplotlib.pyplot as plt

h = scipy.constants.h
k = scipy.constants.k
c = scipy.constants.c
b = scipy.constants.physical_constants['Wien wavelength displacement law constant'][0]
beta = 1.5
T = 40
z = 2.025

def gb_freq(x):
    gb = (x**(beta + 3)) / (np.exp((h * x) / (k * T)) - 1)
    return gb

def normed(x):
	norm_850 = 1		# 1 Jy
	norm_freq = c/(850e-6 / (1+z))
	model_850 = gb_freq(norm_freq)
	norm_factor = norm_850/model_850
	return gb_freq(x) * norm_factor


def FIR_luminosity(z):
    pi = scipy.constants.pi
    D_l = cosmo.luminosity_distance(z)
    print D_l
    print D_l.to(u.m)
    int_lim_up = c/8e-6     # Lower limit for integration, 8 um, in m
    int_lim_lo = c/1000e-6    # Upper limit for integration, 1000 um in m
    # Fir = integrate.quad(gb_freq, int_lim_lo, int_lim_up)  # With flux in Jy, should give units Jy m
    Fir = integrate.quad(normed, int_lim_lo, int_lim_up)  # With flux in Jy, should give units Jy m
    Fir = Fir * (u.Jy) * (u.Hz)
    Lir = 4 * pi * D_l**2 * Fir
    print Lir.to(u.erg / u.s)
    print Lir.to(u.W)
    return Lir.to(u.erg / u.s)

def calc_LIR(f_obs, z):
	c = 3e8*(u.m / u.s)

	int_wl = (np.arange(8,1000,1) * u.micron).to(u.m)  # Wavelength range 8 - 1000 micron
	int_nu = (c / int_wl).to(u.Hz)
	L_model = integrate.quad(gb_freq, int_nu[0], int_nu[-1])
	norm_nu = c / (850 * u.micron).to(u.m) * (1 + z)
	d_l = cosmo.luminosity_distance(z)

	L_nu_obs  = f_obs.to(u.W / u.Hz / u.m**2) * 4 * np.pi * (d_l).to(u.m)**2 / (1 + z)
	L_nu_model = gb_freq(norm_nu)

	L_IR = L_model * L_nu_obs / L_nu_model
	return L_IR


def SFR(Lir):
	SFR = 4.5e-44 * Lir
	return SFR[0] 


# x = c/(np.arange(1,1000, 0.1) * 1e-6 )

# plt.plot(x,normed(x))
# plt.scatter(c/(850e-6/(1+z)), 1)
# plt.gca().set_xscale("log")
# plt.gca().set_yscale("log")
# plt.show()

SFR_1Jy = SFR(calc_LIR(1000, z)) * (u.solMass / u.year / u.erg * u.s)

print SFR_1Jy



