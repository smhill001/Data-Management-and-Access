import json
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np


def formatLB(ch, nh, rgb):
    """
    Converts CH4, NH3, and RGB file prefixes into an object with their L1B file names 
    
    Parameters:
      ch (string): CH4 file name consisting of date and other info
      nh (string): NH3 file name with date and other info
      rgb (string): RGB file in with date and other info
    Returns:
      object: has keys for each file with .png suffix


    """
    obj = {}
    obj['CH4file'] = (ch + ".png") if ch else ""
    obj['NH3file'] = (nh + ".png") if nh else ""
    obj['RGBfile'] = (rgb + ".png") if rgb else ""
    return obj
#???
def formatLTwo(prefix):
     """
     Uses file prefix to create L2 file names 
    
     Parameters:
      prefix (string): format YYYY-MM-DD-HHMM_S-Jupiter-
    Returns:
      object: contains L2 file name for TCH4, TNH3, and CLSL
    """
     obj = {}
     obj['TCH4'] = prefix + "L2TCH4.fits"
     obj['TNH3'] = prefix + "L2TNH3.fits"
     obj['CLSL'] = prefix + "L2CLSL.fits"
     return obj
     
def formatLThree(prefix):
     """
     Uses file prefix to create L2 file names
    
     Parameters:
      prefix (string): format YYYY-MM-DD-HHMM_S-Jupiter-
    Returns:
      object: contains L3 file name for PCld and fNH3
    """
     obj = {}
     obj['PCld'] = prefix + "L3PCld_S0.fits"
     obj['fNH3'] = prefix + "L3fNH3_S0.fits"
     return obj

#returns all files with specific telescope
def getByTelescope(file, telescope):
    """
    Finds all the obskeys using a given telescope
    
    Parameters:
    file (json): catolog.json of obskeys with filenames and metadata
    telescope (string): telescope we are looking for

    Returns: 
    filtered (arr): contains the obskeys with the telescope
    """
    filtered= []
    for key in file:
        if ('Telescope' in file[key]) and file[key]['Telescope'] == telescope:
            filtered.append(key)
    return filtered

def getEndDateTime(endDate):
    """
    Formats endDate so date converted to end of day if no time specified for inclusive date checking
    
    Parameters: 
    endDate(string): date to format

    Returns:
    datetime: end of the day if no time specified, otherwise same date
    
    
    """
    if len(endDate) <= 10:
        return datetime.fromisoformat(endDate).replace(hour=23, minute=59)
    else: 
        return datetime.fromisoformat(endDate)
        
def isBetweenDates(file, startDate, endDate):
         """
         Checks whether a file was taken in a given date range

         Parameters:
         file (string): file name beggining with  YYYY-MM-DD-HHMM_S,
         startDate (string || 0): Lower bound date  (day or time), 0 means no start date
         endDate (string || 0): Upper bound date (day or time), 0 means no end date

         Returns:
         Boolean: True if is within start and end date inclusive
         
         """
         date = datetime.fromisoformat(file[:15])
         
         if startDate == 0:
            endDateTime = getEndDateTime(endDate)
            if endDateTime >= date:
                return True
         elif endDate == 0:
            startDateTime = datetime.fromisoformat(startDate)
            if startDateTime <= date:
                return True
         else:
            startDateTime = datetime.fromisoformat(startDate)
            endDateTime = getEndDateTime(endDate)
            if(min(date, startDateTime) == startDateTime and 
             max(date,endDateTime) == endDateTime):
                return True
         return False


def getAllBetweenDates(data, startDate, endDate):

    """
    Returns list of obskeys RGB, CH4, and NH3 files are in date range

    Parameters:
    data (json): catalog.json
    startDate (string): lower date bound
    endDate (string): upper date bound

    Returns:
    array: list of obskeys in catalog.json where files are present and in date range

    """
    filtered = []
    for key,value in data.items():
         if ('RGBfile' not in value or 'NH3file' not in value or 'CH4file' not in value):
             continue
         if (isBetweenDates(value['RGBfile'], startDate, endDate) and
            isBetweenDates(value['NH3file'], startDate, endDate) and
            isBetweenDates(value['CH4file'], startDate, endDate)):
                filtered.append(key)
    return filtered
