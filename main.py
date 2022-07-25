import numpy as np
import src.visualization.vtkVisualization as pv
import src.geoMaker.circular as geo
import src.visualization.saveVtk as sv
import src.forces.springForce as f
import src.visualization.showMatrix as sm

geo.NN = 4#17
geo.NT = 16#64


sv.point, sv.line, sv.face = geo.gen_cage()
sv.write_vtk('0')
sm.plot(sv.line)
pv.show_point(sv.point)

np.savetxt('point.out', sv.point)
np.savetxt('lines.out', sv.line, delimiter=',', fmt='%1u')
np.savetxt('surfs.out', sv.face, delimiter=',', fmt='%1u')

# the submerged weight are attached to these points
weight_point = [i*18*4+17 for i in range(16)]
weight = 4.48  # [N]

fixed_point = [i*18 for i in range(64)]

run_time = 15  # unit [s]
dt = 0.0001     # unit [s]

# numpy operation
point_mass = 0.01*np.array([1 for i in range(len(sv.point))])
point_mass[weight_point] += weight

position0 = np.array(sv.point)
velocity0 = np.zeros_like(position0)
gravity = np.array([0, 0, -9.81])  # unit [ m /s2]
f.spring_index = sv.line
initial_length = f.calc_spring_length(sv.point)

for i in range(int(run_time/dt)):
    print(i)
    # spring tension force

    sprint_length = f.calc_spring_length(position0)
    spring_force = f.calc_spring_force(sprint_length-initial_length)
    velocity0 += dt * \
        f.map_sprint_force(position0, spring_force) / \
        point_mass.reshape(len(point_mass), -1)

    # gravity force
    velocity0 += dt*gravity*point_mass.reshape(len(point_mass), -1)

    velocity0[fixed_point] *= 0.0  # velocity restriction

    position0 += dt*velocity0
    # print(position0)
    sv.point = position0.tolist()
    if i % 100 == 0:
        sv.write_vtk('ami/'+str(i))
