import pygame
import sys
from persistence import load_settings, save_settings

# ── Цвета ───────────────────────────────────────────────────────────────────
BG        = (20,  20,  30)
PANEL     = (40,  40,  55)
ACCENT    = (0,  200, 255)
WHITE     = (255, 255, 255)
GRAY      = (150, 150, 150)
BTN_IDLE  = (60,  60,  80)
BTN_HOV   = (80,  80, 110)
BTN_ACT   = (0,  160, 200)

CAR_COLORS = ["yellow", "red", "blue", "green", "magenta", "truqouise"]
DIFFICULTIES = ["easy", "normal", "hard"]


# ── Маленький хелпер для кнопки ─────────────────────────────────────────────
def draw_button(surf, rect, text, font, active=False, hovered=False):
    color = BTN_ACT if active else (BTN_HOV if hovered else BTN_IDLE)
    pygame.draw.rect(surf, color, rect, border_radius=8)
    pygame.draw.rect(surf, ACCENT, rect, 2, border_radius=8)
    label = font.render(text, True, WHITE)
    surf.blit(label, label.get_rect(center=rect.center))


# ── Экран настроек ───────────────────────────────────────────────────────────
def settings_screen(screen):
    """Показывает экран настроек. Возвращает обновлённый dict настроек."""
    clock  = pygame.time.Clock()
    font_h = pygame.font.SysFont("Verdana", 28, bold=True)
    font   = pygame.font.SysFont("Verdana", 18)
    font_s = pygame.font.SysFont("Verdana", 14)

    settings = load_settings()
    W, H = screen.get_size()

    # Кнопка "Back"
    back_rect = pygame.Rect(W//2 - 80, H - 60, 160, 40)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_settings(settings)
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                # Sound toggle
                sound_rect = pygame.Rect(W//2 + 20, 150, 120, 36)
                if sound_rect.collidepoint(mx, my):
                    settings["sound"] = not settings["sound"]

                # Car color cycle
                color_rect = pygame.Rect(W//2 + 20, 220, 120, 36)
                if color_rect.collidepoint(mx, my):
                    idx = CAR_COLORS.index(settings["car_color"])
                    settings["car_color"] = CAR_COLORS[(idx + 1) % len(CAR_COLORS)]

                # Difficulty cycle
                diff_rect = pygame.Rect(W//2 + 20, 290, 120, 36)
                if diff_rect.collidepoint(mx, my):
                    idx = DIFFICULTIES.index(settings["difficulty"])
                    settings["difficulty"] = DIFFICULTIES[(idx + 1) % len(DIFFICULTIES)]

                # Back
                if back_rect.collidepoint(mx, my):
                    running = False

        # ── Отрисовка ────────────────────────────────────────────────────────
        screen.fill(BG)

        # Заголовок
        title = font_h.render("SETTINGS", True, ACCENT)
        screen.blit(title, title.get_rect(centerx=W//2, y=80))

        # Строки настроек
        rows = [
            ("Sound",      "ON" if settings["sound"] else "OFF", 150),
            ("Car color",  settings["car_color"].capitalize(),    220),
            ("Difficulty", settings["difficulty"].capitalize(),   290),
        ]
        for label, value, y in rows:
            # Метка слева
            lbl = font.render(label, True, WHITE)
            screen.blit(lbl, (W//2 - 160, y + 6))
            # Кнопка справа (кликабельна)
            btn_rect = pygame.Rect(W//2 + 20, y, 120, 36)
            hovered  = btn_rect.collidepoint(mouse_pos)
            draw_button(screen, btn_rect, value, font, hovered=hovered)
            # Подсказка
            hint = font_s.render("click to change", True, GRAY)
            screen.blit(hint, (W//2 + 148, y + 10))

        # Back
        draw_button(screen, back_rect, "Back", font,
                    hovered=back_rect.collidepoint(mouse_pos))

        pygame.display.flip()
        clock.tick(60)

    save_settings(settings)
    return settings


# ── Main Menu ────────────────────────────────────────────────────────────────
def main_menu(screen):
    """Возвращает: 'play' | 'leaderboard' | 'settings' | 'quit'"""
    clock  = pygame.time.Clock()
    font_h = pygame.font.SysFont("Verdana", 40, bold=True)
    font   = pygame.font.SysFont("Verdana", 20)
    W, H   = screen.get_size()

    items = [("Play",        "play"),
             ("Leaderboard", "leaderboard"),
             ("Settings",    "settings"),
             ("Quit",        "quit")]
    rects = [pygame.Rect(W//2 - 100, 220 + i*70, 200, 46) for i in range(len(items))]

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, (_, action) in zip(rects, items):
                    if rect.collidepoint(event.pos):
                        return action

        screen.fill(BG)
        title = font_h.render("RACER", True, ACCENT)
        screen.blit(title, title.get_rect(centerx=W//2, y=100))
        sub = font.render("Not F1, but still fun!", True, GRAY)
        screen.blit(sub, sub.get_rect(centerx=W//2, y=155))

        for rect, (label, _) in zip(rects, items):
            draw_button(screen, rect, label, font,
                        hovered=rect.collidepoint(mouse_pos))

        pygame.display.flip()
        clock.tick(60)


# ── Game Over ────────────────────────────────────────────────────────────────
def game_over_screen(screen, score, distance, coins):
    """Возвращает: 'retry' | 'menu'"""
    clock  = pygame.time.Clock()
    font_h = pygame.font.SysFont("Verdana", 36, bold=True)
    font   = pygame.font.SysFont("Verdana", 20)
    W, H   = screen.get_size()

    retry_rect = pygame.Rect(W//2 - 110, H - 130, 100, 42)
    menu_rect  = pygame.Rect(W//2 +  10, H - 130, 100, 42)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_rect.collidepoint(event.pos): return 'retry'
                if menu_rect.collidepoint(event.pos):  return 'menu'

        screen.fill(BG)
        title = font_h.render("GAME OVER", True, (255, 80, 80))
        screen.blit(title, title.get_rect(centerx=W//2, y=100))

        stats = [
            f"Score:    {score}",
            f"Distance: {distance} m",
            f"Coins:    {coins}",
        ]
        for i, line in enumerate(stats):
            surf = font.render(line, True, WHITE)
            screen.blit(surf, surf.get_rect(centerx=W//2, y=200 + i*50))

        draw_button(screen, retry_rect, "Retry", font,
                    hovered=retry_rect.collidepoint(mouse_pos))
        draw_button(screen, menu_rect,  "Menu",  font,
                    hovered=menu_rect.collidepoint(mouse_pos))

        pygame.display.flip()
        clock.tick(60)


def leaderboard_screen(screen):
    from persistence import get_top_scores
    clock  = pygame.time.Clock()
    font_h = pygame.font.SysFont("Verdana", 28, bold=True)
    font   = pygame.font.SysFont("Verdana", 17)
    W, H   = screen.get_size()
    back_rect = pygame.Rect(W//2 - 70, H - 60, 140, 40)
    board = get_top_scores()

    # Определяем границы столбцов (x-координаты вертикальных линий)
    # Суммарно ширина таблицы ~340 пикселей (от 30 до 370)
    column_edges = [30, 80, 140, 210, 300, 370] 
    headers = ("Rank", "Name", "Score", "Dist", "Coins")

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos): return

        screen.fill(BG)
        title = font_h.render("LEADERBOARD", True, ACCENT)
        screen.blit(title, title.get_rect(centerx=W//2, y=30))

        # ── Рисуем таблицу ──────────────────────────────────────────────────
        start_y = 90
        row_h   = 35
        table_h = row_h * (len(board) + 1) # +1 для заголовка

        # 1. Горизонтальные линии и текст
        for i in range(len(board) + 2): # +2 линии чтобы закрыть таблицу снизу
            curr_y = start_y + i * row_h
            if i <= len(board) + 1:
                pygame.draw.line(screen, GRAY, (column_edges[0], curr_y), (column_edges[-1], curr_y), 1)
            
            # Пишем текст (заголовок или данные), если это не последняя линия
            if i <= len(board):
                if i == 0: # Заголовок
                    row_data = headers
                    text_color = ACCENT
                else: # Данные игрока
                    entry = board[i-1]
                    row_data = (str(i), entry["name"], str(entry["score"]), 
                                f"{entry['distance']}m", str(entry["coins"]))
                    text_color = (255, 215, 0) if i == 1 else WHITE

                # Рисуем каждую ячейку
                for j in range(len(row_data)):
                    # Вычисляем центр ячейки для центрирования текста
                    cell_x = (column_edges[j] + column_edges[j+1]) // 2
                    cell_y = curr_y + row_h // 2
                    txt_surf = font.render(row_data[j], True, text_color)
                    screen.blit(txt_surf, txt_surf.get_rect(center=(cell_x, cell_y)))

        # 2. Вертикальные линии
        for x in column_edges:
            pygame.draw.line(screen, GRAY, (x, start_y), (x, start_y + table_h), 1)

        # Кнопка Back
        draw_button(screen, back_rect, "Back", font,
                    hovered=back_rect.collidepoint(mouse_pos))
        
        pygame.display.flip()
        clock.tick(60)
        
# ── Username input ───────────────────────────────────────────────────────────
def username_input(screen):
    """Возвращает введённое имя (3 буквы)."""
    clock  = pygame.time.Clock()
    font_h = pygame.font.SysFont("Verdana", 28, bold=True)
    font   = pygame.font.SysFont("Verdana", 60, bold=True)
    font_s = pygame.font.SysFont("Verdana", 16)
    W, H   = screen.get_size()
    name   = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(name) == 3:
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 3 and event.unicode.isalpha():
                    name += event.unicode.upper()

        screen.fill(BG)
        title = font_h.render("ENTER YOUR NAME", True, ACCENT)
        screen.blit(title, title.get_rect(centerx=W//2, y=180))

        name_surf = font.render(name + ("_" if len(name) < 3 else ""), True, (0, 255, 120))
        screen.blit(name_surf, name_surf.get_rect(centerx=W//2, y=260))

        if len(name) == 3:
            hint = font_s.render("Press ENTER to confirm", True, GRAY)
            screen.blit(hint, hint.get_rect(centerx=W//2, y=360))

        pygame.display.flip()
        clock.tick(60)