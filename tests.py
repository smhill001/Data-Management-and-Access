# -*- coding: utf-8 -*-
import json
import os
#from datetime import datetime
import solution as s 

###############################################################################
# Regression Test Reference Output Data
###############################################################################

Test1RefData=['20250116UTa', '20250116UTb', '20250116UTc', '20250116UTd', 
             '20250116UTe', '20250116UTf', '20250116UTg', '20250116UTh', 
             '20250116UTi', '20250116UTj', '20250116UTk', '20250116UTl', 
             '20250116UTm', '20250116UTn', '20250116UTo', '20250116UTp', 
             '20250116UTq', '20250116UTr', '20250116UTs', '20250116UTt', 
             '20250116UTu', '20250117UTa', '20250117UTb', '20250117UTc', 
             '20250117UTd', '20250117UTe', '20250117UTf', '20250117UTg', 
             '20250117UTh', '20250117UTi', '20250117UTj', '20250117UTk', 
             '20250117UTl', '20250117UTm', '20250117UTn', '20250117UTo', 
             '20250117UTp', '20250117UTq', '20250117UTr', '20250117UTs', 
             '20250117UTt']

Test2RefData={'20250116UTa': ['2025-01-16-0036_0-Jupiter_656HIA.CameraSettings.txt', '2025-01-16-0050_2-Jupiter_656HIA.CameraSettings.txt'], 
              '20250116UTb': ['2025-01-16-0056_9-Jupiter_656HIA.CameraSettings.txt', '2025-01-16-0111_1-Jupiter_656HIA.CameraSettings.txt'], 
              '20250116UTc': ['2025-01-16-0117_8-Jupiter_656HIA.CameraSettings.txt', '2025-01-16-0132_0-Jupiter_656HIA.CameraSettings.txt'], 
              '20250116UTd': ['2025-01-16-0138_7-Jupiter_656HIA.CameraSettings.txt', '2025-01-16-0152_9-Jupiter_656HIA.CameraSettings.txt'], 
              '20250116UTe': ['2025-01-16-0159_6-Jupiter_656HIA.CameraSettings.txt', '2025-01-16-0213_8-Jupiter_656HIA.CameraSettings.txt'], 
              '20250116UTf': ['2025-01-16-0220_5-Jupiter_656HIA.CameraSettings.txt', '2025-01-16-0234_7-Jupiter_656HIA.CameraSettings.txt'], 
              '20250116UTg': ['2025-01-16-0241_4-Jupiter_656HIA.CameraSettings.txt', '2025-01-16-0255_6-Jupiter_656HIA.CameraSettings.txt'], 
              '20250116UTh': ['2025-01-16-0304_1-Jupiter_656HIA.CameraSettings.txt', '2025-01-16-0318_4-Jupiter_656HIA.CameraSettings.txt'], 
              '20250116UTi': ['2025-01-16-0325_0-Jupiter_656HIA.CameraSettings.txt', '2025-01-16-0339_3-Jupiter_656HIA.CameraSettings.txt'], 
              '20250116UTj': ['2025-01-16-0347_3-Jupiter_656HIA.CameraSettings.txt', '2025-01-16-0401_6-Jupiter_656HIA.CameraSettings.txt'], 
              '20250116UTk': ['2025-01-16-0408_2-Jupiter_656HIA.CameraSettings.txt', '2025-01-16-0422_5-Jupiter_656HIA.CameraSettings.txt'], 
              '20250116UTl': ['2025-01-16-0441_3-Jupiter_656HIA.CameraSettings.txt', '2025-01-16-0455_5-Jupiter_656HIA.CameraSettings.txt'], 
              '20250116UTm': ['2025-01-16-0502_2-Jupiter_656HIA.CameraSettings.txt', '2025-01-16-0516_4-Jupiter_656HIA.CameraSettings.txt'], 
              '20250116UTn': ['2025-01-16-0523_1-Jupiter_656HIA.CameraSettings.txt', '2025-01-16-0537_3-Jupiter_656HIA.CameraSettings.txt'], 
              '20250116UTo': ['2025-01-16-0544_0-Jupiter_656HIA.CameraSettings.txt', '2025-01-16-0558_3-Jupiter_656HIA.CameraSettings.txt'], 
              '20250116UTp': ['2025-01-16-0604_9-Jupiter_656HIA.CameraSettings.txt', '2025-01-16-0619_2-Jupiter_656HIA.CameraSettings.txt'], 
              '20250116UTq': ['2025-01-16-0625_8-Jupiter_656HIA.CameraSettings.txt', '2025-01-16-0640_1-Jupiter_656HIA.CameraSettings.txt'], 
              '20250116UTr': ['2025-01-16-0646_8-Jupiter_656HIA.CameraSettings.txt', '2025-01-16-0701_0-Jupiter_656HIA.CameraSettings.txt'], 
              '20250116UTs': ['2025-01-16-0707_7-Jupiter_656HIA.CameraSettings.txt', '2025-01-16-0721_9-Jupiter_656HIA.CameraSettings.txt'], 
              '20250116UTt': ['2025-01-16-0728_6-Jupiter_656HIA.CameraSettings.txt', '2025-01-16-0742_8-Jupiter_656HIA.CameraSettings.txt'], 
              '20250116UTu': ['2025-01-16-0749_5-Jupiter_656HIA.CameraSettings.txt', '2025-01-16-0803_7-Jupiter_656HIA.CameraSettings.txt']}


