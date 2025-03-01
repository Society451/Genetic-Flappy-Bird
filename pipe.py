import pygame
from config import SCREEN_HEIGHT, GAME_WIDTH, PIPE_GAP

class Pipe:
    def __init__(self, x, gap_y):
        self.x = x
        self.gap_y = gap_y
        self.width = 60
        self.speed = 5
        self.color = (0, 128, 0)  # Green
        self.passed = False
    
    def update(self):
        self.x -= self.speed
    
    def draw(self, screen):
        # Draw top pipe
        pygame.draw.rect(screen, self.color, (self.x, 0, self.width, self.gap_y))
        
        # Draw bottom pipe
        bottom_pipe_y = self.gap_y + PIPE_GAP
        bottom_pipe_height = SCREEN_HEIGHT - bottom_pipe_y
        pygame.draw.rect(screen, self.color, (self.x, bottom_pipe_y, self.width, bottom_pipe_height))
        
        # Draw pipe edges
        pygame.draw.rect(screen, (0, 100, 0), (self.x, self.gap_y - 20, self.width, 20))
        pygame.draw.rect(screen, (0, 100, 0), (self.x, self.gap_y + PIPE_GAP, self.width, 20))
