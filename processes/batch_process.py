import process_L1X as px
import process_L1Y as py
import os
import solution as s


def batch_process(obskey):
    #put it into subdirectory obskeys
    path="../Data_Samples/" + obskey
    l1Files = os.listdir(path)
    print(l1Files)
    fileMap = s.getL1AProcessingFiles(l1Files)
    for key in fileMap:
        print(key)
    for key in fileMap:

        file_list = fileMap[key]
       
        camera_obs_list = s.getCameraObservations(l1Files)["data"][key]
        px.process_L1X(obskey, file_list, camera_obs_list, key) 
    for key in fileMap:
        py.process_L1Y(obskey, key) 
        
    #px.process_L1X(obskey, "jupiter")
    #py.process_L1Y(obskey)
batch_process("20251017UT")

    