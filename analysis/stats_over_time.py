# Import all the required libraries
import numpy as np
import matplotlib.pyplot as plt
from functions import readinput, fixPlot
# User input param
saveFIG = 0			# Save figure prompt
Ub = 0.012125			# Wave orbital velocity in m/s
kappa = 0.41			# von Karman constant
kvisc = 1e-6			# Kinematic viscosity of the fluid in m^2/s
# Read the input file for basic data input
[fileloc, maskloc, Nx, Ny, Nz, sind, eind, interval, Tw, dt, nphases, isWallRough] = readinput()
# Load all results data
y = np.loadtxt('<location>/y.dat')     			# Ny   (129)
ym = np.loadtxt('<location>/ym.dat')   			# Ny-1 (128)
tke = np.loadtxt('<location>/tke.dat') 			# Ny   (129)
epsilon = np.loadtxt('<location>/epsilon.dat') 		# Ny   (129)
U = np.loadtxt('<location>/Uplan.dat')   		# Ny+1 (130)
uv = np.loadtxt('<location>/uv.dat') 			# Ny+1 (130)
# Average over y to get bulk statistics
tkeavg = np.average(tke[1:,:],axis=0,weights=np.gradient(ym))/(sum(np.gradient(ym)))
epsilonavg = np.average(epsilon[1:,:],axis=0,weights=np.gradient(ym))/(sum(np.gradient(ym)))
Uavg = np.average(U[1:,:],axis=0,weights=np.gradient(y))/(sum(np.gradient(ym)))
uvavg = np.average(uv[1:-1,:],axis=0,weights=np.gradient(ym))/(sum(np.gradient(ym)))
# Setup preliminary parameters
dsize = np.shape(uvavg)
nwaves = dsize[0]/nphases
t = np.linspace(0,Tw*nwaves,dsize[0])/Tw
# Estimate the maximum u* using u'v' peak value
utau = np.sqrt(np.max(abs(uvavg)))
print("Using u* = %f m/s. . ."%(utau))
# Plot all data
figx, figy = 4, 1
plt.figure(1,figsize=(10,10))
fixPlot(thickness=2.0,fontsize=20,texuse=True,labelsize=25)
plt.subplot(figx,figy,1)
plt.plot(t,Uavg/Ub,'m')
plt.ylabel(r'$\langle U_1 \rangle_v^+$',labelpad=10)
plt.grid()
plt.ylim([-10,10])
plt.subplot(figx,figy,2)
plt.plot(t,tkeavg/utau**2,'r')
plt.ylabel(r'${\langle u_i^{\prime} u_i^{\prime}\rangle_v}^+/2$',labelpad=15)
plt.grid()
plt.ylim([1,8])
plt.subplot(figx,figy,3)
plt.plot(t,epsilonavg/(utau**4/(kappa*kvisc)),'b')
plt.ylabel(r'$\nu \langle \partial_j u_i^{\prime} \partial_j u_i^{\prime} \rangle_v^+$',labelpad=10)
plt.grid()
plt.ylim([0,0.15])
plt.subplot(figx,figy,4)
plt.plot(t,uvavg/utau**2,'y')
plt.ylabel(r'$\langle u_{1}^{\prime} u_{3}^{\prime} \rangle_v^+$',labelpad=10)
plt.xlabel(r'$t/T_w$',labelpad=10)
plt.grid()
plt.ylim([-1,1])
if(saveFIG):
    plt.savefig('figure3.eps',format='eps',bbox_inches='tight')
plt.show()
