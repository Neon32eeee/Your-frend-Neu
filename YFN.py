import pygame
import random
import time
import os
import zipfile
import shutil
import json

pygame.init()
class BaseObject():
    def __init__(self, image, pozition):
        self.image = image
        self.pozition = pozition
        self.rect = None

    def draw(self):
        screen.blit(self.image, self.pozition)

base_object = BaseObject(None, None)

class Game:
    
    def __init__(self):
        self.running = True
        # Основные объекты игры
        self.neu = None
        self.dialogue = None
        self.move_tab = None
        self.us_name = None
        self.stove = None
        self.stove_GUI = None
        self.inv = None
        # Системные объекты
        self.screen = None
        self.clock = None
        self.font = None
        # Ресурсы
        self.images = {}
        self.sounds = {}
        self.fonts = {}
        self.objects = {}
        # Регистрация модов
        self.mod_draw_functions = []
        self.mod_event_handlers = []
    
    def init_objects(self):
        """Инициализация ссылок после создания объектов"""
        self.objects = {
            'neu': self.neu,
            'dialogue': self.dialogue,
            'move_tab': self.move_tab,
            'us_name': self.us_name,
            'stove': self.stove,
            'stove_GUI': self.stove_GUI,
            'inv': self.inv,
            'screen': self.screen,
            'clock': self.clock,
            'font': self.font
        }

    def stop(self):
        global running
        running = False

    def mod_log(self, mod_name, message):
        print(f"[MOD {mod_name}] {message}")

    def register_draw_function(self, func):
        """Добавляет функцию отрисовки мода"""
        if func not in self.mod_draw_functions:
            self.mod_draw_functions.append(func)

    def register_event_handler(self, handler):
        """Добавляет обработчик событий мода"""
        if handler not in self.mod_event_handlers:
            self.mod_event_handlers.append(handler)

    def load_image(self, name, path, size):
        try:
            img = pygame.image.load(path)
            if size != ():
                img = pygame.transform.scale(img, size)
            self.images[name] = img
            return img
        except Exception as e:
            print(f"Error load image {path}: {e}")
            return None
    
    def load_sound(self, name, path):
        try:
            sound = pygame.mixer.Sound(path)
            self.sounds[name] = sound
            return sound
        except Exception as e:
            print(f"Error load sound {path}:{e}")
            return None

    def load_font(self, name, path, size):
        try:
            font = pygame.font.Font(path, size)
            self.font[name] = font
            return font
        except Exception as e:
            print(f"Error load font {path}:{e}")

    def regist_object(self, name, object):
        self.objects[name] = object

    def create_rect(self, name):
        obj = self.objects.get(name)
        if obj is None:
            print(f"Данного обьекта с и не менем {name} существует!")

        if hasattr(obj, 'image') and hasattr(obj, 'pozition'):
            obj.rect = obj.image.get_rect(topleft=obj.pozition)
            return obj.rect
        else:
            print(f"Объект '{name}' не имеет необходимых атрибутов для создания Rect")
            return None

    def get_images(self):
        return self.images
    
    def get_sounds(self):
        return self.sounds
    
    def get_fonts(self):
        return self.fonts
    
    def get_object(self):
        return self.objects

    def create_text(self, text, pozition, color):
        text_render = font.render(text, True, color)
        screen.blit(text_render, pozition)

    def draw_dialoge_win(self, text, pozition):
        screen.blit(words_win, pozition)
        game.create_text(text, ((pozition[0]+100), (pozition[1]+60)), (1, 1, 1))

    def add_odj_inventory(self, name, count):
        if name not in inv.inventory:
            inv.inventory[name] = count
            return inv.inventory
        else:
            print("Ошибка при создание обьекта инвенторя. Он уже сушествует!")

game = Game()

screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption('Your frend Neu')
clock = pygame.time.Clock()
game.screen = screen
game.clock = clock

# Список для функций отрисовки от модов
mod_draw_functions = game.mod_draw_functions
mod_event_handlers = game.mod_event_handlers # Для обработки событий


