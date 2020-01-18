class Attribute:

    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.ES = 0     # Entropy of the data set S
        self.T = 0      # Total number of data rows
        self.P = 0      # Number of positive scenario
        self.N = 0      # Number of negative scenario
        self.root