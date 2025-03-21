import pygame
import sys
import random
import os

pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CARO!")

# Load images
ICON = pygame.image.load("assets/icon.jpg")
pygame.display.set_icon(ICON)

BOARD = pygame.image.load("assets/board1.png")
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
CLICK_SOUND = pygame.mixer.Sound("assets/click_sound.wav")

# Scale images
CELL_SIZE = 540 // 7
IMG_SIZE = 60
X_IMG = pygame.transform.smoothscale(X_IMG, (IMG_SIZE, IMG_SIZE))
O_IMG = pygame.transform.smoothscale(O_IMG, (IMG_SIZE, IMG_SIZE))

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
            CLICK_SOUND.play()
            self.action(self.arg)

# Game state
board = [[None for _ in range(7)] for _ in range(7)]
graphical_board = [[[None, None] for _ in range(7)] for _ in range(7)]

to_move = 'X'  # Human starts as X

# Initialize buttons
restart_button = Button(WIDTH - 120, 10, RESTART_IMG, lambda _: reset_game())
home_button = Button(WIDTH - 60, 10, HOME_IMG, lambda _: return_to_menu())

SCREEN.fill(BG_COLOR)
SCREEN.blit(BOARD, (130, 30))
pygame.display.update()

def render_board(board, ximg, oimg):
    global graphical_board
    for i in range(7):
        for j in range(7):
            if board[i][j] == 'X':
                graphical_board[i][j][0] = ximg
                graphical_board[i][j][1] = ximg.get_rect(center=(130 + j*CELL_SIZE + CELL_SIZE//2, 30 + i*CELL_SIZE + CELL_SIZE//2))
            elif board[i][j] == 'O':
                graphical_board[i][j][0] = oimg
                graphical_board[i][j][1] = oimg.get_rect(center=(130 + j*CELL_SIZE + CELL_SIZE//2, 30 + i*CELL_SIZE + CELL_SIZE//2))

    SCREEN.fill(BG_COLOR)
    SCREEN.blit(BOARD, (130, 30))
    for i in range(7):
        for j in range(7):
            if graphical_board[i][j][0] is not None:
                SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])
    restart_button.draw(SCREEN)
    home_button.draw(SCREEN)

def add_X(board, graphical_board):
    current_pos = pygame.mouse.get_pos()
    board_x = 130
    board_y = 30

    j = (current_pos[0] - board_x) // CELL_SIZE
    i = (current_pos[1] - board_y) // CELL_SIZE
    
    if 0 <= i < 7 and 0 <= j < 7 and board[i][j] is None:
        board[i][j] = 'X'
        render_board(board, X_IMG, O_IMG)
        pygame.display.update()
        return True
    return False

def ai_move(board):
    # Check for winning move for O
    for i in range(7):
        for j in range(7):
            if board[i][j] is None:
                board[i][j] = 'O'
                if check_win(board, 'O'):
                    return
                board[i][j] = None

    # Block X from winning
    for i in range(7):
        for j in range(7):
            if board[i][j] is None:
                board[i][j] = 'X'
                if check_win(board, 'X'):
                    board[i][j] = 'O'
                    return
                board[i][j] = None

    # Otherwise, make a random move
    empty_cells = [(i, j) for i in range(7) for j in range(7) if board[i][j] is None]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = 'O'

def check_win(board, player):
    for i in range(7):
        for j in range(3):
            if all(board[i][j + k] == player for k in range(5)):
                return True

    for j in range(7):
        for i in range(3):
            if all(board[i + k][j] == player for k in range(5)):
                return True

    for i in range(3):
        for j in range(3):
            if all(board[i + k][j + k] == player for k in range(5)):
                return True

    for i in range(4, 7):
        for j in range(3):
            if all(board[i - k][j + k] == player for k in range(5)):
                return True
    return False

def check_draw(board):
    return all(board[i][j] is not None for i in range(7) for j in range(7))

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
        restart_button.draw(SCREEN)
        home_button.draw(SCREEN)
        pygame.display.update()
        pygame.time.delay(10)

def reset_game():
    global board, graphical_board, game_finished, to_move
    board = [[None for _ in range(7)] for _ in range(7)]
    graphical_board = [[[None, None] for _ in range(7)] for _ in range(7)]
    to_move = 'X'
    game_finished = False
    SCREEN.fill(BG_COLOR)
    SCREEN.blit(BOARD, (130, 30))
    pygame.display.update()

def return_to_menu():
    pygame.quit()
    os.system("python menu.py")
    sys.exit()

game_finished = False

# Main loop
mouse_was_pressed = (False, False, False)
ai_thinking = False
ai_think_start = 0
AI_THINK_DURATION = 500  # 500ms delay for AI thinking

while True:
    # Event handling
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_finished and not ai_thinking:
                if add_X(board, graphical_board):
                    if check_win(board, 'X'):
                        pygame.time.delay(500)
                        fade_in_image(X_WIN_IMG)
                        WIN_SOUND.play()
                        pygame.time.delay(int(WIN_SOUND.get_length() * 1000))
                        game_finished = True
                    elif check_draw(board):
                        pygame.time.delay(500)
                        fade_in_image(DRAW_IMG)
                        DRAW_SOUND.play()
                        pygame.time.delay(int(WIN_SOUND.get_length() * 1000))
                        game_finished = True
                    else:
                        ai_thinking = True
                        ai_think_start = pygame.time.get_ticks()
            elif game_finished:
                reset_game()

    # Update buttons
    restart_button.update(mouse_pos, mouse_pressed, mouse_was_pressed)
    home_button.update(mouse_pos, mouse_pressed, mouse_was_pressed)

    # Handle AI thinking
    if ai_thinking:
        if pygame.time.get_ticks() - ai_think_start >= AI_THINK_DURATION:
            ai_move(board)
            render_board(board, X_IMG, O_IMG)
            pygame.display.update()
            if check_win(board, 'O'):
                pygame.time.delay(500)
                fade_in_image(O_WIN_IMG)
                WIN_SOUND.play()
                pygame.time.delay(int(WIN_SOUND.get_length() * 1000))
                game_finished = True
            elif check_draw(board):
                pygame.time.delay(500)
                fade_in_image(DRAW_IMG)
                DRAW_SOUND.play()
                pygame.time.delay(int(WIN_SOUND.get_length() * 1000))
                game_finished = True
            ai_thinking = False

    # Redraw the entire screen every frame
    render_board(board, X_IMG, O_IMG)
    pygame.display.update()
    mouse_was_pressed = mouse_pressed