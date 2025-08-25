import os
from astropy.io import fits
import matplotlib.pyplot as pl
import planetmapper as pm
import numpy as np
from datetime import datetime

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
def averageDates(datestr1, datestr2):
    #loses a microsecond
    date1 = datetime.fromisoformat(datestr1)
    date2 = datetime.fromisoformat(datestr2)
    avgDate = datetime.fromtimestamp( (date1.timestamp() + date2.timestamp()) / 2)
    return avgDate.strftime("%Y-%m-%dT%H:%M:%S.%f")

def averageCameraDates(newHdr, hdr1, hdr2, key):
    prefix = "HIERARCH SHRPCAP "
    newHdr[prefix + key] = averageDates(hdr1[prefix + key], hdr2[prefix + key]) + "Z"
def averageJDCameraDates(newHdr, hdr1, hdr2, key):
    prefix = "HIERARCH SHRPCAP "
    newHdr[prefix +  key] = (hdr1[prefix +  key] + hdr2[prefix + key]) / 2




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
        hdr1, hdr2 = hdul1[0].header, hdul2[0].header
        hdul[0].header = hdul1[0].header
        hdr = hdul[0].header
        hdr["DATE-OBS"] = averageDates(hdr1["DATE-OBS"], hdr2["DATE-OBS"])
        averageCameraDates(hdr, hdr1, hdr2, "TimeStamp")
        averageCameraDates(hdr, hdr1, hdr2, "StartCapture")
        averageCameraDates(hdr, hdr1, hdr2, "MidCapture")
        averageCameraDates(hdr, hdr1, hdr2, "EndCapture")
        averageJDCameraDates(hdr, hdr1, hdr2, "JDStartCapture")
        averageJDCameraDates(hdr, hdr1, hdr2, "JDMidCapture")
        averageJDCameraDates(hdr, hdr1, hdr2, "JDEndCapture")
        prefix = "HIERARCH PLANMAP "
        hdr[prefix + "UTC-OBS"] = averageDates(hdr1[prefix + "UTC-OBS"], hdr2[prefix + "UTC-OBS"])
        hdr[prefix + "ET-OBS"] = (hdr1[prefix +  "ET-OBS"] + hdr2[prefix + "ET-OBS"]) / 2
        print(repr(hdr))
        

        
        
        #hdul.writeto('new1.fits')
      
        hdul1.close()
        hdul2.close()


    
process_L1Y()
