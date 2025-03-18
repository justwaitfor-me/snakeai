# Snake.AI

## Overview

Snake.AI is a Python implementation of the classic Snake game. In this version, the snakes are controlled by AI agents using the Gemini API. The game provides a visual representation of the snakes, food, and grid, and it includes logging and video creation capabilities for analyzing game sessions.

## Features

* **AI-Controlled Snakes:** Snakes are driven by AI agents using the Gemini API to make decisions.
* **Configurable Game Settings:** The game's behavior and appearance can be customized through a `conf.yml` file. This includes screen size, colors, snake count, food settings, and more.
* **Visual Representation:** The game is rendered using Pygame, providing a visual interface for the game.
* **Logging:** Game sessions are logged, including errors, AI explanations, and game state information.
* **Video Creation:** The game can automatically generate a video of each game session.
* **Debugging Tools:** A debug mode is available to aid in development and troubleshooting.

## Installation

1.  **Prerequisites:**
    * Python 3.x
    * `pip` package manager
    * A Google Gemini API key
2.  **Clone the repository:**
    ```bash
    git clone https://github.com/justwaitfor-me/snakeai.git
    cd snakeai
    ```
3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up your Gemini API key:**
    * Create a `.env` file in the project root.
    * Add your Gemini API key to the `.env` file as follows:
        ```
        API_KEY=YOUR_API_KEY
        ```

## Configuration

The `conf.yml` file allows you to customize various aspects of the game:

* `project`:  Project metadata (name, version, author).
* `game`:  Game settings such as screen dimensions, colors, font sizes, and snake configurations.
* `food`:  Parameters related to food spawning (minimum, maximum, and per-snake count).
* `settings`:  Game behavior settings like move delay, debug mode, header display, and header height.

## Usage

1.  **Run the `main.py` script:**
    ```bash
    python main.py
    ```
2.  The game will start, and the AI-controlled snakes will begin to move.
3.  Observe the game visually.
4.  Game logs, screenshots, and videos will be saved in the `logs` directory.

## Code Structure

* `main.py`:  The main entry point for the game. It initializes Pygame, manages the game loop, handles snake movements, and calls the AI player.
* `utils.py`:  Provides utility functions for tasks such as configuration loading, screen drawing, collision detection, file operations, and video creation.
* `player.py`:  Handles the interaction with the Gemini API to get the snake's next move.
* `conf.yml`:  Configuration file for the game settings.
* `player.txt`:  System instruction file for the Gemini API, defining the rules and behavior for the AI snake.

## Contributing

Contributions to this project are welcome! If you have suggestions for improvements or find any issues, please submit a pull request or create an issue in the repository.

## License

This project is licensed under the [License Name] License.

## Author

* justwaitfor-me