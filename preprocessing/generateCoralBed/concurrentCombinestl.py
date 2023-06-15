#
# Import required libraries
#
from functions import load_mesh, combine_coral_meshes
#
# Call the defined functions
#
scoral = 0                                      # Starting index of the coral
ncorals = 25                                    # Number of coral files to be combined
outFile = 'assets/coralbed.obj'                 # Name of the combined file
#
# Call the function to combine the stls
#
combined_mesh = combine_coral_meshes(scoral,ncorals,outFile)
