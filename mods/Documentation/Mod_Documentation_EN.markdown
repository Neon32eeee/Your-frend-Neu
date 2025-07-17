# Mod Creation Documentation for the Game *Your Friend Neu*

---

## Game Overview (Optional)
The game *Your Friend Neu* is written in **Python** using the **Pygame** library with an **object-oriented** approach. **The full source code is available in the game files!** The game's plot revolves around Neu, and there are several ways to interact with him:

1. You can feed Neu by pressing the **1** key. When the player presses it, the inventory opens, showing food items that can be given to Neu. Initially, there is no food in the inventory (0). To obtain food, the player must go to the stove, where all available food items can be cooked, adding them to the inventory. Neu also has hidden "love points," and if these points are high enough...

2. You can talk to Neu by pressing the **2** key. When pressed, Neu’s dialogue window appears, displaying a randomly selected phrase.

3. You can hit Neu by pressing the **3** key. When pressed, Neu’s dialogue window appears with random phrases, and a hit counter increases. This also resets the love points counter to 0.

---

## 1. Code Structure
- **Main Classes**:
    - `game`: This is the main object you will primarily work with. It handles the loading and management of game resources.
    - `BaseObject`: This class allows you to create a standard object with an image and position, including a `draw` function.
    - `BaseItemInStove`: This class allows you to create a standard object to be used as food or other items for the stove.
    - `Neu`, `Dialogue`, `MoveTable`, `User_Name`, `Stove`, `GUI_Stove`: Specialized classes for game entities.

- **Configuration Files**:
    You must create a `conf.json` file, otherwise the code will not work. Here is a template for `conf.json`:
    ```json
    {
        "name": "MyMod",
        "version": 1,
        "author": "None"
    }
    ```
    You can fill in the details as needed.

- **File Structure**:
    All main code should be written in a `.py` script. After creating the mod, place it in a ZIP archive along with the mandatory `conf.json` file so the game can read it. You can also include folders with textures, sounds, fonts, etc., in the ZIP file. The ZIP file containing the mod must be placed in the `mods` folder.

---

## 2. Working with Basic Objects
- **Class `BaseObject`**:
    - The object has two variables: `image` and `position`, which are passed when creating the object. Here is an example of creating a `ghost` object:
        ```python
        import os

        ghost_image_path = os.path.join("images", "ghost_image.png")
        game.load_image("ghost_image", ghost_image_path, ())

        ghost = BaseObject(game.images["ghost_image"], (500, 350))
        ```
    - There is also a `rect` attribute, which is used for tracking clicks on the object but is initially set to `None`.
    - Objects created from classes inheriting from `BaseObject` (`base_object`) have a `draw` function that renders the object’s image on the screen at the specified `position`.

- **Class `BaseItemInStove`**:
    - The object has six variables: `name`, `image`, `image_size`, `position`, `add_count`, which are passed when creating the object, and a `rect` attribute. Here is an example of creating an `apple` object:
        ```python
        import os

        apple_image_path = os.path.join("images", "apple_image.png")
        game.load_image("apple_image", apple_image_path, ())

        apple = BaseItemInStove("apple", game.images["apple_image"], (250, 250), (350, 50), 1)
        ```
    - Objects created from classes inheriting from `BaseItemInStove` (`base_item`) have the functions `draw`, `on_click`, and `update_all(size, position)`.

---

## 3. `game` Functions
- **`@game.mod_draw`**:
    - This decorator allows you to create functions for rendering images or other content on the screen. Example with the `ghost` object:
        ```python
        import os

        ghost_image_path = os.path.join("images", "ghost_image.png")
        game.load_image("ghost_image", ghost_image_path, ())

        ghost = BaseObject(game.images["ghost_image"], (500, 350))

        @game.mod_draw
        def draw_ghost():
            ghost.draw()
        ```

