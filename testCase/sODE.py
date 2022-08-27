# Example case
# |     k = 10 N/m   
# |================[m=1 kg]  
# |_____l0=1 m ___________
import numpy as np
import matplotlib.pyplot as plt
k=10.0
m=1.0
l0=1.0
x0=1.2
u0=0

run_time = 40  # unit [s]
dt = 5e-2    # unit [s]

   
# forward Euler (explicit)
position=x0
velocity=u0
result=[]
for i in range(int(run_time/dt)):
    
    spring_force=(position-l0)*k
    velocity -= dt*spring_force/m
    position+= dt*velocity
    result.append([dt*i,position,velocity])




plt.figure()
result=np.array(result)
plt.plot(result[:,0],result[:,1],'-')
plt.plot(result[:,0],result[:,2],'--')
plt.show()

