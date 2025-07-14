# Your Friend Neu

## Overview
"Your Friend Neu" is a 2D interactive game built using Pygame, where players interact with a character named Neu through various actions like feeding, talking, or hitting. The game features a dynamic interface with a stove, inventory system, and mod support, allowing for extensible gameplay through custom mods. The game includes different modes for Neu, such as horror and love modes, triggered by specific player actions.

## Features
- **Interactive Character (Neu)**: Engage with Neu by feeding, talking, or hitting, affecting their state and triggering unique responses.
- **Inventory System**: Collect and manage items like cookies, cakes, and bread to feed Neu.
- **Stove Interface**: Use the stove to acquire items for the inventory.
- **Dialogue System**: Communicate with Neu through dialogue options and see their reactions.
- **Mod Support**: Load custom mods from `.zip` files in the `mods` folder to extend gameplay functionality.
- **Dynamic Visuals and Sounds**: Includes various images and sound effects for an immersive experience.
- **Special Modes**: Trigger horror or love modes based on interactions, with unique visuals and outcomes.

## Requirements
- Python 3.x
- Pygame library (`pip install pygame`)
- A system with graphical interface support (Windows, macOS, or Linux)
- Optional: Custom mods in `.zip` format for additional functionality

## Installation
1. **Clone or Download the Repository**:
   ```bash
   git clone <repository-url>
   cd your-friend-neu
   ```
   Or download the source code as a ZIP and extract it.

2. **Install Dependencies**:
   Ensure Python is installed, then install Pygame:
   ```bash
   pip install pygame
   ```

3. **Prepare Assets**:
   Ensure the `images` and `sound` folders are in the same directory as `YFN.py` with the required assets:
   - Images: `neu.png`, `fon.jpg`, `words.png`, `usna.png`, `cook.png`, `cake.png`, `bread.png`, `hard.png`, `horror_neu.png`, `burrning_neu.png`, `love_neu.png`, `stove.png`, `stove_fon.png`, `inv_fon.png`, `exit.png`
   - Sounds: `horror_sound.mp3`, `burrning_sound.mp3`
   - Font: `PixelifySans-VariableFont_wght.ttf` in the `font` folder

4. **Run the Game**:
   ```bash
   python YFN.py
   ```

## Gameplay
- **Start Screen**: Enter your name when prompted to begin interacting with Neu.
- **Main Interface**:
  - **Feed (Key 1)**: Open the inventory to feed Neu with collected items (cookies, cakes, bread).
  - **Talk (Key 2)**: Engage in dialogue with Neu, triggering random responses.
  - **Hit (Key 3)**: Hit Neu, which may lead to horror mode if done excessively.
  - **Stove Interaction**: Click the stove to access the item collection interface.
  - **Inventory**: Collect items in the stove interface and use them to feed Neu from the inventory.
- **Special Modes**:
  - **Horror Mode**: Triggered after hitting Neu 10 times, leading to a game-ending sequence.
  - **Love Mode**: Triggered by feeding Neu excessively, resulting in a unique game state.
  - **Burning Mode**: Activated by interacting with Neu in the stove interface, leading to a game-ending sequence.
- **Exit**: Use the Escape key to close the inventory or click the exit button in the stove interface.

## Controls
- **Keyboard**:
  - `1`: Open inventory to feed Neu.
  - `2`: Talk to Neu.
  - `3`: Hit Neu.
  - `0`: Load mods from the `mods` folder.
  - `ESC`: Close the inventory.
  - `Backspace`: Delete characters when entering the name.
  - `Space`: Submit the name at the start.
  - Other keys: Type the player's name at the start screen.
- **Mouse**:
  - Click the stove to open the stove interface.
  - Click items in the stove or inventory to collect or use them.
  - Click the exit button to close the stove interface.
  - Click Neu in the stove interface to trigger burning mode.

## Modding
- Place mod `.zip` files in the `mods` folder.
- Mods should contain Python scripts (`.py`) that can register custom draw functions and event handlers using `game.register_draw_function()` and `game.register_event_handler()`.
- Press `0` in-game to load mods dynamically.
- Mods have access to game objects like `neu`, `dialogue`, `move_tab`, `us_name`, `stove`, `stove_GUI`, `inv`, `screen`, `font`, and more.

## Notes
- The game includes system-level commands (e.g., `os.system('shutdown /s /t 0')`) that execute on certain conditions (horror or burning modes). **Use caution** when running the game, as these commands can shut down your system. Consider commenting out these lines for safety:
  ```python
  os.system('shutdown /s /t 0')
  ```
- Ensure all required image, sound, and font files are present in the correct directories to avoid errors.
- The game runs at 60 FPS and is designed for a 1920x1080 resolution.

## Troubleshooting
- **Missing Assets**: Ensure all image, sound, and font files are in the correct folders (`images`, `sound`, `font`).
- **Pygame Errors**: Verify Pygame is installed correctly (`pip install pygame`).
- **Mod Loading Issues**: Check that mod `.zip` files contain valid Python scripts and are placed in the `mods` folder.
- **System Shutdown**: Disable the `os.system('shutdown /s /t 0')` lines in the code to prevent unintended system shutdowns.

## License
This project is provided as-is without a specific license. Please contact the author for usage permissions.