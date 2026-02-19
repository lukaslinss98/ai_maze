import argparse
import os

from algorithms.pathfinding import run_pathfinding
from mdp.mdp import run_mdp

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


def read_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='mode', required=True)

    pathfinding = subparser.add_parser('pathfinding', help='Run search algorithms')
    pathfinding.add_argument('--height', type=int, default=10)
    pathfinding.add_argument('--width', type=int, default=10)
    pathfinding.add_argument('--seed', type=int)
    pathfinding.add_argument('--speed', type=int, default=30)
    pathfinding.add_argument(
        '--solver',
        type=str,
        choices=['bfs', 'dfs', 'astar_manhatten', 'astar_euclid', 'astar_chebyshev'],
        default='dfs',
    )
    pathfinding.add_argument(
        '--generator',
        type=str,
        choices=['prims', 'backtracking', 'aldousbroder', 'binarytree', 'cellular'],
        default='cellular',
    )

    mdp = subparser.add_parser('mdp', help='Run MDP algorithms')
    mdp.add_argument('--height', type=int, default=10)
    mdp.add_argument('--width', type=int, default=10)
    mdp.add_argument('--seed', type=int)
    mdp.add_argument('--speed', type=int, default=30)
    mdp.add_argument('--noise', type=float, default=0.2)
    mdp.add_argument('--discount', type=float, default=0.9)
    mdp.add_argument('--reward', type=float, default=-0.01)
    mdp.add_argument(
        '--solver',
        type=str,
        default='value-iteration',
        choices=['policy-iteration', 'value-iteration'],
    )
    mdp.add_argument(
        '--generator',
        type=str,
        choices=['prims', 'backtracking', 'aldousbroder', 'binarytree', 'cellular'],
        default='cellular',
    )

    return parser.parse_args()


if __name__ == '__main__':
    cli_args = read_args()

    if cli_args.mode == 'pathfinding':
        run_pathfinding(**vars(cli_args))
    elif cli_args.mode == 'mdp':
        run_mdp(**vars(cli_args))
