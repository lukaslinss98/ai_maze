from mazelib import Maze
from mazelib.generate.AldousBroder import AldousBroder
from mazelib.generate.BacktrackingGenerator import BacktrackingGenerator
from mazelib.generate.BinaryTree import BinaryTree
from mazelib.generate.CellularAutomaton import CellularAutomaton
from mazelib.generate.Prims import MazeGenAlgo, Prims


def generate_maze(height: int, width: int, generator: str, seed: None | int):
    m: Maze = Maze()

    if seed:
        m.set_seed(seed)

    m.generator = create_generator(generator, height, width)  # type: ignore[assignment]
    m.generate()
    m.generate_entrances(start_outer=True, end_outer=True)
    return m.grid.tolist(), m.start, m.end  # type: ignore[assignment]


def create_generator(generator, h, w) -> MazeGenAlgo:
    if generator == 'prims':
        return Prims(h, w)
    elif generator == 'backtracking':
        return BacktrackingGenerator(h, w)
    elif generator == 'aldousbroder':
        return AldousBroder(h, w)
    elif generator == 'binarytree':
        return BinaryTree(h, w)
    elif generator == 'cellular':
        return CellularAutomaton(h, w)
    else:
        return BacktrackingGenerator(h, w)