- **`game.register_event_handler`**:
    - This decorator allows you to create functions for handling **Pygame** events, such as key presses. Example:
        ```python
        import pygame

        @game.mod_event
        def key_x_down(event):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    game.neu.num_hit = 0
        ```

- **`game.mod_log`**:
    - This function allows you to output text to the console. Example:
        ```python
        try:
            result = 10 / 0
        except ZeroDivisionError as e:
            game.mod_log("MyMod", f"Error: {e}")
        ```
        Console output:
        ```
        [MOD MyMod] Error: division by zero
        ```

- **`game.stop`**:
    - This function terminates the game process. Example:
        ```python
        import pygame

        @game.mod_event
        def key_down(event):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    game.stop()
        ```

- **`game.register_object`**:
    - This function allows you to add an object to `game.objects` for further interaction. Example with `ghost`:
        ```python
        import os

        ghost_image_path = os.path.join("images", "ghost_image.png")
        game.load_image("ghost_image", ghost_image_path, ())

        ghost = BaseObject(game.images["ghost_image"], (500, 350))

        game.register_object("ghost", ghost)

        @game.mod_draw
        def draw_ghost():
            ghost.draw()
        ```

- **`game.create_rect`**:
    - This function creates a hitbox for tracking clicks on an object. Example with `ghost`:
        ```python
        import os

        ghost_image_path = os.path.join("images", "ghost_image.png")
        game.load_image("ghost_image", ghost_image_path, ())

        ghost = BaseObject(game.images["ghost_image"], (500, 350))

        game.register_object("ghost", ghost)

        @game.mod_draw
        def draw_ghost():
            ghost.draw()

        @game.mod_event
        def register_click(event):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.stop()
        ```

- **`game.get_objects`**:
    - This function returns all objects in `game.objects`. Example with `ghost`:
        ```python
        import os

        ghost_image_path = os.path.join("images", "ghost_image.png")
        game.load_image("ghost_image", ghost_image_path, ())

        ghost = BaseObject(game.images["ghost_image"], (500, 350))

        game.register_object("ghost", ghost)

        @game.mod_draw
        def draw_ghost():
            objects = game.get_objects()
            if "ghost" in objects:
                ghost.draw()
        ```

- **`game.add_obj_inventory`**:
    - This function adds a key and value to `inv.inventory`. Example:
        ```python
        game.add_obj_inventory("apple", 0)
        ```

- **`game.load_*`**:
    - These functions allow you to load resources into the game and retrieve their lists:
        - `game.load_image`:
            - **Example**:
                ```python
                import os

                apple_path = os.path.join("images", "apple_image.png")
                game.load_image("apple", apple_path, ())
                ```
            - The last parameter is the image size. If left empty, the size remains unchanged; otherwise, it changes to the specified size.
        - `game.load_sound`:
            - **Example**:
                ```python
                import os

                bruh_path = os.path.join("sounds", "bruh.mp3")
                game.load_sound("bruh", bruh_path)
                ```
        - `game.load_font`:
            - **Example**:
                ```python
                import os

                my_font_path = os.path.join("fonts", "my_font.ttf")
                game.load_font("my_font", my_font_path)
                ```

- **`game.get_*`**:
    - These functions return lists of images (`game.get_images`), sounds (`game.get_sounds`), and fonts (`game.get_fonts`).

- **`game.create_text`**:
    - This function renders text on the screen. Example:
        ```python
        @game.mod_draw
        def draw_num_hit():
            game.create_text(f"num_hit:{game.neu.num_hit}", (100, 100), (0, 255, 0))
        ```

- **`game.draw_dialogue_win`**:
    - This function draws a dialogue window with a message. Example:
        ```python
        @game.mod_draw
        def draw_hz():
            game.draw_dialogue_win("Something there", (750, 250))
        ```

### Additional Notes:
Through the `game` object, you can also access `neu`, `dialogue`, `move_tab`, `us_name`, `stove`, `stove_GUI`, `inv`, `screen`, `clock`, and `font`.

---

To fully understand the game, you can study its source code.