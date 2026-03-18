import process_L1X as px
import process_L1Y as py
import os
import solution as s
from config import config


def batch_process(obskey,L1X=True,L1Y=True):

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

    
    input_path =  'Test_Data/Inputs' if config['test_mode'] else config['input']
    input_path = input_path + "/" + obskey
    print(input_path)
    l1Files = os.listdir(input_path)
    print(l1Files)
    fileMap = s.getL1AProcessingFiles(l1Files)
    output_path =  'Test_Data/New_Results' if config['test_mode'] else config['output']
    
    if L1X:
        px.process_L1X(obskey, input_path, output_path)
    if L1Y:
        for key in fileMap:
           py.process_L1Y(obskey, key, output_path) 


        
    
batch_process("20251017UT")

    