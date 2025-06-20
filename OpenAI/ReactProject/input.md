File Structure:

```json
{
  "project_directory_name": "neural_network",
  "project_directory_path": "C:\\Users\\kenneth.copas\\OneDrive - PeopleShores PBC\\Desktop\\Projects\\neural_network",
  "subdirectories": {
    "Snapshot": {
      "image_generator.py": "from random import uniform\n\n\n# my_image = (0.4, 0.4, 0.4,\n#             0.4, 0, 0,\n#             0.2, 0.8, 0)\n\n\ndef gen_set(n, length):\n    \"\"\"\n    Generates a random set of images evaluated against a weight graph.\n    \"\"\"\n    my_dict = {}\n    weight_graph = [round(uniform(0, 1), 1) for _ in range(length**2)]\n    \n    for _ in range(n):\n        skew = round(uniform(0, 2))\n        new_image = tuple(\n            round(uniform(0, 1)**skew, 3) for _ in range(length**2)\n        )\n        my_dict[new_image] = eval_image(new_image, weight_graph)\n    \n    return my_dict\n\n\ndef eval_image(image, weight_graph):\n    \"\"\"\n    Evaluates the image by calculating a weighted average score.\n    \"\"\"\n    return round(\n        sum(w * x for w, x in zip(weight_graph, image)) / sum(weight_graph), 3\n    )",
      "layer.py": "from image_generator import gen_set\nimport math\nfrom random import uniform\n\n\nclass Layer:\n    def __init__(self, neuron_count, input_count, prev_layer):\n        \"\"\"\n        Initializes the Layer with neurons and weight matrix.\n        \"\"\"\n        self.prev_layer = prev_layer\n        self.neuron_count = neuron_count\n        self.input_count = input_count\n        self.weight_matrix = [\n            [uniform(-0.5, 0.5) for _ in range(input_count + 1)]\n            for _ in range(neuron_count)\n        ]\n\n    def reset(self):\n        \"\"\"\n        Resets the weight matrix with new random weights.\n        \"\"\"\n        self.weight_matrix = [\n            [uniform(-0.5, 0.5) for _ in range(self.input_count + 1)]\n            for _ in range(self.neuron_count)\n        ]\n\n    def update(self, delta_matrix, lr):\n        \"\"\"\n        Updates weights and biases based on the delta matrix and learning rate.\n        \"\"\"\n        for index in range(len(delta_matrix)):\n            delta_list = delta_matrix[index]\n            a = self.activation_list[index]\n            delta = sum(delta_list) * a * (1 - a)\n            for i in range(len(self.weight_matrix[index]) - 1):\n                self.weight_matrix[index][i] -= lr * delta * self.inputs[i]\n            self.weight_matrix[index][-1] -= lr * delta\n\n    def sigmoid(self, x):\n        \"\"\"\n        Sigmoid activation function.\n        \"\"\"\n        return 1 / (1 + math.exp(-x))\n\n    def fire(self, image):\n        \"\"\"\n        Processes input data through the layer and returns the activations.\n        \"\"\"\n        self.inputs = image\n        activation_list = []\n        for index, weights in enumerate(self.weight_matrix):\n            z = sum(x * w for x, w in zip(image, weights[:-1])) + weights[-1]\n            a = self.sigmoid(z)\n            activation_list.append(a)\n        \n        self.activation_list = activation_list\n        return activation_list\n\n    def info(self):\n        \"\"\"\n        Prints the layer information.\n        \"\"\"\n        print(f\"Neurons: {self.neuron_count}, Inputs: {self.input_count}\")\n\n    def show_matrix(self):\n        \"\"\"\n        Displays the weight matrix and biases.\n        \"\"\"\n        for weights in self.weight_matrix:\n            print(f\"W: {[round(w, 3) for w in weights[:-1]]} | B: {round(weights[-1], 3)}\")",
      "network.py": "from Layer import Layer\nfrom image_generator import gen_set\n\nclass Network:\n\n    layers = []\n\n    def __init__(self, input_count, layer_list):\n        # For each element n at index i in layer list, there are n neurons in layer i\n        prev_count = input_count\n        prev_layer = None\n        for neuron_count in layer_list:\n            self.layers.append(Layer(neuron_count, prev_count, prev_layer))\n            prev_count = neuron_count\n            prev_layer = self.layers[-1]\n\n    def reset(self):\n        for layer in self.layers:\n            layer.reset()\n        \n    def visualize(self):\n        print(\"\")\n        for index, layer in enumerate(self.layers):\n            print(f\"Layer {index}:\\n\")\n            layer.info()\n            print(\"\")\n\n    def train(self, data, lr):\n        c = 0\n        total_error = 0\n        for image, y in data.items():\n            # print(f\"Current image: \\n\\n{image[:3]}\\n{image[3:6]}\\n{image[6:]}\\n\\n\n            if c % 50 == 0: print(f\"Correct Output: {y}\")\n            cur_inputs = image\n\n            # Feed each neuron in each layer all outputs of the neurons from the previous layer\n            for layer in self.layers:\n                cur_inputs = layer.fire(cur_inputs)\n            \n            if c % 50 == 0: print(f\"Network Output: {round(cur_inputs[0], 3)}\\n\")\n\n            c += 1\n            a = cur_inputs[0]\n            total_error += abs(a-y)\n            output_error = (2 * a * (a - y) * (1 - a))\n\n            self.backprop(output_error, lr)\n\n        print(f\"Average Error: {round(total_error/100, 2)}%\")\n\n        # for layer in self.layers:\n        #     layer.show_matrix()\n            \n\n    def backprop(self, output_error, lr):\n        d = output_error\n        for layer in self.layers[::-1][:-1]: # Traverse the layers backwards, skipping the first layer\n            prev_layer = layer.prev_layer\n            delta_matrix = [[] for _ in range(layer.input_count)]\n            for weights in layer.weight_matrix:\n                for i, w in enumerate(weights[:-1]): # Output neuron's weight list\n                    delta_matrix[i].append(w*d)\n            prev_layer.update(delta_matrix, lr)\n\nmy_network = Network(9, [30, 30, 1])\nmy_network.visualize()\nmy_network.train(gen_set(10000, 3), 10) # Not sure why the learning rate has to be so high for this to work, will troubleshoot further"
    },
    "__pycache__": {},
    "image_generator.py": "\"\"\"\nThis file generates the training data used on the neural network. It randomly generates a specified number of \"images\" (a tuple of pixel values between 0 and 1 of length n^2), and evaluates them\nbased on a randomly generated list of weights, of equal length. A skew is applied to the pixel values to prevent consistency. This evaluation takes the weighted sum and averages it, producing \na score between 0 and 1. The result is a dictionary with the keys being the tuple of pixel values and the values being the evaluated score.\n\"\"\"\n\nfrom random import uniform\n\n\ndef gen_set(n, length):\n    \"\"\"\n    Generates a random weight list and image (tuple of random pixel values),\n    then evaluates each list and returns the result as a dictionary\n    \"\"\"\n    my_dict = {}\n    weight_list = [\n        round(uniform(0, 1), 1) for _ in range(length**2)\n    ]  # List of hidden weights\n\n    for _ in range(n):\n        skew = uniform(0, 2)  # Random skew applied to the pixel values to prevent consistency\n        new_image = tuple(\n            uniform(0, 1)**skew for _ in range(length**2)\n        )  # Random pixel values between 0 and 1\n        my_dict[new_image] = eval_image(\n            new_image, weight_list\n        )  # Output data: Key=Image, Value=Evaluation Score\n\n    return my_dict\n\n\ndef eval_image(image, weight_graph):\n    \"\"\"\n    Evaluates the images by taking a weighted sum and averaging it,\n    returning a score between 1 and 0\n    \"\"\"\n    return round(\n        sum(w * x for w, x in zip(weight_graph, image)) /\n        sum(weight_graph), 3\n    )",
    "layer.py": "\"\"\"\nThis was my second attempt at building a neural network, after realizing the a perceptron class was not scalable. This class holds each neuron as a list of weights, with the last element \nbeing the bias, within a larger weight matrix. This makes backpropagation much easier, along with the linked singly-linked nature of this class.\n\"\"\"\n\nfrom image_generator import gen_set\nimport math\nfrom random import uniform\n\n\nclass Layer:\n    \n    def __init__(self, neuron_count, input_count, prev):\n        \"\"\"\n        Initializes the number of neurons in the layer, the number of inputs for each neuron, \n        and a point to the previous layer.\n        \"\"\"\n        self.prev = prev\n        self.neuron_count = neuron_count\n        self.input_count = input_count\n        self.weight_matrix = [\n            [uniform(-1, 1) for _ in range(input_count + 1)] \n            for _ in range(neuron_count)\n        ]  # Uniform random initialization\n\n    def reset(self):\n        \"\"\"\n        Reinitializes the weight matrix after each training set, in case of multiple \n        training sets in one run.\n        \"\"\"\n        self.weight_matrix = [\n            [uniform(-0.5, 0.5) for _ in range(self.input_count + 1)] \n            for _ in range(self.neuron_count)\n        ]\n\n    def update(self, delta_list, lr):\n        \"\"\"\n        Takes a weighted delta matrix during backpropagation and calculates the delta \n        for the current neuron, then updates the weights and bias by calculating the gradients.\n        \"\"\"\n        for index, delta in enumerate(delta_list):\n            for i in range(self.input_count):\n                weight_gradient = lr * delta * self.inputs[i]\n                self.weight_matrix[index][i] -= weight_gradient\n            \n            bias_gradient = lr * delta\n            self.weight_matrix[index][-1] -= bias_gradient\n\n    def fire(self, image):\n        \"\"\"\n        Takes input data, calculates the activation for each neuron in the layer, \n        and returns the activation list.\n        \"\"\"\n        self.inputs = image\n        activation_list = []\n        \n        for weights in self.weight_matrix:\n            z = sum(x * w for x, w in zip(image, weights[:-1])) + weights[-1]\n            a = sigmoid(z)\n            activation_list.append(a)\n        \n        self.activation_list = activation_list\n        return activation_list\n\n    def info(self):\n        \"\"\"Prints the layer info.\"\"\"\n        print(f\"Neurons: {self.neuron_count}, Inputs: {self.input_count}\")\n\n    def show_matrix(self):\n        \"\"\"Prints the weight matrix.\"\"\"\n        for weights in self.weight_matrix:\n            print(f\"W: {[round(w, 3) for w in weights[:-1]]} | B: {round(weights[-1], 3)}\")\n\n\ndef sigmoid(x):\n    \"\"\"Sigmoid activation function.\"\"\"\n    return 1 / (1 + math.exp(-x))",
    "network.py": "\"\"\"\nThis class manages the Layers of the neural network. Along with the input-output passing,\nerror and delta calculations happen here, passing those values to each layer for backpropagation.\nThe Network is initialized with a list of layers (Format: At index i, Layer i will be created \nwith layer_list[i] neurons) and an input_count, which represents the number of inputs that\nthe first layer will receive.\n\"\"\"\n\nfrom layer import Layer\nfrom image_generator import gen_set\n\n\nclass Network:\n\n    def __init__(self, input_count, layer_list):\n        \"\"\"\n        Initializes the network layers.\n        \"\"\"\n        self.layers = []\n        prev_count = input_count\n        prev = None\n        for neuron_count in layer_list:\n            self.layers.append(Layer(neuron_count, prev_count, prev))\n            prev_count = neuron_count\n            prev = self.layers[-1]\n\n    def reset(self):\n        \"\"\"\n        Resets each layer's weight matrix.\n        \"\"\"\n        for layer in self.layers:\n            layer.reset()\n\n    def visualize(self):\n        \"\"\"\n        Prints the layer info for each layer.\n        \"\"\"\n        print(\"\")\n        for index, layer in enumerate(self.layers):\n            print(f\"Layer {index}:\\n\")\n            layer.info()\n            print(\"\")\n\n    def train(self, data, lr, print_all=False):\n        \"\"\"\n        Trains the network given a dataset and learning rate.\n        \"\"\"\n        PRINT_INTERVAL = 1 if print_all else (len(data) // 50)\n        total_error = 0\n        ERROR_INDEX = (len(data) // 5)\n\n        for index, (image, y) in enumerate(data.items()):\n\n            cur_inputs = image\n\n            for layer in self.layers:\n                cur_inputs = layer.fire(cur_inputs)\n\n            if index % PRINT_INTERVAL == 0:\n                print(f\"Correct Output: {y}\")\n                print(f\"Network Output: {round(cur_inputs[0], 3)}\\n\")\n\n            a = cur_inputs[0]\n\n            if index >= ERROR_INDEX:\n                total_error += abs(a - y)\n            output_error = (2 * (a - y)) * (a * (1 - a))\n\n            self.backprop([output_error], lr)\n\n        print(f\"Average Error: {round((total_error / len(data)) * 100, 2)}%\")\n\n    def backprop(self, output_errors, lr):\n        \"\"\"\n        Calculates the delta matrix for each layer, and passes that to the \n        layer for gradient calculation.\n        \"\"\"\n        delta_list = output_errors\n\n        for layer in self.layers[::-1][:-1]:\n            new_delta_list = []\n\n            for i, a in enumerate(layer.prev.activation_list):\n                delta_sum = sum(w[i] * d for w, d in zip(layer.weight_matrix, delta_list))\n                new_delta_list.append(delta_sum * a * (1 - a))\n\n            layer.prev.update(new_delta_list, lr)\n            delta_list = new_delta_list\n\n\nif __name__ == \"__main__\":\n\n    IMAGE_WIDTH = 10\n    TRIALS = 3000\n    LEARNING_RATE = 2\n    LAYERS = [30, 30, 1]\n\n    my_network = Network(IMAGE_WIDTH**2, LAYERS)\n    my_network.visualize()\n    my_network.train(gen_set(TRIALS, IMAGE_WIDTH), LEARNING_RATE)\n",
    "perceptron.py": "\"\"\"\nThis was my first attempt at a neural network from the ground up.\nIt was not scalable, so I switched to a Layer class instead with each neuron as a list in a weight matrix.\n\"\"\"\n\nimport math\nfrom image_generator import gen_set\n\n\nclass Perceptron:\n    def __init__(self, input_count):\n        self.input_count = input_count\n        self.weights = [1 for _ in range(input_count)]\n        self.bias = 0\n\n    def weighted_sum(self, inputs):\n        \"\"\"\n        Creates a list of predicted y values based on training x values.\n        \"\"\"\n        return sum(x * w for x, w in zip(inputs, self.weights)) + self.bias\n\n    def sigmoid(self, x):\n        \"\"\"\n        Sigmoid activation function.\n        \"\"\"\n        return 1 / (1 + math.exp(-x))\n\n    def fire(self, inputs):\n        self.inputs = inputs\n        z = self.weighted_sum(inputs)\n        self.a = self.sigmoid(z)\n        return self.a\n\n    def get_delta(self, delta_list, lr):\n        my_delta = self.weighted_sum(delta_list) * self.a * (1 - self.a)\n        self.update_weights(my_delta, lr)\n\n    def print_update(self, text):\n        fweights = [round(w, 3) for w in self.weights]\n        print(f\"{text}: {fweights}, {round(self.bias, 3)}\")\n  \n    def update_weights(self, delta, lr):\n        for i in range(self.input_count):\n            wg = delta * self.inputs[i]\n            self.weights[i] -= lr * wg\n        bg = delta\n        self.bias -= lr * bg\n    \n    def info(self):\n        print(f\"Perceptron ({self.input_count})\")"
  }
}
```