#returns all files where NH3 in date range
def getNHBetweenDates(data, startDate, endDate):
    """
    Returns list of obskeys NH3 files are in date range

    Parameters:
    data (json): catalog.json
    startDate (string): lower date bound
    endDate (string): upper date bound

    Returns:
    array: list of obskeys in catalog.json where NH3 file is present and in date range

    """
    filtered = []
    for key,value in data.items():
         if('NH3file' not in value):
             continue
         if isBetweenDates(value['NH3file'], startDate, endDate):
             filtered.append(key)
    return filtered
        


def get_info(obskey, data):
    """
    Creates an object containing L1B, L2, and L3 file names for a specific obskey in catalog.json

    Parameters:
    obskey (string): observation key in catalog.json
    data (json): catalog.json

    Returns: 
    Object: Updated observation object with file names for each level of processing files
    
    """
    obsData = data[obskey]
    ch = obsData['CH4file']
    nh = obsData['NH3file']
    rgb = obsData['RGBfile']
    obj =  {**obsData}
    prefix = nh[:26] or ch[:26] or rgb[:26]
    obj['L1B'] = formatLB(ch, nh, rgb)
    obj['L2'] = formatLTwo(prefix)
    obj['L3'] = formatLThree(prefix)
    
    return obj



def sortIntoObservations(files):
    """
    organizes list of L1A filenames into observations

    Parameter:
    files (array): list of LA files sorted by date ascending
    Returns: 
    array: list of filename arrays with 11 files each,  comprising observations
    
    """
    res = []
    i = 0
    while i < len(files):
        obs = []
        fileOrder = ['450', '550', '685', '656', '632', '620', '647', '647', '620',  '632', '656']
        while(i < len(files)):
            while len(fileOrder) and (
                not '_' + fileOrder[-1] in files[i]
                and not 'R' + fileOrder[-1] in files[i]
                ):
                fileOrder.pop()
            if not len(fileOrder):
                res.append(obs) 
                break
            obs.append(files[i])
            fileOrder.pop()
            i += 1
       
    return res

#get by end date?
def filterObsByDate(data , startDate, endDate):
    """
    filters object by date range 

    Parameters:
    data (Object): Obskey with observation array
    startDate (string): lower date bound
    endDate (string): upper date bound

    Returns:
    Object: obskeys with first file of observation in date range
    """
    filteredData = {}
    for key, value in data.items():
        if isBetweenDates(value[0], startDate, endDate):
            filteredData[key] = value
    return filteredData

def filterByKeyword(data, keyword):
    """
    filters observations by substring in filename

    Parameters:
    data(Object): keys with values being list of filenames
    keyword (string): substring to filter filenames by

    Returns:
    Object: keys with filename arrays filtered by keyword
    """
    filteredData = {}
    for key, files in data.items():
        for file in files:
            if keyword in file:
                if not key in filteredData: filteredData[key] = []
                filteredData[key].append(file)
    return filteredData

   
#generates obskeys for each observation
def labelObservations(observations):

    """
    Builds object with obskeys for observations and identifies incomplete obskeys
    Parameters:
    observations(array): array of filename arrays(max 11) (observations) ascending date
    Returns:
    object: contains data property with each file array assigned to unique obskey and 
    incomplete property with obskeys with incomplete file arrays
    
    """
    labeledObs = {}
    incompleteObs = []
    for index, obs in enumerate(observations):
        label = obs[0][:10].replace("-","") + "UT" + chr(ord('a') + index)
        labeledObs[label] = obs
        if len(obs) < 11:
            incompleteObs.append(label)
    
    return {"data": labeledObs, "incomplete": incompleteObs}


