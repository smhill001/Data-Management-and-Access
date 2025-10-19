import os
from astropy.io import fits
import matplotlib.pyplot as pl
import planetmapper as pm
import numpy as np
from datetime import datetime
from astropy.coordinates import SkyCoord
import astropy.units as u



def getMethaneTransmission(methaneMap, contMap):
    return np.array((methaneMap / contMap) * 0.897) 
def getNH3Calibration():
    return (647 - 632) / (656-632)

def getNH3WaveContData(NH3Map, IOMap, HIAMap):
     #(1-X)R632+X*R656), where X=(647 – 632)/(656 – 632) 
    x = (647 - 632) / (656-632)
    a = (1-x) * (IOMap)
    b = x * HIAMap
    #a = (x) * (IOMap)
    #b = (1-x) * HIAMap
    return 0.964*NH3Map / (a + b)
   


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
    """
         Averages RA and Dec from headers and put both result into new header
         
    """
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


def createL1FileName(f1, f2):
    """
    Creates file name for calibrated L1 map file
    Parameters:
    f1(string): file name
    f2(string): file name
    Returns:
    string: file name with date averaged from inputs and L1 Map suffix inserted
    """
    f1Seconds = str(int((float(f1[16]) * 0.1) * 60)).zfill(2)
    f2Seconds = str(int((float(f2[16]) * 0.1) * 60)).zfill(2)
    fileDate = averageDates(f1[:15] + f1Seconds, f2[:15] + f2Seconds, "%Y-%m-%d-%H%M%S")
    seconds = str(int((float(fileDate[16:]) / 60) * 10))
    filterIndex = f1.find("Jupiter_") + 8
    filter = f1[filterIndex: f1.find("-", filterIndex)]
    fnout = fileDate[:15] + "_" + seconds + "-Jupiter_" + filter + "_L1Map.fits"
    return fnout

def createL2FileName(f1, f2):
    f1Seconds = str(int((float(f1[16]) * 0.1) * 60)).zfill(2)
    f2Seconds = str(int((float(f2[16]) * 0.1) * 60)).zfill(2)
    fileDate = averageDates(f1[:15] + f1Seconds, f2[:15] + f2Seconds, "%Y-%m-%d-%H%M%S")
    seconds = str(int((float(fileDate[16:]) / 60) * 10))
    filterIndex = f1.find("Jupiter_") + 8
    filter = f1[filterIndex + 3: f1.find("-", filterIndex)]
    fnout = fileDate[:15] + "_" + seconds + "-Jupiter_Map_L2T" + filter + ".fits"
    return fnout



def normalizeBrightness(radianceArr, emissionArr):
    rows = radianceArr.shape[1]
    cols = radianceArr.shape[2]
    radianceSum = 0
    radianceCount = 0
   
    for r in range(rows):
        for c in range(cols):
            #if emissionArr.data[r][c] < 85:
            if emissionArr.data[r][c] < 80.:
                radianceSum += radianceArr.data[0][r][c]
                radianceCount += 1
    avgRadiance = radianceSum / radianceCount
    print("*radianceCount ",radianceCount)
  
    return np.array(radianceArr.data / avgRadiance)