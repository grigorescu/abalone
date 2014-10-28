class Ball:
    """A single Abalone ball."""

    def __init__(self, name, is_empty=False):
        self.name = name
        self.is_empty = is_empty

    def __repr__(self):
        return self.name


white = Ball("white")
black = Ball("black")
empty = Ball("empty", True)