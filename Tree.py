from anytree import RenderTree, NodeMixin
# https://anytree.readthedocs.io/en/latest/


class MyNode(NodeMixin):
    """
    Custom class for nodes of a decision tree
    """
    def __init__(self, name=None, value=None, parent=None, children=None):
        super(MyNode, self).__init__()
        self.name = name                       # Name of the attribute or a class(if leaf)
        self.value = value                     # If root: None, else: one of attribute's value
        self.parent = parent                   # Parent node, if root: None
        if children:                           # Children nodes, if leaf/attribute.value[x].EV == 0: None
            self.children = children

    # DEF -> CREATE CHILDREN
    def print_out(self):

        for pre, _, node in RenderTree(self):
            treestr = u"%s%s" % (pre, node.name)
            print(treestr.ljust(8), node.value)
