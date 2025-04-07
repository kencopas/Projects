"""

This was my first attempt at a neural network from the ground up. It was not scalable, so I switched to a Layer class instead with each neuron as a list in a weight matrix.

"""

import math
from image_generator import gen_set

class Perceptron:
  def __init__(self, input_count, index):
    self.index = index # Neuron index within layer
    self.input_count = input_count
    self.weights = [1 for _ in range(input_count)]
    self.bias = 0

  # Creates a list of predicited y values based on training x values
  def weighted_sum(self, inputs):
    return sum(x*w for x, w in zip(inputs, self.weights)) + self.bias
  
  def sigmoid(self, x):
    return 1 / (1 + math.exp(-x))
  
  # data: list of length n containing tuples of length 2
  def activate(self, x):
    sigmo = self.sigmoid(z)
    return sigmo
  
  def fire(self, inputs):
    self.inputs = inputs
    z = self.weighted_sum(inputs)
    self.a = self.sigmoid(z)
    return self.a
  
  def get_delta(self, delta_list, lr):
    my_delta = self.weighted_sum(delta_list)*self.a*(1-self.a)
    self.update_weights(my_delta, lr)

  def print_update(self, text):
    fweights = [round(w, 3) for w in self.weights]
    print(f"{text}: {fweights}, {round(self.bias, 3)}")
  
  def update_weights(self, delta, lr):
      for i in range(self.input_count):
        wg = delta * self.inputs[i] # Weight Gradient
        self.weights[i] -= lr*wg
      bg = delta # Bias Gradient
      self.bias -= lr*bg
    
  def info(self):
    print(f"Perceptron ({self.input_count})")

if __name__ == "__main__":
  pass
  # sloper = Perceptron(9)
  # images = gen_set(1000)
  # sloper.train(images, 4)
