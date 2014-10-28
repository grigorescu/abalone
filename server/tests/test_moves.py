import server.gameState
from server.ball import black, white, empty

def test_turns():
    """Ensure that taking turns works as expected."""
    g = server.gameState.GameState()

    assert g.get_turn() == "black"
    g.proc_move("A1-B2")
    assert g.get_turn() == "white"
    g.proc_move("G7-G8")
    assert g.get_turn() == "black"

    # Preview shouldn't update the turn
    g.proc_move("B1-A1", True)
    assert g.get_turn() == "black"

    # Neither should an invalid move:
    try:
        g.proc_move("I8-Q3")
    except ValueError:
        pass
    assert g.get_turn() == "black"


def test_invalid_moves():
    """Ensure that invalid moves are rejected."""
    g = server.gameState.GameState()

    # Invalid move notation
    try:
        g.proc_move("I8-I7-H8-H7")
    except ValueError:
        pass

    try:
        g.proc_move("I8")
    except ValueError:
        pass

    try:
        g.proc_move("I8-I9")
    except ValueError:
        pass

    try:
        g.proc_move("I8-J8")
    except ValueError:
        pass

    try:
        g.proc_move("B6-A6")
    except ValueError:
        pass

    try:
        g.proc_move("I9-I8")
    except ValueError:
        pass

    try:
        g.proc_move("J8-I8")
    except ValueError:
        pass

    try:
        g.proc_move("A1-A4-B1")
    except ValueError:
        pass

    try:
        g.proc_move("A1-A3-A0")
    except ValueError:
        pass

    try:
        g.proc_move("A0-A2-B0")
    except ValueError:
        pass

    # Trying to move too far
    try:
        g.proc_move("C3-E3")
    except ValueError:
        pass

    assert g.board == [
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


def test_whole_game_white_wins():
    """Test an entire game. White wins, invalid moves in here too."""

    g = server.gameState.GameState()

    # Pacs
    g.proc_move("A4-B4")
    g.proc_move("I8-H7")
    g.proc_move("B4-C4")

    try:
        # 1 v 1 pac
        g.proc_move("F5-E4")
    except ValueError:
        pass

    g.proc_move("I9-H8")
    g.proc_move("C3-D4")

    try:
        # 2 v 2 pac
        g.proc_move("G7-F6")
    except ValueError:
        pass

    try:
        # Inferior strength - 1 against 2
        g.proc_move("F6-E5")
    except ValueError:
        pass

    g.proc_move("I5-H4")
    g.proc_move("B3-C3")

    try:
        # Inferior strength - 3 against 4
        g.proc_move("H8-G7")
    except ValueError:
        pass

    g.proc_move("H4-G3")
    g.proc_move("B2-C2")

    try:
        # 3 v 3 pac
        g.proc_move("H8-G7")
    except ValueError:
        pass

    g.proc_move("G3-F3")
    g.proc_move("C3-B2")
    g.proc_move("G6-F5")
    g.proc_move("B1-C2")
    g.proc_move("F3-E3")
    g.proc_move("D3-C2")
    g.proc_move("E3-D3")
    g.proc_move("B1-C2-C1")

    try:
        # Blocked by a marble behind it
        g.proc_move("G6-F5")
    except ValueError:
        pass

    g.proc_move("D3-C3")
    g.proc_move("C1-B1")
    g.proc_move("H7-G6")

    try:
        # Blocked by a marble behind it
        g.proc_move("E5-D4")
    except ValueError:
        pass

    g.proc_move("B2-A3-B3")
    g.proc_move("G6-F5")
    g.proc_move("A5-A4")
    g.proc_move("F5-E4")
    g.proc_move("A1-B2")
    g.proc_move("C3-D3")
    g.proc_move("A4-B4")
    g.proc_move("E4-D3")
    g.proc_move("D2-E2")
    g.proc_move("D3-D2")

    try:
        # Blocked by a marble behind it
        g.proc_move("A2-B2")
    except ValueError:
        pass

    g.proc_move("E5-D5")
    g.proc_move("I7-H6")
    g.proc_move("B3-B2")

    assert g.black_marbles_removed == 2
    assert g.white_marbles_removed == 1

    g.proc_move("D2-D3")
    g.proc_move("B5-C5")
    g.proc_move("D3-C2")
    g.proc_move("C5-D5")
    g.proc_move("C2-C3")
    g.proc_move("B6-B5")

    try:
        # Blocked by a marble behind it
        g.proc_move("H8-G7")
    except ValueError:
        pass

    g.proc_move("C3-D3")
    g.proc_move("D4-E4")
    g.proc_move("D3-D4")
    g.proc_move("B5-C5")

    try:
        # Blocked by a marble behind it
        g.proc_move("H8-G7")
    except ValueError:
        pass

    g.proc_move("G5-G4")

    try:
        # Blocked by a marble behind it
        g.proc_move("C5-D5")
    except ValueError:
        pass

    g.proc_move("F5-G6")
    g.proc_move("F4-F3")
    g.proc_move("G6-H7")
    g.proc_move("G4-F3")
    g.proc_move("H7-I8")
    g.proc_move("F3-E2")
    g.proc_move("I8-I9")
    g.proc_move("E3-D2")
    g.proc_move("A3-A2")
    g.proc_move("F6-G7")
    g.proc_move("B4-C5-A4")
    g.proc_move("F2-E2")

    try:
        g.proc_move("B5-A4-A5")
    except ValueError:
        pass

    g.proc_move("A1-A2")
    g.proc_move("E2-D2")

    try:
        g.proc_move("A2-A1")
    except EOFError:
        pass

    print g.board

    assert g.board == [
            [empty, black, black, black, empty],
            [white, white, empty, empty, black, empty],
            [empty, white, empty, black, empty, empty, empty],
            [white, white, empty, white, black, empty, empty, empty],
            [empty, empty, empty, black, black, empty, empty, empty, empty],
            [empty, empty, empty, empty, empty, empty, empty, empty],
            [empty, empty, empty, empty, white, empty, empty],
            [empty, white, white, empty, white, white],
            [empty, white, empty, empty, white]
            ]



def test_inline_moves_no_pushing():
    """Tests moving a line of 1, 2, or 3 marbles in each direction inline."""

    g = server.gameState.GameState()

    g.proc_move("A1-B2")  # NE - line of 3
    g.proc_move("G7-G8")  # E  - line of 1
    g.proc_move("B1-A1")  # SE - line of 1
    g.proc_move("I8-H7")  # SW - line of 3
    g.proc_move("B4-B3")  # W  - line of 3
    g.proc_move("G8-H8")  # NW - line of 2

    g.proc_move("B3-C4")  # NE - line of 2 (3 done)
    g.proc_move("G5-G6")  # E  - line of 2 (1 done)
    g.proc_move("D5-C4")  # SE - line of 2 (1 done)
    g.proc_move("H8-G7")  # SW - line of 2 (3 done)
    g.proc_move("B5-B4")  # W  - line of 1 (3 done)
    g.proc_move("F5-G5")  # NW - line of 1 (2 done)

    g.proc_move("B6-C7") # NE - line of 1 (2, 3 done)
    g.proc_move("G5-G6") # E  - line of 3 (1, 2 done)
    g.proc_move("B4-C4") # NW - line of 3 (1, 2 done)
    g.proc_move("F6-E5") # SW - line of 1 (2, 3 done)
    g.proc_move("E4-D4") # SE - line of 3 (1, 2 done)
    g.proc_move("G7-G6") # W  - line of 2 (1, 3 done)

    assert g.board == [
            [black, black, black, black, black],
            [black, black, black, black, empty, empty],
            [empty, empty, black, black, black, empty, black],
            [empty, empty, empty, black, empty, empty, empty, empty],
            [empty, empty, empty, empty, white, empty, empty, empty, empty],
            [empty, empty, empty, empty, empty, empty, empty, empty],
            [empty, empty, white, white, empty, white, empty],
            [white, white, white, white, empty, white],
            [white, white, white, white, white]
    ]


def test_broadside_moves():
    """Tests moving a line of 1, 2 or 3 marbles in each direction broadside."""

    g = server.gameState.GameState()

    g.proc_move("C3-C5-D4")  # NE - line of 3
    g.proc_move("G5-G7-F5")  # SE - line of 3
    g.proc_move("D4-D6-C3")  # SW - line of 3
    g.proc_move("F5-F7-G5")  # NW - line of 3
    # Back in start state
    g.proc_move("A1-B1")
    g.proc_move("I9-H9")
    g.proc_move("B1-C1")
    g.proc_move("H9-G9")
    g.proc_move("B2-A2-B1")  # W  - line of 2
    g.proc_move("I8-H8-I9")  # E  - line of 2

    g.proc_move("B5-B6-C6")  # NE - line of 2 (3 done)
    g.proc_move("G6-G5-F6")  # SE - line of 2 (3 done)
    g.proc_move("C7-C6-B6")  # SW - line of 2 (3 done)
    g.proc_move("F5-F6-G5")  # NW - line of 2 (3 done)
    g.proc_move("C3-A3-C2")  # W  - line of 3 (2 done)
    g.proc_move("G7-I7-G8")  # E  - line of 3 (2 done)

    g.proc_move("C5-C5-D6")  # NE - line of 1 (2, 3 done)
    g.proc_move("G6-G6-F6")  # SE - line of 1 (2, 3 done)
    g.proc_move("C4-C4-B3")  # SW - line of 1 (2, 3 done)
    g.proc_move("F6-F6-G6")  # NW - line of 1 (2, 3 done)
    g.proc_move("D1-D1-D2")  # E  - line of 1 (2, 3 done)
    g.proc_move("F9-F9-F8")  # W  - line of 1 (2, 3 done)

    assert g.board == [
            [black, black, empty, black, black],
            [black, black, black, black, black, black],
            [black, black, empty, empty, empty, empty, empty],
            [empty, black, empty, empty, empty, black, empty, empty],
            [empty, empty, empty, empty, empty, empty, empty, empty, empty],
            [empty, empty, empty, empty, empty, empty, white, empty],
            [empty, empty, white, white, empty, white, white],
            [white, white, white, empty, white, white],
            [white, white, empty, white, white]
    ]