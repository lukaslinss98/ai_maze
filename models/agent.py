from typing import List, Protocol

import pygame

from models.cell import Cell
from models.maze import Maze


class Solver(Protocol):
    def solve(self, maze: Maze) -> List[Cell]: ...


class Agent:
    def __init__(self, maze: Maze, solver: Solver) -> None:
        self.maze: Maze = maze
        self.path: List[Cell] = solver.solve(maze)
        self.curr: Cell = maze.start
        self.curr_i: int = 0

    def draw(self, screen: pygame.Surface, cell_size: int = 32) -> None:
        px, py = (
            (self.curr.y * cell_size) + cell_size / 2,
            (self.curr.x * cell_size) + cell_size / 2,
        )
        pygame.draw.circle(screen, (128, 0, 128), (px, py), cell_size // 4)

    def step(self) -> None:
        if len(self.path) - 1 != self.curr_i:
            self.curr = self.path[self.curr_i + 1]
            self.curr_i += 1
