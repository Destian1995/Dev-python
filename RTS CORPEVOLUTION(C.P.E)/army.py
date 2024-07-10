import pygame
import math
from progress_tab import *

images_path = r'C:\Users\User\Desktop\C.P.E'
unit_opolchenec = images_path + r'\units\base2\opolch.png'
unit_bronemashina = images_path + r'\units\base2\bronemashina.png'
unit_shturmovik = images_path + r'\units\base2\shturmovik.png'
unit_tank = images_path + r'\units\base2\tank.png'
unit_btr = images_path + r'\units\base2\btr.png'

class Unit:
    def __init__(self, image_path, x, y, speed):
        self.image = pygame.image.load(image_path)
        self.x = x
        self.y = y
        self.speed = speed
        self.target_position = None

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def update(self):
        if self.target_position:
            target_x, target_y = self.target_position
            distance = math.hypot(target_x - self.x, target_y - self.y)
            if distance > self.speed:
                direction_x = (target_x - self.x) / distance
                direction_y = (target_y - self.y) / distance
                self.x += direction_x * self.speed
                self.y += direction_y * self.speed
            else:
                self.target_position = None

    def set_target_position(self, target_position):
        self.target_position = target_position

class UnitButton:
    def __init__(self, x, y, width, height, text, icon_path, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.icon = pygame.image.load(icon_path)  # Загрузка изображения
        self.icon = pygame.transform.scale(self.icon, (width - 20, height - 20))
        self.action = action

    def draw(self, screen, font):
        pygame.draw.rect(screen, (222, 184, 135), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        icon_x = self.rect.x + (self.rect.width - self.icon.get_width()) // 2
        icon_y = self.rect.y + 5
        screen.blit(self.icon, (icon_x, icon_y))
        text_surf = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.bottom - text_surf.get_height() // 2))
        screen.blit(text_surf, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_clicked(event.pos):
                self.action()

class ArmyTab:
    def __init__(self, screen_width, screen_height, place_unit_callback):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 24)
        self.label_text = "Выберите боевую единицу"
        self.show_army_tab_window = True
        self.place_unit_callback = place_unit_callback
        self.units = []

        # Army unit buttons
        self.opolchenec_button = UnitButton(350, 350, 95, 95, "Ополченец", unit_opolchenec, self.opolchenec_action)
        self.bronemashina_button = UnitButton(450, 350, 95, 95, "Бронемашина", unit_bronemashina, self.bronemashina_action)
        self.shturmovik_button = UnitButton(550, 350, 95, 95, "Штурмовик", unit_shturmovik, self.shturmovik_action)
        self.tank_button = UnitButton(650, 350, 95, 95, "Танк", unit_tank, self.tank_action)
        self.btr_button = UnitButton(750, 350, 95, 95, "БТР", unit_btr, self.btr_action)
        self.close_button = UnitButton(890, 515, 50, 50, "", images_path + "/close.png", self.close_action)

        self.buttons = [self.opolchenec_button, self.bronemashina_button, self.shturmovik_button, self.tank_button, self.btr_button, self.close_button]

    def draw(self, screen):
        if not self.show_army_tab_window:
            return

        pygame.draw.rect(screen, (192, 192, 192), (315, 320, 640, 250))

        text_surf = self.font.render(self.label_text, True, (0, 0, 0))
        screen.blit(text_surf, (self.screen_width // 2 - text_surf.get_width() // 2, 330))

        for button in self.buttons:
            button.draw(screen, self.font)

    def handle_event(self, event):
        if not self.show_army_tab_window:
            return

        for button in self.buttons:
            button.handle_event(event)

    def move_unit(self, mouse_pos):
        for unit in self.units:
            if unit.x <= mouse_pos[0] <= unit.x + unit.image.get_width() and unit.y <= mouse_pos[1] <= unit.y + unit.image.get_height():
                unit.set_target_position(mouse_pos)
                break

    def update_units(self):
        for unit in self.units:
            unit.update()

    def draw_units(self, screen):
        for unit in self.units:
            unit.draw(screen)

    def opolchenec_action(self):
        print("Ополченец кнопка нажата")
        x, y = 900, 400  # Пример координат
        unit = Unit(unit_opolchenec, x, y, speed=2)
        self.units.append(unit)
        self.place_unit_callback("Ополченец", unit_opolchenec, x, y)

    def bronemashina_action(self):
        print("Бронемашина кнопка нажата")
        x, y = 900, 400  # Пример координат
        unit = Unit(unit_bronemashina, x, y, speed=3)
        self.units.append(unit)
        self.place_unit_callback("Бронемашина", unit_bronemashina, x, y)

    def shturmovik_action(self):
        print("Штурмовик кнопка нажата")
        x, y = 900, 400  # Пример координат
        unit = Unit(unit_shturmovik, x, y, speed=4)
        self.units.append(unit)
        self.place_unit_callback("Штурмовик", unit_shturmovik, x, y)

    def tank_action(self):
        print("Танк кнопка нажата")
        x, y = 900, 400  # Пример координат
        unit = Unit(unit_tank, x, y, speed=1)
        self.units.append(unit)
        self.place_unit_callback("Танк", unit_tank, x, y)

    def btr_action(self):
        print("БТР кнопка нажата")
        x, y = 900, 400  # Пример координат
        unit = Unit(unit_btr, x, y, speed=2.5)
        self.units.append(unit)
        self.place_unit_callback("БТР", unit_btr, x, y)

    def close_action(self):
        self.show_army_tab_window = False
        print("Окно армии закрыто")

    def open(self):
        self.show_army_tab_window = True
