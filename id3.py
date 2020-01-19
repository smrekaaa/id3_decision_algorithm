import calculations_id3 as cid3
import Attribute as att
import Tree as tree

class ID3:

    def __init__(self, name, data, header, T, mt):
        self.name = name            # Dataset name
        self.data = data            # Dataset [dataframe]
        self.header = header        # List of column names/attributes
        self.classes = []           # End classes
        self.dic_classes = {}       # Dictionary of classes and their counts
        self.ES = 0                 # Entropy of the whole dataset
        self.metric_type = mt       # Metric for tree building (entropy, info. gain)
        self.T = T                  # Total number of rows
        self.root = None            # Root node of decision tree
        self.done_attributes = []   # Attributes which were already sorted out

        # Setting some initial values
        self.classes = self.set_classes(self.data, self.header)
        self.dic_classes = self.set_dic_classes(self.data, self.header)

        self.ES = cid3.entropy(self.dic_classes, T)
        print("Entropy: " + str(self.ES))
        #self.create_tree(self.classes, self.data, self.root)
        self.tree_create(self.data, self.root)

    @staticmethod
    def set_classes(data, head):
        """
        Sets the classes for classification.
        In my cases, clases are found in LAST column
        :return: List of unique values
        """

        class_column = head[-1]                 # Get the last column name -> classification column
        return data[class_column].unique()      # Gets and sets distinct values of the last column

    @staticmethod
    def set_dic_classes(data, head):
        """
        Sets dictionary of classes and the number of their apperance in the dataset
        :return: Dictionary of distinct values and their counts
        """

        class_column = head[-1]                             # Last column in data set = column of classification
        counts = data[class_column].value_counts()          # List of counts of every distinct value in the column
        counts_indexes = counts.index                       # List of distinct values

        dic = {}
        # Add attributes and their counts to the dictionary
        for i in range(len(counts)):
            dic[counts_indexes[i]] = counts[i]

        return dic

        #print("DIC_CLASSES:\n" + str(self.dic_classes))

    # TREE ---------------------------------------------------------------------------------------

    def create_tree(self, classes, dataset=None, parent=None):
        """
        Creates the tree
        :param data:
        """
        attributes = []                                         # List of all attributes
        head = dataset.columns                                  # header of the dataset
        classes_dic = self.set_dic_classes(dataset, head)       # Counts of the classes
        t_rows = len(dataset.index)                             # Total number of rows in the dataset
        E = cid3.entropy(classes_dic, t_rows)                   # Entropy of the dataset

        # For every column/attribute, except last/class. one
        for i in range(len(head)-1):

            # dataset head
            dataset_head = [head[i], head[-1]]
            if parent:
                dataset_head.append(parent.attribute.name)

            # Get sub dataset
            sub_dataset = dataset[dataset_head]
            # print(sub_dataset)

            # Create new attribute
            new_att = att.Attribute(head[i], sub_dataset, self.classes, self.T, self.ES)

            # Add new attribute to the list
            attributes.append(new_att)

        """OK
        print("Ganis: ")
        for a in attributes:
            print("Name: " + str(a.name) + ", gain: " + str(a.GA))
        print()"""

        # Get attribute for root/node
        print("Wanted attribute")
        wanted_att = self.get_gain_att(attributes)
        wanted_att.print_out()



    # TREE NEW -----------------------------------------------------------------------------------------------------
    def get_gain_att(self, attributes):
        """
        Returns the attribute with wanted information gain based on metric type
        :param attributes: list of attributes
        :return: attribute
        """
        wanted_attribute = attributes[0]
        for a in attributes:
            if self.metric_type == 'entropy':
                if a.GA < wanted_attribute.GA:
                    wanted_attribute = a
            else:
                if a.GA > wanted_attribute.GA:
                    wanted_attribute = a

        return wanted_attribute

    def is_attribute_done(self, att):
        """
        Checks whether attribute's been done.
        :param att: attribute's name
        :return: boolean
        """

        # Check if done_attributes are empty
        if not self.done_attributes:
            return False

        for a in self.done_attributes:
            if a == att:
                return True

        return False

    def tree_create(self, dataset, parent):
        """
        RECURSION
        Creates a decision tree
        :param dataset: Current dataset to ----
        :param parent: parent node if exists
        """

        # Check if all attributes are done
        if self.header.sort == self.done_attributes.sort:
            return

        new_header = list(dataset.columns.values.tolist())  # Current dataset header
        print("New Header: " + str(new_header))

        attributes = []     # List of attributes objects and their values for current dataset

        # For each attribute
        for i in range(len(new_header)-1):

            # Check if it was already done
            if self.is_attribute_done(new_header[i]):
                # Continue to next attribute
                continue
            else:
                # Create new attribute object
                new_att = att.Attribute(new_header[i], dataset, self.classes, self.T, self.ES)

                # Add new attribute to the list
                attributes.append(new_att)

        """OK
        print("Ganis: ")
        for a in attributes:
            print("Name: " + str(a.name) + ", gain: " + str(a.GA))
        print()"""
        # Get the attribute with min/max gain
        print("Wanted attribute")
        winner_attribute = self.get_gain_att(attributes)
        winner_attribute.print_out()

        # For every value/sub_attribute of winner attribute
        children_nodes = []
        for value in winner_attribute.sub_values:
            value.print_out()

            # Check if value/sub_attribute has only one solution, if ESA == 0
            if value.ESA == 0:
                new_child = tree.MyNode(value.get_classification(), value.name)
            else:
                new_child = tree.MyNode(None, value.name)

            children_nodes.append(new_child)

        # Add childeren nodes to the parent
        # Check if parent exists
        if not parent:
            # create root node
            self.root = tree.MyNode(winner_attribute.name, children=children_nodes)
        else:
            # append nodes to the parent
            parent.children = children_nodes

        self.root.print_out()






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



