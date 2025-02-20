def get_possible_moves(board, row, col):
    """
    Calculates the possible moves for a piece at a given position on the chessboard.

    Args:
        board: A 2D list representing the chessboard.
        row: The row index of the piece (0-7).
        col: The column index of the piece (0-7).

    Returns:
        A list of tuples, where each tuple represents a possible move as (row, col) coordinates.
    """

    piece = board[row][col]
    possible_moves = []

    if piece == "r" or piece == "R":  # Rook moves
        possible_moves.extend(get_rook_moves(board, row, col))
    elif piece == "n" or piece == "N":  # Knight moves
        possible_moves.extend(get_knight_moves(board, row, col))
    elif piece == "b" or piece == "B":  # Bishop moves
        possible_moves.extend(get_bishop_moves(board, row, col))
    elif piece == "q" or piece == "Q":  # Queen moves
        possible_moves.extend(get_queen_moves(board, row, col))
    elif piece == "k" or piece == "K":  # King moves
        possible_moves.extend(get_king_moves(board, row, col))
    elif piece == "p":  # Black pawn moves
        possible_moves.extend(get_black_pawn_moves(board, row, col))
    elif piece == "P":  # White pawn moves
        possible_moves.extend(get_white_pawn_moves(board, row, col))

    return possible_moves


def is_valid_move(row, col):
    """
    Checks if a given row and column are within the bounds of the chessboard.
    """
    return 0 <= row < 8 and 0 <= col < 8


def get_rook_moves(board, row, col):
    """
    Calculates possible moves for a Rook.
    """
    moves = []
    # Move upwards
    for r in range(row - 1, -1, -1):
        if board[r][col] == " ":
            moves.append((r, col))
        else:
            if (board[r][col].islower() and board[row][col].isupper()) or (
                board[r][col].isupper() and board[row][col].islower()
            ):
                moves.append((r, col))
            break  # Stop if we encounter another piece

    # Move downwards
    for r in range(row + 1, 8):
        if board[r][col] == " ":
            moves.append((r, col))
        else:
            if (board[r][col].islower() and board[row][col].isupper()) or (
                board[r][col].isupper() and board[row][col].islower()
            ):
                moves.append((r, col))
            break  # Stop if we encounter another piece

    # Move leftwards
    for c in range(col - 1, -1, -1):
        if board[row][c] == " ":
            moves.append((row, c))
        else:
            if (board[row][c].islower() and board[row][col].isupper()) or (
                board[row][c].isupper() and board[row][col].islower()
            ):
                moves.append((row, c))
            break  # Stop if we encounter another piece

    # Move rightwards
    for c in range(col + 1, 8):
        if board[row][c] == " ":
            moves.append((row, c))
        else:
            if (board[row][c].islower() and board[row][col].isupper()) or (
                board[row][c].isupper() and board[row][col].islower()
            ):
                moves.append((row, c))
            break  # Stop if we encounter another piece
    return moves


def get_knight_moves(board, row, col):
    """
    Calculates possible moves for a Knight.
    """
    moves = []
    possible_moves = [
        (row - 2, col - 1),
        (row - 2, col + 1),
        (row - 1, col - 2),
        (row - 1, col + 2),
        (row + 1, col - 2),
        (row + 1, col + 2),
        (row + 2, col - 1),
        (row + 2, col + 1),
    ]

    for r, c in possible_moves:
        if is_valid_move(r, c):
            if (
                board[r][c] == " "
                or (board[r][c].islower() and board[row][col].isupper())
                or (board[r][c].isupper() and board[row][col].islower())
            ):
                moves.append((r, c))
    return moves


