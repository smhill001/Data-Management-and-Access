import os
from astropy.io import fits
import matplotlib.pyplot as pl
import planetmapper as pm
import numpy as np
from datetime import datetime
from astropy.coordinates import SkyCoord
import astropy.units as u

def getFilePairs(files):
    """
         Gets pairs of scientific files for each filter

         Parameters:
         files (Array[string]): list of file names
         Returns:
         Array[Array[string]]: list of file name pairs
    """
    filters = ['HIA', 'OI', 'CH4', 'NH3']
    res = []
    for filter in filters:
        filePair = []
        for file in files:
            if filter in file and "map.fits" in file and file.count("_") == 2:
                filePair.append(file)
       
        res.append(filePair)
    return res
def averageDates(datestr1, datestr2, format):
    """
         Averages dates and outputs result in specified format
         Parameters:
         datestr1, datestr2 (string): dates to average
         format (string): output date format
         Returns:
         String: average date
    """
    #loses a microsecond
    date1 = datetime.fromisoformat(datestr1)
    date2 = datetime.fromisoformat(datestr2)
    avgDate = datetime.fromtimestamp( (date1.timestamp() + date2.timestamp()) / 2)
    return avgDate.strftime(format)

def averageCameraDates(newHdr, hdr1, hdr2, key):
    
    prefix = "HIERARCH SHRPCAP "
    newHdr[prefix + key] = averageDates(hdr1[prefix + key], hdr2[prefix + key], "%Y-%m-%dT%H:%M:%S.%f") + "Z"

def averageHdrNum(newHdr, hdr1, hdr2, key):
    
    newHdr[key] = (hdr1[key] + hdr2[key]) / 2

def sumHdrNum(newHdr, hdr1, hdr2, key):
    newHdr[key] = hdr1[key] + hdr2[key]


#finds midpoint
def averageCoors(newHdr, hdr1, hdr2):
    ra1 = hdr1["HIERARCH SHRPCAP RA"]
    ra2 = hdr2["HIERARCH SHRPCAP RA"] 
    dec1 =  hdr1["HIERARCH SHRPCAP Dec"].split(' ')[0]
    dec2 = hdr2["HIERARCH SHRPCAP Dec"].split(' ')[0]
    
    coord1 = SkyCoord(ra1, dec1, unit = (u.hourangle, u.deg) )
    coord2 = SkyCoord(ra2, dec2, unit = (u.hourangle, u.deg) )
    pa = coord1.position_angle(coord2)
    sep = coord1.separation(coord2)
    midcoor = coord1.directional_offset_by(pa, sep/2)
    newHdr["HIERARCH SHRPCAP RA"] = midcoor.ra.to_string(unit=u.hourangle, sep= ":", precision=1)
    newHdr["HIERARCH SHRPCAP Dec"] = midcoor.dec.to_string(unit=u.deg, sep= ":", precision=0, alwayssign= True) + " (JNOW)"
    
def avgData(extension, f1, f2):
        data1 = f1[extension].data
        data2 = f2[extension].data
        return  np.array((data1 + data2) / 2)


def process_L1Y(obskey="20250116UTa"):
    
    PMpath='./FITS/' + obskey + '/'
    files = os.listdir(PMpath)
    filePairs = getFilePairs(files)

    
    for f1, f2 in filePairs:
        hdul1 = fits.open(PMpath+ '/' + f1)
        hdul2 = fits.open(PMpath+ '/' + f2)
        
        
        
        hdu = fits.PrimaryHDU(avgData(0, hdul1, hdul2))
        lonArr = fits.ImageHDU(hdul1[1].data)
        latArr = fits.ImageHDU(hdul2[2].data)
        incidenceArr = fits.ImageHDU(avgData(3, hdul1, hdul2))
        emissionArr = fits.ImageHDU(avgData(4, hdul1, hdul2))


        hdul = fits.HDUList([hdu, lonArr, latArr, incidenceArr, emissionArr])
        hdr1, hdr2 = hdul1[0].header, hdul2[0].header
        hdul[0].header = hdul1[0].header
        hdr = hdul[0].header
        print(hdr1["HIERARCH SHRPCAP Duration"])
        hdr["DATE-OBS"] = averageDates(hdr1["DATE-OBS"], hdr2["DATE-OBS"], "%Y-%m-%dT%H:%M:%S.%f")
        averageCameraDates(hdr, hdr1, hdr2, "TimeStamp")
        averageCameraDates(hdr, hdr1, hdr2, "StartCapture")
        averageCameraDates(hdr, hdr1, hdr2, "MidCapture")
        averageCameraDates(hdr, hdr1, hdr2, "EndCapture")
        averageHdrNum(hdr, hdr1, hdr2, "HIERARCH SHRPCAP JDStartCapture")
        averageHdrNum(hdr, hdr1, hdr2, "HIERARCH SHRPCAP JDMidCapture")
        averageHdrNum(hdr, hdr1, hdr2, "HIERARCH SHRPCAP JDEndCapture")
        averageHdrNum(hdr, hdr1, hdr2, "HIERARCH PLANMAP ET-OBS")
        prefix = "HIERARCH PLANMAP "
        hdr[prefix + "UTC-OBS"] = averageDates(hdr1[prefix + "UTC-OBS"], hdr2[prefix + "UTC-OBS"], "%Y-%m-%dT%H:%M:%S.%f")
       
        averageHdrNum(hdr, hdr1, hdr2, "HIERARCH SHRPCAP Focuser Temperature")
        averageHdrNum(hdr, hdr1, hdr2, "HIERARCH SHRPCAP Temperature")
        averageCoors(hdr,hdr1,hdr2)

        sumHdrNum(hdr, hdr1, hdr2, "HIERARCH SHRPCAP FrameCount")
        sumHdrNum(hdr, hdr1, hdr2, "HIERARCH PLANMAP SUBPOINT LAT")
        sumHdrNum(hdr, hdr1, hdr2, "HIERARCH PLANMAP SUBPOINT LON")
        sumHdrNum(hdr, hdr1, hdr2, "HIERARCH PLANMAP SUBSOL LAT")
        sumHdrNum(hdr, hdr1, hdr2, "HIERARCH PLANMAP SUBSOL LON")
        sumHdrNum(hdr, hdr1, hdr2, "HIERARCH PLANMAP LIGHT-TIME")
        sumHdrNum(hdr, hdr1, hdr2, "HIERARCH PLANMAP DISTANCE")
        key = "HIERARCH SHRPCAP Duration"
        
        hdr[key] = str(round(float(hdr1[key][:-1]) + float(hdr2[key][:-1]), 3)) + 's'
        print(hdr[key])
        #print(repr(hdr))
        #indices?
        fileDate = averageDates(f1[:15], f2[:15], "%Y-%m-%d-%H%M")
        fnout = fileDate + f1[17:]
        hdul.writeto(PMpath+fnout,overwrite=True)

        
        

        
        
        #hdul.writeto('new1.fits')
      
        hdul1.close()
        hdul2.close()


    
process_L1Y()
