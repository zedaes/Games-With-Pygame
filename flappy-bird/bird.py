import pygame
import math
from constants import *

class Bird:
    def __init__(self):
        self.x = BIRD_START_X
        self.y = BIRD_START_Y
        self.velocity = 0
        self.gravity = GRAVITY
        self.lift = LIFT
        self.images = [
            pygame.image.load("assets/sprites/bluebird-downflap.png").convert_alpha(),
            pygame.image.load("assets/sprites/bluebird-midflap.png").convert_alpha(),
            pygame.image.load("assets/sprites/bluebird-upflap.png").convert_alpha()
        ]
        self.current_image = 0
        self.animation_counter = 0
        self.angle = 0 

    def flap(self):
        self.velocity = self.lift
        self.angle = 20 

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

        if self.velocity < 0:
            self.angle = min(self.angle + 2, 20) 
        else:
            self.angle = max(self.angle - 2, -90) 

        if self.y < 0:
            self.y = 0
            self.velocity = 0

        if self.y > SCREEN_HEIGHT - BASE_HEIGHT - self.images[0].get_height():
            self.y = SCREEN_HEIGHT - BASE_HEIGHT - self.images[0].get_height()
            self.velocity = 0
            return True 

        self.animation_counter += 1
        if self.animation_counter % 5 == 0:
            self.current_image = (self.current_image + 1) % len(self.images)

        return False 

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.images[self.current_image], self.angle)
        new_rect = rotated_image.get_rect(center=self.images[self.current_image].get_rect(topleft=(self.x, self.y)).center)
        screen.blit(rotated_image, new_rect.topleft)