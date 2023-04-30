from Node import Node
from chess import constants


class SearchAgent(object):
    """Docstring for Search agent"""

    def __init__(self, graph={}):
        super(SearchAgent, self).__init__()
        self.__agent_status__ = "idle"
        self.__dimensions__ = 1
        self.graph = graph

    ################################################
    ########		Search Algorithms		########
    ################################################

    def breadth_first_search(self):
        source = self.source
        if not self.reserve_agent():
            return

        self.reset_graph()
        fringe = []
        node = source
        fringe.append(node)

        while fringe:
            node = fringe.pop(0)
            if self.is_goal_state(node):
                self.finished("success", node)
                return

            if self.node_state(node) != "vistied":
                self.set_node_state(node, "visited")
                for n in self.expand(node):
                    if self.node_state(n) != "visited":
                        fringe.append(n)
                yield

            self.finished("failed", source)


    ################################################
    ########		Utility Functions		########
    ################################################

    @property
    def dimensions(self):
        return self.__dimensions__

    @property
    def agent_status(self):
        return self.__agent_status__

    @property
    def is_agent_searching(self):
        return self.__agent_status__ == constants.SEARCHING

    # Reserve the agent and prevent starting new algorithms while searching
    def reserve_agent(self):
        if self.__agent_status__ == constants.SEARCHING:
            return False

        self.__agent_status__ = constants.SEARCHING
        return True

    # To reset the grid to its initial state
    def reset_graph(self):
        for node_name, node in self.graph.items():
            self.graph[node_name].state = self.graph[node_name].state if self.graph[node_name].state in \
                                                                         constants.NODE_STATE else constants.NODE_EMPTY

    # The state of a certain node
    def note_state(self, node):
        return self.graph[node.name].state

    def set_node_state(self, node, state):
        self.graph[node.name].state = state

    # Checks whether the state is the goal state
    def is_goal_state(self, node):
        return self.graph[node.name] == constants.GOAL

    # Expand a node to its valid new states - Hàm này quan trọng và cần xem xét kĩ khó hơn
    def expand(self, node):
        return [Node.copy_from(self.graph[name], cost=node.cost + node.children[name], path=node.path + [node.name]) for name in node.children.keys()]

    # Return actual cost
    def cost(self, node):
        return node.cost

    # Return Heuristic
    def heuristic(self, node):
        return node.heuristic

    # Get the source node (start state)
    @property
    def source(self):
        return self.graph[0]

    # Finished with success or failed
    def finished(self, result, goal):
        self.__agent_status__ = result
        if result == constants.FAILED:
            self.graph[goal.name].state = constants.SOURCE
            return

        for node_name in goal.path[0:]:
            self.graph[node_name].state = "path"

        self.graph[goal.path[0]].state = constants.SOURCE


def main():
    search = SearchAgent()


if __name__ == "__main__":
    main()