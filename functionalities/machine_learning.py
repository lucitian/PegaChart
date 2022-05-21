import numpy as np
from sklearn.metrics import mean_absolute_percentage_error

class LinearRegression:
    """
    Linear Regression is a machine learning algorithm that predicts continuous values based on given parameters.
    """
    def __init__(self):
        """
        Initializes different class-wide variables.
        """
        self.X = np.array([])
        self.y = np.array([])
        self.thetas = np.zeros([])
        self.theta_history = []
        self.cost_history = []
        self.gradient_history = []
        self.norm_max = 0
    
    def fit_data(self, X, y):
        """
        Fits the dataset into the model.
        """
        self.X = np.matrix(X)
        self.y = np.matrix(y).reshape([np.size(y),1])
        self.thetas = np.matrix(np.zeros([len(X.columns),1]))
        self.normalize_features()
    
    def normalize_features(self):
        """
        Normalizes features for ease of training.
        """
        self.norm_max = np.max(self.X)
        self.X = self.X / (self.norm_max)
    
    def cost_function(self):
        """
        Calculates the loss or errors in the model.
        """
        m = np.size(self.y)

        j = (1/2*m) * ((self.X @ self.thetas) - self.y).T @ ((self.X @ self.thetas) - self.y)

        return j
    
    def gradient_descent(self, iterations: int = 1000, learning_rate = 0.05):
        """
        Learning algorithm that calculates the slope of the cost function and subtracts it into the current parameters.
        """
        m = np.size(self.y)

        self.cost_history = np.zeros([iterations, 1])

        for _ in range(0,iterations):
            gradient = (1/m) * (self.X.T @ ((self.X @ self.thetas) - self.y))

            self.cost_history[_] = self.cost_function()
            self.gradient_history.append(gradient)
            self.theta_history.append(self.thetas)

            self.thetas = self.thetas - (learning_rate * gradient)
    
    def predict(self, X, sample_thetas = None):
        """
        Predictor based on the X values.
        """
        if sample_thetas is None:
            return (X/self.norm_max) @ self.thetas
        else:
            return (X/self.norm_max) @ sample_thetas
    
    def mape(self, y_true, y_pred):
        """
        Mean absolute percent error that calculates the average error in the model.
        
        y_true, y_pred = np.array(y_true), np.array(y_pred)
        return np.mean(np.abs((y_true - y_pred) / y_true))
        """

        return mean_absolute_percentage_error(y_true, y_pred) * 100
    
    def r_squared(self, y_true, y_pred):
        """
        Calculates the r-squared value accuracy of the linear regression model.
        """
        corr = np.corrcoef(y_true.tolist(), y_pred[0].tolist())
        return corr[0,1] ** 2