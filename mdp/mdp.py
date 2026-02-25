import os

from algorithms.mdp_algorithms import PolicyIteration, ValueIteration

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

from models.maze import MdpMaze
from util.colors import DARK_GREY
from util.maze_generation import generate_maze
from util.panel import PANEL_WIDTH, draw_info_panel


def run_mdp(**kwargs):
    for k, v in kwargs.items():
        print(f'{k}: {v}')

    height = kwargs['height']
    width = kwargs['width']
    generator = kwargs['generator']
    seed = kwargs['seed']
    solver = kwargs['solver']
    speed = kwargs['speed']
    reward = kwargs['reward']
    discount = kwargs['discount']
    noise = kwargs['noise']
    cell_size = kwargs['cell_size']

    raw_maze, start, end = generate_maze(height, width, generator, seed)
    maze = MdpMaze(raw_maze, start, end, cell_size)
    maze.init_states(initial_value=0, goal_reward=10)

    if solver == 'value-iteration':
        run_value_iteration(
            maze, discount, reward, noise, speed, height, width, generator
        )

    if solver == 'policy-iteration':
        run_policy_iteration(
            maze, discount, noise, reward, speed, height, width, generator
        )


def run_value_iteration(
    maze: MdpMaze, discount, reward, noise, speed, height, width, generator
):
    pygame.init()
    title_font = pygame.font.SysFont('arial', 18, bold=True)
    body_font = pygame.font.SysFont('arial', 14)
    clock = pygame.time.Clock()
    running = True

    cell_size = maze.start.size

    cols, rows = maze.dims()
    maze_pixel_width = rows * cell_size
    maze_pixel_height = cols * cell_size

    screen = pygame.display.set_mode(
        (maze_pixel_width + PANEL_WIDTH, maze_pixel_height), pygame.RESIZABLE
    )

    value_iteration = ValueIteration(discount, reward, noise)
    result = value_iteration.solve(maze)
    iteration = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

        screen.fill(DARK_GREY)

        snapshot = result.snapshots[iteration]
        snapshot.maze.draw(screen, draw_values=False, draw_actions=True)
        is_last = iteration >= len(result.snapshots) - 1
        if is_last:
            snapshot.maze.draw_policy(screen, maze.start, maze.end)
        else:
            iteration += 1

        entries = [
            ('Generator', generator),
            ('Size', f'{width}x{height}'),
            ('Discount', str(discount)),
            ('Noise', str(noise)),
            ('Reward', str(reward)),
            ('---', ''),
            ('Iteration', str(iteration)),
            ('Delta V', f'{snapshot.delta_v:.4f}'),
        ]

        if is_last:
            entries.extend(
                [
                    ('---', ''),
                    ('Path Length', str(len(result.shortest_path))),
                    ('Runtime', f'{result.run_time:.4f}s'),
                    ('Memory', f'{result.peak_memory} B'),
                ]
            )

        draw_info_panel(
            screen,
            maze_pixel_width,
            screen.get_height(),
            'Value Iteration',
            entries,
            title_font,
            body_font,
        )

        pygame.display.flip()
        clock.tick(speed)

    print('\n------------Evaluation-------------\n')

    print(
        f"""Shortest Path Length: {len(result.shortest_path)}
Run Time: {result.run_time:.6f}s,
Peak Memory: {result.peak_memory} bytes
"""
    )
    pygame.quit()


def run_policy_iteration(
    maze: MdpMaze, discount, noise, reward, speed, height, width, generator
):
    pygame.init()
    clock = pygame.time.Clock()
    title_font = pygame.font.SysFont('arial', 20, bold=True)
    body_font = pygame.font.SysFont('arial', 16)
    running = True

    cols, rows = maze.dims()
    cell_size = maze.start.size
    maze_pixel_width = rows * cell_size
    maze_pixel_height = cols * cell_size

    screen = pygame.display.set_mode(
        (maze_pixel_width + PANEL_WIDTH, maze_pixel_height), pygame.RESIZABLE
    )

    policy_iteration = PolicyIteration(discount, reward, noise, theta=0.0001)
    result = policy_iteration.solve(maze)
    iteration = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

        screen.fill(DARK_GREY)

        snapshot = result.snapshots[iteration]
        draw_values = snapshot.mode == 'eval'
        draw_actions = snapshot.mode == 'improve'

        snapshot.maze.draw(screen, draw_values, draw_actions)
        is_last = iteration >= len(result.snapshots) - 1
        if is_last:
            snapshot.maze.draw_policy(screen, maze.start, maze.end)
        else:
            iteration += 1

        entries = [
            ('Generator', generator),
            ('Size', f'{width}x{height}'),
            ('Discount', str(discount)),
            ('Noise', str(noise)),
            ('Reward', str(reward)),
            ('---', ''),
            ('Mode', snapshot.mode),
            ('Eval Iters', str(snapshot.eval_iters)),
            ('Improve Iters', str(snapshot.improve_iters)),
            ('Total Iters', str(snapshot.eval_iters + snapshot.improve_iters)),
            ('Delta V', f'{snapshot.delta_v:.4f}'),
        ]

        if is_last:
            entries.extend(
                [
                    ('---', ''),
                    ('Path Length', str(len(result.shortest_path))),
                    ('Runtime', f'{result.run_time:.4f}s'),
                    ('Memory', f'{result.peak_memory} B'),
                ]
            )

        draw_info_panel(
            screen,
            maze_pixel_width,
            screen.get_height(),
            'Policy Iteration',
            entries,
            title_font,
            body_font,
        )

        pygame.display.flip()
        clock.tick(speed)

    print('\n------------Evaluation-------------\n')
    print(
        f"""Shortest Path Length: {len(result.shortest_path)}
Run Time: {result.run_time:.6f}s,
Peak Memory: {result.peak_memory} bytes
"""
    )
    pygame.quit()
