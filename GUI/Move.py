
class Move:
    def __init__(self, initial, final):
        """
        Initial and final are squares
        :param initial: start Square instance - don't need piece (=None)
        :param final: end Square instance - don't need piece (=None)
        """
        self.initial = initial
        self.final = final

    def __str__(self):
        """
        :return: String before position and now position
        """
        s = ''
        s += f'({self.initial.col}, {self.initial.row})'
        s += f' -> ({self.final.col}, {self.final.row})'
        return s

    def __eq__(self, other):
        """
        Compare when use ==
        :param other: other instance of Class Move
        :return: Boolean
        """
        return self.initial == other.initial and self.final == other.final
