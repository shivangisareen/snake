from os import ST_RDONLY, terminal_size
import pygame, random

pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Ssssnake")

# Set FPS and Clock 
FPS = 20
clock = pygame.time.Clock()

# Set game values
SNAKE_SIZE = 20

head_x = WINDOW_WIDTH//2
head_y = WINDOW_HEIGHT//2 + 100

# keep track of direction of snake
snake_dx = 0
snake_dy = 0

score = 0

# Set colours 
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARKGREEN = (10,50,10)
DARKRED = (150, 0, 0)
WHITE = (255,255,255)
BLACK = (0,0,0)

# Set fonts 
font = pygame.font.SysFont('gabriola', 48)

# Set text 
title_text = font.render("SNAKE", True, GREEN)
title_rect = title_text.get_rect()
title_rect.center = (WINDOW_WIDTH//2, 25)

score_text = font.render("Score: " + str(score), True, GREEN)
score_rect = score_text.get_rect()
score_rect.topleft = (10,10)

game_over_text = font.render("GAME OVER", True, RED, DARKGREEN)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = font.render("Press any button to continue", True, RED, DARKGREEN)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50)


# Set sound and music 
pick_up_sound = pygame.mixer.Sound("./snake/assets/pick_up_sound.wav")


# Set images (in this case use simple rects so just create their coordinates)
# for a rectangle: top-left x, top-left y, width, height
apple_coord = (500, 500, SNAKE_SIZE, SNAKE_SIZE)
apple_rect = pygame.draw.rect(display_surface, RED, apple_coord)

head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)
head_rect = pygame.draw.rect(display_surface, GREEN, head_coord)

body_coords = []


# main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # move the snake
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake_dx = -1 * SNAKE_SIZE
                snake_dy = 0
            
            if event.key == pygame.K_RIGHT:
                snake_dx = SNAKE_SIZE
                snake_dy = 0
            
            if event.key == pygame.K_UP:
                snake_dx = 0
                snake_dy = -1 * SNAKE_SIZE
            
            if event.key == pygame.K_DOWN:
                snake_dx = 0
                snake_dy = SNAKE_SIZE

    # add the head coordinate to the first index of the body coordinate list
    # this will essentially move all the snakes body by one position on the list
    body_coords.insert(0, head_coord)
    body_coords.pop()

    # update the x and y position of the snake head
    head_x += snake_dx
    head_y += snake_dy
    head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)

    # check for game over
    if head_rect.left < 0 or head_rect.right > WINDOW_WIDTH or head_rect.top < 0 or head_rect.bottom > WINDOW_HEIGHT or head_coord in body_coords:
        # snake is off the screen
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()

        # pause the game until the player until the player presses a key, the reset the game
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                # the player wants to play again
                if event.type == pygame.KEYDOWN:
                    score = 0
                    head_x = WINDOW_WIDTH//2
                    head_y = WINDOW_HEIGHT//2 + 100
                    head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)

                    body_coords = []

                    snake_dx = 0
                    snake_dy = 0

                    is_paused = False
                
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False

    # check for collisions
    if head_rect.colliderect(apple_rect):
        score += 1
        pick_up_sound.play()

        apple_x = random.randint(0, WINDOW_WIDTH - SNAKE_SIZE)
        apple_y = random.randint(0, WINDOW_HEIGHT - SNAKE_SIZE)
        apple_coord = (apple_x, apple_y, SNAKE_SIZE, SNAKE_SIZE)
        body_coords.append(head_coord)

    # update HUD
    score_text = font.render("Score: " + str(score), True, GREEN)
    
    # fill the surface
    display_surface.fill(BLACK)

    # blit the HUD
    display_surface.blit(title_text, title_rect)
    display_surface.blit(score_text, score_rect)
    # pygame.draw.line(display_surface, GREEN, (0, 50),(WINDOW_WIDTH, 50), 1)


    # blit assets
    for body in body_coords:
        pygame.draw.rect(display_surface, DARKGREEN, body)

    head_rect = pygame.draw.rect(display_surface, GREEN, head_coord)
    apple_rect = pygame.draw.rect(display_surface, RED, apple_coord)

    # update display and tick clock
    pygame.display.update()
    clock.tick(FPS)

# end the game
pygame.quit()