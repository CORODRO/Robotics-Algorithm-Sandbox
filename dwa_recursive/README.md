# DWA Recursive Experiment

Experimental local-planning sandbox for combining Dynamic Window Approach ideas with an A* style global plan.

## What Is In Here

- `dynamic_window_approach.py`: local planner experiment.
- `a_star_planner.py`: grid-based global planner support.
- helper modules for node expansion, map generation, scoring, and path visualization.

## Algorithms Used

- Dynamic Window Approach style local planning.
- A* search for global path guidance.
- Grid-map generation and path visualization helpers.

## Notes

- This folder is still experimental and should be treated as a study artifact.
- If you reuse it, start by cleaning interfaces and validating the planner assumptions against your own robot model.
