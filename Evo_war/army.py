import os
import math
from progress_tab import *  # Отсюда импортируется и pygame в том числе

images_path = r'C:\Users\User\Desktop\C.P.E'
unit_opolchenec = os.path.join(images_path, r'units\base2\opolch.png')
unit_bronemashina = os.path.join(images_path, r'units\base2\bronemashina.png')
unit_shturmovik = os.path.join(images_path, r'units\base2\shturmovik.png')
unit_tank = os.path.join(images_path, r'units\base2\tank.png')
unit_btr = os.path.join(images_path, r'units\base2\btr.png')
unit_pul = os.path.join(images_path, r'units\base2\pulemet.png')
unit_spt = os.path.join(images_path, r'units\base2\spt-75.png')
unit_sgb = os.path.join(images_path, r'units\base2\sgb-200.png')
unit_sold = os.path.join(images_path, r'units\base2\sold.png')
unit_spez = os.path.join(images_path, r'units\base2\spez.png')
unit_fear = os.path.join(images_path, r'units\base2\fear.png')


class Unit:
    def __init__(self, x, y, unit_type):
        self.x = x
        self.y = y
        self.unit_type = unit_type
        self.target_position = None
        self.speed = self.speed_unit()
        self.image = self.image_unit()
        self.original_image = self.image

    def image_unit(self):
        if self.unit_type == "Бронемашина":
            return pygame.transform.scale(pygame.image.load(unit_bronemashina), (50, 50))
        elif self.unit_type == "БТР":
            return pygame.transform.scale(pygame.image.load(unit_btr), (55, 55))
        elif self.unit_type == 'Ополченец':
            return pygame.transform.scale(pygame.image.load(unit_opolchenec), (40, 40))
        elif self.unit_type == "Штурмовик":
            return pygame.transform.scale(pygame.image.load(unit_shturmovik), (40, 40))
        elif self.unit_type == "Танк":
            return pygame.transform.scale(pygame.image.load(unit_tank), (70, 70))
        elif self.unit_type == "Пулемет":
            return pygame.transform.scale(pygame.image.load(unit_pul), (50, 50))
        elif self.unit_type == "СПТ":
            return pygame.transform.scale(pygame.image.load(unit_spt), (55, 55))
        elif self.unit_type == "Гаубица":
            return pygame.transform.scale(pygame.image.load(unit_sgb), (60, 60))
        elif self.unit_type == "Солдат":
            return pygame.transform.scale(pygame.image.load(unit_sold), (40, 40))
        elif self.unit_type == "Спецназ":
            return pygame.transform.scale(pygame.image.load(unit_spez), (40, 40))
        elif self.unit_type == "ССО":
            return pygame.transform.scale(pygame.image.load(unit_fear), (40, 40))


    def speed_unit(self):
        if self.unit_type == "Бронемашина":
            return 0.9
        elif self.unit_type == "БТР":
            return 0.4
        elif self.unit_type == "Ополченец":
            return 0.2
        elif self.unit_type == "Штурмовик":
            return 0.3
        elif self.unit_type == "Танк":
            return 0.2
        elif self.unit_type == "Пулемет":
            return 0.1
        elif self.unit_type == "СПТ":
            return 0.1
        elif self.unit_type == "Гаубица":
            return 0
        elif self.unit_type == "Солдат":
            return 0.2
        elif self.unit_type == "Спецназ":
            return 0.4
        elif self.unit_type == "ССО":
            return 0.6

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move_to(self, target_x, target_y):
        self.target_position = (target_x, target_y)

    def update(self):
        if self.target_position:
            target_x, target_y = self.target_position
            dx = target_x - self.x
            dy = target_y - self.y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance > 0:
                dx /= distance
                dy /= distance
                # Перемещение юнита с заданной скоростью
                self.x += dx * self.speed
                self.y += dy * self.speed

                # Инвертирование изображения в зависимости от направления
                if dx < 0:
                    self.image = pygame.transform.flip(self.original_image, True, False)
                else:
                    self.image = self.original_image

                # Проверка на достижение цели
                if math.sqrt((target_x - self.x) ** 2 + (target_y - self.y) ** 2) < self.speed:
                    self.x = target_x
                    self.y = target_y
                    self.target_position = None


