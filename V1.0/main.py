import csv
import math
import numpy as np
import serial
import matplotlib.pyplot as plt
from random import random as rnd
from config import *
from nav import *
fieldnames = ['time(s)', 'altitude(m)', 'speed(m/s)', 'acceleration(m/s/s)',
              'body drag(N)', 'airfoil drag(N)', 'atm pressure(Kg/m2)', 'air temp(K)',
              'fin deflection(°)', 'z agnular rate(rad/s)', 'z angle(rad)', 'z torque(N/m2)']


def create_csv(filename):
    with open(filename , mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()


def write_to_csv(filename, _time, _altitude, _speed, _acceleration, A_drag, B_drag, _atm_pressure, _air_temp, _fin_deflection, _z_ang_rate, _z_angle, _z_torque):
    with open(filename, mode='a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writerow(
            {
                'time(s)': _time,
                'altitude(m)': _altitude,
                'speed(m/s)': _speed,
                'acceleration(m/s/s)': _acceleration,
                'airfoil drag(N)': A_drag,
                'body drag(N)': B_drag,
                'atm pressure(Kg/m2)': _atm_pressure,
                'air temp(K)': _air_temp,
                'fin deflection(°)': _fin_deflection,
                'z agnular rate(rad/s)': _z_ang_rate,
                'z angle(rad)': _z_angle,
                'z torque(N/m2)': _z_torque
             })


create_csv(output_file)


def process_forces_moments(m, _mmi, _f, _mo, _pos, _vel, _acc):
    _acc = _f / m
    _vel = _vel + _acc
    _pos = _pos + _vel


