import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch the Falling Objects")

# Load images for animated background
background1 = pygame.image.load("background_image.jpg")  # Replace with your layer image
background2 = pygame.image.load("background_image.jpg")  # Replace with your layer image

# Load images for objects and basket
basket_img = pygame.image.load("baskets.png")  # Replace with your basket image
ball_img = pygame.image.load("balls.png")  # Replace with your object image

# Resize images
background1 = pygame.transform.scale(background1, (SCREEN_WIDTH, SCREEN_HEIGHT))
background2 = pygame.transform.scale(background2, (SCREEN_WIDTH, SCREEN_HEIGHT))
basket_img = pygame.transform.scale(basket_img, (100, 60))  # Adjust basket size
ball_img = pygame.transform.scale(ball_img, (40, 40))  # Adjust object size

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
LIGHT_PURPLE = (180, 100, 255)
GRAY = (200, 200, 200)

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Clock for controlling FPS
clock = pygame.time.Clock()


def draw_text(text, size, color, x, y):
    """Helper function to draw text on the screen."""
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


def start_screen():
    """Display the start screen with instructions."""
    running = True
    while running:
        screen.fill(BLACK)
        draw_text("Welcome to Catch the Falling Objects!", 48, LIGHT_PURPLE, SCREEN_WIDTH // 2, 150)
        draw_text("Instructions:", 36, LIGHT_PURPLE, SCREEN_WIDTH // 2, 250)
        draw_text("1. Use LEFT and RIGHT arrow keys to move the basket.", 28, LIGHT_PURPLE, SCREEN_WIDTH // 2, 300)
        draw_text("2. Catch the falling objects to earn points.", 28, LIGHT_PURPLE, SCREEN_WIDTH // 2, 350)
        draw_text("3. The game ends if you miss an object.", 28, LIGHT_PURPLE, SCREEN_WIDTH // 2, 400)
        draw_text("Click 'Start Game' to begin!", 28, LIGHT_PURPLE, SCREEN_WIDTH // 2, 450)

        # Draw "Start Game" button
        pygame.draw.rect(screen, LIGHT_PURPLE, (SCREEN_WIDTH // 2 - 100, 500, 200, 50))
        draw_text("Start Game", 36, BLACK, SCREEN_WIDTH // 2, 525)

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (SCREEN_WIDTH // 2 - 100 <= mouse_x <= SCREEN_WIDTH // 2 + 100) and (500 <= mouse_y <= 550):
                    return  # Start game


def game_over_screen(score):
    """Display the game over screen."""
    while True:
        screen.fill(BLACK)
        draw_text("Game Over!", 72, LIGHT_PURPLE, SCREEN_WIDTH // 2, 200)
        draw_text(f"Your Score: {score}", 48, LIGHT_PURPLE, SCREEN_WIDTH // 2, 300)

        # Draw "Play Again" and "Exit" buttons
        pygame.draw.rect(screen, LIGHT_PURPLE, (SCREEN_WIDTH // 2 - 150, 400, 130, 50))
        draw_text("Play Again", 28, BLACK, SCREEN_WIDTH // 2 - 85, 425)
        pygame.draw.rect(screen, LIGHT_PURPLE, (SCREEN_WIDTH // 2 + 20, 400, 100, 50))
        draw_text("Exit", 28, BLACK, SCREEN_WIDTH // 2 + 70, 425)

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (SCREEN_WIDTH // 2 - 150 <= mouse_x <= SCREEN_WIDTH // 2 - 20) and (400 <= mouse_y <= 450):
                    return True  # Restart game
                if (SCREEN_WIDTH // 2 + 20 <= mouse_x <= SCREEN_WIDTH // 2 + 120) and (400 <= mouse_y <= 450):
                    pygame.quit()
                    sys.exit()


def game_loop():
    """Main game loop."""
    # Basket properties
    basket_width, basket_height = basket_img.get_size()
    basket_x = (SCREEN_WIDTH - basket_width) // 2
    basket_y = SCREEN_HEIGHT - basket_height - 10
    basket_speed = 10

    # Ball properties
    ball_x = random.randint(0, SCREEN_WIDTH - ball_img.get_width())
    ball_y = -40
    ball_speed = 5

    # Score
    score = 0

    # Background positions
    bg1_y = 0
    bg2_y = -SCREEN_HEIGHT

    running = True
    while running:
        # Background animation
        bg1_y += 2
        bg2_y += 2
        if bg1_y >= SCREEN_HEIGHT:
            bg1_y = -SCREEN_HEIGHT
        if bg2_y >= SCREEN_HEIGHT:
            bg2_y = -SCREEN_HEIGHT

        # Draw background
        screen.blit(background1, (0, bg1_y))
        screen.blit(background2, (0, bg2_y))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Move basket
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and basket_x > 0:
            basket_x -= basket_speed
        if keys[pygame.K_RIGHT] and basket_x < SCREEN_WIDTH - basket_width:
            basket_x += basket_speed

        # Move ball
        ball_y += ball_speed

        # Check collision
        if basket_y < ball_y + ball_img.get_height() and basket_x < ball_x + ball_img.get_width() and basket_x + basket_width > ball_x:
            score += 1
            ball_x = random.randint(0, SCREEN_WIDTH - ball_img.get_width())
            ball_y = -40
            ball_speed += 0.2

        # Ball missed
        if ball_y > SCREEN_HEIGHT:
            running = False

        # Draw basket and ball
        screen.blit(basket_img, (basket_x, basket_y))
        screen.blit(ball_img, (ball_x, ball_y))

        # Draw score
        draw_text(f"Score: {score}", 36, WHITE, 70, 30)

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(30)

    return score


# Main loop
while True:
    start_screen()
    final_score = game_loop()
    if not game_over_screen(final_score):
        break
