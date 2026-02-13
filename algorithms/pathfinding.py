from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass
from typing import Dict, List, OrderedDict

from models.cell import Open
from models.maze import Maze


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

            for neighbors in maze.neighbors(curr):
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

            for neighbors in maze.neighbors(curr):
                if neighbors not in visited:
                    visited[neighbors] = None
                    queue.append(neighbors)
                    parent_map[neighbors] = curr

        return PathFindingResult(list(visited.keys()), [])


class AStar(PathfindingAlgorithm):
    def solve(self, maze: Maze, start: Open) -> PathFindingResult:
        pass
