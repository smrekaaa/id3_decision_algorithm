import calculations_id3 as cid3
import Attribute as att

class ID3:

    def __init__(self, name, data, T, mt):
        self.name = name            # Dataset name
        self.data = data            # Dataset [dataframe]
        self.header = data.columns  # Header of dataset = ATTRIBUTES names
        self.classes = []           # End classes
        self.dic_classes = {}       # Dictionary of classes and number of their occurrances
        self.ES = 0                 # Entropy of the whole data set
        self.metric_type = mt       # Metric for tree building (entropy, info. gain)
        self.T = T                  # Total number of rows
        self.root = None            # Root node of decision tree

        # Setting some initial values
        self.set_classes()
        self.set_dic_classes()

        self.ES = cid3.entropy(self.dic_classes, T)
        print("Entropy: " + str(self.ES))
        self.create_tree()

    def set_classes(self):
        """
        Sets the classes for classification.
        In my cases, clases are found in LAST column
        """

        class_column = self.header[-1]                       # Get the last column name -> classification column
        self.classes = self.data[class_column].unique()      # Gets and sets distinct values of the last column

    def set_dic_classes(self):
        """
        Sets dictionary of classes and the number of their apperance in the dataset
        """
        class_column = self.header[-1]                      # Last column in data set = column of classification
        counts = self.data[class_column].value_counts()     # List of counts of every distinct value in the column
        counts_indexes = counts.index                       # List of distinct values
        # print(counts)
        # print(counts.index)

        # Add attributes and their counts to the dictionary
        for i in range(len(counts)):
            self.dic_classes[counts_indexes[i]] = counts[i]

        #print("DIC_CLASSES:\n" + str(self.dic_classes))

    #TREE ---------------------------------------------------------------------------------------
    def get_gain_att(self, atts):
        """
        Returns the attribute with wanted information gain based on metric type
        :param atts: list of attributes
        :return: attribute
        """
        wanted_attribute = atts[0]
        for a in atts:
            if self.metric_type == 'entropy':
                if a.GA < wanted_attribute.GA:
                    wanted_attribute = a
            else:
                if a.GA > wanted_attribute.GA:
                    wanted_attribute = a

        return wanted_attribute

    def create_tree(self, data=None):
        """
        Creates the tree
        :param data:
        :return:
        """
        attributes = []  # List of all attributes

        # For every column/attribute, except last/class. one
        for i in range(len(self.header)-1):

            # Get sub datasets of only 2 columns(current attribte, class)
            sub_dataset = self.data[[self.header[i], self.header[-1]]]
            # print(sub_dataset)

            # Create new attribute
            new_att = att.Attribute(self.header[i], sub_dataset, self.classes, self.T, self.ES)

            # Add new attribute to the list
            attributes.append(new_att)

        # Get attribute for root/node
        print("Wanted attribute")
        wanted_att = self.get_gain_att(attributes)
        wanted_att.print_out()






    # PRINT OUT --------------------------------------------------------------------------------------------------------
    def print_out(self):
        """
        Prints out the objet data
        """
        print("Name: " + self.name +
                "\n - header: " + str(self.header) +
                "\n - classes: " + str(self.classes) +
                "\n - dic_classes: " + str(self.dic_classes) +
                "\n - T: " + str(self.T) +
                "\n - ES: " + str(self.ES) +
                "\n - root: " + str(self.root) +
                "\n"
              )



