import numpy as np
import src.visualization.vtkVisualization as pv
import src.geoMaker.circular as geo
import src.visualization.saveVtk as sv


geo.NN=17
geo.NT=64


sv.point,sv.line,sv.face =geo.gen_cage()
sv.write_vtk('0')

# pv.show_point(sv.point)

np.savetxt('point.out',sv.point)
np.savetxt('lines.out',sv.line,delimiter=',',fmt='%1u')
np.savetxt('surfs.out',sv.face,delimiter=',',fmt='%1u')
