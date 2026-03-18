#!/usr/bin/env python
"""ROS demo node that converts depth-camera images into OpenCV views for quick terrain-visualization experiments."""

import rospy
import sys
import cv2
import cv2 as cv  #older pre-CV libraries
from sensor_msgs.msg import Image, CameraInfo  #from Gazebo sensors
from cv_bridge import CvBridge, CvBridgeError  #ROS images format to OpenCV format
import numpy as np #OpenCv uses np to do the image processing

class cvBridgeDemo():
    def __init__(self):
        self.node_name = "depth_camera_cv_bridge_demo"
        
        rospy.init_node(self.node_name)
        
        # What we do during shutdown
        rospy.on_shutdown(self.cleanup)
        
        # Create the OpenCV display window for the RGB image
        self.cv_window_name = self.node_name
       # cv.NamedWindow(self.cv_window_name, cv.CV_WINDOW_NORMAL)
        cv2.namedWindow(self.cv_window_name, cv2.WINDOW_AUTOSIZE)
        cv2.moveWindow(self.cv_window_name, 25, 75)
        
        # And one for the depth image
        cv2.namedWindow("Depth Image", cv2.WINDOW_AUTOSIZE)
        cv2.moveWindow("Depth Image", 25, 350)
        
        # Create the cv_bridge object
        self.bridge = CvBridge()
        
        # Subscribe to the camera image and depth topics and set
        # the appropriate callbacks
        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw", Image, self.image_callback, queue_size=1)
        self.depth_sub = rospy.Subscriber("/camera/depth/image_raw", Image, self.depth_callback, queue_size=1)
        
        rospy.loginfo("Waiting for image topics...")
        rospy.wait_for_message("/camera/rgb/image_raw", Image)
        rospy.loginfo("Ready.")

    def image_callback(self, ros_image):
        # Use cv_bridge() to convert the ROS image to OpenCV format
        try:
            frame = self.bridge.imgmsg_to_cv2(ros_image, "bgr8")
        except CvBridgeError as e:
            print(e)
            return
        
        # Convert the image to a numpy array since most cv2 functions
        # require numpy arrays.
        frame = np.array(frame, dtype=np.uint8)
        
        # Process the frame using the process_image() function
        display_image = self.process_image(frame)
                       
        # Display the image.
        cv2.imshow(self.node_name, display_image)
        
        # Process any keyboard commands
        self.keystroke = cv2.waitKey(5)
        if self.keystroke != -1:
            cc = chr(self.keystroke & 255).lower()
            if cc == 'q':
                # The user has press the q key, so exit
                rospy.signal_shutdown("User hit q key to quit.")
                
    def depth_callback(self, ros_image):
        # Use cv_bridge() to convert the ROS image to OpenCV format
        try:
            # Convert the depth image using the default passthrough encoding
            depth_image = self.bridge.imgmsg_to_cv2(ros_image, "passthrough")
        except CvBridgeError as e:
            print(e)
            return

        # Convert the depth image to a Numpy array since most cv2 functions require Numpy arrays.
        depth_array = np.array(depth_image, dtype=np.float32)
                
        # Normalize the depth image to fall between 0 (black) and 1 (white)
        cv2.normalize(depth_array, depth_array, 0, 1, cv2.NORM_MINMAX)
        
        # Process the depth image
        depth_display_image = self.process_depth_image(depth_array)
    
        # Display the result
        cv2.imshow("Depth Image", depth_display_image)
          
    def process_image(self, frame):
        # Convert to greyscale
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Blur the image
        grey = cv2.blur(grey, (7, 7))
        
        # Compute edges using the Canny edge filter
        edges = cv2.Canny(grey, 15.0, 30.0)
        
        return edges
    
    def process_depth_image(self, frame):
        # Just return the raw image for this demo
        return frame
    
    def cleanup(self):
        print("Shutting down vision node.")
        cv2.destroyAllWindows()
    
def main(args):       
    try:
        cvBridgeDemo()
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down vision node.")
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
