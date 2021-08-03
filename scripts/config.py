'''
Configuration file for running sim.sh to produce synthetic ALMA images of 
SIMBA simulated galaxies from 850 um emission maps.

Eventually should implment some user input system for this/ seperate the inputs from user & setup

'''

output_name = "name"
image = "image/path/fits"
nu = 344
total_time = '3000s'
integration_time = '60s'
alma_config = 6 # number between 1 and 9
bands = {alma_config:{'pwv':0.5,'config':'/soft/casa-release-5.1.0-74.el7/data/alma/simmos/alma.cycle4.{}.cfg'.format(alma_config)}}
antenna_config_file = bands[alma_config]['alma_config'],

pwv = bands[alma_config]['pwv']
clean_iter = 100

visibilities_file = 'sim{}/sim{}.alma.cycle4.{}.noisy.ms'.format(output_name,output_name,alma_config)
output_im_name = 'sim_{}.threshold{}.ms.fullRes'.format(output_name,0.01)
