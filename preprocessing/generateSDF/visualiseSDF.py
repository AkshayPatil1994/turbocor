# Import required libraries
import numpy as np
import functions as myf
import matplotlib.pyplot as plt
#
# Setup the gridsize
#
N = [1024,256,512]
#
# Load the grid
#
[xp,zp,yp,xf,zf,yf] = myf.loaddopaminegrid('../../wavywall/grid.out')
#
# Load the file
#
sdfu = np.load('assets/sdfu.npy')
sdfu = np.reshape(sdfu,N)
#
# Plotting for check
#
plt.figure(1)
plt.contour((sdfu[:,20,:]).T,levels=[0,0.0001],colors=['black','black'])
plt.contourf((sdfu[:,20,:]).T)
plt.title('U faces')
plt.colorbar()
plt.clim(-1,1)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()

