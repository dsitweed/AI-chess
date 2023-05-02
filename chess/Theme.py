from Color import Color


class Theme:
    def __init__(self, light_background, dark_background,
                 light_trace, dark_trace,
                 light_moves, dark_moves):
        """

        :param light_background:
        :param dark_background:
        :param light_trace:
        :param dark_trace:
        :param light_moves:
        :param dark_moves:
        """
        self.background = Color(light_background, dark_background)
        self.trace = Color(light_trace, dark_trace)
        self.moves = Color(light_moves, dark_moves)
