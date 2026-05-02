import pygame
import math
from utils import flood_fill

class ToolManager:
    def __init__(self):
        self.mode = "pencil"
        self.drawing = False
        self.start_pos = None
        self.last_pos = None

        # text tool
        self.text_mode = False
        self.text = ""
        self.text_pos = None
        self.font = pygame.font.SysFont(None, 28)

    def draw_shape(self, surface, start, end, color, width):
        x1, y1 = start
        x2, y2 = end

        if self.mode == "rect":
            pygame.draw.rect(surface, color, (x1, y1, x2-x1, y2-y1), width)

        elif self.mode == "square":
            side = min(abs(x2-x1), abs(y2-y1))
            pygame.draw.rect(surface, color, (x1, y1, side, side), width)

        elif self.mode == "circle":
            r = int(math.hypot(x2-x1, y2-y1))
            pygame.draw.circle(surface, color, start, r, width)

        elif self.mode == "rtriangle":
            pygame.draw.polygon(surface, color, [start, (x2, y1), end], width)

        elif self.mode == "etriangle":
            side = math.hypot(x2-x1, y2-y1)
            h = (math.sqrt(3)/2)*side
            p1 = start
            p2 = (x1+side, y1)
            p3 = (x1+side/2, y1-h)
            pygame.draw.polygon(surface, color, [p1,p2,p3], width)

        elif self.mode == "rhombus":
            cx = (x1+x2)//2
            cy = (y1+y2)//2
            pts = [(cx,y1),(x2,cy),(cx,y2),(x1,cy)]
            pygame.draw.polygon(surface, color, pts, width)

    def handle_mouse_down(self, pos, canvas, color):
        self.drawing = True
        self.start_pos = pos
        self.last_pos = pos

        if self.mode == "fill":
            flood_fill(canvas.surface, pos[0], pos[1], color)

        if self.mode == "text":
            self.text_mode = True
            self.text = ""
            self.text_pos = pos

    def handle_mouse_up(self, pos, canvas, color, size):
        if not self.drawing:
            return

        if self.mode in ["line", "rect", "square", "circle",
                         "rtriangle", "etriangle", "rhombus"]:
            self.draw_shape(canvas.surface, self.start_pos, pos, color, size)

        self.drawing = False

    def handle_motion(self, pos, canvas, color, size):
        if self.mode == "pencil" and self.drawing:
            pygame.draw.line(canvas.surface, color, self.last_pos, pos, size) # type: ignore
            self.last_pos = pos

    def draw_preview(self, screen, color, size):
        if self.drawing and self.mode != "pencil":
            current = pygame.mouse.get_pos()
            self.draw_shape(screen, self.start_pos, current, color, size)

        if self.text_mode:
            surf = self.font.render(self.text, True, color)
            screen.blit(surf, self.text_pos)

    def handle_text(self, event, canvas, color):
        if not self.text_mode:
            return

        if event.key == pygame.K_RETURN:
            surf = self.font.render(self.text, True, color)
            canvas.surface.blit(surf, self.text_pos)
            self.text_mode = False

        elif event.key == pygame.K_ESCAPE:
            self.text_mode = False

        elif event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]

        else:
            self.text += event.unicode