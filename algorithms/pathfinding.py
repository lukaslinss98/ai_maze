from abc import ABC, abstractmethod
from typing import List

from models.cell import Cell
from models.maze import Maze


class PathfindingAlgorithm(ABC):
    @abstractmethod
    def solve(self, maze: Maze) -> List[Cell]:
        pass


class DFS(PathfindingAlgorithm):
    def solve(self, maze: Maze) -> List[Cell]:
        pass


class BFS(PathfindingAlgorithm):
    def solve(self, maze: Maze) -> List[Cell]:
        pass
