import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the game window dimensions
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Silly Adventure Game")

# Set up the clock for controlling the frame rate
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the font for rendering text
FONT_SIZE = 24
font = pygame.font.Font(None, FONT_SIZE)

# Define the game states
INTRO = "intro"
CHOICE1 = "choice1"
FOREST = "forest"
MEADOW = "meadow"
ENCHANTED_LAKE = "enchanted_lake"
TREASURE = "treasure"
ENDING = "ending"
GAME_OVER = "game_over"

# Initialize game state
current_state = INTRO

# Initialize user input variables
user_input = ""

# Initialize feedback messages for each state
feedback = {
    CHOICE1: "",
    FOREST: "",
    MEADOW: "",
    ENCHANTED_LAKE: "",
    TREASURE: "",
}

def render_text(lines, start_y=50, line_spacing=30, feedback_message=""):
    """
    Renders a list of text lines on the screen starting from start_y with specified spacing.
    Optionally displays a feedback message and user input.
    """
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, WHITE)
        window.blit(text_surface, (50, start_y + i * line_spacing))

    if feedback_message:
        feedback_surface = font.render(feedback_message, True, (255, 0, 0))  # Red color for feedback
        window.blit(feedback_surface, (50, start_y + len(lines) * line_spacing + 10))

    # Render user input
    input_surface = font.render(f"> {user_input}", True, WHITE)
    window.blit(input_surface, (50, start_y + (len(lines) + 1) * line_spacing + 10))  # Position below the lines

def introduction():
    """
    Displays the introduction scene.
    """
    global current_state
    lines = [
        "Welcome to the Silly Adventure!",
        "You are Monty Python, the chosen hero destined to find the legendary Holy Necklace.",
        "But beware, the path is filled with nonsensical dangers and absurd challenges!",
        "",
        "Press ENTER to start your adventure..."
    ]
    render_text(lines, start_y=50, line_spacing=30)

def first_choice():
    """
    Presents the first choice to the player.
    """
    global current_state
    lines = [
        "You stand at a crossroads. Do you:",
        "1. Take the path into the dark, spooky forest.",
        "2. Walk towards the bright, sunny meadow filled with butterflies.",
        "",
        "Enter 1 or 2:"
    ]
    render_text(lines, start_y=50, line_spacing=30, feedback_message=feedback[CHOICE1])

def spooky_forest():
    """
    Handles the spooky forest path.
    """
    global current_state
    lines = [
        "You bravely enter the dark forest.",
        "A talking tree approaches you and asks for the magic word of politeness.",
        "Enter the password:"
    ]
    render_text(lines, start_y=50, line_spacing=30, feedback_message=feedback[FOREST])

def sunny_meadow():
    """
    Handles the sunny meadow path.
    """
    global current_state
    lines = [
        "You skip happily into the meadow.",
        "A giant butterfly offers you a ride. Do you accept?",
        "1. Yes",
        "2. No",
        "",
        "Enter 1 or 2:"
    ]
    render_text(lines, start_y=50, line_spacing=30, feedback_message=feedback[MEADOW])

def enchanted_lake():
    """
    Handles the enchanted lake path.
    """
    global current_state
    lines = [
        "You fly on the giant butterfly and arrive at the Enchanted Lake.",
        "A fairy appears and presents you with a riddle:",
        "'I fly without wings, I cry without eyes. Whenever I go, darkness flies.'",
        "What am I?",
        "Enter your answer:"
    ]
    render_text(lines, start_y=50, line_spacing=30, feedback_message=feedback[ENCHANTED_LAKE])

def treasure_room():
    """
    Presents the treasure room and final challenge.
    """
    global current_state
    lines = [
        "You've found the secret treasure room!",
        "In the center, you see the Holy Necklace perched on a pedestal.",
        "As you approach, a voice asks, 'What is the airspeed velocity of an unladen swallow?'",
        "(Hint: Think about the origin of the question!)",
        "Enter your answer:"
    ]
    render_text(lines, start_y=50, line_spacing=30, feedback_message=feedback[TREASURE])

