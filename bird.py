import pygame
import numpy as np
from neural_network import NeuralNetwork
from config import SCREEN_HEIGHT

class Bird:
    def __init__(self, brain=None):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.width = 30
        self.height = 30
        self.velocity = 0
        self.gravity = 0.6
        self.jump_force = -10
        self.alive = True
        self.fitness = 0
        self.color = (255, 255, 0)  # Yellow
        
        # Create neural network brain
        if brain:
            self.brain = brain.copy()
        else:
            # Neural network with 4 inputs, 6 hidden neurons, and 1 output
            self.brain = NeuralNetwork([4, 6, 1])
    
    def update(self):
        # Apply gravity
        self.velocity += self.gravity
        self.y += self.velocity
    
    def jump(self):
        self.velocity = self.jump_force
    
    def think(self, inputs):
        return self.brain.feedforward(inputs)[0]
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        # Draw eyes
        pygame.draw.circle(screen, (0, 0, 0), (self.x + self.width - 7, self.y + 10), 5)
        
        # Draw beak
        pygame.draw.polygon(screen, (255, 140, 0), [
            (self.x + self.width, self.y + 15),
            (self.x + self.width + 10, self.y + 15),
            (self.x + self.width, self.y + 20)
        ])
    
    def mutate(self, rate):
        self.brain.mutate(rate)
