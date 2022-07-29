import numpy as np

row_water = 1000.0


class quads:
    def __init__(self,index:list,solidity:float):
        self.sn=solidity # unit [-]  0-1
        self.index=index
        self.np_index=np.array(index)
        self.number_of_point=len(np.unique(np.array(self.index)))
        self.number_of_quad=len(index)
        self.quad_centers=0
        self.vector_Ne=0      
        

    def __calc_area(self,point_position: np.array):   
        """ we assume the quad is numbered as [0,1,2,3]:
            0-------2
            |       |
            |       |
            1-------3

        Args:
            point_position (np.array): _description_
        """

        vector1 = point_position[self.np_index[:, 1]] - point_position[self.np_index[:, 0]]
        vector2 = point_position[self.np_index[:, 2]] - point_position[self.np_index[:, 1]]

        vector_n = np.cross(vector1, vector2, axis=1)

        quad_area = np.linalg.norm(vector_n, axis=1)
        self.vector_Ne = vector_n/quad_area.reshape(self.number_of_quad, -1)
        return quad_area.reshape(self.number_of_quad, -1)


    def __calc_quad_center(self,position: np.array):

        self.quad_centers = 0.25*(position[self.np_index[:, 0]] +
                             position[self.np_index[:, 1]] +
                             position[self.np_index[:, 2]] +
                             position[self.np_index[:, 3]])

    def get_wake_factor(self,point_position:np.array,u):
        self.__calc_quad_center(point_position)
        net_center=np.mean(point_position,axis=0)
        
        vector_cp = self.quad_centers-net_center
        
        filter = np.diagonal(vector_cp@u.T) > 0
        reduction_factor = np.ones(self.number_of_quad)
        cd,cl=self.__calc_force_coe(0)
        r = 1-0.46*cd
        reduction_factor[filter] *= r
        self.Ur=reduction_factor.reshape(self.number_of_quad,-1)
        return r

    def __calc_force_coe(self,theta):
        cd = 0.04 + (-0.04 + self.sn - 1.24 * pow(self.sn, 2) + 13.7 * pow(self.sn, 3)) * np.cos(theta)
        cl = (0.57 * self.sn - 3.54 * pow(self.sn, 2) + 10.1 * pow(self.sn, 3)) * np.sin(2 * theta)
        return cd, cl
    
    def cal_dynamic_force(self,point_position, uc):
        uc_mag = np.linalg.norm(uc, axis=1).reshape(self.number_of_quad, -1)
        # dot product in numpy do not have axis

        quad_area = self.__calc_area(point_position)
        theta = np.arccos(abs(np.diagonal(self.vector_Ne@uc.T)).reshape(self.number_of_quad, -1) / uc_mag)
        cd, cl = self.__calc_force_coe(theta)

        drag_e = uc/uc_mag
        lift_e = np.cross(np.cross(drag_e, self.vector_Ne, axis=1),drag_e,axis=1)

        fd = 0.5*row_water*quad_area*cd*pow(uc_mag*self.Ur, 2)*drag_e
        fl = 0.5*row_water*quad_area*cl*pow(uc_mag*self.Ur, 2)*lift_e

        return fd+fl


    def map_force(self,force_on_quad):
        force_on_point = np.zeros((self.number_of_point, 3))

        for i in range(4):
            force_on_point[self.np_index[:, i]] += force_on_quad*0.25

        return force_on_point
    
    def map_velocity(self,u):
        if len(u) == 3:
            uc = np.ones((self.number_of_quad, 3))*u
        elif len(u) == self.number_of_quad:
            uc = u
        elif len(u) == self.number_of_point:
            uc=np.zeros((self.number_of_quad,3))
            for i in range(4):
                uc+=0.25*u[self.np_index[:,i]]
        else:    
            print("The given U does match element", u)
        return uc
 