Test3RefData=['2025-01-16-0117_8-Jupiter_656HIA.CameraSettings.txt', 
               '2025-01-16-0119_8-Jupiter_632OI.CameraSettings.txt', 
               '2025-01-16-0121_9-Jupiter_620CH4.CameraSettings.txt', 
               '2025-01-16-0123_9-Jupiter_647NH3.CameraSettings.txt', 
               '2025-01-16-0125_9-Jupiter_647NH3.CameraSettings.txt', 
               '2025-01-16-0127_9-Jupiter_620CH4.CameraSettings.txt', 
               '2025-01-16-0130_0-Jupiter_632OI.CameraSettings.txt', 
               '2025-01-16-0132_0-Jupiter_656HIA.CameraSettings.txt', 
               '2025-01-16-0133_8-Jupiter_685NIR.CameraSettings.txt', 
               '2025-01-16-0135_4-Jupiter_550GRN.CameraSettings.txt', 
               '2025-01-16-0136_9-Jupiter_450BLU.CameraSettings.txt']

Test5RefData={'20250116UTm': ['2025-01-16-0502_2-Jupiter_656HIA.CameraSettings.txt', 
                                '2025-01-16-0516_4-Jupiter_656HIA.CameraSettings.txt'], 
                '20250116UTn': ['2025-01-16-0523_1-Jupiter_656HIA.CameraSettings.txt', 
                                '2025-01-16-0537_3-Jupiter_656HIA.CameraSettings.txt'], 
                '20250116UTo': ['2025-01-16-0544_0-Jupiter_656HIA.CameraSettings.txt', 
                                '2025-01-16-0558_3-Jupiter_656HIA.CameraSettings.txt']}

with open('./Data_Samples/Catalog.json') as f:
    d = json.load(f)
    
print()
print("#########  BEGIN TESTS on Catalog.json  ##########")
print()

###############################################################################
print("TEST #1: getAllBetweenDates(d, '2025-01-16', '2025-01-17'")
datedata=s.getAllBetweenDates(d, '2025-01-16', '2025-01-17')
if datedata == Test1RefData:
    print("PASS - identical data")
else:
    print("FAIL - non-identical data")
print()