**STDOUT:**
```
Layer 0:

Neurons: 30, Inputs: 100

Layer 1:

Neurons: 30, Inputs: 30

Layer 2:

Neurons: 1, Inputs: 30

Correct Output: 0.278
Network Output: 0.067

Correct Output: 0.429
Network Output: 0.566

Correct Output: 0.637
Network Output: 0.773

Correct Output: 0.62
Network Output: 0.549

Correct Output: 0.524
Network Output: 0.441

Correct Output: 0.438
Network Output: 0.471

Correct Output: 0.388
Network Output: 0.343

Correct Output: 0.443
Network Output: 0.308

Correct Output: 0.452
Network Output: 0.4

Correct Output: 0.547
Network Output: 0.582

Correct Output: 0.496
Network Output: 0.519

Correct Output: 0.664
Network Output: 0.651

Correct Output: 0.567
Network Output: 0.673

Correct Output: 0.385
Network Output: 0.26

Correct Output: 0.994
Network Output: 0.866

Correct Output: 0.534
Network Output: 0.468

Correct Output: 0.425
Network Output: 0.419

Correct Output: 0.325
Network Output: 0.346

Correct Output: 0.728
Network Output: 0.772

Correct Output: 0.463
Network Output: 0.465

Correct Output: 0.855
Network Output: 0.826

Correct Output: 0.392
Network Output: 0.398

Correct Output: 0.589
Network Output: 0.625

Correct Output: 0.667
Network Output: 0.558

Correct Output: 0.38
Network Output: 0.362

Correct Output: 0.682
Network Output: 0.723

Correct Output: 0.374
Network Output: 0.339

Correct Output: 0.346
Network Output: 0.404

Correct Output: 0.332
Network Output: 0.308

Correct Output: 0.442
Network Output: 0.424

Correct Output: 0.847
Network Output: 0.771

Correct Output: 0.424
Network Output: 0.396

Correct Output: 0.947
Network Output: 0.884

Correct Output: 0.427
Network Output: 0.48

Correct Output: 0.429
Network Output: 0.461

Correct Output: 0.503
Network Output: 0.489

Correct Output: 0.617
Network Output: 0.572

Correct Output: 0.356
Network Output: 0.316

Correct Output: 0.42
Network Output: 0.405

Correct Output: 0.52
Network Output: 0.394

Correct Output: 0.36
Network Output: 0.346

Correct Output: 0.461
Network Output: 0.52

Correct Output: 0.363
Network Output: 0.352

Correct Output: 0.334
Network Output: 0.307

Correct Output: 0.968
Network Output: 0.83

Correct Output: 0.577
Network Output: 0.609

Correct Output: 0.507
Network Output: 0.58

Correct Output: 0.431
Network Output: 0.417

Correct Output: 0.754
Network Output: 0.828

Correct Output: 0.486
Network Output: 0.474

Average Error: 3.88%
```

**STDERR:**
```
[No output]
```