def read_fits_helper(pathandfile,target="Jupiter",LonSys='3',
                     LimbCorrection=False):
    
    import get_spice_ephem as sp_ephem
    from astropy.io import fits
    import numpy as np
    from copy import deepcopy
    from matplotlib import pyplot as pl

    dataobj={}
    
    hdulist=fits.open(pathandfile)
    hdulist.info()
    dataobj['hdr']=hdulist[0].header
    dataobj['data']=np.flipud(hdulist[0].data[0])
    dataobj['lon']=np.flipud(hdulist[1].data)
    dataobj['lat']=np.flipud(hdulist[2].data)
    dataobj['sza']=np.flipud(hdulist[3].data) #!!!! Might have eza and sza reversed
    dataobj['eza']=np.flipud(hdulist[4].data) #!!!! Might have eza and sza reversed
    hdulist.close()


    CM3ck=float(dataobj['hdr']["HIERARCH PLANMAP SUBPOINT LON"])
    eph=sp_ephem.get_spice_ephem(dataobj['hdr']["DATE-OBS"],planet='target')
    dataobj['CM1']=float(eph[0].strip())
    dataobj['CM2']=float(eph[1].strip())
    dataobj['CM3']=float(eph[2].strip())
    if np.abs(CM3ck-dataobj['CM3'])>0.01:
        print("CM ERROR")
        
    if LimbCorrection and 'BUNIT' in dataobj['hdr']:
        exponent={'Cloud-top Press':0.25,'Mole Fraction':0.55}
        amfdata=(1.0/(np.cos(dataobj['sza']*np.pi/180))+1.0/np.cos(dataobj['eza']*np.pi/180.))/2.0
        dataobj['data']=dataobj['data']*(amfdata**exponent[dataobj['hdr']['BUNIT']])
        
    dataobj['datar']=deepcopy(np.roll(dataobj['data'],int(dataobj['CM3']-dataobj['CM'+LonSys]),axis=1))
    """
    fig1,axs1=pl.subplots(1,figsize=(3,6), dpi=150, facecolor="white")
    fig2,axs2=pl.subplots(1,figsize=(3,6), dpi=150, facecolor="white")
    print("############",dataobj['data'].shape,dataobj['datar'].shape,int(dataobj['CM3']-dataobj['CM'+LonSys]))
    axs1.imshow(dataobj['data'])
    axs2.imshow(dataobj['datar'])
    """
    return dataobj


def read_fits_map_Tiktin(obskey="20251016UTa",imagetype="Map",Level="L3",
                        target="Jupiter",LonSys='3',FiveMicron=False,
                        LimbCorrection=False):

    import sys
    import os
    drive='c:'
    sys.path.append(drive+'/Astronomy/Python Play')
    sys.path.append(drive+'/Astronomy/Python Play/Util_P3')
    sys.path.append(drive+'/Astronomy/Python Play/SpectroPhotometry/Spectroscopy')
    sys.path.append('./Services')
    sys.path.append('C:/Astronomy/Projects/SAS 2021 Ammonia/Jupiter_NH3_Analysis_P3/Maps')
    sys.path.append('C:/Astronomy/Projects/SAS 2021 Ammonia/Jupiter_NH3_Analysis_P3/Services')

    sys.path.append('./Services')
    import numpy as np

    pathin="C:/Astronomy/Projects/SAS 2021 Ammonia/Data-Management-and-Access/Test_Data/"
    pathSci=pathin+"New_Results/"+obskey[:-1]+"/"+obskey+"/"+Level+'/'
    filesSci=os.listdir(pathSci)
    print(filesSci)
    pathIGB=pathin+'New_Results/'+obskey[:-1]+'/'+obskey+'/L1/'
    filesIGB=os.listdir(pathIGB)
    print(filesIGB)
    
    PCldfile=[item for item in filesSci if 'PCld' in item][0]
    PCldobj=read_fits_helper(pathSci+PCldfile,target="Jupiter",
                                  LonSys=LonSys,LimbCorrection=LimbCorrection)
 
    fNH3file=[item for item in filesSci if 'fNH3' in item][0]
    fNH3obj=read_fits_helper(pathSci+fNH3file,target="Jupiter",
                                  LonSys=LonSys,LimbCorrection=LimbCorrection)
    
    NIRfile=[item for item in filesIGB if 'NIR' in item][0]
    NIRobj=read_fits_helper(pathIGB+NIRfile,target="Jupiter",
                                  LonSys=LonSys,LimbCorrection=LimbCorrection)
    
    GRNfile=[item for item in filesIGB if 'GRN' in item][0]
    GRNobj=read_fits_helper(pathIGB+GRNfile,target="Jupiter",
                                  LonSys=LonSys,LimbCorrection=LimbCorrection)
    
    BLUfile=[item for item in filesIGB if 'BLU' in item][0]
    BLUobj=read_fits_helper(pathIGB+BLUfile,target="Jupiter",
                                  LonSys=LonSys,LimbCorrection=LimbCorrection)

    IGBdatar=np.dstack((NIRobj['datar'],GRNobj['datar'],BLUobj['datar']))
    IGBdatarx=np.nan_to_num(IGBdatar, nan=0.0, posinf=1.0, neginf=0.0)


    return(PCldobj['hdr'],PCldobj['datar'],PCldobj['CM'+LonSys],
           fNH3obj['hdr'],fNH3obj['datar'],fNH3obj['CM'+LonSys],
           IGBdatarx/np.max(IGBdatarx),GRNobj['CM'+LonSys],GRNobj['hdr']['DATE-OBS'])

    """
    if FiveMicron==False or FiveMicron=="png":
        print(PClouddatar.shape)
        return(PCloudhdr,PClouddatar,
               fNH3hdr,fNH3datar,
               fNH3szar,fNH3ezar,
               RGB,RGBCM,RGBtime)
    elif FiveMicron=="fits":
        return(PCloudhdr,PClouddatar,
               fNH3hdr,fNH3datar,
               fNH3szar,fNH3ezar,
               RGB,RGBCM,RGBtime,
               micronhdr,microndatar)
    """
