# Документация по созданию модов для игры Your frend Neu

---

## Описание игры для понимания (необязательно)
Игра **_Your frend Neu_** на писана на языке **python** при помощи библеотеки **pygame** с **Обьектно ореньтированым** подходом. **Весь исходный код есть в файлах игры!** Сюжет игры строится на Нее, есть несколько способов взимодействовать с ним:

1. Мы можем покормить его при нажатае кнопки 1 и когда игрок нажимает её то открывается инвентарь в котором находятся еда которую мы можем дать ему, изначально еды еды в инвенторе нет (0) а что-бы получить еду нам нужно зайти а печь и том будет вся еда которую мы можем пожарить и тогда у нас появится еда в инвенторе. Так же у Нея есть невидемые очки любви и если очки больше.

2. Мы можем поговарить с ним при нажатие 2 когда игрок нажмёт её то высветится диалоговое окно Нея и рандомно выбирается фраза.

3. Мы можем ударить Нея при нажатие 3 когда игрок нажмёт её то высветится диалоговаое окно Нея где он говарить рандомные фразы и прибовляется очко ударов, так же сбрасывает до 0 счёчик любви.

---

## 1. Структура кода
- **Основные классы**:
    - `game`- это обьект которым в остовно вы и будети пользоваться. Он помогает с загруской и управлением ресурсов игры.
    - `BaseObject`- это класс позваляет создавать стандартный обьект с изовражением и позыцей, функцей `draw` .
    - `BaseItemInStove`- это класс посваляет создовать стандартный обьект для изпользования его в качестве еды или другой веши для печки.
    - `Neu, Dialogue, MoveTable, User_Name, Stove, GUI_Stove`: Специализированные классы для игровых сущностей.
  
- **Конфигоруционые файлы**:
    Обезателно надо создать conf.json иначе код не будет работать. Вот шаблон для conf.json:
    ```json
        {
        "name": "MyMod",
        "version": 1,
        "author": "None"
        }
    ```
    Вы уже сами заполните его

- **Сруктура файлов**:
    
    Всё основной код вы должны писать в .py скрепре после создания мода помистите его, ещё обезательно добавьте conf.json в zip архив что-бы игра могла их прочитать, так же вы можете помечтить в zip файл папки с текстурами, звуками, шифтами и т.д.
    Так же zip мода надопоместить в папку `mods`.

---

## 2. Работа с базовыми обьектами
- Класс `BaseObject`:
    - У обьекта есть 2 переменых это `image` и `poziteon` которые мы передаём при создание обьекта. Вот пример создание обьекта `gost`
        ```python
        import os

        gost_Image_path = os.path.join("images", "gost_imsge.png")
        game.load_image("gost_image", gost_image_path, ())

        gost = base_odject(game.images["gast_image", (500, 350)])
        ```
    - Так же есть `rect` он используесть для тослеживания нажатия по обьекту но изночально он равет ___`None`___.
    - У обьекта созданого из класса наслетника `BaseObject` (`base_object`) есть функция `draw` она вы водит изображение обьекта на экран туда куда мы указали `pozition`.
- Класс `BaseItemInStove`:
    - У обьекта есть 6 переменых это `name`, `image`, `image_size`, `poziteon`, `add_count` которые мы передаём при создание обьекта и так же есть `rect`. Вот пример создание обьекта `appel`
        ```python
        import os

        apple_image_path = os.path.join("images", "apple_image.png")
        game.load_image("apple_image", apple_image_path, ())

        apple = base_item("apple", game.images["apple_Image"], (250, 250), (350, 50), 1)
        ```
    - У обьекта созданого из класса наследника `BaseItemInStove` (`base_item`) есть функции `draw`, `on_click`, `update_all(size, pozition)`.
  
---

## 3. Функции `game`
- __`@game.mod_draw`__:
    - Этот дикоратор позваляет делать функции с отображением картинок или что-то другое на экран. Пример c обьектом `gost`:
        ```python
        import os

        gost_Image_path = os.path.join("images", "gost_image.png")
        game.load_image("gost_image", gost_image_path, ())

        gost = base_odject(game.images["gost_image"], (500, 350))

        @game.mod_draw
        def draw_gost():
            gost.draw()
        ```
