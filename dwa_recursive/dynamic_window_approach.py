# -*- coding: utf-8 -*-
"""Experimental Dynamic Window Approach local planner combined with a grid-based global plan."""

import math
# Enum is a class in python for creating enumerations, which are a set of symbolic names (members) bound to unique, constant values
from enum import Enum

import matplotlib.pyplot as plt
import numpy as np

from expand_open_neighbors import expand_array
from insert_open_list import insert_open
from generate_test_map import mapgenerator
from select_lowest_cost_node import min_fn
from find_node_index import node_index
from plot_path import visual_path
# import dynamic_window_approach as dwa


def ast( start_dot = np.array([0, 0, 0 , 0.0, 0.0]), target_dot = np.array([0, 5])):
    # Define the dimension of the search field
    x_max = 10
    y_max = 10
    # Define start location
    # Start location [x y]
    start = np.array([int(start_dot[0]), int(start_dot[1])])
    # Define Target location
    # Target location [x y]
    target = np.array([int(target_dot[0]), int(target_dot[1])])
    # Define number of obstacles
    N = 20
    # Call the map generation function
    #[map,obst] = mapgenerator(N, int(start[0]), int(start[1]), int(target[0]), int(target[1]), x_max, y_max)
    [map,obst] = mapgenerator()
    # Locate the target in to the map
    map[target[0], target[1]] = 2
    ## Preliminary procedures

    # CLOSED contains all the nodes that don't have to be evaluated
    # CLOSED ==> X val | Y val |
    # I've created the closed array and initialized it with the starting node because I don't know how to create an empty 1x2 array
    CLOSED = start
    # Put all obstacles on the Closed List
    for i in range(0,np.shape(obst)[1],1):
        CLOSED = np.vstack([CLOSED, [obst[0, i], obst[1, i]]]) # [[obst[0,i],obst[1,i]]
    # Update the dimension of the closed list whit the number of obstacles
    closed_count = i+1
    # Set the starting node as the firs node to expand
    xNode = start[0]
    yNode = start[1]
    # Assign a zero cost to the starting node (heuristic_function)
    path_cost = 0
    # Calculate starting distance to the target (cost_function)
    goal_distance = np.sqrt((target[0] - start[0])**2+(target[1] - start[1])**2)
    # OPEN list stores all the coordinates of all the nodes that have to be expanded, the coordinates of the # parent node and the 3 functions linked to that node: heuristic (distance from the start), cost (distance to the target), heuristic + cost.
    # OPEN ==> IS ON LIST 1/0 |X val |Y val |Parent X val |Parent Y val |h(n) |g(n)|f(n)|
    # Same as CLOSED
    OPEN = np.array([0,0,0,0,0,0,0,0])
    OPEN = np.vstack([OPEN,[0, xNode, yNode, xNode, yNode, path_cost, goal_distance, path_cost + goal_distance]])
    # Update the open list dimension with the first node added
    open_count = 2
    # Set the flag which tells us the impossibility to find a path    
    NoPath = 0
    new_node = []

    ## Main algorithm

    # Here there's the main loop which is iterated until the coordindates are
    # the same of the target node or is impossible to find a path
    while (xNode != target[0] or yNode!=target[1]) and NoPath == 0:
        # Expand the actual node exploring the adjacent nodes
        exp_node = expand_array(xNode, yNode, path_cost, target[0], target[1], CLOSED, x_max, y_max)
        # Counter which counts the number of allowed nodes created
        exp_count = np.shape(exp_node)[0]
        # In this loop we check if a node expanded is already present in the OPEN list and if the cost now calculated has decreased we update his cost.
        if np.any(exp_node):   
            for i in range(0,exp_count,1):
                new_node = 1
                for j in range(1,open_count,1):
                    #Check if the node is already present in the open list
                    if (exp_node[i,0] == OPEN[j,1] and exp_node[i,1] == OPEN[j,2]):
                        # If yes it match the cost values for the same node and take the minimum value
                        OPEN[j,7] = np.amin([OPEN[j,7],exp_node[i,4]])
                        new_node = 0
                        # If the cost has been updated (also if two costs are the same, the one already in OPEN e and the one found by the expansion then update all others parameter.
                        if OPEN[j, 7] == exp_node[i, 4]:
                            #UPDATE PARENTS,gn,hn
                            OPEN[j, 3] = xNode
                            OPEN[j, 4] = yNode
                            OPEN[j, 5] = exp_node[i, 2]
                            OPEN[j, 6] = exp_node[i, 3]
                        #End of minimum fn chec
                    #End of node check
                #End of j for
                # If the flag new_node is still 0 it means the node has never been explored before so it has to be added to the OPEN list
                if new_node == 1 :
                    OPEN = np.vstack([OPEN,[insert_open(exp_node[i,0],exp_node[i,1],xNode,yNode,exp_node[i,2],exp_node[i,3],exp_node[i,4])]])
                    open_count += 1
                #End of insert new element into the OPEN list
            #End of i for

        #Find out the node with the smallest fn
        index_min_node = min_fn(OPEN,open_count,target[0],target[1])
        # La funzione da -1 se non ci sono più nodi da espandere
        if (index_min_node != -1):
            #Set xNode and yNode to the node with minimum fn
            xNode = OPEN[index_min_node,1]
            yNode = OPEN[index_min_node,2]
            #Update the cost of reaching the parent node
            path_cost = OPEN[index_min_node,5]
            #Move the Node to list CLOSED
            CLOSED = np.vstack([CLOSED,[xNode,yNode]])
            closed_count += 1
            # Instead of remove the node from the OPEN list it is set unactive
            OPEN[index_min_node,0] = 0
        else:
            #No path exists to the Target!!
            NoPath = 1#Exits the loop!
        #End of index_min_node check
    #End of While Loop

    #Once algorithm has run The optimal path is generated by starting of at the
    #last node(if it is the target node) and then identifying its parent node
    #until it reaches the start node.This is the optimal path

    i = np.shape(CLOSED)[0]
    # Find the last node inserted in the closed list if everithing worked fine it should be the target node
    xval = CLOSED[i-1,0]
    yval = CLOSED[i-1,1]
    # Control if the last CLOSED node is the target one
    if ((xval == target[0] and yval == target[1])):
        #Traverse OPEN and determine the parent nodes

        Optimal_path = [xval, yval]

        parent_x = OPEN[node_index(OPEN,xval,yval),3]
        parent_y = OPEN[node_index(OPEN,xval,yval),4]
        
        while (parent_x != start[0] or parent_y != start[1]):
            Optimal_path = np.vstack([Optimal_path,[parent_x,parent_y]])
            inode = node_index(OPEN, parent_x, parent_y)
            parent_x = OPEN[inode,3]
            parent_y = OPEN[inode,4]     
        # Print a graphical output
        #visual_path(start,map,Optimal_path[1:np.shape(Optimal_path)[0]+1])
        main(start_dot, target[0], target[1], np.transpose(obst), Optimal_path)
    else:
        print('\n Sorry, No path exists to the Target! \n')
        print(map)

