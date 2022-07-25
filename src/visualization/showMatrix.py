import matplotlib.pyplot as plt
import numpy as np

def plot(line_list:list):
    __number_of_point=np.max(np.array(line_list))+1
    print(__number_of_point)
    ma=np.zeros((__number_of_point,__number_of_point))
    for item in line_list:
        ma[item[0],item[1]]-=10
        ma[item[1],item[0]]-=10
    
    # print(a)
    plt.imshow(ma, cmap='hot', interpolation='nearest')
    plt.show()
    
if __name__=="__main__":
    plot()