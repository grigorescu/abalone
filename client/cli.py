from termcolor import colored

from server.ball import white, black
import server.gameState


def draw_ball(ball):
    if ball == white:
        return "O"
    elif ball == black:
        return "@"
    else:
        return "+"


def draw(board):
        """Converts the board state to ASCII art.

             I O O O O O
            H O O O O O O
           G + + O O O + +
          F + + + + + + + +
         E + + + + + + + + +
          D + + + + + + + + 9
           C + + @ @ @ + + 8
            B @ @ @ @ @ @ 7
             A @ @ @ @ @ 6
                1 2 3 4 5
                        """

        color = ["red", "green", "yellow", "blue", "magenta", "cyan", "white", "red", "green"]

        result = ""

        for row in range(8, -1, -1):
            offset = abs(row - 4)
            color_offset = offset
            if row <= 4: color_offset = 0

            space = " " * offset
            label = chr(ord('A') + row)

            result += space + label
            for col in range (0, 9-offset):
                space_color = color[col + color_offset]
                result += "  " + colored(draw_ball(board[row][col]), space_color)

            if row < 4: result += "  " + colored(str(row + 6), color[row + 5])
            result += "\n"
        result += "        " + colored("1", "red") + "  " + colored("2", "green") + "  " + colored("3", "yellow") + "  " + colored("4", "blue") + "  " + colored("5", "magenta")

        print result


moves = []

def get_move(g):
    try:
        move = raw_input("Enter move:")
    except KeyboardInterrupt, e:
        print "\n".join(moves)
        raise e
    print ""
    try:
        board, black_count, white_count = g.proc_move(move, True)
    except ValueError, e:
        print e
        return False, None, None, None, None
    return True, board, black_count, white_count, move

if __name__ == "__main__":
    g = server.gameState.GameState()
    black_count = white_count = 0
    start_moves = ["A4-B4", "I8-H7", "B4-C4", "I9-H8", "C3-D4", "I5-H4", "B3-C3", "H4-G3", "B2-C2", "G3-F3", "C3-B2",
                   "G6-F5", "B1-C2", "F3-E3", "D3-C2", "E3-D3", "B1-C2-C1", "D3-C3", "C1-B1", "H7-G6", "B2-A3-B3",
                   "G6-F5", "A5-A4", "F5-E4", "A1-B2", "C3-D3", "A4-B4", "E4-D3", "D2-E2", "D3-D2", "E5-D5", "I7-H6",
                   "B3-B2",
                   ]
    while True:
        draw(g.board)
        print ""
        print "The score is: Black marbles removed=%d, white marbles removed=%d." % (black_count, white_count)
        print "It is %s's turn." % g.get_turn()
        if not len(start_moves):
            result, board, new_black_count, new_white_count, move = get_move(g)
            while result != True:
                result, board, new_black_count, new_white_count, move = get_move(g)
            draw(board)
            print ""
            if new_black_count >= 6:
                print "*** White would win!"
            elif new_white_count >= 6:
                print "*** Black would win!"
            elif new_black_count != black_count or new_white_count != white_count:
                print "* You would push a marble off!"
            try:
                confirm = raw_input("Confirm move? [y/n]")
            except KeyboardInterrupt, e:
                print "\n".join(moves)
                raise e
            if confirm.upper() == "Y":
                moves.append(move)
                board, black_count, white_count = g.proc_move(move)
        else:
            move = start_moves.pop(0)
            print "*** Executing pre-defined start move", move
            moves.append(move)
            board, black_count, white_count = g.proc_move(move)
