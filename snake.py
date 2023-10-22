import pygame
import time
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
SNAKE_SPEED = 8
DIFFICULTY_LEVELS = [0.5, 0.75, 1.0]

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Initialize the display
gameWindow = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Snake initial position and velocity
snake_x, snake_y = WIDTH // 2, HEIGHT // 2
snake_x_change, snake_y_change = GRID_SIZE, 0

# Snake length
snake_length = 1
snake_body = []

# Food position
food_x, food_y = random.randrange(0, WIDTH - GRID_SIZE, GRID_SIZE), random.randrange(0, HEIGHT - GRID_SIZE, GRID_SIZE)

# Game over flag
game_over = False
retry = False

# Score
score = 0

# Difficulty level
difficulty_level = DIFFICULTY_LEVELS[0]

# Function to display the score on the screen
def show_score(score):
    font = pygame.font.Font(None, 24)
    score_text = font.render("Score: " + str(score), True, WHITE)
    gameWindow.blit(score_text, (10, 10))

# Function to check for collisions
def check_for_collisions():
    global game_over
    for segment in snake_body[:-1]:
        if segment == snake_head:
            game_over = True
            return

    if snake_x >= WIDTH or snake_x < 0 or snake_y >= HEIGHT or snake_y < 0:
        game_over = True

# Function to display the game over screen
def game_over_screen():
    global retry, game_over
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                retry = False
                game_over = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    retry = True
                    game_over = False
                    reset_game()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        gameWindow.fill(BLACK)
        font = pygame.font.Font(None, 48)
        game_over_text = font.render("Game Over!", True, WHITE)
        score_text = font.render("Your Score: " + str(score), True, WHITE)
        retry_text = font.render("Press Enter to Play Again", True, WHITE)
        exit_text = font.render("Press ESC to Exit", True, WHITE)

        gameWindow.blit(game_over_text, (WIDTH // 2 - 120, HEIGHT // 2 - 40))
        gameWindow.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2))
        gameWindow.blit(retry_text, (WIDTH // 2 - 180, HEIGHT // 2 + 60))
        gameWindow.blit(exit_text, (WIDTH // 2 - 130, HEIGHT // 2 + 100))

        pygame.display.update()

# Function to reset the game
def reset_game():
    global snake_x, snake_y, snake_length, snake_body, food_x, food_y, score, game_over
    game_over = False
    snake_x, snake_y = WIDTH // 2, HEIGHT // 2
    snake_x_change, snake_y_change = GRID_SIZE, 0
    snake_length = 1
    snake_body = []
    food_x, food_y = random.randrange(0, WIDTH - GRID_SIZE, GRID_SIZE), random.randrange(0, HEIGHT - GRID_SIZE, GRID_SIZE)
    score = 0

# Main game loop
while not retry:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            retry = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake_x_change = -GRID_SIZE
                snake_y_change = 0
            if event.key == pygame.K_RIGHT:
                snake_x_change = GRID_SIZE
                snake_y_change = 0
            if event.key == pygame.K_UP:
                snake_y_change = -GRID_SIZE
                snake_x_change = 0
            if event.key == pygame.K_DOWN:
                snake_y_change = GRID_SIZE
                snake_x_change = 0

    # Update snake's position
    snake_x += snake_x_change
    snake_y += snake_y_change

    # Check for boundary collisions
    if snake_x >= WIDTH:
        snake_x = 0
    elif snake_x < 0:
        snake_x = WIDTH - GRID_SIZE
    if snake_y >= HEIGHT:
        snake_y = 0
    elif snake_y < 0:
        snake_y = HEIGHT - GRID_SIZE

    # Check for collisions with itself
    check_for_collisions()

    # Draw the game window
    gameWindow.fill(BLACK)

    # Draw the food
    pygame.draw.rect(gameWindow, GREEN, [food_x, food_y, GRID_SIZE, GRID_SIZE])

    # Update the snake's position
    snake_head = {"x": snake_x, "y": snake_y}
    snake_body.append(snake_head)

    if len(snake_body) > snake_length:
        del snake_body[0]

    # Draw the snake
    for segment in snake_body:
        pygame.draw.rect(gameWindow, WHITE, [segment["x"], segment["y"], GRID_SIZE, GRID_SIZE])

    # Display the score
    show_score(score)

    # Update the display
    pygame.display.update()

    # Control the snake's speed
    time.sleep(1 / SNAKE_SPEED * difficulty_level)

    # If the snake eats the food, spawn a new food
    if snake_x == food_x and snake_y == food_y:
        snake_length += 1
        score += 10
        food_x, food_y = random.randrange(0, WIDTH - GRID_SIZE, GRID_SIZE), random.randrange(0, HEIGHT - GRID_SIZE, GRID_SIZE)

    if game_over:
        game_over_screen()

# Quit Pygame
pygame.quit()
sys.exit()
