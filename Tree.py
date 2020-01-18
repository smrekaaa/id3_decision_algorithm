from anytree import RenderTree, NodeMixin
# https://anytree.readthedocs.io/en/latest/

class MyNode(NodeMixin):
    """
    Custom class for nodes of a decision tree
    """
    def __init__(self, value, parent=None, children=None):
        super(MyNode, self).__init__()
        self.value = value
        self.parent = parent
        if children:
            self.children = children