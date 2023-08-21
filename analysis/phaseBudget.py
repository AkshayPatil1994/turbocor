import numpy as np
from functions import welcomemessage, gracefulexit, readField, readmask, readinput, maskdata, \
                      interpolate_x, interpolate_y, interpolate_z, allgradient, tkedissipation                      
import os
import time
import datetime
# Save data prompt
savedata = 1
# Kinematic viscosity used to compute dissipation
kviscosity = 1e-6   
#
# Read input parameters
#
stime = time.time()
welcomemessage()
[fileloc, maskloc, Nx, Ny, Nz, sind, eind, interval, Tw, dt, nphases, isWallRough] = readinput()
# Setup preliminary and auxiliary data
findices = np.arange(sind,eind+interval,interval)
datasize = len(findices)
nwaves = datasize/nphases
# Define the global array sizes
nusize = [Nx,Ny+1,Nz+1]
nvsize = [Nx+1,Ny,Nz+1]
nwsize = [Nx+1,Ny+1,Nz]
npsize = [Nx+1,Ny+1,Nz+1]
# Read masking files
smtime = time.time()
maskin = maskloc+'Umask_in'
Umask = readmask(maskin,nusize)
maskin = maskloc+'Vmask_in'
Vmask = readmask(maskin,nvsize)
maskin = maskloc+'Wmask_in'
Wmask = readmask(maskin,nwsize)
maskin = maskloc+'Pmask_in'
Pmask = readmask(maskin,npsize)
emtime = time.time()
print("All masks read in %f seconds. . ."%(emtime-smtime))
# Initialise all result arrays
iterind = 0                 # Iteration placeholder
Uphase = np.zeros(nusize)
Vphase = np.zeros(nvsize)
Wphase = np.zeros(nwsize)
Pphase = np.zeros(npsize)
# Loop over all files and analyse
print("Total number of waves: %d waves"%(nwaves))
print("Starting analysis loop at %s with %d files. . ."%(datetime.datetime.now(),len(findices)))
print("- - - - - - - - - - - - - -")
for myphase in range(0,nphases):
    # Setup the right phase file to be loaded
    if(myphase == nphases-1):
        phases = np.arange(sind,eind+interval,interval*nphases)
    else:
        phases = np.arange(sind,eind,interval*nphases)
    # First compute the phase average
    print("Computing statistics for phase %d. . ."%(myphase+1))
    for fileInd in phases:
        filename = str(str(fileloc)+'.'+str(fileInd))
        [xf,yf,zf,xm,ym,zm,U,V,W,P] = readField(filename)
        # Mask the data
        U = maskdata(U,Umask)
        V = maskdata(V,Vmask)
        W = maskdata(W,Wmask)
        P = maskdata(P,Pmask)
        # Compute phase average
        Uphase += U
        Vphase += V
        Wphase += W
        Pphase += P

    
    # Increment the starting index and reset all arrays
    sind += interval
    Uphase.fill(0); Vphase.fill(0); Wphase.fill(0); Pphase.fill(0)
    

