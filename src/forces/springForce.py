import numpy as np



def calc_spring_length(points_position, spring_indexs):
    return np.linalg.norm(points_position[spring_indexs[:, 0]]-points_position[spring_indexs[:, 1]], axis=1)



def calc_spring_force(spring_deformation, spring_stiffness):
    """ calculate the force on spring.\n
        If the spring is compressed, che force is negetive, otherwise, is positive

    Args:
        spring_deformation (vector): the deformation of a list of spring. Unit m.
        spring_stiffness (float): the stiffness of a spring, unit n/m

    Returns:
        vector: the force on the springs
    """
    return spring_deformation*spring_stiffness