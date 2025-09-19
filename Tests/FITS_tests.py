# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 13:33:17 2025

@author: smhil
"""

from astropy.io import fits
import os
import matplotlib.pyplot as pl
import numpy as np


pthnew="C:/Astronomy/Projects/SAS 2021 Ammonia/Data-Management-and-Access/FITS/20250116UTa/"
pthref="C:/Astronomy/Projects/SAS 2021 Ammonia/Data-Management-and-Access/Data_Samples/L2 FITS/"

files={'NH3':{'new':'2025-01-16-0043_1-Jupiter_Map_L2TNH3.fits',
              'ref':'2025-01-16-0038_7-Jupiter_Map_L2TNH3.fits'},
       'CH4':{'new':'2025-01-16-0043_1-Jupiter_Map_L2TCH4.fits',
                     'ref':'2025-01-16-0038_0-Jupiter_Map_L2TCH4.fits'}}

for molecule in files:
    print(molecule)
    
    filename=pthnew+files[molecule]["new"]
    hdulist=fits.open(filename)
    hdulist.info()
    hdr=hdulist[0].header
    datanewNH3=hdulist[0].data
    #fNH3sza=fNH3hdulist[1].data
    #fNH3eza=fNH3hdulist[2].data
    hdulist.close()
    
    fig1,axs1=pl.subplots(3,1,figsize=(4.0,6.0), dpi=150, facecolor="white",sharex=True)
    
    show0=axs1[0].imshow(datanewNH3[0,:,:],'gray',origin="lower",vmin=0.85,vmax=1.05)
    pl.colorbar(show0, 
                   orientation='vertical',cmap='gray',
                   ax=axs1[0],fraction=0.046, pad=0.04)
    
    
    filename=pthref+files[molecule]["ref"]
    hdulist=fits.open(filename)
    hdulist.info()
    hdr=hdulist[0].header
    dataref=hdulist[0].data
    #fNH3sza=fNH3hdulist[1].data
    #fNH3eza=fNH3hdulist[2].data
    hdulist.close()
    
    show1=axs1[1].imshow(dataref,'gray',vmin=0.85,vmax=1.05)
    pl.colorbar(show1, 
                   orientation='vertical',cmap='gray',
                   ax=axs1[1],fraction=0.046, pad=0.04)
    show2=axs1[2].imshow(np.flip(datanewNH3[0,:,:],axis=0)/dataref,'coolwarm',vmin=0.9,vmax=1.1)
    pl.colorbar(show2, 
                   orientation='vertical',cmap='coolwarm',
                   ax=axs1[2],fraction=0.046, pad=0.04)


