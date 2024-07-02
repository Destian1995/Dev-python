import pygame
import os
import random

def check_files(directory, extensions):
    files = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            file_extension = os.path.splitext(filename)[1][1:].lower()
            if file_extension in extensions:
                files.append(filepath)
    return files

# Путь к спрайтам
directory_path = r"C:\Users\User\Desktop\C.P.E\sprites"
extensions_to_check = ['png', 'jpg']
found_files = check_files(directory_path, extensions_to_check)
print("Найденные файлы:", found_files)

# Путь к изображениям баз и объектов
base_image_path1 = r"C:\Users\User\Desktop\C.P.E\base\base1.png" # Изображение для базы 1
base_image_path2 = r"C:\Users\User\Desktop\C.P.E\base\base2.png" # Изображение для базы 2
industry_image_path = r"C:\Users\User\Desktop\C.P.E\main_resources\industry.png" # Изображение для industry
surie_image_path = r"C:\Users\User\Desktop\C.P.E\main_resources\surie.png" # Изображение для surie
forest_image_path = r"C:\Users\User\Desktop\C.P.E\alls\forest.png" # Изображение для леса

# Инициализация Pygame
pygame.init()

# Настройка окна
screen_width = 1200
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("C.P.E.")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BEIGE = (222, 184, 135)
PANEL = (100, 149, 237)

# Шрифты
font = pygame.font.Font(None, 24)
menu_font = pygame.font.Font(None, 72)

class Forest:
    def __init__(self, x, y, image_path):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Map:
    def __init__(self, width, height, base_positions):
        self.width = width
        self.height = height
        self.buildings = []
        self.forests = []
        self.base_positions = base_positions
        self.generate_map()

    def generate_map(self):
        def is_overlapping(x, y, width, height, other_rects):
            for ox, oy, owidth, oheight in other_rects:
                if (x < ox + owidth and x + width > ox and y < oy + oheight and y + height > oy):
                    return True
            return False

        all_objects = self.base_positions

        # Генерация зданий
        num_buildings = random.randint(4, 7)
        for _ in range(num_buildings):
            while True:
                x = random.randint(0, self.width - 100)
                y = random.randint(0, self.height - 50)
                if not is_overlapping(x, y, 190, 50, all_objects):
                    self.buildings.append((x, y, 190, 50))
                    all_objects.append((x, y, 190, 50))
                    break

        # Генерация лесов
        num_forests = random.randint(12, 19)
        for _ in range(num_forests):
            while True:
                x = random.randint(0, self.width - 50)
                y = random.randint(0, self.height - 50)
                if not is_overlapping(x, y, 50, 50, all_objects):
                    forest = Forest(x, y, forest_image_path)
                    self.forests.append(forest)
                    all_objects.append((x, y, 50, 50))
                    break

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (0, 0, self.width, self.height))
        for x, y, width, height in self.buildings:
            pygame.draw.rect(screen, GREY, (x, y, width, height))
            self.draw_building_windows(screen, x, y, width, height)
        for forest in self.forests:
            forest.draw(screen)

    def draw_building_windows(self, screen, x, y, width, height):
        window_size = 10
        window_spacing = 5
        for row in range(y + window_spacing, y + height - window_size, window_size + window_spacing):
            for col in range(x + window_spacing, x + width - window_size, window_size + window_spacing):
                pygame.draw.rect(screen, WHITE, (col, row, window_size, window_size))

class Base:
    def __init__(self, x, y, image_path, player_controlled=False):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.resources = {'сырье': 100, 'железная руда': 50, 'провизия': 500, 'людей': 10, 'деньги': 20}
        self.player_controlled = player_controlled
        self.buildings = []

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def build(self, building_type, x, y):
        building = Building(x, y, building_type, self)
        self.buildings.append(building)
        print(f"Строится здание '{building_type}'")

    def upgrade(self):
        # Логика улучшения базы (например, увеличение количества ресурсов)
        print("База улучшена!")

class Resource:
    def __init__(self, x, y, image_path, resource_type):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.resource_type = resource_type

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def collect(self):
        # Функция для сбора ресурса
        if self.resource_type == 'industry':
            print("Собираем железную руду")
        elif self.resource_type == 'surie':
            print("Собираем сырье")

    def is_near_base(self, base):
        # Проверка, находится ли ресурс рядом с базой
        distance = ((self.x - base.x) ** 2 + (self.y - base.y) ** 2) ** 0.5
        return distance <= 100

    # Метод для получения координат центра ресурса (для строительства зданий)
    def get_center(self):
        return self.x + self.rect.width // 2, self.y + self.rect.height // 2

class Applet:
    def __init__(self, x, y, width, height, base):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.base = base

    def draw(self, screen):
        pygame.draw.rect(screen, PANEL, (self.x, self.y, self.width, self.height))
        pygame.draw.line(screen, WHITE, (self.x, self.y), (self.x + self.width, self.y), 5)
        resource_y = self.y + 15
        for resource_name, amount in self.base.resources.items():
            text = font.render(f"{resource_name}: {amount}", True, WHITE)
            screen.blit(text, (self.x + 10, resource_y))
            resource_y += 25

