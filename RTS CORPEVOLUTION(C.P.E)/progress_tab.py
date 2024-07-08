import pygame


images_path = r'C:\Users\User\Desktop\C.P.E\progress'
images_path_lev1_sf = r'C:\Users\User\Desktop\C.P.E\progress\special_forces\1_level'


class Button:
    def __init__(self, x, y, width, height, text, icon_path, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.icon = pygame.image.load(icon_path)
        self.icon = pygame.transform.scale(self.icon, (width - 20, height - 20))
        self.action = action
        self.enabled = True

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


class ProgressTab:
    def __init__(self, screen_width, screen_height, base):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.base = base
        self.font = pygame.font.Font(None, 24)
        self.label_text = "Выберите свою специализацию"
        self.show_progress_window = True

        # General buttons
        self.special_forces_button = Button(350, 350, 150, 160, "Спецназ", images_path + "/special_forces.png",
                                            self.special_forces_action)
        self.armored_vehicles_button = Button(550, 350, 150, 160, "Бронетехника", images_path + "/armored_vehicles.png",
                                              self.armored_vehicles_action)
        self.computing_systems_button = Button(750, 350, 150, 160, "Выч. системы",
                                               images_path + "/computing_systems.png", self.computing_systems_action)
        self.close_button = Button(890, 515, 50, 50, "", images_path + "/close.png", self.close_action)

        self.buttons = [self.special_forces_button, self.armored_vehicles_button, self.computing_systems_button,
                        self.close_button]

        # Armored vehicle upgrade buttons
        self.heavy_weapons_button = Button(350, 420, 60, 60, "Тяжелое оружие",
                                           images_path_lev1_sf + "/big_weap.png", self.heavy_weapons_action)
        self.heavy_armor_button = Button(350, 420, 60, 60, "Тяжелая амуниция",
                                         images_path_lev1_sf + "/ammo.png", self.heavy_armor_action)
        self.unique_alloys_button = Button(350, 420, 60, 60,
                                           "Уникальные сплавы", images_path_lev1_sf + "/splav.png",
                                           self.unique_alloys_action)
        self.advanced_machines_button = Button(350, 420, 60, 60,
                                               "Улучшенные станки", images_path_lev1_sf + "/stanki.png",
                                               self.advanced_machines_action)
        self.close_button = Button(890, 515, 50, 50, "", images_path + "/close.png", self.close_action)

        self.armored_buttons = [self.heavy_weapons_button, self.heavy_armor_button, self.unique_alloys_button,
                                self.advanced_machines_button, self.close_button]

        self.armored_vehicles_open = False


    def draw(self, screen):
        if not self.show_progress_window:
            return

        pygame.draw.rect(screen, (192, 192, 192), (315, 320, 640, 250))

        text_surf = self.font.render(self.label_text, True, (0, 0, 0))
        screen.blit(text_surf, (self.screen_width // 2 - text_surf.get_width() // 2, 330))

        if self.armored_vehicles_open:
            pygame.draw.rect(screen, (192, 192, 192), (270, 320, 740, 350))  # Gray background for the buttons area
            text_surf = self.font.render(self.label_text, True, (0, 0, 0))
            screen.blit(text_surf, (self.screen_width // 2 - text_surf.get_width() // 2, 330))
            for idx, button in enumerate(self.armored_buttons):
                button.rect.y = 350 + idx * 80  # Adjust vertical positioning based on index
                button.draw(screen, self.font)
        else:
            for button in self.buttons:
                button.draw(screen, self.font)


    def handle_event(self, event):
        if not self.show_progress_window:
            return

        if self.armored_vehicles_open:
            for button in self.armored_buttons:
                button.handle_event(event)
        else:
            for button in self.buttons:
                button.handle_event(event)

    def special_forces_action(self):
        print("Спецназ кнопка нажата")

    def armored_vehicles_action(self):
        if not self.armored_vehicles_open:
            self.armored_vehicles_open = True
            self.label_text = 'Выберите улучшение для специализации "Бронетехника"'
            print("Бронетехника кнопка нажата")
        else:
            self.armored_vehicles_open = False
            print("Закрыть Бронетехника")

    def close_action(self):
        if self.heavy_weapons_button.enabled == False or self.heavy_armor_button.enabled == False or self.unique_alloys_button.enabled == False or self.advanced_machines_button.enabled == False:
            self.show_progress_window = False
            print("Специализация бронетехника выбрана")
        else:
            self.armored_vehicles_open = False
            self.show_progress_window = False
            self.label_text = "Выберите свою специализацию"
        print('Кнопка закрыть отжата')

    def heavy_weapons_action(self):
        # (surie, iron, money)
        if self.base.cashe(90, 20, 150):
            self.base.update_resources()
            print("Тяжелое оружие для пехоты улучшено")
            self.heavy_weapons_button.enabled = False
        else:
            print("Не хватает ресурсов")

    def heavy_armor_action(self):
        if self.base.cashe(1500, 3000, 3000):
            self.base.update_resources()
            print("Тяжелая амуниция улучшена")
            self.heavy_armor_button.enabled = False
        else:
            print("Не хватает ресурсов")

    def unique_alloys_action(self):
        if self.base.cashe(1300, 4500, 4000):
            self.base.update_resources()
            print("Уникальные сплавы улучшены")
            self.unique_alloys_button.enabled = False
        else:
            print("Не хватает ресурсов")

    def advanced_machines_action(self):
        if self.base.cashe(2200, 3000, 5000):
            self.base.update_resources()
            print("Улучшенные станки установлены")
            self.advanced_machines_button.enabled = False
        else:
            print("Не хватает ресурсов")

    def computing_systems_action(self):
        pass

    def open(self):
        self.show_progress_window = True

