import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

from models.agent import Agent
from models.maze import Maze
from util.colors import DARK_GREY
from util.maze_generation import generate_maze
from util.panel import PANEL_WIDTH, draw_info_panel


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
    title_font = pygame.font.SysFont('arial', 18, bold=True)
    body_font = pygame.font.SysFont('arial', 14)
    running = True

    raw_maze, start, end = generate_maze(height, width, generator, seed)

    maze = Maze(raw_maze, start, end, cell_size)
    agent = Agent(maze, solver)

    rows, cols = maze.dims()
    cell_size = maze.start.size
    maze_pixel_width = cols * cell_size
    maze_pixel_height = rows * cell_size
    screen = pygame.display.set_mode(
        (maze_pixel_width + PANEL_WIDTH, maze_pixel_height), pygame.RESIZABLE
    )
    clock = pygame.time.Clock()
    iterations = 0
    finished = False
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
            finished = True
        else:
            iterations += 1

        entries = [
            ('Solver', solver),
            ('Generator', generator),
            ('Size', f'{width}x{height}'),
            ('---', ''),
            ('Iteration', str(iterations)),
        ]

        if finished:
            result = agent.pathfinding_result
            entries.extend(
                [
                    ('---', ''),
                    ('Path Length', str(len(result.shortest_path))),
                    ('Visited', str(len(result.visited))),
                    ('Max Frontier', str(result.max_frontier_size)),
                    ('Runtime', f'{result.run_time:.4f}s'),
                    ('Memory', f'{result.peak_memory_bytes} B'),
                ]
            )

        draw_info_panel(
            screen,
            maze_pixel_width,
            screen.get_height(),
            'Pathfinding',
            entries,
            title_font,
            body_font,
        )

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