show_animation = True

#Robot Type
class RobotType(Enum):
    # in "Enum" you may access the instance by name or number
    circle = 0    # Round Robot
    rectangle = 1 # Rectuangular Robot - Skid Steering


""" Be AWARE!! SIMULATION INPUTS HERE!!!!!!! """
# Inputs Class--> Uses the robot type function
    # All the Robot inputs are stored here
class Config:
    """
    simulation parameter class
    """

    def __init__(self):
        # robot parameter
        self.max_speed = 5.0  # [m/s]
        self.min_speed = -2  # [m/s]
        self.max_yawrate = 50.0 * math.pi / 180.0  # [rad/s]
        self.max_accel = 30  # [m/ss]
        self.max_dyawrate = 90.0 * math.pi / 180.0  # [rad/s^2]
        self.v_reso = 0.1  # [m/s]
        self.yawrate_reso = 5 * math.pi / 180.0  # [rad/s]
        self.dt = 0.1  # [s] Time tick for motion prediction
        self.predict_time = 1.5  # [s] How much into the future I am looking into
        # Bigger predict_time produces a longer trajectory at faster speed
        # Smaller predict_time produces a shorter trajectory at higher accelerations (but lower speeds)
        # The gains weights define which will be our objective
        self.to_goal_cost_gain = 0.05 #each gain can vary from 0 to 1
        self.speed_cost_gain = 0.5
        self.obstacle_cost_gain = 0.1
        self.path_cost_gain = 0.2
        self.robot_type = RobotType.circle
        # if goal_gain comparable to speed_gain the drone doesn't move

        # if robot_type == RobotType.circle
        # Also used to check if goal is reached in both types
        self.robot_radius = 0.55  # [m] for collision check

        # if robot_type == RobotType.rectangle
        self.robot_width = 0.5  # [m] for collision check
        self.robot_length = 1.2  # [m] for collision check

    @property
    def robot_type(self):
        # Underscore indicates private variables in Python
        return self._robot_type

    @robot_type.setter
    def robot_type(self, value):
        if not isinstance(value, RobotType):
            raise TypeError("robot_type must be an instance of RobotType")
        self._robot_type = value



