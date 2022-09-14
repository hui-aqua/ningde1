import pyvista as pv
import numpy as np


nodes = [
    [0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0],
    [4.0, 3.0, 0.0],
    [4.0, 0.0, 0.0],
    [0.0, 1.0, 2.0],
    [4.0, 1.0, 2.0],
    [4.0, 3.0, 2.0],
]


edges = [[0, 4],
         [1, 4],
         [3, 4],
         [5, 4],
         [6, 4],
         [3, 5],
         [2, 5],
         [5, 6],
         [2, 6]]
widths=[float(i)/100.0 for i in range(9)]

# We must "pad" the edges to indicate to vtk how many points per edge
edges_w_padding=[[2]+item for item in edges]

#mesh = pv.PolyData(nodes, edges_w_padding)
#mesh.plot(
#    scalars=colors,
#    render_lines_as_tubes=True,
#    style='wireframe',
#    line_width=widths,
#    cmap='jet',
#    show_scalar_bar=False,
#    background='w',
#)

xyz=np.array([[0,0,0],
			  [1,0,0],
			  [0,1,0],
			  [0,0,1]])

dxyz=np.ones((4,3))


arrow = pv.Arrow()


p = pv.Plotter()
# Top row
p.add_mesh(pv.Arrow([1,1,1],[0,1,0]),  show_edges=True)
#p.add_mesh(arrow([1,1,1],[0,0,1]), color="tan", show_edges=True)
p.add_mesh(arrow, color="tan", show_edges=True)
for item in edges:
    p.add_mesh(pv.Tube(nodes[item[0]],nodes[item[1]],radius=widths[item[0]]))



p.add_arrows(xyz,dxyz)



p.add_axes_at_origin()

# Render all of them
p.show()