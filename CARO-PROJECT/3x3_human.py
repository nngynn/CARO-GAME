import pygame
import sys
import os

pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CARO!")

# Load images
ICON = pygame.image.load("assets/icon.jpg")
pygame.display.set_icon(ICON)

BOARD = pygame.image.load("assets/board.png")
X_IMG = pygame.image.load("assets/x.png").convert_alpha()
O_IMG = pygame.image.load("assets/o.png").convert_alpha()
X_WIN_IMG = pygame.image.load("assets/x_win.png").convert_alpha()
O_WIN_IMG = pygame.image.load("assets/o_win.png").convert_alpha()
DRAW_IMG = pygame.image.load("assets/draw.png").convert_alpha()
RESTART_IMG = pygame.image.load("assets/restart.png").convert_alpha()
HOME_IMG = pygame.image.load("assets/home.png").convert_alpha()

# Load sounds
WIN_SOUND = pygame.mixer.Sound("assets/win_sound.mp3")
DRAW_SOUND = pygame.mixer.Sound("assets/draw.mp3")
CLICK_SOUND = pygame.mixer.Sound("assets/click_sound.wav")  # Add a click sound file

# Colors
BG_COLOR = (72, 159, 181)

# Button class for Restart and Home
class Button:
    def __init__(self, x, y, image, action, arg=None):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.action = action
        self.arg = arg
        self.is_over = False
        self.is_pressed = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, mouse_pos, mouse_pressed, mouse_was_pressed):
        self.is_over = self.rect.collidepoint(mouse_pos)
        if self.is_over and mouse_pressed[0] and not mouse_was_pressed[0]:
            self.is_pressed = True
        elif self.is_pressed and not mouse_pressed[0] and mouse_was_pressed[0]:
            self.is_pressed = False
            CLICK_SOUND.play()  # Play sound on button click
            self.action(self.arg)

# Game state
board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
graphical_board = [[[None, None], [None, None], [None, None]], 
                   [[None, None], [None, None], [None, None]], 
                   [[None, None], [None, None], [None, None]]]

to_move = 'X'

# Initialize buttons
restart_button = Button(WIDTH - 120, 10, RESTART_IMG, lambda _: reset_game())
home_button = Button(WIDTH - 60, 10, HOME_IMG, lambda _: return_to_menu())

SCREEN.fill(BG_COLOR)
SCREEN.blit(BOARD, (135, 35))
pygame.display.update()

def render_board(board, ximg, oimg):
    global graphical_board
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                graphical_board[i][j][0] = ximg
                graphical_board[i][j][1] = ximg.get_rect(center=(135 + j*174 + 87, 35 + i*174 + 87))
            elif board[i][j] == 'O':
                graphical_board[i][j][0] = oimg
                graphical_board[i][j][1] = oimg.get_rect(center=(135 + j*174 + 87, 35 + i*174 + 87))
    
    # Redraw the entire screen
    SCREEN.fill(BG_COLOR)
    SCREEN.blit(BOARD, (135, 35))
    for i in range(3):
        for j in range(3):
            if graphical_board[i][j][0] is not None:
                SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])
    # Draw buttons on top of the board
    restart_button.draw(SCREEN)
    home_button.draw(SCREEN)

def add_XO(board, graphical_board, to_move):
    current_pos = pygame.mouse.get_pos()
    cell_size = 174
    board_x = 135
    board_y = 35
    
    j = (current_pos[0] - board_x) // cell_size
    i = (current_pos[1] - board_y) // cell_size
    
    if 0 <= i < 3 and 0 <= j < 3:
        if board[i][j] != 'O' and board[i][j] != 'X':
            board[i][j] = to_move
            if to_move == 'O':
                to_move = 'X'
            else:
                to_move = 'O'
            render_board(board, X_IMG, O_IMG)
            pygame.display.update()
            return board, to_move
    return board, to_move

