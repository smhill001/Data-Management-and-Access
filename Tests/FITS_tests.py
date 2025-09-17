# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 13:33:17 2025

@author: smhil
"""

from astropy.io import fits
import os
import matplotlib.pyplot as pl

pthnew="C:/Astronomy/Projects/SAS 2021 Ammonia/Data-Management-and-Access/FITS/20250116UTa/"
#print(os.listdir("C:/Astronomy/Projects/SAS 2021 Ammonia/Data-Management-and-Access/FITS/20250116UTa"))

filename=pthnew+"2025-01-16-0043_1-Jupiter_Map_L2TCH4.fits"
#filename=pthnew+"2025-01-16-0043_1-Jupiter_Map_L2TNH3.fits"
hdulist=fits.open(filename)
hdulist.info()
hdr=hdulist[0].header
data=hdulist[0].data
#fNH3sza=fNH3hdulist[1].data
#fNH3eza=fNH3hdulist[2].data
hdulist.close()

fig1,axs1=pl.subplots(figsize=(8.0,4.0), dpi=150, facecolor="white")

axs1.imshow(data[0,:,:],'gray',origin="lower")

pthref="C:/Astronomy/Projects/SAS 2021 Ammonia/Data-Management-and-Access/Data_Samples/L2 FITS/"

filename=pthref+"2025-01-16-0038_0-Jupiter_Map_L2TCH4.fits"
#filename=pthref+"2025-01-16-0038_7-Jupiter_Map_L2TNH3.fits"
hdulist=fits.open(filename)
hdulist.info()
hdr=hdulist[0].header
data=hdulist[0].data
#fNH3sza=fNH3hdulist[1].data
#fNH3eza=fNH3hdulist[2].data
hdulist.close()

fig2,axs2=pl.subplots(figsize=(8.0,4.0), dpi=150, facecolor="white")

axs2.imshow(data,'gray')




pthnew="C:/Astronomy/Projects/SAS 2021 Ammonia/Data-Management-and-Access/FITS/20250116UTa/"
#print(os.listdir("C:/Astronomy/Projects/SAS 2021 Ammonia/Data-Management-and-Access/FITS/20250116UTa"))

filename=pthnew+"2025-01-16-0040_1-Jupiter_620CH4-FlatStack600-Alignedmap.fits"
hdulist=fits.open(filename)
hdulist.info()
hdr=hdulist[0].header
data=hdulist[0].data
#fNH3sza=fNH3hdulist[1].data
#fNH3eza=fNH3hdulist[2].data
hdulist.close()

fig3,axs3=pl.subplots(figsize=(8.0,4.0), dpi=150, facecolor="white")

axs3.imshow(data[0,:,:],'gray')

pthref="C:/Astronomy/Projects/SAS 2021 Ammonia/Data-Management-and-Access/Data_Samples/20250116UT/"

filename=pthref+"2025-01-16-0040_1-Jupiter_620CH4-FlatStack600_WV3x20-Aligned.FIT"
hdulist=fits.open(filename)
hdulist.info()
hdr=hdulist[0].header
data=hdulist[0].data
#fNH3sza=fNH3hdulist[1].data
#fNH3eza=fNH3hdulist[2].data
hdulist.close()

fig4,axs4=pl.subplots(figsize=(8.0,4.0), dpi=150, facecolor="white")

axs4.imshow(data[0,:,:],'gray')