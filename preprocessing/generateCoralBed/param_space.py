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
Rew = [351,3990]                         # Wave Reynolds number
Aks = [0.5,1]                            # Relative Roughness
Tw = [5.0,15.0]                          # Wave period is seconds 
nu = 1e-6                                # Kinematic Vicosity
#
# ComputeIt might be that parallelisation  some preliminary parameters
#
omega = 2*np.pi*pow(np.array(Tw),-1)    # Calculate wave frequency
Ub = []                                 # Create wave velocity list
ks = []                                 # Create roughness height list
omega_arr = []                          # Create omega list to plot
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
            omega_arr.append(2*np.pi/Twcomp)
            # Print values to screen
            print("Case %d -- Rew: %d | Aks: %d | Ub: %f | Tw: %d | ks: %f"%(iter,Recomp,Akscomp,Ubr,Twcomp,ksr))
            iter += 1
print("-------------------------------------------------------------------------------------------")
Rek_arr = [351,3990,351,3990,702,7980,702,7980]
Aks_arr = [1,1,1,1,0.5,0.5,0.5,0.5]

gammaRek = np.zeros([len(Rek_arr),1])
for indd in range(0,len(Rek_arr)):
    gammaRek[indd] = Aks_arr[indd]/Rek_arr[indd]

for indd in [0,1,6,7]:
    plt.plot(Aks_arr[indd],gammaRek[indd],'ro',markerfacecolor='None')
for indd in [4,5,2,3]:
    plt.plot(Aks_arr[indd],gammaRek[indd],'k+',markerfacecolor='None')
plt.xlabel(r'$\Gamma$')
plt.ylabel(r'$\Gamma/Re_b^k$')
plt.show()
#
# Plot in phase space
#
# fixPlot(thickness=2.0, fontsize=15, markersize=15, labelsize=30, texuse=False)
# plt.figure(1,figsize=(15,16))
# plt.subplot(1,2,1)
# for pind in range(0,len(Rew),1):
#     for p2ind in range(0,len(Aks),1):
#         plt.loglog(Rew[pind],Aks[p2ind],'ro',markerfacecolor='None',label=r'T_w = '+str(Tw[pind])+' s')
# for pind in range(0,len(Rew),1):
#     for p2ind in range(0,len(Aks),1):
#         plt.loglog(Rew[pind],Aks[p2ind],'k+')        
# #plt.loglog([351.0,351.0],[0.177,0.225],'*')
# # Plot formatting
# plt.loglog([19,1e5],[0.1,6e1],'k',linewidth=1.4)        
# plt.loglog([10,1.9e4],[0.42,1e2],'k',linewidth=1.4)
# plt.axis('square')
# plt.ylim([1e-1,1e2])
# plt.xlim([1e1,1e5])
# plt.xlabel(r'$Re_w \equiv \frac{U_b^2}{\omega \nu}$',fontsize=40)
# plt.ylabel(r'$A/k_s$',fontsize=40)
# plt.grid()
# # plt.tight_layout()
# # Roughness Reynolds number
# plt.subplot(1,2,2)
# for indd in [0,1,4,5]:
#     plt.loglog(Rek_arr[indd],Aks_arr[indd],'ro',markerfacecolor='None')
# for indd in [2,3,6,7]:
#     plt.loglog(Rek_arr[indd],Aks_arr[indd],'k+')
# # Plot formatting
# #plt.loglog([19,1e5],[0.1,6e1],'k',linewidth=1.4)        
# #plt.loglog([10,1.9e4],[0.42,1e2],'k',linewidth=1.4)
# plt.axis('square')
# plt.ylim([1e-1,1e2])
# plt.xlim([1e1,1e5])
# plt.xlabel(r'$Re_k \equiv \frac{U_b k_s}{\nu}$',fontsize=40)
# plt.grid()
# #plt.savefig('figure1.eps',format='eps')
# plt.show()

