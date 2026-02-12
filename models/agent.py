from typing import List, Protocol, Tuple

from models.maze import Maze


class Solver(Protocol):
    def __call__(self, maze: Maze) -> List[Tuple[int, int]]: ...


class Agent:
    def __init__(self, maze: Maze, solver: Solver) -> None:
        self.maze = maze
        self.path = solver(maze)
