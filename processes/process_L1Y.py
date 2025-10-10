import os
from astropy.io import fits
import matplotlib.pyplot as pl
import planetmapper as pm
import numpy as np
from datetime import datetime
from astropy.coordinates import SkyCoord
import astropy.units as u
import process_L1Y_helpers as hp
import cloud_pressure as cp


def process_L1Y(obskey="20250116UTa"):
    PMpath='./FITS/' + obskey + '/'
    files = os.listdir(PMpath)
    filePairs = hp.getFilePairs(files)

    OIContData = None
    HIAContData = None
    CH4ContData = None
    NH3ContData = None
    for f1, f2 in filePairs:
        hdul1 = fits.open(PMpath+ '/' + f1)
        hdul2 = fits.open(PMpath+ '/' + f2)
        
        hdu = fits.PrimaryHDU(hp.avgData(0, hdul1, hdul2))
        
        lonArr = fits.ImageHDU(hdul1[1].data)
        latArr = fits.ImageHDU(hdul2[2].data)
       
        incidenceArr = fits.ImageHDU(hp.avgData(3, hdul1, hdul2))
        emissionArr = fits.ImageHDU(hp.avgData(4, hdul1, hdul2))
        #average radiance
       

        hdul = fits.HDUList([hdu, lonArr, latArr, incidenceArr, emissionArr])
        hdr1, hdr2 = hdul1[0].header, hdul2[0].header
        hdul[0].header = hdul1[0].header
        hdr = hdul[0].header
        hdr["DATE-OBS"] = hp.averageDates(hdr1["DATE-OBS"], hdr2["DATE-OBS"], "%Y-%m-%dT%H:%M:%S.%f")
        hp.averageCameraDates(hdr, hdr1, hdr2, "TimeStamp")
        hp.averageCameraDates(hdr, hdr1, hdr2, "StartCapture")
        hp.averageCameraDates(hdr, hdr1, hdr2, "MidCapture")
        hp.averageCameraDates(hdr, hdr1, hdr2, "EndCapture")
        hp.averageHdrNum(hdr, hdr1, hdr2, "HIERARCH SHRPCAP JDStartCapture")
        hp.averageHdrNum(hdr, hdr1, hdr2, "HIERARCH SHRPCAP JDMidCapture")
        hp.averageHdrNum(hdr, hdr1, hdr2, "HIERARCH SHRPCAP JDEndCapture")
        hp.averageHdrNum(hdr, hdr1, hdr2, "HIERARCH PLANMAP ET-OBS")
        prefix = "HIERARCH PLANMAP "
        hdr[prefix + "UTC-OBS"] = hp.averageDates(hdr1[prefix + "UTC-OBS"], hdr2[prefix + "UTC-OBS"], "%Y-%m-%dT%H:%M:%S.%f")
       
        hp.averageHdrNum(hdr, hdr1, hdr2, "HIERARCH SHRPCAP Focuser Temperature")
        hp.averageHdrNum(hdr, hdr1, hdr2, "HIERARCH SHRPCAP Temperature")
        hp.averageCoors(hdr,hdr1,hdr2)

        hp.sumHdrNum(hdr, hdr1, hdr2, "HIERARCH SHRPCAP FrameCount")
        hp.sumHdrNum(hdr, hdr1, hdr2, "HIERARCH PLANMAP SUBPOINT LAT")
        hp.sumHdrNum(hdr, hdr1, hdr2, "HIERARCH PLANMAP SUBPOINT LON")
        hp.sumHdrNum(hdr, hdr1, hdr2, "HIERARCH PLANMAP SUBSOL LAT")
        hp.sumHdrNum(hdr, hdr1, hdr2, "HIERARCH PLANMAP SUBSOL LON")
        hp.sumHdrNum(hdr, hdr1, hdr2, "HIERARCH PLANMAP LIGHT-TIME")
        hp.sumHdrNum(hdr, hdr1, hdr2, "HIERARCH PLANMAP DISTANCE")
        key = "HIERARCH SHRPCAP Duration"
        
        hdr[key] = str(round(float(hdr1[key][:-1]) + float(hdr2[key][:-1]), 3)) + 's'

        fnout = hp.createL1FileName(f1, f2)
        hdul.writeto(PMpath+fnout,overwrite=True)   

        fnout = hp.createL2FileName(f1, f2)
        print(fnout)
        #print(repr(hdr))
        
        hdul[0].data = hp.normalizeBrightness(hdu, emissionArr)
        #write l2 files
        if("OI" in fnout):
            OIContData = hdul[0].data
            
        if("CH4" in fnout):
            hdul[0].data = hp.getMethaneTransmission(hdul[0].data,OIContData )
            hdul[0].header["CALIBRAT"] = 0.897
            CH4ContData = hdul[0].data
        if("HIA" in fnout):
            HIAContData = hdul[0].data
            
        if("NH3" in fnout):
            hdul[0].data = hp.getNH3WaveContData(hdul[0].data, OIContData, HIAContData)
            hdul[0].header["CALIBRAT"] = 0.964
            NH3ContData = hdul[0].data
        hdul.writeto(PMpath+fnout,overwrite=True) 

        #write L3 files

        if("CH4" in fnout):
            hdul[0].data = cp.computeCloudPressure(CH4ContData, hdul[0].data)
            print(hdul[0].data)
            hdul[0].header["HIERARCH KEFF CH4620"] = 0.427
            hdul.writeto(fnout[:30] + "L3PCld_S0.fits",overwrite=True) 
        if("NH3" in fnout):
             hdul[0].data = cp.computeAmmoniaMoleFraction(CH4ContData, hdul[0].data)
             hdul[0].header["HIERARCH KEFF CH4620"] = 0.427
             hdul[0].header["HIERARCH KEFF NH3647"] = 2.955
             hdul.writeto(fnout[:30] + "L3fNH3_S0.fits",overwrite=True)
           



    #create l3 files
    
    
    



        hdul.close() 
        hdul1.close()
        hdul2.close()


    
process_L1Y()
