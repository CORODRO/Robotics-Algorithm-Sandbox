# CORODRO Algorithm Sandbox

Teaching-oriented archive of prototype scripts, robotics experiments, and algorithm exercises that informed the CORODRO project. This repository is the right place to learn ideas quickly without loading the full mission stack.

The filenames in this repo have been normalized to descriptive `snake_case` names so students can understand the intent of a script before opening it.

Most scripts now parse under Python 3. The top-level perception and teleoperation demos still require a ROS 1 environment with packages such as `rospy`, `sensor_msgs`, `geometry_msgs`, and `cv_bridge`.

## Added Value

- Small scripts that are easier to read than the mission code.
- Early robotics experiments preserved as learning material.
- A student-friendly catalogue of planning, localization, and reinforcement-learning examples.

## Algorithms Used

- Occupancy-grid mapping from lidar data.
- ROS image and OpenCV bridging.
- Q-learning and simple MDP examples.
- A*, D*, FastSLAM, EKF, MPC, Stanley control, and quintic polynomial planning examples.
- Experimental DWA plus A* integration.

## Repository Map

- `ai_general/`: reinforcement learning and optimization exercises.
- `dwa_recursive/`: experimental DWA implementation with A* support.
- `legacy_navigation_planning/`: older planning and SLAM examples not used directly in the final mission stack.
- top-level scripts: small ROS mapping, localization, teleoperation, and perception demos.

## Quick Start

1. Start with `ai_general/` if you want standalone Python examples with no ROS dependency.
2. Move to `legacy_navigation_planning/` for readable reference implementations of classical robotics algorithms.
3. Use the top-level scripts only once you already have ROS 1 and the sensor/message dependencies installed.
4. Treat `dwa_recursive/` as an experimental sandbox rather than a polished planner package.

## Recommended Learning Path

1. Read the top-level ROS examples if you are new to ROS nodes.
2. Move to `ai_general/` for simple algorithm exercises.
3. Explore `legacy_navigation_planning/` for classic robotics algorithms.
4. Finish with `dwa_recursive/` if you want to study a more integrated planning experiment.

## Top-Level Script Guide

- `depth_camera_cv_bridge_demo.py`: ROS/OpenCV demo that converts depth-camera data into a colorized DEM-style visualization.
- `fake_localization_node.py`: ROS helper that publishes simple localization information for navigation tests.
- `fake_mapper_node.py`: ROS helper that publishes a lightweight fake map for planner testing.
- `keyboard_teleop_experiment.py`: ROS keyboard teleoperation experiment.
- `lidar_occupancy_map_builder.py`: ROS lidar-to-occupancy-map prototype.
- `lidar_scan_to_occupancy_grid.py`: ROS LaserScan-to-OccupancyGrid utility.
- `ros_image_to_opencv_bridge.py`: reusable ROS image bridge for OpenCV processing experiments.

## Best First Files

- `ai_general/simple_q_learning_demo.py`: smallest reinforcement-learning example in the repo.
- `ai_general/dynamic_programming_knapsack.py`: compact dynamic-programming example.
- `legacy_navigation_planning/quintic_polynomial_planner.py`: clean trajectory-generation example.
- `dwa_recursive/a_star_planner.py`: readable grid-search helper before opening the larger DWA experiment.

## Notes For Students

- This repo is intentionally eclectic. Think of it as a lab notebook that has been cleaned up into a teaching archive.
- The code quality varies by file because some scripts were written as prototypes or learning exercises.
