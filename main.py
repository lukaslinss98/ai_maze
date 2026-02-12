import argparse
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame

from models.maze import Maze
from util import generate_maze


def main(height, width, generator, seed):
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

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

        screen.fill((30, 30, 30))
        maze.draw(screen, cell_size)
        pygame.display.flip()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--height', type=int, default=10)
    parser.add_argument('--width', type=int, default=10)
    parser.add_argument('--seed', type=int)
    parser.add_argument(
        '--generator',
        type=str,
        choices=['prims', 'backtracking', 'aldousbroder', 'binarytree', 'cellular'],
        default='Prims',
    )

    cli_args = parser.parse_args()
    main(cli_args.height, cli_args.width, cli_args.generator, cli_args.seed)
