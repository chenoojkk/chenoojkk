import pygame
import random
import sys

# 初始化 Pygame
pygame.init()

# 定义常量
TILE_SIZE = 100
ROWS, COLS = 7, 7
FPS = 30
WINDOW_WIDTH = COLS * TILE_SIZE
WINDOW_HEIGHT = ROWS * TILE_SIZE + 300  # 增加高度以容纳存储区域
STORAGE_HEIGHT = 100  # 存储区域的高度
WHITE = (255, 255, 255)
BLACK = (100, 100, 100)
BG_COLOR = (200, 200, 200)
STORAGE_Y = ROWS * TILE_SIZE
STORAGE_X = 0
STORAGE_WIDTH = WINDOW_WIDTH
# 定义不同难度下的最大存储量
DIFFICULTY_SETTINGS = {
    '简单': 7,
    '中等': 5,
    '困难': 4
}
MAX_STORAGE_COUNT = DIFFICULTY_SETTINGS['简单']  # 默认难度为简单
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BUTTON_X = (WINDOW_WIDTH - BUTTON_WIDTH) // 2
BUTTON_Y = WINDOW_HEIGHT - BUTTON_HEIGHT
BUTTON_COLOR = (100, 100, 255)
BUTTON_TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (100, 100, 255)
BUTTON_HOVER_COLOR = (150, 150, 255)
GAME_OVER_COLOR = (255, 0, 0)
COUNTDOWN_SECONDS = 240  # 倒计时总时长（秒）
pygame.mixer.music.load("dieforu.mp3")
# 创建窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption("瓦了个瓦")

# 加载图案图片
patterns = [pygame.image.load(f"pattern_{i}.png") for i in range(1, 8)]
patterns = [pygame.transform.scale(p, (TILE_SIZE, TILE_SIZE)) for p in patterns]

