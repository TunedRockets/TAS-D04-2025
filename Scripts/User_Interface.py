import pygame
import sys
import matplotlib.pyplot as plt
from Model_ALL_Simulation import generate_multitow_layout

# Initialize Pygame
pygame.init()

# Get screen resolution
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
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
tow_width = 50
tow_length = 100
tow_positions = [(50, 50), (150, 150)]

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
    instructions = [
        f"Number of Tows: {num_tows}",
        f"Tow Width: {tow_width}",
        f"Tow Length: {tow_length}",
        f"Tow Positions: {tow_positions}",
        "Click to cycle values. Press S to save."
    ]
    for i, text in enumerate(instructions):
        label = font.render(text, True, (255, 255, 255))
        screen.blit(label, (50, 50 + i * 40))
    draw_button("Back", pygame.Rect(50, HEIGHT - 70, 100, 40))

def handle_settings_events(event):
    global num_tows, tow_width, tow_length, tow_positions, state
    if event.type == pygame.MOUSEBUTTONDOWN:
        # Simple cycling logic
        num_tows = (num_tows % 5) + 1
        tow_width += 10
        tow_length += 10
        tow_positions = [(i * 60, 100) for i in range(num_tows)]
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_s:
            print("Settings saved")
    elif event.type == pygame.MOUSEBUTTONDOWN:
        back_button_rect = pygame.Rect(50, HEIGHT - 70, 100, 40)
        if back_button_rect.collidepoint(event.pos):
            state = MENU


def draw_simulation():
    generate_multitow_layout(num_tows, tow_width, tow_length)

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
