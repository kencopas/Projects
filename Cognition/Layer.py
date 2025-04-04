from image_generator import gen_set
import math
from random import uniform

class Layer:

    def __init__(self, neuron_count, input_count, prev_layer):

        self.prev_layer = prev_layer
        self.neuron_count = neuron_count
        self.input_count = input_count
        self.weight_matrix = [[uniform(-0.5, 0.5) for _ in range(input_count+1)] for _ in range(neuron_count)]
        # self.show_matrix()

    def reset(self):
        self.weight_matrix = [[uniform(-0.5, 0.5) for _ in range(self.input_count+1)] for _ in range(self.neuron_count)]

    def update(self, delta_matrix, lr):
        for index in range(len(delta_matrix)):
            delta_list = delta_matrix[index]
            a = self.activation_list[index]
            delta = sum(delta_list)*a*(1-a)
            for i in range(len(self.weight_matrix[index])-1):
                self.weight_matrix[index][i] -= lr * delta * self.inputs[i]
            self.weight_matrix[index][-1] -= lr * delta

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def fire(self, image):
        self.inputs = image
        activation_list = []
        # Feed the image tuple into each row of the weight matrix
        for index, weights in enumerate(self.weight_matrix):
            z = sum(x*w for x, w in zip(image, weights[:-1])) + weights[-1]
            a = self.sigmoid(z)
            activation_list.append(a)
            #print(f"Activation for neuron {index}: {round(a, 3)}")

        #print(f"Activation List: {[round(a, 3) for a in activation_list]}")
        
        self.activation_list = activation_list
        return activation_list

    def info(self):
        print(f"Neurons: {self.neuron_count}, Inputs: {self.input_count}")

    def show_matrix(self):
        for weights in self.weight_matrix:
            print(f"W: { [round(w, 3) for w in weights[:-1]]} | B: {round(weights[-1], 3)}")