def dwa_control(x, config, goal, ob, pt):
    """
    Dynamic Window Approach control:
        x = position vector (x,y,phi)
        config = Type of robot from Config() Class
        goal =
        ob =
    """

    dw = calc_dynamic_window(x, config)

    u, trajectory = calc_control_and_trajectory(x, dw, config, goal, ob, pt)

    return u, trajectory


def motion(x, u, dt):
    """
    motion model --> Kinematic Model
    We have two controls:
    u(0) = velocity
    u(1) = yaw_rate
    And we have 5 variables
    x(0:4) = x, y, yaw, ...?

    """

    x[2] += u[1] * dt    # Yaw angle [rad]
    x[0] += u[0] * math.cos(x[2]) * dt   # x [m]
    x[1] += u[0] * math.sin(x[2]) * dt   # y [m]
    x[3] = u[0] # V [m/s]
    x[4] = u[1] # omega [rad/s]

    return x


def calc_dynamic_window(x, config):
    """
    calculation dynamic window based on current state x --> How much I am seeing in the future?
    x = initial state [x(m), y(m), yaw(rad), v(m/s), omega(rad/s)]
    """

    # Dynamic window from robot specification
    Vs = [config.min_speed, config.max_speed,
          -config.max_yawrate, config.max_yawrate]

    # Dynamic window from motion model
    Vd = [x[3] - config.max_accel * config.dt,
          x[3] + config.max_accel * config.dt,
          x[4] - config.max_dyawrate * config.dt,
          x[4] + config.max_dyawrate * config.dt]

    #  [vmin, vmax, yaw_rate min, yaw_rate max]
    dw = [max(Vs[0], Vd[0]), min(Vs[1], Vd[1]),
         max(Vs[2], Vd[2]), min(Vs[3], Vd[3])] 

    return dw


def predict_trajectory(x_init, v, y, config):
    """
    predict trajectory with an input
    """

    x = np.array(x_init)
    traj = np.array(x)
    time = 0
    while time <= config.predict_time:

        x = motion(x, [v, y], config.dt)
        traj = np.vstack((traj, x))
        time += config.dt

    return traj


def calc_control_and_trajectory(x, dw, config, goal, ob, pt):
    """
    calculation final input with dynamic window
    x= initial state [x(m), y(m), yaw(rad), v(m/s), yaw_rate(rad/s)]
    dw=
    config=
    goal=
    on=
    """

    x_init = x[:]
    min_cost = float("inf")
    best_u = [0.0, 0.0]
    best_trajectory = np.array([x])


    # Apro il nuovo file per la scrittura
    txt = open("Log_cost", "a")

    # evaluate all trajectory with sampled input in dynamic window
    for v in np.arange(dw[0], dw[1], config.v_reso):
        for y in np.arange(dw[2], dw[3], config.yawrate_reso):

            trajectory = predict_trajectory(x_init, v, y, config)

            txt.write("\n---Velocità: " + str(v) + "\tVelocità angolare: " + str(y))

            # calc cost
            to_goal_cost = config.to_goal_cost_gain * calc_to_goal_cost(trajectory, goal)
            speed_cost = config.speed_cost_gain * (config.max_speed - trajectory[-1, 3])
            ob_cost = config.obstacle_cost_gain * calc_obstacle_cost(trajectory, ob, config)
            pt_cost = config.path_cost_gain * calc_path_cost(trajectory, pt)

            final_cost = to_goal_cost + speed_cost + ob_cost + pt_cost

            txt.write("\n    Goal: " + str(round(to_goal_cost, 4)) + "\tSpeed: " + str(round(speed_cost, 4)) + "\n    Obstacles: " + str(round(ob_cost, 4)) + "\tPath: " + str(round(pt_cost, 4)) + "\n    Total: " + str(round(final_cost, 4)))

            # search minimum trajectory
            if min_cost >= final_cost:
                min_cost = final_cost
                best_u = [v, y]
                best_trajectory = trajectory
        
    txt.write("\n\nBest control:")
    txt.write("\n---Velocità: " + str(best_u[0]) + "\tVelocità angolare: " + str(best_u[1]) + "\n")
    txt.close()


    """ print('to_goal, speed_cost, ob_cost, pt_cost')
    print('{:.2f}, {:.2f}, {:.2f}, {:.2e} -> {:.4f}'.format(to_goal_cost,speed_cost,ob_cost,pt_cost,final_cost))"""

    return best_u, best_trajectory


