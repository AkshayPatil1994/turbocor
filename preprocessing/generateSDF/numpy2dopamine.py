#
# Import all required functions
#
import numpy as np
from functions import loaddopaminegrid, n2carray
#
# User input data
#
gridfile = 'assets/grid.out'
[x,y,z,xm,ym,zm] = loaddopaminegrid(gridfile)
print("--------------------------------------------------------------------------------------------")
print("Preliminary grid information")
print("Cell Faces: %f - %f = Size - %d | Cell Centers %f - %f = Size - %d"%(x[0],x[-1],len(x),xm[0],xm[-1],len(xm)))
print("Cell Faces: %f - %f = Size - %d | Cell Centers %f - %f = Size - %d"%(y[0],y[-1],len(y),ym[0],ym[-1],len(ym)))
print("Cell Faces: %f - %f = Size - %d | Cell Centers %f - %f = Size - %d"%(z[0],z[-1],len(z),zm[0],zm[-1],len(zm)))
print("--------------------------------------------------------------------------------------------")
# Compute grid size of the SDF
N = [len(x)-2,len(y)-1,len(z)-2]
#
# Load the [SDF]
#
sdfu = np.load('stl2sdf/assets/sdfu.npy')
sdfu = np.reshape(sdfu,N)
sdfv = np.load('stl2sdf/assets/sdfv.npy')
sdfv = np.reshape(sdfv,N)
sdfw = np.load('stl2sdf/assets/sdfw.npy')
sdfw = np.reshape(sdfw,N)
sdfp = np.load('stl2sdf/assets/sdfp.npy')
sdfp = np.reshape(sdfp,N)
#
# Port to Dopamine compatible masks
#
sdfud = np.ones([N[0]+2,N[1]+2,N[2]+3])
sdfvd = np.ones([N[0]+3,N[1]+1,N[2]+3])
sdfwd = np.ones([N[0]+3,N[1]+2,N[2]+2])
sdfpd = np.ones([N[0]+3,N[1]+2,N[2]+3])
for ii in range(0,N[0]):
    for jj in range(0,N[1]):
        for kk in range(0,N[2]):
            if(sdfu[ii,jj,kk] < 0):
                sdfud[ii,jj,kk] = 0.0
print("Done U conversion....")
for ii in range(0,N[0]):
    for jj in range(0,N[1]):
        for kk in range(0,N[2]):
            if(sdfv[ii,jj,kk] < 0):
                sdfvd[ii,jj,kk] = 0.0
print("Done V conversion....")
for ii in range(0,N[0]):
    for jj in range(0,N[1]):
        for kk in range(0,N[2]):
            if(sdfw[ii,jj,kk] < 0):
                sdfwd[ii,jj,kk] = 0.0
print("Done W conversion....")
for ii in range(0,N[0]):
    for jj in range(0,N[1]):
        for kk in range(0,N[2]):
            if(sdfp[ii,jj,kk] < 0):
                sdfpd[ii,jj,kk] = 0.0
print("Done P conversion....")
# Write arrays to file
n2carray(sdfud,np.shape(sdfud),'assets/Umask_in')
n2carray(sdfvd,np.shape(sdfvd),'assets/Vmask_in')
n2carray(sdfwd,np.shape(sdfwd),'assets/Wmask_in')
n2carray(sdfpd,np.shape(sdfpd),'assets/Pmask_in')
