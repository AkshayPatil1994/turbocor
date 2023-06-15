# TURCOR

This repository stores all the pre-processing and post-processing code used in the SURFsara funded project titled `Unraveling the Turbulence Dynamics: Investigating Wave-Induced Turbulence over Corals [EINF-6125]` or in short `TURCOR`.

## Requirements
To enable swift error-free runtime environments, you can create a python environment and install the required libraries as shown below.
```  
python -m venv <location to virtual environment>
source <location to virtual environment>/bin/activate
pip install -r requirements.txt
```

## Directory Layout

- `analysis`: Contains all the post-processing code used to obtain the results
- `preprocessing`: Contains all the routines to generate the stochastic coral bed and the signed-distance-field [SDF] used to generate the masking function within the code.  
    - `generateCoralBed`: Python routines to generate the stochastic coral bed
    - `generateSDF`: Python routines to generate the SDF and convert the numpy arrays to `dopamine*` compatible binary files

<hr>

The coral geometries are openly available from the `Smithsonian archive` at [3D Digitisation] , and we would like to thank Smithsonian - 3D Digitisation for making these coral geometries freely available for public use.

<hr>

`*The code for dopamine was graciously shared by Prof. Adrian Lozano-Duran, and we would like to acknowledge the support and insights provided by Prof. Lozano-Duran.`


[3D Digitisation]:https://3d.si.edu/corals