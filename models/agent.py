from typing import List, Protocol

import pygame

from algorithms.pathfinding import PathFindingResult
from models.cell import Open
from models.maze import Maze


class Solver(Protocol):
    def solve(self, maze: Maze, start: Open) -> PathFindingResult: ...


class Agent:
    def __init__(self, maze: Maze, solver: Solver) -> None:
        self.maze: Maze = maze
        self.curr: Open = maze.start
        self.curr_i: int = 0
        self.pathfinding_result: PathFindingResult = solver.solve(maze, self.curr)

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
            pygame.draw.circle(screen, (0, 240, 0), (px, py), cell_size // 4)

    def step(self) -> bool:
        len_visited = len(self.pathfinding_result.visited)
        len_curr_i = self.curr_i + 1

        if len_visited > len_curr_i:
            self.curr = self.pathfinding_result.visited[self.curr_i + 1]
            self.curr_i += 1

        return len_visited == len_curr_i