# Функция для загрузки всех модов из папки mods
def load_mods_from_folder():
    mods_folder = "mods"
    try:
        if not os.path.exists(mods_folder):
            print("Папка 'mods' не найдена. Создаю папку.")
            os.makedirs(mods_folder)
            return

        zip_files = [f for f in os.listdir(mods_folder) if f.endswith('.zip')]
        if not zip_files:
            print("В папке 'mods' нет .zip файлов.")
            return

        for zip_file in zip_files:
            zip_path = os.path.join(mods_folder, zip_file)
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    temp_dir = os.path.join(mods_folder, f"temp_{zip_file}")
                    zip_ref.extractall(temp_dir)
                    
                    py_files = [f for f in zip_ref.namelist() if f.endswith('.py')]
                    if not py_files:
                        print(f"В {zip_file} нет Python-скриптов.")
                        continue

                    conf_file = [f for f in zip_ref.namelist() if f.endswith('.json')]
                    if not conf_file:
                        print(f"В {zip_file} нет конфугурационых файлов.")
                        continue

                    mod_info = {
                        'name': 'Unknown',
                        'version': 'Unknown',
                        'author': 'Unknown'
                    }
                    
                    for conf_file in conf_file:
                        try:
                            with open(os.path.join(temp_dir, conf_file), 'r', encoding='utf-8') as conf:
                                config_data = json.load(conf)
                                mod_info['name'] = config_data.get('name', 'Unknown')
                                mod_info['version'] = config_data.get('version', 'Unknown')
                                mod_info['author'] = config_data.get('author', 'Unknown')
                                print(f"Имя мода: {mod_info['name']} (Версия: {mod_info['version']}, Автор: {mod_info['author']})")
                        except json.JSONDecodeError as e:
                            print(f"Ошибка при разборе {conf_file}: {str(e)}")
                            continue
                        except Exception as e:
                            print(f"Ошибка при чтении {conf_file}: {str(e)}")
                            continue
                                

                    for py_file in py_files:
                        with open(os.path.join(temp_dir, py_file), 'r', encoding='utf-8') as file:
                            code = file.read()
                            globals_dict = {
                                'pygame': pygame,
                                'neu': neu,
                                'dialogue': dialogue,
                                'move_tab': move_tab,
                                'us_name': us_name,
                                'stove': stove,
                                'stove_GUI': stove_GUI,
                                'inv': inv,
                                'game': game,
                                'base_object': BaseObject,
                                'base_item': BaseItemInStove,
                                'screen': screen,
                                'font': font,
                                'mod_draw_functions': mod_draw_functions,
                                'mod_event_handlers': mod_event_handlers,
                                'os': os,
                                'random': random,
                                'time': time
                            }
                            exec(code, globals_dict)
                            print(f"Успешно загружен мод: {py_file} из {zip_file}")

                    
                    shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception as e:
                print(f"Ошибка при загрузке {zip_file}: {str(e)}")
    except Exception as e:
        print(f"Ошибка при обработке папки mods: {str(e)}")


