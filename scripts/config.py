'''
Configuration file for running sim.sh to produce synthetic ALMA images of 
SIMBA simulated galaxies from 850 um emission maps.


'''


### File paths

simba_txt_file_path  = "stuff"
simba_fits_file_path = "file"
output_file_path     = "things"



### CASA simalma parameters

totaltime   = 3000 # in seconds
integration = 60   # in seconds





if __name__ == "__main__":
	print "~"*40
	print "CONFIG CONTENTS"
	print  "~"*40
	for name, value in globals().items():
		if not name.startswith("__"):
			print name.ljust(20), "=", value
	print  "~"*40