- __`game.register_event_handler`__:
    - Этот дикоратор позваляет делать функцие с ивентами *__pygame__* например нажатие клавиши. Пример:
        ```python
        import pygame

        @game.mod_event
        def key_x_down(event):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    game.neu.num_hit = 0
        ```
- __`game.mod_log`__:
    - Она позволяет выводить текс в консосль. Пример:
        ```python
        try:
            result = 10 / 0
        except ZeroDivisionError as e:
            game.mod_log("MyMod" ,f"Error: {e}")
        ```
        Вывод в консоле:
        ```
        [MOD MyMod] Error: division by zero
        ```

- __`game.stop`__:
    - Она позволяет завершить процес игры. Пример:
        ```python
        import pygame

        @game.mod_event
        def key_down(event):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    game.stop()
        ```

- __`game.regist_object`__:
    - Она позволяет добавить обьект в `game.objects` что-бы дальше с ним взоимодействовать. Пример на `gost`:
        ```python
        import os

        gost_Image_path = os.path.join("images", "gost_image.png")
        game.load_image("gost_image", gost_image_path, ())

        gost = base_odject(game.images["gost_image"], (500, 350))

        game.regist_object("gost", gost)

        @game.mod_draw
        def draw_gost():
            gost.draw()
        ```

- __`game.create_rect`__:
    - Она позволяет созтать хит-бокс для откслеживания нажатья по обьекту. Пример c `gost`:
        ```python
        import os

        gost_Image_path = os.path.join("images", "gost_image.png")
        game.load_image("gost_image", gost_image_path, ())

        gost = base_odject(game.images["gost_image"], (500, 350))

        game.regist_object("gost", gost)

        @game.mod_draw
        def draw_gost():
            gost.draw()

        @game.mod_event
        def register_click(event):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.stop()

        game.register_draw_function(draw_gost)
        ```

- __`game.get_objects`__:
    - Она возращает всё обьекты в `game.objects`. Пример с `gost`:
        ```python
        import os

        gost_Image_path = os.path.join("images", "gost_image.png")
        game.load_image("gost_image", gost_image_path, ())

        gost = base_odject(game.images["gost_image"], (500, 350))

        game.regist_object("gost", gost)

        @game.mod_draw
        def draw_gost():
            objects = game.get_objects()
            if "gost" in objects:
                gost.draw()
        ```

- __`game.add_obj_inventory`__:
    - Она позваляет добавить ключ и сначение в `inv.inventory`. Пример:
        ```python
        game.add_obj_invenyory("apple", 0)
        ```

- __`game.load_*`__:
    - Она позволяет загрузить в игру и получать список:
        - `game.load_image`:
            - #### Пример:
                ```python
                import os

                apple_path = os.path.join("images","apple_image.png")
                game.load_image("apple", apple_path, ())
                ```
            - Последнее значение это размер изображения если оставаить его пусты то размер не изменится, иначе изменится на то что нты написал.
        - `game.load_sound`:
            - ### Пример:
                ```python
                import os

                bruh_path = os.path.join("sounds", "bruh.mp3")
                game.load_sound("bruh", bruh_path)
                ```
        - `game.load_font`:
            - ### Пример:
                ```python
                import os

                my_font_path = os.path.join("fonts", "my_font.ttf")
                game.load_font("my_font", my_font_path)
                ```
- __`game.get_*`__:
    - Она возращает список изображений: `game.get_images`, звуков: `game.get_sounds`, шрифтов: `game.get_fonts`.

- __`game.create_text`__:
    - Она позволяет вывводить текст на экран. Пример:
        ```python
        @game.mod_draw
        def draw_num_hit():
            game.create_text(f"num_hit:{game.neu.num_hit}", (100, 100), (0, 255, 0))
        ```

- __`game.draw_dialoge_win`__:
    - Она позволяет отрисоватьдиалоговое окно с какимто сообщением. Пример:
        ```python
        @game.mod_draw
        def draw_hz():
            game.draw_dialoge_win("Что-то там", (750, 250))
        ```
### Дополнение:
через `game` так же можно получить доступ к `neu`, `dialoge`, `move_tab`, `us_name`, `stove`, `stove_GUI`, `inv`, `screen`, `clock` и `font`.

---

Что бы вы до конца розабрались можите почитать код игры.