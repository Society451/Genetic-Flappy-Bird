import random
import numpy as np
from bird import Bird
from config import BIRD_COUNT

class GeneticAlgorithm:
    def __init__(self, game, mutation_rate=0.1):
        self.game = game
        self.population = self.game.birds
        self.mutation_rate = mutation_rate
    
    def calculate_best_fitness(self):
        """Calculate the highest fitness score in the population."""
        return max(bird.fitness for bird in self.population) if self.population else 0
    
    def select_parent(self):
        """Select a parent bird using fitness-based selection."""
        # Calculate sum of fitness scores
        total_fitness = sum(bird.fitness for bird in self.population)
        
        if total_fitness == 0:
            # If all fitness scores are zero, select randomly
            return random.choice(self.population)
        
        # Select parent based on fitness probability
        selection_point = random.uniform(0, total_fitness)
        current_sum = 0
        
        for bird in self.population:
            current_sum += bird.fitness
            if current_sum >= selection_point:
                return bird
        
        # Fallback
        return self.population[-1]
    
    def crossover(self, parent1, parent2):
        """Create a child bird with traits from both parents."""
        child = Bird()
        
        # Crossover weights and biases
        for i in range(len(parent1.brain.weights)):
            # Decide which parent's weights and biases to use for each neuron
            mask = np.random.random(parent1.brain.weights[i].shape) < 0.5
            child.brain.weights[i] = np.where(mask, parent1.brain.weights[i], parent2.brain.weights[i])
            
            mask = np.random.random(parent1.brain.biases[i].shape) < 0.5
            child.brain.biases[i] = np.where(mask, parent1.brain.biases[i], parent2.brain.biases[i])
        
        return child
    
    def evolve(self):
        """Create a new generation of birds using selection, crossover, and mutation."""
        new_population = []
        
        # Find the best bird (might be the only one alive)
        best_bird = max(self.population, key=lambda bird: bird.fitness)
        new_population.append(Bird(best_bird.brain))
        
        # Create the rest of the population based on the best bird
        for _ in range(BIRD_COUNT - 1):
            child = Bird(best_bird.brain)
            child.mutate(self.mutation_rate)
            new_population.append(child)
        
        # Replace old population with new one
        self.population = new_population
        self.game.birds = new_population
