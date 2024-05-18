import csv
import os
import math
import numpy as np
import serial
import matplotlib.pyplot as plt
from random import random as rnd
from simulation_values import *
from navegation import *
fieldnames = ['time(s)', 'altitude(m)', 'speed(m/s)', 'acceleration(m/s/s)',
              'body drag(N)', 'airfoil drag(N)', 'atm pressure(Kg/m2)', 'air temp(K)',
              'fin deflection(°)', 'z agnular rate(rad/s)', 'z angle(rad)', 'z torque(N/m2)', 'mach num']

def create_folder_if_not_exists(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def create_csv(filename, folder):
    create_folder_if_not_exists(folder)
    path = os.path.join(folder, filename)
    with open(path , mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()


def write_to_csv(folder, filename, _time, _altitude, _speed, _acceleration, A_drag, B_drag, _atm_pressure, _air_temp, _fin_deflection, _z_ang_rate, _z_angle, _z_torque, _mach_num):
    path = os.path.join(folder, filename)
    with open(path, mode='a') as csv_file:
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
                'z torque(N/m2)': _z_torque,
                'mach num': _mach_num
             })


create_csv(output_file, output_folder)

max_speed = 0

def sim_cycle():
    global time
    global altitude
    global velocity
    global a_drag
    global b_drag
    global atm_density
    global atm_pressure
    global air_temp
    global a_front_area
    global acceleration
    global a_side_area
    global z_ang_rate
    global z_angle
    global z_torque
    global z_ang_acc
    global max_speed
    global mach_num
    global SoS
    global bias

    time += step

    air_temp = TGL - lease_rate * altitude

    atm_pressure = AirPres_seaLev * pow(1 - ((lease_rate * altitude) / 288.15), (grav * MMA) / (Univ_gas_const * lease_rate))
    atm_density = (atm_pressure * MMA) / (Univ_gas_const * air_temp)

    SoS = math.sqrt(AHCR*(atm_pressure/atm_density))

    b_drag = body_cd * atm_density * velocity * velocity * body_ca

    a_front_area = (math.sin(fin_def) * afoil_side_width + math.cos(fin_def) * afoil_front_width) * afoil_len
    a_drag = .5 * atm_density * velocity * velocity * a_front_area * airfoil_cd(fin_def)

    if altitude < 50:
        p_drag = .5 * atm_density * velocity * velocity * full_chute_area * chute_cd_full
    elif altitude < 100:
        p_drag = .5 * atm_density * velocity * velocity * semi_chute_area * chute_cd_semi
    else:
        p_drag = 0

    acceleration = -grav + (b_drag + a_drag + p_drag) / mass
    altitude = altitude + velocity * step + 0.5 * acceleration * step * step
    velocity = velocity + acceleration * step
    mach_num = velocity/SoS

    a_side_area = math.cos(abs(fin_def)) * afoil_len * afoil_side_width

    fin_tan_vel = z_ang_rate * fin_d_center

    fin_wind_direction = math.atan(fin_tan_vel/velocity)

    pow_vel = pow(velocity, 2)
    pow_tan_vel = pow(fin_tan_vel, 2)

    fin_wind_speed = math.sqrt(pow_vel + pow_tan_vel)

    fin_aoa = fin_def-fin_wind_direction
    z_lift_torque = airfoil_cl(fin_aoa) * afoil_len * afoil_side_width * ((atm_density * pow(fin_wind_speed, 2)) / 2) * fin_amount * fin_d_center

    z_drag_torque = (tilted_plane_cd(fin_def) * a_side_area * ((atm_density * pow(fin_tan_vel, 2)) / 2)) * fin_amount * fin_d_center

    bias = bias + (rnd() - 0.5) * velocity / 200 * step

    z_torque = z_lift_torque + z_drag_torque + bias
    z_ang_acc = z_torque / MMI
    z_angle = z_angle + z_ang_rate * step + 0.5 * z_ang_acc * step * step
    z_ang_rate = z_ang_rate + (z_ang_acc * step)

    if max_speed < abs(velocity):
        max_speed = abs(velocity)

# coms.write()
le = 0
ie = 0
while time/step < max_cycles and altitude > 0:
    # packet = coms.read().decode().strip().split(",")
    # fin_def = packet[0]
    # chute_flag = packet[1]
    ie = ie + z_ang_rate
    control = (PID(0.25, 0.01, 0.6, z_ang_rate/200, le, ie, step))/((velocity**2+0.00000001))
    fin_def = sorted([-0.2, control, 0.2])[1]
    fin_def = fin_def
    sim_cycle()
    packet = [acceleration, z_ang_rate, atm_pressure]
    write_to_csv(output_folder, output_file, time, altitude, velocity, acceleration, a_drag, b_drag, atm_pressure, air_temp, fin_def, z_ang_rate, z_angle, z_torque, mach_num)
    le = z_ang_rate

# coms.close()
print("max speed: " + str(max_speed))
print("flight time: " + str(time))
print("simulation cycles: " + str(round(time/step)))



