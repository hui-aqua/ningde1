import numpy as np
import pyvista as pv
import src.geoMaker.ningde as geo
import src.visualization.saveVtk as sv
import src.element.line as l
import src.element.quad as q

# for circular cage
# import src.case.circularCage as case
# case.main()
nodes=geo.nodes
line=geo.l_all
face=geo.netFace
# sv.write_vtk('initial',point=nodes,line=line,face=face)
sv.write_vtk("initial",point=nodes,face=geo.netFace)
sv.write_line_vtk("initial_l1",point=nodes,line=geo.l1)
sv.write_line_vtk("initial_l2",point=nodes,line=geo.l2)
sv.write_line_vtk("initial_l3",point=nodes,line=geo.l3)
sv.write_line_vtk("initial_l5",point=nodes,line=geo.l5)
sv.write_line_vtk("initial_lm",point=nodes,line=geo.lm)

# define structural properties
num_bodyPoint=31
num_seg=50

m_body=4980760 #[kg]
# l1=l.lines(geo.l1,10e9,0.5)
# l2=l.lines(geo.l2,10e9,1.0)
# l3=l.lines(geo.l3,10e9,1.5)
# l5=l.lines(geo.l5,10e9,2.5)
# lm=l.lines(geo.lm,10e9,0.01)




# 
fixed_point=[num_bodyPoint+num_seg*i for i in range(8)]

xyz=np.array(nodes)
dxyz=np.zeros_like(xyz)
gravity=np.array([0,0,-9.81])


run_time = 10  # unit [s]
dt = 2e-2    # unit [s]

# forward Euler (explicit)
for i in range(int(run_time/dt)):       
       
    # gravity force
    dxyz += dt*gravity
    
    # boundary condition
    dxyz[fixed_point] *= 0.0  # velocity restriction
    dxyz[xyz[:,2]<-22.0]*=np.array([1.0,1.0,0.0]) 
    # velocity[fixed_point] *= np.array([1.0,1.0,0.0])  # fixed on xy plane
    xyz += dt*dxyz
    # print(dxyz)
    # print(position0)
    nodes = xyz.tolist()
    # print(nodes)
    if i % 5 == 0:
        # sv.write_vtk('initial',point=nodes,line=line,face=face)
        sv.write_vtk("ami2/"+"fa"+str(i),point=nodes,face=face)
        sv.write_line_vtk("ami2/"+"l1"+str(i),point=nodes,line=geo.l1)
        sv.write_line_vtk("ami2/"+"l2"+str(i),point=nodes,line=geo.l2)
        sv.write_line_vtk("ami2/"+"l3"+str(i),point=nodes,line=geo.l3)
        sv.write_line_vtk("ami2/"+"l5"+str(i),point=nodes,line=geo.l5)
        sv.write_line_vtk("ami2/"+"lm"+str(i),point=nodes,line=geo.lm)
