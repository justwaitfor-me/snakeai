import pygame
import random
import time
import uuid
import math
from datetime import datetime
from pathlib import Path
from art import *

from player import player
from utils import project, log_error, clear_screen, log_explanations, info, create_video, get_config, draw_element, check_collision, draw_grid, debug

# Load configuration settings from the config
cp, cg, cf, cset = get_config()["project"], get_config()["game"], get_config()["food"], get_config()["settings"]

# Initialize pygame
pygame.init()
uid = uuid.uuid4()
title = cg["title"]
header_height = int(cset["header_height"]) if cset["show_header"] else 0

# Set up the screen dimensions (rounded to nearest 100 for better performance)
screen_width = math.ceil(cg["screen_width"] / 100) * 100
screen_height = math.ceil(cg["screen_height"] / 100) * 100 + header_height
block_size = cg["block_size"]
blocks_x, blocks_y = screen_width // block_size, (screen_height - header_height) // block_size

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(title)

# Fonts setup
font_small = pygame.font.SysFont(None, cg["font_sizes"]["small"])
font_middle = pygame.font.SysFont(None, cg["font_sizes"]["middle"])
font_large = pygame.font.SysFont(None, cg["font_sizes"]["large"])

# Initialize snakes with random starting positions
snakes = [{"color": tuple(snake), "coords": [(random.randint(5, 15), random.randint(5, 15))]} for snake in cg["snakes"]]

# Initialize food positions (spawn range and constraints based on config)
food = [(random.randint(0, blocks_x), random.randint(0, blocks_y)) for _ in range(min(cf["spawn_max"], len(snakes) * cf["per_snake"] + cf["set_count"]))]

# Ensure there are at least the minimum number of food items
while len(food) < cf["spawn_min"]:
    food.append((random.randint(0, blocks_x), random.randint(0, blocks_y)))

running = True
index = 0
error = ""

project(cp)

# Main game loop
while running:
    index += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    
    # Clear the screen and draw grid
    screen.fill(tuple(cg["background_color"]))
    draw_grid(screen, cg, screen_width, block_size, header_height, screen_height)
    debug(screen, cset)
    
    # Show Info if header is active
    if not header_height <= 0:
        # Render the text into an image
        text_uid = font_middle.render(str(uid), True, (255, 255, 255))
        text_datetime = font_small.render(str(datetime.now().strftime("%d.%m.%y %H:%M:%S")), True, (255, 255, 255))
        text_titel = font_large.render(str(title), True, (255, 255, 255))
        text_index = font_small.render(str(index), True, (255, 255, 255))
        
        # Render quit button
        quit_button_rect = pygame.Rect(0, 0, 30, 50)
        quit_text = font_middle.render("Quit", True, (255, 255, 255))

        # Blit the text onto the screen
        screen.blit(text_uid, (5, 5))
        screen.blit(text_datetime, (5, 25))
        screen.blit(text_titel, (5, 45))
        screen.blit(text_index, (5, 80))
        
        # Blit quit Button
        screen.blit(quit_text, (screen_width - 35, 5))
        
        for event in pygame.event.get():
            if quit_button_rect.collidepoint(event.pos):
                running = False
                break

    # Draw the food
    for snack in food:
        draw_element(screen, *snack, (255, 255, 255), block_size, header_height)

    
    # Draw each snake's segments
    for snake in snakes:
        for segment in snake["coords"]:
            draw_element(screen, *segment, snake["color"], block_size, header_height)
            
    # Create info.txt
    if index == 1:
        info(screen, uid, snakes)
        pygame.display.flip()
    
    
    # Check collisions and make moves for each snake
    explanations = []
    for snake in snakes:
        if check_collision(snake, snakes, blocks_x, blocks_y):
            error = "Game Over! A snake collided."
            running = False
            break
        
        try:
            # Get the player's move from the AI or input handler
            out = player(snake, [s for s in snakes if s != snake], food, (blocks_x, blocks_y))
            
            # Wait for a valid move if None was returned
            while out is None:
                time.sleep(0.1)
                out = player(snake, [s for s in snakes if s != snake], food, (blocks_x, blocks_y))
        except Exception as e:
            # Log error if there is an issue with player interaction or move decision
            error = e
            log_error(uid, str(e))
            running = False
            break
        
        # Movement directions mapping
        moves = {"right": (1, 0), "left": (-1, 0), "up": (0, -1), "down": (0, 1)}
        
        # If a valid move is returned, calculate new head position
        if out.get("move") in moves:
            if out.get("explanation"):
                sindex = snakes.index(snake)
                explanations.append([sindex, out])
                print(f"Exp ({index}): {out.get("explanation")}\n")
                
            dx, dy = moves[out["move"]]
            new_head = (snake["coords"][0][0] + dx, snake["coords"][0][1] + dy)
        else:
            error = "Invalid move or movement error"
            running = False
            break
        
        # Update snake's position and remove the last segment to maintain length
        snake["coords"].insert(0, new_head)
        snake["coords"].pop()
        
        # Refresh the screen and handle move delay
        pygame.display.flip()
        time.sleep(cset["move_delay"])
    
    # Log Explanations
    log_explanations(screen, explanations, uid, index)
    
    # Refresh the screen display
    pygame.display.flip()

# After the game loop finishes, create a video of the session
create_video(uid)

# Quit pygame
pygame.quit()

project(cp)
print(f"{error}\n")
print(f"Event Logs: {Path.cwd()}\logs\{uid}\ ")
