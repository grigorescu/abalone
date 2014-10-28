    #
    # def __repr__(self):
    #     """Converts the board state to ASCII art.
    #
    #          I O O O O O
    #         H O O O O O O
    #        G + + O O O + +
    #       F + + + + + + + +
    #      E + + + + + + + + +
    #       D + + + + + + + + 9
    #        C + + @ @ @ + + 8
    #         B @ @ @ @ @ @ 7
    #          A @ @ @ @ @ 6
    #             1 2 3 4 5
    #                     """
    #
    #     color = ["red", "green", "yellow", "blue", "magenta", "cyan", "white", "red", "green"]
    #
    #     result = ""
    #
    #     for row in range(8, -1, -1):
    #         offset = abs(row - 4)
    #         color_offset = offset
    #         if row <= 4: color_offset = 0
    #
    #         space = " " * offset
    #         label = chr(ord('A') + row)
    #
    #         result += space + label
    #         for col in range (0, 9-offset):
    #             result += "  " + colored(str(self.board[row][col]), color[col + color_offset])
    #
    #         if row < 4: result += "  " + colored(str(row + 6), color[row + 5])
    #         result += "\n"
    #     result += "        " + colored("1", "red") + "  " + colored("2", "green") + "  " + colored("3", "yellow") + "  " + colored("4", "blue") + "  " + colored("5", "magenta")
    #
    #     return result