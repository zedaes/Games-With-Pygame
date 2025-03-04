import pygame
from bird import Bird
from pipe import Pipe
from constants import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

background = pygame.image.load("assets/sprites/background-day.png").convert()
base = pygame.image.load("assets/sprites/base.png").convert()
font = pygame.font.Font(None, 40)
start_image = pygame.image.load("assets/sprites/message.png").convert_alpha()
game_over_image = pygame.image.load("assets/sprites/gameover.png").convert_alpha()

wing_sound = pygame.mixer.Sound("assets/audio/wing.ogg")
hit_sound = pygame.mixer.Sound("assets/audio/hit.ogg")
point_sound = pygame.mixer.Sound("assets/audio/point.ogg")

def draw_score(score):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def start_screen():
    screen.blit(background, (0, 0))
    screen.blit(start_image, (SCREEN_WIDTH // 2 - start_image.get_width() // 2, SCREEN_HEIGHT // 2 - start_image.get_height() // 2))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
    return True

def game_over_screen(score):
    screen.blit(background, (0, 0))
    screen.blit(game_over_image, (SCREEN_WIDTH // 2 - game_over_image.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_image.get_height() // 2))
    score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
    return True

def main():
    if not start_screen():
        return

    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + i * PIPE_GAP) for i in range(2)]
    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()
                    wing_sound.play()

        if bird.update():
            hit_sound.play()
            running = False

        for pipe in pipes:
            pipe.update()
            if pipe.collides_with(bird):
                hit_sound.play()
                running = False
            if pipe.passed(bird):
                score += 1
                point_sound.play()

        screen.blit(background, (0, 0))
        for pipe in pipes:
            pipe.draw(screen)
        bird.draw(screen)
        screen.blit(base, (0, SCREEN_HEIGHT - BASE_HEIGHT))
        draw_score(score)

        pygame.display.update()
        clock.tick(FPS)

    if game_over_screen(score):
        main()

if __name__ == "__main__":
    main()