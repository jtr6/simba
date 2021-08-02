import glob


def sim_alma(config, band, image, output_name):

    alma_config = config
    bands = {band:{'pwv':0.5,'alma_config':'/soft/casa-release-5.1.0-74.el7/data/alma/simmos/alma.cycle4.{}.cfg'.format(alma_config)}}

    band = 7
    nu = 344

    totaltime = '3600s'
    integration = '60s'

    simalma(project='sim_{}'.format(output_name),
            dryrun=False,
            skymodel=d,
            incenter='%.2fGHz'%nu,
            inwidth='8GHz',
            setpointings=True,
            integration=integration,
            antennalist=bands[band]['alma_config'],
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
    output_im_name = 'sim_{}.threshold{}.ms.fullRes'.format(trunk,0.01)
    
    clean(vis = 'sim{}/sim{}.alma.cycle4.{}.noisy.ms'.format(basename,basename,alma_config),
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



