import trimesh                              # Trimesh library
import numpy as np                          # Numpy library
import warnings                             # Warning library
import sys                                  # Exit option 
from multiprocessing import Pool            # Multithreading
import math                                 # Basic math
import time                                 # Time operations
import os                                   # FIle I/O
import matplotlib.pyplot as plt             # Plotting
#
# Translate and rotate geometry
#     
def trasRot(saveMesh=False,mesh='dummy.stl',outMesh='output.stl',tarr=[0.0,0.0,0.0],rotang=0.0,rotax=[0.0,0.0,0.0],scalegeo=1.0,verbose=False):    
    '''
        This function translates and rotates the geometry based on user specification
    INPUT
        saveMesh:   [Boolean] Do you wish to save the mesh?  
        inMesh:     [mesh object] Mesh object used to translate and rotate        
        tarr:       [3 x 1 list] Translation array in x, y, and z
        rotang:     [float] Rotation angle in degrees
        rotax:      [3 x 1 list] Rotation axis
        scalegeo:   [float] scale the input geometry by a factor
        verbose:    [Boolean] If true, outputs some  geometric information
    OUTPUT:
        outMesh:    [string] Name of the output mesh, default = output.stl
    '''
    #
    # Exit if inputfile is not defined
    #
    if mesh == 'dummy.stl':
        sys.exit("ERROR: Please specify the input filename and location....")

    rotAngRad = np.radians(rotang)
    rotAxis = np.array(rotax) / np.linalg.norm(rotax)
    rotQuat = trimesh.transformations.quaternion_about_axis(rotAngRad, rotAxis)
    rotMat = trimesh.transformations.quaternion_matrix(rotQuat)

    waterTight = mesh.is_watertight

    if verbose:
        if waterTight == 0:
            warnings.warn("Input file is not watertight, this may cause issues for generating the SDF!")
            print("------------------------------------------------------------------------------------")
        else:
            print("Input file is watertight")
            print("------------------------------------------------------------------------------------")

    if verbose:
        print("Oriented Bounding box [before operations]")
        print("xmin, ymin, zmin --", mesh.bounds[0])
        print("xmax, ymax, zmax --", mesh.bounds[1])
        print("------------------------------------------------------------------------------------")

    centmass = mesh.center_mass
    mesh.vertices -= centmass

    mesh.apply_transform(rotMat)

    mesh.vertices += centmass

    mesh.vertices *= scalegeo

    mesh.vertices += tarr

    if verbose:
        print("Oriented Bounding box [after operations]")
        print("xmin, ymin, zmin --", mesh.bounds[0])
        print("xmax, ymax, zmax --", mesh.bounds[1])
        print("------------------------------------------------------------------------------------")

    if saveMesh:
        mesh.export(outMesh)

    mesh.vertices -= tarr
    mesh.vertices /= scalegeo

    return mesh

#
# Define local random generator function
#
def generate_random_list(n, sr, minx, maxx, miny, maxy, minz, maxz):
    '''
        Generate a list of random numbers that is n x 3
    INPUT
        n:      [integer] Size of the list i.e., n x 3
        sr:     [float] Seperation radius between two centroids
        minx:   [float] Lower bound of the x coordinate
        maxx:   [float] Upper bound of the x coordinate
        miny:   [float] Lower bound of the y coordinate
        maxy:   [float] Upper bound of the y coordinate
        minz:   [float] Lower bound of the z coordinate
        maxz:   [float] Upper bound of the z coordinate
    OUTPUT
        rand_list:  [list] List of size n x 3
    ''' 
    rand_list = []
    for iter in range(n):
        fc = np.random.uniform(minx, maxx)
        sc = np.random.uniform(miny, maxy)
        tc = np.random.uniform(minz, maxz)
        rand_list.append([fc, sc,tc])
            
    return rand_list
#
# Define the load mesh function
#
def load_mesh(ii):
    '''
        This function defines the load mesh function to be used takes the input argument of the coral id
    '''
    # Define the exact location of the coral file
    inFile = f'coralgeo/c{ii}.obj'
    mesh = trimesh.load_mesh(inFile)    # Load the mesh
    return mesh
