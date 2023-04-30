class Node(object):
    """Docstring for Node"""

    def __init__(
            self,
            name,
            position,
            state='empty',
            cost=0,
            heuristic=1, # Tri thức
            children={},
            path=[]
    ):
        self.name = name
        self.position = position
        self.state = state
        self.cost = cost
        self.heuristic = heuristic
        self.children = children
        self.path = path

    @staticmethod
    def copy_from(self, node, cost, path):
        return Node(node.name, node.position, node.state, cost, node.heuristic, node.children, path)