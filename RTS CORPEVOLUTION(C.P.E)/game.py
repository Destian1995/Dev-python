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
base_image_path1 = r"C:\Users\User\Desktop\C.P.E\base\base1.png"  # Изображение для базы 1
base_image_path2 = r"C:\Users\User\Desktop\C.P.E\base\base2.png"  # Изображение для базы 2
industry_image_path = r"C:\Users\User\Desktop\C.P.E\main_resources\industry.png"  # Изображение для industry
surie_image_path = r"C:\Users\User\Desktop\C.P.E\main_resources\surie.png"  # Изображение для surie
forest_image_path = r"C:\Users\User\Desktop\C.P.E\alls\forest.png"  # Изображение для леса

# Инициализация Pygame
pygame.init()

# Настройка окна
screen_width = 1200
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))


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
    def __init__(self, x, y, image_path, player_controlled=True, resource_type=None, production_rate=15):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.iron = 0
        self.surie = 0
        self.provision = 0
        self.people = 0
        self.money = 200
        self.resources = {'сырье': self.surie, 'железная руда': self.iron, 'провизия': self.provision,
                          'люди': self.people, 'деньги': self.money}
        self.player_controlled = player_controlled
        self.buildings = []
        self.upgrade_coefficients = {
            'железная руда': 1.0,
            'сырье': 1.0,
            'провизия': 1.0,
            'деньги': 1.0
        }
        self.slowdown_factor = 0.01  # Коэффициент замедления

        self.resource_type = resource_type
        self.production_rate = production_rate
        self.upgrade_button_rect = pygame.Rect(self.x, self.y + self.image.get_height(), 100, 40)
        self.show_upgrade_window = False
        self.summ_upgrade_iron = self.production_rate * 5
        self.summ_upgrade_surie = self.production_rate * 3
        self.summ_upgrade_people = self.production_rate * 1

    def draw_upgrade_window(self, screen):
        window_width = 600
        window_height = 200
        window_x = (screen_width - window_width) // 2
        window_y = (screen_height - window_height) // 2
        pygame.draw.rect(screen, GREY, (window_x, window_y, window_width, window_height))
        pygame.draw.rect(screen, BLACK, (window_x, window_y, window_width, window_height), 2)

        title_text = font.render("Поднятие уровня экономики", True, WHITE)
        screen.blit(title_text, (window_x + 60, window_y + 10))

        # Создание кнопок с использованием класса Button
        self.upgrade_button_iron = Button(window_x + 50, window_y + 40, 300, 30, "Улучшить производство железа", self.upgrade)
        self.upgrade_button_surie = Button(window_x + 50, window_y + 80, 300, 30, "Улучшить производство сырья", self.upgrade)
        self.upgrade_button_people = Button(window_x + 50, window_y + 120, 300, 30, "Улучшить содержание людей", self.upgrade)

        # Отрисовка кнопок
        self.upgrade_button_iron.draw(screen)
        self.upgrade_button_surie.draw(screen)
        self.upgrade_button_people.draw(screen)

        # Отрисовка текста стоимости рядом с каждой кнопкой
        cost_text_iron = font.render(f"Стоимость: {self.summ_upgrade_iron} монет", True, WHITE)
        screen.blit(cost_text_iron, (window_x + 370, window_y + 50))
        cost_text_surie = font.render(f"Стоимость: {self.summ_upgrade_surie} монет", True, WHITE)
        screen.blit(cost_text_surie, (window_x + 370, window_y + 90))
        cost_text_people = font.render(f"Стоимость: {self.summ_upgrade_people} монет", True, WHITE)
        screen.blit(cost_text_people, (window_x + 370, window_y + 130))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        if self.show_upgrade_window:
            self.draw_upgrade_window(screen)

    def produce_resources(self):
        # Базовый прирост ресурсов
        base_production = {
            'сырье': 3,
            'железная руда': 1.2,
            'провизия': 2,
            'деньги': 1.4
        }
        for resource, base_amount in base_production.items():
            self.resources[resource] = round(self.resources[resource] + base_amount * self.upgrade_coefficients[resource] * self.slowdown_factor, 2)

    def update_resources(self):
        self.resources['сырье'] = self.surie
        self.resources['железная руда'] = self.iron
        self.resources['провизия'] = self.provision
        self.resources['люди'] = self.people
        self.resources['деньги'] = self.money

    def deduct_money(self, amount):
        if self.resources['деньги'] >= amount:
            self.resources['деньги'] -= amount
            self.update_resources()
            return True
        else:
            return False

    def handle_event(self, event, screen_width, screen_height):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.upgrade_button_rect.collidepoint(mouse_pos):
                self.show_upgrade_window = True

            if self.show_upgrade_window:
                window_width = 600
                window_height = 200
                window_x = (screen_width - window_width) // 2
                window_y = (screen_height - window_height) // 2

                buttons = [
                    pygame.Rect(window_x + 50, window_y + 40, 300, 30),
                    pygame.Rect(window_x + 50, window_y + 80, 300, 30),
                    pygame.Rect(window_x + 50, window_y + 120, 300, 30),
                ]

                for i, button_rect in enumerate(buttons):
                    if button_rect.collidepoint(mouse_pos):
                        resource_type = ['железная руда', 'сырье', 'деньги'][i]
                        self.upgrade(resource_type)
                        self.show_upgrade_window = False
                        break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.show_upgrade_window = False

    def upgrade(self, resource_type):
        if resource_type == 'железная руда':
            upgrade_cost = self.summ_upgrade_iron
        elif resource_type == 'сырье':
            upgrade_cost = self.summ_upgrade_surie
        elif resource_type == 'деньги':
            upgrade_cost = self.summ_upgrade_people
        else:
            upgrade_cost = 0

        if self.deduct_money(upgrade_cost):
            self.upgrade_coefficients[resource_type] *= 1.1  # Increase coefficient by 10%
            print(f"Улучшение {resource_type} выполнено!")
        else:
            print("Недостаточно денег для улучшения!")


