import numpy as np
import os
# import pyfits
import glob
import config

print config.totaltime

exit()

alma_configs = [1,2,3,4,5,6,7,8,9]

for i in alma_configs:
  print "alma_CONFIG CALLED: ", i
  alma_config = i
  bands = {7:{'pwv':0.5,'alma_config':'/soft/casa-release-5.1.0-74.el7/data/alma/simmos/alma.cycle4.%d.cfg'%alma_config}}

  print bands
	
  # outimage = 'alma_sim.fits'

  # os.system('rm %s'%outimage)

  images = glob.glob('./data/images/arrays/*.fits')

  angle=0

  for d in images:

      basename = d.split('/')[-1].split('.')[0]
      print basename
      band = 7
      nu = 344

      # os.system('rm -r sim%s'%basename)
      # os.system('rm -r sim%s*{model,pbcor,flux,residual,psf,image}'%basename)
      totaltime = '3600s'
      integration = '60s'
   
      #scale = '0.0Jy/pixel'

      simalma(project='sim%s'%basename,
              dryrun=False,
              skymodel=d,
              incenter='%.2fGHz'%nu,
              inwidth='8GHz',
              setpointings=True,
              integration=integration,
              antennalist=bands[band]['alma_config'],
              #mapsize=['3arcsec','3arcsec'],
              hourangle='-03:00:00',
              totaltime=totaltime,
              pwv=bands[band]['pwv'],
              niter = 0,
              image=True,
              verbose=True,
              overwrite=True,
              graphics='file')
      
      trunk = basename

      niter = 100

      output_im_name = 'sim_%s.threshold%s.ms.fullRes'%(trunk,0.01)
      print output_im_name

      clean(vis = 'sim%s/sim%s.alma.cycle4.%d.noisy.ms'%(basename,basename,alma_config),
            imagename = output_im_name,
            spw = '',
            mode = 'mfs',
            interactive = False,
            imsize = [512,512],
            cell = '0.01arcsec',
            #multiscale = [0,int(0.5/0.06),int(1./0.06),int(2./0.06)], 
            niter=niter,
            phasecenter = 0,
            outframe='BARY',
            weighting = 'briggs',
            robust = 0.5,
            threshold='0.01mJy',
            pbcor=False, 
            minpb=0.5,
            negcomponent = -1)


      myimagebases =[output_im_name]

      for myimagebase in myimagebases:
          print myimagebase
          impbcor(imagename=myimagebase+'.image', pbimage=myimagebase+'.flux', outfile= myimagebase+'.image.pbcor', overwrite=True)
          exportfits(imagename= myimagebase+'.image.pbcor', fitsimage= myimagebase+'_conf{}.image.pbcor.fits'.format(alma_config),overwrite=True)
          exportfits(imagename= myimagebase+'.image', fitsimage= myimagebase+'_conf{}.image.fits'.format(alma_config),overwrite=True)
      
          for ext in ['.image.pbcor.fits', '.image.fits']:
              outimage = myimagebase+"_conf{}".format(alma_config) + ext
              h = pyfits.getheader(outimage)
              d = 1.e3*pyfits.getdata(outimage)
              pyfits.writeto(outimage,d,header=h,clobber=True)

		
		