def calc_obstacle_cost(trajectory, ob, config):
    """
        calc obstacle cost inf: collision
    """
    ox = ob[:, 0]
    oy = ob[:, 1]
    dx = trajectory[:, 0] - ox[:, None]
    dy = trajectory[:, 1] - oy[:, None]
    r = np.hypot(dx, dy)

    if config.robot_type == RobotType.rectangle:
        yaw = trajectory[:, 2]
        rot = np.array([[np.cos(yaw), -np.sin(yaw)], [np.sin(yaw), np.cos(yaw)]])
        rot = np.transpose(rot, [2, 0, 1])
        local_ob = ob[:, None] - trajectory[:, 0:2]
        local_ob = local_ob.reshape(-1, local_ob.shape[-1])
        local_ob = np.array([local_ob @ x for x in rot])
        local_ob = local_ob.reshape(-1, local_ob.shape[-1])
        upper_check = local_ob[:, 0] <= config.robot_length / 2
        right_check = local_ob[:, 1] <= config.robot_width / 2
        bottom_check = local_ob[:, 0] >= -config.robot_length / 2
        left_check = local_ob[:, 1] >= -config.robot_width / 2
        if (np.logical_and(np.logical_and(upper_check, right_check),
                           np.logical_and(bottom_check, left_check))).any():
            return float("Inf")
    elif config.robot_type == RobotType.circle:
        if (r <= config.robot_radius).any():
            return float("Inf")

    min_r = np.min(r)
    return 1.0 / min_r  # OK


def calc_to_goal_cost(trajectory, goal):
    """
        calc to goal cost with angle difference
    """

    dx = goal[0] - trajectory[-1, 0]
    dy = goal[1] - trajectory[-1, 1]
    error_angle = math.atan2(dy, dx)
    cost_angle = error_angle - trajectory[-1, 2]
    cost = abs(math.atan2(math.sin(cost_angle), math.cos(cost_angle)))
    #cost = abs(dx**2 + dy**2) * cost

    return cost

def calc_path_cost(trajectory, pt):
    """
        calc the cost outside the path
    """
    cost = 0
    for j in range(0,len(trajectory)):
        x = trajectory[j, 0]
        y = trajectory[j, 1]
        flag = 0
        for i in range(0,len(pt)):
            px = pt[i,0]
            py = pt[i,1]
            if (abs(x-px)<0.5 and abs(y-py)<0.5):
                flag = 1
        if flag == 0:
            cost += 1

    return cost

def plot_arrow(x, y, yaw, length=0.5, width=0.1):  # pragma: no cover
    plt.arrow(x, y, length * math.cos(yaw), length * math.sin(yaw),
              head_length=width, head_width=width)
    plt.plot(x, y)


def plot_robot(x, y, yaw, config):  # pragma: no cover
    if config.robot_type == RobotType.rectangle:
        outline = np.array([[-config.robot_length / 2, config.robot_length / 2,
                             (config.robot_length / 2), -config.robot_length / 2,
                             -config.robot_length / 2],
                            [config.robot_width / 2, config.robot_width / 2,
                             - config.robot_width / 2, -config.robot_width / 2,
                             config.robot_width / 2]])
        Rot1 = np.array([[math.cos(yaw), math.sin(yaw)],
                         [-math.sin(yaw), math.cos(yaw)]])
        outline = (outline.T.dot(Rot1)).T
        outline[0, :] += x
        outline[1, :] += y
        plt.plot(np.array(outline[0, :]).flatten(),
                 np.array(outline[1, :]).flatten(), "-k")
    elif config.robot_type == RobotType.circle:
        circle = plt.Circle((x, y), config.robot_radius, color="b")
        plt.gcf().gca().add_artist(circle)
        out_x, out_y = (np.array([x, y]) +
                        np.array([np.cos(yaw), np.sin(yaw)]) * config.robot_radius)
        plt.plot([x, out_x], [y, out_y], "-k")


