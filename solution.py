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

def getByTelescope(file, telescope):
    filtered= []
    for key in file:
        if ('Telescope' in file[key]) and file[key]['Telescope'] == telescope:
            filtered.append(key)
    return filtered

def isBetweenDates(file, startDate, endDate):
         date = datetime.fromisoformat(file[:15])
         print(file[:15])
         if startDate == 0:
            endDateTime = datetime.fromisoformat(endDate).replace(hour=23, minute=59)
            if endDateTime >= date:
                print(file)
                return True
         elif endDate == 0:
            startDateTime = datetime.fromisoformat(startDate)
            if startDateTime <= date:
                print(file)
                return True
         else:
            startDateTime = datetime.fromisoformat(startDate)
            endDateTime = datetime.fromisoformat(endDate).replace(hour=23, minute=59)
            if(min(date, startDateTime) == startDateTime and 
             max(date,endDateTime) == endDateTime):
                print(file)
                return True
         return False



def getNHBetweenDates(data, startDate, endDate):
    filtered = []
    for key,value in data.items():
         if isBetweenDates(value['NH3file'], startDate, endDate):
             filtered.append(key)
    return filtered
        


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
    
    print(getNHBetweenDates(d, '2025-01-06', '2025-01-16'))
    print(get_info("20200720UTa", d))