#get camera.txt
def getCameraObservations(files):
    """
    gets object with camera files sorted into observations
    Parameters:
    files (array): list of LA file names
    Returns:
    Object: data: camera.txt files sorted into observations and assigned obskeys
            incomplete: list of incomplete observations
    """
    #print('sorting files by date')
    sortedFiles = sortFilesByDate(getLAFiles(files, isCameraFile))
    #print('sorting into observations')
    observations = sortIntoObservations(sortedFiles)
    #print('labeling observations')
    labeledObservations = labelObservations(observations)
    return labeledObservations



def sortIntoExtendedObservations(files, cameraFiles):
    """
    sorts file list into obskeys based on obskeys for camera.txt files
    Parameters: 
    files (array): array of L1A files in ascending date order
    cameraFiles (object): camera.txt file names sorted into obskeys
    Returns:
    Object: array of files for each obskey created
    by comparing date taken to date of camera.txt files in that obskey

    """
    res = {}
    i = 0
    for obsKey in cameraFiles.keys():
        fileObj = {}
        fileArr = []
        for cfile in cameraFiles[obsKey]:
            
            cdate = datetime.fromisoformat(cfile[:15])
            prefix = cfile[0:-19]
            while (i < len(files)):
                filedate = datetime.fromisoformat(files[i][:15])
                if filedate > cdate:
                    break
                if filedate == cdate:
                    fileArr.append(files[i])
                i += 1
            #fileObj[prefix] = fileArr
        #print("fileArr=",fileArr)
        fileObj = fileArr
        res[obsKey] = fileObj
    return res    

        
#gets files for processing from camera files
def getL1AProcessingFiles(files):
    """
    Gets L1A filenames needed for processing using camera observations
    Parameters:
    files (array): List of file names
    Returns:
    object: obskeys each with an array of .png filenames:
        science files: flatstack, aligned, no WV , 
        context files: flatstack, aligned, WV 
        
    
    """
    cameraObservations = getCameraObservations(files)["data"]
    sortedFiles = sortFilesByDate(getLAFiles(files, isProcessingFile))
    observations = sortIntoExtendedObservations(sortedFiles, cameraObservations)
    #print(observations)
    return observations
    
def isCameraFile(file):
    """
    Determines if file is for camera settings
    Parameters:
    file (string): file name
    Returns:
    Boolean: Whether it is a camera settings file
    
    """
    return file[-18:] == 'CameraSettings.txt'

#identifies whether it is a png that is necessary for processing
def isProcessingFile(file):
    """
    Determines if file is needed for processing
    Parameters:
    file (string): file name
    Returns:
    Boolean: Whether it is WV, aligned, flatstack for context or not WV, aligned, flatstack for science
    """
    if not "png" in file:
        return False
    isRGBFile = ("BLU" in file or "GRN" in file or "NIR" in file)
    if isRGBFile:
        return "Flatstack" in file or "Aligned" in file and "WV" in file 
    else:
        return ("Flatstack" in file or "Aligned" in file) and "WV" not in file
    
def getLAFiles(files, selector):
    """
    gets a list of files filtered by a selector

    Parameters:
    files (array): lsit of LA file names 
    selector (function): function to filter file names
    Returns:
    array: list of filtered file names
    
    """
    selectedFiles = []
    for file in files:
        if selector(file):
            selectedFiles.append(file)
    return selectedFiles

def sortFilesByDate(files):
    """
    Parameters: 
    files (array): list of file names
    Returns:
    array: files sorted by date ascending
    
    """
    files.sort(key=lambda file: datetime.fromisoformat(file[:15]))
    return files


l1Files = os.listdir("../Data_Samples/20250117UT")


#creates json file with incomplete property for keys with missing files
def obsToJSON():
    """
    Side Effect: loads object with camera observations into a json 
    -data property with list of obskeys and their files array
    -incomplete property with list of obskeys containing less than eleven files
   

    """
    with open('../observations.json', 'w', encoding='utf-8') as f:
        json.dump(getCameraObservations(l1Files), f, ensure_ascii=False, indent=4)
    
