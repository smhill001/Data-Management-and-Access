import json

def formatLB(ch, nh, rgb):
    obj = {}
    obj['CH4file'] = (ch + ".png") if ch else ""
    obj['NH3file'] = (nh + ".png") if nh else ""
    obj['RGBfile'] = (rgb + ".png") if rgb else ""
    return obj

def formatLTwo(prefix):
     obj = {}
     obj['TCH4'] = prefix + "L2TCH4.fits"
     obj['TNH3'] = prefix + "L2NH3.fits"
     obj['CLSL'] = prefix + "L2CLSL.fits"
     return obj
     
def formatLThree(prefix):
     obj = {}
     obj['PCld'] = prefix + "L3PCld_S0.fits"
     obj['fNH3'] = prefix + "L3fNH3_S0.fits"
     return obj

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
    cleanObj(obsData)
    return obj

def cleanObj(data):
    data.pop('CH4file')
    data.pop('NH3file')
    data.pop('RGBfile')

with open('Data_Samples/Catalog.json') as f:
    d = json.load(f)
    print(get_info("20200720UTa", d))

