"""
Author: Dr. Hui CHeng
Any questions about this code,
please email: hui.cheng@uis.no \n

"""
# For a circular type fish cage, top fixed and no bottom ring and net.

import numpy as np

cr_top=1.75/2.0   #[m]
cage_height=1.5   #[m]
NT=64#64
NN=17#17


def gen_points():
    point_one_cage=[]
    for i in range(0, NT):
        for j in range(NN+1):
            point_one_cage.append(
                [cr_top * np.cos(i * 2 * np.pi / float(NT)),
                 cr_top * np.sin(i * 2 * np.pi / float(NT)),
                 - j * cage_height / float(NN)])
    return point_one_cage

def gen_lines():
    ##todo  check it
    line_element=[]
    for i in range(NN):
        line_element.append([1+i, 1+i+(NN)*(NT-1)])
    for j in range(NT-1):
        line_element.append([1+i+j*(NN), 1+i+(j+1)*(NN)])

    # vertical con for netting
    for i in range(NN-1):
        for j in range(NT):
            line_element.append([1+i+j*(NN), 1+1+i+j*(NN)])
    return line_element

def gen_surfs():
    ##todo  check it
    surf_element=[]
    
    for i in range(NN-1):
        for j in range(NT):
            if j < NT-1:
                surf_element.append([1+i+j*(NN+1),1+1+i+j*(NN+1),
                                        1+i+(j+1)*(NN+1),1+1+i+(j+1)*(NN+1)])
            else:
                pass
                surf_element.append([1+i+j*(NN+1),1+1+i+j*(NN+1),
                                        1+i,1+1+i]) 
    return surf_element


def gen_cage():
    points=gen_points()
    lines=gen_lines()
    surfs=gen_surfs()
    return points,lines,surfs
