import pygame
import sys
import math
import time
from brain import get_possible_moves

# Initialize Pygame
pygame.init()

# Constants for the display
BOARD_SIZE = 8
SQUARE_SIZE = 120
WIDTH, HEIGHT = BOARD_SIZE * SQUARE_SIZE, BOARD_SIZE * SQUARE_SIZE
COLOR_1 = (253, 232, 182)
COLOR_2 = (88, 57, 39)

# Create a window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Chess Game")


class Piece:
    def __init__(self):
        self.type = " "
        self.value = 0
        self.curr_pos = (0, 0)
        self.possible_moves = []  # List of tuples (x,y)
        self.best_score = 0
        self.best_move = (0, 0)


class Bot:
    def __init__(self, board):
        self.pieces = []
        self.best_piece = Piece()
        self.create_pieces(board)

    def create_pieces(self, board):
        piece_values = {"p": 1, "n": 3, "b": 3, "r": 5, "q": 9, "k": 1337}

        for row in range(2):
            for col in range(8):
                piece = Piece()
                piece.type = board[row][col]
                piece.curr_pos = (row, col)
                piece.value = piece_values.get(piece.type)
                piece.possible_moves = get_possible_moves(
                    board, piece.curr_pos[0], piece.curr_pos[1]
                )
                self.choose_best_square(board, piece, piece.possible_moves)
                self.pieces.append(piece)

        if len(self.pieces) != 16:
            print("Error in piece creation...")
            quit()

    def choose_best_square(self, board, piece, possible_moves):
        """
        Chooses the best square to move a piece to, prioritizing capturing higher-value pieces.
        This is a VERY simplified example.
        """
        piece_values = {
            "p": 1,
            "r": 5,
            "n": 3,
            "b": 3,
            "q": 9,
            "k": 0,
            "P": 1,
            "R": 5,
            "N": 3,
            "B": 3,
            "Q": 9,
            "K": 0,
        }  # Relative piece values

        best_score = -float("inf")  # Initialize with a very low score
        piece.best_Score = -float("inf")  # Initialize with a very low score

        for move_row, move_col in possible_moves:
            target_piece = board[move_row][move_col]

            # Check if we are capturing a piece
            if target_piece != " ":
                score = piece_values.get(
                    target_piece.lower(), 0
                )  # Value of captured piece (absolute value)
            else:
                score = 0  # No capture

            #  Add a small bonus for controlling the center
            if (move_row, move_col) in [(3, 3), (3, 4), (4, 3), (4, 4)]:
                score += 0.1

            if score > best_score:
                best_score = score
                piece.best_score = score
                piece.best_move = (move_row, move_col)

    def update_moves(self, board):
        top_score = -1
        for piece in self.pieces:
            piece.possible_moves = get_possible_moves(
                board, piece.curr_pos[0], piece.curr_pos[1]
            )
            self.choose_best_square(board, piece, piece.possible_moves)
            if piece.best_score > top_score:
                top_score = piece.best_score
                self.best_piece = piece

    def move(self, board):
        self.update_moves(board)
        end_x, end_y = self.best_piece.best_move
        board[self.best_piece.curr_pos[0]][self.best_piece.curr_pos[1]] = " "
        board[end_x][end_y] = self.best_piece.type
        self.best_piece.curr_pos = (end_x, end_y)
        self.best_piece = Piece()
        # self.update_moves(board)
        return board


class Game:
    def __init__(self):
        def load_piece_icons():
            piece_images = {}
            pieces = ["r", "n", "b", "q", "k", "p"]
            colors = ["w", "b"]

            for color in colors:
                for piece in pieces:
                    piece_name = f"{color}_{piece}"  # e.g., 'w_k', 'b_p'
                    try:
                        piece_images[piece_name] = pygame.image.load(
                            f"icons/{color}/{piece}.png"
                        )
                        piece_images[piece_name] = pygame.transform.scale(
                            piece_images[piece_name], (SQUARE_SIZE, SQUARE_SIZE)
                        )
                    except pygame.error:
                        print(f"Could not load image for {color}_{piece}")
            return piece_images

        self.chosen_piece = " "
        self.is_white = True

        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.possible_moves = []

        self.board = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"],
        ]

        self.piece_icons = load_piece_icons()

    def move(self, col, row, bot):
        if self.chosen_piece == " ":
            self.chosen_piece = self.board[row][col]
            self.start_x = row
            self.start_y = col
            self.possible_moves = get_possible_moves(self.board, row, col)
        else:
            self.end_x = row
            self.end_y = col

            for possible_x, possible_y in self.possible_moves:
                print(self.end_x, possible_x)
                if self.end_x == possible_x and self.end_y == possible_y:
                    self.board[row][col] = self.chosen_piece
                    self.board[self.start_x][self.start_y] = " "
                    self.chosen_piece = " "
                    self.possible_moves = []
                    self.board = bot.move(self.board)  # Move that botty boy


