from functions import readField, readmask
import matplotlib.pyplot as plt
import numpy as np
import cmocean
#
# User input data
#
yloc = 10
filename = '../fields/channel_test.23200'
#
# Load data
#
[xf,yf,zf,xm,ym,zm,U,V,W,P] = readField(filename)
umask = readmask('../Umask_in',np.shape(U))
U[umask==0] = np.nan
#
# Plotting
#
cmap = cmocean.cm.ice                   # Choose the colormap
plt.figure(1,figsize=(10,10))
plt.axes(facecolor='red')
plt.contourf(xf,zm,(U[:,yloc,0:-2]).T,cmap=cmap)
plt.colorbar()
plt.show()
