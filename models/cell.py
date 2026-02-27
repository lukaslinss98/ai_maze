from dataclasses import dataclass
from typing import List

import pygame
from pygame import Surface

from models.direction import Action
from util.colors import BLACK


@dataclass(eq=True)
class Cell:
    x: int
    y: int
    size: int

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
    value = 100.0
    policy = Action.NORTH

    def draw_action(self, screen: Surface, color=BLACK):
        if not self.policy:
            return

        cx = self.y * self.size + self.size // 2
        cy = self.x * self.size + self.size // 2
        half = self.size // 3

        if self.policy == Action.NORTH:
            points = [(cx, cy - half), (cx - half, cy + half), (cx + half, cy + half)]
        elif self.policy == Action.SOUTH:
            points = [(cx, cy + half), (cx - half, cy - half), (cx + half, cy - half)]
        elif self.policy == Action.EAST:
            points = [(cx + half, cy), (cx - half, cy - half), (cx - half, cy + half)]
        elif self.policy == Action.WEST:
            points = [(cx - half, cy), (cx + half, cy - half), (cx + half, cy + half)]
        else:
            print(f'Could not work with direction {self.policy}')
            return

        pygame.draw.polygon(screen, color, points)

    def open_directions(self) -> List[Action]:
        dirs: List[Action] = []
        if self.north:
            dirs.append(Action.NORTH)
        if self.south:
            dirs.append(Action.SOUTH)
        if self.west:
            dirs.append(Action.WEST)
        if self.east:
            dirs.append(Action.EAST)

        return dirs

    def __str__(self) -> str:
        return f'({self.x}, {self.y}), V={self.value}'

    def __hash__(self):
        return hash((self.x, self.y, self.north, self.east, self.south, self.west))


@dataclass(eq=True)
class Wall(Cell):
    pass