# картинка Нея
neu_images = pygame.image.load('images/neu.png')
neu_images = pygame.transform.scale(neu_images, (400, 400))
# картинка фона
fon_image = pygame.image.load('images/fon.jpg')
fon_image = pygame.transform.scale(fon_image, (1920, 1080))
# картинка диаголоваго окна
words_win = pygame.image.load('images/words.png')
words_win = pygame.transform.scale(words_win, (600, 200))
# каритинка usna
usna_image = pygame.image.load('images/usna.png')
usna_image = pygame.transform.scale(usna_image, (700, 300))
# картинка пиченья
cook_image = pygame.image.load('images/cook.png')
cook_image = pygame.transform.scale(cook_image, (180, 180))
# картинка торта
cake_image = pygame.image.load('images/cake.png')
cake_image = pygame.transform.scale(cake_image, (90, 123))
# картинка хлеба
bread_image = pygame.image.load('images/bread.png')
bread_image = pygame.transform.scale(bread_image, (90, 90))
# картинка седца
hard_image = pygame.image.load('images/hard.png')
hard_image = pygame.transform.scale(hard_image, (90, 80))
# хоррор Ней
horror_neu_image = pygame.image.load('images/horror_neu.png')
horror_neu_image = pygame.transform.scale(horror_neu_image, (1000, 1000))
# сгоревший Ней
burrning_heu = pygame.image.load('images/burrning_neu.png')
burrning_heu = pygame.transform.scale(burrning_heu, (1920, 1012))
# любйщий Ней
love_neu = pygame.image.load('images/love_neu.png')
love_neu = pygame.transform.scale(love_neu, (1920, 1012))
# картинка печки
stove_image = pygame.image.load('images/stove.png')
stove_image = pygame.transform.scale(stove_image, (275, 350))
# фон печки
stove_fon_image = pygame.image.load('images/stove_fon.png')
stove_fon_image = pygame.transform.scale(stove_fon_image, (1920, 1012))
# фон инвенторя
fon_inv = pygame.image.load('images/inv_fon.png')
fon_inv = pygame.transform.scale(fon_inv, (500, 250))
# картинка выхода
exit_image = pygame.image.load('images/exit.png')
exit_image = pygame.transform.scale(exit_image, (100, 200))

horror_sound = pygame.mixer.Sound('sound/horror_sound.mp3')
burrning_sound = pygame.mixer.Sound('sound/burrning_sound.mp3')

font = pygame.font.Font('font/PixelifySans-VariableFont_wght.ttf', 25)
game.font = font

# Основа Ней
class Neu():
    def __init__(self, image):
        self.image = image
        self.pozition = (500, 350)
        self.size = (400, 400)
        self.rect = neu_images.get_rect(topleft=self.pozition)
        self.horror_mode = False
        self.stove_mode = False
        self.love_mode = False
        self.horror_time_start = 0
        self.burning_time_start = 0
        self.love_time_start = 0
        self.stop_words = ['Хватит!',
                        'Прекрати!',
                        'Больше так не делай!',
                        'Зачем ты это делаешь?',
                        'Умаляю перкати', 'ЗАЧЕМ?',
                        'За что?', 'Я сказал прекрати!',
                        'Почему ты это делаешь?', 'ПОЧЕМУ?']
        
        self.words = ['Сколько тебе лет?',
                      'Как дела?',
                      'Какой твой любимый цвет?',
                      'У тебя есть питомец?',
                      'Бла-бла-бла']
        
        self.num_hit = 0
        self.num_love = 0


    def hit(self):
        if self.num_hit < 10:
            self.num_hit += 1
            self.num_love = 0
        else:
            self.num_love = 0
            self.horror_mode = True
            if self.horror_time_start == 0:
                self.horror_time_start = time.time()
                horror_sound.play()

    
    
    def time_horror_log(self):
        return time.time() - self.horror_time_start >= 1

    def time_burrning_log(self):
        return time.time() - self.burning_time_start >= 1.5
    
    def time_love_log(self):
        return time.time() - self.love_time_start >= 1.5
    
    def burning(self):
        self.stove_mode = True
        if self.burning_time_start == 0:
            self.burning_time_start = time.time()
            burrning_sound.play()

    
    # Функция отрисовки
    def draw(self):
        if stove.win_on == False:
            self.image = pygame.transform.scale(self.image, self.size)
            screen.blit(self.image, self.pozition)
        else:
            self.image = pygame.transform.scale(self.image, self.size)
            screen.blit(self.image, self.pozition)

    def horror_draw(self):
        screen.blit(horror_neu_image, (450, 0))
    
    def burrning_draw(self):
        screen.blit(burrning_heu, (0, 0))

    def love_draw(self):
        screen.blit(love_neu, (0, 0))

    def food(self, count):
        if self.num_hit > 0:
                self.num_hit -= 1
        if self.num_love < 14:
                self.num_love += count
        else:
            self.love_mode = True
            if self.love_time_start == 0:
                self.love_time_start = time.time()
                with open('love.txt', 'w', encoding='utf-8') as file:
                    for i in range(1500):
                        file.write('LOVE ')
    
    def update_rect(self):
        self.rect = neu_images.get_rect(topleft=self.pozition)


