import pygame, sys
from settings import *
from canvas import Canvas
from tools import ToolManager
from ui import draw_ui, handle_ui_click
from utils import save_canvas

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont(None, 24)

canvas = Canvas()
tools = ToolManager()

current_color = BLACK
current_size = BRUSH_SIZES[1]

running = True

while running:
    screen.fill(WHITE)
    canvas.draw(screen)
    draw_ui(screen, font)

    tools.draw_preview(screen, current_color, current_size)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                current_size = BRUSH_SIZES[int(event.unicode)]

            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_canvas(canvas.surface)

            tools.handle_text(event, canvas, current_color)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            current_color, current_size = handle_ui_click(
                event.pos, tools, current_color, current_size
            )
            if event.pos[1] < HEIGHT - TOOLBAR_HEIGHT:
                tools.handle_mouse_down(event.pos, canvas, current_color)

        elif event.type == pygame.MOUSEBUTTONUP:
            tools.handle_mouse_up(event.pos, canvas, current_color, current_size)

        elif event.type == pygame.MOUSEMOTION:
            tools.handle_motion(event.pos, canvas, current_color, current_size)

    pygame.display.flip()

pygame.quit()
sys.exit()