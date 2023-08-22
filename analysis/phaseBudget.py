import numpy as np
from functions import welcomemessage, gracefulexit, readField, readmask, readinput, maskdata, \
                      interpolate_x, interpolate_y, interpolate_z, allgradient, tkedissipation, \
                      write2File                      
import os
import time
import datetime
# Save data prompt
savedata = 1
savetimeseries = 1
# Kinematic viscosity used to compute dissipation
kviscosity = 1e-6   
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
Uphase, urms, ut = [np.zeros(nusize) for i in range(3)]
Vphase, vrms, vt = [np.zeros(nvsize) for i in range(3)]
Wphase, wrms, wt = [np.zeros(nwsize) for i in range(3)]
Pphase, prms, pt = [np.zeros(npsize) for i in range(3)]
uv, tke, epsilon = [np.zeros(nusize) for i in range(3)]
# Planform average statistics for time series convergence
uplan_ts, urms_ts = [np.zeros([nusize[1],datasize]) for i in range(2)]
vrms_ts = np.zeros([nvsize[1],datasize])
wrms_ts = np.zeros([nwsize[1],datasize])
prms_ts = np.zeros([npsize[1],datasize])
uv_ts, tke_ts, epsilon_ts = [np.zeros([Ny,datasize]) for i in range(3)]
# Loop over all files and analyse
print("Total number of waves: %d waves"%(nwaves))
print("Starting analysis loop at %s with %d files. . ."%(datetime.datetime.now(),datasize))
print("- - - - - - - - - - - - - -")
for myphase in range(0,nphases):
    # Setup the right phase file to be loaded
    if(myphase == nphases-1):
        phases = np.arange(sind,eind+interval,interval*nphases)
    else:
        phases = np.arange(sind,eind,interval*nphases)
    # First compute the phase average
    for fileInd in phases:
        sitime = time.time()
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
        # Screen dump at the end of load cycle
        iterind += 1; mywave += 1
        eitime = time.time()
        print("Round 1 - Data for channel_test.%d | wave %d/%d for phase %d  | Global file %d/%d | Took %f s. . ."%(fileInd,mywave,nwaves,myphase+1,iterind,datasize,eitime-sitime))
    # Loop again to compute the turbulence statistics
    mywave = 0                  # Reset the wave number
    for fileInd in phases:
        sitime = time.time()
        filename = str(str(fileloc)+'.'+str(fileInd))
        [xf,yf,zf,xm,ym,zm,U,V,W,P] = readField(filename)
        # Mask the data
        U = maskdata(U,Umask)
        V = maskdata(V,Vmask)
        W = maskdata(W,Wmask)
        P = maskdata(P,Pmask)
        # Compute the turbulent rms component (phase averaged!!!)
        urms += (U - Uphase)**2
        vrms += (V - Vphase)**2
        wrms += (W - Wphase)**2
        prms += (P - Pphase)**2
        # Interpolate u', v', and w' to cell centers
        dummy1 = interpolate_x(U - Uphase)
        dummy2 = interpolate_y(V - Vphase)
        dummy3 = interpolate_z(W - Wphase)
        # Compute cross terms (uv and tke)
        uv[0:Nx,0:Ny,0:Nz] += dummy1[0:Nx,0:Ny,0:Nz]*dummy2[0:Nx,0:Ny,0:Nz]
        tke[0:Nx,0:Ny,0:Nz] += 0.5*(dummy1[0:Nx,0:Ny,0:Nz]**2 + \
                    dummy2[0:Nx,0:Ny,0:Nz]**2 + \
                    dummy3[0:Nx,0:Ny,0:Nz]**2)
        # Compute phase averaged dissipation
        # Compute derivatives [cell-centers common locations]
        [dudx, dvdx, dwdx, dudy, dvdy, dwdy, dudz, dvdz, dwdz] = allgradient(dummy1,dummy2,dummy3,xm,ym,zm)
        epsilon[0:Nx,0:Ny,0:Nz] += tkedissipation(kviscosity,dudx[0:Nx,0:Ny,0:Nz],dudy[0:Nx,0:Ny,0:Nz],dudz[0:Nx,0:Ny,0:Nz], \
                                dvdx[0:Nx,0:Ny,0:Nz],dvdy[0:Nx,0:Ny,0:Nz],dvdz[0:Nx,0:Ny,0:Nz], \
                                dwdx[0:Nx,0:Ny,0:Nz],dwdy[0:Nx,0:Ny,0:Nz],dwdz[0:Nx,0:Ny,0:Nz])
        # Planform average to store the stats for time series
        uplan_ts[:,giterind] = np.nanmean(U,axis=(0,2))
        urms_ts[:,giterind] = np.sqrt(np.nanmean((U - Uphase)**2,axis=(0,2)))
        vrms_ts[:,giterind] = np.sqrt(np.nanmean((V - Vphase)**2,axis=(0,2)))
        wrms_ts[:,giterind] = np.sqrt(np.nanmean((W - Wphase)**2,axis=(0,2)))
        prms_ts[:,giterind] = np.sqrt(np.nanmean((P - Pphase)**2,axis=(0,2)))
        uv_ts[0:Ny,giterind] = np.nanmean(dummy1[:,0:-1,:]*dummy2[0:-1,:,:],axis=(0,2))
        tke_ts[0:Ny,giterind] = np.nanmean(0.5*(dummy1[0:Nx,0:Ny,0:Nz]**2 + \
                                     dummy2[0:Nx,0:Ny,0:Nz]**2 + \
                                     dummy3[0:Nx,0:Ny,0:Nz]**2), axis=(0,2))
        epsilon_ts[0:Ny,giterind] = np.nanmean(tkedissipation(kviscosity,dudx[0:Nx,0:Ny,0:Nz],dudy[0:Nx,0:Ny,0:Nz],dudz[0:Nx,0:Ny,0:Nz], \
                                dvdx[0:Nx,0:Ny,0:Nz],dvdy[0:Nx,0:Ny,0:Nz],dvdz[0:Nx,0:Ny,0:Nz], \
                                dwdx[0:Nx,0:Ny,0:Nz],dwdy[0:Nx,0:Ny,0:Nz],dwdz[0:Nx,0:Ny,0:Nz]),axis=(0,2))
        # Increment the wave number
        mywave += 1; giterind += 1
        eitime = time.time()
        print("Round 2 - Data for channel_test.%d | wave %d/%d for phase %d | Took %f s. . ."%(fileInd,mywave,nwaves,myphase+1,eitime-sitime))
    # Write the phase averaged velocity arrays (note averaging is data/nwaves as time-avg == 0)
    if(savedata):
        # Write phase averaged velocity data
        write2File(Uphase/nwaves,str('data/Uphase_'+str(myphase+1)+'.bin'))
        write2File(Vphase/nwaves,str('data/Vphase_'+str(myphase+1)+'.bin'))
        write2File(Wphase/nwaves,str('data/Wphase_'+str(myphase+1)+'.bin'))
        write2File(Pphase/nwaves,str('data/Pphase_'+str(myphase+1)+'.bin'))
        # Write turbulence statistics (rms)
        write2File(np.sqrt(urms/nwaves),str('data/urms_'+str(myphase+1)+'.bin'))
        write2File(np.sqrt(vrms/nwaves),str('data/vrms_'+str(myphase+1)+'.bin'))
        write2File(np.sqrt(wrms/nwaves),str('data/wrms_'+str(myphase+1)+'.bin'))
        write2File(np.sqrt(prms/nwaves),str('data/prms_'+str(myphase+1)+'.bin'))
        # Write the cross terms (uv, tke, epsilon)
        write2File(uv/nwaves,str('data/uv_'+str(myphase+1)+'.bin'))
        write2File(tke/nwaves,str('data/tke_'+str(myphase+1)+'.bin'))
        write2File(epsilon/nwaves,str('data/epsilon_'+str(myphase+1)+'.bin'))
    # Reset and/or increment required arrays
    sind += interval
    mywave = 0                      # Reset the wave counter to 0 at start of the new phase
    # Reset all arrays to zero before the next phase of sequencing
    Uphase.fill(0); Vphase.fill(0); Wphase.fill(0); Pphase.fill(0)
    urms.fill(0); vrms.fill(0); wrms.fill(0); prms.fill(0)
    uv.fill(0); tke.fill(0); epsilon.fill(0)
# Final write time series data
if(savetimeseries==1):
    np.savetxt('data/y.dat',yf)
    np.savetxt('data/ym.dat',ym)
    np.savetxt('data/Uplan_timeseries.dat',uplan_ts)
    np.savetxt('data/uv_timeseries.dat',uv_ts)
    np.savetxt('data/urms_timeseries.dat',urms_ts)
    np.savetxt('data/vrms_timeseries.dat',vrms_ts)
    np.savetxt('data/wrms_timeseries.dat',wrms_ts)
    np.savetxt('data/tke_timeseries.dat',tke_ts)
    np.savetxt('data/epsilon_timeseries.dat',epsilon_ts)
# Exit message
etime=time.time()
gracefulexit(stime,etime)