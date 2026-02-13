from typing import List, Protocol

import pygame

from models.cell import Open
from models.maze import Maze


class Solver(Protocol):
    def solve(self, maze: Maze, start: Open) -> List[Open]: ...


class Agent:
    def __init__(self, maze: Maze, solver: Solver) -> None:
        self.maze: Maze = maze
        self.curr: Open = maze.start
        self.curr_i: int = 0
        self.path: List[Open] = solver.solve(maze, self.curr)

    def draw(self, screen: pygame.Surface, cell_size: int = 32) -> None:
        sub_path = self.path[: self.curr_i + 1]
        for i, cell in enumerate(sub_path):
            px, py = (
                (cell.y * cell_size) + cell_size / 2,
                (cell.x * cell_size) + cell_size / 2,
            )
            color = (0, 240, 0) if i == len(sub_path) - 1 else (128, 0, 128)
            pygame.draw.circle(screen, color, (px, py), cell_size // 4)

    def step(self) -> None:
        if len(self.path) > self.curr_i + 1:
            self.curr = self.path[self.curr_i + 1]
            self.curr_i += 1
