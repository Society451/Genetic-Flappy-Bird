import pygame
import sys
from game import Game
from genetic_algorithm import GeneticAlgorithm
from utils import save_population, load_population
from settings_panel import SettingsPanel

def main():
    pygame.init()
    pygame.display.set_caption("Genetic Flappy Bird")
    
    # Initialize game and genetic algorithm
    game = Game()
    genetic_algorithm = GeneticAlgorithm(game)
    settings_panel = SettingsPanel(genetic_algorithm)
    
    # Check if a saved population exists
    try:
        population = load_population("population.json")
        genetic_algorithm.population = population
        game.birds = population
        print("Loaded saved population")
    except:
        print("Starting with new population")
    
    generation = 1
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Handle settings panel events
            settings_panel.handle_event(event)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    save_population(genetic_algorithm.population, "population.json")
                    print("Population saved")
                if event.key == pygame.K_l:
                    try:
                        genetic_algorithm.population = load_population("population.json")
                        game.birds = genetic_algorithm.population
                        print("Population loaded")
                    except:
                        print("No saved population found")
                if event.key == pygame.K_SPACE:
                    game.speed = 1 if game.speed > 1 else 5
        
        # Run game simulation
        game.update()
        game.draw()
        
        # Draw settings panel
        settings_panel.draw(game.screen)
        
        # If all birds except one are dead, create a new generation
        if game.all_birds_except_one_dead():
            print(f"Generation {generation} complete")
            print(f"Best fitness: {genetic_algorithm.calculate_best_fitness()}")
            generation += 1
            genetic_algorithm.evolve()
            game.reset()
        
        clock.tick(60)
        pygame.display.flip()

if __name__ == "__main__":
    main()