def fade_in_image(image):
    alpha = 0
    for alpha in range(0, 256, 10):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        image.set_alpha(alpha)
        SCREEN.fill(BG_COLOR)
        SCREEN.blit(image, (0, 0))
        # Draw buttons during fade-in
        restart_button.draw(SCREEN)
        home_button.draw(SCREEN)
        pygame.display.update()
        pygame.time.delay(10)

def check_win(board):
    winner = None
    for row in range(0, 3):
        if ((board[row][0] == board[row][1] == board[row][2]) and (board[row][0] is not None)):
            winner = board[row][0]
            pygame.time.delay(500)
            if winner == 'X':
                fade_in_image(X_WIN_IMG)
                WIN_SOUND.play()
                pygame.time.delay(int(WIN_SOUND.get_length() * 1000))
            else:
                fade_in_image(O_WIN_IMG)
                WIN_SOUND.play()
                pygame.time.delay(int(WIN_SOUND.get_length() * 1000))
            pygame.display.update()
            return winner

    for col in range(0, 3):
        if ((board[0][col] == board[1][col] == board[2][col]) and (board[0][col] is not None)):
            winner = board[0][col]
            pygame.time.delay(500)
            if winner == 'X':
                fade_in_image(X_WIN_IMG)
                WIN_SOUND.play()
                pygame.time.delay(int(WIN_SOUND.get_length() * 1000))
            else:
                fade_in_image(O_WIN_IMG)
                WIN_SOUND.play()
                pygame.time.delay(int(WIN_SOUND.get_length() * 1000))
            pygame.display.update()
            return winner

    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):
        winner = board[0][0]
        pygame.time.delay(500)
        if winner == 'X':
            fade_in_image(X_WIN_IMG)
            WIN_SOUND.play()
            pygame.time.delay(int(WIN_SOUND.get_length() * 1000))
        else:
            fade_in_image(O_WIN_IMG)
            WIN_SOUND.play()
            pygame.time.delay(int(WIN_SOUND.get_length() * 1000))
        pygame.display.update()
        return winner

    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None):
        winner = board[0][2]
        pygame.time.delay(500)
        if winner == 'X':
            fade_in_image(X_WIN_IMG)
            WIN_SOUND.play()
            pygame.time.delay(int(WIN_SOUND.get_length() * 1000))
        else:
            fade_in_image(O_WIN_IMG)
            WIN_SOUND.play()
            pygame.time.delay(int(WIN_SOUND.get_length() * 1000))
        pygame.display.update()
        return winner

    if winner is None:
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] != 'X' and board[i][j] != 'O':
                    return None
        pygame.time.delay(500)
        fade_in_image(DRAW_IMG)
        DRAW_SOUND.play()
        pygame.time.delay(int(WIN_SOUND.get_length() * 1000))
        pygame.display.update()
        return "DRAW"

def reset_game():
    global board, graphical_board, to_move, game_finished
    board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    graphical_board = [[[None, None], [None, None], [None, None]], 
                      [[None, None], [None, None], [None, None]], 
                      [[None, None], [None, None], [None, None]]]
    to_move = 'X'
    game_finished = False
    SCREEN.fill(BG_COLOR)
    SCREEN.blit(BOARD, (135, 35))
    pygame.display.update()

def return_to_menu():
    pygame.quit()
    os.system("python menu.py")
    sys.exit()

game_finished = False

# Main loop
mouse_was_pressed = (False, False, False)
while True:
    # Event handling
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_finished:
                board, to_move = add_XO(board, graphical_board, to_move)
                result = check_win(board)
                if result is not None:
                    game_finished = True
            else:
                reset_game()

    # Update buttons
    restart_button.update(mouse_pos, mouse_pressed, mouse_was_pressed)
    home_button.update(mouse_pos, mouse_pressed, mouse_was_pressed)

    # Redraw the entire screen every frame
    render_board(board, X_IMG, O_IMG)
    pygame.display.update()
    mouse_was_pressed = mouse_pressed