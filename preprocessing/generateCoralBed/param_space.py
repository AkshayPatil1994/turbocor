#
# Import the required libraries
#
import numpy as np
import matplotlib.pyplot as plt
import cmocean
from functions import *
#
# User input data
#
Rew = [351,3990]                        # Wave Reynolds number
Aks = [1,10]                            # Relative Roughness
Tw = [5.0,15.0]                          # Wave period is seconds 
nu = 1e-6                               # Kinematic Vicosity
#
# ComputeIt might be that parallelisation  some preliminary parameters
#
omega = 2*np.pi*pow(np.array(Tw),-1)   # Calculate wave frequency
Ub = []                                 # Create wave velocity list
ks = []                                 # Create roughness height list
#
# Loop over all combinations to get the parameters
#
print("-------------------------------------------------------------------------------------------")
iter = 1
for aind in range(0,len(Aks),1):
    for rind in range(0,len(Rew),1):
        for tind in range(0,len(Tw),1):
            Ubr = np.sqrt(Rew[rind]*omega[tind]*nu)  # Compute the wave Reynolds number
            ksr = Ubr/(omega[tind]*Aks[aind])        # Compute the roughness height
            # Verify the estimate
            Recomp = Ubr**2/(omega[tind]*nu)
            Akscomp = (Ubr/omega[tind])/ksr
            Twcomp = 2*np.pi/omega[tind]
            # Append results to the list
            ks.append(ksr)
            Ub.append(Ubr)
            # Print values to screen
            print("Case %d -- Rew: %d | Aks: %d | Ub: %f | Tw: %d | ks: %f"%(iter,Recomp,Akscomp,Ubr,Twcomp,ksr))
            iter += 1
print("-------------------------------------------------------------------------------------------")
#
# Plot in phase space
#
fixPlot(thickness=2.0, fontsize=15, markersize=10, labelsize=30, texuse=False)
plt.figure(1,figsize=(10,10))
for pind in range(0,len(Rew),1):
    for p2ind in range(0,len(Aks),1):
        plt.loglog(Rew[pind],Aks[p2ind],'o',markerfacecolor='None',label=r'T_w = '+str(Tw[pind])+' s')
for pind in range(0,len(Rew),1):
    for p2ind in range(0,len(Aks),1):
        plt.loglog(Rew[pind],Aks[p2ind],'*')        
plt.loglog([351.0,351.0],[0.177,0.225],'*')
# Plot formatting
plt.loglog([19,1e5],[0.1,6e1],'k',linewidth=1.4)        
plt.loglog([10,1.9e4],[0.42,1e2],'k',linewidth=1.4)
plt.axis('square')
plt.ylim([1e-1,1e2])
plt.xlim([1e1,1e5])
plt.xlabel(r'$Re_w$',fontsize=40)
plt.ylabel(r'$A/k_s$',fontsize=40)
plt.legend()
plt.grid()
plt.show()
