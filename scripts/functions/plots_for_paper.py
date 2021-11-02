import numpy as np
import matplotlib.pyplot as plt
plt.style.use('../mplstyles/biolinum.mplstyle')



def clean_axes(ax):
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.spines['left'].set_linewidth(1.5)
	ax.spines['bottom'].set_linewidth(1.5)
	ax.spines['left'].set_color(colour_main)
	ax.spines['bottom'].set_color(colour_main)
	ax.tick_params(direction='out', width=1.5, colors=colour_main, labelcolor=colour_main)


# colour_scheme = ["#264653","#275c62","#287271","#2a9d8f","#8ab17d","#e9c46a","#f4a261","#e76f51"]
colour_scheme = ["#1e4b5d","#1e646b","#1f7a79","#20a797","#65D272","#eec663","#f7a35f","#ed6b4a"]
colour_main     = colour_scheme[0]
colour_dark     = colour_scheme[1]
colour_light    = colour_scheme[2]
colour_lightest = colour_scheme[3]
colour_alt      = colour_scheme[4]
colour_accent3  = colour_scheme[5]
colour_accent2  = colour_scheme[6]
colour_accent   = colour_scheme[7]



## Hodge galaxies:

hodge = np.genfromtxt("../../data/hodge_aless_data.txt", skip_header=2, names="ID,z,z_source,log_Mstar,log_Mstar_uperr,log_Mstar_loerr,log_sfr,log_sfr_uperr,log_sfr_loerr", dtype=(str, float, str, float, float, float, float, float, float))
ms_data = np.genfromtxt("../../data/sf_main_sequence.csv", delimiter=", ", names="M, SFR")
simba = np.genfromtxt("../../data/simba_data.txt", skip_header=2, names="ID, log_Mstar, SFR, 850", dtype=(str, float, float, float))

h_m_errs = np.array((hodge["log_Mstar_loerr"], hodge["log_Mstar_uperr"]))
h_sfr_errs = np.array((hodge["log_sfr_loerr"], hodge["log_sfr_uperr"]))

m11 = np.linspace(0.01, 10, 100)

sfr = 200 * m11**0.9

fig = plt.figure(figsize=(4,4))

plt.scatter(ms_data["M"], ms_data["SFR"], marker='.', c=colour_light, edgecolors='none', alpha=0.7, label="Main sequence galaxies")
plt.scatter(10**hodge["log_Mstar"], 10**hodge["log_sfr"], c=colour_accent, label="Hodge et al. 2019 galaxies")
plt.scatter(10**simba["log_Mstar"], simba["SFR"], c=colour_accent3, label="Simba galaxies")
plt.plot(m11*1e11, sfr, c=colour_light)
plt.xlim(11**9, 11**12)
plt.ylim(5, 1700)
plt.xscale("log")
plt.yscale("log")
plt.xlabel("log $\mathrm{M}_{\star}\mathrm{[M}_{\odot}]$", c=colour_main)
plt.ylabel("SFR [$\mathrm{M}_{\odot}/\mathrm{yr}^-1$]", c=colour_main)
plt.legend()
clean_axes(plt.gca())

# plt.gca().tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)
plt.savefig("../../plots/main_sequence_simba_hodge.pdf", format="pdf")
plt.show()