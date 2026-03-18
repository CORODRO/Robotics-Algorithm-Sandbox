# Legacy Navigation and Planning Examples

Archived planning and estimation scripts that were explored during development but were not the final operational stack.

## Included Algorithms

- D*
- Depth-first search planning
- EKF
- FastSLAM
- MPC
- Stanley controller
- Quintic polynomial planning

## Script Guide

- `d_star_planner.py`: D* path-planning example.
- `depth_first_search_planner.py`: graph-search baseline using depth-first search.
- `ekf_localization_demo.py`: EKF localization/SLAM study example.
- `fastslam_demo.py`: particle-based SLAM example.
- `mpc_demo.py`: model-predictive-control driving example.
- `quintic_polynomial_planner.py`: smooth trajectory generation with quintic polynomials.
- `stanley_controller_demo.py`: path-tracking example based on the Stanley controller.

## Best Use

Read these files as references and study material. They are useful for comparing alternative approaches against the final navigation stack used in the mission.

Several scripts in this folder are adapted from public robotics teaching examples. Read them as algorithm references rather than mission-ready packages.
