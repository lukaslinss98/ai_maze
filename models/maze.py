from typing import List, Tuple

import pygame

from models.cell import Cell, Open, Wall
from models.direction import Direction
from util.colors import DARK_GREY, GREEN, RED, WHITE


class Maze:
    def __init__(self, maze: List[List[int]], start: Tuple, end: Tuple) -> None:
        self.grid: List[List[Cell]] = self._build_maze(maze, start, end)
        self.start: Open = self.get_cell(*start)
        self.end: Open = self.get_cell(*end)
        self.policy: dict[Open, Open] = {}

    def _build_maze(self, grid: List[List[int]], start, end) -> List[List[Cell]]:
        rows, cols = len(grid), len(grid[0])

        def is_wall(x: int, y: int) -> bool:
            return grid[x][y] == 1 and (x, y) != start and (x, y) != end

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

    def init_state_values(self, initial_value: float) -> None:
        for cell in self.open_cells():
            if isinstance(cell, Open):
                cell.value = initial_value if cell != self.end else 100.0

    def value_iteration(self) -> float:
        discount_factor = 0.9
        living_reward = -1
        max_dv = float('-inf')
        for cell in self.open_cells():
            if cell == self.end:
                continue

            dir_by_n = {n: d for d, n in self.neighbors(cell)}

            if not dir_by_n:
                print('No neighbors')
                continue

            max_neighbor = max(dir_by_n, key=lambda c: c.value or 0.0)
            max_q = max_neighbor.value or 0.0

            old_value = cell.value or 0.0
            new_value = living_reward + discount_factor * max_q

            max_dv = max(max_dv, abs(new_value - old_value))
            cell.value = new_value
            cell.best_direction = dir_by_n[max_neighbor]
            self.policy[cell] = max_neighbor

        return max_dv

    def draw_policy(self, screen, start, cell_size) -> None:
        path: List[Open] = []
        curr = start
        while curr:
            path.append(curr)
            curr = self.policy.get(curr, None)

        for c in path:
            c.draw_cell_arrow(screen, cell_size, GREEN)

    def draw(
        self, screen: pygame.Surface, cell_size: int = 32, draw_values=False
    ) -> None:
        for x, row in enumerate(self.grid):
            for y, cell in enumerate(row):
                px, py = y * cell_size, x * cell_size
                rect = pygame.Rect(px, py, cell_size, cell_size)

                if isinstance(cell, Wall):
                    pygame.draw.rect(screen, DARK_GREY, rect)
                elif isinstance(cell, Open):
                    if cell == self.start:
                        pygame.draw.rect(screen, GREEN, rect)
                    elif cell == self.end:
                        pygame.draw.rect(screen, RED, rect)
                    else:
                        pygame.draw.rect(screen, WHITE, rect)

                    if draw_values:
                        cell.draw_cell_value(screen, px, py, cell_size)

    def get_cell(self, x, y) -> Open:
        cell = self.grid[x][y]
        if isinstance(cell, Open):
            return cell

        raise Exception(f'Cell at ({x},{y}) is not of type Open')

    def get(self, curr, direction: str) -> Open:
        if direction == 'north':
            return self.get_cell(curr.x - 1, curr.y)
        elif direction == 'south':
            return self.get_cell(curr.x + 1, curr.y)
        elif direction == 'west':
            return self.get_cell(curr.x, curr.y - 1)
        elif direction == 'east':
            return self.get_cell(curr.x, curr.y + 1)
        else:
            raise Exception(f'unexpected value for direction {direction}')

    def neighbors(self, cell: Open) -> List[Tuple[Direction, Open]]:
        neigbors = []
        if cell.north:
            neigbors.append((Direction.NORTH, self.get_cell(cell.x - 1, cell.y)))
        if cell.west:
            neigbors.append((Direction.WEST, self.get_cell(cell.x, cell.y - 1)))
        if cell.south:
            neigbors.append((Direction.SOUTH, self.get_cell(cell.x + 1, cell.y)))
        if cell.east:
            neigbors.append((Direction.EAST, self.get_cell(cell.x, cell.y + 1)))

        return neigbors

    def open_cells(self) -> List[Open]:
        return [cell for row in self.grid for cell in row if isinstance(cell, Open)]

    def __str__(self) -> str:
        str = ''
        for r in self.grid:
            for c in r:
                str += f'{c.__str__()},'
            str += '\n'

        return str
