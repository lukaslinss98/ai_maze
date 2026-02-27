import csv
import os
import uuid
from dataclasses import dataclass

from algorithms.mdp_algorithms import PolicyIteration, ValueIteration
from algorithms.pathfinding_algorithms import (
    BFS,
    DFS,
    AStar,
    chebyshev_distance,
    euclidean_distance,
    manhatten_distance,
)
from models.maze import Maze, MdpMaze
from util.maze_generation import generate_maze

RESULTS_DIR = os.path.join(os.path.dirname(__file__), 'results')


@dataclass(frozen=True)
class EvalRow:
    size: int
    seed: int
    type: str
    algorithm: str
    path_length: int
    visited: int | None
    total_iterations: int | None
    inner_iterations: int | None
    outer_iterations: int | None
    max_frontier_size: int | None
    runtime_s: float
    memory_bytes: int


def run_eval(**kwargs):
    sizes = [int(s) for s in kwargs['size'].split(',')]
    generator = kwargs['generator']
    seed_arg = kwargs['seed']
    noise = kwargs['noise']
    discount = kwargs['discount']
    reward = kwargs['reward']
    write_csv = kwargs['csv']
    run_pathfinding = kwargs['pathfinding']
    run_mdp = kwargs['mdp']

    if not run_pathfinding and not run_mdp:
        run_pathfinding = True
        run_mdp = True

    seeds = [int(s) for s in seed_arg.split(',')] if seed_arg else [None]
    run_id = uuid.uuid4().hex[:8]

    print(f'Run ID: {run_id}')

    all_rows = []
    for size in sizes:
        for seed in seeds:
            print(f'\n--- Size: {size}, Seed: {seed} ---')

            raw_maze, start, end = generate_maze(size, size, generator, seed)

            print(f'Maze: {size}x{size} | Generator: {generator} | Seed: {seed}')

            rows = []
            if run_pathfinding:
                rows.extend(_run_pathfinding_eval(raw_maze, start, end, size, seed))
            if run_mdp:
                rows.extend(
                    _run_mdp_eval(
                        raw_maze, start, end, discount, reward, noise, size, seed
                    )
                )

            _print_results(rows)
            all_rows.extend(rows)

    if write_csv:
        _write_csv(all_rows, generator, run_id)


def _run_pathfinding_eval(
    raw_maze, start, end, size: int, seed: int | None
) -> list[EvalRow]:
    maze = Maze(raw_maze, start, end, cell_size=1)

    solvers = [
        ('DFS', DFS()),
        ('BFS', BFS()),
        ('A* (Manhattan)', AStar(heuristic=manhatten_distance)),
        ('A* (Euclidean)', AStar(heuristic=euclidean_distance)),
        ('A* (Chebyshev)', AStar(heuristic=chebyshev_distance)),
    ]

    rows = []
    for name, solver in solvers:
        result = solver.solve(maze, maze.start)
        rows.append(
            EvalRow(
                size=size,
                seed=seed,
                type='pathfinding',
                algorithm=name,
                path_length=len(result.shortest_path),
                visited=len(result.visited),
                total_iterations=None,
                inner_iterations=None,
                outer_iterations=None,
                max_frontier_size=result.max_frontier_size,
                runtime_s=result.run_time,
                memory_bytes=result.peak_memory_bytes,
            )
        )

    return rows


def _run_mdp_eval(
    raw_maze, start, end, discount, reward, noise, size: int, seed: int | None
) -> list[EvalRow]:
    maze = MdpMaze(raw_maze, start, end, cell_size=1)
    maze.init_states(initial_value=0, goal_reward=10)

    vi = ValueIteration(discount, reward, noise)
    vi_result = vi.solve(maze, take_snapshots=False)

    maze_pi = MdpMaze(raw_maze, start, end, cell_size=1)
    maze_pi.init_states(initial_value=0, goal_reward=10)

    pi = PolicyIteration(discount, reward, noise, theta=0.0001)
    pi_result = pi.solve(maze_pi, take_snapshots=False)

    return [
        EvalRow(
            size=size,
            seed=seed,
            type='mdp',
            algorithm='Value Iteration',
            path_length=len(vi_result.shortest_path),
            visited=None,
            total_iterations=vi_result.iterations,
            inner_iterations=None,
            outer_iterations=None,
            max_frontier_size=None,
            runtime_s=vi_result.run_time,
            memory_bytes=vi_result.peak_memory,
        ),
        EvalRow(
            size=size,
            seed=seed,
            type='mdp',
            algorithm='Policy Iteration',
            path_length=len(pi_result.shortest_path),
            visited=None,
            total_iterations=pi_result.total_eval_iterations
            + pi_result.total_improve_iterations,
            inner_iterations=pi_result.total_eval_iterations,
            outer_iterations=pi_result.total_improve_iterations,
            max_frontier_size=None,
            runtime_s=pi_result.run_time,
            memory_bytes=pi_result.peak_memory,
        ),
    ]


def _print_results(rows: list[EvalRow]) -> None:
    pf_rows = [r for r in rows if r.type == 'pathfinding']
    mdp_rows = [r for r in rows if r.type == 'mdp']

    if pf_rows:
        print('\n=== Pathfinding ===\n')
        print(
            f'{"Algorithm":<22} {"Path Length":>11} {"Visited":>8}'
            f' {"Max Frontier":>13} {"Runtime":>10} {"Memory":>10}'
        )
        for r in pf_rows:
            print(
                f'{r.algorithm:<22} {r.path_length:>11}'
                f' {r.visited:>8}'
                f' {r.max_frontier_size:>13}'
                f' {r.runtime_s:>9.4f}s'
                f' {r.memory_bytes:>8} B'
            )

    if mdp_rows:
        print('\n=== MDP ===\n')
        print(
            f'{"Algorithm":<22} {"Path Length":>11} {"Total":>6}'
            f' {"Inner":>6} {"Outer":>6}'
            f' {"Runtime":>10} {"Memory":>10}'
        )
        for r in mdp_rows:
            inner = str(r.inner_iterations) if r.inner_iterations is not None else ''
            outer = str(r.outer_iterations) if r.outer_iterations is not None else ''
            print(
                f'{r.algorithm:<22} {r.path_length:>11}'
                f' {r.total_iterations:>6}'
                f' {inner:>6}'
                f' {outer:>6}'
                f' {r.runtime_s:>9.4f}s'
                f' {r.memory_bytes:>8} B'
            )


def _write_csv(rows: list[EvalRow], generator: str, run_id: str) -> None:
    os.makedirs(RESULTS_DIR, exist_ok=True)

    filename = f'{run_id}_eval_{generator}.csv'
    filepath = os.path.join(RESULTS_DIR, filename)

    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                'size',
                'seed',
                'type',
                'algorithm',
                'path_length',
                'visited',
                'total_iterations',
                'inner_iterations',
                'outer_iterations',
                'max_frontier_size',
                'runtime_s',
                'memory_bytes',
            ]
        )
        for r in rows:
            writer.writerow(
                [
                    r.size,
                    r.seed if r.seed is not None else '',
                    r.type,
                    r.algorithm,
                    r.path_length,
                    r.visited if r.visited is not None else '',
                    r.total_iterations if r.total_iterations is not None else '',
                    r.inner_iterations if r.inner_iterations is not None else '',
                    r.outer_iterations if r.outer_iterations is not None else '',
                    r.max_frontier_size if r.max_frontier_size is not None else '',
                    f'{r.runtime_s:.6f}',
                    r.memory_bytes,
                ]
            )

    print(f'\nResults written to {filepath}')
