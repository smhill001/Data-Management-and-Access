import os
from astropy.io import fits
import matplotlib.pyplot as pl
import planetmapper as pm
import numpy as np

def getFilePairs(files):
    filters = ['HIA', 'OI', 'CH4', 'NH3']
    res = []
    for filter in filters:
        filePair = []
        for file in files:
            if filter in file and "map.fits" in file:
                filePair.append(file)
       
        res.append(filePair)
    return res


def process_L1Y(obskey="20250116UTa"):
    PMpath='./FITS/' + obskey
    files = os.listdir(PMpath)
    filePairs = getFilePairs(files)

    def avgData(extension, f1, f2):
        data1 = f1[extension].data
        data2 = f2[extension].data
        return  np.array((PMImgdata1 + PMImgdata2) / 2)
    for f1, f2 in filePairs:
        hdul1 = fits.open(PMpath+ '/' + f1)
        hdul2 = fits.open(PMpath+ '/' + f2)
        PMImgdata1 = hdul1[0].data  
        PMImgdata2 = hdul2[0].data 
        
        hdu = fits.PrimaryHDU(avgData(0, hdul1, hdul2))
        lonArr = fits.ImageHDU(hdul1[1].data)
        latArr = fits.ImageHDU(hdul2[2].data)
        incidenceArr = fits.ImageHDU(avgData(3, hdul1, hdul2))
        emissionArr = fits.ImageHDU(avgData(4, hdul1, hdul2))


        hdul = fits.HDUList([hdu, lonArr, latArr, incidenceArr, emissionArr])
        #hdul.writeto('new1.fits')
      
        hdul1.close()
        hdul2.close()


    
process_L1Y()
