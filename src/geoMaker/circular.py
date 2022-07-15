"""
Author: Dr. Hui CHeng
Any questions about this code,
please email: hui.cheng@uis.no \n

"""
# For a circular type fish cage, top fixed and no bottom ring and net.

import numpy as np

cr_top=1.75/2.0   #[m]
cage_height=1.5   #[m]
NT=15
NN=5


def gen_points():
    point_one_cage=[]
    for i in range(0, NT):
        for j in range(NN):
            point_one_cage.append(
                [cr_top * np.cos(i * 2 * np.pi / float(NT)),
                 cr_top * np.sin(i * 2 * np.pi / float(NT)),
                 - j * cage_height / float(NN)])
    return point_one_cage