def get_bishop_moves(board, row, col):
    """
    Calculates possible moves for a Bishop.
    """
    moves = []

    # Up-left diagonal
    r, c = row - 1, col - 1
    while is_valid_move(r, c):
        if board[r][c] == " ":
            moves.append((r, c))
            r -= 1
            c -= 1
        else:
            if (board[r][c].islower() and board[row][col].isupper()) or (
                board[r][c].isupper() and board[row][col].islower()
            ):
                moves.append((r, c))
            break  # Stop if we encounter another piece

    # Up-right diagonal
    r, c = row - 1, col + 1
    while is_valid_move(r, c):
        if board[r][c] == " ":
            moves.append((r, c))
            r -= 1
            c += 1
        else:
            if (board[r][c].islower() and board[row][col].isupper()) or (
                board[r][c].isupper() and board[row][col].islower()
            ):
                moves.append((r, c))
            break  # Stop if we encounter another piece

    # Down-left diagonal
    r, c = row + 1, col - 1
    while is_valid_move(r, c):
        if board[r][c] == " ":
            moves.append((r, c))
            r += 1
            c -= 1
        else:
            if (board[r][c].islower() and board[row][col].isupper()) or (
                board[r][c].isupper() and board[row][col].islower()
            ):
                moves.append((r, c))
            break  # Stop if we encounter another piece

    # Down-right diagonal
    r, c = row + 1, col + 1
    while is_valid_move(r, c):
        if board[r][c] == " ":
            moves.append((r, c))
            r += 1
            c += 1
        else:
            if (board[r][c].islower() and board[row][col].isupper()) or (
                board[r][c].isupper() and board[row][col].islower()
            ):
                moves.append((r, c))
            break  # Stop if we encounter another piece

    return moves


def get_queen_moves(board, row, col):
    """
    Calculates possible moves for a Queen.
    """
    moves = []
    moves.extend(get_rook_moves(board, row, col))
    moves.extend(get_bishop_moves(board, row, col))
    return moves


def get_king_moves(board, row, col):
    """
    Calculates possible moves for a King.
    """
    moves = []
    possible_moves = [
        (row - 1, col - 1),
        (row - 1, col),
        (row - 1, col + 1),
        (row, col - 1),
        (row, col + 1),
        (row + 1, col - 1),
        (row + 1, col),
        (row + 1, col + 1),
    ]

    for r, c in possible_moves:
        if is_valid_move(r, c):
            if (
                board[r][c] == " "
                or (board[r][c].islower() and board[row][col].isupper())
                or (board[r][c].isupper() and board[row][col].islower())
            ):
                moves.append((r, c))
    return moves


def get_black_pawn_moves(board, row, col):
    """
    Calculates possible moves for a black pawn.
    """
    moves = []
    # Move forward one square
    if is_valid_move(row + 1, col) and board[row + 1][col] == " ":
        moves.append((row + 1, col))

    # Move forward two squares (only on the starting rank)
    if row == 1 and board[row + 1][col] == " " and board[row + 2][col] == " ":
        moves.append((row + 2, col))

    # Capture diagonally
    if is_valid_move(row + 1, col - 1) and board[row + 1][col - 1].isupper():
        moves.append((row + 1, col - 1))
    if is_valid_move(row + 1, col + 1) and board[row + 1][col + 1].isupper():
        moves.append((row + 1, col + 1))

    return moves


def get_white_pawn_moves(board, row, col):
    """
    Calculates possible moves for a white pawn.
    """
    moves = []

    # Move forward one square
    if is_valid_move(row - 1, col) and board[row - 1][col] == " ":
        moves.append((row - 1, col))

    # Move forward two squares (only on the starting rank)
    if row == 6 and board[row - 1][col] == " " and board[row - 2][col] == " ":
        moves.append((row - 2, col))

    # Capture diagonally
    if is_valid_move(row - 1, col - 1) and board[row - 1][col - 1].islower():
        moves.append((row - 1, col - 1))
    if is_valid_move(row - 1, col + 1) and board[row - 1][col + 1].islower():
        moves.append((row - 1, col + 1))

    return moves


# Example Usage
if __name__ == "__main__":
    board = [
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", "Q", "K", "B", "N", "R"],
    ]

    # Example: Get possible moves for the rook at (0, 0)
    rook_row = 0
    rook_col = 0
    possible_moves_rook = get_possible_moves(board, rook_row, rook_col)
    print(f"Possible moves for rook at ({rook_row}, {rook_col}): {possible_moves_rook}")

    # Example: Get possible moves for the knight at (0, 1)
    knight_row = 0
    knight_col = 1
    possible_moves_knight = get_possible_moves(board, knight_row, knight_col)
    print(
        f"Possible moves for knight at ({knight_row}, {knight_col}): {possible_moves_knight}"
    )

    # Example: Get possible moves for the white pawn at (6, 0)
    pawn_row = 6
    pawn_col = 0
    possible_moves_pawn = get_possible_moves(board, pawn_row, pawn_col)
    print(
        f"Possible moves for white pawn at ({pawn_row}, {pawn_col}): {possible_moves_pawn}"
    )