###############################################################################
print("TEST #2: FilterbyKeyword ('656HIA')")
l1Files = os.listdir("./Data_Samples/20250116UT")
#print(l1Files)
alldata=s.getCameraObservations(l1Files)
#print(alldata)
fwkw=s.filterByKeyword(s.getCameraObservations(l1Files)['data'], '656HIA')
#print(fwkw)
if len(fwkw) == len(Test2RefData):
    print("PASS - correct number")
else:
    print("FAIL - incorrect number")
if fwkw == Test2RefData:
    print("PASS - identical data")
else:
    print("FAIL - non-identical data")
print()

###############################################################################    
print("TEST #3: Get labeled observations for 20250116UTc")
labeledObservations=s.getCameraObservations(l1Files)
if len(labeledObservations['data']['20250116UTc']) == len(Test3RefData):
    print("PASS - correct number")
else:
    print("FAIL")

if labeledObservations['data']['20250116UTc'] == Test3RefData:
    print("PASS - correct files")
else:
    print("FAIL")
print()

###############################################################################
print("TEST #4: Filter by Obs date '2025-01-16 05:00' to '2025-01-16 06:00'")
fobsdate=s.filterObsByDate(s.getCameraObservations(l1Files)['data'] ,
                           '2025-01-16 05:00', '2025-01-16 06:00')
print(len(fobsdate))
if len(fobsdate) == 3:
    print("PASS - correct number")
else:
    print("FAIL")
if list(fobsdate.keys()) == ['20250116UTm','20250116UTn','20250116UTo']:
    print("PASS - correct obskeys")
else:
    print("FAIL")
print()

###############################################################################
print("TEST #5: Filter by Obs date '2025-01-16 05:00' to '2025-01-16 06:00' AND keword")
superfilter=s.filterByKeyword(s.filterObsByDate(s.getCameraObservations(l1Files)['data'],
                                                '2025-01-16 05:00','2025-01-16 06:00'),
                              '656HIA')
if superfilter == Test5RefData:
    print("PASS - identical")
else:
    print("FAIL - non-identical")


###############################################################################
print("TEST #6: Create Observations JSON from test data 20250116UT")
with open('./observations.json', 'w', encoding='utf-8') as f:
    json.dump(s.getCameraObservations(l1Files), f, ensure_ascii=False, indent=4)
print("TEST #9: Create Processing Files JSON from REAL data on 20241202UT")

###############################################################################
print("TEST #6a: Create Processing JSON from test data 20250116UT")
with open('./processing.json', 'w', encoding='utf-8') as f:
    json.dump(s.getL1AProcessingFiles(l1Files), f, ensure_ascii=False, indent=4)
    
###############################################################################
print("TEST #7: Create Observations JSON from test data 20250117UT")
#l1Files = os.listdir("./Data_Samples/20250117UT")
#with open('./observations.json', 'w', encoding='utf-8') as f:
#    json.dump(s.getCameraObservations(l1Files), f, ensure_ascii=False, indent=4)
        
###############################################################################
print("TEST #8: Create Observations JSON from REAL data on 20241202UT")

path="C:/Astronomy/Projects/Planets/Jupiter/Imaging Data/20241202UT"
l1Files = os.listdir(path)
with open(path+'/observations.json', 'w', encoding='utf-8') as f:
    json.dump(s.getCameraObservations(l1Files), f, ensure_ascii=False, indent=4)
    
###############################################################################

"""
print("TEST #8: Create Observations JSON from test data")

pth="C:/Astronomy/Projects/Planets/Jupiter/Imaging Data/"
subdirs=next(os.walk(pth))[1]
for subdir in subdirs:
    print(subdir)
    path=pth+subdir
    l1Files = os.listdir(path)
    print(l1Files)
    if int(subdir[:4]) >2024:
        with open(path+'/'+subdir+'observations.json', 'w', encoding='utf-8') as f:
            print(s.getCameraObservations(l1Files))
            json.dump(s.getCameraObservations(l1Files), f, ensure_ascii=False, indent=4)
            f.close()
"""



