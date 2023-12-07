import math
import numpy as np

# simulation settings
max_cycles = 50000  # how many times steps the simulation will run for
step = .02  # how much time will advance every cycle
output_file = 'test.csv'  # file name
output_folder = 'test'

# vehicle statistics
mass = 2  # kg
MMI = 0.005  # mass moment of inertia (Kg/m2)
body_ca = 0.005  # cross-sectional area of body (m2)
body_cd = 0.5  # coefficient of drag of body
TGL = 298.15  # temperature at ground level (K)
fin_amount = 4  # fin amount
fin_d_center = 0.065  # m from center (m)
afoil_len = 0.05  # m
afoil_front_width = 0.01  # m
afoil_side_width = 0.05  # m
chute_area = 0.2  # m
chute_deploy_time = 1  # s
chute_cd = 0.8  # coefficient of drag


def airfoil_cd(A2):  # calculate coefficient of drag of the airfoil
    if (A2 == 0):
        return 0
    else:
        A3 = np.rad2deg(abs(A2))
        Result = abs(0.00923899999509634 * A3 ** 0 + 0.00043159972302756 *
        A3 ** 1 + 0.000132734706815724 * A3 ** 2 + -0.000148114605613209 *
        A3 ** 3 + 0.0000439395863143115 * A3 ** 4 + -0.00000408475413644642 *
        A3 ** 5 + -0.000000058028630987062 * A3 ** 6 + 0.0000000234925648145887 *
        A3 ** 7 + -0.00000000012738092984552 * A3 ** 8 + -4.99262938461462E-11 *
        A3 ** 9 + -1.76052490060542E-12 * A3 ** 10 + 1.17822471242556E-13 *
        A3 ** 11 + -1.638626233964E-16 * A3 ** 12 + 1.35169501160575E-17 *
        A3 ** 13 + 3.03085194441072E-17 * A3 ** 14 + -3.83914612541049E-19 *
        A3 ** 15 + -4.02858013082047E-20 * A3 ** 16 + -6.63483675952617E-21 *
        A3 ** 17 + 3.10156981587596E-22 * A3 ** 18)
        return Result * (A2/abs(A2))


def airfoil_cl(A3):  # calculate coefficient of lift of the airfoil
    if (A3 == 0):
        return 0
    else:
        A2 = np.rad2deg(abs(A3))
        Result = 0.000514121378662637 * A2**0 + 0.0140261409761768 * \
        A2**1 + 0.04847878217861 * A2**2 + -0.00818489540656251 * \
        A2**3 + 0.000566436678761745 * A2**4 + -0.0000140727260857348 * A2**5

        return Result * (A3 / abs(A3))

# variables
time = 0  # time in S
altitude = 25000  # meters
velocity = 0  # m/s
mach_num = 0;
acceleration = 0  # m/s2
b_drag = 0  # N, of body
a_drag = 0  # N, of body
atm_density = 0  # Kg/m2
atm_pressure = 0  # pa
air_temp = 0  # K
SoS = 0;
fin_def = math.radians(0)  # degrees°
a_side_area = 0  # airfoil side area (m2)
a_front_area = 0  # airfoil frontal area (m2)
z_angle = 0  # angle in degrees from staring position oon the z axis
z_ang_rate = 0  # z angular rate
z_ang_acc = 0  # angular acceleration on z
z_torque = 0  # angular torque on z
bias = 0;
chute_flag = False


# constants
lease_rate = 0.0098  # rate at which temperature drops (K/m)
AirDens_seaLev = 1.225  # air density at sea level (Kg/m2)
AirPres_seaLev = 101325  # air pressure at sea level (pa)
grav = 9.807  # gravity(m/s2)
Univ_gas_const = 8.3144598
SGCA = 287.05  # specific gas constant of air
AHCR = 1.4  # heat capacity ratio of air
MMA = 0.0289644  # molar mass of air


def tilted_plane_cd(_angle):
    return math.sin(_angle) * 1.40 + 0.12