obsToJSON()
getL1AProcessingFiles(l1Files)

def createYearDatesArray(keys, year = None):
    """
    Gets array of dates of observations in a year to plot observation frequency
    Parameters:
    keys (array): array of obskeys
    year (string): year we want to get observations dates for
    Returns:
    Array: array of dates each obskey was taken with duplicates

    
    """
    dateData = []
 
    for key in keys:
        if (not year) or year == key[:4]:
            dateData.append(mdates.datestr2num(key[0:8]))
    return dateData

def createDatesArray(keys, year = None):
    """
    Gets array of dates of observations in a year to plot observation frequency
    Parameters:
    keys (array): array of obskeys
    year (string): year we want to get observations dates for
    Returns:
    Array: array of dates each obskey was taken with duplicates with year replaced to be the same

    
    """
    dateData = []
    for key in keys:
        if (not year) or year == key[:4]:
            dateData.append(datetime.strptime("1492" + key[4:8], "%Y%m%d"))
  
    return dateData

def createYearsHistogram(data):  
    """
    Parameters:
    data (object): catalog.json

    Side Effect:
    Creates histogram showing observation frequency each month from 2020 and 2026
    """
    dates = createYearDatesArray(list(data.keys()))
    fig, ax = plt.subplots(1,1)
    bins = []
    for year in range(2020, 2026):
        bins += [datetime(year, month, 1) for month in range(1, 13)]
  
    ax.hist(dates, bins=bins, color='blue')
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('20%y'))
    
    plt.xlabel("Year")
    plt.ylabel("Observations")
    plt.show()

def createHistogram(data, yearArr): 
    """
    Parameters:
    data (object): catalog.json

    Side Effect:
    Creates overlapping histograms comparing observation frequency each months for each year
    """
    colorArr = ['red', 'black', 'blue', 'lightblue', 'green', 'orange']
    fig, ax = plt.subplots(1,1)
    
    year = 1492
    start = datetime(year, 1, 1)
    end = datetime(year, 12, 31)
    delta = end - start
    bins = [mdates.date2num(start + timedelta(days=i)) for i in range(delta.days + 2)]
   
    
    ax.set_xlim(start, end)
    for i in range(len(yearArr)):
        dates = createDatesArray(list(data.keys()), yearArr[i])
        ax.hist(dates, bins = bins, alpha = 0.5, color = colorArr[i], label=yearArr[i])
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b')) 
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.ylabel("Observations")
    plt.show()
    



with open('../Data_Samples/Catalog.json') as f:
    d = json.load(f)
    """
    print()
    print("getAllBetweenDates(d, '2025-01-16', '2025-01-16'")
    print()
   
    print(getAllBetweenDates(d, '2025-01-16', '2025-01-16'))
    print()
   """
    createHistogram(d, ['2020','2021', '2022', '2023', '2024', '2025'])
    createYearsHistogram(d)
    #print("get_info('20200720UTa', d)")
    #print(get_info('20200720UTa', d))
    
l1Files = os.listdir("../Data_Samples/20250116UT")
fwkw=filterByKeyword(getCameraObservations(l1Files), '685NIR')
#print(fwkw)

labeledObservations=getCameraObservations(l1Files)
#print(labeledObservations, len(labeledObservations['data']))

#print("Filter by Obs date '2025-01-16 05:00' to '2025-01-16 06:00'")
#fobsdate=filterObsByDate(getCameraObservations(l1Files) ,'2025-01-16 05:00', '2025-01-16 06:00')
#print(len(fobsdate['data']))
#if len(fobsdate) == 3:
#    print("PASS - correct number")
#else:
#    print("FAIL")
#if list(fobsdate.keys()) == ['20250116UTm','20250116UTn','20250116UTo']:
#    print("PASS - correct obskeys")
#else:
#    print("FAIL")
#print(