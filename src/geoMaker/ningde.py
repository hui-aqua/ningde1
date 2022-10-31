import numpy as np

# node no main body
nodes = [[-58.5, 26.5,   0.0],
         [-28.5, 26.5,   0.0],
         [0,     26.5,   0.0],
         [28.5,  26.5,   0.0],
         [58.5,  26.5,   0.0],

         [-58.5,  0.0,   0.0],
         [-28.5,  0.0,   0.0],
         [0,      0.0,   0.0],
         [28.5,   0.0,   0.0],
         [58.5,   0.0,   0.0],
         [-58.5, -26.5,  0.0],
         [-28.5, -26.5,  0.0],
         [0,     -26.5,  0.0],
         [28.5,  -26.5,  0.0],
         [58.5,  -26.5,  0.0],

         [-58.5, 26.5,   -10.0],
         [-28.5, 26.5,   -10.0],
         [0,     26.5,   -10.0],
         [28.5,  26.5,   -10.0],
         [58.5,  26.5,   -10.0],
         [-58.5,  0.0,   -10.0],
         [-28.5,  0.0,   -10.0],
         [0,      0.0,   -10.0],
         [28.5,   0.0,   -10.0],
         [58.5,   0.0,   -10.0],
         [-58.5, -26.5,  -10.0],
         [-28.5, -26.5,  -10.0],
         [0,     -26.5,  -10.0],
         [28.5,  -26.5,  -10.0],
         [58.5,  -26.5,  -10.0],
         [0, 0, 13.75]]

# node on mooring lines

anchor_point = [
                 [-276.405,	-226.173	, -22], # 10--8
                 [-258.173,	-244.405	, -22], # 10--7
                 [276.405,	-226.173	, -22], # 14--6
                 [258.173,	-244.405	, -22], # 14--5
                 [-276.6,	226.352		, -22], # 0--1
                 [-258.352,	244.6		, -22], # 0--2
                 [276.6,	226.352		, -22], # 4--3
                 [258.352,	244.6		, -22]] # 4--4

attached_point=[10,10,14,14,0,0,4,4]  # Index of node for the main body

# 50 segments per mooring line.
num_seg=50
mooring_point=[]
for i in range(8):
    ml=np.linspace(anchor_point[i],nodes[attached_point[i]],num_seg,endpoint=False)
    mooring_point+=ml.tolist()

# New_mooring line
# 50 segments per mooring line.
num_seg=50
new_mooring_point=[]
for i in range(8):
    ml=np.linspace(anchor_point[i],nodes[attached_point[i]],num_seg)
    new_mooring_point+=ml.tolist()
mooringLine=[]
for i in range(8):
    for j in range(50):
        mooringLine.append([j+i*51,j+1+i*51])




# distance:
# mnarray=np.array(mooring_nodes)
# for i in range(8):
#     print(np.linalg.norm(mnarray[i]-mnarray[i+8]))

# 296.37121309938317
# 296.37121309938317
# 296.37121309938317
# 296.37121309938317
# 296.635183186351
# 296.63518318635096
# 296.635183186351
# 296.63518318635096

nodes += mooring_point

## lines
# frame
l1 = [[0, 6], [1, 6], [2, 6], [10, 6], [11, 6], [12, 6],
      [2, 8], [3, 8], [4, 8], [12, 8], [13, 8], [14, 8],
      [2, 7], [7, 12],
      [15, 21], [16, 21], [17, 21], [25, 21], [26, 21], [27, 21],
      [17, 23], [18, 23], [19, 23], [27, 23], [28, 23], [29, 23],
      [17, 22], [22, 27]]
l2 = [[0, 1], [1, 2], [2, 3], [3, 4],
      [5, 6], [6, 7], [7, 8], [8, 9],
      [10, 11], [11, 12], [12, 13], [13, 14],
      [0, 5], [5, 10], [4, 9], [9, 14]]
l3 = (np.array(l2) + 15).tolist()
# add vertical 2m pipe
for i in range(15):
    l2.append([i, i + 15])

l1 += [[15, 1], [17, 1], [17, 3], [19, 3],
       [25, 11], [27, 11], [27, 13], [29, 13]]
l5 = [[7, 30]]

# mooring lines
num_body_point=31
lm=[]
for i in range(8):
    for j in range(num_seg-1):
        lm.append([i*num_seg+num_body_point+j,i*num_seg+num_body_point+j+1])
    lm.append([i*num_seg+num_body_point+j+1,attached_point[i]])
l_all=l1+l2+l3+l5+lm

## face
netFace=[[0,1,15,16],
         [1,2,16,17],
         [2,3,17,18],
         [3,4,18,19],
         [4,9,19,24],
         [9,14,24,29],
         [14,13,29,28],
         [13,12,28,27],
         [12,11,27,26],
         [11,10,26,25],
         [10,5,25,20],
         [5,0,20,15],
         [0,1,5,6],
         [5,6,10,11],
         [1,2,6,7],
         [6,7,11,12],
         [2,3,7,8],
         [7,8,12,13],
         [3,4,8,9],
         [8,9,13,14],
         [25,26,20,21],
         [20,21,15,16],
         [26,27,21,22],
         [21,22,16,17],
         [27,28,22,23],
         [22,23,17,18],
         [28,29,23,24],
         [23,24,18,19]]

if __name__ == '__main__':
    pass
	# from ..visualization import saveVtk as sv
	# sv.write_vtk("initial",point=nodes,face=netFace)
	# sv.write_line_vtk("initial_l1",point=nodes,line=l1)
	# sv.write_line_vtk("initial_l2",point=nodes,line=l2)
	# sv.write_line_vtk("initial_l3",point=nodes,line=l3)
	# sv.write_line_vtk("initial_l5",point=nodes,line=l5)
	# sv.write_line_vtk("initial_lm",point=nodes,line=lm)