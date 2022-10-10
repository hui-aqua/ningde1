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

#wave=rw.Airywave(wave_height=1.0,wave_period=10.0,water_depth=22,direction=0,phase=0)
spe=ws.jonswap_spectra(np.linspace(0.02,10,100),)
iwave=iw.summation()

wave_prob=np.array([[1,0,0]]*800)*np.linspace(-200,200,800).reshape(800,1)
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
    #xyz += dt*dxyz
    
    
    nodes = xyz.tolist()
    if i % 5 == 0:
        elevation=wave.calc_elevation(wave_prob,dt*i)
        elevation=wave_prob+np.array([[0,0,1]]*800)*elevation.reshape(800,1)
        sv.write_wave_vtk("ami2/"+"resu"+str(i),elevation,100)
        # sv.write_vtk('initial',point=nodes,line=line,face=face)
        sv.write_vtk("ami2/"+"resu"+str(i),point=nodes,face=face,line=geo.l_all)

