# CORODRO Algorithm Sandbox

Teaching-oriented archive of prototype scripts, robotics experiments, and algorithm exercises that informed the CORODRO project. This repository is the right place to learn ideas quickly without loading the full mission stack.

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

## Recommended Learning Path

1. Read the top-level ROS examples if you are new to ROS nodes.
2. Move to `ai_general/` for simple algorithm exercises.
3. Explore `legacy_navigation_planning/` for classic robotics algorithms.
4. Finish with `dwa_recursive/` if you want to study a more integrated planning experiment.

## Top-Level Script Guide

- `Cv_bridge_demo.py`: converts depth-camera data into a colorized DEM-style visualization.
- `Fake_localization_node_for_ROS.py`: publishes simple localization information for navigation tests.
- `Fake_mapper_node_ROS.py`: lightweight fake map publisher for planner testing.
- `First_teleop_code_implemented_in_python.py`: early teleoperation experiment.
- `create_map_ROS.py`: lidar-to-occupancy-map prototype.
- `laserscan_from_git_used_to_create_ROS_Map.py`: supporting lidar mapping script.
- `ros2opencv2.py`: wrapper between ROS image topics and OpenCV processing.

## Notes For Students

- This repo is intentionally eclectic. Think of it as a lab notebook that has been cleaned up into a teaching archive.
- The code quality varies by file because some scripts were written as prototypes or learning exercises.
