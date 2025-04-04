from Layer import Layer
from image_generator import gen_set

class Network:

    layers = []

    def __init__(self, input_count, layer_list):
        # For each element n at index i in layer list, there are n neurons in layer i
        prev_count = input_count
        prev_layer = None
        for neuron_count in layer_list:
            self.layers.append(Layer(neuron_count, prev_count, prev_layer))
            prev_count = neuron_count
            prev_layer = self.layers[-1]

    def reset(self):
        for layer in self.layers:
            layer.reset()
        
    def visualize(self):
        print("")
        for index, layer in enumerate(self.layers):
            print(f"Layer {index}:\n")
            layer.info()
            print("")

    def train(self, data, lr):
        c = 0
        total_error = 0
        for image, y in data.items():
            # print(f"Current image: \n\n{image[:3]}\n{image[3:6]}\n{image[6:]}\n\n
            if c % 50 == 0: print(f"Correct Output: {y}")
            cur_inputs = image

            # Feed each neuron in each layer all outputs of the neurons from the previous layer
            for layer in self.layers:
                cur_inputs = layer.fire(cur_inputs)
            
            if c % 50 == 0: print(f"Network Output: {round(cur_inputs[0], 3)}\n")

            c += 1
            a = cur_inputs[0]
            total_error += abs(a-y)
            output_error = (2 * a * (a - y) * (1 - a))

            self.backprop(output_error, lr)

        print(f"Average Error: {round(total_error/100, 2)}%")

        # for layer in self.layers:
        #     layer.show_matrix()
            

    def backprop(self, output_error, lr):
        d = output_error
        for layer in self.layers[::-1][:-1]: # Traverse the layers backwards, skipping the first layer
            prev_layer = layer.prev_layer
            delta_matrix = [[] for _ in range(layer.input_count)]
            for weights in layer.weight_matrix:
                for i, w in enumerate(weights[:-1]): # Output neuron's weight list
                    delta_matrix[i].append(w*d)
            prev_layer.update(delta_matrix, lr)

my_network = Network(9, [30, 30, 1])
my_network.visualize()
my_network.train(gen_set(1000, 10), 10) # Not sure why the learning rate has to be so high for this to work, will troubleshoot further