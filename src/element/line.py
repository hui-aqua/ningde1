import numpy as np

row_water=1000.0
row_air=1.001
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
        self.dw0=dw0
    # private function 

    def __calc_lengths(self,point_position:np.array):
        line_vector=point_position[self.np_index[:, 0]]-point_position[self.np_index[:, 1]]
        line_length=np.linalg.norm(line_vector, axis=1)
        self.unit_vector=line_vector/line_length.reshape(self.number_of_line,-1)
        self.line_length=line_length
        return line_length
    
    
    # public function
    def assign_length(self,input_value):
        """This is a initial function to assign a length to a group line element

        Args:
            input_value (varian): the input value can be:\n 
            (1) one single value, then the length of line element will be the same as input value.\n
            (2) a python list of length, to assign a variant length to the line group.\n
            (3) a n*3 numpy array of all the nodes position, then the length can bu calculated based on the array.\n
            

        Returns:
            float: get the mean length of this line group.
        """
        if type(input_value)==type(np.zeros(3)):
            self.initial_line_length = self.__calc_lengths(input_value)
        elif type(input_value)==type([1]) and len(input_value)== self.number_of_line:
            self.initial_line_length = input_value
        elif type(input_value) ==type(4.2):
            self.initial_line_length = self.number_of_line*[input_value]
        
        return np.mean(self.initial_line_length)
        
    
    def calc_tension_force(self,point_position):
        line_length=self.__calc_lengths(point_position)
        deformations=line_length - self.initial_line_length 
        # no compression force
        deformations[deformations<0]*=0.0
        tension=deformations*self.k
        return tension
    
    def calc_compression_force(self,point_position):
        line_length=self.__calc_lengths(point_position)
        deformations=line_length - self.initial_line_length 
        # no compression force
        deformations[deformations>0]*=0.0
        tension=deformations*self.k
        return tension
    
    
    def map_tension(self,forces:np.array,num_point:int):
        # spring forces on the points of first column of spring index
        force1 = -self.unit_vector *forces.reshape(self.number_of_line, -1)
        force2 =  self.unit_vector *forces.reshape(self.number_of_line, -1)
        force_on_point=np.zeros((num_point,3))
        force_on_point[self.np_index[:,0]]+=force1
        force_on_point[self.np_index[:,1]]+=force2
        return force_on_point
    
    def pbd_position(self,forces,mass):
        force1 = -self.unit_vector *forces.reshape(self.number_of_line, -1)
        force2 =  self.unit_vector *forces.reshape(self.number_of_line, -1)
        force_on_point=np.zeros((self.number_of_point,3))
        force_on_point[self.np_index[:,0]]+=force1
        force_on_point[self.np_index[:,1]]+=force2
        return force_on_point
        
    
    
    def calculate_extenal_force(self,node_position,u): 
        # calculate the buoyancy and drag force (based on Morison equation).
        pass
    
    
    def map_hydrodynamic_force(self,forces):
        force_on_point=np.zeros((self.number_of_point,3))
        force_on_point[self.np_index[:,0]]+=forces/2.0
        force_on_point[self.np_index[:,1]]+=forces/2.0

    
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

    def __cal_aw_ratio(self,):
        # calculate the ratio between air and water
        # consider as slender bar
        pass
    
    
    def __calculate_buoyancy_force(self,node_position, elevation):
                
        # force on line element, initial as zeros
        force_on_element = np.zeros((self.number_of_line, 3),dtype=float)
        
        p1_z=elevation[self.np_index[:,0]]-node_position[self.np_index[:,0]][:,2]
        p2_z=elevation[self.np_index[:,1]]-node_position[self.np_index[:,1]][:,2]
        
        
        for index, element in enumerate(self.line_elements):
            p1 = node_position[int(element[0])]
            p2 = node_position[int(element[1])]

            list_z = []
            for each in element:
                list_z.append(float(elevation[each] - node_position[each][2]))
            ratio = self.__cal_aw_ratio(list_z)
            row = row_water*ratio+row_air*(1-ratio)

            element_length = np.linalg.norm(p1-p2)
            element_volume = 0.25*np.pi*pow(self.dwh, 2)*element_length           
            force_on_element[index] = [0.0, 0.0, element_volume*9.81*row]

        self.hydro_static_forces = np.array(force_on_element)
        return np.array(force_on_element)
    
    
    
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
    
    
    
# class pipe(line):
    
#     """
#     For Morison hydrodynamic models, the forces on netting are calculated based on individual pipe.
#     The twines are taken as cylindrical elements. In practice, the force is usually decomposed into two components:
#     normal drag force F_n and tangential drag force F_t (Cheng et al., 2020)
#     """
#     def __init__(self,index:list,stiffness:float,dw0:float,thickness:float):
#         self.k=stiffness # unit [N/m] a.k.a -> K
#         self.index=index
#         self.np_index=np.array(index)
#         self.number_of_point=len(np.unique(np.array(self.index)))
#         self.number_of_line=len(index)
#         self.initial_line_length=0
#         self.dw0=dw0
#         self.t=thickness
            
#     def __cal_aw_ratio(self,):
#         # calculate the ratio between air and water
#         # consider as thick pipe
#         pass
    


if __name__ == "__main__":
    pass