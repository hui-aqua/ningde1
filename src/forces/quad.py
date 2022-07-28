from matplotlib.pyplot import axes
import numpy as np


quad_unit_vector = 0  # point out side the fish cage
quad_center = 0
quad_index = []
number_of_point = 0
number_of_quad=0
sn = 0.25
row_water = 1000.0


def map_velocity(u):
    if len(u) == 3:
        uc = np.ones((number_of_quad, 3))*u
    elif len(u) == len(number_of_quad):
        uc = u
    else:
        print("The given U does match element", u)
    return uc
 

def __cal_area(point_position: np.array):
    """ we assume the quad is numbered as [0,1,2,3]:
        0-------2
        |       |
        |       |
        1-------3

    Args:
        point_position (np.array): _description_
    """
    global quad_unit_vector
    __quad_index = np.array(quad_index)

    vector1 = point_position[__quad_index[:, 1]] - point_position[__quad_index[:, 0]]
    vector2 = point_position[__quad_index[:, 2]] - point_position[__quad_index[:, 1]]

    vector_n = np.cross(vector1, vector2, axis=1)

    quad_area = np.linalg.norm(vector_n, axis=1)
    quad_unit_vector = vector_n/quad_area.reshape(number_of_quad, -1)
    return quad_area.reshape(number_of_quad, -1)


def __cal_quad_center(position: np.array):
    global quad_center
    __quad_index = np.array(quad_index)
    quad_center = 0.25*(position[__quad_index[:, 0]] +
                        position[__quad_index[:, 1]] +
                        position[__quad_index[:, 2]] +
                        position[__quad_index[:, 3]])


def __cal_wake_factor(point_position, cd, u):
    __cal_quad_center(point_position)
    net_center = np.mean(point_position, axis=0)
    vector_cp = quad_center-net_center
    filter = np.diagonal(vector_cp@u.T) > 0
    reduction_factor = np.ones(number_of_quad)
    r = 1-0.46*np.max(cd)
    reduction_factor[filter] *= r
    return reduction_factor.reshape(number_of_quad,-1)


def __cal_force_coe(theta):
    cd = 0.04 + (-0.04 + sn - 1.24 * pow(sn, 2) + 13.7 * pow(sn, 3)) * np.cos(theta)
    cl = (0.57 * sn - 3.54 * pow(sn, 2) + 10.1 * pow(sn, 3)) * np.sin(2 * theta)
    return cd, cl


def cal_dynamic_force(point_position, uc):


    uc_mag = np.linalg.norm(uc, axis=1).reshape(number_of_quad, -1)
    # dot product in numpy do not have axis

    quad_area = __cal_area(point_position)
    # print(abs(np.diagonal(quad_unit_vector@uc.T)) .shape)
    # print(uc_mag.shape)
    theta = np.arccos(abs(np.diagonal(quad_unit_vector@uc.T)).reshape(number_of_quad, -1) / uc_mag)
    
    cd, cl = __cal_force_coe(theta)

    ru = __cal_wake_factor(point_position, cd, uc)

    drag_e = uc/uc_mag
 
    lift_e = np.cross(np.cross(drag_e, quad_unit_vector, axis=1),drag_e,axis=1)

    fd = 0.5*row_water*quad_area*cd*pow(uc_mag, 2)*drag_e*ru
    fl = 0.5*row_water*quad_area*cl*pow(uc_mag, 2)*lift_e*ru

    return fd+fl


def map_force(force_on_quad):
    force_on_point = np.zeros((number_of_point, 3))
    __quad_index = np.array(quad_index)

    for i in range(4):
        force_on_point[__quad_index[:, i]] += force_on_quad*0.25

    return force_on_point
