# Loading all required libraries
import matplotlib.pyplot as plt
from functions import readmask, readSingleField, maskdata, loaddopaminegrid, fixPlot
import time
import cmocean
#
# User input data
#
figx, figy = 15, 8			# Define the size of the figure
cmap = cmocean.cm.tarn			# Define the colormap to be used when plotting
yloc = 20				# Vertical location of the slice
wavephase = 1				# Wave phase index to be used
N = [515,130,515]                   	# This is the largest value for all directions
maskloc = '../run/'			# Location of the masking arrays [base location only!]
#
# Loading allthe data
#
gridfile = '../run/grid.out'
[xf,yf,zf,xm,ym,zm] = loaddopaminegrid(gridfile)
#
maskin = maskloc+'Umask_in'
Umask = readmask(maskin,[N[0]-1,N[1],N[2]])
filein = str('data/Uphase_'+str(wavephase+1)+'.bin')
U = readSingleField(filein,[N[0]-1,N[1],N[2]])
U = maskdata(U,Umask)
#
maskin = maskloc+'Vmask_in'
Vmask = readmask(maskin,[N[0],N[1]-1,N[2]])
filein = str('data/Vphase_'+str(wavephase+1)+'.bin')
V = readSingleField(filein,[N[0],N[1]-1,N[2]])
V = maskdata(V,Vmask)
#
maskin = maskloc+'Wmask_in'
Wmask = readmask(maskin,[N[0],N[1],N[2]-1])
filein = str('data/Wphase_'+str(wavephase+1)+'.bin')
W = readSingleField(filein,[N[0],N[1],N[2]-1])
W = maskdata(W,Wmask)
#
# Plotting the figure
#
fixPlot(thickness=1.5, fontsize=20, markersize=8, labelsize=25, texuse=True, tickSize = 15)
plt.figure(1,figsize=(figx,figy))
plt.subplot(1,3,1)
plt.contourf(xf,zm,(U[:,yloc,0:-2]).T,cmap=cmap)
plt.ylabel(r'$x_1$')
plt.xlabel(r'$x_2$')
plt.subplot(1,3,2)
plt.contourf(xm,zm,(V[0:-2,yloc,0:-2]).T,cmap=cmap)
plt.xlabel(r'$x_2$')
plt.subplot(1,3,3)
plt.contourf(xm,zf,(W[0:-2,yloc,:]).T,cmap=cmap)
plt.xlabel(r'$x_2$')
plt.show()
