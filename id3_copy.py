import calculations_id3 as cid3
import Attribute as att


class ID3:

    def __init__(self, name, data, T, mt):
        self.name = name  # Dataset name
        self.data = data  # Dataset [dataframe]
        self.header = data.columns  # Header of dataset = ATTRIBUTES names
        self.classes = []  # End classes
        self.dic_classes = {}  # Dictionary of classes and number of their occurrances
        self.ES = 0  # Entropy of the whole data set
        self.metric_type = mt  # Metric for tree building (entropy, info. gain)
        self.T = T  # Total number of rows
        self.root = None  # Root node of decision tree

        # Setting some initial values
        self.set_classes()
        self.dic_classes = self.set_dic_classes(self.data)

        self.ES = cid3.entropy(self.dic_classes, T)
        print("Entropy: " + str(self.ES))
        self.create_tree(self.data, self.root)
        self.tree_create(self.data, self.root)

    def set_classes(self):
        """
        Sets the classes for classification.
        In my cases, clases are found in LAST column
        """

        class_column = self.header[-1]  # Get the last column name -> classification column
        self.classes = self.data[class_column].unique()  # Gets and sets distinct values of the last column

    def set_dic_classes(self, dataset):
        """
        Sets dictionary of classes and the number of their apperance in the dataset
        """
        dic = {}
        class_column = dataset.columns[-1]  # Last column in data set = column of classification
        counts = dataset[class_column].value_counts()  # List of counts of every distinct value in the column
        counts_indexes = counts.index  # List of distinct values
        # print(counts)
        # print(counts.index)

        # Add attributes and their counts to the dictionary
        for i in range(len(counts)):
            dic[counts_indexes[i]] = counts[i]

        return dic
        # print("DIC_CLASSES:\n" + str(self.dic_classes))

    # TREE -------------------------------------------------------------------------------------------------------------
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

    def create_tree(self, dataset=None, parent=None):
        """
        Creates the tree
        :param data:
        """

        """
        1. Preveri ali obstaja parent:
            NE:
                1. Za vsak atribut pridobi GA (IA+ES)
                    1.1 Pridobi: header, classes, classes counts, T, ES, pod_attribute
                        header = classes + attribute
                2. Pridobi vse GA in uizberi ustreznega in/max
                3. Ustvari root -> root(att.name, att, value=None, children=None)
                4. Groupiraj dataset glede na izbran atribut
                5. Za vsak pod_atribut izbranega atributa:
                    5.1 Preveri ali ima atribut sub_att:
                    ustvari nov node in ga dodaj v parenta
                    node(sub_att.name, attribute=None, value=sub_att.name, parent=root)
                6. Za vsak atribut pridobi dataset in groups.
                    pojdi v novo rekurzijo
                    
        """
        attributes = []  # List of all attributes
        head = dataset.columns

        # For every column/attribute, except last/class. one
        for i in range(len(self.header) - 1):
            # Get sub datasets of only 2 columns(current attribte, class)
            sub_dataset = self.data[[self.header[i], self.header[-1]]]
            # print(sub_dataset)

            # Create new attribute
            new_att = att.Attribute(self.header[i], sub_dataset, self.classes, self.T, self.ES)

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

    # TREE NEW ---------------------------------------------------------------------------------------------------------
    def is_leaf(self, node):
        """
        Checks if node is a leaf => Check if node's value is sama as any class
        :param node: tree node
        :return:
        """
        if not node:
            return False

        for c in self.classes:
            if c == node.value:
                return True
        return False

    def tree_create(self, dataset, parent):

        print("TREE CREATE ----------------")
        # Check if node value is same as any class
        # If so, recursion stops.
        if self.is_leaf(parent):
            print("Check if leaf")
            return

        t_rows = len(dataset.index)                        # Total number of data rows
        head = dataset.columns
        classes_counts = self.set_dic_classes(dataset)

        print("Head: " + str(head))
        print("Classes_coounts:\n" + str(classes_counts))






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



