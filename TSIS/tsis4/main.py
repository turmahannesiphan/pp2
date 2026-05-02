import pygame
import random
import sys
import db # Импортируем наш модуль БД

pygame.init()

# Константы
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
WHITE, BLACK, RED, GREEN = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0)
DARK_RED, GOLD, BLUE = (139, 0, 0), (255, 215, 0), (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("Verdana", 20)
clock = pygame.time.Clock()

def get_username():
    user_name = ""
    while True:
        screen.fill(BLACK)
        txt = font.render(f"Enter Name: {user_name}", True, WHITE)
        hint = font.render("Press ENTER to start", True, GREEN)
        screen.blit(txt, (WIDTH//2 - 100, HEIGHT//2 - 20))
        screen.blit(hint, (WIDTH//2 - 100, HEIGHT//2 + 20))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and user_name: return user_name
                elif event.key == pygame.K_BACKSPACE: user_name = user_name[:-1]
                else: 
                    if len(user_name) < 10: user_name += event.unicode

def play_game(username):
    # Начальное состояние
    snake = [[100, 60], [80, 60], [60, 60]]
    direction = 'RIGHT'
    score, level, speed = 0, 1, 10
    obstacles = []
    has_shield = False
    
    # Функция генерации еды (избегая змею и препятствия)[cite: 1]
    def spawn(items):
        while True:
            pos = [random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE)]
            if pos not in snake and pos not in obstacles: return pos

    food = spawn([])
    poison = spawn([food])
    powerup = None
    powerup_timer = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN': direction = 'UP'
                if event.key == pygame.K_DOWN and direction != 'UP': direction = 'DOWN'
                if event.key == pygame.K_LEFT and direction != 'RIGHT': direction = 'LEFT'
                if event.key == pygame.K_RIGHT and direction != 'LEFT': direction = 'RIGHT'

        # Движение[cite: 1]
        head = list(snake[0])
        if direction == 'UP': head[1] -= BLOCK_SIZE
        elif direction == 'DOWN': head[1] += BLOCK_SIZE
        elif direction == 'LEFT': head[0] -= BLOCK_SIZE
        elif direction == 'RIGHT': head[0] += BLOCK_SIZE
        
        # Проверка столкновений (Стены, хвост, препятствия)[cite: 1]
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT or \
           head in snake or head in obstacles:
            if has_shield:
                has_shield = False # Щит спасает один раз
            else:
                return score, level # Конец игры

        snake.insert(0, head)

        # Логика еды[cite: 1]
        if head == food:
            score += 1
            if score % 3 == 0: # Уровень растет каждые 3 очка[cite: 1]
                level += 1
                speed += 2
                if level >= 3: # С 3 уровня добавляем препятствия
                    obstacles.append(spawn([food, poison]))
            food = spawn([poison])
        elif head == poison:
            if len(snake) > 2: # Яд укорачивает змею на 2
                snake.pop(); snake.pop()
            else: return score, level
            poison = spawn([food])
        elif powerup and head == powerup:
            has_shield = True # Бонус щита
            powerup = None
        else:
            snake.pop()

        # Шанс появления бонуса
        if not powerup and random.random() < 0.02:
            powerup = spawn([food, poison])
            powerup_timer = pygame.time.get_ticks()
        
        if powerup and pygame.time.get_ticks() - powerup_timer > 5000:
            powerup = None # Бонус исчезает через 5 сек

        # Отрисовка[cite: 1]
        screen.fill(BLACK)
        for p in snake: pygame.draw.rect(screen, GREEN, (*p, BLOCK_SIZE, BLOCK_SIZE))
        for o in obstacles: pygame.draw.rect(screen, WHITE, (*o, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, RED, (*food, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, DARK_RED, (*poison, BLOCK_SIZE, BLOCK_SIZE))
        if powerup: pygame.draw.ellipse(screen, BLUE, (*powerup, BLOCK_SIZE, BLOCK_SIZE))
        
        info = font.render(f"{username} | Score: {score} Lvl: {level}", True, WHITE)
        screen.blit(info, (10, 10))
        if has_shield: screen.blit(font.render("SHIELD ON", True, BLUE), (10, 35))
        
        pygame.display.flip()
        clock.tick(speed)

def game_over(username, score, level):
    db.save_score(username, score, level) # Сохранение в БД
    while True:
        screen.fill(BLACK)
        msg = font.render(f"GAME OVER, {username}!", True, RED)
        sc = font.render(f"Final Score: {score} | Level: {level}", True, WHITE)
        hint = font.render("Press R to Restart or Q to Quit", True, GREEN)
        screen.blit(msg, (WIDTH//2 - 100, HEIGHT//2 - 60))
        screen.blit(sc, (WIDTH//2 - 100, HEIGHT//2 - 20))
        screen.blit(hint, (WIDTH//2 - 140, HEIGHT//2 + 40))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: return True
                if event.key == pygame.K_q: return False

# ЗАПУСК ИГРЫ
name = get_username()
while True:
    sc, lvl = play_game(name)
    if not game_over(name, sc, lvl): break