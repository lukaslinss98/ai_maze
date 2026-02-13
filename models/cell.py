from dataclasses import dataclass


@dataclass(frozen=True)
class Cell:
    x: int
    y: int

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def coordinates(self):
        return (self.x, self.y)


@dataclass(frozen=True)
class Open(Cell):
    north: bool
    east: bool
    south: bool
    west: bool


@dataclass(frozen=True)
class Wall(Cell):
    pass
