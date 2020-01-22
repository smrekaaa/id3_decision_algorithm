import sys
import anytree as tree
import calculations_id3 as cid3
import Attribute as att
import Tree as tree
import numpy as np
import pandas as pd


class ID3:

    def __init__(self, name, data, header, T, mt):
        self.name = name            # Dataset name
        self.learn_data = data      # Dataset [dataframe] for learning
        self.learn_header = header  # List of column names/attributes of learn_data
        self.learn_classes = []     # End classes of learn_data
        self.dic_classes = {}       # Dictionary of classes and their counts
        self.ES = 0                 # Entropy of the whole dataset
        self.metric_type = mt       # Metric for tree building (entropy, info. gain)
        self.T = T                  # Total number of rows
        self.root = None            # Root node of decision tree

        # For testing
        self.test_data = None      # Dataset [dataframe] for testing
        self.test_header = []      # List of column names/attributes of learn_data
        self.test_classes = []     # End classes of test_data
        self.class_indexes = {}    # Dictionary of classes and their matrix indexes
        self.confusion_mtr = []    # Confusion matrix

        # Setting some initial values
        self.learn_classes = self.set_classes(self.learn_data, self.learn_header)
        self.dic_classes = self.set_dic_classes(self.learn_data, self.learn_header)

        self.ES = cid3.entropy(self.dic_classes, T)
        print("Entropy: " + str(self.ES))
        #self.create_tree(self.classes, self.data, self.root)
        self.tree_create(self.learn_data, self.root)

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

    # CREATE TREE ------------------------------------------------------------------------------------------------------
    def get_gain_att(self, attributes):
        """
        Returns the attribute with wanted information gain based on metric type
        :param attributes: list of attributes
        :return: attribute
        """
        if not attributes:
            return None

        wanted_attribute = attributes[0]
        for a in attributes:
            if self.metric_type == 'entropy':
                if a.GA < wanted_attribute.GA:
                    wanted_attribute = a
            else:
                if a.GA > wanted_attribute.GA:
                    wanted_attribute = a

        return wanted_attribute

    def check_purity(self, data):

        class_column = self.learn_header[-1]
        unique = data[class_column].unique()

        if len(unique) <= 1:
            return True
        return False

    def tree_create(self, dataset, parent):
        """
        RECURSION
        Creates a decision tree
        :param dataset: Current dataset to ----
        :param parent: parent node if exists
        """

        if self.check_purity(dataset) or len(dataset.index) < 2:
            return

        # Check if is a leaf, is classified
        if parent:
            for c in self.learn_classes:
                if c == parent.name:
                    return

        new_header = list(dataset.columns.values.tolist())  # Current dataset header
        # print("New Header: " + str(new_header))
        attributes = []     # List of attributes objects and their values for current dataset

        # For each attribute
        for i in range(len(new_header)-1):

            # Create new attribute object
            new_att = att.Attribute(new_header[i], dataset, self.learn_classes, self.T, self.ES)

            # Add new attribute to the list
            attributes.append(new_att)

        """ print("Gains: ")
        for a in attributes:
            print("Name: " + str(a.name) + ", gain: " + str(a.GA))
        print()"""

        # Get the attribute with min/max gain
        # print("Wanted attribute")
        winner_attribute = self.get_gain_att(attributes)
        # winner_attribute.print_out()

        ## GROUP dataset based on winner attribute
        # Group current dataset by winner attribute
        grouped = dataset.groupby([winner_attribute.name])  # Dictionary of grouped datasets

        ## Nastavi nov node
        # Check if parent exists

        node = parent
        if not node:
            # create root node
            node = tree.MyNode(name=winner_attribute.name)
            self.root = node
        else:
            # append nodes to the parent
            node.name = winner_attribute.name

        ## Iterate over attribte values if it has any
        values_len = len(winner_attribute.sub_values)
        if values_len > 0:
            for value in winner_attribute.sub_values:

                new_child = tree.MyNode(value=value.name, parent=node)
                if value.ESA == 0:
                    new_child.name = value.get_classification()
                    continue        # Jump on net value, cause it does not need to split anymore
                if value.ESA == 1:
                    new_child.parent = None
                    continue
                # print("new child: " + str(new_child.name) + ", value: " + str(new_child.value))

                # remove column of winner attribute
                sub_dataset = grouped.get_group(value.name)
                del sub_dataset[winner_attribute.name]
                # print(sub_dataset)

                self.tree_create(sub_dataset, new_child)

        # self.root.print_out()

    # TEST TREE --------------------------------------------------------------------------------------------------------
    def set_class_indexes(self):
        """
        Sets the dictionary of classes' indexes
        """
        i = 0
        for c in self.learn_classes:
            self.class_indexes[c] = i
            i += 1

        # print("CLASS INDEXES:\n" + str(self.class_indexes))

    def check_classes(self, data, header):
        """
        Check whether classes are the same in both file.
        :param data: test dataset
        :param header: test dataset header
        :param n_rows: test dataset total number of rows
        """
        test_classes = self.set_classes(data, header)

        if test_classes.sort() != self.learn_classes.sort():
            print("Razredi datotek se ne ujemajo")
            sys.exit(1)

        self.test_data = data
        self.test_header = header
        self.test_classes = test_classes

        self.set_class_indexes()
        return True

    # MATRIKA ----------------------------------------------------------------------------------------------------------
    def set_confusion_mtr(self):
        """
        Sets confusion matrix
        """
        n = len(self.learn_classes)
        self.confusion_mtr = np.zeros((n, n))

    def print_confusion_mtr(self):
        """
        Prints out the confusion matrix as a data frame
        """
        # Create data frame from 2d array
        print("Confusion Matrix:")
        df = pd.DataFrame(data=self.confusion_mtr, index=self.learn_classes, columns=self.test_classes)
        print(df)

    def get_decision_class(self, node, row):
        """
        Recursivly gets the class of th row from test dataset.
        :param node: current node
        :param row: row from dataset
        :return: class
        """

        # Checks if node is leaf, if so recursion ends
        if node.is_leaf:
            return node.name

        node_att = node.name        # Attribute name of the node
        val = row[node_att]         # Value of the attribute in the row

        # Iterating over node's children to continue on matchin branch
        for c in node.children:
            if c.value == val:
                return self.get_decision_class(c, row)

        # If there was no match, select the first one
        # Not really the correct way to overgo over-fitting data or something like that
        return self.get_decision_class(node.children[0], row)

    def calculate_confusion_mtrx(self):
        """
        Calculates the confusion matrix
        """

        # Create a nxn zero matrix, n=number of classes
        self.set_confusion_mtr()

        # For every row in test_data go through decision tree and update confusion mtr
        for index, row in self.test_data.iterrows():

            row_dec_class = self.get_decision_class(self.root, row)     # Class got from our decision tree
            row_class = row[-1]                                         # Definied class

            # Update the matrix
            self.confusion_mtr[self.class_indexes[row_dec_class]][self.class_indexes[row_class]] += 1

    def calculate_metrics(self):
        """
        Calculates and prints wanted metrics
        """

        accuracy = cid3.accuracy(self.confusion_mtr)

        precisions = cid3.precisions(self.confusion_mtr)
        prec = cid3.precision(precisions)

        recalls = cid3.precisions(self.confusion_mtr)
        rec = cid3.recall(recalls)

        f_scores = cid3.class_f_scores(self.confusion_mtr, recalls, precisions)
        fscore = cid3.f_score(self.confusion_mtr, f_scores)

        print("Metrics:" +
              "\nAccuracy: " + str(accuracy) +
              "\nF-score: " + str(fscore) +
              "\nRecall: " + str(rec) +
              "\nPrecision: " + str(prec)
              )

    # PRINT OUT --------------------------------------------------------------------------------------------------------
    def print_out(self):
        """
        Prints out the objet data
        """
        print("Name: " + self.name +
                "\n - header: " + str(self.learn_header) +
                "\n - classes: " + str(self.learn_classes) +
                "\n - dic_classes: " + str(self.dic_classes) +
                "\n - T: " + str(self.T) +
                "\n - ES: " + str(self.ES) +
                "\n - root: " + str(self.root) +
                "\n"
              )