class Button:
    def __init__(self, x, y, width, height, text, font=font):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font

    def draw(self, screen):
        pygame.draw.rect(screen, BEIGE, (self.x, self.y, self.width, self.height))
        text = self.font.render(self.text, True, WHITE)
        text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text, text_rect)

    def is_clicked(self, mouse_pos):
        if self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height:
            return True
        return False

class MainMenu:
    def __init__(self):
        self.start_button = Button(screen_width // 2 - 150, screen_height // 2 - 50, 300, 60, "Старт", font=menu_font)
        self.exit_button = Button(screen_width // 2 - 150, screen_height // 2 + 50, 300, 60, "Выход", font=menu_font)

    def draw(self, screen):
        screen.fill(BLACK)
        self.start_button.draw(screen)
        self.exit_button.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.is_clicked(pygame.mouse.get_pos()):
                return 'start'
            if self.exit_button.is_clicked(pygame.mouse.get_pos()):
                return 'exit'
        return None

def is_overlapping(x, y, width, height, other_rects):
    for ox, oy, owidth, oheight in other_rects:
        if (x < ox + owidth and x + width > ox and y < oy + oheight and y + height > oy):
            return True
    return False

def create_resources_around_base(base, all_objects):
    resources = []
    resource_types = [('industry', industry_image_path), ('surie', surie_image_path)]
    for resource_type, image_path in resource_types:
        while True:
            x = base.x + random.randint(-50, 110)
            y = base.y + random.randint(-50, 110)
            if not is_overlapping(x, y, 70, 70, all_objects): # Предположим, что размер ресурсов 70x70
                resource = Resource(x, y, image_path, resource_type)
                resources.append(resource)
                all_objects.append((x, y, 70, 70))
                break
    return resources


class Building:
    def __init__(self, x, y, building_type, base):
        self.x = x
        self.y = y
        self.building_type = building_type
        self.base = base
        self.level = 1
        self.production_rate = self.get_initial_production_rate()
        self.upgrade_cost = self.get_upgrade_cost()

    def get_initial_production_rate(self):
        if self.building_type == 'industry':
            return 45  # Железо в минуту
        elif self.building_type == 'surie':
            return 55  # Сырье в минуту

    def get_upgrade_cost(self):
        return 100 * self.level  # Стоимость улучшения (монеты)

    def upgrade(self):
        if self.base.resources['деньги'] >= self.upgrade_cost:
            self.base.resources['деньги'] -= self.upgrade_cost
            self.level += 1
            self.production_rate *= 1.35  # Увеличение производства на 35%
            self.upgrade_cost = self.get_upgrade_cost()
            print(f"Здание '{self.building_type}' улучшено до уровня {self.level}")
        else:
            print("Недостаточно ресурсов для улучшения")



# Цикл игры
status_game = True
game_state = 'menu'
base1 = Base(50, 50, base_image_path1, player_controlled=False)  # Противник
base2 = Base(900, 500, base_image_path2, player_controlled=True) # Игрок
all_objects = [(base1.x, base1.y, base1.rect.width, base1.rect.height),
               (base2.x, base2.y, base2.rect.width, base2.rect.height)]
resources = create_resources_around_base(base1, all_objects) + create_resources_around_base(base2, all_objects)
map = Map(screen_width, screen_height - 200, all_objects)

# Апплет
applet = Applet(0, screen_height - 200, screen_width, 150, base1)

# Кнопки
build_button = Button(10, screen_height - 40, 100, 30, "Стройка")
upgrade_button = Button(120, screen_height - 40, 110, 30, "Улучшения")
unit_button = Button(240, screen_height - 40, 110, 30, "Армия")

# Главное меню
main_menu = MainMenu()

while status_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status_game = False

        if game_state == 'menu':
            result = main_menu.handle_event(event)
            if result == 'start':
                game_state = 'game'
            elif result == 'exit':
                status_game = False
        elif game_state == 'game':
            if event.type == pygame.MOUSEBUTTONDOWN:
                if upgrade_button.is_clicked(pygame.mouse.get_pos()):  # Проверяем, была ли нажата кнопка "Улучшение"
                    for building in base2.buildings:  # Проверяем, было ли нажато на здание
                        if building.rect.collidepoint(event.pos):
                            building.upgrade()  # Улучшаем здание
                            break
                if upgrade_button.is_clicked(pygame.mouse.get_pos()):
                    print("Клик по кнопке Улучшения")
                if unit_button.is_clicked(pygame.mouse.get_pos()):
                    print("Клик по кнопке Юниты")

    # Отрисовка
    if game_state == 'menu':
        main_menu.draw(screen)
    elif game_state == 'game':
        screen.fill(BLACK)
        map.draw(screen)
        base1.draw(screen)
        base2.draw(screen)
        for resource in resources:
            resource.draw(screen)
        applet.draw(screen)

        build_button.draw(screen)
        upgrade_button.draw(screen)
        unit_button.draw(screen)

    pygame.display.flip()

pygame.quit()
