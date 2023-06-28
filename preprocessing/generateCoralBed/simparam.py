import math
#
# Setup simulation parameters
#
fldsize = 1.1           # Size of each 3D array [GB]
wclkperdt = 2.5         # Wall clock time per iteration [s]
dt = 5e-3	            # Time step size [s]
Tw = 5		            # Wave Period [s]
Nwaves = 40	            # Number of wave period
nsaves = 20	            # Number of saves per wave period
#
# Compute requried setup
#
treal = Tw*Nwaves	                        # Total simulation time [s]
nsteps = treal/dt                           # Total number of time steps
tsavetime = Tw/nsaves                       # Simulation data saved every __ [s]
nitersave = math.floor(tsavetime/dt)        # Simulations are saved every __ iterations
ntotiters = math.floor(treal/dt)            # Total simulation iterations
simwallt_sec = ntotiters*wclkperdt          # Total simulation wall clock time [s]
totsnaps = ntotiters/nitersave              # Number of snapshots for 3D fields
totfldsize = totsnaps*fldsize               # Total size of each 3D array
#
# Print info to screen
#
print("------------------------------------------------------------------")
print("Total Simulation Time: %f seconds"%(treal))
print("Results saved every %f seconds"%(tsavetime))
print("- - - - - -")
print("Simulation will have %d snapshots of 3D data"%(totsnaps))
print("Estimated storage %f GB per field"%(totfldsize))
print("Nsaves: %d"%(nitersave))
print("Niters: %d"%(ntotiters))
print("Simulation wall lock time: %f hours .or. %f days"%(simwallt_sec/3600,(simwallt_sec/3600)/24))
print("             - - - - - *** - - - - - - *** - - - - - -")
print("Accounting for 10 percent I/O cost gives: %f hours .or. %f days"%(1.1*(simwallt_sec/3600),1.1*((simwallt_sec/3600)/24)))
print("------------------------------------------------------------------")
