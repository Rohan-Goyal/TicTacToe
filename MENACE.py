import random

# NOTE: For now, humans are Y and machines are X
board_geometric = [
    [(-1, 1), (0, 1), (1, 1)],
    [(-1, 0), (0, 0), (1, 0)],
    [(-1, -1), (0, -1), (1, -1)],
]
# Matrix representation of tic-tac-toe board

# IDEA: Replace with letters/symbols for simplicity

board = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
round = 0


# Utility functions


def reset():
    global board
    global round
    board = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    round = 0
    # After a victory, resets all global vars (round)
    return


def pprint(someboard):
    for x in someboard:
        print(*x, sep=" ")


def index_2d(data, search):
    for i, e in enumerate(data):
        try:
            return i, e.index(search)
        except ValueError:
            pass
    raise ValueError("{} is not in list".format(repr(search)))


def boxify(character):
    "If input=X, returns"

    pass


def construct_columns(gameboard, measure=3):
    column_set = []
    for col_num in range(0, measure):
        # Generates a list representing a column
        column = [i[col_num] for i in gameboard]
        column_set.append(column)
    return column_set


def construct_diagonals(gameboard, measure=3):
    downward_diagonal = [gameboard[n][n] for n in range(0, measure)]
    upward_diagonal = [
        gameboard[2][0],
        gameboard[1][1],
        gameboard[0][2],
    ]  # Incredibly shoddy, FIXME
    return downward_diagonal, upward_diagonal


# Play the game
# NOTE: In this game, the machine always goes first


