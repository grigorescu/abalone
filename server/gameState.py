from ball import white, black, empty
import utils


class GameState:
    """Stores the state of the game at any given time."""

    def __init__(self):
        """Start a new game."""
        self.board = [
            [black, black, black, black, black],
            [black, black, black, black, black, black],
            [empty, empty, black, black, black, empty, empty],
            [empty, empty, empty, empty, empty, empty, empty, empty],
            [empty, empty, empty, empty, empty, empty, empty, empty, empty],
            [empty, empty, empty, empty, empty, empty, empty, empty],
            [empty, empty, white, white, white, empty, empty],
            [white, white, white, white, white, white],
            [white, white, white, white, white]
        ]
        self.turn = black
        self.black_marbles_removed = 0
        self.white_marbles_removed = 0

    def proc_move(self, move, preview=False):
        """Process a move. If preview == True, it won't actually store the move, just return the board state that would
        result.

        Move notation:
           In-line move:
              Start and end position of the "pushing" marble. e.g. I5-H5
           Broad-side move:
              Start positions of the two extremities of the row followed by the end position of the first one. e.g.
              I5-I7-H4
        """
        black_count = self.black_marbles_removed
        white_count = self.white_marbles_removed

        if black_count >= 6:
            raise ValueError("The game is over - white has won")
        if white_count >= 6:
            raise ValueError("The game is over - black has won")

        if move.count("-") == 1:
            result, marble_removed = self._proc_inline_move(move)
            if marble_removed and self.turn == white:
                black_count += 1
            if marble_removed and self.turn == black:
                white_count += 1
        elif move.count("-") == 2:
            result = self._proc_broadside_move(move)
        else:
            raise ValueError("Unknown move notation")

        if preview:
            return result, black_count, white_count

        self.turn = utils.get_opposite_marble(self.turn)
        self.black_marbles_removed = black_count
        self.white_marbles_removed = white_count
        self.board = result

        return result

    def _proc_inline_move(self, move):
        """Process an inline move, e.g. I5-H5.

        Returns a tuple of: the new board position, T if a black marble was removed, T if a white marble was removed"""

        #########
        # Check 1 - Are we moving a distance of 1?
        start, end = move.split('-')

        start_row, start_col = utils.parse_position(start)
        end_row, end_col = utils.parse_position(end)

        direction, distance = utils.get_direction(start_row, start_col, end_row, end_col)
        if distance != 1:
            raise ValueError("Invalid move")

        marble = self.turn

        #########
        # Check 2 - Is there a matching marble in the starting position?
        try:
            if self._get_marble(start_row, start_col) != marble:
                raise ValueError("Invalid move")
        #######
        # Check 3 - If we're here, the starting position is not on the board.
        except IndexError:
            raise ValueError("Invalid move")

        #########
        # Check 4 - The end position can't have a marble of the opposite color.
        try:
            if self._get_marble(end_row, end_col) == utils.get_opposite_marble(marble):
                raise ValueError("Invalid move")
        #######
        # Check 5 - If we're here, the end position is not on the board.
        except IndexError:
            raise ValueError("Invalid move")

        # For documentation, we'll assume our marble is white

        if self._get_marble(start_row, start_col, direction, 1) == empty:
            # We're pushing one white into an empty space - Legal move
            board = self._set_marble(start_row, start_col, empty)
            r, c = utils.calc_position_at_distance(start_row, start_col, direction, 1)
            board = self._set_marble(r, c, marble, board)
            return board, False
        elif self._get_marble(start_row, start_col, direction, 1) == utils.get_opposite_marble(marble):
            # One white against one black. Can't do this, but is this a pac or just an invalid move?
            if self._get_marble(start_row, start_col, direction, 2) == empty:
                # We're pushing one white against one black, followed by an empty space
                raise ValueError("Pac")
            else:
                # We're pushing one white against one black and some other stuff
                raise ValueError("Invalid move")
        else:
            # Two white marbles in a row.
            if self._get_marble(start_row, start_col, direction, 2) == empty:
                # We're pushing two whites into an empty space - Legal move
                board = self._set_marble(start_row, start_col, empty)
                r, c = utils.calc_position_at_distance(start_row, start_col, direction, 2)
                board = self._set_marble(r, c, marble, board)
                return board, False
            elif self._get_marble(start_row, start_col, direction, 2) == utils.get_opposite_marble(marble):
                # Two whites against one black. What's in the next space?
                if self._get_marble(start_row, start_col, direction, 3, True) == empty:
                    # Two whites pushing one black into an empty space - Legal move
                    board = self._set_marble(start_row, start_col, empty)
                    r, c = utils.calc_position_at_distance(start_row, start_col, direction, 2)
                    board = self._set_marble(r, c, marble, board)
                    try:
                        r, c = utils.calc_position_at_distance(start_row, start_col, direction, 3)
                        board = self._set_marble(r, c, utils.get_opposite_marble(marble), board)
                    except IndexError:
                        # We just pushed a black off the edge
                        return board, True
                    return board, False
                elif self._get_marble(start_row, start_col, direction, 3) == utils.get_opposite_marble(marble):
                    # Two whites against two blacks. Can't do this, but is this a pac or just an invalid move?
                    if self._get_marble(start_row, start_col, direction, 4) == empty:
                        # We're pushing two whites against two blacks followed by an empty space
                        raise ValueError("Pac")
                    else:
                        # We're pushing two whites against two blacks and some other stuff
                        raise ValueError("Invalid move")
                else:
                    # Two whites, one black, one white
                    raise ValueError("Invalid move")
            else:
                # Three white marbles in a row.
                if self._get_marble(start_row, start_col, direction, 3) == empty:
                    # We're pushing three whites into an empty space - Legal move
                    board = self._set_marble(start_row, start_col, empty)
                    r, c = utils.calc_position_at_distance(start_row, start_col, direction, 3)
                    board = self._set_marble(r, c, marble, board)
                    return board, False
                elif self._get_marble(start_row, start_col, direction, 3) == utils.get_opposite_marble(marble):
                    # Three whites against one black. What's in the next space?
                    if self._get_marble(start_row, start_col, direction, 4, True) == empty:
                        # Three whites pushing one black into an empty space - Legal move
                        board = self._set_marble(start_row, start_col, empty)
                        r, c = utils.calc_position_at_distance(start_row, start_col, direction, 3)
                        board = self._set_marble(r, c, marble, board)
                        try:
                            r, c = utils.calc_position_at_distance(start_row, start_col, direction, 4)
                            board = self._set_marble(r, c, utils.get_opposite_marble(marble), board)
                        except IndexError:
                            # We just pushed a black off the edge
                            return board, True
                        return board, False
                    elif self._get_marble(start_row, start_col, direction, 4) == utils.get_opposite_marble(marble):
                        # Three whites against two blacks. What's in the next space?
                        if self._get_marble(start_row, start_col, direction, 5, True) == empty:
                            # Three whites pushing two blacks into an empty space - Legal move
                            board = self._set_marble(start_row, start_col, empty)
                            r, c = utils.calc_position_at_distance(start_row, start_col, direction, 3)
                            board = self._set_marble(r, c, marble, board)
                            try:
                                r, c = utils.calc_position_at_distance(start_row, start_col, direction, 5)
                                board = self._set_marble(r, c, utils.get_opposite_marble(marble), board)
                            except IndexError:
                                # We just pushed a black off the edge
                                return board, True
                            return board, False
                        elif self._get_marble(start_row, start_col, direction, 5) == utils.get_opposite_marble(marble):
                            # Three whites against three blacks. Can't do this, but is this a pac or just an invalid move?
                            if self._get_marble(start_row, start_col, direction, 6) == empty:
                                # We're pushing three whites against three blacks followed by an empty space
                                raise ValueError("Pac")
                            else:
                                # We're pushing three whites against three blacks and some other stuff
                                raise ValueError("Invalid move")
                        else:
                            # Three whites, two blacks, white
                            raise ValueError("Invalid move")
                    else:
                        # Three whites, one black, white
                        raise ValueError("Invalid move")
                else:
                    # Four whites
                    raise ValueError("Invalid move")

    def _proc_broadside_move(self, move):
        """Process an broadside move, e.g. I5-I7-H5"""

        line_start, line_end, end = move.split('-')

        line_start_row, line_start_col = utils.parse_position(line_start)
        line_end_row, line_end_col = utils.parse_position(line_end)
        end_row, end_col = utils.parse_position(end)

        #########
        # Check 1 - Is the line actually a line and <= 3 in length?
        line_direction, line_distance = utils.get_direction(line_start_row, line_start_col, line_end_row, line_end_col)
        if line_distance > 3:
            raise ValueError("Invalid move")
        if line_distance == 3:
            # Direction:
            #  NE = 1, E = 2, SE = 3
            #  SW = 4, W = 5, NW = 6

            # Col changes in all cases except for SE and NW
            if line_direction not in (3, 6):
                line_mid_col = max(line_start_col, line_end_col) - 1
            # Row changes in all cases except for E and W
                line_mid_row = max(line_start_row, line_end_row) - 1

        if line_distance == 1:
            # This is the same as an inline push of 1 marble
            return self._proc_inline_move(move[3:8])

        marble = self.turn

        #########
        # Check 2 - Is there a matching marble in the line start position?
        try:
            if self._get_marble(line_start_row, line_start_col) != marble:
                raise ValueError("Invalid move")
        #######
        # Check 3 - If we're here, the line start position is not on the board.
        except IndexError:
            raise ValueError("Invalid move")

        #########
        # Check 4 - Is there a matching marble in the line end position?
        try:
            if self._get_marble(line_end_row, line_end_col) != marble:
                raise ValueError("Invalid move")
        #######
        # Check 5 - If we're here, the line end position is not on the board.
        except IndexError:
            raise ValueError("Invalid move")

        #########
        # Check 6 - If the line is of length 3, is there a matching marble in the middle position?
        try:
            if line_distance == 3 and self._get_marble(line_mid_row, line_mid_col) != marble:
                raise ValueError("Invalid move")
        #######
        # Check 7 - If we're here, the middle position is not on the board... defying the laws of physics, somehow
        except IndexError:
            raise ValueError("Invalid move")

        move_direction, move_distance = utils.get_direction(line_start_row, line_start_col, end_row, end_col)
        if move_distance != 1:
            raise ValueError("Invalid move")

        ######
        # Check 8 - Is the end position of the first marble empty?
        try:
            if self._get_marble(end_row, end_col) != empty:
                raise ValueError("Invalid move")
        ######
        # Check 9 - If we're here, the end position of the first marble is not on the board.
        except IndexError:
            raise ValueError("Invalid move")

        ######
        # Check 10 - Is the end position of the last marble empty?
        try:
            if self._get_marble(line_end_row, line_end_col, move_direction, 1) != empty:
                raise ValueError("Invalid move")
        ######
        # Check 11 - If we're here, the end position of the last marble is not on the board.
        except IndexError:
            raise ValueError("Invalid move")

        if line_distance == 3:
            ######
            # Check 14 - Is the end position of the middle marble empty?
            try:
                if self._get_marble(line_mid_row, line_mid_col, move_direction, 1) != empty:
                    raise ValueError("Invalid move")
            ######
            # Check 15 - If we're here, the end position of the middle marble is not on the board - somehow.
            except IndexError:
                raise ValueError("Invalid move")

        board = self._set_marble(line_start_row, line_start_col, empty)
        board = self._set_marble(end_row, end_col, marble, board)

        board = self._set_marble(line_end_row, line_end_col, empty, board)
        r, c = utils.calc_position_at_distance(line_end_row, line_end_col, move_direction, 1)
        board = self._set_marble(r, c, marble, board)

        if line_distance == 3:
            board = self._set_marble(line_mid_row, line_mid_col, empty, board)
            r, c = utils.calc_position_at_distance(line_mid_row, line_mid_col, move_direction, 1)
            board = self._set_marble(r, c, marble, board)

        return board

    def _get_marble(self, row, col, direction=0, hops=0, edge_is_empty=False):
        """For a given starting row & col (e.g. (1, 3)), a direction, and a number of "hops," return the marble in that
         position.

         If edge_is_empty=True, treat positions off the board as empty (this is useful for pushing when you
         don't care if you're pushing off the board or not)."""

        try:
            r, c = utils.calc_position_at_distance(row, col, direction, hops)
        except IndexError, e:
            if edge_is_empty:
                return empty
            else:
                raise IndexError(e)

        if r < 4:
            return self.board[r][c]
        return self.board[r][c-(r-4)]

    def _set_marble(self, row, col, marble, board=None):
        """Set the marble at (row, col)."""

        if not board:
            board = list(self.board)

        if row < 4:
            board[row][col] = marble
            return board

        board[row][col-(row-4)] = marble
        return board
