import numpy as np

# Define the initial Euler angles in degrees
initial_angles_deg = np.array([10, 20, 30])  # Example initial Euler angles (in degrees)

# Convert degrees to radians
initial_angles_rad = np.deg2rad(initial_angles_deg)

# Define the rotation angles in degrees
rotation_angles_deg = np.array([90, 0, 0])  # Example rotation angles (in degrees)

# Convert degrees to radians
rotation_angles_rad = np.deg2rad(rotation_angles_deg)

# Create the rotation matrices
rotation_matrix_x = np.array([
    [1, 0, 0],
    [0, np.cos(rotation_angles_rad[0]), -np.sin(rotation_angles_rad[0])],
    [0, np.sin(rotation_angles_rad[0]), np.cos(rotation_angles_rad[0])]
])

rotation_matrix_y = np.array([
    [np.cos(rotation_angles_rad[1]), 0, np.sin(rotation_angles_rad[1])],
    [0, 1, 0],
    [-np.sin(rotation_angles_rad[1]), 0, np.cos(rotation_angles_rad[1])]
])

rotation_matrix_z = np.array([
    [np.cos(rotation_angles_rad[2]), -np.sin(rotation_angles_rad[2]), 0],
    [np.sin(rotation_angles_rad[2]), np.cos(rotation_angles_rad[2]), 0],
    [0, 0, 1]
])

# Apply the rotations successively
rotated_angles_rad = np.dot(rotation_matrix_z, np.dot(rotation_matrix_y, np.dot(rotation_matrix_x, initial_angles_rad)))

# Convert radians to degrees
rotated_angles_deg = np.rad2deg(rotated_angles_rad)

# Print the rotated Euler angles in degrees
print(rotated_angles_deg)
