import numpy as np
import matplotlib.pyplot as plt
from functions import readinput, fixPlot, fixDataOrder
# User input param
saveIMG = 0
kappa = 0.41
kvisc = 1e-6
[fileloc, maskloc, Nx, Ny, Nz, sind, eind, interval, Tw, dt, nphases, isWallRough] =readinput()
# Load all data
y = np.loadtxt('data/y.dat')     # 129
ym = np.loadtxt('data/ym.dat')   # 128
tke = np.loadtxt('data/tke_timeseries.dat') # 129
epsilon = np.loadtxt('data/epsilon_timeseries.dat') # 129
U = np.loadtxt('data/Uplan_timeseries.dat')   # 130 
urms = np.loadtxt('data/urms_timeseries.dat') # 130
vrms = np.loadtxt('data/vrms_timeseries.dat') # 129
wrms = np.loadtxt('data/wrms_timeseries.dat') # 130
uv = np.loadtxt('data/uv_timeseries.dat') # 130
# Compute the length of the dataset
datasize = np.shape(tke)
print(datasize)
nwaves = int(datasize[1]/nphases)
# Fix the data organisation [due to analysis per phase vs. data write]
tke = fixDataOrder(tke,nphases,nwaves)
epsilon = fixDataOrder(epsilon,nphases,nwaves)
U = fixDataOrder(U,nphases,nwaves)
urms = fixDataOrder(urms,nphases,nwaves)
vrms = fixDataOrder(vrms,nphases,nwaves)
wrms = fixDataOrder(wrms,nphases,nwaves)
uv = fixDataOrder(uv,nphases,nwaves)
# Integrate over y to get bulk statistics
print('Channel height is:',(sum(np.gradient(y))),' m')
tkeavg = np.average(tke[1:,:],axis=0,weights=np.gradient(ym))/(sum(np.gradient(ym)))
epsilonavg = np.average(epsilon[1:,:],axis=0,weights=np.gradient(ym))/(sum(np.gradient(ym)))
Uavg = np.average(U[1:,:],axis=0,weights=np.gradient(y))/(sum(np.gradient(y)))
urmsavg = np.average(urms[1:,:],axis=0,weights=np.gradient(y))/(sum(np.gradient(y)))
vrmsavg = np.average(vrms[1:,:],axis=0,weights=np.gradient(ym))/(sum(np.gradient(ym)))
wrmsavg = np.average(wrms[1:-1,:],axis=0,weights=np.gradient(ym))/(sum(np.gradient(ym)))
uvavg = np.average(uv[0:-1,:],axis=0,weights=np.gradient(ym))/(sum(np.gradient(ym)))
# Setup preliminary parameters
dsize = np.shape(uvavg)
nwaves = dsize[0]/nphases
t = np.linspace(0,Tw*nwaves,dsize[0])/Tw
# Estimate the maximum u* using u'v' peak value
utau = np.sqrt(np.max(-uv))
print("Using u* = %f m/s. . ."%(utau))
# Subplot labels
subplot_labels = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)']
# Plot all data
figx, figy = 3, 2
plt.figure(1,figsize=(12.5,8.6))
fixPlot(thickness=2.0,fontsize=20,texuse=True)
plt.subplot(figx,figy,1)
plt.plot(t,tkeavg/utau**2,'r')
plt.ylabel(r'$k^+ = \frac{\langle u_i^{\prime} u_i^{\prime}\rangle_v^+}{2}$')
plt.grid()
plt.subplot(figx,figy,2)
plt.plot(t,epsilonavg/(utau**4/(kappa*kvisc)),'b')
plt.ylabel(r'$\epsilon^+ = \frac{\nu}{2} \langle \partial_j u_i^{\prime} \partial_j u_i^{\prime} \rangle_v^+$')
plt.grid()
plt.subplot(figx,figy,3)
plt.plot(t,urmsavg/utau,'k')
plt.ylabel(r'$\langle u_{1,rms}^{\prime} \rangle_v^+$')
plt.grid()
plt.subplot(figx,figy,4)
plt.plot(t,vrmsavg/utau,'g')
plt.ylabel(r'$\langle u_{3,rms}^{\prime} \rangle_v^+$')
plt.grid()
plt.subplot(figx,figy,5)
plt.plot(t,wrmsavg/utau,'m')
plt.ylabel(r'$\langle u_{2,rms}^{\prime} \rangle_v^+$')
plt.xlabel(r'$t/T_w$')
plt.grid()
plt.subplot(figx,figy,6)
plt.plot(t,uvavg/utau**2,'y')
plt.ylabel(r'$\langle u_{1}^{\prime} u_{3}^{\prime} \rangle_v^+$')
plt.xlabel(r'$t/T_w$')
plt.yticks([-1,0,1])
plt.tight_layout(); plt.grid()
# Adding subplot labels
for i in range(figx * figy):
    plt.subplot(figx,figy,i+1)
    plt.annotate(subplot_labels[i], xy=(-0.2, 0.92), xycoords='axes fraction', fontsize=20, fontweight='bold')
if(saveIMG):
    plt.savefig('figure3.eps',format='eps',bbox_inches='tight')
plt.show()