# 加载背景图片
bg_image = pygame.image.load("background1.jpg")
bg_image = pygame.transform.scale(bg_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

# 加载背景图片
bg_1_image = pygame.image.load("background2.jpg")
bg_1_image = pygame.transform.scale(bg_1_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

# 加载背景图片
bg_2_image = pygame.image.load("background3.jpg")
bg_2_image = pygame.transform.scale(bg_2_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

# 创建图片池
max_count = 21
image_pool = []
for pattern in patterns:
    image_pool.extend([pattern] * max_count)

# 打乱图片池
random.shuffle(image_pool)

# 创建游戏板
click_counts = [[0 for _ in range(COLS)] for _ in range(ROWS)]
board = []
for row in range(ROWS):
    board_row = []
    for col in range(COLS):
        # 从图片池中选取元素并移除
        element = image_pool.pop()
        board_row.append(element)
    board.append(board_row)
selected = []
stored_patterns = []

# 绘制按钮
def draw_button(text, rect, color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, rect)
    else:
        pygame.draw.rect(screen, color, rect)
    
    font = pygame.font.SysFont(None, 36)
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=rect.center)  # 将文字矩形居中于按钮矩形
    screen.blit(text_surf, text_rect)

# 游戏开始界面
def start_screen():
    while True:
        screen.blit(bg_2_image, (0, 0))  # 绘制背景图片
        font = pygame.font.SysFont(None, 48)
        
        # 绘制按钮
        draw_button("Start Game", pygame.Rect(WINDOW_WIDTH  // 2 - 100, WINDOW_HEIGHT // 2 - 50, 220, 50), BUTTON_COLOR, BUTTON_HOVER_COLOR)
        draw_button("Select Difficulty", pygame.Rect(WINDOW_WIDTH  // 2 - 100, WINDOW_HEIGHT // 2 + 30, 220, 50), BUTTON_COLOR, BUTTON_HOVER_COLOR)
        draw_button("Exit Game", pygame.Rect(WINDOW_WIDTH  // 2 - 100, WINDOW_HEIGHT // 2 + 110, 220, 50), BUTTON_COLOR, BUTTON_HOVER_COLOR)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if pygame.Rect(WINDOW_WIDTH  // 2 - 100, WINDOW_HEIGHT // 2 - 30, 220, 50).collidepoint(mouse_pos):
                    start_game()
                elif pygame.Rect(WINDOW_WIDTH  // 2 - 100, WINDOW_HEIGHT // 2 + 30, 220, 50).collidepoint(mouse_pos):
                    draw_difficulty_menu()
                    handle_difficulty_selection()
                elif pygame.Rect(WINDOW_WIDTH  // 2 - 100, WINDOW_HEIGHT // 2 + 110, 220, 50).collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
        
        pygame.display.flip()

# 难度选择
def choose_difficulty(difficulty):
    global MAX_STORAGE_COUNT
    if difficulty in DIFFICULTY_SETTINGS:
        MAX_STORAGE_COUNT = DIFFICULTY_SETTINGS[difficulty]

def draw_difficulty_menu():
    screen.blit(bg_image, (0, 0))  # 绘制背景图片
    font1 = pygame.font.Font(None, 20)
    font = pygame.font.Font(None, 45)
    text = font.render('Select Difficulty', True, (0, 0, 0))
    text1 = font1.render('The number indicates the maximum ', True, (0, 0, 0))
    text2 = font1.render('number of images that can be selected', True, (0, 0, 0))
    screen.blit(text, (WINDOW_WIDTH  // 2 - 120, WINDOW_HEIGHT // 2 - 170))
    screen.blit(text1, (WINDOW_WIDTH  // 2 - 120, WINDOW_HEIGHT // 2 + 170))
    screen.blit(text2, (WINDOW_WIDTH  // 2 - 120, WINDOW_HEIGHT // 2 + 190))
    draw_button("simple(7)", pygame.Rect(WINDOW_WIDTH  // 2 - 100, WINDOW_HEIGHT // 2 - 50, 220, 50), BUTTON_COLOR, BUTTON_HOVER_COLOR)
    draw_button("medium(5)", pygame.Rect(WINDOW_WIDTH  // 2 - 100, WINDOW_HEIGHT // 2 + 30, 220, 50), BUTTON_COLOR, BUTTON_HOVER_COLOR)
    draw_button("hard(4)", pygame.Rect(WINDOW_WIDTH  // 2 - 100, WINDOW_HEIGHT // 2 + 110, 220, 50), BUTTON_COLOR, BUTTON_HOVER_COLOR)
    pygame.display.flip()

def handle_difficulty_selection():
    global MAX_STORAGE_COUNT
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if pygame.Rect(WINDOW_WIDTH  // 2 - 100, WINDOW_HEIGHT // 2 - 30, 220, 50).collidepoint(mouse_pos):
                    choose_difficulty('简单')
                    return
                elif pygame.Rect(WINDOW_WIDTH  // 2 - 100, WINDOW_HEIGHT // 2 + 30, 220, 50).collidepoint(mouse_pos):
                    choose_difficulty('中等')
                    return
                elif pygame.Rect(WINDOW_WIDTH  // 2 - 100, WINDOW_HEIGHT // 2 + 110, 220, 50).collidepoint(mouse_pos):
                    choose_difficulty('困难')
                    return

# 创建使图片随机的按钮
def draw_button_shuffle():
    pygame.draw.rect(screen, BUTTON_COLOR, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
    font = pygame.font.Font(None, 36)
    text = font.render('Shuffle', True, BUTTON_TEXT_COLOR)
    text_rect = text.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2))
    screen.blit(text, text_rect)

def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            tile = board[row][col]
            if tile is not None:
                screen.blit(tile, (col * TILE_SIZE, row * TILE_SIZE))
    for row, col in selected:
        pygame.draw.rect(screen, (255, 0, 0), (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 3)

def draw_storage():
    for i, pattern in enumerate(stored_patterns):
        if pattern is not None:
            x = STORAGE_X + (i % 7) * TILE_SIZE
            y = STORAGE_Y + (i // 7) * TILE_SIZE + 100
            screen.blit(pattern, (x, y))

def check_storage():
    global stored_patterns
    pattern_count = {}
    for pattern in stored_patterns:
        pattern_count[pattern] = pattern_count.get(pattern, 0) + 1

    stored_patterns = [pattern for pattern in stored_patterns if pattern_count[pattern] < 3]

    if len(stored_patterns) > MAX_STORAGE_COUNT:
        game_over_bad()
        pygame.quit()
        exit()

def check_click(row, col):
    global stored_patterns

    if board[row][col] is not None:
        clicked_image = board[row][col]
        board[row][col] = None
        stored_patterns.append(clicked_image)
        check_storage()
        click_counts[row][col] += 1
        if click_counts[row][col] < 3:
            new_image = image_pool.pop()
            board[row][col] = new_image
        else:
            board[row][col] = None  # 位置已被选择三次，置为空
      

def check_button_click(x, y):
    if BUTTON_X <= x <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
        shuffle_images()

def shuffle_images():
    global board
    flat_board = [board[row][col] for row in range(ROWS) for col in range(COLS) if click_counts[row][col] < 3]
    # 过滤掉已点击超过三次的位置
    unclicked_positions = [(row, col) for row in range(ROWS) for col in range(COLS) if click_counts[row][col] < 3]
    # 打乱未点击位置的图片
    random.shuffle(flat_board)
    # 将打乱后的图片分配到未点击位置
    index = 0
    for row in range(ROWS):
        for col in range(COLS):
            if click_counts[row][col] < 3:
                board[row][col] = flat_board[index]
                index += 1
    # 保持已点击位置的图片不变
    for row in range(ROWS):
        for col in range(COLS):
            if click_counts[row][col] >= 3:
                # 确保位置的图片不会被覆盖
                pass

# 点击开始游戏游戏后循环
def start_game():
    running = True
    number = 0
    start_time = pygame.time.get_ticks()  # 获取游戏开始时的时间
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col, row = x // TILE_SIZE, y  // TILE_SIZE
                if row < ROWS and col < COLS:
                    check_click(row, col)
                    number = number + 1
                else:
                    check_button_click(x, y)
         # 检查倒计时
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # 计算经过的时间（秒）
        remaining_time = COUNTDOWN_SECONDS - elapsed_time
        if remaining_time <= 0:
            game_over_bad()
            pygame.quit()
            exit()
        
        screen.blit(bg_1_image, (0, 0))  # 绘制背景图片
        draw_board()
        draw_button_shuffle()
        draw_storage()
        # 绘制倒计时
        font = pygame.font.SysFont(None, 36)
        timer_text = font.render(f"Time Left: {int(remaining_time)}s", True, (255, 0, 0))
        screen.blit(timer_text, (10, 700))
        pygame.display.flip()
        # 检查游戏是否结束
        if number >= 147:
            game_over_good()
            pygame.quit()
            exit()


def game_over_good():
    font = pygame.font.SysFont(None, 48)
    text = font.render("Successfully!", True, GAME_OVER_COLOR)
    screen.blit(bg_image, (0, 0))  # 绘制背景图片
    screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)  # 显示2秒钟

def game_over_bad():
    
    font = pygame.font.SysFont(None, 48)
    text = font.render("Game Over!", True, GAME_OVER_COLOR)
    screen.blit(bg_image, (0, 0))  # 绘制背景图片
    screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)  # 显示2秒钟
pygame.mixer.music.play(-1)  # 循环播放音乐
clock = pygame.time.Clock()
start_screen()    
pygame.quit()
