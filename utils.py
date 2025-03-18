import os
import json
import re
import glob
import yaml
import cv2
import pygame
import random
from art import *
from dotenv import load_dotenv
from datetime import datetime
from typing import Dict, List, Tuple

def get_config() -> Dict:
    """Loads the configuration file."""
    with open('conf.yml', 'r') as file:
        return yaml.safe_load(file)
    
def clear_screen() -> None:
    """Clear Terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
def project(project: dict) -> None:
    """Prints start screen and ascii art"""
    clear_screen()
    tprint(project["name"])
    print(project["version"])
    print(f"Author: {project["author"]}")
    print("#"*int(os.get_terminal_size().columns))
    print("\n")
    

def draw_grid(screen: pygame.Surface, cg: Dict[str, Tuple[int, int, int]], screen_width: int, block_size: int, header_height: int, screen_height: int) -> None:
    """Draws a grid on the screen."""
    for x in range(0, screen_width, block_size):
        for y in range(header_height, screen_height, block_size):
            rect = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(screen, tuple(cg["grid_color"]), rect, 1)  # Light gray grid lines

def debug(screen: pygame.Surface, cset: Dict[str, bool]) -> None:
    """Draws random-colored squares for debugging purposes."""
    if cset["debug_mode"]:
        for x in range(20):
            pygame.draw.rect(screen, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (x * 20, x * 20, 20, 20))

def check_collision(snake: Dict[str, List[Tuple[int, int]]], snakes: List[Dict[str, List[Tuple[int, int]]]], blocks_x: int, blocks_y: int) -> bool:
    """Checks for collisions with the walls, itself, or other snakes."""
    head = snake["coords"][0]
    return (
        head[0] < 0 or head[0] >= blocks_x or head[1] < 0 or head[1] >= blocks_y or
        head in snake["coords"][1:] or
        any(head in other_snake["coords"] for other_snake in snakes if other_snake != snake)
    )

def draw_element(screen: pygame.Surface, x: int, y: int, color: Tuple[int, int, int], block_size: int, header_height: int) -> None:
    """Draws an element (snake, food, etc.) on the screen."""
    pygame.draw.rect(screen, color, (x * block_size, y * block_size + header_height, block_size, block_size))

def read_file(path: str) -> str:
    """Reads a file and returns its content."""
    with open(path, "r") as file:
        return file.read()

def build_prompt(snake: List[Tuple[int, int]], opp_snake: List[Tuple[int, int]], food: List[Tuple[int, int]], grid: Tuple[int, int]) -> str:
    """Creates a JSON-formatted string as input for an AI."""
    return json.dumps({
        "your_snake": snake,
        "opponent_snake": opp_snake,
        "food": food,
        "grid_size": grid
    })

def get_key() -> str:
    """Loads the API key from the .env file."""
    load_dotenv()
    return os.getenv("API_KEY", "")

def parse_ai_response(response_str: str) -> Dict:
    """Parses the AI response and returns a JSON object."""
    try:
        response_str = re.sub(r"```(?:json)?\s*|```", "", response_str).strip()
        response_json = json.loads(response_str)
        if "explanation" in response_json:
            response_json["explanation"] = response_json["explanation"].replace("\n", " ")
        return response_json
    except json.JSONDecodeError:
        return {}

def save_text(file_path: str, text: str, mode: str = "w") -> None:
    """Saves text to a file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, mode) as file:
        file.write(text)

def info(screen: pygame.Surface, uid: str, snakes: List[Dict[str, List[Tuple[int, int]]]]) -> None:
    """Saves game information to a log file."""
    current_time = datetime.now().strftime('%H:%M:%S')
    text = f"#### {uid} ####\n({current_time})\n\nStarting Snakes:\n"
    
    for snake in snakes:
        text += f"Color: {snake['color']}\nCoords: {snake['coords']}\n\n"
    
    text += f"#### {uid} ####"
    save_text(f"logs/{uid}/info.txt", text)
    pygame.image.save(screen, f"logs/{uid}/thumbnail.png")

def log_error(uid: str, error: str) -> None:
    """Logs errors to a file."""
    current_time = datetime.now().strftime('%H:%M:%S')
    save_text(f"logs/{uid}/info.txt", f"\n\n#### ERROR ({current_time}): \n{error}", mode="a")

def log_explanations(screen: pygame.Surface, explanations: List[Dict[str, str]], uid: str, index: int) -> None:
    """Saves AI explanations and screenshots."""
    current_time = datetime.now().strftime('%H:%M:%S')
    text = f"(Player {index}) {current_time}\n"
    text += "\n".join(f"({exp[0]}) {exp[1]['move']}: {exp[1]['explanation']}" for exp in explanations) + "\n\n"
    
    save_text(f"logs/{uid}/explanations.log", text, mode="a")
    os.makedirs(f"logs/{uid}/images", exist_ok=True)
    pygame.image.save(screen, f"logs/{uid}/images/{index}.png")

def create_video(uid: str) -> None:
    """Creates a video from saved images."""
    image_folder = f"logs/{uid}/images"
    video_path = f"logs/{uid}/video.avi"
    
    images = sorted(glob.glob(f'{image_folder}/*.png'), key=os.path.getmtime)
    if not images:
        return
    
    first_image = cv2.imread(images[0])
    height, width, layers = first_image.shape
    size = (width, height)
    
    out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'DIVX'), 2, size)
    for filename in images:
        out.write(cv2.imread(filename))
    out.release()
