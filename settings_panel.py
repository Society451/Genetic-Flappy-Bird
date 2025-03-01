import pygame
from config import GAME_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT
from utils import save_population, load_population

class Button:
    def __init__(self, x, y, width, height, text, color=(200, 200, 200), hover_color=(150, 150, 150)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.SysFont('Arial', 16)
        
    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Border
        
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.text = text
        self.font = pygame.font.SysFont('Arial', 16)
        self.active = False
        
    def draw(self, screen):
        # Draw slider track
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Border
        
        # Calculate handle position
        handle_x = self.rect.x + int((self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width)
        handle_rect = pygame.Rect(handle_x - 5, self.rect.y - 5, 10, self.rect.height + 10)
        pygame.draw.rect(screen, (100, 100, 100), handle_rect)
        
        # Draw text and value
        text_surface = self.font.render(f"{self.text}: {self.value:.2f}", True, (0, 0, 0))
        screen.blit(text_surface, (self.rect.x, self.rect.y - 20))
        
    def update(self, mouse_pos):
        if self.active:
            # Calculate new value based on mouse position
            relative_x = max(0, min(mouse_pos[0] - self.rect.x, self.rect.width))
            self.value = self.min_val + (self.max_val - self.min_val) * (relative_x / self.rect.width)
            return True
        return False
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.active = False

class SettingsPanel:
    def __init__(self, genetic_algorithm):
        self.genetic_algorithm = genetic_algorithm
        self.x = GAME_WIDTH
        self.width = SCREEN_WIDTH - GAME_WIDTH
        self.height = SCREEN_HEIGHT
        self.bg_color = (240, 240, 240)
        self.font = pygame.font.SysFont('Arial', 20)
        
        # Create UI elements
        self.save_button = Button(self.x + 20, 50, 160, 40, "Save Population")
        self.load_button = Button(self.x + 20, 100, 160, 40, "Load Population")
        self.mutation_slider = Slider(self.x + 20, 180, 160, 20, 0.01, 0.5, self.genetic_algorithm.mutation_rate, "Mutation Rate")
        self.speed_slider = Slider(self.x + 20, 240, 160, 20, 1, 100, self.genetic_algorithm.game.speed, "Game Speed")
        
        # Toggle for vector visualization
        self.show_vectors_button = Button(self.x + 20, 300, 160, 40, "Toggle Vectors")
        self.genetic_algorithm.game.show_vectors = False
        
    def draw(self, screen):
        # Draw panel background
        pygame.draw.rect(screen, self.bg_color, (self.x, 0, self.width, self.height))
        pygame.draw.line(screen, (0, 0, 0), (self.x, 0), (self.x, self.height), 2)
        
        # Draw title
        title_text = self.font.render("Settings", True, (0, 0, 0))
        screen.blit(title_text, (self.x + 20, 15))
        
        # Draw UI elements
        self.save_button.draw(screen)
        self.load_button.draw(screen)
        self.mutation_slider.draw(screen)
        self.speed_slider.draw(screen)
        self.show_vectors_button.draw(screen)
        
    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        
        # Update button hover states
        self.save_button.check_hover(mouse_pos)
        self.load_button.check_hover(mouse_pos)
        self.show_vectors_button.check_hover(mouse_pos)
        
        # Handle slider events
        self.mutation_slider.handle_event(event)
        self.speed_slider.handle_event(event)
        
        if self.mutation_slider.update(mouse_pos):
            self.genetic_algorithm.mutation_rate = self.mutation_slider.value
            
        if self.speed_slider.update(mouse_pos):
            self.genetic_algorithm.game.speed = int(self.speed_slider.value)
        
        # Handle button clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.save_button.is_clicked(mouse_pos, True):
                save_population(self.genetic_algorithm.population, "population.json")
                print("Population saved")
            
            if self.load_button.is_clicked(mouse_pos, True):
                try:
                    population = load_population("population.json")
                    self.genetic_algorithm.population = population
                    self.genetic_algorithm.game.birds = population
                    print("Population loaded")
                except:
                    print("No saved population found")
                    
            if self.show_vectors_button.is_clicked(mouse_pos, True):
                self.genetic_algorithm.game.show_vectors = not self.genetic_algorithm.game.show_vectors
                self.show_vectors_button.text = "Hide Vectors" if self.genetic_algorithm.game.show_vectors else "Show Vectors"
