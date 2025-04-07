"""

This was my second attempt at building a neural network, after realizing the a perceptron class was not scalable. This class holds each neuron as a list of weights, with the last element 
being the bias, within a larger weight matrix. This makes backpropagation much easier, along with the linked singly-linked nature of this class.

"""

from image_generator import gen_set
import math
from random import uniform

class Layer:

    # Initializes the number of nuerons in the layer, the number of inputs for each neuron, and a point to the previous layer
    def __init__(self, neuron_count, input_count, prev_layer):

        self.prev_layer = prev_layer
        self.neuron_count = neuron_count
        self.input_count = input_count
        self.weight_matrix = [[uniform(-1, 1) for _ in range(input_count+1)] for _ in range(neuron_count)] # Uniform random initialization

    # Reinitializes the weight matrix after each training set, in the case of multiple training sets in one run
    def reset(self):
        self.weight_matrix = [[uniform(-0.5, 0.5) for _ in range(self.input_count+1)] for _ in range(self.neuron_count)]

    # Takes a weighted delta matrix during backpropagation and calculates the delta for the current neuron. Then updates the weights and bias by calculating the gradients
    def update(self, delta_matrix, lr):

        output_delta_list = []
        
        # Traverses the weighted delta matrix, each interation focusing on a single neuron
        for index in range(len(delta_matrix)):
            
            cur_delta_list = delta_matrix[index]                # Store weighted delta list
            a = self.activation_list[index]                     # Store activation
            delta = sum(cur_delta_list)*a*(1-a)                 # Calculate delta | Formula: (Weighted Delta Sum) * (Sigmoid Derivative)

            # Traverses each weight within the current neurons weight list
            for i in range(len(self.weight_matrix[index])-1):
                weight_gradient = lr * delta * self.inputs[i]
                self.weight_matrix[index][i] -= weight_gradient # Weight update
            
            bias_gradient = lr * delta
            self.weight_matrix[index][-1] -= bias_gradient      # Bias update

            output_delta_list.append(delta)                     # Append each calculated delta to the output list before returning it

        return output_delta_list

    # Takes input data, calculates the activation for each neuron in the layer, and returns the activation list
    def fire(self, image):

        self.inputs = image # Stores inputs for reference during backpropagation
        activation_list = []
        
        # Feed the image tuple into each row of the weight matrix
        for index, weights in enumerate(self.weight_matrix):
            z = sum(x*w for x, w in zip(image, weights[:-1])) + weights[-1] # Weighted Sum + Bias
            a = sigmoid(z)                                                  # Applies activation function
            activation_list.append(a)                                       # Appends activation to the list
        
        self.activation_list = activation_list # Stores activation list for reference during backpropagation
        return activation_list

    # Prints the layer info
    def info(self):
        print(f"Neurons: {self.neuron_count}, Inputs: {self.input_count}")

    # Prints the weight matrix
    def show_matrix(self):
        for weights in self.weight_matrix:
            print(f"W: { [round(w, 3) for w in weights[:-1]]} | B: {round(weights[-1], 3)}")

# Sigmoid activation function
def sigmoid(x):
    return 1 / (1 + math.exp(-x))