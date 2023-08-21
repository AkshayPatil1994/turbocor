#
# Import all libraries
# 
import numpy as np
import datetime
#
# Define the function to read the binary snapshot
#
def readField(filein):
    '''
        This function reads the binary snapshot created by `DOPAMINE`
    INPUT
        filein:     [string] Filename and location of the binary snapshot
    OUTPUT
        x,y,z:          [numpy arrays] X,Y, and Z coordinate axes arrays [face locations]
        xm,ym,zm:       [numpy arrays] X,Y, and Z coordinate axes arrays [Cell-Center locations]
        U,V,W,P:        [3D numpy arrays] Data arrays with velocity and pressure
    '''
    fid = open(filein,'rb')

    n = np.fromfile(fid, dtype='<i4', count=1)
    x = np.fromfile(fid, dtype='<f8', count=n[0])

    n = np.fromfile(fid, dtype='<i4', count=1)
    y = np.fromfile(fid, dtype='<f8', count=n[0])

    n = np.fromfile(fid, dtype='<i4', count=1)
    z = np.fromfile(fid, dtype='<f8',count=n[0])

    n = np.fromfile(fid, dtype='<i4', count=1)
    xm = np.fromfile(fid, dtype='<f8', count=n[0])

    n = np.fromfile(fid, dtype='<i4', count=1)
    ym = np.fromfile(fid, dtype='<f8', count=n[0])

    n = np.fromfile(fid, dtype='<i4', count=1)
    zm = np.fromfile(fid, dtype='<f8', count=n[0])

    n = np.fromfile(fid, dtype='<i4', count=3)
    U = np.fromfile(fid, dtype='<f8', count=n[0]*n[1]*n[2]).reshape(n,order='F')

    n = np.fromfile(fid, dtype='<i4', count=3)
    V = np.fromfile(fid, dtype='<f8', count=n[0]*n[1]*n[2]).reshape(n,order='F')

    n = np.fromfile(fid, dtype='<i4', count=3)
    W = np.fromfile(fid, dtype='<f8', count=n[0]*n[1]*n[2]).reshape(n,order='F')

    n = np.fromfile(fid, dtype='<i4', count=3)
    P = np.fromfile(fid, dtype='<f8', count=n[0]*n[1]*n[2]).reshape(n,order='F')

    fid.close()

    return x,y,z,xm,ym,zm,U,V,W,P
#
# Load the masking arrays
#
def readmask(filein,n):
    '''
        This function reads the masking array
    INPUT
        filein:     [string] Name and location of the file to be loaded
        n:          [3 x 1 list] List with grid points info i.e., Nx, Ny, Nz
    OUTPUT
        mask:       [Nx,Ny,Nz numpy array] Masking binary array of size `n`
    '''
    fid = open(filein,'rb')
    mask = np.fromfile(fid, dtype='<f8', count=n[0]*n[1]*n[2]).reshape(n,order='F')
    
    return mask
#
# Read input parameters from file
#
def readinput(infile='input_parameters'):
    '''
        This function reads the file inputfile that sets the analysis parameters
    INPUT
        infile:     [string, Optional] Name and location of the inputfile. Default value `input_parameters`
    OUTPUT
        fileloc:    [string] Name and location of the result files

    '''
    myinpf = open(infile, "r")
    dummy = myinpf.readline()
    fileloc = myinpf.readline()
    fileloc = fileloc.strip()
    fileloc = fileloc[1:-1]
    dummy = myinpf.readline()
    tempread = myinpf.readline()
    data = tempread.split(" ")
    [Nx,Ny,Nz] = map(int,data)
    dummy = myinpf.readline()
    tempread = myinpf.readline()
    data = tempread.split(" ")
    [sind,eind,interval] = map(int,data)
    dummy = myinpf.readline()
    tempread = myinpf.readline()
    data = tempread.split(" ")
    Tw, dt, nphases = float(data[0]), float(data[2]), int(data[4])
    dummy = myinpf.readline()
    tempread = myinpf.readline()
    data = tempread.split(" ")
    isWallRough = int(data[0])
    dummy = myinpf.readline()
    maskloc = myinpf.readline()
    maskloc = maskloc.strip()
    maskloc = maskloc[1:-1]
    myinpf.close()

    # Print summary of the key parameters
    print("- - - - - - - - - - - - - - ")
    print("Input File Summary. . .")
    print("Nx = %d | Ny = %d | Nz = %d"%(Nx,Ny,Nz))
    print("start = %d | end = %d | interval = %d"%(sind,eind,interval))
    print("Tw = %f | dt = %f | nphases = %d"%(Tw,dt,nphases))
    print("Wall rough = %d "%(isWallRough))
    print("- - - - - - - - - - - - - - ")
    return fileloc, maskloc, Nx, Ny, Nz, sind, eind, interval, Tw, dt, nphases, isWallRough