def human_play():
    print()
    pprint(board)
    choice = int(input("Choose your position: "))
    # The position the player places their piece
    if board[choice // 3][choice % 3] != "X":
        board[choice // 3][choice % 3] = "Y"
    else:
        print("Try again- that spot is taken")


def play_at(position_list):
    random.shuffle(position_list)
    for point in position_list:
        # If there are any possibilities left left, it plays a corner
        if (
            type(board[point[0]][point[1]]) == int
        ):  # Has not been overwritten by x or y string
            board[point[0]][point[1]] = "X"
            return True
    return False


def victory_approaching(
    gameboard, winner, defender
):  # Winner is whoever has 2 already. Defender is the other one.
    # TODO: REFACTOR WITH LIST COMPREHENSIONS/FILTERS/LAMBDA
    # Returns: The integer denoting the square where the AI must play in order to stop the victory.
    for row in gameboard:
        if row.count(winner) >= 2 and row.count(defender) == 0:
            for element in row:  # FIXME
                if element != winner:
                    return element

    columns = construct_columns(gameboard)
    for column in columns:
        if column.count(winner) >= 2 and column.count(defender) == 0:
            for element in column:  # FIXME
                if element != winner:
                    return element

    diagonals = construct_diagonals(gameboard)
    for diagonal in diagonals:
        if diagonal.count(winner) >= 2 and diagonal.count(defender) == 0:
            for element in diagonal:  # FIXME
                if element != winner:
                    return element
    # Check if there are two 'y's in the same line/diagonal
    # If there is, it returns:
    # The integer of that location
    # Given this information, machine should play at that point
    return False


def exploit_victory(gameboard, winner, defender):
    victory = victory_approaching(board, winner, defender)
    if victory:
        a = index_2d(board, victory)  # Tuple, row/col coords of that integer
        board[a[0]][a[1]] = "X"
        return


def machine_ai(gameboard):

    if round == 0:
        board[1][1] = "X"
        return  # Plays the center on the starting round

    exploit_victory(board, "X", "Y")
    exploit_victory(board, "Y", "X")

    corner_positions = [(0, 0), (2, 2), (0, 2), (2, 0)]
    if play_at(corner_positions):
        return

    remaining = [(0, 1), (1, 0), (2, 1), (1, 2)]
    if play_at(remaining):
        return


# Victory conditions


def isidentical(somelist):
    for i in somelist:
        if i != somelist[0]:
            return False
    return True


def check_victor(somelist):
    if somelist[0] == "X":
        return "X"
    elif somelist[0] == "Y":
        return "Y"
    return False


def integrated_victory(somelist):
    if isidentical(somelist):
        return check_victor(somelist)
    else:
        return False


def row_victory(gameboard):
    x = [integrated_victory(row) for row in gameboard]
    for i in x:
        if i != False:
            return i
    return False


def column_victory(gameboard):
    x = [integrated_victory(column) for column in construct_columns(gameboard)]
    for i in x:
        if i != False:
            return i
    return False  # Only triggered if no columns are identical


def diagonal_victory(gameboard):
    diagonals = construct_diagonals(gameboard)
    return (
        integrated_victory(diagonals[0])
        if integrated_victory(diagonals[0])
        else integrated_victory(diagonals[1])
    )
    # return False  # After checking everything


def is_victory(gameboard):
    for i in (
        diagonal_victory(gameboard),
        column_victory(gameboard),
        row_victory(gameboard),
    ):
        if i:
            return i
    return False


def is_draw(gameboard):
    # Check for remaining integers
    for row in gameboard:  # Cycles through every element of the matrix
        for i in row:
            if type(i) == int:
                return False
    return True  # Only if there are no integers left


# Main function
def main():
    global round
    round = 0
    while True:
        if is_victory(board):
            print("The victor is " + str(is_victory(board)))
            pprint(board)
            break
        elif is_draw(board):
            print("draw reached")
            pprint(board)
            break
        else:
            machine_ai(board)
            if is_victory(board):
                print("The victor is " + str(is_victory(board)))
                pprint(board)
                break
            elif is_draw(board):
                print("Draw reached")
                pprint(board)
                break
            human_play()
            round += 1
    reset()


if __name__ == "__main__":
    main()

# Unused functions


def machine_play():  # Random player; will customise later.
    choice_x = random.randint(0, 2)
    choice_y = random.randint(0, 2)
    # TODO: Write these choices to text/JSON/list
    if board[choice_y][choice_x] != "Y":  # Spot not taken
        board[choice_y][choice_x] = "X"  # Claims the spot
        return
    else:
        machine_play()


def play_corner():
    corners = (0, 2)
    x = random.choice(corners)
    y = random.choice(corners)
    if board[x][y] != "Y":
        board[x][y] = "X"
        return
    else:
        play_corner()


def play_remaining():
    remaining = [(0, 1), (1, 0), (2, 1), (1, 2)]
    random.shuffle(remaining)
    chosen = random.choice(remaining)
    x = chosen[0]
    y = chosen[1]
    if board[x][y] != "Y":
        board[x][y] = "X"
        return
    else:
        play_remaining()

# Proper AI implementation:
# TODO: (Maybe) Refactor the machine as a class or object
"Across the course of the game, note every choice (x,y) combo. If it wins, you increase the probability of each combo by appending them to some massive index of possibilities (presumably). If it loses, you delete the first instance of each of those choices"
""" Data Structure: Each choice is represented by a matrix and an integer or tuple (yet to decide). The matrix represents the position before the move, and the integer represents the position of the 'Y', or the tuple represents the X and Y coordinates. Since we don't care about coordinates here, an int probably makes more sense."""
""" For every position, there are some number of possible moves. The computer identifies the position via seaching through a massive set of matrices, and then picks a random move from the associated moveset. It saves this random move to a variable. If the game is a loss, it deletes each move it made from the associated list (once). If it wins, it adds 3 instances of that element, and it adds a single element on a draw  """
""" NB: A maximum of 5 moves (from the first player- 4 from the second) can occur in a game. This lowers the search space and eliminates the need for a WHILE loop  """


def generate_all_possible_matrices():
    board = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    all_possible_boards = {}
    for array in board:
        for index, item in enumerate(array):
            board1 = board
            board1[array][index] = "X"  # FIXME
            all_possible_boards.update(index, board1)
