import math
from typing import Protocol

import pygame

from algorithms.algorithms import BFS, DFS, AStar, PathFindingResult
from models.cell import Open
from models.maze import Maze

chebyshev = lambda c1, c2: max(abs(c2.x - c1.x), abs(c2.y - c1.y))
euclidean_distance = lambda c1, c2: math.sqrt((c2.x - c1.x) ** 2 + (c1.y - c2.y) ** 2)
manhatten_distance = lambda c1, c2: abs(c1.x - c2.x) + abs(c1.y - c2.y)


class Solver(Protocol):
    def solve(self, maze: Maze, start: Open) -> PathFindingResult: ...


class Agent:
    def __init__(self, maze: Maze, solver: str) -> None:
        self.maze: Maze = maze
        self.curr: Open = maze.start
        self.curr_i: int = 0
        self.solver = self._create_solver(solver)
        self.pathfinding_result: PathFindingResult = self.solver.solve(maze, self.curr)

    def draw(self, screen: pygame.Surface, cell_size: int = 32) -> None:
        sub_path = self.pathfinding_result.visited[: self.curr_i + 1]
        for i, cell in enumerate(sub_path):
            px, py = (
                (cell.y * cell_size) + cell_size / 2,
                (cell.x * cell_size) + cell_size / 2,
            )
            color = (0, 240, 0) if i == len(sub_path) - 1 else (128, 0, 128)
            pygame.draw.circle(screen, color, (px, py), cell_size // 4)

    def draw_shortest_path(self, screen: pygame.Surface, cell_size: int = 32) -> None:
        shortest_path = self.pathfinding_result.shortest_path
        for cell in shortest_path:
            px, py = (
                (cell.y * cell_size) + cell_size / 2,
                (cell.x * cell_size) + cell_size / 2,
            )
            pygame.draw.circle(screen, (0, 230, 0), (px, py), cell_size // 3.5)

    def step(self) -> bool:
        len_visited = len(self.pathfinding_result.visited)
        len_curr_i = self.curr_i + 1

        if len_visited > len_curr_i:
            self.curr = self.pathfinding_result.visited[self.curr_i + 1]
            self.curr_i += 1

        return len_visited == len_curr_i

    def _create_solver(self, solver: str | None) -> Solver:
        if solver == 'bfs':
            return BFS()
        elif solver == 'dfs':
            return DFS()
        elif solver == 'astar_manhatten':
            return AStar(heuristic=manhatten_distance)
        elif solver == 'astar_euclid':
            return AStar(heuristic=euclidean_distance)
        elif solver == 'astar_chebyshev':
            return AStar(heuristic=chebyshev)
        else:
            return DFS()
