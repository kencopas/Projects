class linear_regression:

    def __init__(self, slope=1, bias=0, learning_rate=0.001):
        self.mb = (slope, bias)
        self.learning_rate = learning_rate

    # Create a list of predicted y values using the formula: ypi = m*xi + b
    def predictions(self):
        m, b = self.mb
        return [(m*x + b) for x in self.inputs]
    
    # Calculate the errors using the actual and predicted values
    def calculate_errors(self, actuals, predictions):
        
        act_pred = zip(actuals, predictions)
        return [actual - predicted for actual, predicted in act_pred]
    
    # Calculate the gradients using the gradient descent formulas: dm = -2/n * sum((yi - ypi) * xi) and db = -2/n * sum(yi - ypi) where (yi - ypi) is already calculated as a list of errors
    def gradients(self, n, errors, inputs):
        
        gd = (-2/n)
        dm = gd * sum(err * x for err, x in zip(errors, inputs))
        db = gd * sum(err for err in errors)
        return (dm, db)

    # Update the weights using the calculated slope and bias gradients and the learning rate
    def update_weights(self, dm, db, lr):
        self.m -= lr * dm
        self.b -= lr * db

    # Train the model using training data and a specified number of iterations
    def train(self, data: list, iterations):

        # Unzip the data into inputs and outputs and establish n as the number of data points
        self.inputs, self.outputs = zip(*data)
        self.n = len(data)

        # Predict, calculate errors, calculate gradients, and update the weights. Repeat for specified iterations
        for _ in range(iterations):
            predictions = self.predictions()
            errors = self.calculate_errors(self.outputs, predictions)
            dm, db = self.gradients(self.n, errors, self.inputs)
            self.update_weights(dm, db, self.learning_rate)

        print(f"Linear equation reached after {iterations} iterations: y = {self.m}x + {self.b}")
        

my_model = linear_regression()
my_model.train()