class UnitButton:
    def __init__(self, x, y, width, height, text, icon_path, action):
        if not isinstance(icon_path, str):
            raise ValueError(f"icon_path должен быть строкой, получен {type(icon_path)}")
        if not os.path.isfile(icon_path):
            raise ValueError(f"Файл не найден: {icon_path}")
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.icon = pygame.image.load(icon_path)
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
    def __init__(self, screen_width, screen_height, place_unit_callback, base, progress):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 24)
        self.label_text = "Выберите боевую единицу"
        self.show_army_tab_window = True
        self.place_unit_callback = place_unit_callback
        self.units = []
        self.base = base
        self.progress = progress
        self.transition_duration = 0.5

        # Army unit buttons
        self.opolchenec_button = UnitButton(350, 350, 95, 95, "Ополченец", unit_opolchenec, self.opolchenec_action)
        self.close_button = UnitButton(890, 515, 50, 50, "", os.path.join(images_path, "close.png"), self.close_action)
        self.buttons = [self.opolchenec_button, self.close_button]
        self.buttons_sturm = UnitButton(450, 350, 95, 95, "Штурмовик", unit_shturmovik, self.shturmovik_action)
        self.buttons_lev1_arm = [self.buttons_sturm]
        self.buttons_bronemach = UnitButton(550, 350, 95, 95, "Бронемашина", unit_bronemashina,
                                            self.bronemashina_action)
        self.buttons_lev2_arm = [self.buttons_bronemach]
        self.buttons_btr = UnitButton(650, 350, 95, 95, "БТР", unit_btr, self.btr_action)
        self.buttons_tank = UnitButton(750, 350, 95, 95, "Танк", unit_tank, self.tank_action)
        self.buttons_lev3_arm = [self.buttons_btr, self.buttons_tank]
        self.buttons_pul = UnitButton(450, 350, 95, 95, "Пулемет", unit_pul, self.pulemet)
        self.buttons_spt = UnitButton(550, 350, 95, 95, "ПТ-Орудие", unit_spt, self.pt_75mm)
        self.buttons_sgb = UnitButton(650, 350, 95, 95, "Гаубица", unit_sgb, self.sgb_200)
        self.buttons_lev1_sys = [self.buttons_pul]
        self.buttons_lev2_sys = [self.buttons_spt]
        self.buttons_lev3_sys = [self.buttons_sgb]

        self.buttons_sold = UnitButton(450, 350, 95, 95, "Солдат", unit_sold, self.sold)
        self.buttons_spez = UnitButton(550, 350, 95, 95, "Спецназ", unit_spez, self.spez)
        self.buttons_fear = UnitButton(650, 350, 95, 95, "ССО", unit_fear, self.fear)
        self.buttons_lev1_sp = [self.buttons_sold]
        self.buttons_lev2_sp = [self.buttons_spez]
        self.buttons_lev3_sp = [self.buttons_fear]

    def draw(self, screen):
        if not self.show_army_tab_window:
            return

        pygame.draw.rect(screen, (30, 30, 60), (315, 320, 640, 250))

        text_surf = self.font.render(self.label_text, True, (255, 255, 255))
        screen.blit(text_surf, (self.screen_width // 2 - text_surf.get_width() // 2, 330))

        if self.progress.check_army_armor() == 1:
            for button in self.buttons_lev1_arm:
                button.draw(screen, self.font)

            for button in self.buttons:
                button.draw(screen, self.font)

        elif self.progress.check_army_armor() == 2:
            for button in self.buttons_lev1_arm:
                button.draw(screen, self.font)

            for button in self.buttons_lev2_arm:
                button.draw(screen, self.font)

            for button in self.buttons:
                button.draw(screen, self.font)

        elif self.progress.check_army_armor() == 3:

            for button in self.buttons_lev1_arm:
                button.draw(screen, self.font)

            for button in self.buttons_lev2_arm:
                button.draw(screen, self.font)

            for button in self.buttons_lev3_arm:
                button.draw(screen, self.font)

            for button in self.buttons:
                button.draw(screen, self.font)

        elif self.progress.check_army_sys() == 1:
            for button in self.buttons_lev1_sys:
                button.draw(screen, self.font)
            for button in self.buttons:
                button.draw(screen, self.font)

        elif self.progress.check_army_sys() == 2:
            for button in self.buttons_lev1_sys:
                button.draw(screen, self.font)
            for button in self.buttons_lev2_sys:
                button.draw(screen, self.font)
            for button in self.buttons:
                button.draw(screen, self.font)

        elif self.progress.check_army_sys() == 3:
            for button in self.buttons_lev1_sys:
                button.draw(screen, self.font)
            for button in self.buttons_lev2_sys:
                button.draw(screen, self.font)
            for button in self.buttons_lev3_sys:
                button.draw(screen, self.font)
            for button in self.buttons:
                button.draw(screen, self.font)

        elif self.progress.check_army_sp() == 1:
            for button in self.buttons_lev1_sp:
                button.draw(screen, self.font)
            for button in self.buttons:
                button.draw(screen, self.font)

        elif self.progress.check_army_sp() == 2:
            for button in self.buttons_lev1_sp:
                button.draw(screen, self.font)
            for button in self.buttons_lev2_sp:
                button.draw(screen, self.font)
            for button in self.buttons:
                button.draw(screen, self.font)

        elif self.progress.check_army_sp() == 3:
            for button in self.buttons_lev1_sp:
                button.draw(screen, self.font)
            for button in self.buttons_lev2_sp:
                button.draw(screen, self.font)
            for button in self.buttons_lev3_sp:
                button.draw(screen, self.font)
            for button in self.buttons:
                button.draw(screen, self.font)

        else:
            for button in self.buttons:
                button.draw(screen, self.font)

    def handle_event(self, event):
        if not self.show_army_tab_window:
            return

        if self.progress.armored_vehicles_open:
            if self.progress.check_army_armor() == 1:
                for button in self.buttons_lev1_arm:
                    button.handle_event(event)

                for button in self.buttons:
                    button.handle_event(event)

            elif self.progress.check_army_armor() == 2:
                for button in self.buttons_lev1_arm:
                    button.handle_event(event)

                for button in self.buttons_lev2_arm:
                    button.handle_event(event)

                for button in self.buttons:
                    button.handle_event(event)

            elif self.progress.check_army_armor() == 3:

                for button in self.buttons_lev1_arm:
                    button.handle_event(event)

                for button in self.buttons_lev2_arm:
                    button.handle_event(event)

                for button in self.buttons_lev3_arm:
                    button.handle_event(event)

                for button in self.buttons:
                    button.handle_event(event)

            else:
                for button in self.buttons:
                    button.handle_event(event)

        if self.progress.system_open:
            if self.progress.check_army_sys() == 1:
                for button in self.buttons_lev1_sys:
                    button.handle_event(event)

                for button in self.buttons:
                    button.handle_event(event)

            elif self.progress.check_army_sys() == 2:

                for button in self.buttons_lev1_sys:
                    button.handle_event(event)

                for button in self.buttons_lev2_sys:
                    button.handle_event(event)

                for button in self.buttons:
                    button.handle_event(event)

            elif self.progress.check_army_sys() == 3:
                for button in self.buttons_lev1_sys:
                    button.handle_event(event)

                for button in self.buttons_lev2_sys:
                    button.handle_event(event)

                for button in self.buttons_lev3_sys:
                    button.handle_event(event)

                for button in self.buttons:
                    button.handle_event(event)

            else:
                for button in self.buttons:
                    button.handle_event(event)

        if self.progress.speznaz_open:
            if self.progress.check_army_sp() == 1:
                for button in self.buttons_lev1_sp:
                    button.handle_event(event)

                for button in self.buttons:
                    button.handle_event(event)

            elif self.progress.check_army_sp() == 2:

                for button in self.buttons_lev1_sp:
                    button.handle_event(event)

                for button in self.buttons_lev2_sp:
                    button.handle_event(event)

                for button in self.buttons:
                    button.handle_event(event)

            elif self.progress.check_army_sp() == 3:
                for button in self.buttons_lev1_sp:
                    button.handle_event(event)

                for button in self.buttons_lev2_sp:
                    button.handle_event(event)

                for button in self.buttons_lev3_sp:
                    button.handle_event(event)

                for button in self.buttons:
                    button.handle_event(event)

            else:
                for button in self.buttons:
                    button.handle_event(event)

        else:
            for button in self.buttons:
                button.handle_event(event)

    def move_unit(self, unit_index, target_x, target_y):
        if unit_index < len(self.units):
            unit = self.units[unit_index]
            unit.move_to(target_x, target_y)
        else:
            print("Неверный индекс юнита:", unit_index)

    def opolchenec_action(self):
        print("Ополченец кнопка нажата")
        if self.base.cashe(1, 2, 3):
            self.base.update_resources()
            x, y = 900, 300
            self.place_unit_callback("Ополченец", unit_opolchenec, x, y)

    def bronemashina_action(self):
        print("Бронемашина кнопка нажата")
        if self.base.cashe(1, 2, 3):
            self.base.update_resources()
            x, y = 900, 350
            self.place_unit_callback("Бронемашина", unit_bronemashina, x, y)

    def shturmovik_action(self):
        print("Штурмовик кнопка нажата")
        if self.base.cashe(1, 2, 3):
            self.base.update_resources()
            x, y = 900, 400
            self.place_unit_callback("Штурмовик", unit_shturmovik, x, y)

    def btr_action(self):
        print("БТР кнопка нажата")
        if self.base.cashe(1, 2, 3):
            self.base.update_resources()
            x, y = 850, 500
            self.place_unit_callback("БТР", unit_btr, x, y)

    def tank_action(self):
        print("Танк кнопка нажата")
        if self.base.cashe(1, 2, 3):
            self.base.update_resources()
            x, y = 900, 450
            self.place_unit_callback("Танк", unit_tank, x, y)

    def pulemet(self):
        print("Пулемет кнопка нажата")
        if self.base.cashe(1, 2, 3):
            self.base.update_resources()
            x, y = 900, 300
            self.place_unit_callback("Пулемет", unit_pul, x, y)

    def pt_75mm(self):
        if self.base.cashe(1, 2, 3):
            self.base.update_resources()
            x, y = 850, 500
            self.place_unit_callback("СПТ", unit_spt, x, y)

    def sgb_200(self):
        if self.base.cashe(1, 2, 3):
            self.base.update_resources()
            x, y = 900, 400
            self.place_unit_callback("Гаубица", unit_sgb, x, y)

    def sold(self):
        if self.base.cashe(1, 2, 3):
            self.base.update_resources()
            x, y = 850, 400
            self.place_unit_callback("Солдат", unit_sold, x, y)

    def spez(self):
        if self.base.cashe(1, 2, 3):
            self.base.update_resources()
            x, y = 950, 500
            self.place_unit_callback("Спецназ", unit_spez, x, y)

    def fear(self):
        if self.base.cashe(1, 2, 3):
            self.base.update_resources()
            x, y = 850, 500
            self.place_unit_callback("ССО", unit_fear, x, y)

    def close_action(self):
        self.show_army_tab_window = False
        print("Окно армии закрыто")

    def open(self):
        self.show_army_tab_window = True