neu = Neu(neu_images)
game.neu = neu


#  Диаголовое окно его функции
class Dialogue:
    def __init__(self):
        self.text_pozition = (850, 310)
        self.dialogue_pozition = (750, 250)
        self.open_second = False
        self.open_hit = False
        self.open_food = False
        self.start = True
        self.start_time = 0
        self.text = ""
        self.food_image = None

    # функция расчёта времени
    def time_log(self):
        return time.time() - self.start_time >= 3.0
    
    def text_start(self):
        screen.blit(words_win, self.dialogue_pozition)
        text = font.render('Привет! Как тебя завут?', True, 'Black')
        screen.blit(text, self.text_pozition)

    # функция орисовки фразы при ударе
    def text_if_hit(self):
        screen.blit(words_win, self.dialogue_pozition)
        text = font.render(self.text, True, 'Black')
        screen.blit(text, self.text_pozition)
    
    # функция отрисовки фразы при выборе поговарить
    def text_if_second(self):
        screen.blit(words_win, self.dialogue_pozition)
        text = font.render(self.text, True, 'Black')
        screen.blit(text, self.text_pozition)
    
    def if_food(self):
        screen.blit(words_win, self.dialogue_pozition)
        screen.blit(hard_image, (870, 320))
        screen.blit(self.food_image, (980, 320))

dialogue = Dialogue()
game.dialogue = dialogue


class MoveTable:
    def __init__(self):
        self.muve_text_1 = font.render('1.Пкормить', True, 'Black')
        self.muve_text_2 = font.render('2.Поговарить', True, 'Black')
        self.muve_text_3 = font.render('3.Ударить', True, 'Black')
        self.pozition_muve_1 = (450, 350)
        self.pozition_muve_2 = (450, 375)
        self.pozition_muve_3 = (450, 395)
    
    def draw(self):
        screen.blit(self.muve_text_1, self.pozition_muve_1)
        screen.blit(self.muve_text_2, self.pozition_muve_2)
        screen.blit(self.muve_text_3, self.pozition_muve_3)


move_tab = MoveTable()
game.move_tab = move_tab


class User_Name:
    def __init__(self):
        self.user_name_text_2 = font.render('Имя:', True, 'Black')
        self.poziteon_text = (550, 750)
        self.poziteon_usna = (550, 725)
        self.poziteon_ustext = (600, 825)
        self.user_name = ''

    def draw(self):
        screen.blit(usna_image, self.poziteon_usna)
        screen.blit(self.user_name_text_2, self.poziteon_text)
        user_text_name = font.render(self.user_name, True, 'Black')
        screen.blit(user_text_name, self.poziteon_ustext)


us_name = User_Name()
game.us_name = us_name

class Stove:
    def __init__(self):
        self.image = stove_image
        self.pozition = (925, 225)
        self.rect = stove_image.get_rect(topleft=self.pozition)
        self.win_on = False

    def draw(self):
        screen.blit(self.image, self.pozition)

    def on_click_first(self):
        self.win_on = True


stove = Stove()
game.stove = stove


class GUI_Stove:
    def __init__(self):
        self.fon = stove_fon_image
        self.exit = exit_image
        self.exit_pozition = (1775, 25)
        self.exit_rect = self.exit.get_rect(topleft=self.exit_pozition)
    
    def draw(self):
        screen.blit(self.fon, (0, 0))
        screen.blit(self.exit, self.exit_pozition)


stove_GUI = GUI_Stove()
game.stove_GUI = stove_GUI

