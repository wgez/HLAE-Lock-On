# What this program does:
# Builds a campath where a stationary camera will automatically turn to face your player model.
# 1) Paste your desired stationary cam position (x, y, z) at the bottom. (get into position and use "mirv_input position")
# 2) Provide your input campath file location (these are the points to rotate towards, spam points while in firstperson)
# 3) Provide the name you'd like your output campath file to be saved as (it will be auto-generated).
# NOTE: This program may break if not in the same format produced by HLAE.

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
    # Given a campath point line, extract and store its data.
    for i in range(1, 6): # Read (t, x, y, z, fov) only.
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
    with open(INPUT_FILEPATH) as f:
        lines = f.readlines()

    # Consider campath points only.
    for data_line in lines:
        data = data_line.split()
        if data and data[0] == "<p":
            readDataAndStore(data)
    
def generateOutput():
    # Output xml campath file.
    f = open(OUTPUT_FILEPATH, "w")
    f.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
    f.write("<campath>\n")
    f.write("\t<points>\n")
    f.write("\t\t<!--Points are in Quake coordinates, meaning x=forward, y=left, z=up and rotation order is first rx, then ry and lastly rz.\n")
    f.write("Rotation direction follows the right-hand grip rule.\n")
    f.write("rx (roll), ry (pitch), rz(yaw) are the Euler angles in degrees.\n")
    f.write("qw, qx, qy, qz are the quaternion values.\n")
    f.write("When read it is sufficient that either rx, ry, rz OR qw, qx, qy, qz are present.\n")
    f.write("If both are present then qw, qx, qy, qz take precedence.-->\n")
    for i in range(0, len(time_new)):
        f.write(f'\t\t<p t=\"{time_new[i]:.6f}\" x=\"{x_new[i]:.6f}\" y=\"{y_new[i]:.6f}\" z=\"{z_new[i]:.6f}\" fov=\"{fov_new[i]:.6f}\" rx=\"{rx_new[i]:.6f}\" ry=\"{ry_new[i]:.6f}\" rz=\"{rz_new[i]:.6f}\"/>\n')
    f.write("\t</points>\n")
    f.write("</campath>\n")
    f.close()

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
    r_solutions = {} # Hashmap solutions for reuse. Format: (x1, y1, z1) => (rx, ry, rz)
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

        try: # 0. If a point is repeated, reuse answer found from earlier.
            rx, ry, rz = r_solutions[(x1, y1, z1)]
        except KeyError:
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

            # 5. Calculate euler angles, store solutions for reuse.
            r = R.from_matrix(rot_matrix)
            e_angles = r.as_euler('xyz', degrees=True)
            rx = e_angles[0]
            ry = e_angles[1]
            rz = e_angles[2]
            r_solutions[(x1, y1, z1)] = (rx, ry, rz)

        # 6. Populate output data.
        appendData(t, x0, y0, z0, fov, rx, ry, rz)

def main():
    populateInput()
    calculateRotation()
    generateOutput()

##########################################################
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
cam_position_input = "0.000000 0.000000 0.000000" # your chosen stationary cam position (use "mirv_input position")
directory_path = "C:/Program Files (x86)/Steam/steamapps/common/Team Fortress 2/tf/campath/"
input_filename = "gorgealone_pulsev1" # the data points to rotate towards
output_filename = "yourOutputCampathFilename" # chosen output campath file name (will auto-generate one for you)

#################################################
INPUT_FILEPATH = f"{directory_path}{input_filename}"
OUTPUT_FILEPATH = f"{directory_path}{output_filename}"
cam_position = [float(x) for x in cam_position_input.split()]
main()