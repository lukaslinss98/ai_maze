# Maze Pathfinding & MDP Solver

## Overview

This project is an implementation for an Artificial Intelligence module that demonstrates various AI
concepts including:

- **Uninformed Search Algorithms**
- **Informed Search Algorithms**
- **Markov Decision Processes (MDPs)**

The project provides a comprehensive framework for maze generation, pathfinding, and decision-making
under uncertainty.

## Project Structure

```
.
├── algorithms/          # Core algorithm implementations
│   ├── algorithms.py    # General algorithm interfaces
│   └── pathfinding.py   # Pathfinding algorithms (A*, BFS, DFS, etc.)
├── mdp/                 # Markov Decision Process implementation
│   └── mdp.py          # MDP solver with value/policy iteration
├── models/             # Data models and representations
│   ├── agent.py        # Agent representation
│   ├── cell.py         # Maze cell structure
│   ├── direction.py    # Direction enumerations
│   └── maze.py         # Maze representation and logic
├── util/               # Utility functions
│   ├── colors.py       # Color schemes for visualization
│   ├── datastructures.py # Custom data structures
│   └── maze_generation.py # Maze generation algorithms
└── main.py             # Main entry point
```

## Features

### Pathfinding Algorithms

- **Uninformed Search**
  - Breadth-First Search (BFS)
  - Depth-First Search (DFS)
  - Uniform Cost Search
- **Informed Search**
  - A\* Search
  - Greedy Best-First Search
  - Other heuristic-based algorithms

### Markov Decision Processes

- Value Iteration
- Policy Iteration
- Optimal policy computation for stochastic environments
- Support for different reward structures

### Maze Generation

- Multiple maze generation algorithms
- Customizable maze sizes and complexity
- Visual representation with color coding

## Installation

1. Clone the repository:

```bash
git clone [repository-url]
cd [project-directory]
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

_Note: Check `pyproject.toml` for specific package requirements_

## Usage

Run the main program:

```bash
python3 -m main
```

## Key Components

### Models

- **Agent**: Represents an entity navigating the maze
- **Cell**: Individual maze cells with properties (walls, rewards, etc.)
- **Direction**: Enumeration for movement directions
- **Maze**: Complete maze representation with methods for manipulation

### Algorithms

- Modular design allowing easy addition of new algorithms
- Common interface for all pathfinding algorithms
- Performance metrics and comparison capabilities

### MDP Module

- Handles stochastic environments
- Computes optimal policies considering uncertainty
- Supports various discount factors and convergence criteria

## Academic Context

This project demonstrates understanding of:

1. **Search Algorithms**: Both uninformed and informed strategies
2. **Heuristics**: Design and implementation for informed search
3. **Decision Making**: Optimal decision-making in uncertain environments
4. **Algorithm Comparison**: Time/space complexity analysis

## Future Enhancements

- [ ] Reinforcement Learning integration
- [ ] More sophisticated visualization
- [ ] Additional maze generation algorithms
- [ ] Performance benchmarking suite
- [ ] Interactive GUI for algorithm visualization

## Requirements

- Python 3.13+
- See `pyproject.toml` for complete dependency list

## License

This project is created for academic purposes as part of an Artificial Intelligence module.

---

**Course**: Artificial Intelligence Module  
**Topics Covered**: Uninformed Search, Informed Search, Markov Decision Processes
