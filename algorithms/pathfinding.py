from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass
from typing import Callable, Dict, List, OrderedDict

from models.cell import Cell, Open
from models.maze import Maze
from util.datastructures import PriorityQueue


@dataclass(frozen=True)
class PathFindingResult:
    visited: List[Open]
    shortest_path: List[Open]


class PathfindingAlgorithm(ABC):
    @abstractmethod
    def solve(self, maze: Maze, start: Open) -> PathFindingResult:
        pass


class DFS(PathfindingAlgorithm):
    def solve(self, maze: Maze, start: Open) -> PathFindingResult:
        stack = [start]
        visited = OrderedDict.fromkeys([])
        parent_map: Dict[Open, Open | None] = {start: None}

        while stack:
            curr = stack.pop()

            if curr == maze.end:
                shortest_path = []
                at = curr
                while at:
                    shortest_path.append(at)
                    at = parent_map.get(at)

                return PathFindingResult(list(visited.keys()), shortest_path)

            if curr in visited:
                continue

            visited[curr] = None

            for _, neighbors in maze.neighbors(curr):
                if neighbors not in visited:
                    stack.append(neighbors)
                    parent_map[neighbors] = curr

        return PathFindingResult(list(visited.keys()), [])


class BFS(PathfindingAlgorithm):
    def solve(self, maze: Maze, start: Open) -> PathFindingResult:
        queue = deque([start])
        visited = OrderedDict.fromkeys([])
        parent_map: Dict[Open, Open | None] = {start: None}

        visited[start] = None
        while queue:
            curr = queue.popleft()

            if curr == maze.end:
                shortest_path = []
                at = curr
                while at:
                    shortest_path.append(at)
                    at = parent_map.get(at)

                return PathFindingResult(list(visited.keys()), shortest_path)

            for _, neighbor in maze.neighbors(curr):
                if neighbor not in visited:
                    visited[neighbor] = None
                    queue.append(neighbor)
                    parent_map[neighbor] = curr

        return PathFindingResult(list(visited.keys()), [])


class AStar(PathfindingAlgorithm):
    def __init__(self, heuristic: Callable[[Cell, Cell], float]) -> None:
        self.heuistic = heuristic

    def solve(self, maze: Maze, start: Open) -> PathFindingResult:
        priority_queue = PriorityQueue()

        visited = OrderedDict.fromkeys([])
        parent_by_cell: Dict[Open, Open | None] = {start: None}
        path_cost_by_cell = {start: 0.0}

        priority_queue.push(start, 1.0)
        visited[start] = None
        while priority_queue:
            curr = priority_queue.pop()

            if curr == maze.end:
                shortest_path = []
                at = curr
                while at:
                    shortest_path.append(at)
                    at = parent_by_cell.get(at)

                return PathFindingResult(list(visited.keys()), shortest_path)

            for _, neighbor in maze.neighbors(curr):
                if neighbor not in visited:
                    visited[neighbor] = None
                    path_cost_by_cell[neighbor] = path_cost_by_cell[curr] + 1.0

                    f = self.heuistic(neighbor, maze.end) + path_cost_by_cell[neighbor]

                    priority_queue.push(neighbor, f)
                    parent_by_cell[neighbor] = curr

        return PathFindingResult(list(visited.keys()), [])
