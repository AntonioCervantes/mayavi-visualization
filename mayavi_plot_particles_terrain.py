from cv2 import COLORMAP_HOT
import numpy as np
from mayavi import mlab
import pandas as pd
import glob
import os
from IPython import embed

###############
### Data IO ###
###############

# Choose simulation folder name
#terrain = 'Manning_Creek'
terrain = 'FF2'

# Choose simulation run folder name
sim_name = 'Run_20'


# Join Data Paths
cur_path = os.path.curdir
data_path = os.path.join(cur_path, "Data")
sim_path = os.path.join(data_path, terrain)
terrain_path = os.path.join(sim_path, "terrain_data")

X_path = os.path.join(terrain_path, 'X.csv')
Y_path = os.path.join(terrain_path, 'Y.csv')
HGT_path = os.path.join(terrain_path, 'HGT.csv')
fire_path = os.path.join(terrain_path, 'Fire.csv')   # Not yet working

X = np.genfromtxt(X_path, delimiter=',')
Y = np.genfromtxt(Y_path, delimiter=',')
HGT = np.genfromtxt(HGT_path, delimiter=',')
fire = np.genfromtxt(fire_path, delimiter=',')

# Add this if you want to plot fire (NOT WORKING)
# fireX = np.genfromtxt(terrain_path+'\FireX.csv', delimiter=',')
# fireY = np.genfromtxt(terrain_path+'\FireY.csv', delimiter=',')
# fireZ = np.genfromtxt(terrain_path+'\FireZ.csv', delimiter=',')


####################
### Mayavi Plots ###
####################

# Plot Terrain
b = mlab.figure(bgcolor=(1, 1, 1), fgcolor=(0,0,0))
s = mlab.mesh(X, Y, HGT, colormap="summer", name="Terrain Height [m]")

# Plot XYZ axes
#ax=mlab.axes()
# Manning Creek
#ax = mlab.axes(xlabel='X [m]',ylabel='Y [m]',zlabel='Z [m]',extent=[0, 17000, 0, 17000, 1800, 5000],nb_labels=3)
# FF2
ax = mlab.axes(xlabel='X [m]',ylabel='Y [m]',zlabel='Z [m]',extent=[0, 1000, 0, 1600, 0, 200],nb_labels=3, color=(0,0,0))

# #mlab.colorbar()
#ax.orientation_axes(xlabel='X', ylabel='Y', zlabel='Z')
ax.label_text_property.font_family = 'times'
ax.label_text_property.font_size = 14
ax.title_text_property.font_family = 'times'
ax.title_text_property.font_size = 14

# Plot fire on terrain
#s = mlab.surf(fireX, fireY, fireZ, color="red")
#s = mlab.points3d(fireX, fireY, fireZ, scale_factor=3, color="red")

# Initialize arrays for particles
Xp = np.empty(1)
Yp = np.empty(1)
Zp = np.empty(1)
s = np.empty(1)

particle_path = os.path.join(sim_path, sim_name)
files_path = os.path.join(particle_path,'*')
data_files = glob.glob(files_path + '*.csv')


for filename in data_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    traj = df.to_numpy()
    Xp = np.append(Xp,traj[:,1],axis=0)
    Yp = np.append(Yp,traj[:,2],axis=0)
    Zp = np.append(Zp,traj[:,3],axis=0)



plot = mlab.points3d(Xp, Yp, Zp, scale_factor=3, color=(0.69,0.69,1))

# Alternative methods for plotting particles
# colors = 1.0 * (Xp + Zp)/(max(Xp)+max(Zp))
# plot = mlab.points3d(Xp, Yp, Zp, scale_factor=3, color=colors)
#plot.glyph.scale_mode = 'scale_by_vector'
#plot.mlab_source.dataset.point_data.scalars = colors

mlab.show()