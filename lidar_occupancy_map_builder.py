#!/usr/bin/env python
"""Prototype ROS node that builds an occupancy grid from lidar scans and TF data."""

import rospy
import tf
from nav_msgs.msg import OccupancyGrid
from sensor_msgs.msg import LaserScan
from math import sin, cos
import numpy as np


class Create_Map():
    """
         Messages to Handle:
         nav_msgs/OccupancyGrid Message
         nav_msgs/OccupancyGrid.header.seq --> consecutively increasing ID 
         nav_msgs/OccupancyGrid.header.stamp -->T wo-integer timestamp
         nav_msgs/OccupancyGrid.header.frame_id --> Frame this data is associated with
         
         nav_msgs/OccupancyGrid.MapMetaData.time --> The time at which the map was loaded
         nav_msgs/OccupancyGrid.MapMetaData.resolution --> The map resolution [m/cell]
         nav_msgs/OccupancyGrid.MapMetaData.width --> Map width [cells]
         nav_msgs/OccupancyGrid.MapMetaData.height --> # Map height [cells]
         nav_msgs/OccupancyGrid.MapMetaData.Pose.Point --> # The origin of the map [m, m, rad].  This is the real-world pose of the cell (0,0) in the map.
         nav_msgs/OccupancyGrid.MapMetaData.Pose.Quaternions --> # The origin of the map [m, m, rad].  This is the real-world pose of the cell (0,0) in the map.
         
         nav_msgs/OccupancyGrid.data --> # The map data, in row-major order, starting with (0,0).  Occupancy probabilities are in the range [0,100].  Unknown is -1.
        
    """
    def __init__(self):
        # initialize node
        rospy.init_node('Create_map')
        
        # Initialize occupancy grid message
        map_msg = OccupancyGrid()
        map_msg.header.frame_id = 'map'

        # Map Metadata: origin, resolution, width, height, grid
        self.origin_x = rospy.get_param('~origin_x', 0)  #[m]
        self.origin_y = rospy.get_param('~origin_y', 0)  #[m]
        self.resolution = rospy.get_param('~resolution', 1)  #[m]
        self.width = rospy.get_param('~width', 500)  #[m]
        self.height = rospy.get_param('~height', 500)  #[m]
        self.grid = np.zeros((self.height, self.width))       
        
        # Understand the rover pose between base_link and the world frame
        self.rover_pose=tf.TransformListener()
        # Set the footprint of the rover and initialize rover position
        self.rover_footprint = rospy.get_param('rover_footprint ', 0.1)  #[m]
        # initial rover pose at the start of the simulation
        self.x_rover_init = rospy.get_param('~x_rover_init', 0)  #[m]
        self.y_rover_init = rospy.get_param('~y_rover_init', 0)  #[m]
        # Initialize Pose of the rover relative to the word
        self.x_rover = self.x_rover_init
        self.y_rover = self.y_rover_init
        # Map update rate(default to 5 Hz) --> Usually the map update rate is low
        self.map_rate = rospy.get_param('~map_rate', 5)  #[Hz]
        # Range data
        self.rover_range = 0.0
        # Initialize rover position
        self.position =[0,0]
        # rover footprint in the map to set 
        self.size = int(self.rover_footprint//self.resolution)
        
        rospy.loginfo('Subscribing to Laser')
        # Subscribe to laser
        range_sub = rospy.Subscriber("/scan", LaserScan, self.scan_callback, queue_size=1)
        # Publish in occupancy grid
        occ_pub = rospy.Publisher("/map", OccupancyGrid, queue_size = 1)
        # fill default map_messages
        map_msg.info.resolution = self.resolution
        map_msg.info.width = self.width
        map_msg.info.height = self.height
        map_msg.data = range(self.width*self.height)
        
        # initialize grid with 0 (free)
        self.grid = np.ndarray((self.width, self.height), buffer=np.zeros((self.width, self.height), dtype=np.int),dtype=np.int)
        self.grid.fill(int(0))
        
        # set map origin [meters]
        map_msg.info.origin.position.x = - self.width // 2 * self.resolution
        map_msg.info.origin.position.y = - self.height // 2 * self.resolution
        
        loop_rate = rospy.Rate(self.map_rate)
        
        while not rospy.is_shutdown():
            try:
                #  For now we sent the global ref. system in odom
                t = self.rover_pose.getLatestCommonTime("/base_footprint", "/odom")
                self.position, self.quaternion = self.rover_pose.lookupTransform("/odom", "/base_footprint", t)
            except(tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                continue
            
            try:
                t = self.rover_pose.getLatestCommonTime("/base_footprint", "/kinect_depth_frame")
                self.position_laser, self.quaternion_laser = self.rover_pose.lookupTransform("/base_footprint", "/kinect_depth_frame", t)
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                continue

            # write 0 (null obstacle probability) to the free areas in grid
            self.set_free_cells()
            
            # write p>0 (non-null obstacle probability) to the occupied areas in grid
            self.set_obstacle()
            
            # stamp current ros time to the message
            map_msg.header.stamp = rospy.Time.now()
            
            # build ros map message and publish
            for i in range(self.width*self.height):
                map_msg.data[i] = self.grid.flat[i]
            occ_pub.publish(map_msg)
            
            loop_rate.sleep()
                

    def set_free_cells(self):
        # set free the cells 
        # grid:				ndarray [width,height]
        # position:			[x y] pose of the car
        # size: 			r     radius of the footprint
        
        off_x = self.position[1] // self.resolution + self.width  // 2
        off_y = self.position[0] // self.resolution + self.height // 2
        
        # known free positions
        for i in range(-self.size//2, self.size//2):
            for j in range(-self.size//2, self.size//2):
                self.grid[int(i + off_x), int(j + off_y)] = 1
                
    def set_obstacle(self):
        # set the occupied cells when detecting an obstacle
        # grid:				ndarray [width,height]
        # position:			[x y] pose of the car
        # orientation:      quaternion, orientation of the car
        
        off_x = self.position[1] // self.resolution + self.width  // 2
        off_y = self.position[0] // self.resolution + self.height // 2
        euler = tf.transformations.euler_from_quaternion(self.quaternion)
        
        if not self.rover_range == 0.0:
            rotMatrix = np.array([[cos(euler[2]),   sin(euler[2])],
                                     [-sin(euler[2]),  cos(euler[2])]])
            self.obstacle = np.dot(rotMatrix,np.array([0, (self.rover_range + self.position_laser[0]) // self.resolution])) + np.array([off_x, off_y])
            rospy.loginfo("FOUND OBSTACLE AT: x:%f y:%f", self.obstacle[0], self.obstacle[1])
            
            # set probability of occupancy to 100 and neighbour cells to 50
            self.grid[int(self.obstacle[0]), int(self.obstacle[1])] = int(100)
            if  self.grid[int(self.obstacle[0]+1), int(self.obstacle[1])]   < int(1):
                self.grid[int(self.obstacle[0]+1), int(self.obstacle[1])]   = int(50)
            if  self.grid[int(self.obstacle[0]),   int(self.obstacle[1]+1)] < int(1):
                self.grid[int(self.obstacle[0]),   int(self.obstacle[1]+1)] = int(50)
            if  self.grid[int(self.obstacle[0]-1), int(self.obstacle[1])]   < int(1):
                self.grid[int(self.obstacle[0]-1), int(self.obstacle[1])]   = int(50)
            if  self.grid[int(self.obstacle[0]),   int(self.obstacle[1]-1)] < int(1):
                self.grid[int(self.obstacle[0]),   int(self.obstacle[1]-1)] = int(50)
                
            t = 0.5
            i = 1
            
            free_cell = np.dot(rotMatrix,np.array([0, t*i])) + np.array([off_x,off_y])
            while self.grid[int(free_cell[0]), int(free_cell[1])] < int(1):
                self.grid[int(free_cell[0]), int(free_cell[1])] = int(0)
                free_cell = np.dot(rotMatrix,np.array([0, t*i])) + np.array([off_x,off_y])
                i = i+1;
    
    def scan_callback(self,msg):
        self.rover_range = msg.ranges[0]
        
        
if __name__ == '__main__':
    try:
        m = Create_Map()
    except rospy.ROSInterruptException:
        pass