import process_L1X as px
import process_L1Y as py
import os
import solution as s


def batch_process(obskey):

    '''
    Takes filter pngs of Jupiter and outputs mapped fits of
      ammonia mole fraction and cloud pressure

    Input: String formatted as YYYYMMDDUT, which refers to a 
    directory of png files in Data samples directory  

    Output:
    Creates directory in FITS directory with same name, and creates a list of subdirectories
    with unprocessed_L1, L1, L2, and L3 subdirectories containing fits files. The L3 directory contains the final mapped fits 
    of ammonia mole fraction and cloud pressure
    '''

    path="../Data_Samples/" + obskey
    l1Files = os.listdir(path)
    fileMap = s.getL1AProcessingFiles(l1Files)
    
  
    px.process_L1X(obskey)
    for key in fileMap:
        py.process_L1Y(obskey, key) 
        
    
batch_process("20251016UT")

    