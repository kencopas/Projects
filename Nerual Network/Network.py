"""

This class manages the Layers of the neural network. Along with the input-output passing, error and delta calculations happen here, passing those values to each layer for backpropagation
The Network is initialized with a list of layers (Format: At index i, Layer i will be created with layer_list[i] neurons) and an input_count, which represents the number of inputs that
the first layer will recieve.

"""

from Layer import Layer
from image_generator import gen_set

class Network:

    layers = []

    def __init__(self, input_count, layer_list):
        # For each element n at index i in layer list, there are n neurons in layer i
        prev_count = input_count
        prev = None
        for neuron_count in layer_list:
            self.layers.append(Layer(neuron_count, prev_count, prev))
            prev_count = neuron_count
            prev = self.layers[-1]

    # Resets each layer's weight matrix
    def reset(self):
        for layer in self.layers:
            layer.reset()
        
    # Prints the layer info for each layer
    def visualize(self):
        print("")
        for index, layer in enumerate(self.layers):
            print(f"Layer {index}:\n")
            layer.info()
            print("")

    # Trains the network given a dataset and learning rate
    def train(self, data, lr, print_all=False):

        PRINT_INTERVAL = 1 if print_all else (len(data) // 50)          # Interval that prevents every output from printing unless specified
        total_error = 0
        ERROR_INDEX = (len(data) // 5)                                  # Index that starts after the first 20% of the iterations, skipping the learning stage when calculating total error

        # Traverse each image
        for index, (image, y) in enumerate(data.items()):

            cur_inputs = image

            # Feed each neuron in each layer all outputs of the neurons from the previous layer
            for layer in self.layers:
                cur_inputs = layer.fire(cur_inputs)
            
            if index % PRINT_INTERVAL == 0:
                print(f"Correct Output: {y}")
                print(f"Network Output: {round(cur_inputs[0], 3)}\n")

            a = cur_inputs[0]
            
            if index >= ERROR_INDEX:                                    # Increment total error once learning stage (first 20%) has ended
                total_error += abs(a-y)                  
            output_error = (2 * (a - y)) * (a * (1 - a))                # Output Error calculation | Formula: (MSE Derivative) * (Sigmoid Derivative)

            self.backprop([output_error], lr)                           # Start backpropagation

        print(f"Average Error: {round((total_error/len(data))*100, 2)}%")
            

    # Calculates the delta matrix for each layer, and passes that to the layer for gradient calculation
    def backprop(self, output_errors, lr):  

        delta_list = output_errors

        # Traverse all layers backwards, skipping the input layer
        for layer in self.layers[::-1][:-1]:

            new_delta_list = []                                                             # Initialize new delta list

            # Traverse the activation of each neuron
            for i, a in enumerate(layer.prev.activation_list):

                delta_sum = sum(w[i]*d for w, d in zip(layer.weight_matrix, delta_list))    # Weighted delta sum
                new_delta_list.append(delta_sum * a*(1-a))                                  # List of deltas for each neuron in the previous layer | Formula: weighted_delta_sum * sigmoid derivative

            layer.prev.update(new_delta_list, lr)                                           # Update weights and bias for previous layer with calculated deltas
            delta_list = new_delta_list

# This test case creates a network of two layers, each with 30 neurons, and trains it on 10,000 generated 10x10 images with the corresponding correct evaluation
if __name__ == "__main__":

    # Feel free to play with these values
    IMAGE_WIDTH = 10
    TRIALS = 3000
    LEARNING_RATE = 2
    LAYERS = [30, 30, 1] # Format: At index i, Layer i is created with LAYERS[i] neurons
    
    my_network = Network(IMAGE_WIDTH**2, LAYERS)
    my_network.visualize() # Print the network structure
    my_network.train(gen_set(TRIALS, IMAGE_WIDTH), LEARNING_RATE)