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
        self.iron = 0
        self.surie = 0
        self.provision = 0
        self.people = 0
        self.money = 200
        self.resources = {'сырье': self.surie, 'железная руда': self.iron, 'провизия': self.provision,
                          'люди': self.people, 'деньги': self.money}
        self.player_controlled = player_controlled
        self.buildings = []

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def progress(self):
        # Логика улучшения технологий
        print("База улучшена!")

class Economic(Base):
    def __init__(self, x, y, image_path, resource_type, production_rate=15):
        super().__init__(x, y, image_path)
        self.resource_type = resource_type
        self.production_rate = production_rate
        self.resources = {self.resource_type: 0}
        self.upgrade_button_rect = pygame.Rect(self.x, self.y + self.image.get_height(), 100, 40)
        self.show_upgrade_window = False
        self.upgrade_coefficients = {
            'iron': 1.0,
            'surie': 1.0,
            'people': 1.0
        }

    def draw(self, screen):
        super().draw(screen)

    def profit(self):
        self.resources[self.resource_type] += self.production_rate * self.upgrade_coefficients[self.resource_type]

    def draw_upgrade_window(self, screen):
        window_width = 600
        window_height = 200
        window_x = (screen_width - window_width) // 2
        window_y = (screen_height - window_height) // 2
        pygame.draw.rect(screen, GREY, (window_x, window_y, window_width, window_height))
        pygame.draw.rect(screen, BLACK, (window_x, window_y, window_width, window_height), 2)

        title_text = font.render("Поднятие уровня экономики", True, WHITE)
        screen.blit(title_text, (window_x + 60, window_y + 10))

        upgrade_button_rect_iron = pygame.Rect(window_x + 50, window_y + 40, 300, 30)
        pygame.draw.rect(screen, BEIGE, upgrade_button_rect_iron)
        upgrade_button_rect_surie = pygame.Rect(window_x + 50, window_y + 80, 300, 30)
        pygame.draw.rect(screen, BEIGE, upgrade_button_rect_surie)
        upgrade_button_rect_people = pygame.Rect(window_x + 50, window_y + 120, 300, 30)
        pygame.draw.rect(screen, BEIGE, upgrade_button_rect_people)
        upgrade_button_text_iron = font.render("Улучшить производство железа", True, BLACK)
        screen.blit(upgrade_button_text_iron, (upgrade_button_rect_iron.x + 10, upgrade_button_rect_iron.y + 5))
        upgrade_button_text_surie = font.render("Улучшить производство сырья", True, BLACK)
        screen.blit(upgrade_button_text_surie, (upgrade_button_rect_surie.x + 10, upgrade_button_rect_surie.y + 5))
        upgrade_button_text_people = font.render("Улучшить содержание людей", True, BLACK)
        screen.blit(upgrade_button_text_people, (upgrade_button_rect_people.x + 10, upgrade_button_rect_people.y + 5))

        cost_text_iron = font.render(f"Стоимость: {self.production_rate * 5} денег", True, WHITE)
        screen.blit(cost_text_iron, (window_x + 370, window_y + 50))
        cost_text_surie = font.render(f"Стоимость: {self.production_rate * 3} денег", True, WHITE)
        screen.blit(cost_text_surie, (window_x + 370, window_y + 90))
        cost_text_people = font.render(f"Стоимость: {self.production_rate * 1} денег", True, WHITE)
        screen.blit(cost_text_people, (window_x + 370, window_y + 130))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            window_width = 600
            window_height = 200
            window_x = (screen_width - window_width) // 2
            window_y = (screen_height - window_height) // 2
            upgrade_button_rect_iron = pygame.Rect(window_x + 50, window_y + 40, 300, 30)
            upgrade_button_rect_surie = pygame.Rect(window_x + 50, window_y + 80, 300, 30)
            upgrade_button_rect_people = pygame.Rect(window_x + 50, window_y + 120, 300, 30)
            if upgrade_button_rect_iron.collidepoint(mouse_pos):
                self.upgrade('iron')
                self.show_upgrade_window = False
            elif upgrade_button_rect_surie.collidepoint(mouse_pos):
                self.upgrade('surie')
                self.show_upgrade_window = False
            elif upgrade_button_rect_people.collidepoint(mouse_pos):
                self.upgrade('people')
                self.show_upgrade_window = False

    def upgrade(self, resource_type):
        # Логика улучшения
        upgrade_cost = self.production_rate * {'iron': 5, 'surie': 3, 'people': 1}[resource_type]
        if self.money >= upgrade_cost:
            self.money -= upgrade_cost
            self.upgrade_coefficients[resource_type] += 0.1  # Увеличение коэффициента на 10%
            print(f"Улучшение {resource_type} выполнено!")
        else:
            print("Недостаточно денег для улучшения!")

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

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
        self.start_button = Button(screen_width // 2 - 100, screen_height // 2 - 25, 200, 50, "Играть")
        self.exit_button = Button(screen_width // 2 - 100, screen_height // 2 + 50, 200, 50, "Выход")

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
                resource = Economic(x, y, image_path, resource_type)
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
economic = Economic(400, 350, base_image_path2, "iron", 15)
# Апплет
applet = Applet(0, screen_height - 200, screen_width, 150, base2)

# Кнопки
economic_button = Button(10, screen_height - 40, 100, 30, "Экономика")
progress_button = Button(120, screen_height - 40, 110, 30, "Прогресс")
army_button = Button(240, screen_height - 40, 110, 30, "Армия")
exchange_button = Button(360, screen_height - 40, 110, 30, "Рынок")
diplomacy_button = Button(480, screen_height - 40, 110, 30, "Дипломатия")
exit_button = Button(1000, screen_height - 40, 170, 30, "Выход из игры")

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
                    status_game = False
            if economic.show_upgrade_window:
                economic.handle_event(event)

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

        economic_button.draw(screen)
        progress_button.draw(screen)
        army_button.draw(screen)
        exchange_button.draw(screen)
        diplomacy_button.draw(screen)
        exit_button.draw(screen)

        if economic.show_upgrade_window:
            economic.draw_upgrade_window(screen)

    pygame.display.flip()

pygame.quit()
