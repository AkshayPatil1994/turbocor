#
# Python routines to translate stl
#
# Load the library
from functions import trasRot, generate_random_list
import trimesh
import numpy as np
import time
# Log start time
st = time.time()
#
# Call functions
#
saveMesh = 1                                        # Do you wish to save the new mesh
vinfo = False                                        # Output additional geometry information to screen?
scale = 0.3                                         # Scale the mesh
initscale = scale                                   # Save initscale as a default used later
rotAx = [0, 1, 0]                                   # Rotate about z axis
numCorals = 25                                      # Number of corals to be generated
rotAngArray = np.random.uniform(0,360,numCorals)    # Rotation angles generated randomly
xlim = [0.03,0.19]                                  # Limits for sampling x coordinate
zlim = [0.03,0.19]                                  # Limits for sampling y coordinate
ylim = [0,0.005]                                    # Limits for sampling z coordinate
sepRadius = 0.0                                     # Seperation radius between to centroids
inFileRandomIndex = [np.random.randint(0, 3) for _ in range(numCorals)]    # Random index to choose which coral is used
inFileArray = ['assets/secale.obj','assets/favulus.obj','assets/cervicornis.obj']      # Input file + location
#
# Load all the mesh and later access only
#
mesh0 = trimesh.load(inFileArray[0])
mesh1 = trimesh.load(inFileArray[1])
mesh2 = trimesh.load(inFileArray[2])
meshList = [mesh0,mesh1,mesh2]
#
# Sample the random translation location
#
print("Generating translation points . . . .")
t1 = time.time()
traslationArray = generate_random_list(numCorals,sepRadius,xlim[0],xlim[1],ylim[0],ylim[1],zlim[0],zlim[1])
t2 = time.time()
print("Finished generating translation points in %f seconds"%(t2-t1))
lenLoop = len(rotAngArray)                          # Compute the length of loop
print("Looping through %d files..."%(lenLoop))      # Screen message
# Log end time for setup
et = time.time()
totalTime = et - st
# Loop over all rotation angles to generate the corals
for ii in range(0,lenLoop,1):
    st = time.time()
    inFile = meshList[inFileRandomIndex[ii]]
    outFile = 'coralgeo/c'+str(ii)+'.obj'                                   # Define the output file
    if(inFileRandomIndex[ii]==1 or inFileRandomIndex[ii]==2):
        scale = 0.4
    else:
        scale = initscale
    print(scale)
    # Translate, scale, and rotate the geometry    
    translation = np.array(traslationArray[ii])                             # Translation in x y and z input
    trasRot(saveMesh,inFile,outFile,translation,rotAngArray[ii],rotAx,scale,verbose=vinfo)    
    et = time.time()
    totalTime += et - st
    print("Choosing coral index: %d"%(inFileRandomIndex[ii]))
    print("Iteration %d done in %f seconds"%(ii+1,et-st))
#
# Print info and close
#
print("-----------------------------------------------------------------------")
print("Total time required: %f seconds"%(round(totalTime,4)))
print("-----------------------------------------------------------------------")
