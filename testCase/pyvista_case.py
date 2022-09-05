import pyvista as pv
import numpy as np
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



p.add_arrows(xyz,dxyz)



p.add_axes_at_origin()

# Render all of them
p.show()