import argparse
import os

from evaluation.evaluation import run_eval
from mdp.mdp import run_mdp
from pathfinding.pathfinding import run_pathfinding

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


def read_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='mode', required=True)

    pathfinding = subparser.add_parser('pathfinding', help='Run search algorithms')
    pathfinding.add_argument('--height', type=int, default=10)
    pathfinding.add_argument('--width', type=int, default=10)
    pathfinding.add_argument('--seed', type=int)
    pathfinding.add_argument('--speed', type=int, default=40)
    pathfinding.add_argument('--cell-size', type=int, default=20)
    pathfinding.add_argument(
        '--solver',
        type=str,
        choices=['bfs', 'dfs', 'astar_manhattan', 'astar_euclid', 'astar_chebyshev'],
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
    mdp.add_argument('--speed', type=int, default=40)
    mdp.add_argument('--cell-size', type=int, default=20)
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

    eval_parser = subparser.add_parser(
        'eval', help='Run headless evaluation of all algorithms'
    )
    eval_parser.add_argument(
        '--size',
        type=str,
        default='10',
        help='Comma-separated list of sizes, e.g. 10,20,50',
    )
    eval_parser.add_argument('--seed', type=str)
    eval_parser.add_argument(
        '--generator',
        type=str,
        choices=['prims', 'backtracking', 'aldousbroder', 'binarytree', 'cellular'],
        default='cellular',
    )
    eval_parser.add_argument('--noise', type=float, default=0.0)
    eval_parser.add_argument('--discount', type=float, default=0.9)
    eval_parser.add_argument('--reward', type=float, default=-0.01)
    eval_parser.add_argument(
        '--csv', action='store_true', help='Write results to CSV file'
    )
    eval_parser.add_argument(
        '--pathfinding', action='store_true', help='Run pathfinding algorithms'
    )
    eval_parser.add_argument('--mdp', action='store_true', help='Run MDP algorithms')

    return parser.parse_args()


if __name__ == '__main__':
    cli_args = read_args()

    if cli_args.mode == 'pathfinding':
        run_pathfinding(**vars(cli_args))
    elif cli_args.mode == 'mdp':
        run_mdp(**vars(cli_args))
    elif cli_args.mode == 'eval':
        run_eval(**vars(cli_args))
