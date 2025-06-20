import json
from datetime import datetime


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
def isBetweenDates(file, startDate, endDate):
         date = datetime.fromisoformat(file[:15])
         if startDate == 0:
            endDateTime = datetime.fromisoformat(endDate).replace(hour=23, minute=59)
            if endDateTime >= date:
                return True
         elif endDate == 0:
            startDateTime = datetime.fromisoformat(startDate)
            if startDateTime <= date:
                return True
         else:
            startDateTime = datetime.fromisoformat(startDate)
            endDateTime = datetime.fromisoformat(endDate).replace(hour=23, minute=59)
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



with open('Data_Samples/Catalog.json') as f:
    d = json.load(f)
    print()
    print("getAllBetweenDates(d, '2025-01-16', '2025-01-16'")
    print()
    print(getAllBetweenDates(d, '2025-01-16', '2025-01-16'))
    print()
    print("get_info('20200720UTa', d)")
    print(get_info('20200720UTa', d))

