import json
import numpy as np
from bird import Bird
from neural_network import NeuralNetwork

def save_population(population, filename):
    """Save the current bird population to a JSON file."""
    data = {
        "birds": [
            {
                "fitness": bird.fitness,
                "brain": bird.brain.to_dict()
            }
            for bird in population
        ]
    }
    
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_population(filename):
    """Load bird population from a JSON file."""
    with open(filename, 'r') as f:
        data = json.load(f)
    
    population = []
    
    for bird_data in data["birds"]:
        bird = Bird()
        bird.fitness = bird_data["fitness"]
        bird.brain = NeuralNetwork.from_dict(bird_data["brain"])
        population.append(bird)
    
    return population
