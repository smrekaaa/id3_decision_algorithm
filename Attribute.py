import calculations_id3 as cid3
import sub_attribute as sa


class Attribute:

    def __init__(self, name, data, classes, T, ES, root=None):
        self.name = name            # Name of the attribute
        self.sub_data = data        # Sub dataset
        self.classes = classes      # Classes of main dataset
        self.values = []            # List of distinct values names
        self.sub_values = []        # List of all values' objects
        self.groups = {}            # Dictionary of grouped data by this attribut
        self.IA = 0                 # Average information entropy of the attribute
        self.GA = 0                 # Information gain of the attribute
        self.ES = ES                # Main dataset entropy
        self.T = T                  # Total number of rows
        self.root = root            # Root node of the decision tree
        self.node = None            # Node of the attribute when known

        # Setting some initial values
        self.set_values()
        self.set_groups()
        self.set_avg_info_entropy()
        self.set_gain()

    def set_values(self):
        """
        Sets the list of unique values for the attribute
        """
        self.values = self.sub_data[self.name].unique()

    def set_groups(self):
        """
        Sets the groups by the distinct attribute value.
        And createc new objects of sub attributes.
        """
        self.groups = self.sub_data.groupby([self.name])            # List of grouped data by this attribute

        # For every distinct value, create new sub attribute object
        for i in range(len(self.values)):
            data = self.groups.get_group((self.values[i]))         # Sub data set for the value

            # New object
            new_sub_att = sa.SubAttribute(self.values[i], data, self.classes)

            # Add new sub attribute to the list
            self.sub_values.append(new_sub_att)

    def set_avg_info_entropy(self):
        """
        Calculates average information gain for the attribute
        """
        avg_info_ent = 0

        for v in self.sub_values:
            avg_info_ent += ((v.TSA/self.T) * v.ESA)

        self.IA = avg_info_ent

    def set_gain(self):
        """
        Calculates and sets the attribute gain
        :return:
        """

        self.GA = self.ES - self.IA

    # PRINT OUT --------------------------------------------------------------------------------------------------------
    def print_out(self):
        """
        Prints out the objet data
        """
        print(  "ATTRIBUTE:" +
                "\n -Name: " + self.name +
                "\n - values: " + str(self.values) +
                "\n - classes: " + str(self.classes) +
                "\n - grouped_dic: " + str(self.groups.groups) +
                "\n - T: " + str(self.T) +
                "\n - IA: " + str(self.IA) +
                "\n - GA: " + str(self.GA) +
                "\n - root: " + str(self.root) +
                "\n"
              )

