import numpy as np


def ground(x):
    """ The ground is a function of x

    Args:
        x (float):The x position of a point

    Returns:
        float: The height of the ground in y direction.
    """
    # return 0*x
    return np.sin(x/2)


def ground_force(state_y, k, m_vector):
    """calculate the vertical force on each point.

    Args:
        state_y (vector): the relative distance to the ground for a list of point
        k (float): the stiffness of the ground.
        m_vector (vector): the mass of a list of point

    Returns:
        vector: the reaction force due to the hit on the ground
    """
    df = -2*k*state_y/m_vector
    df[state_y > 0] = 0
    return df


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


def calc_point_acceleration(points_position, spring_indexs, force_on_spring, m_vector):
    """calculate the acceleration of each points

    Args:
        points_position (matirx): a nx2 matrix, n is the number of point, 2 is due to 2 dimential simulation
        spring_indexs (matrix): a mx2 matrix, m is the number of spring, 2 is due to 2 dimential simulation
        force_on_spring (matrix): a mx2 matrix, m is the number of spring, 2 is due to 2 dimential simulation
        m_vector (vector): the mass of a list of point.

    Returns:
        matrix: a nx2 matrix
    """
    spring_length = calc_spring_length(points_position, spring_indexs)
    unit_vector = (points_position[spring_indexs[:, 0]] -
                   points_position[spring_indexs[:, 1]])/spring_length.reshape(len(spring_length), 1)
    # spring forces on the points of first column of spring index
    force1 = -unit_vector*force_on_spring.reshape(len(force_on_spring), 1)
    force2 = unit_vector*force_on_spring.reshape(len(force_on_spring), 1)
    big_ma = np.zeros((len(points_position), len(points_position), 2))

    for index, item in enumerate(spring_indexs.tolist()):
        big_ma[item[0]][item[1]] = force1[index]
        big_ma[item[1]][item[0]] = force2[index]

    acceleration = np.sum(big_ma, axis=1) / m_vector.reshape(len(m_vector), 1)

    return acceleration
