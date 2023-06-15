#%% IMPORT REQUIRED LIBRARIES
#from mesh_to_sdf import *                 # mesh to sdf library
import trimesh                            # Trimesh library
import skimage                            # Sci-kit library
import numpy as np                        # Numpy library
import functions as myf                   # CaNS related grid operations
from mpi4py import MPI                    # MPI for python module for parallelisation
import time                               # Timing library to time the process
import sys                                # Import system to exit script
#
# Initialise MPI and communications
#
comm = MPI.COMM_WORLD   # Initialise MPI comm-world        
rank = comm.Get_rank()  # Get rank of each proc
size = comm.Get_size()  # Get size of mpirun for each instance
#
# Rank 0 does all the I/O and initial setup
#
if rank == 0:
    start_time = time.time()        # Store start time
    print("---------------------------------------------------------")
    print("███████╗████████╗██╗     ██████╗ ███████╗██████╗ ███████╗")
    print("██╔════╝╚══██╔══╝██║     ╚════██╗██╔════╝██╔══██╗██╔════╝")
    print("███████╗   ██║   ██║      █████╔╝███████╗██║  ██║█████╗  ")
    print("╚════██║   ██║   ██║     ██╔═══╝ ╚════██║██║  ██║██╔══╝  ")
    print("███████║   ██║   ███████╗███████╗███████║██████╔╝██║     ")
    print("╚══════╝   ╚═╝   ╚══════╝╚══════╝╚══════╝╚═════╝ ╚═╝")
    print("---------------------------------------------------------")
    print(" - - - - - - - Starting the MPI job - - - - - - - ")
    print("    User requested ",size," CPUs for this job  ")
    print("---------------------------------------------------------")
    #
    # User flag to write SDF to files
    #
    writeData = True
    #
    # Name of the input-output file
    #
    inFile = 'assets/coralbed.obj'
    #
    # Target mesh folder
    #
    filename = 'assets/'
    #
    # Number of sampling points used to compute the SDF 
    # [large values are memory and compute time intensive .but. improve the SDF computation]
    #
    nsamples = 1000000
    #
    # Load the mesh
    #
    #[xp,yp,zp,xf,yf,zf] = myf.readGrid(filename,[1,1,1],[0.0,0.0,0.0],1)    # Loading the grid
    gridfile = 'assets/grid.out'
    [xft,yft,zft,xpt,ypt,zpt] = myf.loaddopaminegrid(gridfile)
    #
    # Slice arrays to fit
    #
    xp = xpt[1:]
    yp = ypt
    zp = zpt[1:]
    xf = xft[2:]
    yf = yft[1:]
    zf = zft[2:]
    #
    # Print grid information to screen
    #
    print("xp grid -- starts at %f | ends at %f with %d points"%(xp[0],xp[-1],len(xp)))
    print("yp grid -- starts at %f | ends at %f with %d points"%(yp[0],yp[-1],len(yp)))
    print("zp grid -- starts at %f | ends at %f with %d points"%(zp[0],zp[-1],len(zp)))
    print("xf grid -- starts at %f | ends at %f with %d points"%(xf[0],xf[-1],len(xf)))
    print("yf grid -- starts at %f | ends at %f with %d points"%(yf[0],yf[-1],len(yf)))
    print("zf grid -- starts at %f | ends at %f with %d points"%(zf[0],zf[-1],len(zf)))
    #
    # Define the size of the array for U, V, W, and P 
    #
    Nu = np.array([len(xf),len(yp),len(zp)])
    Nv = np.array([len(xp),len(yf),len(zp)])
    Nw = np.array([len(xp),len(yp),len(zf)])
    Ns = np.array([len(xp),len(yp),len(zp)])
    print("Size Nu: %d %d %d"%(Nu[0],Nu[1],Nu[2]))
    print("Size Nv: %d %d %d"%(Nv[0],Nv[1],Nv[2]))
    print("Size Nw: %d %d %d"%(Nw[0],Nw[1],Nw[2]))
    print("Size Ns: %d %d %d"%(Ns[0],Ns[1],Ns[2]))    
    #
    # Load stl/obj file as mesh object
    #
    mesh = trimesh.load(inFile)
    #
    # Do some consistency checks on the mesh
    #
    ismeshWT = mesh.is_watertight           # Check if the mesh is watertight
    if(ismeshWT):
        print("---------------------------------------------------------")
        print("File %s is watertight"%(inFile))
        print("---------------------------------------------------------")
    else:
        print("---------------------------------------------------------")
        print("File %s is *NOT* watertight, the resulting SDF may not be accurate!"%(inFile))
        print("---------------------------------------------------------")
    #
    # Force check for number of processors
    #
    remMod = Nu[0]%size
    if remMod != 0:
        sys.exit("Please set nprocs such that Nx%nprocs == 0...")
#
# Force all processors to arrive at this barrier
#
comm.Barrier()
#
# Allocate memory on all procs for broadcasted data
#
if rank != 0:
    inFile = ""
    nsamples = None
    Nu = np.array([0,0,0])
    Nv = np.array([0,0,0])
    Nw = np.array([0,0,0])
    Ns = np.array([0,0,0])
