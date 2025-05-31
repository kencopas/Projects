"""

This file generates the training data used on the neural network. It randomly generates a specified number of "images" (a tuple of pixel values between 0 and 1 of length n^2), and evaluates them
based on a randomly generated list of weights, of equal length. A skew is applied to the pixel values to prevent consistency. This evaluation takes the weighted sum and averages it, producing 
a score between 0 and 1. The result is a dictionary with the keys being the tuple of pixel values and the values being the evaluated score.

"""

from random import uniform

# Generates a random weight list and image (tuple of random pixel values),
# then evaluates each list and returns the result as a dictionary
def gen_set(n, length):

    my_dict = {}
    weight_list = [round(uniform(0, 1), 1) for _ in range(length**2)] # List of hidden weights

    for _ in range(n):
        skew = uniform(0, 2)  # Random skew applied to the pixel values to prevent consistency
        new_image = tuple(uniform(0, 1)**skew for _ in range(length**2))  # Random pixel values between 0 and 1
        my_dict[new_image] = eval_image(new_image, weight_list)  # Output data: Key=Image, Value=Evaluation Score

    return my_dict

# Evaluates the images by taking a weighted sum and averaging it, returning a score between 1 and 0
def eval_image(image, weight_graph):
    return round(sum([w*x for w, x in zip(weight_graph, image)])/sum(weight_graph), 3)
