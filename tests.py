# -*- coding: utf-8 -*-
import json
import os
#from datetime import datetime
import solution as s 

datedataref=['20250116UTa', '20250116UTb', '20250116UTc', '20250116UTd', 
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

H1Akeywordcount=21 #for 2025-01-16

labeledobsref=['2025-01-16-0117_8-Jupiter_656HIA.CameraSettings.txt', 
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

superfilterref={'20250116UTm': ['2025-01-16-0502_2-Jupiter_656HIA.CameraSettings.txt', 
                                '2025-01-16-0516_4-Jupiter_656HIA.CameraSettings.txt'], 
                '20250116UTn': ['2025-01-16-0523_1-Jupiter_656HIA.CameraSettings.txt', 
                                '2025-01-16-0537_3-Jupiter_656HIA.CameraSettings.txt'], 
                '20250116UTo': ['2025-01-16-0544_0-Jupiter_656HIA.CameraSettings.txt', 
                                '2025-01-16-0558_3-Jupiter_656HIA.CameraSettings.txt']}

with open('./Data_Samples/Catalog.json') as f:
    d = json.load(f)
    
print()
print("#########  BEGIN TESTS  ##########")
print()
print("getAllBetweenDates(d, '2025-01-16', '2025-01-17'")
datedata=s.getAllBetweenDates(d, '2025-01-16', '2025-01-17')
if datedata == datedataref:
    print("PASS")
else:
    print("FAIL")
print()


print("FilterbyKeyword ('656HIA')")
l1Files = os.listdir("./Data_Samples/20250116UT")
print(l1Files)
alldata=s.getCameraObservations(l1Files)
print(alldata)
fwkw=s.filterByKeyword(s.getCameraObservations(l1Files), '685NIR')
print(fwkw)
if len(fwkw) == H1Akeywordcount:
    print("PASS")
else:
    print("FAIL")
print()

print("Get labeled observations")
labeledObservations=s.getCameraObservations(l1Files)
if len(labeledObservations['data']) == H1Akeywordcount:
    print("PASS - correct number")
else:
    print("FAIL")
print()    
    
print("Get labeled observations for 20250116UTc")
if len(labeledObservations['data']['20250116UTc']) == 11:
    print("PASS - correct number")
else:
    print("FAIL")

if labeledObservations['data']['20250116UTc'] == labeledobsref:
    print("PASS - correct files")
else:
    print("FAIL")
print()

print("Filter by Obs date '2025-01-16 05:00' to '2025-01-16 06:00'")
fobsdate=s.filterObsByDate(s.getCameraObservations(l1Files) ,'2025-01-16 05:00', '2025-01-16 06:00')
print(len(fobsdate['data']))
if len(fobsdate) == 3:
    print("PASS - correct number")
else:
    print("FAIL")
if list(fobsdate.keys()) == ['20250116UTm','20250116UTn','20250116UTo']:
    print("PASS - correct obskeys")
else:
    print("FAIL")
print()

print("Filter by Obs date '2025-01-16 05:00' to '2025-01-16 06:00' AND keword")
superfilter=s.filterByKeyword(s.filterObsByDate(s.getCameraObservations(l1Files) ,'2025-01-16 05:00', '2025-01-16 06:00'),'656HIA')
if superfilter == superfilterref:
    print("PASS - identical")
else:
    print("FAIL")
