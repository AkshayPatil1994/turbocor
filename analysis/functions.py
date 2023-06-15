#
# Import all libraries
# 
import numpy as np
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



