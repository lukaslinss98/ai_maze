from dataclasses import dataclass


@dataclass
class Cell:
    x: int
    y: int

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def coordinates(self):
        return (self.x, self.y)


@dataclass
class Open(Cell):
    north: bool
    east: bool
    south: bool
    west: bool

    def __str__(self) -> str:
        return f'({self.x}, {self.y}, n: {self.north}, e: {self.east}, s: {self.south}, w: {self.west})'


@dataclass
class Wall(Cell):
    pass
