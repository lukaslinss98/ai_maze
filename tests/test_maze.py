import unittest

from models.cell import Open
from models.maze import Maze


# TODO Fix tests
class TestMaze(unittest.TestCase):
    def test_construct_basic_maze(self) -> None:
        false_list = [False] * 4
        raw_maze = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]

        expected_maze = [
            [None, None, None],
            [None, Open(1, 1, *false_list), None],
            [None, None, None],
        ]

        actual = Maze(raw_maze)

        self.assertEqual(actual.grid, expected_maze)

    def test_construct_maze_5x5(self) -> None:
        raw = [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1],
        ]

        expected = [
            [None, None, None, None, None],
            [
                None,
                Open(1, 1, False, True, True, False),
                Open(1, 2, False, True, False, True),
                Open(1, 3, False, False, True, True),
                None,
            ],
            [
                None,
                Open(2, 1, True, False, True, False),
                None,
                Open(2, 3, True, False, True, False),
                None,
            ],
            [
                None,
                Open(3, 1, True, True, False, False),
                Open(3, 2, False, True, False, True),
                Open(3, 3, True, False, False, True),
                None,
            ],
            [None, None, None, None, None],
        ]

        actual = Maze(raw)
        self.assertEqual(actual.grid, expected)

    def test_no_free_side_into_wall_or_oob(self) -> None:
        raw = [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1],
        ]
        m = Maze(raw)

        rows, cols = len(raw), len(raw[0])

        dirs = [
            (-1, 0, 'north'),
            (0, 1, 'east'),
            (1, 0, 'south'),
            (0, -1, 'west'),
        ]

        for x in range(rows):
            for y in range(cols):
                cell = m.grid[x][y]
                if raw[x][y] == 1:
                    self.assertIsNone(cell)
                    continue

                self.assertIsNotNone(cell)
                for dx, dy, attr in dirs:
                    free = getattr(cell, attr)
                    if not free:
                        continue

                    nx, ny = x + dx, y + dy
                    with self.subTest(x=x, y=y, direction=attr, nx=nx, ny=ny):
                        self.assertTrue(0 <= nx < rows and 0 <= ny < cols)
                        self.assertEqual(raw[nx][ny], 0)

    def test_free_sides_are_symmetric(self) -> None:
        raw = [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1],
        ]
        m = Maze(raw)

        rows, cols = len(raw), len(raw[0])

        dirs = [
            ('north', -1, 0, 'south'),
            ('east', 0, 1, 'west'),
            ('south', 1, 0, 'north'),
            ('west', 0, -1, 'east'),
        ]

        for x in range(rows):
            for y in range(cols):
                cell = m.grid[x][y]
                if cell is None:
                    continue

                for attr, dx, dy, opp in dirs:
                    if not getattr(cell, attr):
                        continue

                    nx, ny = x + dx, y + dy
                    with self.subTest(x=x, y=y, direction=attr, nx=nx, ny=ny):
                        self.assertTrue(0 <= nx < rows and 0 <= ny < cols)
                        neighbor = m.grid[nx][ny]
                        self.assertIsNotNone(neighbor)
                        self.assertTrue(getattr(neighbor, opp))

    def test_all_walls_yields_all_none(self) -> None:
        raw = [
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
        ]
        m = Maze(raw)

        self.assertEqual(len(m.grid), len(raw))
        self.assertEqual(len(m.grid[0]), len(raw[0]))

        for x, row in enumerate(m.grid):
            for y, cell in enumerate(row):
                with self.subTest(x=x, y=y):
                    self.assertIsNone(cell)


if __name__ == '__main__':
    unittest.main()
