import pygame
import time

images_path = r'C:\Users\User\Desktop\C.P.E\progress'
images_path_lev1_arm = r'C:\Users\User\Desktop\C.P.E\progress\armor\1_level'
images_path_lev2_arm = r'C:\Users\User\Desktop\C.P.E\progress\armor\2_level'
images_path_lev1_sp = r'C:\Users\User\Desktop\C.P.E\progress\spez\1_level'
images_path_lev2_sp = r'C:\Users\User\Desktop\C.P.E\progress\spez\2_level'
images_path_lev1_sys = r'C:\Users\User\Desktop\C.P.E\progress\system\1_level'
images_path_lev2_sys = r'C:\Users\User\Desktop\C.P.E\progress\system\2_level'

class Button:
    def __init__(self, x, y, width, height, text, icon_path, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.icon = pygame.image.load(icon_path)
        self.icon = pygame.transform.scale(self.icon, (width - 20, height - 20))
        self.action = action
        self.enabled = True

    def draw(self, screen, font):
        if self.enabled:
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
            if self.is_clicked(event.pos) and self.enabled:
                self.action()


class TextApplet:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.enabled = True

    def draw(self, screen, font):
        if self.enabled:
            text_surf = font.render(self.text, True, (0, 0, 0))
            text_rect = text_surf.get_rect(topleft=(self.rect.x, self.rect.y))
            screen.blit(text_surf, text_rect)


class ProgressTab:
    def __init__(self, screen_width, screen_height, base):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.base = base
        self.font = pygame.font.Font(None, 24)
        self.label_text = "Выберите свою специализацию"
        self.show_progress_window = True
        self.armored_vehicles_open = False
        self.speznaz_open = False
        self.message = ""
        self.message_time = 0
        self.all_upgrades_purchased = False

        # General buttons
        self.special_forces_button = Button(350, 350, 150, 160, "Спецназ", images_path + "/special_forces.png",
                                            self.special_forces_action)
        self.armored_vehicles_button = Button(550, 350, 150, 160, "Бронетехника", images_path + "/armored_vehicles.png",
                                              self.armored_vehicles_action)
        self.computing_systems_button = Button(750, 350, 150, 160, "Выч. системы",
                                               images_path + "/computing_systems.png", self.computing_systems_action)
        self.close_button = Button(955, 280, 70, 70, "", images_path + "/close.png", self.close_action)

        self.buttons = [self.special_forces_button, self.armored_vehicles_button, self.computing_systems_button,
                        self.close_button]

        # Armored vehicle upgrade buttons and text applets
        self.heavy_weapons_button = Button(350, 370, 60, 60, "", images_path_lev1_arm + "/big_weap.png",
                                           self.heavy_weapons_action)
        self.heavy_armor_button = Button(350, 440, 60, 60, "", images_path_lev1_arm + "/ammo.png",
                                         self.heavy_armor_action)
        self.unique_alloys_button = Button(350, 510, 60, 60, "", images_path_lev1_arm + "/splav.png",
                                           self.unique_alloys_action)
        self.advanced_machines_button = Button(350, 580, 60, 60, "", images_path_lev1_arm + "/stanki.png",
                                               self.advanced_machines_action)

        self.heavy_weapons_applet = TextApplet(420, 390, 200, 50, "Тяжелое оружие: 300 железа, 450 сырья, 500 золота")
        self.heavy_armor_applet = TextApplet(420, 460, 200, 50, "Тяжелая амуниция: 300 железа, 450 сырья, 500 золота")
        self.unique_alloys_applet = TextApplet(420, 530, 200, 50,
                                               "Уникальные сплавы: 300 железа, 450 сырья, 500 золота")
        self.advanced_machines_applet = TextApplet(420, 600, 200, 50,
                                                   "Улучшенные станки: 300 железа, 450 сырья, 500 золота")

        self.armored_buttons_lev1 = [self.heavy_weapons_button, self.heavy_armor_button, self.unique_alloys_button,
                                     self.advanced_machines_button, self.close_button]

        self.armored_applets_lev1 = [self.heavy_weapons_applet, self.heavy_armor_applet, self.unique_alloys_applet,
                                     self.advanced_machines_applet]

        self.dvg_buttons = Button(350, 370, 60, 60, "", images_path_lev2_arm + "/dvg.png", self.dvg_arm)
        self.sbor_buttons = Button(350, 440, 60, 60, "", images_path_lev2_arm + "/sbor.png", self.sbor_arm)
        self.kum_buttons = Button(350, 510, 60, 60, "", images_path_lev2_arm + "/kum.png", self.kum_arm)

        self.dvg_applet = TextApplet(420, 390, 200, 50, "ДВГ: 1 железо, 2 сырья, 3 золота")
        self.sbor_applet = TextApplet(420, 460, 200, 50, "Новая сборочная линия: 1 железо, 2 сырья, 3 золота")
        self.kum_applet = TextApplet(420, 530, 200, 50, "Кумулятивные боеприпасы: 1 железо, 2 сырья, 3 золота")

        self.armored_buttons_lev2 = [self.dvg_buttons, self.sbor_buttons, self.kum_buttons]
        self.armored_applets_lev2 = [self.dvg_applet, self.sbor_applet, self.kum_applet]

        self.sp_ammo_buttons = Button(350, 370, 60, 60, "", images_path_lev1_sp+"/ammo.png", self.sp_ammo)
        self.sp_appar_buttons = Button(350, 440, 60, 60, "", images_path_lev1_sp+"/appar.png", self.sp_appar)
        self.sp_connect_buttons = Button(350, 510, 60, 60, "", images_path_lev1_sp+"/connect.png", self.sp_connect)
        self.sp_ekip_buttons = Button(350, 580, 60, 60, "", images_path_lev1_sp+"/ekip.png", self.sp_ekip)

        self.sp_ammo_applet = TextApplet(420, 390, 200, 50, "Улучшенные винтовки: 400 железа, 900 сырья, 350 золота")
        self.sp_appar_applet = TextApplet(420, 460, 200, 50, "Тепловизоры, ПНВ: 300 железа, 700 сырья, 1500 золота")
        self.sp_connect_applet = TextApplet(420, 530, 200, 50, "Спутниковая связь: 1000 железа, 1200 сырья, 3000 золота")
        self.sp_ekip_applet = TextApplet(420, 600, 200, 50, 'Экипировка класса "Альфа": 150 железа, 700 сырья, 2600 золота')

        self.sp_buttons_lev1 = [self.sp_ammo_buttons, self.sp_appar_buttons, self.sp_connect_buttons, self.sp_ekip_buttons, self.close_button]
        self.sp_applets_lev1 = [self.sp_ammo_applet, self.sp_appar_applet, self.sp_connect_applet, self.sp_ekip_applet]

        self.sp_aggit_buttons = Button(350, 370, 60, 60, "", images_path_lev2_sp+"/aggitation.png", self.sp_aggit)
        self.sp_bio_buttons = Button(350, 440, 60, 60, "", images_path_lev2_sp+"/bio.png", self.sp_bio)
        self.sp_electro_buttons = Button(350, 510, 60, 60, "", images_path_lev2_sp+"/electro.png", self.sp_electro)

        self.sp_aggit_applet = TextApplet(420, 390, 200, 50, "Аггитация: 100 железа, 1900 сырья, 9000 золота")
        self.sp_bio_applet = TextApplet(420, 460, 200, 50, "Биологическая модернизация: 50 железа, 4500 сырья, 25000 золота")
        self.sp_electro_applet = TextApplet(420, 530, 200, 50, "Экспериментальная электроника: 600 железа, 7000 сырья, 40000 золота")

        self.sp_buttons_lev2 = [self.sp_aggit_buttons, self.sp_bio_buttons, self.sp_electro_buttons]
        self.sp_applets_lev2 = [self.sp_aggit_applet, self.sp_bio_applet, self.sp_electro_applet]

    def draw(self, screen):
        if not self.show_progress_window:
            return

        pygame.draw.rect(screen, (192, 192, 192), (315, 320, 640, 250))

        text_surf = self.font.render(self.label_text, True, (0, 0, 0))
        screen.blit(text_surf, (self.screen_width // 2 - text_surf.get_width() // 2, 330))

        if self.armored_vehicles_open:
            pygame.draw.rect(screen, (192, 192, 192), (270, 320, 740, 350))
            text_surf = self.font.render(self.label_text, True, (0, 0, 0))
            screen.blit(text_surf, (self.screen_width // 2 - text_surf.get_width() // 2, 330))
            for button in self.armored_buttons_lev1:
                button.draw(screen, self.font)

            for applet in self.armored_applets_lev1:
                applet.draw(screen, self.font)

            if self.check_armor_ready_1lev():
                for button in self.armored_buttons_lev2:
                    button.draw(screen, self.font)
                for applet in self.armored_applets_lev2:
                    applet.draw(screen, self.font)

        elif self.speznaz_open:
            pygame.draw.rect(screen, (192, 192, 192), (270, 320, 740, 350))
            text_surf = self.font.render(self.label_text, True, (0, 0, 0))
            screen.blit(text_surf, (self.screen_width // 2 - text_surf.get_width() // 2, 330))
            for button in self.sp_buttons_lev1:
                button.draw(screen, self.font)

            for applet in self.sp_applets_lev1:
                applet.draw(screen, self.font)

            if self.check_sp_ready_1lev():
                for button in self.sp_buttons_lev2:
                    button.draw(screen, self.font)
                for applet in self.sp_applets_lev2:
                    applet.draw(screen, self.font)

        else:
            for button in self.buttons:
                button.draw(screen, self.font)

        # Отображение временного сообщения
        if self.message:
            message_surf = self.font.render(self.message, True, (0, 0, 0))
            screen.blit(message_surf, (self.screen_width // 2 - message_surf.get_width() // 2, 640))

            if time.time() - self.message_time > 2:
                self.message = ""

        # Отображение статичного сообщения
        if self.all_upgrades_purchased:
            static_message_surf = self.font.render("Все улучшения были приобретены!", True, (0, 0, 0))
            screen.blit(static_message_surf, (self.screen_width // 2 - static_message_surf.get_width() // 2, 450))

    def handle_event(self, event):
        if not self.show_progress_window:
            return

        if self.armored_vehicles_open:
            for button in self.armored_buttons_lev1:
                button.handle_event(event)

            if self.check_armor_ready_1lev():
                for button in self.armored_buttons_lev2:
                    button.handle_event(event)

        elif self.speznaz_open:
            for button in self.sp_buttons_lev1:
                button.handle_event(event)

            if self.check_sp_ready_1lev():
                for button in self.sp_buttons_lev2:
                    button.handle_event(event)

        else:
            for button in self.buttons:
                button.handle_event(event)


    def armored_vehicles_action(self):
        if not self.armored_vehicles_open:
            self.armored_vehicles_open = True
            self.label_text = 'Выберите улучшение для специализации "Бронетехника"'
        else:
            self.armored_vehicles_open = False
            self.label_text = "Выберите свою специализацию"

    def computing_systems_action(self):
        print("Вычислительные системы кнопка нажата")

    def close_action(self):
        if self.heavy_weapons_button.enabled == False or self.heavy_armor_button.enabled == False or self.unique_alloys_button.enabled == False or self.advanced_machines_button.enabled == False \
                or self.sp_ammo_buttons.enabled == False or self.sp_appar_buttons.enabled == False or self.sp_connect_buttons.enabled == False or self.sp_ekip_buttons.enabled == False:
            self.show_progress_window = False
        else:
            self.armored_vehicles_open = False
            self.speznaz_open = False
            self.show_progress_window = False
            self.label_text = "Выберите свою специализацию"

    def heavy_weapons_action(self):
        if self.base.cashe(1, 2, 3):
            self.base.update_resources()
            print("Тяжелое оружие улучшено")
            self.heavy_weapons_button.enabled = False
            self.heavy_weapons_applet.enabled = False
            self.display_message("Тяжелое оружие улучшено!")
        else:
            print("Не хватает ресурсов")
        self.update_buttons_state()
        self.check_all_upgrades_purchased()

    def heavy_armor_action(self):
        if self.base.cashe(1, 2, 3):
            self.base.update_resources()
            print("Тяжелая амуниция улучшена")
            self.heavy_armor_button.enabled = False
            self.heavy_armor_applet.enabled = False
            self.display_message("Тяжелая амуниция улучшена!")
        else:
            print("Не хватает ресурсов")
        self.update_buttons_state()
        self.check_all_upgrades_purchased()

    def unique_alloys_action(self):
        if self.base.cashe(1, 2, 3):
            self.base.update_resources()
            print("Уникальные сплавы улучшены")
            self.unique_alloys_button.enabled = False
            self.unique_alloys_applet.enabled = False
            self.display_message("Уникальные сплавы улучшены!")
        else:
            print("Не хватает ресурсов")
        self.update_buttons_state()
        self.check_all_upgrades_purchased()

    def advanced_machines_action(self):
        if self.base.cashe(1, 2, 3):
            self.base.update_resources()
            print("Улучшенные станки установлены")
            self.advanced_machines_button.enabled = False
            self.advanced_machines_applet.enabled = False
            self.display_message("Улучшенные станки установлены!")
        else:
            print("Не хватает ресурсов")
        self.update_buttons_state()
        self.check_all_upgrades_purchased()

    def dvg_arm(self):
        if self.base.cashe(1, 2, 3):
            self.base.update_resources()
            print("Получены двигатели нового поколения")
            self.dvg_buttons.enabled = False
            self.dvg_applet.enabled = False
            self.display_message("Двигатели нового поколения получены!")
        else:
            print("Не хватает ресурсов")
        self.check_all_upgrades_purchased()

    def sbor_arm(self):
        if self.base.cashe(1, 2, 3):
            self.base.update_resources()
            print("Построена новая сборочная линия")
            self.sbor_buttons.enabled = False
            self.sbor_applet.enabled = False
            self.display_message("Новая сборочная линия построена!")
        else:
            print("Не хватает ресурсов")
        self.check_all_upgrades_purchased()

    def kum_arm(self):
        if self.base.cashe(1, 2, 3):
            self.base.update_resources()
            print("Кумулятивные боеприпасы получены!")
            self.kum_buttons.enabled = False
            self.kum_applet.enabled = False
            self.display_message("Кумулятивные боеприпасы получены!")
        else:
            print("Не хватает ресурсов")
        self.check_all_upgrades_purchased()

    def check_armor_unit_one(self):
        return (not self.heavy_weapons_button.enabled and not self.heavy_armor_button.enabled and
                not self.unique_alloys_button.enabled and not self.advanced_machines_button.enabled)

    def check_sp_unit_one(self):
        return (not self.sp_connect_buttons.enabled and not self.sp_ammo_buttons.enabled and
                not self.sp_appar_buttons.enabled and not self.sp_ekip_buttons.enabled)

    def check_armor_ready_1lev(self):
        return self.check_armor_unit_one()

    def check_sp_ready_1lev(self):
        return self.check_sp_unit_one()

    def check_armor_unit_two(self):
        return not self.dvg_buttons.enabled and not self.sbor_buttons.enabled and not self.kum_buttons.enabled

    def check_sp_unit_two(self):
        return not self.sp_electro_buttons.enabled and not self.sp_aggit_buttons.enabled and not self.sp_bio_buttons.enabled

    def special_forces_action(self):
        if not self.speznaz_open:
            self.speznaz_open = True
            self.label_text = "Выберите улучшения для Спецназа"
        else:
            self.speznaz_open = False
            self.label_text = "Выберите свою специализацию"

    def sp_ammo(self):
        if self.base.cashe(1, 2, 3):
            self.base.update_resources()
            self.sp_ammo_buttons.enabled = False
            self.sp_ammo_applet.enabled = False
            self.display_message("Улучшенные винтовки получены")
        else:
            self.display_message("Не хватает ресурсов!")
        self.update_buttons_state()
        self.check_all_upgrades_purchased()

    def sp_appar(self):
        if self.base.cashe(1, 2, 3):
            self.base.update_resources()
            self.sp_appar_buttons.enabled = False
            self.sp_appar_applet.enabled = False
            self.display_message("Полученна новая аппаратура")
        else:
            self.display_message("Не хватает ресурсов")
        self.update_buttons_state()
        self.check_all_upgrades_purchased()

    def sp_connect(self):
        if self.base.cashe(1, 2, 3):
            self.base.update_resources()
            self.sp_connect_buttons.enabled = False
            self.sp_connect_applet.enabled = False
            self.display_message("Теперь наш обзор стал шире")
        else:
            self.display_message("Не хватает ресурсов")
        self.update_buttons_state()
        self.check_all_upgrades_purchased()

    def sp_ekip(self):
        if self.base.cashe(1, 2, 3):
            self.base.update_resources()
            self.sp_ekip_buttons.enabled = False
            self.sp_ekip_applet.enabled = False
            self.display_message("Теперь нас будут замечать с меньшего расстояния")
        else:
            self.display_message("Не хватает ресурсов")
        self.update_buttons_state()
        self.check_all_upgrades_purchased()

    def sp_aggit(self):
        if self.base.cashe(1, 2, 3):
            self.base.update_resources()
            self.sp_aggit_buttons.enabled = False
            self.sp_aggit_applet.enabled = False
            self.display_message("Теперь мы можем саботировать экономику противника")
        else:
            self.display_message("Не хватает ресурсов")
        self.check_all_upgrades_purchased()

    def sp_bio(self):
        if self.base.cashe(1, 2, 3):
            self.base.update_resources()
            self.sp_bio_buttons.enabled = False
            self.sp_bio_applet.enabled = False
            self.display_message("Теперь наши солдаты стали значительно крепче")
        else:
            self.display_message("Не хватает ресурсов")
        self.check_all_upgrades_purchased()

    def sp_electro(self):
        if self.base.cashe(1, 2, 3):
            self.base.update_resources()
            self.sp_electro_buttons.enabled = False
            self.sp_electro_applet.enabled = False
            self.display_message("Теперь мы получаем данные об их передвижении")
        else:
            self.display_message("Не хватает ресурсов")
        self.check_all_upgrades_purchased()


    def display_message(self, text):
        self.message = text
        self.message_time = time.time()

    def open(self):
        self.show_progress_window = True

    def update_buttons_state(self):
        if self.check_armor_ready_1lev():
            for button in self.armored_buttons_lev2:
                button.enabled = True
            for applet in self.armored_applets_lev2:
                applet.enabled = True
        else:
            for button in self.armored_buttons_lev2:
                button.enabled = False
            for applet in self.armored_applets_lev2:
                applet.enabled = False

        if self.check_sp_ready_1lev():
            for button in self.sp_buttons_lev2:
                button.enabled = True
            for applet in self.sp_applets_lev2:
                applet.enabled = True
        else:
            for button in self.sp_buttons_lev2:
                button.enabled = False
            for applet in self.sp_applets_lev2:
                applet.enabled = False

    def check_all_upgrades_purchased(self):
        if self.check_armor_ready_1lev() and self.check_armor_unit_two() or self.check_sp_ready_1lev() and self.check_sp_unit_two():
            self.all_upgrades_purchased = True
