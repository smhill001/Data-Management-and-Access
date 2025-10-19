import numpy as np
import gravity as g
#set constants and set gravity as a function of latitude (Jupiter is so oblate that gravity
#  varies significantly from the equator to the poles. 

amagat = 2.69e24 #Lodschmits number. (cm-2) This is really km-amagat - an arcane atmospheric science unit
mean_mol_wt = 3.85e-24 #gm/molecule, which is 2.22 gm/mole
fCH4 = 2.04e-3 #mole fraction of ammonia (old value from Galileo was 1.81e-3)
STP = 1.01e6  #dyne/cm^2 [(g-cm/s^2)/cm^2]`- standard pressure for one atmosphere
gravity = g.gravity() #see file dropped in processes
K_eff_CH4620 = 0.427
K_eff_NH3647 = 2.955

def computeCloudPressure(CH4data, NH3data):
    #compute ammonia optical depth according to Beer-Lambert law
    CH4_tau = -np.log(CH4data)
    NH3_tau = -np.log(NH3data) 

    #compute column abundance of molecules along the line-of-sight where 1000 corrects for units
    #  and K_eff are the effective absorption cross sections of each molecule, 0.427 and 2.955 for 
    #  methane and ammonia respectively
    CH4_Ncol = 1000*CH4_tau/K_eff_CH4620 

    #compute cloud pressure - CH4_Cloud_Press is computed in units of mb
    CH4_Cloud_Press = CH4_Ncol*amagat*gravity*mean_mol_wt/(fCH4*STP)
   
    return CH4_Cloud_Press
        
def computeAmmoniaMoleFraction(CH4data, NH3data):
    #compute ammonia optical depth according to Beer-Lambert law
    CH4_tau = -np.log(CH4data)
    NH3_tau = -np.log(NH3data) 
  

    #compute column abundance of molecules along the line-of-sight where 1000 corrects for units
    #  and K_eff are the effective absorption cross sections of each molecule, 0.427 and 2.955 for 
    #  methane and ammonia respectively
    CH4_Ncol = 1000*CH4_tau/K_eff_CH4620 
    NH3_Ncol = 1000*NH3_tau/K_eff_NH3647
    fNH3=fCH4*NH3_Ncol/CH4_Ncol
    print(fNH3)
    return fNH3

#compute ammonia mole fraction - ratio of column densities multiplied by methane mole fraction
