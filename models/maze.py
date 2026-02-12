from typing import List, cast

import pygame

from models import Cell, Open, Wall


class Maze:
    def __init__(self, maze: List[List[int]], start=None, end=None) -> None:
        self.start = start
        self.end = end
        self.grid: List[List[Cell]] = self._build_maze(maze)
        self.WALL_COLOR = (20, 20, 20)
        self.OPEN_COLOR = (240, 240, 240)
        self.START_COLOR = (0, 240, 0)
        self.END_COLOR = (240, 0, 0)

    def _build_maze(self, grid: List[List[int]]) -> List[List[Cell]]:
        rows, cols = len(grid), len(grid[0])

        def is_wall(x: int, y: int) -> bool:
            return grid[x][y] == 1 and (x, y) != self.start and (x, y) != self.end

        maze: List[List[Cell]] = []
        for x in range(rows):
            row = []
            for y in range(cols):
                if is_wall(x, y):
                    row.append(Wall(x, y))
                else:
                    north = (x != 0) and not is_wall(x - 1, y)
                    south = (x != rows - 1) and not is_wall(x + 1, y)
                    west = (y != 0) and not is_wall(x, y - 1)
                    east = (y != cols - 1) and not is_wall(x, y + 1)
                    row.append(Open(x, y, north, east, south, west))

            maze.append(row)

        return maze

    def draw(self, screen: pygame.Surface, cell_size: int = 32) -> None:
        for x, row in enumerate(self.grid):
            for y, cell in enumerate(row):
                px, py = y * cell_size, x * cell_size
                rect = pygame.Rect(px, py, cell_size, cell_size)

                if isinstance(cell, Wall):
                    pygame.draw.rect(screen, self.WALL_COLOR, rect)
                else:
                    if cell.coordinates() == self.start:
                        pygame.draw.rect(screen, self.START_COLOR, rect)
                    elif cell.coordinates() == self.end:
                        pygame.draw.rect(screen, self.END_COLOR, rect)
                    else:
                        pygame.draw.rect(screen, self.OPEN_COLOR, rect)

    def __str__(self) -> str:
        str = ''
        for r in self.grid:
            for c in r:
                str += f'{c.__str__()},'
            str += '\n'

        return str
