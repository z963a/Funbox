import pygame

# 初始化 pygame
pygame.init()

# 设置窗口大小
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("乒乓球游戏 - 速度提升版")

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 挡板设置
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 6

# 球的设置
BALL_SIZE = 15
BALL_SPEED_X, BALL_SPEED_Y = 5, 5
speed_multiplier = 1.05  # 每次击中挡板速度增加 5%
max_speed = 12  # 限制最大速度

# 计分板
score1, score2 = 0, 0
font = pygame.font.Font(None, 36)

# 挡板 & 球的初始位置
paddle1 = pygame.Rect(30, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle2 = pygame.Rect(WIDTH-40, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

# 游戏主循环
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 挡板控制（W/S 和 ↑/↓）
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle1.top > 0:
        paddle1.y -= PADDLE_SPEED
    if keys[pygame.K_s] and paddle1.bottom < HEIGHT:
        paddle1.y += PADDLE_SPEED
    if keys[pygame.K_UP] and paddle2.top > 0:
        paddle2.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and paddle2.bottom < HEIGHT:
        paddle2.y += PADDLE_SPEED

    # 移动球
    ball.x += BALL_SPEED_X
    ball.y += BALL_SPEED_Y

    # 碰撞检测（上/下墙壁）
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        BALL_SPEED_Y = -BALL_SPEED_Y  # 反弹

    # 碰撞检测（挡板）
    if ball.colliderect(paddle1) or ball.colliderect(paddle2):
        BALL_SPEED_X = -BALL_SPEED_X  # 反弹
        # 速度逐步增加（但不超过最大速度）
        BALL_SPEED_X *= speed_multiplier
        BALL_SPEED_Y *= speed_multiplier
        BALL_SPEED_X = min(max_speed, max(-max_speed, BALL_SPEED_X))
        BALL_SPEED_Y = min(max_speed, max(-max_speed, BALL_SPEED_Y))

    # 检测得分
    if ball.left <= 0:
        score2 += 1  # 玩家2 得分
        ball.x, ball.y = WIDTH//2, HEIGHT//2  # 重新放置球
        BALL_SPEED_X, BALL_SPEED_Y = 5, 5  # 速度重置
    if ball.right >= WIDTH:
        score1 += 1  # 玩家1 得分
        ball.x, ball.y = WIDTH//2, HEIGHT//2
        BALL_SPEED_X, BALL_SPEED_Y = -5, 5  # 速度重置

    # 绘制挡板、球
    pygame.draw.rect(screen, WHITE, paddle1)
    pygame.draw.rect(screen, WHITE, paddle2)
    pygame.draw.ellipse(screen, WHITE, ball)

    # 绘制中线
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

    # 绘制分数
    score_text = font.render(f"{score1}  -  {score2}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - 30, 20))

    # 刷新屏幕
    pygame.display.flip()
    clock.tick(60)

# 退出游戏
pygame.quit()
