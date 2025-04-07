# Projects
This repository holds my first attempt at creating a neural network from scratch. The structure is most likely unconventional as I am personally implementing the matrix multiplication and calculus behind backpropagation.
## Perceptron Class
I originally created this class as a blueprint for each neuron in a network. I was able to make a neural network with two neurons work using this class, but upon attempting to implement backpropagation for a network of even six neurons I realized this approach was not scalable.
## Layer Class
Because the only unique attributes held by each neuron instance was a list of weights and a bias, I created a Layer class instead that holds a matrix of weights with the last element as the bias for each neuron. This made backpropagation much easier and the network more scalable, however, with the calculations behind backpropagation being incredibly complex, this class proved very difficult to create effectively.
## Network Class
This class acts as a Layer manager, overseeing the passing of inputs and outputs forward along with the error calculations backwards. The biggest challenge I faced with this class was deciding what portion of the calculations to perform within the Network as opposed to within the Layer, as many calculations are incredibly complicated, require referencing past variables, and can be combined for efficiency.
##
