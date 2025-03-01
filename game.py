import pygame
import random
from bird import Bird
from pipe import Pipe
from config import GAME_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT, PIPE_GAP, PIPE_FREQUENCY, BIRD_COUNT

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.birds = [Bird() for _ in range(BIRD_COUNT)]  # Initial population using config
        self.pipes = []
        self.score = 0
        self.speed = 1
        self.frame_counter = 0
        self.font = pygame.font.SysFont('Arial', 25)
        self.bg_color = (135, 206, 250)  # Light blue
    
    def update(self):
        # Add new pipe periodically
        if self.frame_counter % PIPE_FREQUENCY == 0:
            gap_y = random.randint(100, SCREEN_HEIGHT - 100 - PIPE_GAP)
            self.pipes.append(Pipe(SCREEN_WIDTH, gap_y))
        
        # Update all game objects
        for _ in range(self.speed):
            # Update pipes
            for pipe in self.pipes:
                pipe.update()
            
            # Remove pipes that have gone off screen
            self.pipes = [pipe for pipe in self.pipes if pipe.x > -pipe.width]
            
            # Update birds
            for bird in self.birds:
                if bird.alive:
                    # Get inputs for neural network
                    closest_pipe = self.get_closest_pipe(bird)
                    
                    if closest_pipe:
                        inputs = [
                            bird.y / SCREEN_HEIGHT,
                            closest_pipe.x / SCREEN_WIDTH,
                            closest_pipe.gap_y / SCREEN_HEIGHT,
                            (closest_pipe.gap_y + PIPE_GAP) / SCREEN_HEIGHT
                        ]
                        
                        # Make decision based on neural network output
                        if bird.think(inputs) > 0.5:
                            bird.jump()
                    
                    bird.update()
                    
                    # Check for collisions
                    if self.check_collision(bird):
                        bird.alive = False
                    else:
                        bird.fitness += 0.1  # Reward for staying alive
                        
                        # Check if bird passed a pipe
                        for pipe in self.pipes:
                            if pipe.x + pipe.width / 2 < bird.x < pipe.x + pipe.width / 2 + 4 and not pipe.passed:
                                bird.fitness += 5  # Reward for passing pipe
                                pipe.passed = True
                                self.score += 1
            
            self.frame_counter += 1
    
    def draw(self):
        # Draw game area background
        pygame.draw.rect(self.screen, self.bg_color, (0, 0, GAME_WIDTH, SCREEN_HEIGHT))
        
        # Draw pipes
        for pipe in self.pipes:
            pipe.draw(self.screen)
        
        # Draw birds
        for bird in self.birds:
            if bird.alive:
                bird.draw(self.screen)
        
        # Draw score and info
        score_text = self.font.render(f'Score: {self.score}', True, (0, 0, 0))
        alive_text = self.font.render(f'Alive: {sum(bird.alive for bird in self.birds)}', True, (0, 0, 0))
        speed_text = self.font.render(f'Speed: {self.speed}x', True, (0, 0, 0))
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(alive_text, (10, 40))
        self.screen.blit(speed_text, (10, 70))
    
    def get_closest_pipe(self, bird):
        closest_pipe = None
        closest_distance = float('inf')
        
        for pipe in self.pipes:
            if pipe.x + pipe.width > bird.x:  # Only consider pipes ahead of bird
                distance = pipe.x - bird.x
                if distance < closest_distance:
                    closest_distance = distance
                    closest_pipe = pipe
        
        return closest_pipe
    
    def check_collision(self, bird):
        # Check if bird hits the floor or ceiling
        if bird.y <= 0 or bird.y >= SCREEN_HEIGHT - bird.height:
            return True
        
        # Check if bird hits a pipe
        for pipe in self.pipes:
            # Check collision with top pipe
            if (bird.x < pipe.x + pipe.width and 
                bird.x + bird.width > pipe.x and 
                bird.y < pipe.gap_y):
                return True
            
            # Check collision with bottom pipe
            if (bird.x < pipe.x + pipe.width and 
                bird.x + bird.width > pipe.x and 
                bird.y + bird.height > pipe.gap_y + PIPE_GAP):
                return True
        
        return False
    
    def all_birds_dead(self):
        return all(not bird.alive for bird in self.birds)
    
    def all_birds_except_one_dead(self):
        """Return True if only one or fewer birds are alive."""
        alive_count = sum(bird.alive for bird in self.birds)
        return alive_count <= 1
    
    def reset(self):
        self.pipes = []
        self.score = 0
        self.frame_counter = 0
