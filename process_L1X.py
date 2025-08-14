def process_L1X(obskey="20250116UTa",planet='Jupiter'):

    import planetmapper
    import os
    import solution as s
    
    path="./Data_Samples/20250116UT/"
    l1Files = os.listdir(path)
    file_list=s.getL1AProcessingFiles(l1Files)[obskey]
    
    First=True
    for fn in file_list:
        time=fn[0:10]+"T"+fn[11:13]+":"+fn[13:15]
        observation = planetmapper.Observation(path+fn,target=planet,utc=time)
        #print("1##########observation.backplanes=",list(observation.backplanes.keys()))
        
        del observation.backplanes['DOPPLER']
        del observation.backplanes['LON-CENTRIC']
        del observation.backplanes['LAT-CENTRIC']
        del observation.backplanes['RA']
        del observation.backplanes['DEC']
        del observation.backplanes['KM-X']
        del observation.backplanes['KM-Y']
        del observation.backplanes['RING-RADIUS']
        del observation.backplanes['RING-LON-GRAPHIC']
        del observation.backplanes['RING-DISTANCE']
        del observation.backplanes['LIMB-LON-GRAPHIC']
        del observation.backplanes['LIMB-DISTANCE']
        del observation.backplanes['RADIAL-VELOCITY']
        del observation.backplanes['LOCAL-SOLAR-TIME']
        del observation.backplanes['AZIMUTH']
        del observation.backplanes['PHASE']
        del observation.backplanes['LIMB-LAT-GRAPHIC']
        del observation.backplanes['ANGULAR-X']
        del observation.backplanes['ANGULAR-Y']
        del observation.backplanes['PIXEL-X']
        del observation.backplanes['PIXEL-Y']
        del observation.backplanes['DISTANCE']
        #print("******************")
        #print("2##########observation.backplanes=",observation.backplanes.keys())
        
        if First:
            coords = observation.run_gui()
            #print("coords",coords)
            params=observation.get_disc_params()
            print("######### params1=",params)
        else:
            observation.set_disc_params(params[0],params[1],params[2],params[3])

        #observation.add_header_metadata()
        observation.append_to_header('HEIRARCH SHRPCAP '+'TESTKEY','This is a test',hierarch_keyword=False)

        observation.save_observation(fn.replace(".png",".fits"))
        observation.save_mapped_observation(fn.replace(".png","map.fits"))
        First=False