""" Be AWARE!! SIMULATION INPUTS HERE!!!!!!! """
def main(start, gx, gy, ob, pt, robot_type=RobotType.circle):
    print(__file__ + " start!!")
    # Apro il file per il salvataggio degli stati
    file = open("Log_states.txt","w")
    file.write( "\t" + "x" + "\t\t" + "y" + "\t" + "theta" + "\t" + "V" + "\t\t" + "omega" )
    file.close()
    # Cancello il file precedente per il salvataggio dei costi
    txt = open("Log_cost", "w")
    txt.close()
    
    # initial state [x(m), y(m), yaw(rad), v(m/s), omega(rad/s)]
    #x = np.array([sx, sy, math.pi / 8.0, 0.0, 0.0])
    x = start
    # goal position [x(m), y(m)]
    """ FINAL OBJECTIVE""" # --> Maybe our final waypoint or the waypoints defined from A*
    goal = np.array([gx, gy])
   
    """ OBSTACLES"""
    # obstacles [x(m) y(m), ....] --> Cells with Obstacles in x, y --> From Path Planning
    # We have to make sure we can feed a new matrix while computing (i.e. for new obstacles recognition)
    
    # input [forward speed, yaw_rate]
    config = Config() # Kinetic Definition Robot
    config.robot_type = robot_type
    trajectory = np.array(x)

    time_ellapsed = 0
    ttt = 0
    dist_to_goal=0
    while True:
        file = open("Log_states.txt","a")
        # u, predicted_trajectory is UNPACKING a vector returned by dwa_control
        # which is made by best_u (best control) and best trajectory found
        u, predicted_trajectory = dwa_control(x, config, goal, ob, pt) # --> How much in the future I am looking into?
        x = motion(x, u, config.dt)  # simulate robot
        file.write("\n" + str(round(x[0], 4)) + "\t" + str(round(x[1], 4)) + "\t" + str(round(x[2], 4)) + "\t" + str(round(x[3], 4)) + "\t" + str(round(x[4], 4)) )
        file.close()
        trajectory = np.vstack((trajectory, x))  # store state history
        time_ellapsed += config.dt
        if time_ellapsed > config.predict_time * 800000:
            print(trajectory)
            ast(trajectory[-1,:], goal)
        if show_animation:
            ttt +=config.dt
            plt.cla()
            plt.title("u(0)=V={:+3.2f} m/s, u(1)=dot(psi)={:+05.2f} rad/s, goal={:+05.2f} m".format(u[0],u[1],dist_to_goal))
            # for stopping simulation with the esc key.
            plt.gcf().canvas.mpl_connect('key_release_event',
                    lambda event: [exit(0) if event.key == 'escape' else None])
            plt.plot(predicted_trajectory[:, 0], predicted_trajectory[:, 1], "-g")
            plt.plot(x[0], x[1], "xr")
            plt.plot(goal[0], goal[1], "xb")
            plt.plot(pt[:,0], pt[:,1], "og")
            plt.plot(ob[:, 0], ob[:, 1], "ok")
            plot_robot(x[0], x[1], x[2], config)
            plot_arrow(x[0], x[1], x[2])
            plt.axis("equal")
            plt.grid(True)
            plt.pause(0.0001)


        # check reaching goal
        dist_to_goal = math.hypot(x[0] - goal[0], x[1] - goal[1])
        if dist_to_goal <= config.robot_radius:
            print("Goal!!")
            file.close()
            break

    print("Done")
    if show_animation:
        plt.plot(trajectory[:, 0], trajectory[:, 1], "-r")
        plt.pause(0.0001)

    plt.show()


"""if __name__ == '__main__':
    main(robot_type=RobotType.circle) """
ast()