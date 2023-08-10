import numpy as np
from functions import welcomemessage, gracefulexit, readField, readmask, readinput, maskdata
import os
import time
import datetime
#
# Setup input parameters
#
stime = time.time()
welcomemessage()
[fileloc, maskloc, Nx, Ny, Nz, sind, eind, interval, Tw, dt, nphases, isWallRough] = readinput()
# Setup preliminary and auxiliary data
findices = np.arange(sind,eind,interval)
datasize = len(findices)
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
print("All masks read in %f seconds...."%(emtime-smtime))
# Initialise all result arrays
iterind = 0                 # Iteration placeholder
Uplan = np.zeros([nusize[1],len(findices)])
uprime = np.zeros(nusize)

# Loop over all files and analyse
print("Starting analysis time loop at %s"%(datetime.datetime.now()))
for iter in findices:
    sitime = time.time()
    filename = str(str(fileloc)+'.'+str(iter))
    [xf,yf,zf,xm,ym,zm,U,V,W,P] = readField(filename)
    # Mask the data
    U = maskdata(U,Umask)
    V = maskdata(V,Vmask)
    W = maskdata(W,Wmask)
    P = maskdata(P,Pmask)
    # Compute Planform average
    Uplan[:,iterind] = np.mean(U,axis=(0,2))
    uprime = U - Uplan[np.newaxis,:,iterind,np.newaxis] 
    eitime = time.time()
    print("File channel_test.%d done in %f s . . ."%(iter,eitime-sitime))
# Write data to file
print("Writing analysis results to file. . .")

# Exit message
etime=time.time()
gracefulexit(stime,etime)
    

