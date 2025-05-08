import pygame
import sys
import matplotlib.pyplot as plt
from Model_ALL_Simulation import generate_multitow_layout
import tkinter as tk
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg

# Get screen resolution with Tkinter
root = tk.Tk()
root.withdraw()
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()
root.destroy()

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Tow Simulation Interface")

font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

# UI States
MENU = "menu"
SETTINGS = "settings"
SIMULATION = "simulation"
state = MENU

# Default settings
num_tows = 2
tow_width = 6
tow_length = 100
tow_positions = [(50, 50), (150, 150)]
active_input_field = None
input_text = ""

def generate_multitow_layout_wrapped(num_tows, tow_width, tow_length):
    # Save and override plt.show
    original_show = plt.show
    plt.show = lambda *args, **kwargs: None  # Disable showing

    plt.clf()
    generate_multitow_layout(num_tows, tow_width, tow_length)
    fig = plt.gcf()

    plt.show = original_show  # Restore show
    return fig


def draw_button(text, rect, active=True):
    color = (70, 130, 180) if active else (100, 100, 100)
    pygame.draw.rect(screen, color, rect)
    label = font.render(text, True, (255, 255, 255))
    screen.blit(label, (rect.x + 10, rect.y + 10))

def draw_menu():
    screen.fill((30, 30, 30))
    draw_button("Simulations", pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 100, 200, 50))
    draw_button("Settings", pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 200, 50))
    draw_button("Quit", pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 100, 200, 50))

def draw_settings():
    screen.fill((40, 40, 40))
    settings = [
        ("Number of Tows", num_tows),
        ("Tow Width", tow_width),
        ("Tow Length", tow_length),
    ]

    global field_rects
    field_rects = []  # Store clickable input boxes

    for i, (label_text, value) in enumerate(settings):
        y = 50 + i * 60
        label = font.render(f"{label_text}:", True, (255, 255, 255))
        screen.blit(label, (50, y))

        rect = pygame.Rect(300, y, 200, 40)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2)

        value_str = input_text if active_input_field == i else str(value)
        value_surface = font.render(value_str, True, (255, 255, 255))
        screen.blit(value_surface, (rect.x + 5, rect.y + 5))

        field_rects.append(rect)

    # Tow positions info
    label = font.render(f"Tow Positions: {tow_positions}", True, (255, 255, 255))
    screen.blit(label, (50, y + 70))

    draw_button("Back", pygame.Rect(50, HEIGHT - 70, 100, 40))

def handle_settings_events(event):
    global num_tows, tow_width, tow_length, tow_positions
    global active_input_field, input_text, state

    if event.type == pygame.MOUSEBUTTONDOWN:
        # Check Back button
        back_button_rect = pygame.Rect(50, HEIGHT - 70, 100, 40)
        if back_button_rect.collidepoint(event.pos):
            active_input_field = None
            input_text = ""
            state = MENU
            return

        # Check if user clicked any input field
        for i, rect in enumerate(field_rects):
            if rect.collidepoint(event.pos):
                active_input_field = i
                input_text = ""
                return

    elif event.type == pygame.KEYDOWN and active_input_field is not None:
        if event.key == pygame.K_RETURN:
            try:
                value = int(input_text)
                if active_input_field == 0:
                    num_tows = value
                elif active_input_field == 1:
                    tow_width = value
                elif active_input_field == 2:
                    tow_length = value
                tow_positions = [(i * 60, 100) for i in range(num_tows)]
            except ValueError:
                print("Invalid input")
            active_input_field = None
            input_text = ""
        elif event.key == pygame.K_BACKSPACE:
            input_text = input_text[:-1]
        else:
            char = event.unicode
            if char.isdigit():
                input_text += char

def wait_for_back():
    global state
    back_rect = pygame.Rect(50, HEIGHT - 70, 100, 40)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and back_rect.collidepoint(event.pos):
                state = MENU
                return

def draw_simulation():
    screen.fill((0, 0, 0))  # Clear screen

    # Get the Matplotlib figure
    fig = generate_multitow_layout_wrapped(num_tows, tow_width, tow_length)

    # Render the figure to a buffer (Agg backend)
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    
    # Convert the buffer into a Pygame-compatible image
    buf = canvas.buffer_rgba()  # Buffer contains RGBA data
    width, height = canvas.get_width_height()  # Get figure dimensions

    # Create a Pygame surface from the buffer
    image = pygame.image.frombuffer(buf, (width, height), "RGBA")

    # Optionally, scale the image to fit the screen (optional)
    image = pygame.transform.smoothscale(image, (WIDTH, HEIGHT))  # Resize if necessary

    # Center the image in the Pygame window
    x = (WIDTH - width) // 2
    y = (HEIGHT - height) // 2
    screen.blit(image, (x, y))  # Blit the image to the screen

    # Draw "Back" button
    draw_button("Back", pygame.Rect(50, HEIGHT - 70, 100, 40))

    pygame.display.flip()  # Update the display

    # Wait for user to click "Back"
    wait_for_back()

def main():
    global state
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if state == MENU:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    sim_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 100, 200, 50)
                    settings_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 200, 50)
                    quit_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 100, 200, 50)

                    if sim_rect.collidepoint(event.pos):
                        state = SIMULATION
                        draw_simulation()
                        state = MENU
                    elif settings_rect.collidepoint(event.pos):
                        state = SETTINGS
                    elif quit_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            elif state == SETTINGS:
                handle_settings_events(event)

        # Drawing
        if state == MENU:
            draw_menu()
        elif state == SETTINGS:
            draw_settings()

        pygame.display.flip()
        clock.tick(30)

main()
