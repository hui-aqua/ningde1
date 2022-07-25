import matplotlib.pyplot as plt
import numpy as np

def plot_square(line_list:list):
    __number_of_point=np.max(np.array(line_list))+1
    print(__number_of_point)
    ma=np.zeros((__number_of_point,__number_of_point))
    for item in line_list:
        ma[item[0],item[1]]-=10
        ma[item[1],item[0]]-=10
    
    # print(a)
    plt.imshow(ma, cmap='hot', interpolation='nearest')
    plt.show()


def plot_element(element:list):
    __number_of_point=np.max(np.array(element))+1
    print(__number_of_point)
    ma=np.zeros((__number_of_point,len(element)))
    for index,item in enumerate(element) :
        for node in item:
            ma[node,index]-=10
        
    
    # print(a)
    plt.imshow(ma, cmap='hot', interpolation='nearest')
    plt.xlabel('Element')
    plt.ylabel('Nodes')
    plt.show()
    

if __name__=="__main__":
    plot_square()