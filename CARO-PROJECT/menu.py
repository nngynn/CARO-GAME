import pygame
import sys
import os
import pygame.mixer  # Add this to your imports

# Initialize Pygame mixer
pygame.mixer.init()

# Initialize Pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Caro - Main Menu")
click_sound = pygame.mixer.Sound("assets/click_sound.wav")  # Update the path if necessary

# Load icon
ICON = pygame.image.load("assets/icon.jpg")
pygame.display.set_icon(ICON)

# Colors
BG_COLOR = (0,0,0)  # Background color (teal/cyan)
WHITE = (255, 255, 255)
GRAY = (60, 64, 72)        # Updated: Soft blue-gray for buttons
GRAY_OVER = (100, 104, 112)  # Updated: Mid-tone blue-gray for hover
GRAY_PRESSED = (50, 54, 62)  # Updated: Slightly darker blue-gray for pressed
DARK_BG = (40, 44, 52)     # Updated: Soft dark blue for boxes
OUTLINE_COLOR = (72, 159, 181)

# Fonts
regular_font = pygame.font.Font(None, 36)  # Default font for regular text
bold_font = pygame.font.Font(None, 48)     # Bold font for buttons and title
small_bold_font = pygame.font.Font(None, 40)  # Smaller bold font for longer button text
title_font = pygame.font.Font(None, 100)    # Larger font for "CARO"
close_font = pygame.font.Font(None, 30)    # Font for the "X" button

# Global variables
running = True
show_instructions = False
show_mode = False  # Initialize show_mode to False
selected_mode = None  # Will be "human" or "ai"

