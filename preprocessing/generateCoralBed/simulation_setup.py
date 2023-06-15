#
# Simulation Parameters
#
import numpy as np
import matplotlib.pyplot as plt
#
# User Input Data
#
dfac = [40,60,40]   # Domain Factors
Tw = 5.0            # Wave period [s]
Ub = 0.021          # Wave Orbital Velocity [m/s]
kv = 1e-6           # Kinematic Viscosity [m^2/s]
ks = 0.017          # Height of the roughness [m]
#
# Compute requisite parameters
#   
delta = np.sqrt((2*kv)/(2*np.pi/Tw))
Lx = dfac[0]*delta 
Ly = dfac[1]*delta
Lz = dfac[2]*delta  
#
# Print info to screen
#
print("The Stokes [laminar] boundary layer thickenss is %f m"%(delta))   
print("Minimum Domain: %f x %f x %f [m]"%(Lx,Ly,Lz)) 