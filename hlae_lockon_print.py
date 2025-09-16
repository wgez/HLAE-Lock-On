# What this program does:
# Build a campath where a stationary camera will automatically turn to face your player model.
# 1) Provide your desired stationary cam position x0, y0, z0 (at bottom)
# 2) Provide your campath file contents (the points to rotate towards)
# 3) Copy/Paste this entire code file into this website: https://www.w3schools.com/python/trypython.asp?filename=demo_default
# 4) Click the "Run" button, then copy/paste the output to a new campath file (make a copy of your old campath file and use that).

import io
import numpy as np
from scipy.spatial.transform import Rotation as R

def storeDataInput(data_point, data_type):
    if data_type == 1:
        time_orig.append(data_point)
    if data_type == 2:
        x_orig.append(data_point)
    if data_type == 3:
        y_orig.append(data_point)
    if data_type == 4:
        z_orig.append(data_point)
    if data_type == 5:
        fov_orig.append(data_point)

def readDataAndStore(data_points):
    # For only the relevant data points, store the data in between the quotes ("").
    for i in range(1, 6): # Read data points t -> z.
        current_point = data_points[i]
        extraction = ""
        for j in range(len(current_point)):
            current_char = current_point[j]
            if current_char == "\"": # Extract what's between quotes ("").
                for c in current_point[j + 1:len(current_point)]:
                    if c == "\"":
                        break
                    else:
                        extraction = extraction + c
                storeDataInput(float(extraction), i)
                break

def populateInput():
    # Read input data.
    f = io.StringIO(campath)
    lines = f.readlines()

    # Formula to look at lines with campath points only: lines[9:len(lines)-3]
    for data_line in lines[9:len(lines)-3]:
        data_points = data_line.split()
        readDataAndStore(data_points)
    
def generateOutput():
    # Output xml campath file.
    print("<?xml version=\"1.0\" encoding=\"utf-8\"?>")
    print("<campath>")
    print("\t<points>")
    print("\t\t<!--Points are in Quake coordinates, meaning x=forward, y=left, z=up and rotation order is first rx, then ry and lastly rz.")
    print("Rotation direction follows the right-hand grip rule.")
    print("rx (roll), ry (pitch), rz(yaw) are the Euler angles in degrees.")
    print("qw, qx, qy, qz are the quaternion values.")
    print("When read it is sufficient that either rx, ry, rz OR qw, qx, qy, qz are present.")
    print("If both are present then qw, qx, qy, qz take precedence.-->")
    for i in range(0, len(time_new)):
        print(f'\t\t<p t=\"{time_new[i]:.6f}\" x=\"{x_new[i]:.6f}\" y=\"{y_new[i]:.6f}\" z=\"{z_new[i]:.6f}\" fov=\"{fov_new[i]:.6f}\" rx=\"{rx_new[i]:.6f}\" ry=\"{ry_new[i]:.6f}\" rz=\"{rz_new[i]:.6f}\"/>')
    print("\t</points>")
    print("</campath>")

def appendData(t, x, y, z, fov, rx, ry, rz):
    time_new.append(t)
    x_new.append(x)
    y_new.append(y)
    z_new.append(z)
    fov_new.append(fov)
    rx_new.append(rx)
    ry_new.append(ry)
    rz_new.append(rz)

def calculateRotation():
    for i in range(0, len(time_orig)):
        t = time_orig[i]
        x0 = cam_position[0]
        y0 = cam_position[1]
        z0 = cam_position[2]
        fov = fov_orig[i]
        x1 = x_orig[i]
        y1 = y_orig[i]
        z1 = z_orig[i]
        camera_pos = np.array([x0, y0, z0])
        target_pos = np.array([x1, y1, z1])

        # 1. Calculate "forward" vector.
        f_vec = target_pos - camera_pos
        f_norm = np.linalg.norm(f_vec)
        if f_norm == 0: # cam position = target position (no rotation)
            rx = ry = rz = 0.0
            appendData(t, x0, y0, z0, fov, rx, ry, rz)
            continue
        f_vec /= f_norm

        # 2. Calculate "right" vector.
        u_unit_vec = np.array([0.0, 0.0, 1.0])
        r_vec = np.cross(u_unit_vec, f_vec)
        if np.linalg.norm(r_vec) < 1e-6:  # Forward parallel to up
            r_vec = np.array([0.0, 1.0, 0.0]) 
        else:
            r_vec /= np.linalg.norm(r_vec)

        # 3. Calculate "up" vector.
        u_vec = np.cross(f_vec, r_vec)

        # 4. Construct rotation matrix (note: adjusted for Source axes).
        rot_matrix = np.column_stack((f_vec, r_vec, u_vec))

        # 5. Calculate euler angles.
        r = R.from_matrix(rot_matrix)
        e_angles = r.as_euler('xyz', degrees=True)
        rx = e_angles[0]
        ry = e_angles[1]
        rz = e_angles[2]

        # 6. Populate output data.
        appendData(t, x0, y0, z0, fov, rx, ry, rz)

def main():
    populateInput()
    calculateRotation()
    generateOutput()

#################################################
time_orig = []
x_orig = []
y_orig = []
z_orig = []
fov_orig = []
time_new = []
x_new = []
y_new = []
z_new = []
fov_new = []
rx_new = []
ry_new = []
rz_new = []

############## SUPPLY THESE INPUTS ##############
cam_position = [100.0, -100.0, 100.0] # chosen stationary cam position
campath = '''

*** COPY/PASTE YOUR ENTIRE CAMPATH FILE HERE ***

'''
main()