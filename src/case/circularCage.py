import numpy as np
import src.element.line as l
import src.element.quad as q
import src.waterWave.regularWaves as ww
import pyvista as pv
import src.geoMaker.circular as geo
import src.visualization.saveVtk as sv



# For a circular type fish cage, top fixed and no bottom ring and net.
def main():
    geo.NN = 17
    geo.NT = 64


    sv.point, sv.face = geo.gen_cage()
    hline,vline=geo.gen_lines()
    sv.line=hline+vline
    num_point=len(sv.point)
    np.savetxt('point.out', sv.point)
    np.savetxt('lines.out', sv.line, delimiter=',', fmt='%1u')
    np.savetxt('surfs.out', sv.face, delimiter=',', fmt='%1u')

    ## visualization using pyvista
    p = pv.Plotter()
    edges=[[[2]+item] for item in sv.line]
    mesh=pv.PolyData(sv.point,edges)
    p.add_mesh(mesh,color='tan',style='wireframe')
    p.add_axes_at_origin()
    p.show()
    mesh.save("mesh.vtk")

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

    hline_element=l.lines(hline,1e6,0.03)
    vline_element=l.lines(vline,1e6,0.03)
    # must check initial length
    print('hline length is ', hline_element.assign_length(position))
    print('vline length is ', vline_element.assign_length(position))

    quad_element=q.quads(sv.face,0.2)

    run_time = 10  # unit [s]
    dt = 4e-5    # unit [s]

    uc=np.array([0.25,0,0])
    u=quad_element.map_velocity(uc)

    wave=ww.Airywave(0.05,0.95,10)

    # must check velocity reduction factor
    print('velocity reduction factor is ', quad_element.get_wake_factor(position,u))
    
    # forward Euler (explicit)
    for i in range(int(run_time/dt)):       
        # tension force on lines
        spring_force = hline_element.calc_tension_force(position)
        velocity += dt * hline_element.map_tension(spring_force,num_point) / point_mass

        spring_force = vline_element.calc_tension_force(position)
        velocity += dt * vline_element.map_tension(spring_force,num_point) / point_mass

        # hydro force
        u=quad_element.map_velocity(uc)
        uw=quad_element.map_velocity(wave.get_velocity_at_nodes(position,i*dt))
        u+=uw
        hydro_force=quad_element.cal_dynamic_force(position,u)
        velocity += dt * quad_element.map_force(hydro_force) / point_mass        

        # gravity force
        velocity += dt*gravity

        velocity[fixed_point] *= 0.0  # velocity restriction
        # velocity[fixed_point] *= np.array([1.0,1.0,0.0])  # fixed on xy plane

        position += dt*velocity
        # print(position0)
        sv.point = position.tolist()
        if i % 500 == 0:
            print('t = ','{:f}'.format(i*dt)) 
            sv.write_vtk('ami2/'+str(i),point=sv.point,line=sv.line,face=sv.face)
   