from ball import white, black


def get_opposite_marble(marble):
    """Return the opponent's marble."""
    if marble.is_empty:
        ValueError("Empty marble passed to get_opposite_marble")

    if marble == black:
        return white
    elif marble == white:
        return black
    else:
        ValueError("Unknown marble passed to get_opposite_marble")

def get_direction(start_row, start_col, end_row, end_col):
    """Return a tuple of direction, distance between start and end."""

    # Direction:
    #  NE = 1, E = 2, SE = 3
    #  SW = 4, W = 5, NW = 6

    if start_row == end_row:
        # An east <-> west move
        distance = abs(start_col - end_col)
        if start_col > end_col:
            direction = 2
        else:
            direction = 5
    elif start_col == end_col:
        # A north-west <-> south-east move
        distance = abs(start_row - end_row)
        if start_row > end_row:
            direction = 3
        else:
            direction = 6
    elif abs(start_col - end_col) == abs(start_row - end_row):
        # A north-east <-> south-west move
        distance = abs(start_col - end_col)
        if start_col > end_col:
            direction = 1
        else:
            direction = 4
    else:
        raise ValueError("Start and end position not in a straight line for get_direction")

    return direction, distance


def parse_position(pos):
    """Take a position description (e.g. H6) and return a tuple of row number, col number."""

    if len(pos) != 2:
        ValueError("Unknown position")

    row_name, col = pos[0], int(pos[1])-1
    row = ord(row_name.upper()) - ord('A')
    if col < 5:
        if row > (col + 4):
            ValueError("Unknown position")
    else:
        if row < (col - 4):
            ValueError("Unknown position")

    return row, col

def calc_position_at_distance(start_row, start_col, direction, hops):
    """For a given starting row & col (e.g. (1, 3)), a direction, and a number of "hops," return a tuple of row number,
        col number of the end position.

        Direction:
          NE = 1, E = 2, SE = 3
          SW = 4, W = 5, NW = 6
        """

    if not 0 < direction < 7:
        return ValueError("Unknown direction")

    r, c = start_row, start_col

    # East directions increase the column number, except for SE
    if direction in (1, 2):
        c += hops
    # West directions decrease the column number, except for NW
    if direction in (4, 5):
        c -= hops
    # North directions decrease the row number
    if direction in (1, 6):
        r -= hops
    # South directions increase the row number
    if direction in (3, 4):
        r += hops

    return r, c