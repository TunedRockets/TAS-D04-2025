"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     This file runs the user interace for simulating tows     ║
║        Please be aware of the units for the inputs!          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""





















import pygame
import sys
import matplotlib.pyplot as plt
import tkinter as tk
import os
from matplotlib.backends.backend_agg import FigureCanvasAgg
import time

# Add the Scripts folder (where the Model_ALL_Simulation module is) to the system path
script_path = os.path.join(os.path.dirname(__file__), 'Scripts')
sys.path.append(script_path)
from Scripts.Model_ALL_Simulation import generate_multitow_layout


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
tow_positions = [(50, 50), (150, 150)]
active_input_field = None
input_text = ""
figure_counter = 1
save_confirmation = False
save_time = None  # Track the time when the save happens
save_duration = 200  # Duration in milliseconds for the green color

# Default settings
num_tows = 2                                    # Unitless
tow_width = 6.35                                # mm
steps_per_mm = 43                               # step/mm
tow_length = 100 * steps_per_mm                 # step
tow_length_mm = int(tow_length / steps_per_mm)  # mm
tow_spacing = 6.35                              # mm

def generate_multitow_layout_wrapped(num_tows, tow_width, tow_length_mm, tow_spacing):
    tow_length = int(tow_length_mm * steps_per_mm)
    # Save and override plt.show
    original_show = plt.show
    plt.show = lambda *args, **kwargs: None  # Disable showing

    plt.clf()
    gap_overlap_df, gap_df, overlap_df, gap_percent, overlap_percent = generate_multitow_layout(num_tows, tow_spacing, tow_width, tow_length)
    fig = plt.gcf()

    plt.show = original_show  # Restore show
    return fig, gap_percent, overlap_percent

def draw_button(text, rect, active=True, green=False):
    color = (70, 130, 180) if active else (100, 100, 100)
    
    # If the save was successful, make the button green for 0.5 seconds
    if green:
        color = (11, 230, 44)  # Green color for confirmation
    
    pygame.draw.rect(screen, color, rect)
    label = font.render(text, True, (255, 255, 255))
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

def draw_menu():
    screen.fill((30, 30, 30))
    button_width, button_height = 200, 50
    button_spacing = 20
    start_y = HEIGHT // 2 - (3 * button_height + 2 * button_spacing) // 2
    buttons = ["Simulation", "Settings", "Quit"]

    for i, label in enumerate(buttons):
        rect = pygame.Rect(WIDTH // 2 - button_width // 2,
                        start_y + i * (button_height + button_spacing),
                        button_width, button_height)
        draw_button(label, rect)

