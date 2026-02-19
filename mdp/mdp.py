import os

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

    raw_maze, start, end = generate_maze(height, width, generator, seed)
    maze = MdpMaze(raw_maze, start, end, cell_size=32)
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
        (cols * cell_size, rows * cell_size), pygame.RESIZABLE
    )

    delta_V = float('inf')
    iterations = 0
    theta = 0.0001

    converged = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

        screen.fill(DARK_GREY)

        maze.draw(screen, draw_values=True)

        if not converged:
            delta_V = maze.value_iteration_step(discount, reward, noise)
            converged = delta_V < theta
            iterations += 1

        else:
            maze.draw_policy(screen, maze.start, maze.end)

        eval_text = font.render(
            f'ΔV={delta_V:.4f} Iterations={iterations}',
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
        (cols * cell_size, rows * cell_size), pygame.RESIZABLE
    )

    delta = float('inf')
    is_stable = False
    eval_iters = 0
    improve_iters = 0
    theta = 0.0001

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

        screen.fill(DARK_GREY)

        mode = 'eval' if delta > theta else 'improve'

        draw_values = mode == 'eval'
        draw_actions = mode == 'improve'

        print(draw_values)

        maze.draw(screen, draw_values, draw_actions)
        if not is_stable:
            if mode == 'eval':
                eval_iters += 1
                delta = maze.policy_evaluation_step(discount, reward, noise)
            elif mode == 'improve':
                improve_iters += 1
                is_stable = maze.policy_improvement_step()
                delta = float('inf')

            eval_text = font.render(
                f'Mode={mode}, ΔV={delta:.4f} Total Iters={eval_iters + improve_iters}, {eval_iters=}, {improve_iters=}',
                True,
                WHITE,
            )
            screen.blit(eval_text, (10, 10))
        else:
            maze.draw_policy(screen, maze.start, maze.end)

        pygame.display.flip()
        clock.tick(speed)

    pygame.quit()