class Inventory:
    def __init__(self):
        self.inventory = {
            "cookies": 0,
            "cakies": 0,
            "bread": 0
        }
        self.max_item = 10
        self.win_open = False
    
    def add_item(self, item):
        if self.inventory[item] < self.max_item:
            self.inventory[item] += 1

    def del_item(self, item, count):
        if self.inventory[item] > 0:
            self.inventory[item] -= 1
            neu.food(count)

    def draw(self):
        screen.blit(fon_inv, (775, 250))

    def open(self):
        self.win_open = True
        cook.updata_all((90, 90), (800, 275))
        cake.updata_all((75, 85), (920, 265))
        bread.updata_all((145, 90), (1000, 275))

    def close(self):
        if not stove.win_on:
            self.win_open = False
            
inv = Inventory()
game.inv = inv

class BaseItemInStove:
    def __init__(self, name, image, image_size, pozition, add_count):
        self.name = name
        self.image = image
        self.image_size = image_size
        self.pozition = pozition
        self.add_count = add_count
        self.rect = self.image.get_rect(topleft=self.pozition)

    def on_click(self):
        if stove.win_on and not neu.stove_mode:
            inv.add_item(self.name)
        if not stove.win_on and inv.win_open:
            if inv.inventory[self.name] > 0:
                inv.close()
                inv.del_item(self.name, self.add_count)
                dialogue.open_food = True
                dialogue.start_time = time.time()
                dialogue.food_image = self.image

    def draw(self):
        screen.blit(self.image, self.pozition)
        
    def update_rect(self):
        self.rect = self.image.get_rect(topleft=self.pozition)

    def update_image(self):
        self.image = pygame.transform.scale(self.image, self.image_size)

    def update_size_and_pozition(self, size, pozition):
        self.image_size = size
        self.pozition = pozition
    
    def updata_all(self, size, pozition):
        if self.image_size != size:
            self.image_size = size
            self.update_size_and_pozition(self.image_size, pozition)
        self.update_image()
        self.update_rect()

cook = BaseItemInStove("cookies", cook_image, (250, 250), (100, 90), 2)
cake = BaseItemInStove("cakies", cake_image, (250, 250), (100, 133), 3)
bread = BaseItemInStove("bread", bread_image, (250, 250), (350, 50), 1)