def ending():
    """
    Displays the game ending.
    """
    global current_state
    lines = [
        "Congratulations! You've obtained the Holy Necklace!",
        "With it, you bring laughter to the entire world.",
        "As a reward, you are crowned the Supreme Leader of Silly Walks.",
        "You live happily ever after in a world filled with giggles and guffaws!",
        "",
        "*** THE END ***"
    ]
    render_text(lines, start_y=50, line_spacing=30)

def game_over(message):
    """
    Displays a game over message.
    """
    global current_state
    lines = [
        f"Game Over! {message}",
        "",
        "Press ENTER to exit the game."
    ]
    render_text(lines, start_y=50, line_spacing=30)

def handle_input():
    """
    Processes the user input based on the current state.
    """
    global current_state, user_input, feedback

    if current_state == INTRO:
        # Enter key pressed in INTRO state
        first_choice()
        current_state = CHOICE1  # Transition to CHOICE1 state
        user_input = ""
        feedback[CHOICE1] = ""  # Clear any previous feedback

    elif current_state == CHOICE1:
        if user_input == "1":
            spooky_forest()
            current_state = FOREST
            feedback[FOREST] = ""  # Clear feedback for FOREST
        elif user_input == "2":
            sunny_meadow()
            current_state = MEADOW
            feedback[MEADOW] = ""  # Clear feedback for MEADOW
        else:
            feedback[CHOICE1] = "Invalid choice. Please enter 1 or 2."
        user_input = ""

    elif current_state == FOREST:
        if user_input.lower() == "please":
            treasure_room()
            current_state = TREASURE
            feedback[TREASURE] = ""  # Clear feedback for TREASURE
        else:
            feedback[FOREST] = "Incorrect password. Please try again."
        user_input = ""

    elif current_state == MEADOW:
        if user_input == "1":
            enchanted_lake()
            current_state = ENCHANTED_LAKE
            feedback[ENCHANTED_LAKE] = ""  # Clear feedback for ENCHANTED_LAKE
        elif user_input == "2":
            # Return to the crossroads
            first_choice()
            current_state = CHOICE1
            feedback[CHOICE1] = ""  # Clear feedback for CHOICE1
        else:
            feedback[MEADOW] = "Invalid choice. Please enter 1 or 2."
        user_input = ""

    elif current_state == ENCHANTED_LAKE:
        if user_input.lower() == "cloud":
            treasure_room()
            current_state = TREASURE
            feedback[TREASURE] = ""  # Clear feedback for TREASURE
        else:
            feedback[ENCHANTED_LAKE] = "Incorrect answer. Please try again."
        user_input = ""

    elif current_state == TREASURE:
        if "african or european" in user_input.lower():
            ending()
            current_state = ENDING
        else:
            feedback[TREASURE] = "Incorrect answer. Please try again."
        user_input = ""

def clear_screen():
    """
    Clears the game window by filling it with black color.
    """
    window.fill(BLACK)

def update_display():
    """
    Updates the entire display.
    """
    pygame.display.flip()

def main():
    global user_input

    # Start with the introduction
    introduction()

    while True:
        clear_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if current_state == GAME_OVER:
                        pygame.quit()
                        sys.exit()
                    else:
                        handle_input()
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    if current_state in [CHOICE1, FOREST, MEADOW, ENCHANTED_LAKE, TREASURE]:
                        if event.unicode.isalnum() or event.unicode in [" ", "?", "."]:
                            user_input += event.unicode

        # Render current state
        if current_state == INTRO:
            introduction()
        elif current_state == CHOICE1:
            first_choice()
        elif current_state == FOREST:
            spooky_forest()
        elif current_state == MEADOW:
            sunny_meadow()
        elif current_state == ENCHANTED_LAKE:
            enchanted_lake()
        elif current_state == TREASURE:
            treasure_room()
        elif current_state == ENDING:
            ending()
        elif current_state == GAME_OVER:
            game_over("You have failed your quest.")
        
        update_display()
        clock.tick(30)  # Limit the frame rate to 30 FPS

if __name__ == "__main__":
    main()
