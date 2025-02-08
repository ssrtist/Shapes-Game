import sys
import pygame
import random

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()

# Game variables
min_num_choices = 1 # Maximum number of choices
max_num_choices = 5 # Maximum number of choices
num_choices = 2 # Customizable number of choices

shape_items = {}
shape_items = {
    "triangle": { 
        "value" : "triangle",
        "sound" : pygame.mixer.Sound("assets/triangle.wav"),
        "toggle" : False
    },
    "square": { 
        "value" : "square",
        "sound" : pygame.mixer.Sound("assets/square.wav"),
        "toggle" : True
    },
    "circle": { 
        "value" : "circle",
        "sound" : pygame.mixer.Sound("assets/circle.wav"),
        "toggle" : True
    },
    # "star": { 
    #     "value" : "star",
    #     "sound" : pygame.mixer.Sound("assets/star.wav"),
    #     "toggle" : False
    # },
    "oval": { 
        "value" : "oval",
        "sound" : pygame.mixer.Sound("assets/oval.wav"),
        "toggle" : False
    },
    "rectangle": {
         "value" : "rectangle",
         "sound" : pygame.mixer.Sound("assets/rectangle.wav"),
         "toggle" : True
     },
    "line": { 
        "value" : "line",
        "sound" : pygame.mixer.Sound("assets/line.wav"),
        "toggle" : False
    }
}

shape_names = list(shape_items.keys())

# Screen dimensions
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Selection Game")

# Fonts
font = pygame.font.Font(None, 74)
big_font = pygame.font.Font(None, 96)
button_font = pygame.font.Font(None, 50)
score_font = pygame.font.Font(None, 50)

# Sound effects
pygame.mixer.init()
sounds = {}
title_sound = pygame.mixer.Sound("assets/title.wav")    
select_sound = pygame.mixer.Sound("assets/select.wav")  
correct_sound = pygame.mixer.Sound("assets/right.wav")  
wrong_sound = pygame.mixer.Sound("assets/wrong.wav")      
well_done_sound = pygame.mixer.Sound("assets/well_done.wav")
click_sound = pygame.mixer.Sound("assets/mouse_click.wav")

# Emojis
happy_face = pygame.image.load("assets/happy_face.png") 
sad_face = pygame.image.load("assets/red_sad_face.png")     
happy_face = pygame.transform.scale(happy_face, (200, 200))  
sad_face = pygame.transform.scale(sad_face, (200, 200))      

# square_size = 150
square_size = WIDTH // max_num_choices - 10  # Square size based on max number of choices
score = 0
target_score = 10
game_over = False

