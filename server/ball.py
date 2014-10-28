class Ball:
    """A single Abalone ball."""

    def __init__(self, name, is_empty=False):
        self.name = name
        self.is_empty = is_empty

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other.name


white = Ball("white")
black = Ball("black")
empty = Ball("empty", True)