def draw_settings():
    global tow_spacing
    screen.fill((40, 40, 40))
    settings = [
    ("Number of Tows    ", num_tows),
    ("Tow Width     (mm)", tow_width),
    ("Tow Length   (mm)", tow_length_mm),
    ("Tow Spacing (mm)", tow_spacing),
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

    draw_button("Back", pygame.Rect(50, HEIGHT - 70, 100, 40))

def handle_settings_events(event):
    global num_tows, tow_width, tow_length_mm, tow_positions, tow_spacing
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
                value = float(input_text)
                if active_input_field == 0:
                    num_tows = int(value)
                elif active_input_field == 1:
                    tow_width = value
                elif active_input_field == 2:
                    tow_length_mm = int(value)
                elif active_input_field == 3:
                    tow_spacing = float(value)
                tow_positions = [(i * tow_spacing, 100) for i in range(num_tows)]
            except ValueError:
                print("Invalid input")
            active_input_field = None
            input_text = ""
        elif event.key == pygame.K_BACKSPACE:
            input_text = input_text[:-1]
        else:
            char = event.unicode
            if char.isdigit() or (char == '.' and '.' not in input_text):
                input_text += char

def wait_for_back(fig):
    global state, figure_counter, save_confirmation, save_time
    back_rect = pygame.Rect(50, HEIGHT - 70, 100, 40)
    save_rect = pygame.Rect(WIDTH - 150, HEIGHT - 70, 100, 40)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    state = MENU
                    return
                elif save_rect.collidepoint(event.pos):
                    # Ensure the Figures directory exists
                    save_dir = "Figures"
                    os.makedirs(save_dir, exist_ok=True)

                    # Find the next available filename
                    while True:
                        filename = os.path.join(save_dir, f"figure_{figure_counter}.png")
                        if not os.path.exists(filename):
                            break
                        figure_counter += 1

                    # Save the figure
                    fig.savefig(filename)
                    print(f"Saved figure as {filename}")
                    figure_counter += 1

                    # Set save confirmation flag and record the current time for color change
                    save_confirmation = True
                    save_time = pygame.time.get_ticks()  # Get the current time in milliseconds

        # Check if the save time has elapsed, reset color back after 500ms
        if save_confirmation:
            if pygame.time.get_ticks() - save_time > save_duration:
                save_confirmation = False  # Reset the flag after 0.5 seconds

        # Draw the Save button with color change on confirmation
        if save_confirmation:
            draw_button("Save", pygame.Rect(WIDTH - 150, HEIGHT - 70, 100, 40), active=False, green=True)
        else:
            draw_button("Save", pygame.Rect(WIDTH - 150, HEIGHT - 70, 100, 40))

        # Draw the Back button
        draw_button("Back", pygame.Rect(50, HEIGHT - 70, 100, 40))

        pygame.display.flip()  # Update the screen

def draw_simulation():
    screen.fill((0, 0, 0))  # Clear screen

    # Get the Matplotlib figure and values
    fig, gap_percent, overlap_percent = generate_multitow_layout_wrapped(num_tows, tow_width, tow_length_mm, tow_spacing)

    # Render the figure to a buffer (Agg backend)
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    buf = canvas.buffer_rgba()
    width, height = canvas.get_width_height()

    image = pygame.image.frombuffer(buf, (width, height), "RGBA")

    # Calculate the scaling factor to maintain aspect ratio
    aspect_ratio = width / height
    if width > HEIGHT or height > WIDTH:
        if aspect_ratio > 1:
            new_width = min(width, WIDTH)
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = min(height, HEIGHT)
            new_width = int(new_height * aspect_ratio)
        image = pygame.transform.smoothscale(image, (new_width, new_height))
    else:
        new_width, new_height = width, height

    # Center the image
    x = (WIDTH - new_width) // 2
    y = (HEIGHT - new_height) // 2
    screen.blit(image, (x, y))

    # Draw percentages below the image
    info_text = f"Gap %: {gap_percent:.2f}    Overlap %: {overlap_percent:.2f}"
    info_surface = font.render(info_text, True, (255, 255, 255))
    info_rect = info_surface.get_rect(center=(WIDTH // 2, y + new_height + 30))
    screen.blit(info_surface, info_rect)

    # Draw Back button
    draw_button("Back", pygame.Rect(50, HEIGHT - 70, 100, 40))

    # Draw Save button
    draw_button("Save", pygame.Rect(WIDTH - 150, HEIGHT - 70, 100, 40))

    pygame.display.flip()
    wait_for_back(fig)

def draw_loading_screen():
    screen.fill((20, 20, 20))
    loading_text = font.render("Generating simulation...", True, (255, 255, 255))
    loading_rect = loading_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(loading_text, loading_rect)
    pygame.display.flip()

def main():
    global state
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if state == MENU:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    button_width, button_height = 200, 50
                    button_spacing = 20
                    start_y = HEIGHT // 2 - (3 * button_height + 2 * button_spacing) // 2
                    button_labels = ["Simulations", "Settings", "Quit"]

                    for i, label in enumerate(button_labels):
                        rect = pygame.Rect(
                            WIDTH // 2 - button_width // 2,
                            start_y + i * (button_height + button_spacing),
                            button_width,
                            button_height
                        )
                        if rect.collidepoint(event.pos):
                            if label == "Simulations":
                                # Step 2: Draw loading screen
                                screen.fill((0, 0, 0))
                                loading_text = font.render("Loading simulation...", True, (255, 255, 255))
                                loading_rect = loading_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                                screen.blit(loading_text, loading_rect)
                                pygame.display.flip()  # Force update to show loading screen

                                # Continue to simulation
                                state = SIMULATION
                                draw_simulation()
                                state = MENU
                            elif label == "Settings":
                                state = SETTINGS
                            elif label == "Quit":
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