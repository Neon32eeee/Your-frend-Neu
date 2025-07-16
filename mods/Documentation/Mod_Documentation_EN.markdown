# Mod Creation Documentation for the Game Your Friend Neu

---

## Game Overview (Optional)
The game **Your Friend Neu** is written in **Python** using the **Pygame** library with an **Object-Oriented** approach. **The full source code is available in the game files!** The game's plot revolves around Neu, and there are several ways to interact with him:

1. You can feed Neu by pressing the **1** key. When the player presses it, the inventory opens, showing the food that can be given to Neu. Initially, there is no food in the inventory (0). To obtain food, you need to access the stove, where all available food items can be cooked, adding them to the inventory. Neu also has invisible love points, and if these points are high enough...

2. You can talk to Neu by pressing the **2** key. When pressed, Neu's dialogue window appears, and a random phrase is displayed.

3. You can hit Neu by pressing the **3** key. When pressed, Neu's dialogue window appears with random phrases, a hit counter increases, and the love points are reset to 0.

---

## 1. Code Structure
- **Main Classes**:
    - `game`: This is the main object you will primarily use. It helps with loading and managing game resources.
    - `BaseObject`: This class allows you to create a standard object with an image and position, and includes a `draw` function.
    - `BaseItemInStove`: This class allows you to create a standard object used as food or other items for the stove.
    - `Neu`, `Dialogue`, `MoveTable`, `User_Name`, `Stove`, `GUI_Stove`: Specialized classes for game entities.

- **File Structure**:
    All main code should be written in a `.py` script. After creating a mod, place it in a ZIP archive so the game can read it. You can also include folders with textures, sounds, fonts, etc., in the ZIP file. The ZIP mod file should be placed in the `mods` folder.

---

## 2. Working with Basic Objects
- **Class `BaseObject`**:
    - The object has two variables: `image` and `position`, which are passed when creating the object. Here’s an example of creating a `gost` object:
        ```python
        import os

        gost_image_path = os.path.join("images", "gost_image.png")
        game.load_image("gost_image", gost_image_path, ())

        gost = BaseObject(game.images["gost_image"], (500, 350))
        ```
    - The object also has a `rect` attribute, which is used to track clicks on the object but is initially set to `None`.
    - An object created from a class inheriting `BaseObject` has a `draw` function that renders the object’s image on the screen at the specified `position`.

- **Class `BaseItemInStove`**:
    - The object has six variables: `name`, `image`, `image_size`, `position`, `add_count`, which are passed when creating the object, and also a `rect` attribute. Here’s an example of creating an `apple` object:
        ```python
        import os

        apple_image_path = os.path.join("images", "apple_image.png")
        game.load_image("apple_image", apple_image_path, ())

        apple = BaseItemInStove("apple", game.images["apple_image"], (250, 250), (350, 50), 1)
        ```
    - An object created from a class inheriting `BaseItemInStove` has the functions `draw`, `on_click`, and `update_all(size, position)`.

---

## 3. Functions of `game`
- **`game.register_draw_function`**:
    - This function allows you to register a function for rendering images or other content on the screen. Example with the `gost` object:
        ```python
        import os

        gost_image_path = os.path.join("images", "gost_image.png")
        game.load_image("gost_image", gost_image_path, ())

        gost = BaseObject(game.images["gost_image"], (500, 350))

        def draw_gost():
            gost.draw()

        game.register_draw_function(draw_gost)
        ```

- **`game.register_event_handler`**:
    - This function allows you to register a function to handle **Pygame** events, such as key presses. Example:
        ```python
        import pygame

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
    - This function allows you to terminate the game process. Example:
        ```python
        import pygame

        def key_down(event):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    game.stop()

        game.register_event_handler(key_down)
        ```

- **`game.regist_object`**:
    - This function allows you to add an object to `game.objects` for further interaction. Example with `gost`:
        ```python
        import os

        gost_image_path = os.path.join("images", "gost_image.png")
        game.load_image("gost_image", gost_image_path, ())

        gost = BaseObject(game.images["gost_image"], (500, 350))

        game.regist_object("gost", gost)

        def draw_gost():
            gost.draw()

        game.register_draw_function(draw_gost)
        ```

- **`game.create_rect`**:
    - This function allows you to create a hitbox for tracking clicks on an object. Example with `gost`:
        ```python
        import os

        gost_image_path = os.path.join("images", "gost_image.png")
        game.load_image("gost_image", gost_image_path, ())

        gost = BaseObject(game.images["gost_image"], (500, 350))

        game.regist_object("gost", gost)

        def draw_gost():
            gost.draw()

        def register_click(event):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.stop()

        game.register_draw_function(draw_gost)
        game.register_event_handler(register_click)
        ```

- **`game.get_objects`**:
    - This function returns all objects in `game.objects`. Example with `gost`:
        ```python
        import os

        gost_image_path = os.path.join("images", "gost_image.png")
        game.load_image("gost_image", gost_image_path, ())

        gost = BaseObject(game.images["gost_image"], (500, 350))

        game.regist_object("gost", gost)

        def draw_gost():
            objects = game.get_objects()
            if "gost" in objects:
                gost.draw()

        game.register_draw_function(draw_gost)
        ```

- **`game.add_obj_inventory`**:
    - This function allows you to add a key and value to `inv.inventory`. Example:
        ```python
        game.add_obj_inventory("apple", 0)
        ```

- **`game.load_*`**:
    - These functions allow you to load and access lists of game resources:
        - **`game.load_image`**:
            - Example:
                ```python
                import os

                apple_path = os.path.join("images", "apple_image.png")
                game.load_image("apple", apple_path, ())
                ```
            - The last parameter is the image size. If left empty, the size remains unchanged; otherwise, it is resized to the specified dimensions.
        - **`game.load_sound`**:
            - Example:
                ```python
                import os

                bruh_path = os.path.join("sounds", "bruh.mp3")
                game.load_sound("bruh", bruh_path)
                ```
        - **`game.load_font`**:
            - Example:
                ```python
                import os

                my_font_path = os.path.join("fonts", "my_font.ttf")
                game.load_font("my_font", my_font_path)
                ```

- **`game.get_*`**:
    - These functions return lists of images (`game.get_images`), sounds (`game.get_sounds`), or fonts (`game.get_fonts`).

- **`game.create_text`**:
    - This function allows you to render text on the screen. Example:
        ```python
        def draw_num_hit():
            game.create_text(f"num_hit:{game.neu.num_hit}", (100, 100), (0, 255, 0))

        game.register_draw_function(draw_num_hit)
        ```

- **`game.draw_dialoge_win`**:
    - This function allows you to render a dialogue window with a message. Example:
        ```python
        def draw_hz():
            game.draw_dialoge_win("Something there", (750, 250))

        game.register_draw_function(draw_hz)
        ```

### Additional Notes:
Through the `game` object, you can also access `neu`, `dialoge`, `move_tab`, `us_name`, `stove`, `stove_GUI`, `inv`, `screen`, `clock`, and `font`.

---

To fully understand, you can review the game’s source code.