class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, BEIGE, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        text_surf = font.render(self.text, True, BLACK)
        screen.blit(text_surf, (self.rect.x + (self.rect.width - text_surf.get_width()) // 2,
                                self.rect.y + (self.rect.height - text_surf.get_height()) // 2))

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class Applet:
    def __init__(self, x, y, width, height, base):
        self.rect = pygame.Rect(x, y, width, height)
        self.base = base

    def draw(self, screen):
        pygame.draw.rect(screen, PANEL, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        for i, (resource, amount) in enumerate(self.base.resources.items()):
            resource_text = font.render(f"{resource}: {amount}", True, BLACK)
            screen.blit(resource_text, (self.rect.x + 10, self.rect.y + 10 + i * 30))


class MainMenu:
    def __init__(self):
        self.title = "Эволюция войн"
        self.start_button = Button(screen_width // 2 - 100, screen_height // 2 - 25, 200, 50, "Игра", None)
        self.exit_button = Button(screen_width // 2 - 100, screen_height // 2 + 50, 200, 50, "Выход", None)

    def draw(self, screen):
        screen.fill(BLACK)
        title_surf = menu_font.render(self.title, True, WHITE)
        screen.blit(title_surf, (screen_width // 2 - title_surf.get_width() // 2, screen_height // 2 - 100))
        self.start_button.draw(screen)
        self.exit_button.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.start_button.is_clicked(mouse_pos):
                return 'start'
            elif self.exit_button.is_clicked(mouse_pos):
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
            if not is_overlapping(x, y, 70, 70, all_objects):  # Предположим, что размер ресурсов 70x70
                resource = Base(x, y, image_path, player_controlled=True, resource_type="сырье", production_rate=15)
                resources.append(resource)
                all_objects.append((x, y, 70, 70))
                break
    return resources

# Основной игровой цикл
status_game = True
game_state = 'menu'
base1 = Base(50, 50, base_image_path1, player_controlled=False)  # Противник
base2 = Base(900, 500, base_image_path2, player_controlled=True)  # Игрок
all_objects = [(base1.x, base1.y, base1.rect.width, base1.rect.height),
               (base2.x, base2.y, base2.rect.width, base2.rect.height)]
resources = create_resources_around_base(base1, all_objects) + create_resources_around_base(base2, all_objects)
map = Map(screen_width, screen_height - 200, all_objects)
economic = Base(400, 350, base_image_path2, player_controlled=True, resource_type="железная руда", production_rate=15)
# Апплет
applet = Applet(0, screen_height - 200, screen_width, 150, base2)

# Кнопки
economic_button = Button(10, screen_height - 40, 100, 30, "Экономика", None)
progress_button = Button(120, screen_height - 40, 110, 30, "Прогресс", None)
army_button = Button(240, screen_height - 40, 110, 30, "Армия", None)
exchange_button = Button(360, screen_height - 40, 110, 30, "Рынок", None)
diplomacy_button = Button(480, screen_height - 40, 110, 30, "Дипломатия", None)
exit_button = Button(1000, screen_height - 40, 170, 30, "Пауза", None)

# Главное меню
main_menu = MainMenu()

# Основной игровой цикл
clock = pygame.time.Clock()

# Основной игровой цикл
while status_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status_game = False  # Выход из игры при закрытии окна

        if game_state == 'menu':
            result = main_menu.handle_event(event)  # Обработка событий главного меню
            if result == 'start':
                game_state = 'game'  # Переход в игровой режим при выборе "начать игру"
            elif result == 'exit':
                status_game = False  # Выход из игры при выборе "выход"

        elif game_state == 'game':
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Обработка нажатия кнопок
                if economic_button.is_clicked(pygame.mouse.get_pos()):
                    print("Экономика")
                    economic.show_upgrade_window = True
                if progress_button.is_clicked(pygame.mouse.get_pos()):
                    print("Прогресс")
                if army_button.is_clicked(pygame.mouse.get_pos()):
                    print("Армия")
                if exchange_button.is_clicked(pygame.mouse.get_pos()):
                    print("Рынок")
                if diplomacy_button.is_clicked(pygame.mouse.get_pos()):
                    print("Дипломатия")
                if exit_button.is_clicked(pygame.mouse.get_pos()):
                    game_state = 'menu'  # Возврат в главное меню при нажатии "пауза"

                if economic.show_upgrade_window:
                    economic.handle_event(event, screen_width, screen_height)

    # Обновление ресурсов базы игрока в игровом режиме
    if game_state == 'game':
        base2.produce_resources()

    # Отрисовка экрана в зависимости от текущего состояния игры
    if game_state == 'menu':
        main_menu.draw(screen)  # Отображение главного меню
    elif game_state == 'game':
        screen.fill(BLACK)  # Заливка экрана черным цветом
        map.draw(screen)  # Отрисовка карты
        base1.draw(screen)  # Отрисовка базы противника
        base2.draw(screen)  # Отрисовка базы игрока
        for resource in resources:
            resource.draw(screen)  # Отрисовка ресурсов около баз
        applet.draw(screen)  # Отрисовка апплета снизу

        # Отрисовка кнопок
        economic_button.draw(screen)
        progress_button.draw(screen)
        army_button.draw(screen)
        exchange_button.draw(screen)
        diplomacy_button.draw(screen)
        exit_button.draw(screen)

        # Отображение окна улучшения экономической базы, если оно активировано
        if economic.show_upgrade_window:
            economic.draw_upgrade_window(screen)

    pygame.display.flip()  # Обновление экрана
    clock.tick(90)  # Ограничение частоты кадров

pygame.quit()  # Выход из Pygame при завершении игры
