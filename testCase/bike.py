import gen as g
import numpy as np
import sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# initial, setup the physical world
# the positions of points are generated using random funciton from np
num_point=4
points_position = np.random.rand(num_point, 2)*8+3

# for test
# points_position = np.array([[1.0, 5],
#                             [1, 10],
#                             [5, 10],
#                             [5, 5]])
# points_position+=5
start_x = np.max(points_position[:, 0])
points_velocity = np.zeros_like(points_position)

points_mass = np.array([20, 20, 0.1, 0.1])  # unit [m]
wheel_radius = 1.2  # unit [m]

spring_indexs = []
for i in range(num_point):
    for j in range(num_point):
        if i!=j:
            spring_indexs.append([i,j])
spring_indexs=np.array(spring_indexs)

spring_stiffness = 1e3  # unit [N/m] a.k.a -> K

gravity = -9.81  # unit [ m /s2]
spring_initial_length = g.calc_spring_length(points_position, spring_indexs)

# for animation
run_time = 15  # unit [s]
dt = 0.01     # unit [s]

fig, ax = plt.subplots()
ax.set_title('Bike animation')
ax.axis('equal')
ax.set_xlim(0, 35)
ax.set_ylim(-5, 20)

ax.plot(np.arange(-10, 40, 0.5), g.ground(np.arange(-10, 40, 0.5)), 'k')  # ground

balls = []
balls.append(plt.Circle(
    (points_position[0][0], points_position[0][1]), wheel_radius, color='r'))
balls.append(plt.Circle(
    (points_position[1][0], points_position[1][1]), wheel_radius))

lines = []
for item in spring_indexs:
    lines.append(ax.plot([points_position[item[0], 0], points_position[item[1], 0]],
                         [points_position[item[0], 1], points_position[item[1], 1]],
                         'o-', markersize=9, markerfacecolor='b'))
for item in balls:
    ax.add_patch(item)

def update(frame):
    global points_position, points_velocity
    # boundary condition 1
    if np.min(points_position[2:, 1] - g.ground(points_position[2:, 0])) < 0:
        print('Max-distance is %.2f m' % (np.max(points_position[:, 0])-start_x))
        sys.exit(0)
    else:
        ax.set_title('Bike animation at %.2f s\n Max-distance is %.2f m' %
                     (frame*dt, np.max(points_position[:, 0])-start_x))

        state_y = points_position[:, 1] - g.ground(points_position[:, 0])
        state_y[0] -= wheel_radius
        state_y[1] -= wheel_radius

        # update position
        points_position += points_velocity*dt

        # update velocity
        spring_length = g.calc_spring_length(points_position, spring_indexs)
        spring_force = g.calc_spring_force(
            spring_length-spring_initial_length, spring_stiffness)

        points_velocity += g.calc_point_acceleration(
            points_position, spring_indexs, spring_force, points_mass)*dt
        points_velocity[:,
                        1] += g.ground_force(state_y, spring_stiffness, points_mass)*dt
        points_velocity[:, 1] += gravity*dt

        # damp the vertical velocity to make the solution stable
        yfliter = state_y * points_velocity[:, 1] > 0
        points_velocity[:, 1][yfliter] *= 0.01
        # boundary condition 2
        if points_position[0, 1] < wheel_radius+g.ground(points_position[0, 0]):
            points_velocity[0, 0] = 2

        # rendering
        for index, item in enumerate(spring_indexs):
            lines[index][0].set_data([points_position[item[0], 0], points_position[item[1], 0]],
                                     [points_position[item[0], 1], points_position[item[1], 1]],)
        for i in [0, 1]:
            balls[i].center = (points_position[i][0], points_position[i][1])

        return lines, balls


ani = FuncAnimation(
    fig,
    update,
    np.arange(1, int(run_time/dt)),  # the length of simulation
    interval=10,
    repeat=False,
)


plt.show()
