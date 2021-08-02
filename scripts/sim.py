#  Attempting to neaten up the code for the Simba project
# This needs to be an input file for casa to run
#

from config import *

simalma(project='sim_{}'.format(output_name),
        dryrun=False,
        skymodel=image,
        incenter='%.2fGHz'%nu,
        inwidth='8GHz',
        setpointings=True,
        integration=integration_time,
        antennalist=antenna_config_file,
        hourangle='-03:00:00',
        totaltime=total_time,
        pwv=pwv,
        niter = 0,
        image=True,
        verbose=True,
        overwrite=True,
        graphics='file')

clean(vis = visibilities_file,
    imagename = output_im_name,
    spw = '',
    mode = 'mfs',
    interactive = False,
    imsize = [512,512],
    cell = '0.01arcsec',
    niter=niter,
    phasecenter = 0,
    outframe='BARY',
    weighting = 'briggs',
    robust = 0.5,
    threshold='0.01mJy',
    pbcor=False, 
    minpb=0.5,
    negcomponent = -1)


im_root_name =[output_im_name]

for im_root in im_root_name:
    print (im_root)
    impbcor(imagename=im_root+'.image', pbimage=im_root+'.flux', outfile= im_root+'.image.pbcor', overwrite=True)
    exportfits(imagename= im_root+'.image.pbcor', fitsimage= im_root+'_conf{}.image.pbcor.fits'.format(alma_config),overwrite=True)
    exportfits(imagename= im_root+'.image', fitsimage= im_root+'_conf{}.image.fits'.format(alma_config),overwrite=True)

    for ext in ['.image.pbcor.fits', '.image.fits']:
        outimage = im_root+"_conf{}".format(alma_config) + ext
        h = pyfits.getheader(outimage)
        d = 1.e3*pyfits.getdata(outimage)
        pyfits.writeto(outimage,d,header=h,clobber=True)