#
# Mask the velocity and pressure data
#
def maskdata(indata,maskdata):
    '''
        This function masks the `indata` using the `maskdata` array
    INPUT
        indata:     [3D numpy array] Input data that needs to be masked
        maskdata:   [3D numpy array] Masking array
    OUTPUT
        indata:     [3D numpy array] Input data masked in place
    '''
    indata[maskdata==0] = np.nan

    return indata
#
# Interpolate array in x [Copied from Lozano-Duran's code]
#
def interpolate_x(uin):
    '''
        This function interpolates the array from cell face to cell center in the X-direction
    INPUT
        uin:    [3D numpy array] Input array to interpolate 
    OUTPUT
        uout:   [3D numpy array] Output array
    '''
    nusize = np.shape(uin)
    uout = np.zeros(nusize)
    uout[0:nusize[0]-1,0:nusize[1],0:nusize[2]] = 0.5*(uin[0:nusize[0]-1,:,:]+uin[1:nusize[0],:,:])

    return uout
#
# Interpolate array in z [Copied from Lozano-Duran's code]
#
def interpolate_z(uin):
    '''
        This function interpolates the array from cell face to cell center in the Z-direction
    INPUT
        uin:    [3D numpy array] Input array to interpolate 
    OUTPUT
        uout:   [3D numpy array] Output array
    '''
    nusize = np.shape(uin)
    uout = np.zeros(nusize)
    uout[0:nusize[0],0:nusize[1],0:nusize[2]-1] = 0.5*(uin[:,:,0:nusize[2]-1]+uin[:,:,1:nusize[2]])

    return uout
#
# Interpolate array in y [Copied from Lozano-Duran's code]
#
def interpolate_y(uin):
    '''
        Interpolate the array in the Y-direction
    INPUT
        uin:    [3D numpy array] Input array to be interpolated¯
    OUTPUT
        uout:   [3D numpy array] Output array
    '''
    nusize = np.shape(uin)
    uout = np.zeros(nusize)
    
    uout[0:nusize[0],0:nusize[1]-1,0:nusize[2]] = 0.5*(uin[:,0:nusize[1]-1,:]+uin[:,1:nusize[1],:])

    return uout
