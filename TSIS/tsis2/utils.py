import pygame
from datetime import datetime

def flood_fill(surface, x, y, new_color):
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return

    stack = [(x, y)]

    while stack:
        px, py = stack.pop()

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), new_color)

        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = px + dx, py + dy
            if 0 <= nx < surface.get_width() and 0 <= ny < surface.get_height():
                stack.append((nx, ny))


def save_canvas(surface):
    filename = datetime.now().strftime("drawing_%Y%m%d_%H%M%S.png")
    pygame.image.save(surface, filename)
    print("Saved:", filename)