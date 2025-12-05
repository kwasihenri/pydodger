import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyDodger")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
player_size = 50
player_x = (WIDTH - 50) / 2
player_y = HEIGHT - 50 - 10

try:
    player_img = pygame.transform.scale(pygame.image.load("assets/images/player.png").convert(), (player_size, player_size))
    obstacle_img = pygame.image.load("assets/images/obstacle.png").convert()
    obstacle_fast_img = pygame.image.load("assets/images/obstacle_fast.png").convert()
    obstacle_wide_img = pygame.image.load("assets/images/obstacle_wide.png").convert()
    background_img = pygame.image.load("assets/images/background.png").convert()
    collision_sound = pygame.mixer.Sound("assets/sounds/crash.ogg")
    score_sound = pygame.mixer.Sound("assets/sounds/score.wav")
    game_over_sound = pygame.mixer.Sound("assets/sounds/gameover.ogg")
    pygame.mixer.music.load("assets/sounds/background.mp3")
except pygame.error:
    print("Error loading assets")
    sys.exit()

collision_sound.set_volume(0.5)


player_rect = player_img.get_rect(center=(player_x, player_y))
player_speed = 5

obstacles = []
obstacle_speed = 5
obstacle_types = [
    {'image': obstacle_img, 'speed': obstacle_speed},
    {'image': obstacle_fast_img, 'speed': obstacle_speed + 5},
    {'image': obstacle_wide_img, 'speed': obstacle_speed - 2},
]

clock = pygame.time.Clock()

def main_menu():
    menu_font = pygame.font.Font(None, 74)
    menu_text = menu_font.render("PyDodger", True, BLUE)
    menu_rect = menu_text.get_rect(center=(WIDTH/2, HEIGHT/2 - 40))
    
    start_font = pygame.font.Font(None, 50)
    start_text = start_font.render("Press any key to start", True, BLUE)
    start_rect = start_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 40))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                game_loop()

        screen.blit(background_img, (0, 0))
        screen.blit(menu_text, menu_rect)
        screen.blit(start_text, start_rect)
        pygame.display.flip()

def game_loop():
    pygame.mixer.music.play(-1)
    running = True
    game_over = False
    score = 0
    level = 1
    lives = 3
    font = pygame.font.Font(None, 36)

    invincible = False
    invincible_timer = 0

    player_rect.center = (player_x, player_y)
    obstacles.clear()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
            player_rect.x += player_speed

        if invincible:
            invincible_timer -= 1
            if invincible_timer <= 0:
                invincible = False

        level = 1 + score // 10
        spawn_rate = max(5, 25 - level * 2)
            
        if random.randint(0, spawn_rate) == 0:
            obstacle_type = random.choice(obstacle_types)
            obstacle_img_choice = obstacle_type['image']
            obstacle_speed_choice = obstacle_type['speed']
            obstacle_x = random.randint(0, WIDTH - obstacle_img_choice.get_width())
            obstacle_rect = obstacle_img_choice.get_rect(topleft=(obstacle_x, -obstacle_img_choice.get_height()))
            obstacles.append({'rect': obstacle_rect, 'image': obstacle_img_choice, 'speed': obstacle_speed_choice})

        for obstacle in obstacles[:]:
            obstacle['rect'].y += obstacle['speed'] + level
            if obstacle['rect'].top > HEIGHT:
                obstacles.remove(obstacle)
                score += 1
                score_sound.play()
            if not invincible and player_rect.colliderect(obstacle['rect']):
                obstacles.remove(obstacle)
                lives -= 1
                collision_sound.play()
                if lives <= 0:
                    game_over = True
                    running = False
                else:
                    invincible = True
                    invincible_timer = 120 # 2 seconds at 60fps

        screen.blit(background_img, (0, 0))
        
        if invincible:
            if (invincible_timer // 6) % 2 == 0:
                screen.blit(player_img, player_rect)
        else:
            screen.blit(player_img, player_rect)
            
        for obstacle in obstacles:
            screen.blit(obstacle['image'], obstacle['rect'])

        score_text = font.render(f"Score: {score}", True, BLUE)
        screen.blit(score_text, (10, 10))

        lives_text = font.render(f"Lives: {lives}", True, BLUE)
        screen.blit(lives_text, (WIDTH - 120, 10))
            
        pygame.display.flip()
        
        clock.tick(60)

    if game_over:
        game_over_font = pygame.font.Font(None, 74)
        game_over_text = game_over_font.render("Game Over", True, BLUE)
        game_over_rect = game_over_text.get_rect(center=(WIDTH/2, HEIGHT/2 - 80))
        screen.blit(game_over_text, game_over_rect)

        final_score_text = font.render(f"Final Score: {score}", True, BLUE)
        final_score_rect = final_score_text.get_rect(center=(WIDTH/2, HEIGHT/2 - 20))
        screen.blit(final_score_text, final_score_rect)
        
        play_again_font = pygame.font.Font(None, 50)
        play_again_text = play_again_font.render("Play Again", True, WHITE)
        play_again_rect = pygame.Rect(WIDTH/2 - 100, HEIGHT/2 + 40, 200, 50)
        pygame.draw.rect(screen, BLUE, play_again_rect)
        play_again_text_rect = play_again_text.get_rect(center=play_again_rect.center)
        screen.blit(play_again_text, play_again_text_rect)

        quit_text = play_again_font.render("Quit", True, WHITE)
        quit_rect = pygame.Rect(WIDTH/2 - 100, HEIGHT/2 + 110, 200, 50)
        pygame.draw.rect(screen, BLUE, quit_rect)
        quit_text_rect = quit_text.get_rect(center=quit_rect.center)
        screen.blit(quit_text, quit_text_rect)

        pygame.display.flip()
        
        pygame.mixer.music.stop()
        game_over_sound.play()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_again_rect.collidepoint(event.pos):
                        waiting = False
                        main_menu()
                    if quit_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    else:
                        waiting = False
                        main_menu()
        main_menu()

def main():
    main_menu()

if __name__ == '__main__':
    main()
