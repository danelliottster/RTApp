import numpy as np
import math

def mm_from_idx(row_idx, col_idx, slice_idx, start_pos, vox_sz):
    return ( start_pos[0] + row_idx * vox_sz[0] ,
             start_pos[1] + col_idx * vox_sz[1] ,
             start_pos[2] + slice_idx * vox_sz[2] )

def find_closest_slice(pos_mm , slice_start_mm , slice_thicknes_mm , num_slices):
    if (pos_mm > compute_voxel_pos(slice_start_mm , slice_thicknes_mm , num_slices) + slice_thicknes_mm) or (pos_mm < slice_start_mm - slice_thicknes_mm):
        return -1
    else:
        slice_positions = np.arange(slice_start_mm ,
                                    slice_start_mm + slice_thicknes_mm * num_slices ,
                                    step = slice_thicknes_mm)
        return np.argmin(np.abs(slice_positions - pos_mm))

def compute_voxel_pos(start , size , index):
    return start + size * index

def add_translation(xtransl , ytransl , ztransl , transf_mat):
    transf_mat[0,3] = xtransl
    transf_mat[1,3] = ytransl
    transf_mat[2,3] = ztransl
    transf_mat[3,3] = 1.0

def build_x_rot_mat(deg):
    x_ang = math.radians(deg)
    return np.array([[1 , 0 , 0 , 0],
                     [0 , math.cos(x_ang) , -math.sin(x_ang) , 0],
                     [0 , math.sin(x_ang) , math.cos(x_ang) , 0],
                     [0 , 0 , 0 , 1]])

def build_y_rot_mat(deg):
    y_ang = math.radians(deg)
    return np.array([[math.cos(y_ang) , 0 , -math.sin(y_ang) , 0],
                     [0 , 1 , 0 , 0],
                     [math.sin(y_ang) , 0 , math.cos(y_ang) , 0],
                     [0 , 0 , 0 , 1]])

def build_z_rot_mat(deg):
    z_ang = math.radians(deg)
    return np.array([[math.cos(z_ang) , -math.sin(z_ang) , 0 , 0],
                     [math.sin(z_ang) , math.cos(z_ang) , 0 , 0],
                     [0 , 0 , 1 , 0],
                     [0 , 0 , 0 , 1]])

def compose_rotations(x_rot , y_rot , z_rot , rot_order):
    rot_mats = {"x" : build_x_rot_mat(x_rot) , 
                "y" : build_y_rot_mat(y_rot) ,
                "z" : build_z_rot_mat(z_rot) }
    return np.dot( rot_mats[rot_order[2]] , np.dot(rot_mats[rot_order[1]] , rot_mats[rot_order[0]]))

# determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs.
def point_inside_polygon(xy,poly):
    x = xy[0]; y = xy[1];
    n = len(poly)
    inside =False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y
    return inside
