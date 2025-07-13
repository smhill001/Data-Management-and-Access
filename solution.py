import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates



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
    for index, obs in enumerate(observations):
        label = obs[0][:10].replace("-","") + "UT" + chr(ord('a') + index)
        labeledObs[label] = obs
    return labeledObs

def getObservations(files):
    sortedFiles = sortFilesByDate(getLAFiles(files))
    observations = sortIntoObservations(sortedFiles)
    labeledObservations = labelObservations(observations)
    return labeledObservations
    


def getLAFiles(files):
    selectedFiles = []
    for file in files:
        last = file[-18:]
        if last == 'CameraSettings.txt':
            selectedFiles.append(file)
    return selectedFiles

def sortFilesByDate(files):
    files.sort(key=lambda file: datetime.fromisoformat(file[:15]))
    return files


l1Files = os.listdir("./Data_Samples/20250116UT")

with open('./observations.json', 'w', encoding='utf-8') as f:
    json.dump(getObservations(l1Files), f, ensure_ascii=False, indent=4)

def createDatesArray(keys, year = None):
    dateData = []
    print(len(keys))
    for key in keys:
        if (not year) or year == key[:4]:
            dateData.append(mdates.datestr2num(key[:8]))
    return dateData

def createYearsHistogram(data):  
    dates = createDatesArray(list(data.keys()))
    fig, ax = plt.subplots(1,1)
    ax.hist(dates, bins=70, color='blue')
    #
    #ax.set_xticks(selected_dates)
    #ax.set_xticklabels(labels)
    #
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('20%y'))
    plt.xlabel("Year")
    plt.ylabel("Observations")
    plt.show()

def createHistogram(data, year): 
    dates = createDatesArray(list(data.keys()), year)
    print(dates)
    fig, ax = plt.subplots(1,1)
    ax.hist(dates, bins=365, color='black')
    #
    #ax.set_xticks(selected_dates)
    #ax.set_xticklabels(labels)
    #
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    #ax.xaxis.set_major_formatter(mdates.DateFormatter('%m'))
    ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    plt.xticks(rotation=45)
    plt.tight_layout()
  
    plt.ylabel("Observations")
    plt.xlabel(year)
    plt.show()
    



with open('./Data_Samples/Catalog.json') as f:
    d = json.load(f)
    
    print()
    print("getAllBetweenDates(d, '2025-01-16', '2025-01-16'")
    print()
   
    print(getAllBetweenDates(d, '2025-01-16', '2025-01-16'))
    print()
    #print(createDatesArray(list(d.keys())))
    createYearsHistogram(d)
    #print("get_info('20200720UTa', d)")
    #print(get_info('20200720UTa', d))
    




