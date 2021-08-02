import matplotlib.pyplot as plt
import numpy as np

def clean_axes(ax):
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.spines['left'].set_linewidth(1.5)
	ax.spines['bottom'].set_linewidth(1.5)
	# ax.spines['left'].set_color(colour_main)
	# ax.spines['bottom'].set_color(colour_main)
	ax.tick_params(direction='out', width=1.5)

def uniform_figsize(fig, small=True):
	fig = plt.gcf()
	if small == True:
		# mpl.rcParams["font.size"] = 9
		fig.set_size_inches(4, 4)
	else:
		# mpl.rcParams["font.size"] = 9
		fig.set_size_inches(8, 5)

x  = np.random.rand(1,10)
y  = np.random.rand(1,10)
x2 = np.random.rand(1,10)
y2 = np.random.rand(1,10)