#
# Define the combine mesh function
#
def combine_coral_meshes(startc,endc,outFile='combined_coral.stl'):
    '''
        This function combines the corals into a single stl file using multithreading
    INPUT
        startc:     [integer] Start index of the coral file to be combined
        endc:    [integer] End index of coral files to be combined
    OUTPUT
        outFile:    [string] The name of the combined output file
    '''
    #
    # Start the program here
    #
    progress_counter = 0  # Counter to track progress
    #
    # Pool the loading mechanism
    #
    with Pool() as pool:
        #
        # Map load_mesh function to the range of ncorals
        #
        mesh_list = pool.map(load_mesh, range(startc,endc,1))
        #
        # Print progress for each completed iteration
        #
        for _ in pool.imap_unordered(load_mesh, range(startc,endc,1)):
            progress_counter += 1
            print(f"Iteration {progress_counter}/{endc-startc} done..")
    #
    # Combine the mesh here and export
    #
    combined_mesh = trimesh.util.concatenate(mesh_list)
    combined_mesh.export(outFile)
    # Return the combined mesh
    return combined_mesh
#
# Function to downsample the stl [limits the size]
#
def reduce_stl_size(input_file, output_file, reduction_ratio,verbose=False,fileobj=False):
    '''
        This function downsamples the given stl
    INPUT
        input_file:         [string] Name and location of the file to be downsampled
        reduction_ratio:    [float] Reduction ratio ranging between 0.0 to 1.0. A value of 0.1 means 1/10th the size
        verbose:            [Boolean] Display info to screen
        fileobj:            [Boolean] Output file as obj
    OUTPUT
        output_file:        [string] Name and location of the downsampled stl file
    '''
    # Query file size
    ifilesize = os.path.getsize(input_file)
    # Load the input STL file
    st = time.time()
    mesh = trimesh.load_mesh(input_file)
    et = time.time()
    print("------------------------------------------------------------------------")
    print("Mesh loaded in %f seconds"%(et-st))
    # Get the number of total active faces
    num_faces = mesh.faces.shape[0]
    # Compute the target number of faces using the reduction ratio
    tgt_numfaces = math.floor(num_faces*reduction_ratio)
    # Print info to screen
    if(verbose):
        print("------------------------------------------------------------------------")
        print("The mesh currently has %d faces"%(num_faces))
        print("User requested downsampling to %d faces"%(tgt_numfaces))    
        print("------------------------------------------------------------------------")
    # Simplify the mesh
    st = time.time()
    simplified_mesh = mesh.simplify_quadric_decimation(tgt_numfaces)
    et = time.time()
    # Check the reduction in the number of faces
    actual_faces = simplified_mesh.faces.shape[0]
    if(verbose):
        print("The downsampled mesh has %d faces"%(actual_faces))    
        print("Reduced mesh is water tight?: ",simplified_mesh.is_watertight)
        print("Reduction Ratio requested: %f | Reduction ratio achieved: %f"%(reduction_ratio,round(actual_faces/num_faces,4)))
        print("------------------------------------------------------------------------")
        print("Writing file to %s"%(output_file))
    # Export the simplified mesh to an STL file
    if(fileobj):
        simplified_mesh.export(output_file,file_type='obj')        
    else:
        simplified_mesh.export(output_file)
    # Query file size
    ofilesize = os.path.getsize(output_file)
    print("Took %f seconds to downsample....."%(et-st))
    print("Original file size: %d MB | Modified file size: %d MB"%(ifilesize*1e-6,ofilesize*1e-6))
    print("------------------------------------------------------------------------")
#
# Set default plotting size
#
def fixPlot(thickness=1.0, fontsize=12, markersize=6, labelsize=10, texuse=False):
    '''
        This plot sets the default plot parameters
    INPUT
        thickness:      [float] Default thickness of the axes lines
        fontsize:       [integer] Default fontsize of the axes labels
        markersize:     [integer] Default markersize
        labelsize:      [integer] Default label size
    OUTPUT
        None
    '''
    # Set the thickness of plot axes
    plt.rcParams['axes.linewidth'] = thickness    
    # Set the default fontsize
    plt.rcParams['font.size'] = fontsize    
    # Set the default markersize
    plt.rcParams['lines.markersize'] = markersize    
    # Set the axes label size
    plt.rcParams['axes.labelsize'] = labelsize
    # Enable LaTeX rendering
    plt.rcParams['text.usetex'] = texuse

