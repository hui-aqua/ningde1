import numpy as np
import pyvista as pv
import src.geoMaker.ningde as geo
import src.visualization.saveVtk as sv
import src.element.line as l
import src.element.quad as q
import src.waterWave.regularWaves as rw
import src.waterWave.irregularWaves as iw
import src.waterWave.waveSpectrum as ws

nodes=geo.nodes
line=geo.l_all
face=geo.netFace
sv.write_vtk('initial',point=nodes,line=line,face=face)
xyz=np.array(nodes)
# sv.write_vtk("initial",point=nodes,face=geo.netFace)
# sv.write_line_vtk("initial_l1",point=nodes,line=geo.l1)
# sv.write_line_vtk("initial_l2",point=nodes,line=geo.l2)
# sv.write_line_vtk("initial_l3",point=nodes,line=geo.l3)
# sv.write_line_vtk("initial_l5",point=nodes,line=geo.l5)
# sv.write_line_vtk("initial_lm",point=nodes,line=geo.lm)

# define structural properties
num_point=len(nodes)
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
print(point_mass)
point_mass+=[m_mooring1*6]*int(num_mooringPoint/2)
point_mass+=[m_mooring2*6]*int(num_mooringPoint/2)
point_mass=np.array(point_mass)
# 
fixed_point=[num_bodyPoint+num_seg*i for i in range(8)]


prev_xyz=np.array(nodes)
dxyz=np.zeros_like(xyz)
gravity=np.array([0,0,-9.81])

#wave=rw.Airywave(wave_height=1.0,wave_period=10.0,water_depth=22,direction=0,phase=0)
spe=ws.jonswap_spectra(np.linspace(0.02,10,100),hs=3.43,tp=6.7)
kk=np.hstack((np.linspace(0.02,10,100).reshape(100,1),spe.reshape(100,1)))
iwave=iw.summation(kk,22,0)

wave_prob=np.array([[1,0,0]]*800)*np.linspace(-200,200,800).reshape(800,1)
run_time = 5  # unit [s]
dt = 2e-4    # unit [s]




# forward Euler (explicit)
for i in range(int(run_time/dt)): 
    nodes = xyz.tolist()  
    if i % 100 == 0:
        elevation=iwave.get_elevations_at_one_time(wave_prob,dt*i)
        elevation=wave_prob+np.array([[0,0,1]]*800)*elevation.reshape(800,1)
        sv.write_wave_vtk("ami2/"+"resu"+str(i),elevation,100)
        # sv.write_vtk('initial',point=nodes,line=line,face=face)
        sv.write_vtk("ami2/"+"resu"+str(i),point=nodes,face=face,line=geo.l_all) 
        
           
    # prev_xyz=xyz.copy()
    ### external forces    
    # gravity force
    dxyz += dt*gravity
    
 

    # ### edge constraints
    # spring_force = lm.calc_tension_force(xyz)
    # dxyz += dt * lm.map_tension(spring_force,num_point) / point_mass.reshape(num_point,1)
    # spring_force = l1.calc_tension_force(xyz)+l1.calc_compression_force(xyz)
    # dxyz += dt * l1.map_tension(spring_force,num_point) / point_mass.reshape(num_point,1)
    # spring_force = l2.calc_tension_force(xyz)+l2.calc_compression_force(xyz)
    # dxyz += dt * l2.map_tension(spring_force,num_point) / point_mass.reshape(num_point,1)
    # spring_force = l3.calc_tension_force(xyz)+l3.calc_compression_force(xyz)
    # dxyz += dt * l3.map_tension(spring_force,num_point) / point_mass.reshape(num_point,1)
    # spring_force = l5.calc_tension_force(xyz)+l5.calc_compression_force(xyz)
    # dxyz += dt * l5.map_tension(spring_force,num_point) / point_mass.reshape(num_point,1)
      
    
    # boundary condition
    dxyz[fixed_point] *= 0.0  # fixed point boundary
    # dxyz[[0,10,4,14]] *= 0.0  # for test
    dxyz[xyz[:,2]<-22.0]*=np.array([1.0,1.0,0.0]) # sea bead boundary
    xyz += dt*dxyz
    