def validate_move(piece, board, start_x, end_x, start_y, end_y, is_white):
    target = board[end_x][end_y]
    # Ensure there is a piece at the start position and it's the player's piece
    if (
        piece == " "
        or (is_white and piece.islower())
        or (not is_white and piece.isupper())
    ):
        return False

    # Ensure the target space is not occupied by a piece of the same color
    if (is_white and target.isupper()) or (not is_white and target.islower()):
        return False

    # Piece movement rules
    if piece.lower() == "p":  # Pawn movement
        if is_white:
            if (
                start_x == 6
                and end_x == 4
                and start_y == end_y
                and board[5][start_y] == " "
                and board[4][start_y] == " "
            ):
                return True  # First double move
            if end_x == start_x - 1 and start_y == end_y and target == " ":
                return True  # Single move forward
            if end_x == start_x - 1 and abs(start_y - end_y) == 1 and target.islower():
                return True  # Capture diagonally
        else:
            if (
                start_x == 1
                and end_x == 3
                and start_y == end_y
                and board[2][start_y] == " "
                and board[3][start_y] == " "
            ):
                return True  # First double move
            if end_x == start_x + 1 and start_y == end_y and target == " ":
                return True  # Single move forward
            if end_x == start_x + 1 and abs(start_y - end_y) == 1 and target.isupper():
                return True  # Capture diagonally

    elif piece.lower() == "r":  # Rook movement
        if start_x == end_x:  # Horizontal move
            step = 1 if start_y < end_y else -1
            for y in range(start_y + step, end_y, step):
                if board[start_x][y] != " ":
                    return False
            return True
        elif start_y == end_y:  # Vertical move
            step = 1 if start_x < end_x else -1
            for x in range(start_x + step, end_x, step):
                if board[x][start_y] != " ":
                    return False
            return True

    elif piece.lower() == "n":  # Knight movement
        if (abs(start_x - end_x), abs(start_y - end_y)) in [(2, 1), (1, 2)]:
            return True

    elif piece.lower() == "b":  # Bishop movement
        if abs(start_x - end_x) == abs(start_y - end_y):
            x_step = 1 if end_x > start_x else -1
            y_step = 1 if end_y > start_y else -1
            x, y = start_x + x_step, start_y + y_step
            while x != end_x and y != end_y:
                if board[x][y] != " ":
                    return False
                x += x_step
                y += y_step
            return True

    elif piece == "q":
        if validate_move(
            piece="r",
            board=board,
            start_x=start_x,
            end_x=end_x,
            start_y=start_y,
            end_y=end_y,
            is_white=False,
        ) or validate_move(
            piece="b",
            board=board,
            start_x=start_x,
            end_x=end_x,
            start_y=start_y,
            end_y=end_y,
            is_white=False,
        ):
            return True

    elif piece == "Q":
        if validate_move(
            piece="R",
            board=board,
            start_x=start_x,
            end_x=end_x,
            start_y=start_y,
            end_y=end_y,
            is_white=True,
        ) or validate_move(
            piece="B",
            board=board,
            start_x=start_x,
            end_x=end_x,
            start_y=start_y,
            end_y=end_y,
            is_white=True,
        ):
            return True

    elif piece.lower() == "k":  # King movement
        if abs(start_x - end_x) <= 1 and abs(start_y - end_y) <= 1:
            return True

    return False


# Function to draw the chessboard
def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = COLOR_1 if (row + col) % 2 == 0 else COLOR_2
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(
                    col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE
                ),
            )


# Function to draw pieces using images
def draw_pieces(piece_images, board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board[row][col]
            if piece != " ":
                color = "w" if piece.isupper() else "b"
                piece_type = piece.lower()
                image_key = f"{color}_{piece_type}"
                screen.blit(
                    piece_images[image_key], (col * SQUARE_SIZE, row * SQUARE_SIZE)
                )


def draw_possible_moves(possible_moves):
    for row, col in possible_moves:
        pygame.draw.rect(
            screen,
            (0, 255, 0, 128),
            pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
        )


def display_temp_text(message, duration):
    BLACK = (0, 0, 0)
    font = pygame.font.SysFont("Arial", 50)
    start_time = time.time()

    while time.time() - start_time < duration:
        # screen.fill(BLACK)  # Clear screen
        # Render and display the message
        text = font.render(message, True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)  # Display the text at a position
        pygame.display.flip()
        pygame.time.wait(10)  # Small delay to keep screen responsive


# Main game loop
def main():
    game = Game()
    bot = Bot(game.board)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and game.is_white:
                x, y = pygame.mouse.get_pos()
                col = math.floor(x / SQUARE_SIZE)
                row = math.floor(y / SQUARE_SIZE)
                game.move(col, row, bot)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_board()
        draw_pieces(game.piece_icons, game.board)
        draw_possible_moves(game.possible_moves)
        pygame.display.flip()


# Run the game
if __name__ == "__main__":
    main()
