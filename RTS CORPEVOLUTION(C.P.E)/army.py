from progress_tab import *
import pygame

images_path = r'C:\Users\User\Desktop\C.P.E'
unit_opolchenec = images_path + r'\units\base2\opolch.png'


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

        # Army unit buttons
        self.opolchenec_button = UnitButton(350, 350, 95, 95, "Ополченец", unit_opolchenec, self.opolchenec_action)
        self.close_button = UnitButton(890, 515, 50, 50, "", images_path + "/close.png", self.close_action)

        self.buttons = [self.opolchenec_button, self.close_button]

    def draw(self, screen):
        if not self.show_army_tab_window:
            return

        pygame.draw.rect(screen, (192, 192, 192), (315, 320, 640, 250))

        text_surf = self.font.render(self.label_text, True, (0, 0, 0))
        screen.blit(text_surf, (self.screen_width // 2 - text_surf.get_width() // 2, 330))

        for button in self.buttons:
            button.draw(screen, self.font)  # Вызов метода отрисовки кнопки

    def handle_event(self, event):
        if not self.show_army_tab_window:
            return

        for button in self.buttons:
            button.handle_event(event)

    def opolchenec_action(self):
        print("Ополченец кнопка нажата")
        self.place_unit_callback("Ополченец", unit_opolchenec)

    def close_action(self):
        self.show_army_tab_window = False
        print("Окно армии закрыто")

    def open(self):
        self.show_army_tab_window = True
        print('Окно армии открыто')
