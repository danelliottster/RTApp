import numpy as np
import math

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

def create_rigid_reg_mat( xyz_rot , xyz_transl ):

    rot_mat = compose_rotations( xyz_rot[0] , xyz_rot[1] , xyz_rot[2] , "xyz")
    transf_mat = np.copy(rot_mat)
    add_translation(xyz_transl[0] , xyz_transl[1] , xyz_transl[2] , transf_mat)

    return transf_mat
