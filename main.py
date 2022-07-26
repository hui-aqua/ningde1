from turtle import position
import numpy as np
import src.visualization.vtkVisualization as pv
import src.geoMaker.circular as geo
import src.visualization.saveVtk as sv
import src.forces.springForce as f
import src.visualization.showMatrix as sm
import src.forces.quad as q
# import sys
# np.set_printoptions(threshold=sys.maxsize)
geo.NN = 17
geo.NT = 64


sv.point, sv.line, sv.face = geo.gen_cage()
print(geo.number_of_horizontal_line)
sv.write_vtk('0')
# pv.show_point(sv.point)


np.savetxt('point.out', sv.point)
np.savetxt('lines.out', sv.line, delimiter=',', fmt='%1u')
np.savetxt('surfs.out', sv.face, delimiter=',', fmt='%1u')

# the submerged weight are attached to these points
weight_point = [1088+4*i for i in range(16)]
weight = 4.48  # [N]

fixed_point = [i for i in range(64)]
# ref KikkoNet: 0.59kg/m2
# netting area=1.75*3.14159*1.5=8.24667375 [m2]
# total netting mass=0.59*8.25= 4.865 kg
point_mass = np.ones((len(sv.point),1))*4.865/len(sv.point)
point_mass[weight_point] += weight/9.81

position0 = np.array(sv.point)
velocity0 = np.zeros_like(position0)

gravity = np.array([0, 0, -9.81])  # unit [ m /s2]

f.spring_index = sv.line
f.number_of_point=len(sv.point)
initial_length = f.calc_spring_length(sv.point)
print(min(initial_length))
print(max(initial_length))
print(max(initial_length)*min(initial_length))
q.quad_index=sv.face
print(q.cal_area(position0))
print(q.quad_unit_vector)
run_time = 10  # unit [s]
dt = 0.00005    # unit [s]

# forward Euler (explicit)
for i in range(int(run_time/dt)):
     
    
    # spring tension force
    sprint_length = f.calc_spring_length(position0)
    spring_force = f.calc_spring_force(sprint_length-initial_length)
    velocity0 += dt * f.map_sprint_force(spring_force) / point_mass
    # hydro force
    filter=[i*64 for i in range(18)]
    velocity0+=np.array([0.001,0,0])/point_mass
    
    # gravity force
    velocity0 += dt*gravity

    velocity0[fixed_point] *= 0.0  # velocity restriction

    position0 += dt*velocity0
    # print(position0)
    sv.point = position0.tolist()
    if i % 1 == 00:
        print('t = ','{:f}'.format(i*dt)) 
        sv.write_vtk('ami/'+str(i))
 