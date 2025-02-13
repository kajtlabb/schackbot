import pygame
import sys
import math
import time

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

class Game:
    def __init__(self):
        def load_piece_icons():
            piece_images = {}
            pieces = ['r', 'n', 'b', 'q', 'k', 'p']
            colors = ['w', 'b']

            for color in colors:
                for piece in pieces:
                    piece_name = f"{color}_{piece}"  # e.g., 'w_k', 'b_p'
                    try:
                        piece_images[piece_name] = pygame.image.load(f"icons/{color}/{piece}.png")
                        piece_images[piece_name] = pygame.transform.scale(piece_images[piece_name], (SQUARE_SIZE, SQUARE_SIZE))
                    except pygame.error:
                        print(f"Could not load image for {color}_{piece}")
            return piece_images
    
        self.in_play = " "
        self.is_white = True

        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0

        self.board = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"]
        ]

        self.piece_icons = load_piece_icons()

    def move(self, col, row):
        if self.in_play == " ":
                self.in_play = self.board[row][col]
                self.board[row][col] = " "
                self.start_x = row
                self.start_y = col
        else:
                self.end_x = row
                self.end_y = col
                if not self.validate_move(piece = self.in_play):
                    self.reset()
                else:
                    if self.board[row][col] == "K" or self.board[row][col] == "k":
                        display_temp_text("GAME OVER", 2)
                        pygame.quit()
                        quit()
                    self.board[row][col] = self.in_play
                    self.in_play = " "
                    self.is_white = not self.is_white
                    draw_pieces(self.piece_icons, self.board)
                    display_temp_text(f'{"WHITE" if self.is_white else "BLACK"} TURN', 1)
    
    def reset(self):
        self.board[self.start_x][self.start_y] = self.in_play
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.in_play = " "

    def validate_move(self, piece):
            print(piece)
            target = self.board[self.end_x][self.end_y]
            # Ensure there is a piece at the start position and it's the player's piece
            if piece == " " or (self.is_white and piece.islower()) or (not self.is_white and piece.isupper()):
                return False
            
            # Ensure the target space is not occupied by a piece of the same color
            if (self.is_white and target.isupper()) or (not self.is_white and target.islower()):
                return False

            # Piece movement rules
            if piece.lower() == "p":  # Pawn movement
                if self.is_white:
                    if self.start_x == 6 and self.end_x == 4 and self.start_y == self.end_y and self.board[5][self.start_y] == " " and self.board[4][self.start_y] == " ":
                        return True  # First double move
                    if self.end_x == self.start_x - 1 and self.start_y == self.end_y and target == " ":
                        return True  # Single move forward
                    if self.end_x == self.start_x - 1 and abs(self.start_y - self.end_y) == 1 and target.islower():
                        return True  # Capture diagonally
                else:
                    if self.start_x == 1 and self.end_x == 3 and self.start_y == self.end_y and self.board[2][self.start_y] == " " and self.board[3][self.start_y] == " ":
                        return True  # First double move
                    if self.end_x == self.start_x + 1 and self.start_y == self.end_y and target == " ":
                        return True  # Single move forward
                    if self.end_x == self.start_x + 1 and abs(self.start_y - self.end_y) == 1 and target.isupper():
                        return True  # Capture diagonally
            
            elif piece.lower() == "r":  # Rook movement
                if self.start_x == self.end_x:  # Horizontal move
                    step = 1 if self.start_y < self.end_y else -1
                    for y in range(self.start_y + step, self.end_y, step):
                        if self.board[self.start_x][y] != " ":
                            return False
                    return True
                elif self.start_y == self.end_y:  # Vertical move
                    step = 1 if self.start_x < self.end_x else -1
                    for x in range(self.start_x + step, self.end_x, step):
                        if self.board[x][self.start_y] != " ":
                            return False
                    return True
            
            elif piece.lower() == "n":  # Knight movement
                if (abs(self.start_x - self.end_x), abs(self.start_y - self.end_y)) in [(2, 1), (1, 2)]:
                    return True
            
            elif piece.lower() == "b":  # Bishop movement
                if abs(self.start_x - self.end_x) == abs(self.start_y - self.end_y):
                    x_step = 1 if self.end_x > self.start_x else -1
                    y_step = 1 if self.end_y > self.start_y else -1
                    x, y = self.start_x + x_step, self.start_y + y_step
                    while x != self.end_x and y != self.end_y:
                        if self.board[x][y] != " ":
                            return False
                        x += x_step
                        y += y_step
                    return True
            
            elif piece == "q":
                if self.validate_move(piece="r") or self.validate_move(piece="b"):
                    return True
            
            elif piece == "Q":
                if self.validate_move(piece="R") or self.validate_move(piece="B"):
                    return True
            
            elif piece.lower() == "k":  # King movement
                if abs(self.start_x - self.end_x) <= 1 and abs(self.start_y - self.end_y) <= 1:
                    return True

            return False
# Function to draw the chessboard
def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = COLOR_1 if (row + col) % 2 == 0 else COLOR_2
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Function to draw pieces using images
def draw_pieces(piece_images, board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board[row][col]
            if piece != " ":
                color = "w" if piece.isupper() else "b"
                piece_type = piece.lower()
                image_key = f"{color}_{piece_type}"
                screen.blit(piece_images[image_key], (col * SQUARE_SIZE, row * SQUARE_SIZE))

def display_temp_text(message, duration):
    # Define colors
    BLACK = (0, 0, 0)
    # Font
    font = pygame.font.SysFont('Arial', 50)
    start_time = time.time()
    while time.time() - start_time < duration:
        #screen.fill(BLACK)  # Clear screen
        # Render and display the message
        text = font.render(message, True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT// 2))
        screen.blit(text, text_rect)  # Display the text at a position
        pygame.display.flip()
        pygame.time.wait(10)  # Small delay to keep screen responsive

# Main game loop
def main():
    game = Game()
    while True:        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                col = math.floor(x / SQUARE_SIZE)
                row = math.floor(y / SQUARE_SIZE)
                game.move(col, row)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        draw_board()
        draw_pieces(game.piece_icons, game.board)
        pygame.display.flip()

# Run the game
if __name__ == "__main__":
    main()
