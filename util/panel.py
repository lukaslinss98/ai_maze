import pygame
from pygame import Surface

from util.colors import WHITE

PANEL_WIDTH = 220
PANEL_BG = (30, 30, 30)
SEPARATOR_COLOR = (60, 60, 60)
LABEL_COLOR = (180, 180, 180)


def draw_info_panel(
    screen: Surface,
    x: int,
    height: int,
    title: str,
    entries: list[tuple[str, str] | None],
    title_font: pygame.font.Font,
    body_font: pygame.font.Font,
) -> None:
    panel_rect = pygame.Rect(x, 0, PANEL_WIDTH, height)
    pygame.draw.rect(screen, PANEL_BG, panel_rect)

    y = 15

    title_surface = title_font.render(title, True, WHITE)
    screen.blit(title_surface, (x + 15, y))
    y += 30

    pygame.draw.line(screen, SEPARATOR_COLOR, (x + 10, y), (x + PANEL_WIDTH - 10, y))
    y += 15

    for entry in entries:
        if entry is None:
            y += 10
            continue

        label, value = entry
        if label == '---':
            pygame.draw.line(
                screen,
                SEPARATOR_COLOR,
                (x + 10, y),
                (x + PANEL_WIDTH - 10, y),
            )
            y += 15
            continue

        label_surface = body_font.render(f'{label}: ', True, LABEL_COLOR)
        value_surface = body_font.render(str(value), True, WHITE)
        screen.blit(label_surface, (x + 15, y))
        screen.blit(value_surface, (x + 15 + label_surface.get_width(), y))
        y += 22
