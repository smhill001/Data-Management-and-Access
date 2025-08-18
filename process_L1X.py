def process_L1X(obskey="20250116UTa",planet='Jupiter'):

    import planetmapper
    import os
    import solution as s
    
    path="./Data_Samples/20250116UT/"
    l1Files = os.listdir(path)
    file_list=s.getL1AProcessingFiles(l1Files)[obskey]
    camera_obs_list = s.getCameraObservations(l1Files)["data"][obskey]
    
    planetmapper.set_kernel_path('~/Jupiter/Data-Management-and-Access')

    First=True
    i = 0
    for fn in file_list:
        """if not "450BLU" in fn:
            continue"""
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
        #filetype = fn[fn.index('_') + 1: fn.index('-')]
        
        camera_file = camera_obs_list[i]
       #ioptron key does not fit standard
        with open(path + camera_file, 'r') as cf:
            for line in cf:
                pair = line.strip()
                if "iOptron" in pair:
                    startIndex = pair.index('=')
                    key1 = 'RA'
                    commaIndex = pair.find(',', startIndex)
                    value1 = pair[startIndex + 4: commaIndex]
                    key2 = 'Dec'
                    value2 = pair[pair.find('=', commaIndex) + 1:]
                    observation.append_to_header(key1, value1, hierarch_keyword=True)
                    observation.append_to_header(key2, value2, hierarch_keyword=True)

                elif "=" in pair:
                    key = pair[:pair.index('=')]
                    value = pair[pair.index('=') + 1:]
                   
                    observation.append_to_header(key, value, hierarch_keyword=True)
        i += 1

        observation.save_observation(fn.replace(".png",".fits"))
        observation.save_mapped_observation(fn.replace(".png","map.fits"))
        First=False
process_L1X()
