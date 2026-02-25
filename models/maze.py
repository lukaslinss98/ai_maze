import random
from typing import List, Tuple

import pygame
from pygame import Surface

from models.cell import Cell, Open, Wall
from models.direction import Action
from util.colors import DARK_GREY, GREEN, RED, WHITE


class Maze:
    def __init__(
        self, maze: List[List[int]], start: Tuple, end: Tuple, cell_size: int = 20
    ) -> None:
        self.grid: List[List[Cell]] = self._build_maze(maze, start, end, cell_size)
        self.start: Open = self.get_cell(*start)
        self.end: Open = self.get_cell(*end)

    def draw(
        self, screen: pygame.Surface, draw_values=False, draw_actions=False
    ) -> None:
        for cell in self.get_cells():
            cell_size = cell.size
            px, py = cell.y * cell_size, cell.x * cell_size
            rect = pygame.Rect(px, py, cell_size, cell.size)

            if isinstance(cell, Wall):
                pygame.draw.rect(screen, DARK_GREY, rect)
            elif isinstance(cell, Open):
                if cell == self.start:
                    pygame.draw.rect(screen, RED, rect)
                elif cell == self.end:
                    pygame.draw.rect(screen, GREEN, rect)
                else:
                    pygame.draw.rect(screen, WHITE, rect)

                if draw_values:
                    cell.draw_value(screen)
                if draw_actions:
                    cell.draw_action(screen)

    def get_cell(self, x: int, y: int) -> Open:
        cell = self.grid[x][y]
        if isinstance(cell, Open):
            return cell

        raise Exception(f'Cell at ({x},{y}) is not of type Open')

    def move_to(self, curr: Open, action: Action) -> Open:
        if action == Action.NORTH:
            return self.get_cell(curr.x - 1, curr.y)
        elif action == Action.SOUTH:
            return self.get_cell(curr.x + 1, curr.y)
        elif action == Action.WEST:
            return self.get_cell(curr.x, curr.y - 1)
        elif action == Action.EAST:
            return self.get_cell(curr.x, curr.y + 1)

    def neighbors(self, cell: Open) -> List[Tuple[Action, Open]]:
        neigbors = []
        if cell.north:
            neigbors.append((Action.NORTH, self.get_cell(cell.x - 1, cell.y)))
        if cell.west:
            neigbors.append((Action.WEST, self.get_cell(cell.x, cell.y - 1)))
        if cell.south:
            neigbors.append((Action.SOUTH, self.get_cell(cell.x + 1, cell.y)))
        if cell.east:
            neigbors.append((Action.EAST, self.get_cell(cell.x, cell.y + 1)))

        return neigbors

    def get_open_cells(self) -> List[Open]:
        return [c for c in self.get_cells() if isinstance(c, Open)]

    def get_cells(self) -> List[Cell]:
        return [cell for row in self.grid for cell in row]

    def dims(self) -> Tuple[int, int]:
        return (len(self.grid), len(self.grid[0]))

    def _build_maze(
        self, grid: List[List[int]], start, end, cell_size: int
    ) -> List[List[Cell]]:
        rows, cols = len(grid), len(grid[0])

        def is_wall(x: int, y: int) -> bool:
            return grid[x][y] == 1 and (x, y) != start and (x, y) != end

        maze: List[List[Cell]] = []
        for x in range(rows):
            row = []
            for y in range(cols):
                if is_wall(x, y):
                    row.append(Wall(x, y, cell_size))
                else:
                    north = (x != 0) and not is_wall(x - 1, y)
                    south = (x != rows - 1) and not is_wall(x + 1, y)
                    west = (y != 0) and not is_wall(x, y - 1)
                    east = (y != cols - 1) and not is_wall(x, y + 1)
                    row.append(Open(x, y, cell_size, north, east, south, west))

            maze.append(row)

        return maze

    def __str__(self) -> str:
        str = ''
        for r in self.grid:
            for c in r:
                str += f'{c.__str__()},'
            str += '\n'

        return str


class MdpMaze(Maze):
    def __init__(
        self, maze: List[List[int]], start: Tuple, end: Tuple, cell_size: int = 20
    ) -> None:
        super().__init__(maze, start, end, cell_size)

    def init_states(self, initial_value: float, goal_reward: float) -> None:
        for cell in super().get_open_cells():
            cell.value = initial_value if cell != self.end else goal_reward
            cell.policy = random.choice(cell.open_directions())

    def policy_evaluation_step(
        self, discount: float, living_reward: float, noise: float
    ) -> float:
        max_delta_v = float('-inf')
        for cell in super().get_open_cells():
            if cell == self.end:
                continue

            old_value = cell.value

            exp_value = self.value_by_action(cell, noise)[cell.policy]

            cell.value = living_reward + discount * exp_value
            dV = abs(cell.value - old_value)
            max_delta_v = max(max_delta_v, dV)

        return max_delta_v

    def policy_improvement_step(self) -> bool:
        is_stable = True

        for cell in super().get_open_cells():
            if cell == self.end:
                continue

            old_policy = cell.policy
            max_value = float('-inf')
            for action, neighbor in self.neighbors(cell):
                if neighbor.value > max_value:
                    max_value = neighbor.value
                    cell.policy = action

            if old_policy != cell.policy:
                is_stable = False

        return is_stable

    def draw_policy(self, screen: Surface, start: Open, end: Open) -> None:
        for c in self.shortest_path(start, end):
            c.draw_action(screen, GREEN)

    def shortest_path(self, start, end) -> List[Open]:
        path: List[Open] = []
        seen = set()
        curr = start
        while curr and curr not in seen:
            if curr == end:
                break

            path.append(curr)
            seen.add(curr)
            curr = self.move_to(curr, curr.policy)

        return path

    def value_by_action(self, cell, noise) -> dict[Action, float]:
        value_by_action = {}
        neighbors = self.neighbors(cell)
        for dir, neigh in neighbors:
            if neigh.value is None:
                continue

            expected_value = 0
            for dir2, neigh2 in neighbors:
                no_neighbors = len(neighbors)
                if no_neighbors == 1:
                    expected_value += neigh2.value
                else:
                    probability = (
                        1 - noise if dir == dir2 else noise / (no_neighbors - 1)
                    )

                    expected_value += probability * neigh2.value

            value_by_action[dir] = expected_value
        return value_by_action
