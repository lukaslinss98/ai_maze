import argparse
import os

from util.colors import DARK_GREY, WHITE

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame

from models.agent import Agent
from models.maze import Maze
from util.maze_generation import generate_maze


def run_mdp(height, width, generator, seed, speed, **_):

    print(
        f"""height: {height}\nwidth: {width}\ngenerator: {generator}\nseed: {seed}\nspeed: {speed}"""
    )

    pygame.init()
    clock = pygame.time.Clock()
    running = True

    raw_maze, start, end = generate_maze(height, width, generator, seed)

    rows, cols = len(raw_maze), len(raw_maze[0])
    cell_size = 32
    screen = pygame.display.set_mode(
        (cols * cell_size, rows * cell_size), pygame.RESIZABLE
    )
    clock = pygame.time.Clock()

    maze = Maze(raw_maze, start, end)

    maze.init_state_values(initial_value=0, goal_reward=10)
    print(maze.start)
    print(maze.neighbors(maze.start))

    delta_V = float('inf')
    iteration = 0
    font = pygame.font.SysFont('arial', 16)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

        screen.fill(DARK_GREY)

        maze.draw(screen, cell_size, draw_values=True)
        theta = 0.0001
        if delta_V > theta:
            delta_V = maze.value_iteration_step(
                discount_factor=0.9, living_reward=-0.01, noise=0.2
            )
            iteration += 1
        else:
            maze.draw_policy(screen, start=maze.start, cell_size=cell_size)

        status = font.render(f'ΔV={delta_V:.4f} Iterations={iteration}', True, WHITE)
        screen.blit(status, (10, 10))
        pygame.display.flip()
        clock.tick(speed)

    pygame.quit()


def run_pathfinding(height, width, solver, generator, seed, speed, **_):

    print(
        f"""height: {height}\nwidth: {width}\ngenerator: {generator}\nsolver:{solver}\nseed: {seed}\nspeed: {speed}"""
    )

    pygame.init()
    clock = pygame.time.Clock()
    running = True

    raw_maze, start, end = generate_maze(height, width, generator, seed)

    rows, cols = len(raw_maze), len(raw_maze[0])
    cell_size = 16
    screen = pygame.display.set_mode(
        (cols * cell_size, rows * cell_size), pygame.RESIZABLE
    )
    clock = pygame.time.Clock()

    maze = Maze(raw_maze, start, end)
    agent = Agent(maze, solver)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

        screen.fill(DARK_GREY)

        maze.draw(screen, cell_size)
        agent.draw(screen, cell_size)
        is_last_step = agent.step()
        if is_last_step:
            agent.draw_shortest_path(screen, cell_size)

        pygame.display.flip()
        clock.tick(speed)

    print(
        f"""Shortest Path Length: {len(agent.pathfinding_result.shortest_path)}\nCells Visited: {len(agent.pathfinding_result.visited)}"""
    )
    pygame.quit()


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
        default='Prims',
    )

    mdp = subparser.add_parser('mdp', help='Run MDP algorithms')
    mdp.add_argument('--height', type=int, default=10)
    mdp.add_argument('--width', type=int, default=10)
    mdp.add_argument('--seed', type=int)
    mdp.add_argument('--speed', type=int, default=30)
    mdp.add_argument(
        '--generator',
        type=str,
        choices=['prims', 'backtracking', 'aldousbroder', 'binarytree', 'cellular'],
        default='Prims',
    )

    return parser.parse_args()


if __name__ == '__main__':
    cli_args = read_args()

    if cli_args.mode == 'pathfinding':
        run_pathfinding(**vars(cli_args))
    elif cli_args.mode == 'mdp':
        run_mdp(**vars(cli_args))
