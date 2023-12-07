import csv

import math

from simulation_values import *

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

while time/step < max_cycles and altitude > 0:
    time = time + step

    air_temp = TGL - lease_rate * altitude

    atm_pressure = AirPres_seaLev * pow(grav / (grav + (altitude - 0)* lease_rate), 1 + grav * MMEG / Univ_gas_const * lease_rate)

    b_drag = 1/2*atm_pressure * pow(velocity, 2) * body_ca * body_cd

    a_front_area = (math.sin(fin_def*0.0174533)*afoil_side_width + math.cos(fin_def*0.0174533)*afoil_front_width)*afoil_len
    a_drag = 1 / 2 * atm_pressure * pow(velocity, 2) * a_front_area * airfoil_cd(fin_def)

    acceleration = grav + (b_drag + a_drag) / mass
    altitude = altitude + velocity * step + 0.5 * acceleration * step * step
    velocity = velocity + acceleration * step

    a_side_area = math.cos(fin_def * 0.0174533) * afoil_len * afoil_side_width

    fin_tan_vel = z_ang_rate * fin_d_center

    fin_air_speed = math.sqrt(pow(fin_tan_vel, 2) + pow(velocity, 2))

    fin_air_dir = math.atan(fin_tan_vel/velocity)

    z_lift_torque = airfoil_cl(fin_def - fin_air_dir) * afoil_len * afoil_side_width * ((atm_pressure * pow(fin_air_speed, 2))/ 2) * fin_amount * fin_d_center

    z_drag_torque = (tilted_plane_cd(fin_def) * a_side_area *
                     ((atm_pressure * pow(fin_tan_vel, 2)) / 2)) * fin_amount * fin_d_center

    z_torque = z_lift_torque - z_drag_torque
    z_ang_acc = z_torque * 9.81 / MMI
    z_ang_rate = z_ang_rate + z_ang_acc * step
    z_angle = z_angle + z_ang_rate * step

    write_to_csv(output_file, time, altitude, velocity, acceleration, a_drag, b_drag, atm_pressure, air_temp, fin_def, z_ang_rate, z_angle, z_torque)

