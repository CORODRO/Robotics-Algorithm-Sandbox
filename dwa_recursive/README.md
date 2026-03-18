# DWA Recursive Experiment

Experimental local-planning sandbox for combining Dynamic Window Approach ideas with an A* style global plan.

## What Is In Here

- `dynamic_window_approach.py`: local planner experiment.
- `a_star_planner.py`: grid-based global planner support.
- `expand_open_neighbors.py`: grid-neighbor expansion helper.
- `insert_open_list.py`: helper for building A* open-list entries.
- `generate_test_map.py`: simple map generator for planner experiments.
- `select_lowest_cost_node.py`: helper for choosing the next A* node.
- `find_node_index.py`: utility for locating nodes in the open list.
- `plot_path.py`: text-based path-visualization helper.

## Algorithms Used

- Dynamic Window Approach style local planning.
- A* search for global path guidance.
- Grid-map generation and path visualization helpers.

## Notes

- This folder is still experimental and should be treated as a study artifact.
- If you reuse it, start by cleaning interfaces and validating the planner assumptions against your own robot model.
