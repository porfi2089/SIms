import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

# Initialize figure and 3D axis
fig = plt.figure()
pos = fig.add_subplot(111, projection='3d')
ta = fig.add_subplot(11, projection='2d')



# Data lists for the curve
xp, yp, zp = [], [], []
posx, posy, posz = pos
# Update function for animation
def update(num):
    t = num / 10  # We will have 10 frames per second

    xp.append(posx)
    yp.append(posy)
    zp.append(posz)

    pos.clear()  # Clear the current state of the plot
    pos.plot(xp, yp, zp, label='position')
    pos.legend()

    pos.set_xlabel('X pos')
    pos.set_ylabel('Y pos')
    pos.set_zlabel('Z pos')

    pos.set_xlim([min(xp)-5, max(xp)+5])
    pos.set_ylim([min(yp)-5, max(yp)+5])
    pos.set_zlim([0, max(zp)+5])

# Set up the animation
def showSim(position, rotation):

    ani = FuncAnimation(fig, update, frames=1000, interval=100)

plt.show()
