import numpy as np
import pyvista as pv
import src.geoMaker.ningde as geo
import src.visualization.saveVtk as sv

# for circular cage
# import src.case.circularCage as case
# case.main()
nodes=geo.nodes
line=geo.l_all
face=geo.netFace
sv.write_vtk('initial',point=nodes,line=line,face=face)