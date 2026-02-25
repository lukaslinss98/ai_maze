import os

from algorithms.mdp import PolicyIteration, ValueIteration

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

from models.maze import MdpMaze
from util.colors import DARK_GREY, WHITE
from util.maze_generation import generate_maze


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
        run_value_iteration(maze, discount, reward, noise, speed)

    if solver == 'policy-iteration':
        run_policy_iteration(maze, discount, noise, reward, speed)


def run_value_iteration(maze: MdpMaze, discount, reward, noise, speed):

    pygame.init()
    font = pygame.font.SysFont('arial', 16)
    clock = pygame.time.Clock()
    running = True

    cell_size = maze.start.size

    cols, rows = maze.dims()

    screen = pygame.display.set_mode(
        (rows * cell_size, cols * cell_size), pygame.RESIZABLE
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
        if iteration < len(result.snapshots) - 1:
            iteration += 1
        else:
            snapshot.maze.draw_policy(screen, maze.start, maze.end)

        eval_text = font.render(
            f'ΔV={snapshot.delta_v:.4f} Iterations={iteration}',
            True,
            WHITE,
        )
        screen.blit(eval_text, (10, 10))
        pygame.display.flip()
        clock.tick(speed)

    pygame.quit()


def run_policy_iteration(maze: MdpMaze, discount, noise, reward, speed):
    pygame.init()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('arial', 16)
    running = True

    cols, rows = maze.dims()
    cell_size = maze.start.size

    screen = pygame.display.set_mode(
        (rows * cell_size, cols * cell_size), pygame.RESIZABLE
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

        snapshot.maze.draw(screen, draw_values=False, draw_actions=True)
        if iteration < len(result.snapshots) - 1:
            iteration += 1
        else:
            snapshot.maze.draw_policy(screen, maze.start, maze.end)

        eval_text = font.render(
            f'Mode={snapshot.mode}, ΔV={snapshot.delta_v:.4f} '
            f'Total Iters={snapshot.eval_iters + snapshot.improve_iters}, '
            f'Eval={snapshot.eval_iters}, Improve={snapshot.improve_iters}',
            True,
            WHITE,
        )
        screen.blit(eval_text, (10, 10))

        pygame.display.flip()
        clock.tick(speed)

    pygame.quit()
