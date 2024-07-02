import pygame
import os
import random

def check_files(directory, extensions):
  """
  Проверяет наличие файлов с заданными расширениями в указанном каталоге.

  Args:
    directory: Строка, путь к каталоге.
    extensions: Список строк, расширения файлов для проверки (['png', 'jpg']).

  Returns:
    Список файлов, найденных в каталоге.
  """
  files = []
  for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)
    if os.path.isfile(filepath):
      file_extension = os.path.splitext(filename)[1][1:].lower()
      if file_extension in extensions:
        files.append(filepath)
  return files

directory_path = r"C:\Users\User\Desktop\sprites" # Путь со спрайтами
extensions_to_check = ['png', 'jpg'] # Расширения
found_files = check_files(directory_path, extensions_to_check)
print("Найденные файлы:", found_files)

# Инициализация Pygame
pygame.init()

# Настройка окна
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)

# Шрифты
font = pygame.font.Font(None, 24)

# Класс карты
class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (0, 0, self.width, self.height))

# Класс базы
class Base:
    def __init__(self, x, y, player_controlled=False):
        self.x = x
        self.y = y
        self.resources = {'сырье': 100, 'электроника': 50, 'провизия': 500,'людей': 10, 'деньги': 20}
        self.player_controlled = player_controlled

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, 60, 60))

# Класс апплета с кнопками и ресурсами
class Applet:
    def __init__(self, x, y, width, height, base):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.base = base

    def draw(self, screen):
        pygame.draw.rect(screen, GREY, (self.x, self.y, self.width, self.height))

        # Отображаем данные
        resource_y = self.y + 15
        for resource_name, amount in self.base.resources.items():
            text = font.render(f"{resource_name}: {amount}", True, WHITE)
            screen.blit(text, (self.x + 10, resource_y))
            resource_y += 25

# Класс кнопки
class Button:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, GREY, (self.x, self.y, self.width, self.height))
        text = font.render(self.text, True, WHITE)
        text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text, text_rect)

    def is_clicked(self, mouse_pos):
        if self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height:
            return True
        return False

# Цикл игры
status_game = True
map = Map(screen_width, screen_height)
base1 = Base(50, 50, player_controlled=True)
base2 = Base(900, 500, player_controlled=False)

# Апплет
applet = Applet(10, screen_height - 220, 360, 150, base1)

# Кнопки
build_button = Button(10, screen_height - 60, 100, 40, "Стройка")
upgrade_button = Button(120, screen_height - 60, 110, 40, "Улучшения")
unit_button = Button(240, screen_height - 60, 130, 40, "Набор людей")

while status_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status_game = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if build_button.is_clicked(pygame.mouse.get_pos()):
                print("Клик по кнопке Стройка")
            if upgrade_button.is_clicked(pygame.mouse.get_pos()):
                print("Клик по кнопке Улучшения")
            if unit_button.is_clicked(pygame.mouse.get_pos()):
                print("Клик по кнопке Юниты")

    # Отрисовка
    screen.fill(BLACK)
    map.draw(screen)
    base1.draw(screen)
    base2.draw(screen)
    applet.draw(screen)

    # Отрисовка кнопок
    build_button.draw(screen)
    upgrade_button.draw(screen)
    unit_button.draw(screen)

    pygame.display.flip()

pygame.quit()
