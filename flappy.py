import pygame
import random

# Window dimensions
WIDTH = 400
HEIGHT = 600

# Bird dimensions
BIRD_WIDTH = 50
BIRD_HEIGHT = 40

# Pipe dimensions
PIPE_WIDTH = 70
PIPE_HEIGHT = 400
PIPE_GAP = 200

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

pygame.init()

# Create the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 36)


def display_score(score):
    text = font.render("Score: " + str(score), True, BLACK)
    window.blit(text, (10, 10))


def draw_bird(x, y):
    pygame.draw.rect(window, BLUE, (x, y, BIRD_WIDTH, BIRD_HEIGHT))


def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(window, GREEN, (pipe[0], 0, PIPE_WIDTH, pipe[1]))
        pygame.draw.rect(
            window,
            GREEN,
            (pipe[0], pipe[1] + PIPE_GAP, PIPE_WIDTH, HEIGHT - pipe[1] - PIPE_GAP),
        )


def is_collision(bird_x, bird_y, pipes):
    if bird_y < 0 or bird_y + BIRD_HEIGHT > HEIGHT:
        return True

    for pipe in pipes:
        if (
            bird_x + BIRD_WIDTH > pipe[0]
            and bird_x < pipe[0] + PIPE_WIDTH
            and (bird_y < pipe[1] or bird_y + BIRD_HEIGHT > pipe[1] + PIPE_GAP)
        ):
            return True

    return False


def game_over(score):
    game_over_text = font.render("Game Over!", True, BLACK)
    score_text = font.render("Score: " + str(score), True, BLACK)
    window.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    window.blit(score_text, (WIDTH // 2 - 70, HEIGHT // 2))


def flappy_bird():
    bird_x = 50
    bird_y = HEIGHT // 2 - BIRD_HEIGHT // 2
    bird_velocity = 0

    pipes = []
    pipe_width = PIPE_WIDTH + PIPE_GAP
    pipe_timer = 1500  # Add a new pipe every 1.5 seconds
    pipe_speed = 3

    score = 0

    game_over_flag = False

    while not game_over_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = -10

        bird_y += bird_velocity
        bird_velocity += 0.5

        if bird_velocity > 10:
            bird_velocity = 10

        window.fill(WHITE)

        if len(pipes) > 0 and pipes[0][0] + PIPE_WIDTH < 0:
            pipes.pop(0)

        if len(pipes) == 0 or WIDTH - pipes[-1][0] > pipe_width:
            pipe_height = random.randint(50, HEIGHT - PIPE_GAP - 50)
            pipes.append([WIDTH, pipe_height])

        draw_pipes(pipes)
        draw_bird(bird_x, bird_y)

        if is_collision(bird_x, bird_y, pipes):
            game_over_flag = True

        for pipe in pipes:
            pipe[0] -= pipe_speed

        if not game_over_flag:
            display_score(score)
            score += 1

        pygame.display.update()
        clock.tick(60)

    game_over(score)
    pygame.display.update()
    pygame.time.wait(2000)
    pygame.quit()
    quit()


flappy_bird()