# Button class
class Button:
    def __init__(self, x, y, w, h, text, font, text_color, color, over_color, pressed_color, action, arg=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.font = font
        self.text_color = text_color
        self.color = color
        self.over_color = over_color
        self.pressed_color = pressed_color
        self.action = action
        self.arg = arg
        self.is_over = False
        self.is_pressed = False
        self.label = self.font.render(self.text, True, self.text_color)

    def draw(self, screen):
        color = self.color
        if self.is_pressed:
            color = self.pressed_color
        elif self.is_over:
            color = self.over_color
        pygame.draw.rect(screen, color, (self.x, self.y, self.w, self.h), border_radius=10)
        pygame.draw.rect(screen, OUTLINE_COLOR, (self.x, self.y, self.w, self.h), 2, border_radius=10)
        text_rect = self.label.get_rect(center=(self.x + self.w // 2, self.y + self.h // 2))
        screen.blit(self.label, text_rect)

    def update(self, mouse_pos, mouse_pressed, mouse_was_pressed):
        self.is_over = self.x <= mouse_pos[0] <= self.x + self.w and self.y <= mouse_pos[1] <= self.y + self.h
        if self.is_over and mouse_pressed[0] and not mouse_was_pressed[0]:  # Mouse button pressed this frame
            self.is_pressed = True
            click_sound.play()
        elif self.is_pressed and not mouse_pressed[0] and mouse_was_pressed[0]:  # Mouse button released this frame
            self.is_pressed = False
            if callable(self.action):  # Ensure action is callable
                self.action(self.arg)

# Menu functions
def start_game(script_name):
    print(f"Starting game: {script_name}")  # Debug print
    pygame.quit()  # Close the menu window
    os.system(f"python {script_name}")  # Run the game script
    sys.exit()  # Exit the menu script after launching the game

def show_how_to_play(arg):
    global show_instructions, close_button
    show_instructions = not show_instructions
    if show_instructions:
        # Initialize the close button when showing instructions
        box_width, box_height = 680, 300
        box_x, box_y = WIDTH // 2 - box_width // 2, HEIGHT // 2 - box_height // 2
        close_button = Button(box_x + box_width - 40, box_y + 10, 30, 30, "X", close_font, WHITE, GRAY, GRAY_OVER, GRAY_PRESSED, close_instructions, None)
    else:
        close_button = None

def close_instructions(arg):
    global show_instructions, close_button
    show_instructions = False
    close_button = None

def show_mode_selection(arg):
    global show_mode, mode_buttons, close_button
    show_mode = True
    mode_buttons.clear()

    # Box dimensions
    box_width, box_height = 400, 200
    box_x, box_y = WIDTH // 2 - box_width // 2, HEIGHT // 2 - box_height // 2

    # Close button for the mode selection box
    close_button = Button(box_x + box_width - 40, box_y + 10, 30, 30, "X", close_font, WHITE, GRAY, GRAY_OVER, GRAY_PRESSED, close_mode_selection, None)

    # Buttons for 3x3 and 7x7 modes
    mode_buttons.append(Button(box_x + 50, box_y + 80, 120, 50, "3x3", bold_font, WHITE, GRAY, GRAY_OVER, GRAY_PRESSED, start_game, f"3x3_{arg}.py"))
    mode_buttons.append(Button(box_x + 230, box_y + 80, 120, 50, "7x7", bold_font, WHITE, GRAY, GRAY_OVER, GRAY_PRESSED, start_game, f"7x7_{arg}.py"))

def close_mode_selection(arg):
    global show_mode, mode_buttons, close_button
    show_mode = False
    mode_buttons.clear()
    close_button = None

def draw_mode_selection(screen):
    global show_mode, mode_buttons, close_button
    if show_mode:
        # Draw the box
        box_width, box_height = 400, 200
        box_x, box_y = WIDTH // 2 - box_width // 2, HEIGHT // 2 - box_height // 2
        pygame.draw.rect(screen, DARK_BG, (box_x, box_y, box_width, box_height), border_radius=10)
        pygame.draw.rect(screen, OUTLINE_COLOR, (box_x, box_y, box_width, box_height), 2, border_radius=10)

        # Draw the title
        title_text = bold_font.render("Select Mode", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, box_y + 40))
        screen.blit(title_text, title_rect)

        # Draw the buttons
        for button in mode_buttons:
            button.draw(screen)

        # Draw the close button
        if close_button:
            close_button.draw(screen)

def exit_game(arg):
    pygame.quit()
    sys.exit()

# Button list
buttons = []
mode_buttons = []
close_button = None

# Initialize menu
def init_menu():
    global buttons
    buttons.clear()
    
    # Background outline and fill
    buttons.append(Button(WIDTH // 2 - 200, HEIGHT // 2 - 250, 400, 500, "", regular_font, WHITE, OUTLINE_COLOR, OUTLINE_COLOR, OUTLINE_COLOR, lambda x: None))
    buttons.append(Button(WIDTH // 2 - 180, HEIGHT // 2 - 230, 360, 460, "", regular_font, WHITE, DARK_BG, DARK_BG, DARK_BG, lambda x: None))

    # Buttons (adjusted positions to fit the new title layout)
    buttons.append(Button(WIDTH // 2 - 100, HEIGHT // 2 - 60, 210, 60, "Play vs Human", small_bold_font, WHITE, GRAY, GRAY_OVER, GRAY_PRESSED, show_mode_selection, "human"))
    buttons.append(Button(WIDTH // 2 - 100, HEIGHT // 2 + 10, 210, 60, "Play vs AI", bold_font, WHITE, GRAY, GRAY_OVER, GRAY_PRESSED, show_mode_selection, "ai"))
    buttons.append(Button(WIDTH // 2 - 100, HEIGHT // 2 + 80, 210, 60, "How to Play", bold_font, WHITE, GRAY, GRAY_OVER, GRAY_PRESSED, show_how_to_play, None))
    buttons.append(Button(WIDTH // 2 - 100, HEIGHT // 2 + 150, 210, 60, "Exit", bold_font, WHITE, GRAY, GRAY_OVER, GRAY_PRESSED, exit_game, None))
# Instructions
def draw_instructions(screen):
    global show_instructions, close_button  # Declare global at the start of the function
    if show_instructions:
        # Draw a box to cover the background and buttons
        box_width, box_height = 680, 300
        box_x, box_y = WIDTH // 2 - box_width // 2, HEIGHT // 2 - box_height // 2
        pygame.draw.rect(screen, DARK_BG, (box_x, box_y, box_width, box_height+50), border_radius=10)
        pygame.draw.rect(screen, OUTLINE_COLOR, (box_x, box_y, box_width, box_height+50), 2, border_radius=10)

        # Instructions text
        instructions = [
            "How to Play:",
            "1. Play vs Human: Two players alternate 'X' or 'O'.",
            "2. Play vs AI: Play against an AI opponent.",
            "3. Goal: Get 3 in a row to win (3x3); ",
            "4. Goal: Get 5 in a row to win (7x7).",
            "5. Click a cell to place your mark.",
            "6. Click again after win/draw to restart."
        ]
        for i, line in enumerate(instructions):
            text = regular_font.render(line, True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100 + i * 40))
            screen.blit(text, text_rect)

        # Draw the close button if it exists
        if close_button:
            close_button.draw(screen)

# Global variables
running = True
show_instructions = False
selected_mode = None  # Will be "human" or "ai"

# Main loop
init_menu()
mouse_was_pressed = (False, False, False)  # Initialize outside the loop to track previous state
while running:
    SCREEN.fill(BG_COLOR)
    
    # Event handling
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()  # Current mouse state
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the main menu if neither instructions nor mode selection is active
    if not show_instructions and not show_mode:
        # Background outline and fill
        buttons[0].draw(SCREEN)  # Outline
        buttons[1].draw(SCREEN)  # Fill
        # "CARO" title
        main_title = title_font.render("CARO", True, WHITE)
        main_title_rect = main_title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
        SCREEN.blit(main_title, main_title_rect)
        # "CARO!" title
        title = bold_font.render("", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 140))
        SCREEN.blit(title, title_rect)
        # Update and draw interactive buttons
        for button in buttons[2:]:  # Skip the first two (background buttons)
            button.update(mouse_pos, mouse_pressed, mouse_was_pressed)
            button.draw(SCREEN)

    # Draw instructions if active
    if show_instructions:
        draw_instructions(SCREEN)
        if close_button:
            close_button.update(mouse_pos, mouse_pressed, mouse_was_pressed)

    # Draw and update mode selection if active
    if show_mode:
        draw_mode_selection(SCREEN)
        for button in mode_buttons:
            button.update(mouse_pos, mouse_pressed, mouse_was_pressed)
        if close_button:
            close_button.update(mouse_pos, mouse_pressed, mouse_was_pressed)

    pygame.display.update()
    
    # Update previous mouse state for the next frame
    mouse_was_pressed = mouse_pressed

pygame.quit()