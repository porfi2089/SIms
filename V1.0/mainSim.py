import csv
from scipy.spatial.transform import Rotation as R
import numpy as np
import matplotlib.pyplot as plt
from random import random as rnd
from config import *
from nav import *
import piphy as ph

fieldnames = ['time', 'posx', 'posy', 'posz', 'velx', 'vely', 'velz', 'accx', 'accy', 'accz', 'rotx', 'roty', 'rotz', 'rot_accx', 'rot_accy', 'rot_accz', 'rot_velx', 'rot_vely', 'rot_velz']


def create_csv(filename):
    with open(filename , mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

def write_to_csv(filename: str, _time: float, _pos: np.ndarray, _vel: np.ndarray, _acc: np.ndarray, _rot: np.ndarray, _rot_acc: np.ndarray, _rot_vel: np.ndarray):
    with open(filename, mode='a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writerow({
                'time': _time,
                'posx': _pos[0],
                'posy': _pos[1],
                'posz': _pos[2],
                'velx': _vel[0],
                'vely': _vel[1],
                'velz': _vel[2],
                'accx': _acc[0],
                'accy': _acc[1],
                'accz': _acc[2],
                'rotx': _rot[0],
                'roty': _rot[1],
                'rotz': _rot[2],
                'rot_accx': _rot_acc[0],
                'rot_accy': _rot_acc[1],
                'rot_accz': _rot_acc[2],
                'rot_velx': _rot_vel[0],
                'rot_vely': _rot_vel[1],
                'rot_velz': _rot_vel[2]
             })

def processAcc(pos: np.ndarray, vel: np.ndarray, acc: np.ndarray) -> np.ndarray:
    vel = vel + acc
    pos = pos + vel
    return np.array([pos, vel])

def forceToAcc(Wforces: np.ndarray, mas: float) -> np.ndarray:
    return Wforces / mass

def torqueFromForce(force: ph.Force) -> np.ndarray:
    _trq = np.zeros((1,3))
    mag = force.mag
    Lpos = force.Lpos

    _trq[0] = Lpos[1]*mag[2] - Lpos[2]*mag[1]
    _trq[1] = Lpos[0]*mag[2] - Lpos[2]*mag[0]
    _trq[2] = Lpos[1]*mag[0] - Lpos[0]*mag[1]

    return _trq

def globalizeForces(forces:np.ndarray[ph.Force], _rotmat: R) -> np.ndarray[ph.Force]:
    """globalizes forces to the world frame.\n Taking in the rotation matrix of the object and he forces that are to be rotated"""
    _Wforces = np.array([])
    for F in forces:
        F.mag = F.mag * _rotmat
        _Wforces.append(F)
    return _Wforces

def combineLinealForces(_forces: np.ndarray[ph.Force]) -> ph.Force:
    """combines multiple forces into one"""
    tot_forces = np.zeros((1,3))
    for f in _forces:
        tot_forces += f.mag
    
    return ph.Force(tot_forces)

def getTotTorque(_forces: np.ndarray[ph.Force]) -> np.ndarray[float]:
    tot_trq = np.zeros((1,3))
    for f in _forces:
        tot_trq += torqueFromForce()
    return tot_trq

def getEnviroment(TGL: float, alt:float) -> np.ndarray[float, float, float, float]:
    '''calculates the enviroment of the object'''
    air_temp = TGL - 0.0098 * alt
    atm_pressure = 101325 * pow(1 - ((0.0098 * alt) / 288.15), (9.807 * 0.0289644) / (8.3144598 * 0.0098))
    atm_density = (atm_pressure * 0.0289644) / (8.3144598 * air_temp)
    SoS = math.sqrt(1.4*(atm_pressure/atm_density))
    return np.array([air_temp, atm_pressure, atm_density, SoS])

pos = np.zeros((1,3))
vel = np.zeros((1,3))
acc = np.zeros((1,3))
ang = R.from_euler('XYZ', [0,0,0], degrees=True)
ang_vel = np.zeros((1,3))
ang_acc = np.zeros((1,3))
forces:np.ndarray[ph.Force]

def Cycle():
    global time
    global forces
    global pos
    global vel
    global acc
    global ang
    time += step

    # get enviroment
    air_temp, atm_pressure, atm_density, SoS = getEnviroment(TGL, pos[2])

    # get forces
    

    # get torques
    torque = getTotTorque(forces)
    ang_acc = torque / MMI
    ang_vel = ang_vel + ang_acc
    ang = ang * R.from_euler('XYZ', ang_vel, degrees=True)

    # globalize forces
    rotmat = ang.as_matrix()
    Wforces = globalizeForces(forces, rotmat)

    # final 
    acc = forceToAcc(Wforces, mass)
    pos, vel = processAcc(pos, vel, acc)


