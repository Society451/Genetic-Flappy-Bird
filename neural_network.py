import numpy as np
import json

class NeuralNetwork:
    def __init__(self, layer_sizes=None, weights=None, biases=None):
        if weights and biases:
            self.weights = weights
            self.biases = biases
            self.layer_sizes = [weights[0].shape[1]] + [w.shape[0] for w in weights]
        else:
            self.layer_sizes = layer_sizes
            self.weights = []
            self.biases = []
            
            # Initialize weights and biases with random values
            for i in range(len(layer_sizes) - 1):
                self.weights.append(np.random.randn(layer_sizes[i+1], layer_sizes[i]))
                self.biases.append(np.random.randn(layer_sizes[i+1], 1))
    
    def feedforward(self, inputs):
        """Feed inputs through the neural network to get outputs."""
        a = np.array(inputs).reshape(-1, 1)  # Convert to column vector
        
        for w, b in zip(self.weights, self.biases):
            a = self.sigmoid(np.dot(w, a) + b)
        
        return a.flatten()  # Convert back to regular array
    
    def sigmoid(self, x):
        """Sigmoid activation function."""
        return 1 / (1 + np.exp(-x))
    
    def copy(self):
        """Create a copy of this neural network."""
        return NeuralNetwork(weights=[w.copy() for w in self.weights], 
                            biases=[b.copy() for b in self.biases])
    
    def mutate(self, rate):
        """Mutate weights and biases by a random amount."""
        for i in range(len(self.weights)):
            # Apply random mutations with probability 'rate'
            mask = np.random.random(self.weights[i].shape) < rate
            self.weights[i] += mask * np.random.randn(*self.weights[i].shape)
            
            mask = np.random.random(self.biases[i].shape) < rate
            self.biases[i] += mask * np.random.randn(*self.biases[i].shape)
    
    def to_dict(self):
        """Convert neural network to dictionary for JSON serialization."""
        return {
            "layer_sizes": self.layer_sizes,
            "weights": [w.tolist() for w in self.weights],
            "biases": [b.tolist() for b in self.biases]
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create neural network from dictionary."""
        weights = [np.array(w) for w in data["weights"]]
        biases = [np.array(b) for b in data["biases"]]
        return cls(weights=weights, biases=biases)
