"""for mooring lines optimization
"""

import numpy as np
import pyvista as pv
import src.geoMaker.ningde as geo
import src.visualization.saveVtk as sv
import src.element.line as l
import src.element.quad as q
import src.waterWave.regularWaves as rw
import src.waterWave.irregularWaves as iw
import src.waterWave.waveSpectrum as ws

initial_node=geo.new_mooring_point
line=geo.mooringLine
print(line)
sv.write_vtk('initial',point=initial_node,line=line)


# define structural properties
num_point=len(initial_node)
num_bodyPoint=31
num_mooringPoint=num_point-num_bodyPoint
num_seg=50

m_body=4980760 #[kg]

m_mooring1=219 #[kg/m]
m_mooring2=185.36 #[kg/m]




l1=l.lines(geo.l1,10e9,0.5)
l2=l.lines(geo.l2,10e9,1.0)
l3=l.lines(geo.l3,10e9,1.5)
l5=l.lines(geo.l5,10e9,2.5)
lm=l.lines(geo.lm,10e9,0.01)


l1.assign_length(xyz)
l2.assign_length(xyz)
l3.assign_length(xyz)
l5.assign_length(xyz)

lm.assign_length(300/50.0)




point_mass=[m_body/num_bodyPoint]*num_bodyPoint
point_mass+=[m_mooring1*6]*int(num_mooringPoint/2)
point_mass+=[m_mooring2*6]*int(num_mooringPoint/2)
point_mass=np.array(point_mass).reshape(len(point_mass),1)
print(point_mass.shape)
# 
fixed_point=[num_bodyPoint+num_seg*i for i in range(8)]


position=np.array(initial_node)
velocity=np.zeros_like(xyz)
gravity=np.array([0,0,-9.81])

#wave=rw.Airywave(wave_height=1.0,wave_period=10.0,water_depth=22,direction=0,phase=0)
spe=ws.jonswap_spectra(np.linspace(0.02,10,100),hs=3.43,tp=6.7)
kk=np.hstack((np.linspace(0.02,10,100).reshape(100,1),spe.reshape(100,1)))
iwave=iw.summation(kk,22,0)

wave_prob=np.array([[1,0,0]]*800)*np.linspace(-200,200,800).reshape(800,1)
run_time = 5  # unit [s]
dt = 2e-4    # unit [s]



# PBD
for i in range(int(run_time/dt)):       
    if i % 200 == 0:
        print('t = ','{:f}'.format(i*dt)) 
        position_list=position.tolist()
        sv.write_vtk('ami2/pbd'+str(i),point=position_list,line=sv.line,face=sv.face)  
        
    ### forward Euler (explicit)
    
    ## external loads
    pre_position=position.copy()
    # gravity force
    velocity += dt*gravity
    # current load
    # u=quad_element.map_velocity(uc)
    # uw=quad_element.map_velocity(wave.get_velocity_at_nodes(position,i*dt))
    # u+=uw
    # hydro_force=quad_element.cal_dynamic_force(position,u)
    # velocity += dt * quad_element.map_force(hydro_force) / mass_matrix
    
    ## boundary condition
    velocity[fixed_point] *= 0.0  # velocity restriction
    velocity[position[:,2]<-44]*=np.array([1,1,0])# ground
    position += dt*velocity
    ### constraint function 
    position+=lm.pbd_edge_constraint(position,point_mass,dt)
    
    ### velocity correction
    velocity=(position-pre_position)/dt