#
# Broadcast common data to all ranks
#
inFile = comm.bcast(inFile,root=0)    # This syntax only for type str
nsamples = comm.bcast(nsamples,root=0)
comm.Bcast([Nu, MPI.DOUBLE],root=0)
comm.Bcast([Nv, MPI.DOUBLE],root=0)
comm.Bcast([Nw, MPI.DOUBLE],root=0)
comm.Bcast([Ns, MPI.DOUBLE],root=0)
#
# Broadcast common data to all procs
#
if rank != 0:
    # Grid data
    yp = np.empty(Ns[1],dtype=np.float64)
    zp = np.empty(Ns[2],dtype=np.float64)
    yf = np.empty(Nv[1],dtype=np.float64)
    zf = np.empty(Nw[2],dtype=np.float64)
    xf = np.empty(np.int64(Nu[0]/size),dtype=np.float64)
    xp = np.empty(np.int64(Ns[0]/size),dtype=np.float64)
#
# Create local arrays that are split to distribute the workload
#
xpl = np.empty(np.int64(Ns[0]/size),dtype=np.float64)
xfl = np.empty(np.int64(Nu[0]/size),dtype=np.float64)  
#
# Broadcast all arrays as is and then split the workload [easier but **in-efficient**]
# Since the grid arrays have small memory footprint, this does not lead to any efficiency downgrade
#
comm.Bcast([yp, MPI.DOUBLE],root=0)
comm.Bcast([zp, MPI.DOUBLE],root=0)
comm.Bcast([yf, MPI.DOUBLE],root=0)
comm.Bcast([zf, MPI.DOUBLE],root=0)
comm.Scatter(xf,xfl,root=0)
comm.Scatter(xp,xpl,root=0)
#
# All procs now load the obj file
#
mesh = trimesh.load(inFile)
#
# Check start time of analysis
#
if rank == 0:
    anaStartTime = time.time()
#
# Compute the SDF on each proc for all components
#
SDFUlocal = myf.computeSDF(mesh,xfl,yp,zp,nsamples)
SDFVlocal = myf.computeSDF(mesh,xpl,yf,zp,nsamples)
SDFWlocal = myf.computeSDF(mesh,xpl,yp,zf,nsamples)
SDFPlocal = myf.computeSDF(mesh,xpl,yp,zp,nsamples)
# Type conversion [Change precision of the output array below]
SDFUlocal = SDFUlocal.astype(np.float64,casting='same_kind')
SDFVlocal = SDFVlocal.astype(np.float64,casting='same_kind')
SDFWlocal = SDFWlocal.astype(np.float64,casting='same_kind')
SDFPlocal = SDFPlocal.astype(np.float64,casting='same_kind')
#
# Check end time of analysis
#
if rank == 0:
    anaEndTime = time.time()
# Define size of the SDF required
sdfusize = Nu[0]*Nu[1]*Nu[2]
sdfvsize = Nv[0]*Nv[1]*Nv[2]
sdfwsize = Nw[0]*Nw[1]*Nw[2]
sdfpsize = Ns[0]*Ns[1]*Ns[2]
#
# Gather the array from all processors to id = 0
#
sdfu_recv = None
sdfv_recv = None
sdfw_recv = None
sdfp_recv = None
if rank == 0:
    sdfu_recv = np.empty(sdfusize,dtype='d')
    sdfv_recv = np.empty(sdfvsize,dtype='d')
    sdfw_recv = np.empty(sdfwsize,dtype='d')
    sdfp_recv = np.empty(sdfpsize,dtype='d')
#
# Gather all data
#
# Life is great as long as array chunk < 2GB see https://github.com/mpi4py/mpi4py/issues/23
# MPI and mpi4py give SystemError: Negative size passed to PyBytes_FromStringAndSize for chunk > 2GB
# For array chunks < 2GB comm.gather() works. However, for chunks > 2GB one needs to use comm.Gatherv([sentbuf, MPI.double],root=0)
#sdfu_recv = comm.gather(SDFUlocal,root=0)
#sdfv_recv = comm.gather(SDFVlocal,root=0)
#sdfw_recv = comm.gather(SDFWlocal,root=0)
#sdfp_recv = comm.gather(SDFPlocal,root=0)
comm.Gatherv(SDFUlocal,sdfu_recv,root=0)
comm.Gatherv(SDFVlocal,sdfv_recv,root=0)
comm.Gatherv(SDFWlocal,sdfw_recv,root=0)
comm.Gatherv(SDFPlocal,sdfp_recv,root=0)
#
# Write SDF to file
#
if rank == 0 and writeData:
    sdfu_recv = np.array(sdfu_recv)   
    np.save('assets/sdfu',sdfu_recv)
    sdfv_recv = np.array(sdfv_recv)   
    np.save('assets/sdfv',sdfv_recv)
    sdfw_recv = np.array(sdfu_recv)   
    np.save('assets/sdfw',sdfw_recv)
    sdfp_recv = np.array(sdfp_recv)   
    np.save('assets/sdfp',sdfp_recv)
#
# Print exit information
#
if rank == 0:
    end_time = time.time()
    process_time = end_time - start_time
    print("Code took around ",np.round(anaEndTime-anaStartTime,4),"seconds to run the analysis...")
    print("- Total wall-clock time: ",np.round(process_time,4),"seconds - ")
