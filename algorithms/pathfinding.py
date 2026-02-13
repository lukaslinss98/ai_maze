from abc import ABC, abstractmethod
from typing import List

from models.cell import Open
from models.maze import Maze


class PathfindingAlgorithm(ABC):
    @abstractmethod
    def solve(self, maze: Maze, start: Open) -> List[Open]:
        pass


class DFS(PathfindingAlgorithm):
    def solve(self, maze: Maze, start: Open) -> List[Open]:
        stack = []
        visited = []
        curr = start
        while (stack or curr) and curr != maze.end:
            visited.append(curr)
            if curr.north and maze.get(curr, 'north') not in visited:
                stack.append(curr)
                curr = maze.get(curr, 'north')
            elif curr.east and maze.get(curr, 'east') not in visited:
                stack.append(curr)
                curr = maze.get_cell(curr.x, curr.y + 1)
            elif curr.south and maze.get(curr, 'south') not in visited:
                stack.append(curr)
                curr = maze.get_cell(curr.x + 1, curr.y)
            elif curr.west and maze.get(curr, 'west') not in visited:
                stack.append(curr)
                curr = maze.get_cell(curr.x, curr.y - 1)
            else:
                curr = stack.pop()

        if curr == maze.end:
            visited.append(curr)

        return visited


class BFS(PathfindingAlgorithm):
    def solve(self, maze: Maze, start: Open) -> List[Open]:
        pass


class AStar(PathfindingAlgorithm):
    def solve(self, maze: Maze, start: Open) -> List[Open]:
        pass
