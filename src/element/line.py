import numpy as np

row_water=1000.0
kinematic_viscosity = 1.004e-6  # when the water temperature is 20 degree.
dynamic_viscosity = 1.002e-3  # when the water temperature is 20 degree.

class lines:
    def __init__(self,index:list,stiffness:float,dw0:float):
        self.k=stiffness # unit [N/m] a.k.a -> K
        self.index=index
        self.np_index=np.array(index)
        self.number_of_point=len(np.unique(np.array(self.index)))
        self.number_of_line=len(index)
        self.initial_line_length=0
        
        
    
    def __calc_lengths(self,point_position:np.array):
        line_vector=point_position[self.np_index[:, 0]]-point_position[self.np_index[:, 1]]
        line_length=np.linalg.norm(line_vector, axis=1)
        self.unit_vector=line_vector/line_length.reshape(self.number_of_line,-1)
        self.line_length=line_length
        return line_length

    def check_initial_lengths(self,point_position:np.array):
        self.initial_line_length = self.__calc_lengths(point_position)
        return max(self.initial_line_length),min(self.initial_line_length),np.mean(self.initial_line_length)
    
    def calc_tension_force(self,point_position):
        line_length=self.__calc_lengths(point_position)
        deformations=line_length - self.initial_line_length 
        # no compression force
        deformations[deformations<0]*=0.0
        tension=deformations*self.k
        return tension
    
    def map_forces(self,forces):
        # spring forces on the points of first column of spring index
        force1 = -self.unit_vector *forces.reshape(self.number_of_line, -1)
        force2 =  self.unit_vector *forces.reshape(self.number_of_line, -1)

        force_on_point=np.zeros((self.number_of_point,3))
        force_on_point[self.np_index[:,0]]+=force1
        force_on_point[self.np_index[:,1]]+=force2

        return force_on_point
    
    
    def __calculate_coe(self,uc:np.array):
        reynolds_number = row_water * self.dw0 * np.linalg.norm(uc) / dynamic_viscosity
        drag_tangent = np.pi * dynamic_viscosity * (
                        0.55 * np.sqrt(reynolds_number) + 0.084 * pow(reynolds_number, 2.0 / 3.0))
        s = -0.07721565 + np.log(8.0 / reynolds_number)
        if 0 < reynolds_number < 1:
            drag_normal = 8 * np.pi * \
                (1 - 0.87 * pow(s, -2)) / (s * reynolds_number)
        elif reynolds_number < 30:
            drag_normal = 1.45 + 8.55 * pow(reynolds_number, -0.9)
        elif reynolds_number < 2.33e5:
            drag_normal = 1.1 + 4 * pow(reynolds_number, -0.5)
        elif reynolds_number < 4.92e5:
            drag_normal = (-3.41e-6) * (reynolds_number - 5.78e5)
        elif reynolds_number < 1e7:
            drag_normal = 0.401 * \
                (1 - np.exp(-reynolds_number / 5.99 * 1e5))
        else:
            print("Reynold number=" + str(reynolds_number) +
                  ", and it exceeds the range.")
            print("Now, current_velocity is " + str(uc))
            print("Now, norm of current_velocity is " +
                  str(np.linalg.norm(uc)))
            exit()
        return drag_normal, drag_tangent

    def __calculate_dynamic_force(self,uc:np.array):
        """calculate the hydrodynamic forces on line element based on Morison model

        Args:
            sprint_length (np.array): list of the length of line element (M,1) 
            uc (np.array): fluid velocity at the element centroid (M,3) 
        """

        cn,ct=self.__calculate_coe(uc)
        # todo check the un ut
        un=self.unit_vector*uc*self.unit_vector
        ut=self.unit_vector*uc*self.unit_vector

        ft=0.5*ct*row_water*self.dw0*self.line_length*ut*np.linalg.norm(ut,axis=1)
        fn=0.5*cn*row_water*self.dw0*self.line_length*un*np.linalg.norm(un,axis=1)

        return ft+fn