# Function to draw shapes from center point
def draw_shape(center, shape, size):
    x, y = center
    border_width = 4

    if shape == "rectangle":
        myshape = pygame.draw.rect(screen, "cyan", (x - size // 2, y - size // 4, size, size // 2), border_width)
    elif shape == "circle":
        myshape = pygame.draw.circle(screen, "cyan", center, size // 2, border_width)
    elif shape == "triangle":
        myshape = pygame.draw.polygon(screen, "cyan", [
            (x, y - size // 2),
            (x + size // 2, y + size // 2),
            (x - size // 2, y + size // 2)
        ], border_width)
    elif shape == "square":
        myshape = pygame.draw.rect(screen, "cyan", (x - size // 2, y - size // 2, size, size), border_width)
    elif shape == "oval":
        myshape = pygame.draw.ellipse(screen, "cyan", (x - size, y - size // 2, size * 2, size), border_width)
    elif shape == "line":
        myshape = pygame.draw.line(screen, "cyan", (x - size // 2, y), (x + size // 2, y), 5)
    return myshape

def options_screen():
    global num_choices, toggles

    # Draw checkboxes
    opt_rect = {}
    opt_size = 50
    opt_width = 4
    opt_x = (WIDTH - opt_size * 2 * len(shape_names)) // 2
    opt_y = HEIGHT // 2 + 100

    # Event handling for options screen
    waiting = True
    while waiting:
        screen.fill((128, 128, 128))  # Grey background
        title_text = font.render("Options", True, (0, 0, 0))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
        # Display the current number of choices
        choices_text = button_font.render(f"Number of choices: {num_choices}", True, "white")
        screen.blit(choices_text, (WIDTH // 2 - choices_text.get_width() // 2, HEIGHT * 2 // 5 - 50))
        # Draw "+" button
        button_width, button_height = 50, 50
        plus_button_x = WIDTH // 2 - button_width // 2 + 50
        plus_button_y = HEIGHT * 2 // 5
        plus_button_rect = pygame.Rect(plus_button_x, plus_button_y, button_width, button_height)
        plus_button_text = button_font.render("+", True, (255, 255, 255))
        pygame.draw.rect(screen, (0, 128, 0), plus_button_rect)  # Green button
        screen.blit(plus_button_text, (plus_button_x + 20, plus_button_y + 10))
        # Draw "-" button
        minus_button_x = WIDTH // 2 - button_width // 2 - 50
        minus_button_y = HEIGHT * 2 // 5
        minus_button_rect = pygame.Rect(minus_button_x, minus_button_y, button_width, button_height)
        minus_button_text = button_font.render("-", True, (255, 255, 255))
        pygame.draw.rect(screen, (128, 0, 0), minus_button_rect)  # Red button
        screen.blit(minus_button_text, (minus_button_x + 20, minus_button_y + 10))

        # Color checkboxes
        choices_text = button_font.render("Available shapes: ", True, "white")
        screen.blit(choices_text, (WIDTH // 2 - choices_text.get_width() // 2, HEIGHT // 2 + 50))

        # Draw "OK" button
        button_width, button_height = 200, 50
        quit_button_x = WIDTH // 2 - button_width // 2
        quit_button_y = HEIGHT // 2 + 50 + 200
        quit_button_rect = pygame.Rect(quit_button_x, quit_button_y, button_width, button_height)
        quit_button_text = button_font.render("OK", True, (255, 255, 255))
        pygame.draw.rect(screen, (0, 128, 0), quit_button_rect)  # Green button
        screen.blit(quit_button_text, (quit_button_x + 20, quit_button_y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Return to the title screen
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if plus_button_rect.collidepoint(x, y):
                    # Increase the number of choices
                    click_sound.play()
                    num_choices = min(num_choices + 1, max_num_choices)
                if minus_button_rect.collidepoint(x, y):
                    # Decrease the number of choices
                    click_sound.play()
                    num_choices = max(num_choices - 1, 2)
                for acolor in shape_names:
                    if opt_rect[acolor].collidepoint(x, y):
                        click_sound.play()
                        shape_items[acolor]["toggle"] = not shape_items[acolor]["toggle"]
                        num_available_colors = sum(1 for item in shape_items.values() if item["toggle"])
                        if num_available_colors < num_choices:
                            shape_items[acolor]["toggle"] = not shape_items[acolor]["toggle"]
                if quit_button_rect.collidepoint(x, y):
                    # Return to the title screen
                    click_sound.play()
                    return

        # Draw options shapes
        i = 0
        for ashape in shape_names:
            opt_rect[ashape] = pygame.Rect(i * opt_size * 2 + opt_x, opt_y + 60, opt_size, opt_size)
            pygame.draw.rect(screen, "white", opt_rect[ashape], opt_width)
            if shape_items[ashape]["toggle"]:
                # draw smaller box
                pygame.draw.rect(screen, "orange", opt_rect[ashape].inflate(-16, -16))
            draw_shape((i * opt_size * 2 + opt_x + 25, opt_y + 20), ashape, 50)
            i += 1

        pygame.display.flip()
        clock.tick(30)
#
def title_screen():
    global running

    # Event handling for title screen
    waiting = True
    while waiting:
        # Display the title screen
        screen.fill((128, 128, 128))  # Grey background
        title_text = font.render("Color Selection Game", True, (0, 0, 0))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 50))

        # Draw "Start" button
        button_width, button_height = 200, 50
        start_button_x = WIDTH // 2 - button_width // 2
        start_button_y = HEIGHT // 2 + 50
        start_button_rect = pygame.Rect(start_button_x, start_button_y, button_width, button_height)
        start_button_text = button_font.render("Start", True, (255, 255, 255))
        pygame.draw.rect(screen, (0, 128, 0), start_button_rect)  # Green button
        screen.blit(start_button_text, (start_button_x + 20, start_button_y + 10))

        # Draw "Options" button
        option_button_x = WIDTH // 2 - button_width // 2
        option_button_y = HEIGHT // 2 + 50 + 75
        option_button_rect = pygame.Rect(option_button_x, option_button_y, button_width, button_height)
        option_button_text = button_font.render("Options", True, (255, 255, 255))
        pygame.draw.rect(screen, (0, 128, 0), option_button_rect)  # Green button
        screen.blit(option_button_text, (option_button_x + 20, option_button_y + 10))

        # Draw "Quit" button
        quit_button_x = WIDTH // 2 - button_width // 2
        quit_button_y = HEIGHT // 2 + 50 + 150
        quit_button_rect = pygame.Rect(quit_button_x, quit_button_y, button_width, button_height)
        quit_button_text = button_font.render("Quit", True, (255, 255, 255))
        pygame.draw.rect(screen, (128, 0, 0), quit_button_rect)  # Green button
        screen.blit(quit_button_text, (quit_button_x + 20, quit_button_y + 10))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if start_button_rect.collidepoint(x, y):
                    # Proceed to the next round
                    click_sound.play()
                    return True
                if option_button_rect.collidepoint(x, y):
                    # Switch to options screen
                    click_sound.play()
                    options_screen()
                if quit_button_rect.collidepoint(x, y):
                    click_sound.play()
                    pygame.quit()
                    sys.exit()
        clock.tick(30)
# 
def draw_screen():
    global correct_shape, all_shapes, square_positions, result, show_next_button, all_shape_rects
    screen.fill((128, 128, 128))  # Grey background

    # Display the score
    score_text = score_font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (20, 20))

    # Display the title text
    game_text = font.render(f"Find {correct_shape.capitalize()}", True, "black")
    game_rect = pygame.Rect(WIDTH // 2 - game_text.get_width() // 2 - 2, 50 - 2, game_text.get_width() + 4, game_text.get_height() + 4)
    pygame.draw.rect(screen, "gold", game_rect.inflate(0, 0))
    screen.blit(game_text, (WIDTH // 2 - game_text.get_width() // 2, 50))
    # Draw title text background
    if result is not None:
        pygame.draw.rect(screen, "brown", (highlight_x - 10, highlight_y - 10, square_size + 20, square_size + 20),5)    
        
    # Draw the squares
    all_shape_rects = []
    for i, pos in enumerate(square_positions):
        # pygame.draw.rect(screen, "red", (*pos, square_size, square_size))
        all_shape_rects += [draw_shape((pos[0] + square_size // 2, pos[1] + square_size // 2), all_shapes[i], square_size)]


    # Display result
    if result is not None:
        result_text = big_font.render(result, True, pygame.Color("green" if result == "RIGHT !" else "red"))
        screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT - HEIGHT // 9))
        # Display emoji based on result
        if result == "RIGHT !":
            screen.blit(happy_face, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
        else:
            screen.blit(sad_face, (WIDTH // 2 - 100, HEIGHT // 2 + 50))

    # Draw the "Next" button if the round is over
    if show_next_button and not game_over:
        pygame.draw.rect(screen, (0, 128, 0), next_button_rect)  # Green button
        screen.blit(next_button_text, (next_button_x + 20, next_button_y + 10))

    # Draw the "Quit" button
    if not game_over:
        pygame.draw.rect(screen, (255, 0, 0), quit_button_rect)  # Red button
        screen.blit(quit_button_text, (quit_button_x + 20, quit_button_y + 10))

    # Update the display
    pygame.display.flip()

    # Play sounds
    # if not show_next_button:
    if result is None:
        pygame.time.delay(250)  # Delay for 1 second
        title_sound.play()  # Play title sound at the beginning of each round
        pygame.time.delay(500)
        shape_items[correct_shape]["sound"].play()  # Play correct color sound at the title screen
    return game_rect

# Function to generate square positions dynamically
def generate_square_positions(num_choices):
    positions = []
    # Dynamic layout for numbers of choices
    spacing = WIDTH // num_choices - square_size
    total_width = num_choices * square_size + (num_choices - 1) * spacing
    start_x = (WIDTH - total_width) // 2
    start_y = HEIGHT // 2 - square_size
    for i in range(num_choices):
        x = start_x + i * (square_size + spacing)
        y = start_y
        positions.append((x, y))
    return positions

# Function to generate squares with only one correct choice
def generate_squares(num_choices):
    really_available_colors = [c for c in shape_names if shape_items[c]["toggle"]]
    correct_shape = random.choice(really_available_colors)
    # Ensure the correct color is only present once
    incorrect_colors = random.sample([c for c in really_available_colors if c != correct_shape], num_choices - 1)  # Pick incorrect colors
    all_shapes = incorrect_colors + [correct_shape]  # Combine incorrect and correct colors
    random.shuffle(all_shapes)  # Shuffle to randomize positions
    return correct_shape, all_shapes

# Button variables
button_width, button_height = 200, 50

# "Next" button
next_button_x = WIDTH - button_width - 20
next_button_y = HEIGHT - button_height - 20
next_button_rect = pygame.Rect(next_button_x, next_button_y, button_width, button_height)
next_button_text = button_font.render("Next", True, (255, 255, 255))

# "Quit" button
quit_button_x = WIDTH - button_width - 20
quit_button_y = 20
quit_button_rect = pygame.Rect(quit_button_x, quit_button_y, button_width, button_height)
quit_button_text = button_font.render("Quit", True, (255, 255, 255))

# "New Game" and "Exit Game" buttons
new_game_button_rect = pygame.Rect(WIDTH // 2 - button_width - 10, HEIGHT // 2 + 50, button_width, button_height)
new_game_button_text = button_font.render("New Game", True, (255, 255, 255))
exit_game_button_rect = pygame.Rect(WIDTH // 2 + 10, HEIGHT // 2 + 50, button_width, button_height)
exit_game_button_text = button_font.render("Exit Game", True, (255, 255, 255))

# Display the title screen 
title_screen()

# Main game loop
new_screen = True
running = True
result = None
show_next_button = False
highlight_x, highlight_y = 0, 0
all_shape_rects = []

# Initialize the first question
square_positions = generate_square_positions(num_choices)
correct_shape, all_shapes = generate_squares(num_choices)

# Clear any lingering events
pygame.event.clear()  

while running:
    if new_screen:
        find_color_rect = draw_screen()
        new_screen = False
    if game_over:
        pygame.time.delay(1000)  # Delay for 1 second
        screen.fill((128, 128, 128))  # Grey background
        well_done_text = font.render("Well Done!", True, pygame.color.Color("gold"))
        screen.blit(well_done_text, (WIDTH // 2 - well_done_text.get_width() // 2, HEIGHT // 2 - 50))
        well_done_sound.play()  # Play well done sound
        # Draw "New Game" and "Exit Game" buttons
        pygame.draw.rect(screen, (0, 128, 0), new_game_button_rect)  # Green button
        screen.blit(new_game_button_text, (new_game_button_rect.x + 10, new_game_button_rect.y + 10))
        pygame.draw.rect(screen, (255, 0, 0), exit_game_button_rect)  # Red button
        screen.blit(exit_game_button_text, (exit_game_button_rect.x + 10, exit_game_button_rect.y + 10))
        pygame.display.flip()

        # Event handling for game over screen
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if new_game_button_rect.collidepoint(x, y):
                        # Reset the game
                        click_sound.play()
                        result = None
                        score = 0
                        game_over = False
                        correct_shape, all_shapes = generate_squares(num_choices)
                        show_next_button = False
                        waiting = False
                    elif exit_game_button_rect.collidepoint(x, y):
                        click_sound.play()
                        running = False  # Exit the game
                        waiting = False

        # pygame.display.flip()
        new_screen = True
        continue

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if show_next_button and next_button_rect.collidepoint(x, y):
                # Proceed to the next round
                click_sound.play()
                show_next_button = False
                result = None
                correct_shape, all_shapes = generate_squares(num_choices)
                screen.fill((128, 128, 128))  # Grey background
                new_screen = True
            elif quit_button_rect.collidepoint(x, y):
                click_sound.play()
                running = False  # Quit the game
            elif not show_next_button:
                # for i, pos in enumerate(all_shape_rects):
                #     if pos.collidepoint(x, y):
                #         if all_shapes[i] == correct_shape:
                #             result = "RIGHT !"
                #             correct_sound.play()  # Play correct sound effect
                #             show_next_button = True
                #             score += 1  # Increase score
                #             if score >= target_score:
                #                 game_over = True
                #             if show_next_button and not game_over:
                #                 pygame.draw.rect(screen, (0, 128, 0), next_button_rect)  # Green button
                #                 screen.blit(next_button_text, (next_button_x + 20, next_button_y + 10))
                #                 pygame.display.flip()
                #         else:
                #             result = "WRONG !"
                #             wrong_sound.play()  # Play wrong sound effect
                #             show_next_button = False
                #         break
                for i, pos in enumerate(square_positions):
                    if pos[0] <= x <= pos[0] + square_size and pos[1] <= y <= pos[1] + square_size:
                        highlight_x, highlight_y = pos
                        if all_shapes[i] == correct_shape:
                            result = "RIGHT !"
                            correct_sound.play()  # Play correct sound effect
                            show_next_button = True
                            score += 1  # Increase score
                            if score >= target_score:
                                game_over = True
                            if show_next_button and not game_over:
                                pygame.draw.rect(screen, (0, 128, 0), next_button_rect)  # Green button
                                screen.blit(next_button_text, (next_button_x + 20, next_button_y + 10))
                                pygame.display.flip()
                        else:
                            result = "WRONG !"
                            wrong_sound.play()  # Play wrong sound effect
                            show_next_button = False
                        break
                new_screen = True
    clock.tick(30)

# Quit pygame
pygame.quit()
