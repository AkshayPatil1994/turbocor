#
# Python routines to translate stl
#
# Load the library
from functions import trasRot       
import numpy as np
import trimesh
import time
#
# File I/O
#
saveMesh = True                                             # Save mesh flag
scale = 1.0                                                 # Scale mesh 
rotAx = [1, 0, 0]                                           # Which rotation axis to rotate about?
rotAngle = 0                                                # Rotation angle in degrees
translation = [0.014,-0.001526,0.008]                             # Translation array
inFile = 'assets/coralbed_wrapped.obj'                      # Input file + location
outFile = 'assets/coralbed_ztrans.obj'                      # Output file + location
#
# Create the first coral with the right scaling
#
mesh = trimesh.load_mesh(inFile)
trasRot(saveMesh,mesh,outFile,translation,rotAngle,rotAx,scale,verbose=True)