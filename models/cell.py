from dataclasses import dataclass

import pygame
from pygame import Surface

from models import direction
from models.direction import Direction
from util.colors import BLACK


@dataclass(eq=True)
class Cell:
    x: int
    y: int

    def coordinates(self):
        return (self.x, self.y)

    def manhatten_dist(self, other) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'


@dataclass(eq=True)
class Open(Cell):
    north: bool
    east: bool
    south: bool
    west: bool
    value: float = 100
    best_direction: Direction | None = Direction.NORTH

    def draw_cell_value(self, screen: Surface, cell_size: int):
        font = pygame.font.SysFont('arial', 11)
        cx = self.y * cell_size
        cy = self.x * cell_size

        if self.value is not None:
            text = font.render(f'{self.value:.2f}', True, BLACK)
        else:
            text = font.render('-', True, BLACK)

        # screen.blit(text, (cx + cell_size // 4, cy + cell_size // 4))
        self.draw_cell_arrow(screen, cell_size)

    def draw_cell_arrow(self, screen: Surface, cell_size: int, color=BLACK):
        if not self.best_direction:
            return

        cx = self.y * cell_size + cell_size // 2
        cy = self.x * cell_size + cell_size // 2
        half = cell_size // 3

        if self.best_direction == Direction.NORTH:
            points = [(cx, cy - half), (cx - half, cy + half), (cx + half, cy + half)]
        elif self.best_direction == Direction.SOUTH:
            points = [(cx, cy + half), (cx - half, cy - half), (cx + half, cy - half)]
        elif self.best_direction == Direction.EAST:
            points = [(cx + half, cy), (cx - half, cy - half), (cx - half, cy + half)]
        elif self.best_direction == Direction.WEST:
            points = [(cx - half, cy), (cx + half, cy - half), (cx + half, cy + half)]
        else:
            print(f'Could not work with direction {self.best_direction}')
            return

        pygame.draw.polygon(screen, color, points)

    def __str__(self) -> str:
        return f'({self.x}, {self.y}), V={self.value}'

    def __hash__(self):
        return hash((self.x, self.y, self.north, self.east, self.south, self.west))


@dataclass(eq=True)
class Wall(Cell):
    pass
