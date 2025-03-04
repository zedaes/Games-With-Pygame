import pygame
import random
from constants import *

class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(PIPE_GAP_MIN, PIPE_GAP_MAX)
        self.pipe_bottom = pygame.image.load("assets/sprites/pipe-green.png").convert_alpha()
        self.pipe_top = pygame.transform.flip(self.pipe_bottom, False, True)
        self.passed_by_bird = False

    def update(self):
        self.x -= PIPE_SPEED
        if self.x < -self.pipe_top.get_width():
            self.x = SCREEN_WIDTH
            self.gap_y = random.randint(PIPE_GAP_MIN, PIPE_GAP_MAX)
            self.passed_by_bird = False

    def draw(self, screen):
        screen.blit(self.pipe_top, (self.x, self.gap_y - self.pipe_top.get_height()))
        screen.blit(self.pipe_bottom, (self.x, self.gap_y + PIPE_GAP_HEIGHT))

    def collides_with(self, bird):
        bird_rect = pygame.Rect(bird.x, bird.y, bird.images[0].get_width(), bird.images[0].get_height())
        top_pipe_rect = pygame.Rect(self.x, self.gap_y - self.pipe_top.get_height(), self.pipe_top.get_width(), self.pipe_top.get_height())
        bottom_pipe_rect = pygame.Rect(self.x, self.gap_y + PIPE_GAP_HEIGHT, self.pipe_bottom.get_width(), self.pipe_bottom.get_height())
        return bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect)

    def passed(self, bird):
        if self.x + self.pipe_top.get_width() < bird.x and not self.passed_by_bird:
            self.passed_by_bird = True
            return True
        return False