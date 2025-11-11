import process_L1X as px
import process_L1Y as py
import os
import solution as s


def batch_process(obskey):
    #put it into subdirectory obskeys
    path="../Data_Samples/" + obskey
    l1Files = os.listdir(path)
    fileMap = s.getL1AProcessingFiles(l1Files)
    
  
    px.process_L1X(obskey)
    for key in fileMap:
        py.process_L1Y(obskey, key) 
        
    
batch_process("20251017UT")

    