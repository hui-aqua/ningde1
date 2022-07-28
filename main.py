from turtle import position
import numpy as np
import src.visualization.vtkVisualization as pv
import src.geoMaker.circular as geo
import src.visualization.saveVtk as sv
import src.forces.line as l
import src.visualization.showMatrix as sm
import src.forces.quad as q

geo.NN = 17
geo.NT = 64


sv.point, sv.face = geo.gen_cage()
hline,vline=geo.gen_lines()
sv.line=hline+vline

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

position = np.array(sv.point)
velocity = np.zeros_like(position)

gravity = np.array([0, 0, -9.81])  # unit [ m /s2]

l.spring_index = sv.line
l.number_of_point=len(sv.point)
initial_length = l.calc_spring_length(sv.point)
q.quad_index=sv.face
q.number_of_point=len(sv.point)
q.number_of_quad=len(sv.face)


run_time = 10  # unit [s]
dt = 5e-5    # unit [s]
uc=np.array([0.3,0,0])
u=q.map_velocity(uc)


# forward Euler (explicit)
for i in range(int(run_time/dt)):       
    # spring tension force
    sprint_length = l.calc_spring_length(position)
    spring_force = l.calc_spring_force(sprint_length-initial_length)
    velocity += dt * l.map_force(spring_force) / point_mass
    
    # hydro force
    
    hydro_force=q.cal_dynamic_force(position,u)
    velocity += dt * q.map_force(hydro_force) / point_mass        
    
    # gravity force
    velocity += dt*gravity

    velocity[fixed_point] *= 0.0  # velocity restriction

    position += dt*velocity
    # print(position0)
    sv.point = position.tolist()
    if i % 100 == 0:
        print('t = ','{:f}'.format(i*dt)) 
        sv.write_vtk('ami/'+str(i))
 