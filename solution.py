import json
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np


def formatLB(ch, nh, rgb):
    obj = {}
    obj['CH4file'] = (ch + ".png") if ch else ""
    obj['NH3file'] = (nh + ".png") if nh else ""
    obj['RGBfile'] = (rgb + ".png") if rgb else ""
    return obj

def formatLTwo(prefix):
     obj = {}
     obj['TCH4'] = prefix + "L2TCH4.fits"
     obj['TNH3'] = prefix + "L2TNH3.fits"
     obj['CLSL'] = prefix + "L2CLSL.fits"
     return obj
     
def formatLThree(prefix):
     obj = {}
     obj['PCld'] = prefix + "L3PCld_S0.fits"
     obj['fNH3'] = prefix + "L3fNH3_S0.fits"
     return obj

#returns all files with specific telescope
def getByTelescope(file, telescope):
    filtered= []
    for key in file:
        if ('Telescope' in file[key]) and file[key]['Telescope'] == telescope:
            filtered.append(key)
    return filtered
#checks if date in filename is between dates inclusive, if start or end date is set as zero, 
#does not make comparison but at least one must be specified
def getEndDateTime(endDate):
    
    if len(endDate) <= 10:
        return datetime.fromisoformat(endDate).replace(hour=23, minute=59)
    else: 
        return datetime.fromisoformat(endDate)
        
def isBetweenDates(file, startDate, endDate):
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

#returns all files where RGB, CH4, and NH3 in specified date range
def getAllBetweenDates(data, startDate, endDate):
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
    filtered = []
    for key,value in data.items():
         if('NH3file' not in value):
             continue
         if isBetweenDates(value['NH3file'], startDate, endDate):
             filtered.append(key)
    return filtered
        

#returns object with metadata, LB, L2, and L3 file names
def get_info(obskey, data):
    obsData = data[obskey]
    ch = obsData['CH4file']
    nh = obsData['NH3file']
    rgb = obsData['RGBfile']
    obj =  {**obsData}
    prefix = nh[:26] or ch[:26] or rgb[:26]
    obj['L1B'] = formatLB(ch, nh, rgb)
    obj['L2'] = formatLTwo(prefix)
    obj['L3'] = formatLThree(prefix)
    #cleanObj(obsData)
    return obj


def cleanObj(data):
    data.pop('CH4file')
    data.pop('NH3file')
    data.pop('RGBfile')

def sortIntoObservations(files):
    res = []
    i = 0
    while i < len(files):
        obs = []
        fileOrder = ['450', '550', '685', '656', '632', '620', '647', '647', '620',  '632', '656']
        while(True):
            while len(fileOrder) and files[i][26:29] != fileOrder[-1]:
                fileOrder.pop()
            if not len(fileOrder):
                res.append(obs)
                break
            obs.append(files[i])
            fileOrder.pop()
            i += 1
    return res

#filters by date of first file(HIA)
def filterObsByDate(data , startDate, endDate):
    filteredData = {}
    for key, value in data.items():
        if isBetweenDates(value[0], startDate, endDate):
            filteredData[key] = value
    return filteredData
#looks for word in file name
def filterByKeyword(data, keyword):
    filteredData = {}
    for key, files in data.items():
        for file in files:
            if keyword in file:
                if not key in filteredData: filteredData[key] = []
                filteredData[key].append(file)
    return filteredData

   
#generates obskeys for each observation
def labelObservations(observations):
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
    sortedFiles = sortFilesByDate(getLAFiles(files, isCameraFile))
    observations = sortIntoObservations(sortedFiles)
    labeledObservations = labelObservations(observations)
    return labeledObservations


#sorts processing files based on date of file
#sorted into obskeys and then filter type
def sortIntoExtendedObservations(files, cameraFiles):
    res = {}
    i = 0
    for obsKey in cameraFiles.keys():
        
        fileObj = {}
        for cfile in cameraFiles[obsKey]:
            
            cdate = datetime.fromisoformat(cfile[:15])
            prefix = cfile[0:-19]
            fileArr = []
            while (i < len(files)):
                filedate = datetime.fromisoformat(files[i][:15])
                if filedate > cdate:
                    break
                if filedate == cdate:
                    fileArr.append(files[i])
                i += 1
            fileObj[prefix] = fileArr
        res[obsKey] = fileObj
    return res    

        
#gets files for processing from camera files
def getL1AProcessingFiles(files):
    cameraObservations = getCameraObservations(files)["data"]
    sortedFiles = sortFilesByDate(getLAFiles(files, isProcessingFile))
    observations = sortIntoExtendedObservations(sortedFiles, cameraObservations)
    print(observations)
    return observations
    


def getLAExtendedFiles(files):
    selectedFiles = []
    #for file in files:
        
def isCameraFile(file):
    return file[-18:] == 'CameraSettings.txt'

#identifies whether it is a png that is necessary for processing
def isProcessingFile(file):
    if not "png" in file:
        return False
    isRGBFile = ("BLU" in file or "GRN" in file or "NIR" in file)
    if isRGBFile:
        return "Flatstack" in file or "Aligned" in file or "WV" in file 
    else:
        return ("Flatstack" in file or "Aligned" in file) and "WV" not in file
def getLAFiles(files, selector):
    selectedFiles = []
    for file in files:
        if selector(file):
            selectedFiles.append(file)
    return selectedFiles

def sortFilesByDate(files):
    files.sort(key=lambda file: datetime.fromisoformat(file[:15]))
    return files


l1Files = os.listdir("./Data_Samples/20250116UT")


#creates json file with incomplete property for keys with missing files
def obsToJSON():
    with open('./observations.json', 'w', encoding='utf-8') as f:
        json.dump(getCameraObservations(l1Files), f, ensure_ascii=False, indent=4)
    

getL1AProcessingFiles(l1Files)

def createYearDatesArray(keys, year = None):
    dateData = []
 
    for key in keys:
        if (not year) or year == key[:4]:
            dateData.append(mdates.datestr2num(key[0:8]))
    return dateData

def createDatesArray(keys, year = None):
    dateData = []
    for key in keys:
        if (not year) or year == key[:4]:
            dateData.append(datetime.strptime("1492" + key[4:8], "%Y%m%d"))
            #dateData.append(mdates.datestr2num("1492" + key[4:8]))
  
    return dateData

def createYearsHistogram(data):  
    dates = createYearDatesArray(list(data.keys()))
    fig, ax = plt.subplots(1,1)
    ax.hist(dates, bins=70, color='blue')
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('20%y'))
    plt.xlabel("Year")
    plt.ylabel("Observations")
    plt.show()

def createHistogram(data, yearArr): 
    colorArr = ['red', 'black', 'blue', 'lightblue', 'green', 'orange']
    fig, ax = plt.subplots(1,1)
    
    year = 1492
    start = datetime(year, 1, 1)
    end = datetime(year, 12, 31)
    delta = end - start
    bins = [mdates.date2num(start + timedelta(days=i)) for i in range(delta.days + 2)]

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
    



with open('./Data_Samples/Catalog.json') as f:
    d = json.load(f)
    
    print()
    print("getAllBetweenDates(d, '2025-01-16', '2025-01-16'")
    print()
   
    print(getAllBetweenDates(d, '2025-01-16', '2025-01-16'))
    print()
   
    createHistogram(d, ['2020','2021', '2022', '2023', '2024', '2025'])
    #print("get_info('20200720UTa', d)")
    #print(get_info('20200720UTa', d))
    