#
# All gradient computations
#
def allgradient(u,v,w,x,y,z):
    '''
        This function computes the gradient for given u,v,w velocities in all directions using first order accurate scheme
    INPUT
        u,v,w:  [3D numpy arrays] Velocity arrays
        x,y,z:  [1D numpy arrays] Cartesian coordinates
    OUTPUT
        djui:   [3D numpy arrays] Gradient arrays corresponding to all the components [9 in total]
    '''
    # Check size of the input arrays
    nu = np.shape(u)
    nv = np.shape(v)
    nw = np.shape(w)
    # Initialise data
    dudx, dvdx, dwdx = np.zeros(nu), np.zeros(nv), np.zeros(nw)
    dudy, dvdy, dwdy = np.zeros(nu), np.zeros(nv), np.zeros(nw)
    dudz, dvdz, dwdz = np.zeros(nu), np.zeros(nv), np.zeros(nw)
    # Compute the grid size
    dx = x[10] - x[9]
    dy = np.gradient(y,edge_order=1)
    dz = z[10] - z[9]
    # Gradients in x
    dudx[0:nu[0]-1,:,:] = (u[1:nu[0],:,:] - u[0:nu[0]-1,:,:])/dx
    dvdx[0:nv[0]-1,:,:] = (v[1:nv[0],:,:] - v[0:nv[0]-1,:,:])/dx
    dwdx[0:nw[0]-1,:,:] = (w[1:nw[0],:,:] - w[0:nw[0]-1,:,:])/dx
    # Gradient in y
    dudy[:,0:nu[1]-2,:] = (u[:,1:nu[1]-1,:] - u[:,0:nu[1]-2,:])/dy[:,np.newaxis]
    dvdy[:,0:nv[1]-2,:] = (v[:,1:nv[1]-1,:] - v[:,0:nv[1]-2,:])/dy[0:nv[1]-2,np.newaxis]
    dwdy[:,0:nw[1]-2,:] = (w[:,1:nw[1]-1,:] - w[:,0:nw[1]-2,:])/dy[:,np.newaxis]
    # Gradients in z
    dudz[:,:,1:nw[2]] = (u[:,:,1:nw[2]] - u[:,:,0:nw[2]-1])/dz
    dvdz[:,:,1:nw[2]] = (v[:,:,1:nw[2]] - v[:,:,0:nw[2]-1])/dz
    dwdz[:,:,1:nw[2]] = (w[:,:,1:nw[2]] - w[:,:,0:nw[2]-1])/dz
    # Handling end points
    dudx[-1,:,:], dvdx[-1,:,:], dwdx[-1,:,:] = dudx[-2,:,:], dvdx[-2,:,:], dwdx[-2,:,:]
    dudy[:,-1,:], dvdx[:,-1,:], dwdx[:,-1,:] = dudx[:,-2,:], dvdx[:,-2,:], dwdx[:,-2,:]
    dudz[:,:,-1], dvdx[:,:,-1], dwdx[:,:,-1] = dudx[:,:,-2], dvdx[:,:,-2], dwdx[:,:,-2]

    return dudx, dvdx, dwdx, dudy, dvdy, dwdy, dudz, dvdz, dwdz 
#
# Compute Turbulent Kinetic Energy Dissipation Rate
#
def tkedissipation(kvisc,dudx,dudy,dudz,dvdx,dvdy,dvdz,dwdx,dwdy,dwdz):
    '''
        This function computes the turbulent kinetic energy dissipation rate
    INPUT
        kvisc:      [3D numpy arrays] Kinetmatic viscosity in m^2/s
        djui:       [3D numpy arrays] Gradients in all directions
    OUTPUT
        epsilon:    [3D numpy array] TKE dissipation rate
    '''
    epsilon = kvisc*(dudx**2 + dudy**2 + dudz**2 + dvdx**2 + dvdy**2 + dvdz**2 + dwdx**2 + dwdy**2 + dwdz**2)

    return epsilon
#
# Welcome message for analysis
#
def welcomemessage():
    '''
        This function prints a welcome message
    INPUT
        None
    OUTPUT
        I/O to screen
    '''
    print("*** Dopamine sequence starting ***")
    mytime = datetime.datetime.now()
    print("Sequence started on: %s"%(mytime))
#
# Graceful exit message
#
def gracefulexit(stime,etime):
    '''
        This function prints an exit message
    INPUT
        stime:      [float] Starting time of the analysis
        etime:      [float] Ending time of the analysis
    OUTPUT
        I/O to screen
    '''
    print("- - - - - - - - - - - - - - ")
    print("Ending analysis time loop on: %s"%(datetime.datetime.now()))
    print("Total Analysis Time: %f hours"%((etime-stime)/3600))
    print("*** Dopamine squence analysed ***")
