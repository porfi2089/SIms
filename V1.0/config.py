import math
import numpy as np

#sim setings
max_cycles = 2500
step = 0.2
output_file = 'test.csv'

#vehicle data
mass = 0.48
MMI = [0.005, 0.005, 0.0025]  # mass moment of inertia (Kg/m2)
body_ca = 0.01  # cross-sectional area of body (m2)
body_cd = 0.75  # coefficient of drag of body
TGL = 298.15  # temperature at ground level (K)
fin_amount = 4  # fin amount
fin_d_center = 0.085  # m from center (m)
afoil_len = 0.043  # m
afoil_front_width = 0.005  # m
afoil_side_width = 0.05  # m
chute_area = 0.2  # m2
chute_deploy_time = 1  # s
chute_cd = 1  # coefficient of drag

# variables
time = 0  # time in S
position = np.array([400, 0, 0])
velocity = np.zeros((3, 1))  # m/s
acceleration = np.zeros((3, 1))  # m/s2
rot = np.zeros((3, 1))
rot_acc = np.zeros((3, 1))
rot_vel = np.zeros((3, 1))
b_drag = 0  # N, of body
a_drag = 0  # N, of body 
atm_density = 0  # Kg/m2
atm_pressure = 0  # pa
air_temp = 0  # K
fin_def = math.radians(0)  # degrees°
a_side_area = 0  # airfoil side area (m2)
a_front_area = 0  # airfoil frontal area (m2)
z_angle = 0  # angle in degrees from staring position oon the z axis
z_ang_rate = 0  # z angular rate
z_ang_acc = 0  # angular acceleration on z
z_torque = 0  # angular torque on z
chute_flag = False