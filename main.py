import numpy as np
import src.visualization.vtkVisualization as pv
import src.geoMaker.circular as geo

p=geo.gen_points()
# print(p)
pv.show_point(p)


geo.NN=17
geo.NT=64

point,lines,surfs =geo.gen_cage()
print(point)

pv.save_vtk(point,surfs,'0')

np.savetxt('point.out',point)
np.savetxt('lines.out',lines,delimiter=',',fmt='%1u')
np.savetxt('surfs.out',surfs,delimiter=',',fmt='%1u')
