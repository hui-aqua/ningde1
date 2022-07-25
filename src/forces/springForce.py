import numpy as np
spring_stiffness = 1e6  # unit [N/m] a.k.a -> K
sprint_unit_vector=0
spring_index=[]

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
        If the spring is compressed, che force is negetive, otherwise, is positive

    Args:
        spring_deformation (vector): the deformation of a list of spring. Unit m.
        spring_stiffness (float): the stiffness of a spring, unit n/m

    Returns:
        vector: the force on the springs
    """
    # no compression force
    spring_deformation[spring_deformation<0]*=0
    
    tension=spring_deformation*spring_stiffness
    
    return tension

def map_sprint_force(points_position, force_on_spring):
    """calculate the acceleration of each points

    Args:
        points_position (matirx): a nx2 matrix, n is the number of point, 2 is due to 2 dimential simulation
        spring_indexs (matrix): a mx2 matrix, m is the number of spring, 2 is due to 2 dimential simulation
        force_on_spring (matrix): a mx2 matrix, m is the number of spring, 2 is due to 2 dimential simulation

    Returns:
        matrix: a nx2 matrix
    """
    # spring forces on the points of first column of spring index
    force1 = -sprint_unit_vector*force_on_spring.reshape(len(force_on_spring), 1)
    force2 = sprint_unit_vector*force_on_spring.reshape(len(force_on_spring), 1)
    
    big_ma = np.zeros((len(points_position), len(points_position), 3))

    for index, item in enumerate(spring_index):
        big_ma[item[0]][item[1]] = force1[index]
        big_ma[item[1]][item[0]] = force2[index]

    acceleration = np.sum(big_ma, axis=1) 

    return acceleration

