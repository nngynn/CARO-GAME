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
board = [[None, None, None], [None, None, None], [None, None, None]]
graphical_board = [[[None, None], [None, None], [None, None]], 
                   [[None, None], [None, None], [None, None]], 
                   [[None, None], [None, None], [None, None]]]

to_move = 'X'
PLAYER = 'X'
AI = 'O'

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
    
    if 0 <= i < 3 and 0 <= j < 3 and board[i][j] is None:
        board[i][j] = to_move
        render_board(board, X_IMG, O_IMG)
        pygame.display.update()
        return True
    return False

def check_win(board):
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            return board[row][0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    
    if all(board[i][j] is not None for i in range(3) for j in range(3)):
        return "DRAW"
    return None

def minimax(board, depth, is_maximizing):
    result = check_win(board)
    if result == AI:
        return 10 - depth
    elif result == PLAYER:
        return -10 + depth
    elif result == "DRAW":
        return 0
    
    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    board[i][j] = AI
                    score = minimax(board, depth + 1, False)
                    board[i][j] = None
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    board[i][j] = PLAYER
                    score = minimax(board, depth + 1, True)
                    board[i][j] = None
                    best_score = min(score, best_score)
        return best_score

def ai_move(board):
    best_score = -float('inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                board[i][j] = AI
                score = minimax(board, 0, False)
                board[i][j] = None
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    if best_move:
        board[best_move[0]][best_move[1]] = AI

def fade_in_image(image):
    alpha = 0
    start_time = pygame.time.get_ticks()
    while alpha < 255:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        elapsed_time = pygame.time.get_ticks() - start_time
        alpha = min(255, elapsed_time * 255 // 250)
        
        image.set_alpha(alpha)
        SCREEN.fill(BG_COLOR)
        SCREEN.blit(image, (0, 0))
        # Draw buttons during fade-in
        restart_button.draw(SCREEN)
        home_button.draw(SCREEN)
        pygame.display.update()
        pygame.time.wait(10)

def reset_game():
    global board, graphical_board, to_move, game_finished, result, result_displayed
    board = [[None, None, None], [None, None, None], [None, None, None]]
    graphical_board = [[[None, None], [None, None], [None, None]], 
                      [[None, None], [None, None], [None, None]], 
                      [[None, None], [None, None], [None, None]]]
    to_move = 'X'
    game_finished = False
    result = None
    result_displayed = False
    SCREEN.fill(BG_COLOR)
    SCREEN.blit(BOARD, (135, 35))
    pygame.display.update()

def return_to_menu():
    pygame.quit()
    os.system("python menu.py")
    sys.exit()

game_finished = False
result = None
result_displayed = False

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
            if not game_finished and to_move == PLAYER:
                if add_XO(board, graphical_board, PLAYER):
                    result = check_win(board)
                    if result:
                        game_finished = True
                        pygame.time.wait(500)
                        if result == "DRAW":
                            fade_in_image(DRAW_IMG)
                            DRAW_SOUND.play()
                            pygame.time.delay(int(WIN_SOUND.get_length() * 1000))
                        elif result == 'X':
                            fade_in_image(X_WIN_IMG)
                            WIN_SOUND.play()
                            pygame.time.delay(int(WIN_SOUND.get_length() * 1000))
                        else:
                            fade_in_image(O_WIN_IMG)
                            WIN_SOUND.play()
                            pygame.time.delay(int(WIN_SOUND.get_length() * 1000))
                        result_displayed = True
                    else:
                        to_move = AI
            elif game_finished:
                reset_game()

    # Update buttons
    restart_button.update(mouse_pos, mouse_pressed, mouse_was_pressed)
    home_button.update(mouse_pos, mouse_pressed, mouse_was_pressed)

    if to_move == AI and not game_finished:
        pygame.time.wait(500)
        ai_move(board)
        render_board(board, X_IMG, O_IMG)
        pygame.display.update()
        result = check_win(board)
        if result:
            game_finished = True
            pygame.time.wait(500)
            if result == "DRAW":
                fade_in_image(DRAW_IMG)
                DRAW_SOUND.play()
                pygame.time.delay(int(WIN_SOUND.get_length() * 1000))
            elif result == 'X':
                fade_in_image(X_WIN_IMG)
                WIN_SOUND.play()
                pygame.time.delay(int(WIN_SOUND.get_length() * 1000))
            else:
                fade_in_image(O_WIN_IMG)
                WIN_SOUND.play()
                pygame.time.delay(int(WIN_SOUND.get_length() * 1000))
            result_displayed = True
        else:
            to_move = PLAYER

    # Redraw the entire screen every frame
    render_board(board, X_IMG, O_IMG)
    pygame.display.update()
    mouse_was_pressed = mouse_pressed