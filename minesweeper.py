import pygame
import random

# 游戏设置
WIDTH, HEIGHT = 400, 400  # 游戏窗口大小
GRID_SIZE = 10  # 网格的行列数
CELL_SIZE = WIDTH // GRID_SIZE  # 每个格子的大小
NUM_MINES = 10  # 地雷的数量

# 颜色设置
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 游戏状态
game_over = False

# 初始化 pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("扫雷游戏")
font = pygame.font.Font(None, 36)

# 定义格子的状态
UNCLICKED = 0
CLICKED = 1
FLAGGED = 2

# 创建一个空的网格
grid = [[UNCLICKED for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
mine_grid = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
numbers_grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# 随机放置地雷
def place_mines():
    global mine_grid
    count = 0
    while count < NUM_MINES:
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if not mine_grid[x][y]:
            mine_grid[x][y] = True
            count += 1
    calculate_numbers()

# 计算每个格子周围的地雷数量
def calculate_numbers():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if mine_grid[i][j]:
                continue
            mine_count = 0
            for x in range(i-1, i+2):
                for y in range(j-1, j+2):
                    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and mine_grid[x][y]:
                        mine_count += 1
            numbers_grid[i][j] = mine_count

# 显示数字
def draw_numbers():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == CLICKED:
                num = numbers_grid[i][j]
                if num > 0:
                    text = font.render(str(num), True, BLUE)
                    screen.blit(text, (j * CELL_SIZE + CELL_SIZE // 3, i * CELL_SIZE + CELL_SIZE // 3))

# 绘制格子
def draw_grid():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            color = WHITE
            if grid[i][j] == CLICKED:
                color = GRAY
            elif grid[i][j] == FLAGGED:
                color = RED
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

# 点击事件处理
def handle_click(x, y):
    global game_over
    if grid[x][y] != UNCLICKED:
        return
    grid[x][y] = CLICKED
    if mine_grid[x][y]:
        game_over = True
    elif numbers_grid[x][y] == 0:
        reveal_empty_cells(x, y)

# 标记旗帜
def handle_right_click(x, y):
    if grid[x][y] == UNCLICKED:
        grid[x][y] = FLAGGED
    elif grid[x][y] == FLAGGED:
        grid[x][y] = UNCLICKED

# 自动揭示周围的空白格子
def reveal_empty_cells(x, y):
    if numbers_grid[x][y] != 0:
        return
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if 0 <= i < GRID_SIZE and 0 <= j < GRID_SIZE:
                if grid[i][j] == UNCLICKED:
                    grid[i][j] = CLICKED
                    if numbers_grid[i][j] == 0:
                        reveal_empty_cells(i, j)

# 游戏主循环
place_mines()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            x //= CELL_SIZE
            y //= CELL_SIZE
            if event.button == 1:  # 左键点击
                if not game_over:
                    handle_click(y, x)
            elif event.button == 3:  # 右键点击
                if not game_over:
                    handle_right_click(y, x)

    # 绘制背景和网格
    screen.fill(BLACK)
    draw_grid()
    draw_numbers()

    # 游戏结束处理
    if game_over:
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if mine_grid[i][j]:
                    grid[i][j] = CLICKED
        game_over_text = font.render("Game Over!", True, RED)
        screen.blit(game_over_text, (WIDTH // 4, HEIGHT // 2))

    pygame.display.update()