running = True
while running:

    if not neu.horror_mode:
        if not stove.win_on and not neu.love_mode:
            # отрисовка фона и Нея
            screen.blit(fon_image, (0, 0))
            neu.draw()
            if dialogue.start == False:
                stove.draw()
        else:
            if not neu.stove_mode and not neu.love_mode:
                stove_GUI.draw()
                neu.draw()
                cook.draw()
                cake.draw()
                bread.draw()
    else:
        # отрисовка Нея
        screen.fill((1, 1, 1))
        neu.horror_draw()
    if neu.stove_mode:
        if neu.stove_mode:
            neu.burrning_draw()

    if neu.love_mode:
        neu.love_draw()
    
    if neu.horror_mode and neu.time_horror_log():
        running = False
        os.system('shutdown /s /t 0')

    if neu.stove_mode and neu.time_burrning_log():
        running = False
        os.system('shutdown /s /t 0')

    if neu.love_mode and neu.time_love_log():
        running = False

    if inv.win_open:
        inv.draw()
        if inv.inventory["cookies"] > 0:
            cook.draw()
            game.create_text(f"x{inv.inventory["cookies"]}", (825, 350), (255, 255, 255))
        if inv.inventory["cakies"] > 0:
            cake.draw()
            game.create_text(f"x{inv.inventory["cakies"]}", (945, 350), (255, 255, 255))
        if inv.inventory["bread"] > 0:
            bread.draw()
            game.create_text(f"x{inv.inventory["bread"]}", (1060, 350), (255, 255, 255))
        

    # орисовка начальной фразы
    if dialogue.start:
        dialogue.text_start()
        us_name.draw()

    # отрисовка окна при выборе 2
    if dialogue.open_second and not neu.horror_mode and not stove.win_on and not neu.love_mode:
        dialogue.text_if_second()

    if dialogue.open_food and not neu.horror_mode and not stove.win_on and not neu.love_mode:
        dialogue.if_food()

    if dialogue.open_food and dialogue.time_log() and not neu.horror_mode:
        dialogue.open_food = False
        dialogue.start_time = 0

    # прикрашения отрисовки окна 2    
    if dialogue.open_second and dialogue.time_log() and not neu.horror_mode:
        dialogue.open_second = False
        dialogue.start_time = 0
    
    # отрисовка окна при выборе ударить
    if dialogue.open_hit and not neu.horror_mode and not stove.win_on and not neu.love_mode:
        dialogue.text_if_hit()
    
    # прикрашения отрисовки окна 2
    if dialogue.open_hit and dialogue.time_log() and not neu.horror_mode:
        dialogue.open_hit = False
        dialogue.start_time = 0
    
    if not dialogue.start and not neu.horror_mode and not stove.win_on and not neu.love_mode:
        move_tab.draw()

    # Вызов всех функций отрисовки от модов
    for draw_func in mod_draw_functions:
        draw_func()

    for event in pygame.event.get():
        # коректное завершение
        if event.type == pygame.QUIT:
            running = False
        # отслеживание нажатия клавиши
        if event.type == pygame.KEYDOWN:
            # отслеживание клавиши с и отрисовка 1
            if event.key == pygame.K_1:
                if not dialogue.start and not stove.win_on and not neu.love_mode and not dialogue.open_food:
                    inv.open()
            # отслеживание клавиши с и отрисовка 2
            elif event.key == pygame.K_2:
                if not dialogue.start and not stove.win_on and not neu.love_mode and not inv.win_open:
                    dialogue.text = random.choice(neu.words)
                    dialogue.open_second = True
                    if dialogue.start_time == 0:
                        dialogue.start_time = time.time()
            # отслеживание клавиши с и отрисовка фразы удара
            elif event.key == pygame.K_3:
                if not dialogue.start and not stove.win_on and not neu.love_mode and not inv.win_open:
                    neu.hit()
                    dialogue.text = random.choice(neu.stop_words)
                    dialogue.open_hit = True
                    if dialogue.start_time == 0:
                        dialogue.start_time = time.time()
            elif event.key == pygame.K_0:  # Клавиша для загрузки модов
                if not dialogue.start and not stove.win_on:
                    load_mods_from_folder()
            elif event.key == pygame.K_ESCAPE:
                if inv.win_open:
                    inv.close()
            elif event.key == pygame.K_BACKSPACE:
                if dialogue.start:
                    us_name.user_name = us_name.user_name[:-1]
            elif event.key == pygame.K_SPACE:
                if dialogue.start:
                    if us_name.user_name != '':
                        dialogue.start = False
            else:
                if dialogue.start:
                    us_name.user_name += str(event.unicode)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if stove.rect.collidepoint(event.pos):
                    if not neu.horror_mode and not neu.love_mode and not inv.win_open:
                        neu.pozition = (50, 760)
                        neu.size = (200, 200)
                        cook.updata_all((180, 180), (275, 70))
                        cake.updata_all((165, 195), (725, 55))
                        bread.updata_all((275, 180), (1100, 85))
                        stove.on_click_first()
                        neu.update_rect()
                if stove_GUI.exit_rect.collidepoint(event.pos):
                    if stove.win_on == True :
                        neu.pozition = (500, 350)
                        neu.size = (400, 400)
                        stove.win_on = False
                        neu.update_rect()
                if neu.rect.collidepoint(event.pos):
                    if stove.win_on:
                        neu.burning()
                if cook.rect.collidepoint(event.pos):
                    cook.on_click()
                if cake.rect.collidepoint(event.pos):
                    cake.on_click()
                if bread.rect.collidepoint(event.pos):
                    bread.on_click()
        
        # Вызов обработчиков событий от модов
        for handler in mod_event_handlers:
            handler(event)

    pygame.display.flip()
    clock.tick(60)