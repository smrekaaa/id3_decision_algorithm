import calculations_id3 as cid3


class SubAttribute:

    def __init__(self, name, data, classes):
        self.name = name              # Name of the sub attribute
        self.sub_data = data          # Sub dataset of attribute
        self.header = \
            self.sub_data.columns     # Head of the sub dataset (2)
        self.classes = classes        # Classes of main dataset
        self.class_counts = {}        # Dictionary of class occurances for this sub att.
        self.ESA = 0                   # Entropy of the attribute value
        self.TSA = len(data.index)    # Total number of sub attribute occurrance

        # Set values
        self.set_class_counts()
        self.ESA = cid3.entropy(self.class_counts, self.TSA)

    def set_class_counts(self):
        """
        Sets dictionary of classes counts
        """
        counts = self.sub_data[self.header[-1]].value_counts()  # List of counts
        counts_indexes = counts.index                           # List of counted values

        # Sets dictionary key and their values to 0
        # Otherwise there wouldn't be all the classes
        self.class_counts = {c: 0 for c in self.classes}

        # Add values and their counts to the dictionary
        for i in range(len(counts)):
            self.class_counts[counts_indexes[i]] = counts[i]

    def get_classification(self):
        """
        Return non zero class. Used for leaf nodes.
        :return: class name
        """
        for c, count in self.class_counts.items():
            if count != 0:
                return c

    # PRINT OUT --------------------------------------------------------------------------------------------------------
    def print_out(self):
        """
        Prints out the objet data
        """
        print(  "SUB ATTRIBUTE:" +
                "\n - Name: " + str(self.name) +
                "\n - classes: " + str(self.classes) +
                "\n - class_counts: " + str(self.class_counts) +
                "\n - ESA: " + str(self.ESA) +
                "\n - TSA: " + str(self.TSA) +
                "\n"
              )

