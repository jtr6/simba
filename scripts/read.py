import numpy as np
import pyfits
import glob

def dump(in_image):
    data = open(in_image).readlines()

    image = np.zeros((512,512)).astype(np.float)
    
    for i,line in enumerate(data):
        _data = np.array([float(d) for d in line.split()])
        image[:,i]=_data

    #image *= 1.e6 #Jy/sr

    #target_flux = 4.77e-3

    fits_file = in_image.replace('.txt','.fits')
    pyfits.writeto(fits_file,image,clobber=True)

    h = pyfits.getheader(fits_file)
    scale = 8.5 #kpc/asec
    one_pix_kpc = 60. / h['NAXIS1']
    one_pix_asec = one_pix_kpc / scale

    one_pix_sr = (one_pix_asec*one_pix_asec)/4.25e10

    area_of_image = ((one_pix_asec*h['NAXIS1'])*np.pi/(180.*3600))**2
    one_pix_sr = area_of_image/np.product(image.shape)

    #image*=area_of_image
    #image/=np.product(image.shape)


    image*=3 #fudge (target_flux/np.sum(image))
    print np.sum(image)*1000, in_image

    h['CDELT1'] = -one_pix_asec/3600.
    h['CDELT2'] = one_pix_asec/3600.
    h['CRPIX1'] = h['NAXIS1']/2
    h['CRPIX2'] = h['NAXIS2']/2
    h['CRVAL1'] = 334.35869
    h['CRVAL2'] = 0.2096619
    h['CUNIT1'] = 'deg'
    h['CUNIT2'] = 'deg'
    h['CTYPE1'] = 'RA---TAN'
    h['CTYPE2'] = 'DEC--TAN'
    
    pyfits.writeto(fits_file,image,header=h,clobber=True)

# images = glob.glob('./images/arrays/*.txt')
images = glob.glob('../data/jo_images/arrays/*.txt')


for i in images: dump(i)
