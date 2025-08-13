from astropy.io import fits
import matplotlib.pyplot as pl

# (1) Level 3 FITS image file example. One data array. Show data image and header metadata

L3FITSpath='./Data_Samples/L3 FITS/'

PCloudhdulist=fits.open(L3FITSpath+'2025-01-16-0038_0-Jupiter_Img_L3PCld_S0.fits')
PCloudhdulist.info()
PCloudhdr=PCloudhdulist[0].header
PClouddata=PCloudhdulist[0].data     #Image
PCloudhdulist.close()

fig1,axs1=pl.subplots(1,1,figsize=(6,6), dpi=150, facecolor="white")

axs1.imshow(PClouddata)

print(PCloudhdr.keys)

# (2) Level 3 FITS map file example. Two data arrays. Show data maps and header metadata
L3FITSpath='./Data_Samples/L3 FITS/'

PCloudhdulist=fits.open(L3FITSpath+'2025-01-16-0038_0-Jupiter_Map_L3PCld_S0.fits')
PCloudhdulist.info()
PCloudhdr=PCloudhdulist[0].header
PClouddata=PCloudhdulist[0].data      #Map
PClouddata1=PCloudhdulist[1].data     #Incidence angle
PCloudhdulist.close()

fig2a,axs2a=pl.subplots(1,1,figsize=(6,6), dpi=150, facecolor="white")
axs2a.imshow(PClouddata)

fig2b,axs2b=pl.subplots(1,1,figsize=(6,6), dpi=150, facecolor="white")
axs2b.imshow(PClouddata1)

print(PCloudhdr.keys)

# (3) PlanetMapper Image
PMpath='./'

PMImghdulist=fits.open(PMpath+'2025-01-16-0055_1-Jupiter_450BLU-FlatStack600_WV3x20-Aligned.fits')
PMImghdulist.info()
PMImghdr=PMImghdulist[0].header
PMImgdata=PMImghdulist[0].data      #Image
PMImgdata1=PMImghdulist[1].data     #Incidence angle
PMImghdulist.close()

fig3a,axs3a=pl.subplots(1,1,figsize=(6,6), dpi=150, facecolor="white")
axs3a.imshow(PMImgdata[0,:,:])

fig3b,axs3b=pl.subplots(1,1,figsize=(6,6), dpi=150, facecolor="white")
axs3b.imshow(PMImgdata1)

print(PMImghdr.keys)

# (4) New FITS File with updated header
from astropy.io import fits

hdu = fits.PrimaryHDU(PMImgdata)
secondarray=fits.ImageHDU(PMImgdata1)
hdul = fits.HDUList([hdu,secondarray])


hdul[0].header=PMImghdr
    
hdul[0].header['NEW']='A NEW keyword'

print()
print(hdul[0].header)
  
fnout='New.FITS'

hdul.writeto(PMpath+fnout,overwrite=True)
hdul.close()

# View primary, extension arrays and header with QFitsView



