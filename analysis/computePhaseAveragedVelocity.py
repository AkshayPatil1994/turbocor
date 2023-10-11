import numpy as np
from functions import welcomemessage, gracefulexit, readField, readmask, readinput, maskdata, \
                      write2File                      
import os
import time
import datetime
# Save data prompt
savedata = 1 
#
# Read input parameters
#
stime = time.time()
welcomemessage()
[fileloc, maskloc, Nx, Ny, Nz, sind, eind, interval, Tw, dt, nphases, isWallRough] = readinput()
# Check if results folder exists
if(os.path.exists('data')):
    print("`data` folder exists. . .")
else:
    print("Creating `data` to write files. . .")
    os.makedirs('data')
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
iterind, giterind, mywave = 0, 0, 0                 # Iteration placeholder
Uphase = np.zeros([nusize[0],nusize[1],nusize[2],nphases])
Vphase = np.zeros([nvsize[0],nvsize[1],nvsize[2],nphases])
Wphase = np.zeros([nwsize[0],nwsize[1],nwsize[2],nphases])
Pphase = np.zeros([npsize[0],npsize[1],npsize[2],nphases])
# Loop over all files and analyse
print("Total number of waves: %d waves"%(nwaves))
print("Starting analysis loop at %s with %d files. . ."%(datetime.datetime.now(),datasize))
print("- - - - - - - - - - - - - -")
# First compute the phase average
for fileInd in findices:
    sitime = time.time()
    if(mywave == 20):
        mywave = 0
    # Set the name of the file    
    filename = str(str(fileloc)+'.'+str(fileInd))
    [_,_,_,_,_,_,U,V,W,P] = readField(filename)
    # Mask the data
    U = maskdata(U,Umask)
    V = maskdata(V,Vmask)
    W = maskdata(W,Wmask)
    P = maskdata(P,Pmask)
    # Compute phase average
    Uphase[:,:,:,mywave] += U
    Vphase[:,:,:,mywave] += V
    Wphase[:,:,:,mywave] += W
    Pphase[:,:,:,mywave] += P
    # Screen dump at the end of load cycle
    iterind += 1; giterind += 1
    mywave += 1
    eitime = time.time()
    print("Wave Phase %d | Data for channel_test.%d | Took %f s | File %d/%d. . ."%(mywave,fileInd,eitime-sitime,giterind,datasize))
# Write files to data
if(savedata):
    print("- - - - - - - - - - - - - -")
    print("Writing all phase data to binary files.....")
    for myphase in range(0,nphases):
        time1 = time.time()        
        write2File(Uphase[:,:,:,myphase]/nwaves - np.nanmean(Uphase,axis=3),str('data/Uphase_'+str(myphase+1)+'.bin'))
        write2File(Vphase[:,:,:,myphase]/nwaves - np.nanmean(Vphase,axis=3),str('data/Vphase_'+str(myphase+1)+'.bin'))
        write2File(Wphase[:,:,:,myphase]/nwaves - np.nanmean(Wphase,axis=3),str('data/Wphase_'+str(myphase+1)+'.bin'))
        write2File(Pphase[:,:,:,myphase]/nwaves - np.nanmean(Pphase,axis=3),str('data/Pphase_'+str(myphase+1)+'.bin'))
        time2 = time.time()
        print("Finished write2File for wavephase %d in %f seconds...."%(myphase,time2-time1))
# Exit message
etime=time.time()
gracefulexit(stime,etime)