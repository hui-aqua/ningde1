import numpy as np
spring_stiffness = 1e6  # unit [N/m] a.k.a -> K
sprint_unit_vector=0
spring_index=[]
number_of_point=0
dwh=0
dw0=0
row_water=1000.0
current_velocity=0  
kinematic_viscosity = 1.004e-6  # when the water temperature is 20 degree.
dynamic_viscosity = 1.002e-3  # when the water temperature is 20 degree.

def calc_spring_length(points_position:list):
    global sprint_unit_vector
    points_position=np.array(points_position)
    __spring_index=np.array(spring_index)
    spring_vector=points_position[__spring_index[:, 0]]-points_position[__spring_index[:, 1]]
    sprint_length=np.linalg.norm(spring_vector, axis=1)
    sprint_unit_vector=spring_vector/sprint_length.reshape(len(sprint_length), 1)
    return sprint_length



def calc_spring_force(spring_deformation):
    """ calculate the force on spring.\n
        If the spring is compressed, che force is negative, otherwise, is positive

    Args:
        spring_deformation (vector): the deformation of a list of spring. Unit m.
        spring_stiffness (float): the stiffness of a spring, unit n/m

    Returns:
        vector: the force on the springs
    """
    # no compression force
    spring_deformation[spring_deformation<0]*=0.0
    
    tension=spring_deformation*spring_stiffness
    
    return tension

def map_force(force_on_spring):
    """calculate the acceleration of each points

    Args:
        points_position (matirx): a nx2 matrix, n is the number of point, 2 is due to 2 dimential simulation
        force_on_spring (matrix): a mx2 matrix, m is the number of spring, 2 is due to 2 dimential simulation

    Returns:
        matrix: a nx2 matrix
    """
    # spring forces on the points of first column of spring index
    num_of_line=len(force_on_spring)
    force1 = -sprint_unit_vector*force_on_spring.reshape(num_of_line, 1)
    force2 =  sprint_unit_vector*force_on_spring.reshape(num_of_line, 1)

    force_on_point=np.zeros((number_of_point,3))
    __spring_index=np.array(spring_index)
    ## todo need to make the 1152 as variable, 
    # hint: number of horizontal lines and vertical lines need to be separate.
    force_on_point[__spring_index[:1152,0]]+=force1[:1152]
    force_on_point[__spring_index[:1152,1]]+=force2[:1152]
    force_on_point[__spring_index[1152:,0]]+=force1[1152:]
    force_on_point[__spring_index[1152:,1]]+=force2[1152:]

    return force_on_point

def __calculate_coe(uc:np.array):
    reynolds_number = row_water * dw0 * np.linalg.norm(uc) / dynamic_viscosity
    drag_tangent = np.pi * dynamic_viscosity * (
                    0.55 * np.sqrt(reynolds_number) + 0.084 * pow(reynolds_number, 2.0 / 3.0))
    s = -0.07721565 + np.log(8.0 / reynolds_number)
    if 0 < reynolds_number < 1:
        drag_normal = 8 * np.pi * \
            (1 - 0.87 * pow(s, -2)) / (s * reynolds_number)
    elif reynolds_number < 30:
        drag_normal = 1.45 + 8.55 * pow(reynolds_number, -0.9)
    elif reynolds_number < 2.33e5:
        drag_normal = 1.1 + 4 * pow(reynolds_number, -0.5)
    elif reynolds_number < 4.92e5:
        drag_normal = (-3.41e-6) * (reynolds_number - 5.78e5)
    elif reynolds_number < 1e7:
        drag_normal = 0.401 * \
            (1 - np.exp(-reynolds_number / 5.99 * 1e5))
    else:
        print("Reynold number=" + str(reynolds_number) +
              ", and it exceeds the range.")
        print("Now, current_velocity is " + str(uc))
        print("Now, norm of current_velocity is " +
              str(np.linalg.norm(uc)))
        exit()
    return drag_normal, drag_tangent

def __calculate_dynamic_force(sprint_length:np.array,uc:np.array):
    """calculate the hydrodynamic forces on line element based on Morison model

    Args:
        sprint_length (np.array): list of the length of line element (M,1) 
        uc (np.array): fluid velocity at the element centroid (M,3) 
    """
    
    cn,ct=__calculate_coe(uc)
    # todo check the un ut
    un=sprint_unit_vector*uc*sprint_unit_vector
    ut=sprint_unit_vector*uc*sprint_unit_vector
    
    ft=0.5*ct*row_water*dwh*sprint_length*ut*np.linalg.norm(ut,axis=1)
    fn=0.5*cn*row_water*dwh*sprint_length*un*np.linalg.norm(un,axis=1)
    
    return ft+fn