from matplotlib.pyplot import axes
import numpy as np

dwh = 0
dw0 = 0
quad_unit_vector = 0  # point out side the fish cage
quad_center = 0
quad_index = []
number_of_point=0
sn = 0.25
row_water = 1000.0
current_velocity = 0
kinematic_viscosity = 1.004e-6  # when the water temperature is 20 degree.
dynamic_viscosity = 1.002e-3  # when the water temperature is 20 degree.


def __cal_area(point_position: np.array):
    """ we assume the quad is numbered as [1,2,3,4]:
        0-------2
        |       |
        |       |
        1-------3

    Args:
        point_position (np.array): _description_
    """
    global quad_unit_vector
    __quad_index = np.array(quad_index)

    vector1 = point_position[__quad_index[:, 1]] - \
        point_position[__quad_index[:, 0]]
    vector2 = point_position[__quad_index[:, 2]] - \
        point_position[__quad_index[:, 1]]

    vector_n = np.cross(vector1, vector2, axis=1)

    quad_area = np.linalg.norm(vector_n, axis=1)
    quad_unit_vector = vector_n/quad_area.reshape(len(vector_n), -1)
    return quad_area


def __cal_quad_center(position: np.array):
    global quad_center
    __quad_index = np.array(quad_index)
    quad_center =0.25*(position[__quad_index[:, 0]]+position[__quad_index[:, 1]]+position[__quad_index[:, 3]]+position[__quad_index[:, 4]])
    

def __cal_wake_factor(point_position,cd,u):
    __cal_quad_center(point_position)
    center=np.mean(point_position,axis=0)
    vectorp=quad_center-center
    # filter=
    
    r=1-0.46*cd

def __cal_force_coe(theta):
    cd = 0.04 + (-0.04 + sn - 1.24 * pow(sn, 2) +13.7 * pow(sn, 3)) * np.cos(theta)
    cl = (0.57 * sn - 3.54 * pow(sn, 2) + 10.1 * pow(sn, 3)) * np.sin(2 * theta)
    return cd, cl

def cal_dynamic_force(point_position,u):
    if len(u) == 3:
        uc = np.ones((len(quad_index), 3))*u
    elif len(u) == len(quad_index):
        uc = u
    else:
        print("The given U does match element", u)
        
    uc_mag=np.linalg.norm(uc, axis=1).reshape(len(uc), -1)
    ## dot do not have axis
    theta = np.arccos(abs(np.dot(quad_unit_vector, uc, axis=1))) / uc_mag
    quad_area=__cal_area(point_position)
    
    cd,cl=__cal_force_coe(theta)
    
    
    drag_e=uc/uc_mag
    lift_e=np.cross(np.cross(drag_e,quad_unit_vector,axis=1),axis=1)
    
    
    fd=0.5*row_water*quad_area*cd*pow(uc_mag,2)*drag_e
    fl=0.5*row_water*quad_area*cl*pow(uc_mag,2)*lift_e
    
    return fd+fl




def map_force(force_on_quad):
    force_on_point=np.zeros((number_of_point,3))
    __quad_index=np.array(quad_index)
    for i in range(4):
        force_on_point[__quad_index[:,i]]+=force_on_quad*0.25
        
    return force_on_point
