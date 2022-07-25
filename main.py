import numpy as np
import src.visualization.vtkVisualization as pv
import src.geoMaker.circular as geo
import src.visualization.saveVtk as sv
import src.forces.springForce as f


geo.NN = 17
geo.NT = 64


sv.point, sv.line, sv.face = geo.gen_cage()
sv.write_vtk('0')

pv.show_point(sv.point)

np.savetxt('point.out', sv.point)
np.savetxt('lines.out', sv.line, delimiter=',', fmt='%1u')
np.savetxt('surfs.out', sv.face, delimiter=',', fmt='%1u')

# the submerged weight are attached to these points
weight_point=[i*18*4+17 for i in range(16)]
weight=4.48 #[N]

fixed_point=[i*18 for i in range(64) ]

gravity = -9.81  # unit [ m /s2]

initial_length=f.calc_spring_length(sv.point,sv.line)
point_mass=0.01*np.array([1 for i in range(len(sv.point))])

spring_stiffness = 1e3  # unit [N/m] a.k.a -> K



gravity = -9.81  # unit [ m /s2]

def update(point_position,point_velocity):
    position0=np.array(point_position)
    velocity0=np.zeros_like(position0)
    
    
    
    pass


run_time = 15  # unit [s]
dt = 0.01     # unit [s]

for i in range(int(run_time/dt)):
    update()