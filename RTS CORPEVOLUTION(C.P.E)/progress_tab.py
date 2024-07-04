import pygame

images_path = r'C:\Users\User\Desktop\C.P.E\progress'

class Button:
    def __init__(self, x, y, width, height, text, icon_path, action):
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
        screen.blit(text_surf, (self.rect.x + (self.rect.width - text_surf.get_width()) // 2,
                                self.rect.y + self.rect.height - text_surf.get_height() - 5))

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_clicked(event.pos):
                self.action()

class ProgressTab:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 24)
        self.label_text = "Выберите свою специализацию"

        # Позиционирование кнопок в меньшем окне прогресса
        self.special_forces_button = Button(350, 350, 150, 160, "Спецназ", images_path+"/special_forces.png", self.special_forces_action)
        self.armored_vehicles_button = Button(550, 350, 150, 160, "Бронетехника", images_path+"/armored_vehicles.png", self.armored_vehicles_action)
        self.computing_systems_button = Button(750, 350, 150, 160, "Выч. системы", images_path+"/computing_systems.png", self.computing_systems_action)
        self.close_button = Button(890, 515, 50, 50, "", images_path + "/close.png", self.close_action)

        self.buttons = [self.special_forces_button, self.armored_vehicles_button, self.computing_systems_button,
                        self.close_button]

    def draw(self, screen):
        # Заполняем экран серым цветом в заданных пределах
        pygame.draw.rect(screen, (192, 192, 192), (315, 320, 640, 250))

        # Отображаем текстовую надпись
        text_surf = self.font.render(self.label_text, True, (0, 0, 0))
        screen.blit(text_surf, (self.screen_width // 2 - text_surf.get_width() // 2, 330))

        # Отображаем кнопки
        for button in self.buttons:
            button.draw(screen, self.font)

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event) 

    def special_forces_action(self):
        print("Спецназ кнопка нажата")

    def armored_vehicles_action(self):
        print("Бронетехника кнопка нажата")

    def computing_systems_action(self):
        print("Вычислительные системы кнопка нажата")

    def close_action(self):
        self.show_progress_window = False
        print('Кнопка закрыть отжата')
