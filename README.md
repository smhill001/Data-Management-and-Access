# Jupiter Atmospheric Data Processing

## Overview

This pipeline takes observational filtered image data and outputs multiple levels of processed FITS data files. The top level consists of an RGB color map and maps of ammonia content and cloud top pressure in the atmosphere of Jupiter.

## Getting Started

This project requires planetmapper and spice kernels to be installed
The path to the spice kernels may need to be specified in ProcessL1X using 

```
planetmapper.set_kernel_path()

```


## Data

### Input Data

The input image data is png format. The pipeline expects 7 filter pngs:
    - 450BLU
    - 550GRN
    - 685NIR 
    - 656HIA 
    - 632OI
    - 620CH4 (methane band)
    - 647NH3 (ammonia band)

Each image also has an associated CameraSettings.txt file

Each observation set consists of one of each of the RGB filter(450, 550, 685) for context and two of the scientific filters(656, 632, 620, 647) to account for the rotation of Jupiter during the two-minute observation period. The files should be listed in the order they were taken(450, 550, 685, 656, 632, 620, 647, 647, 620, 632, 656). The pipeline is not robust to a different input order, but will accept missing files. The image names have the prefix YYYY-MM-DD-HHMM_N-Jupiter_, then the filter, then a suffix with the image format/preprocessing. 

### Output Data

For each observation, the pipeline outputs:
  - unprocessed L1: Contains a mapped and unmapped fits file for each image
  - L1
    - RGB: Same as unprocessed L1, since there is only one image for these filters in the   observation
    - Scientific Files: Creates new fits file with incidence, emission, and radiance values averaged
  - L2: 
    - FITS file with normalized brightness from dividing by average radiance, which is calculated from all pixels with an emission angle < 80 (to avoid effects from limb darkening)
    - Methane: Calculates strength of CH4 absorption by dividing CH4 band reflectance by continuoum(estimated from OI map) 
    - NH3: Calculates NH3 absorption by dividing NH3 band reflectance by NH3 continuoum(estimated from HIA and OI maps), accounting for calibration factor
  - L3: 
    - Cloud pressure: computed by finding optical depth of methane, converting into column abundance to find how deep the clouds are
    - ammonia mole fraction:  ratio of column densities multiplied by methane mole fraction


## Usage

Input and output paths can be configured in config.py, input data should be in specified format below

The process can be called on a directory with a name of the format YYYYMMDDUT. The path to the parent directory should be listed in the config.py under the 'input' keyword. The process is run by caling the batch_process function on the directory name. For example:

```
batch_process("20251016UT")
```

A popup will appear in which you should rotate and scale the image of Jupiter to fit the required dimensions before closing it. Once the process runs, a new directory will be created with the same name if one does not already exist in the output directory listed in the config file. This directory will have file structure:

-20251016UT
    - 20251016UTa
        -L1
        -L2
        -L3
        -unprocessed_L1
    - 20251016UTb
        - ... 

With the corresponding data for each observation in each folder. The header and image arrays for these files can be viewed by opening the file in QFITS.view

The batch_process script runs two scripts: process_L1X.py and process_L1Y.py which may be run independently. 


Process_L1X is responsible for converting each input png file into two fits files, one with the suffix map.fits and another with the suff .fits, and populates the unprocessed_L1 folder with these files for each observation. This process runs on a timescale of minutes to hours depending on the number of observations being processed. This process works on one date at a time

Process_L1Y performs transformations and computations on the output of Process_L1X. It works on a single observation at a time. For this observation, it populates the L1, L2, and L3 directories for the given observation. This process should take less than a minute to run.




## Testing

## Applications

The output L3 data is compatible with the L3_Jup_Map_Plot_V2 function in Visualization-and-analysis repository by @smhill001




