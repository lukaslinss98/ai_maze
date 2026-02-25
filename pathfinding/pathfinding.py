import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

from models.agent import Agent
from models.maze import Maze
from util.colors import DARK_GREY, WHITE
from util.maze_generation import generate_maze


def run_pathfinding(**kwargs):
    for k, v in kwargs.items():
        print(f'{k}: {v}')

    height = kwargs['height']
    width = kwargs['width']
    generator = kwargs['generator']
    seed = kwargs['seed']
    solver = kwargs['solver']
    speed = kwargs['speed']
    cell_size = kwargs['cell_size']

    pygame.init()
    font = pygame.font.SysFont('arial', 16)
    running = True

    raw_maze, start, end = generate_maze(height, width, generator, seed)

    maze = Maze(raw_maze, start, end, cell_size)
    agent = Agent(maze, solver)

    rows, cols = maze.dims()
    cell_size = maze.start.size
    screen = pygame.display.set_mode(
        (rows * cell_size, cols * cell_size), pygame.RESIZABLE
    )
    clock = pygame.time.Clock()
    iterations = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

        screen.fill(DARK_GREY)

        maze.draw(screen)
        agent.draw(screen)
        is_last_step = agent.step()

        if is_last_step:
            agent.draw_shortest_path(screen, cell_size)
        else:
            iterations += 1

        eval_text = font.render(
            f'Iterations={iterations}',
            True,
            WHITE,
        )
        screen.blit(eval_text, (10, 10))

        pygame.display.flip()
        clock.tick(speed)

    result = agent.pathfinding_result
    print('\n------------Evaluation-------------\n')

    print(
        f"""Shortest Path Length: {len(result.shortest_path)}
Cells Visited: {len(result.visited)}
Run Time: {result.run_time:.6f}s,
Peak Memory: {result.peak_memory_bytes} bytes
"""
    )
    pygame.quit()
