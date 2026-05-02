import pygame
from settings import WIDTH, HEIGHT, TOOLBAR_HEIGHT, COLORS, BRUSH_SIZES

def draw_ui(screen, font):
    pygame.draw.rect(screen, (220,220,220),
                     (0, HEIGHT-TOOLBAR_HEIGHT, WIDTH, TOOLBAR_HEIGHT))

    y = HEIGHT - TOOLBAR_HEIGHT + 10

    for i, c in enumerate(COLORS):
        pygame.draw.rect(screen, c, (10 + i*50, y, 40, 40))

    for i, key in enumerate(BRUSH_SIZES):
        size = BRUSH_SIZES[key]
        x = 300 + i*60
        pygame.draw.circle(screen, (0,0,0), (x, y+20), size)
        pygame.draw.rect(screen, (0,0,0), (x-20, y, 40, 40), 1)

    tools = [
        "pencil","line","fill","text",
        "rect","circle","square",
        "rtriangle","etriangle","rhombus"
    ]

    for i, t in enumerate(tools):
        x = 10 + i*80
        pygame.draw.rect(screen, (180,180,255), (x, y+50, 70, 40))
        screen.blit(font.render(t[:5], True, (0,0,0)), (x+5, y+60))


def handle_ui_click(pos, tools, current_color, current_size):
    x, y = pos

    if y < HEIGHT - TOOLBAR_HEIGHT:
        return current_color, current_size


    for i, c in enumerate(COLORS):
        if pygame.Rect(10+i*50, HEIGHT-TOOLBAR_HEIGHT+10, 40,40).collidepoint(pos):
            return c, current_size

    for i, key in enumerate(BRUSH_SIZES):
        rect = pygame.Rect(300+i*60-20, HEIGHT-TOOLBAR_HEIGHT+10, 40,40)
        if rect.collidepoint(pos):
            return current_color, BRUSH_SIZES[key]


    tools_list = [
        "pencil","line","fill","text",
        "rect","circle","square",
        "rtriangle","etriangle","rhombus"
    ]

    for i, t in enumerate(tools_list):
        rect = pygame.Rect(10+i*80, HEIGHT-TOOLBAR_HEIGHT+60, 70,40)
        if rect.collidepoint(pos):
            tools.mode = t

    return current_color, current_size