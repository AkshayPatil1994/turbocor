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
Uplan = np.zeros([nusize[1],len(findices)])
uvplan = np.zeros([nusize[1],len(findices)])
urms = np.zeros([nusize[1],len(findices)])
vrms = np.zeros([nvsize[1],len(findices)])
wrms = np.zeros([nwsize[1],len(findices)])
tke = np.zeros([Ny,len(findices)])
epsilon = np.zeros([Ny,len(findices)])
uprime = np.zeros(nusize)
# Loop over all files and analyse
print("Starting analysis loop at %s with %d files. . ."%(datetime.datetime.now(),len(findices)))
for iter in findices:
    sitime = time.time()
    filename = str(str(fileloc)+'.'+str(iter))
    [xf,yf,zf,xm,ym,zm,U,V,W,P] = readField(filename)
    # Mask the data
    U = maskdata(U,Umask)
    V = maskdata(V,Vmask)
    W = maskdata(W,Wmask)
    P = maskdata(P,Pmask)
    # Compute Statistics
    Uplan[:,iterind] = np.nanmean(U,axis=(0,2))
    dummy0 = Uplan[:,iterind]
    uprime = U[:,:,:] - dummy0[np.newaxis,:,np.newaxis] 
    # Interpolate U, V, and W to cell centers
    dummy1 = interpolate_x(uprime)
    dummy2 = interpolate_y(V)
    dummy3 = interpolate_z(W)
    # Compute required quantities
    uvplan[0:-1,iterind] = np.nanmean(dummy1[:,0:-1,:]*dummy2[0:-1,:,:],axis=(0,2))
    urms[:,iterind] = np.sqrt(np.nanmean(uprime**2,axis=(0,2)))
    vrms[:,iterind] = np.sqrt(np.nanmean(dummy2**2,axis=(0,2)))
    wrms[:,iterind] = np.sqrt(np.nanmean(dummy3**2,axis=(0,2)))
    tke[:,iterind] = np.nanmean(0.5*(dummy1[0:Nx,0:Ny,0:Nz]**2 + \
                                     dummy2[0:Nx,0:Ny,0:Nz]**2 + \
                                     dummy3[0:Nx,0:Ny,0:Nz]**2), axis=(0,2))
    # Compute derivatives [cell-centers common locations]
    [dudx, dvdx, dwdx, dudy, dvdy, dwdy, dudz, dvdz, dwdz] = allgradient(dummy1,dummy2,dummy3,xm,ym,zm)
    dummy4 = tkedissipation(kviscosity,dudx[0:Nx,0:Ny,0:Nz],dudy[0:Nx,0:Ny,0:Nz],dudz[0:Nx,0:Ny,0:Nz], \
                             dvdx[0:Nx,0:Ny,0:Nz],dvdy[0:Nx,0:Ny,0:Nz],dvdz[0:Nx,0:Ny,0:Nz], \
                             dwdx[0:Nx,0:Ny,0:Nz],dwdy[0:Nx,0:Ny,0:Nz],dwdz[0:Nx,0:Ny,0:Nz])
    epsilon[:,iterind] = np.nanmean(dummy4,axis=(0,2))
    # Finalise the time step
    iterind += 1
    eitime = time.time()
    print("File %d/%d | channel_test.%d done in %f s. . ."%(iterind,len(findices),iter,eitime-sitime))
# Write data to file
print("- - - - - - - - - - - - - - ")
print("Writing analysis results to file. . .")
if(savedata==1):
    np.savetxt('y.dat',yf)
    np.savetxt('ym.dat',ym)
    np.savetxt('Uplan.dat',Uplan)
    np.savetxt('uv.dat',uvplan)
    np.savetxt('urms.dat',urms)
    np.savetxt('vrms.dat',vrms)
    np.savetxt('wrms.dat',wrms)
    np.savetxt('tke.dat',tke)
    np.savetxt('epsilon.dat',epsilon)
# Exit message
etime=time.time()
gracefulexit(stime,etime)
