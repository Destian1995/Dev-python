import sys
import os
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QTextEdit, QVBoxLayout, QTableWidget, QHeaderView, \
    QTableWidgetItem, QWidget, QLineEdit, QRadioButton, QTabWidget, QListWidget, QDateEdit, QComboBox, QPlainTextEdit, \
    QLabel, QListWidgetItem
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from plyer import notification

class DailyPlannerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.selected_execute_index = None

    def init_ui(self):
        self.setWindowTitle('Менеджер задач v.1.5.4')
        self.setGeometry(600, 250, 750, 650)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        # Создаем виджет вкладок
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setStyleSheet(
            "QTabWidget::pane { border: 2px solid #F5F5DC; }")  # Устанавливаем границу вокруг вкладок

        # Создаем вкладку "Добавление новых задач"
        self.add_task_tab = QWidget()
        self.init_add_task_tab()
        self.tab_widget.addTab(self.add_task_tab, "Добавление новых задач")
        self.tab_widget.setTabIcon(0, QIcon('icons/add.png'))  # Устанавливаем иконку для вкладки

        # Создаем вкладку "Просмотр текущих задач"
        self.view_tasks_tab = QWidget()
        self.init_view_tasks_tab()
        self.tab_widget.addTab(self.view_tasks_tab, "Просмотр текущих задач")
        self.tab_widget.setTabIcon(1, QIcon('icons/view.png'))  # Устанавливаем иконку для вкладки

        # Создаем вкладку "История"
        self.history_tab = QWidget()
        self.init_history_tab()
        self.tab_widget.addTab(self.history_tab, "История")
        self.tab_widget.setTabIcon(2, QIcon('icons/history.png'))  # Устанавливаем иконку для вкладки
        self.load_history()

        self.layout.addWidget(self.tab_widget)
        self.central_widget.setLayout(self.layout)

        # Создаем вкладку "Исполнители"
        self.execute_tab = QWidget()
        self.init_execute_tab()
        self.tab_widget.addTab(self.execute_tab, "Исполнители")
        self.tab_widget.setTabIcon(3, QIcon('icons/users.png'))
        self.load_executes()

        # Стилизация
        self.setStyleSheet("""
            QMainWindow {
                background-color: #003366; /* Бежевый цвет */
            }
            QTabWidget::pane {
                background-color: #003366;
            }
            QTabBar::tab {
                background-color: #003366; /* Темно-синий цвет для вкладок */
                color: #FFFFFF;
                padding: 8px 20px;
                margin: 0;
            }
            QTabBar::tab:selected {
                background-color: #005BB5;
            }
            QPushButton {
                background-color: #003366; /* Темно-синий цвет для кнопок */
                color: #FFFFFF;
                border: none;
                padding: 8px 20px;
                margin: 5px 0;
            }
            QPushButton:hover {
                background-color: #005BB5;
            }
            QTextEdit, QDateEdit, QComboBox {
                background-color: #FFFFFF;
                color: #000000;
            }
        """)

    def load_executes(self):
        self.execute_table.setRowCount(0)  # Очистите таблицу перед загрузкой данных
        execute_file_path = os.path.join('DataBases', 'execute.md')
        executes = []

        if os.path.exists(execute_file_path):
            with open(execute_file_path, 'r', encoding='utf-8') as file:
                executes = [execute.strip() for execute in file.readlines()]

        self.execute_table.setRowCount(len(executes))

        for index, execute in enumerate(executes):
            self.execute_table.setItem(index, 0, QTableWidgetItem(execute))
            task_count = self.get_task_count_for_execute(execute)
            self.execute_table.setItem(index, 1, QTableWidgetItem(str(task_count)))
        self.execute_combo.clear()
        self.execute_combo.addItems(executes)

    def init_add_task_tab(self):
        layout = QVBoxLayout()

        self.task_input = QTextEdit(self)
        layout.addWidget(self.task_input)

        self.due_date_label = QLabel('Выполнить к дате:', self)
        self.due_date_label.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(self.due_date_label)

        self.due_date_edit = QDateEdit(QDate.currentDate(), self)
        self.due_date_edit.setCalendarPopup(True)
        layout.addWidget(self.due_date_edit)

        self.priority_label = QLabel('Приоритет:', self)
        self.priority_label.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(self.priority_label)

        self.priority_combo = QComboBox(self)
        self.priority_combo.addItems(['Обычный', 'Повышенный', 'Срочный'])
        self.priority_combo.setStyleSheet("QComboBox { background-color: #F5F5DC; }")
        layout.addWidget(self.priority_combo)

        self.execute_label = QLabel('Исполнитель:', self)
        self.execute_label.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(self.execute_label)

        self.execute_combo = QComboBox(self)  # Создаем выпадающий список
        layout.addWidget(self.execute_combo)

        # Загружаем исполнителей из файла execute.md и добавляем их в выпадающий список
        execute_file_path = os.path.join('DataBases', 'execute.md')
        if os.path.exists(execute_file_path):
            with open(execute_file_path, 'r', encoding='utf-8') as file:
                executes = file.readlines()
                self.execute_combo.addItems([execute.strip() for execute in executes])

        self.add_task_button = QPushButton('Добавить задачу', self)
        self.add_task_button.setIcon(QIcon('icons/add_work.png'))
        self.add_task_button.clicked.connect(self.add_task)
        layout.addWidget(self.add_task_button)

        self.add_task_tab.setLayout(layout)

    def init_view_tasks_tab(self):
        layout = QVBoxLayout()

        self.tasks_list = QListWidget(self)
        self.tasks_list.setWordWrap(True)
        layout.addWidget(self.tasks_list)

        # Добавляем радиокнопки для выбора критерия сортировки
        self.sort_priority_radio = QRadioButton('Сортировать по приоритету', self)
        self.sort_priority_radio.setChecked(True)
        self.sort_priority_radio.toggled.connect(self.load_tasks)
        self.sort_priority_radio.setStyleSheet("color: white;")  # Устанавливаем белый цвет для текста
        layout.addWidget(self.sort_priority_radio)

        self.sort_date_radio = QRadioButton('Сортировать по дате выполнения', self)
        self.sort_date_radio.toggled.connect(self.load_tasks)
        self.sort_date_radio.setStyleSheet("color: white;")  # Устанавливаем белый цвет для текста
        layout.addWidget(self.sort_date_radio)

        self.delete_task_button = QPushButton('Удалить задачу', self)
        self.delete_task_button.setIcon(QIcon('icons\delete.png'))
        self.delete_task_button.clicked.connect(self.delete_task)
        layout.addWidget(self.delete_task_button)

        self.load_tasks()
        self.view_tasks_tab.setLayout(layout)

    def init_execute_tab(self):
        self.execute_tab = QWidget()
        layout = QVBoxLayout()

        self.execute_input = QLineEdit(self)
        layout.addWidget(self.execute_input)

        self.add_execute_button = QPushButton('Создать нового исполнителя', self)
        self.add_execute_button.setIcon(QIcon('icons/newuser.png'))
        self.add_execute_button.clicked.connect(self.add_execute)
        layout.addWidget(self.add_execute_button)

        # Создаем горизонтальный виджет для кнопок "Добавить нового пользователя" и "Refresh"
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_execute_button)

        # Добавляем горизонтальный виджет к вертикальному слою
        self.layout.addLayout(button_layout)
        # Создаем QTableWidget для исполнителей
        self.execute_table = QTableWidget(self)
        self.execute_table.setColumnCount(2)
        self.execute_table.setHorizontalHeaderLabels(["Исполнитель", "Количество задач на исполнителе"])
        self.execute_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.execute_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # Расширяйте оба столбца

        # Задаем названия заголовков для столбцов таблицы
        self.execute_table.horizontalHeaderItem(0).setText("Исполнитель")
        self.execute_table.horizontalHeaderItem(1).setText("Количество задач на исполнителе")

        # Скрыть вертикальные заголовки таблицы
        self.execute_table.verticalHeader().setVisible(True)
        # Скрыть рамку вокруг таблицы
        self.execute_table.setFrameShape(QTableWidget.NoFrame)
        # Установите режим выделения только по строкам
        self.execute_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.execute_table.doubleClicked.connect(self.handle_table_double_click)
        self.selected_execute_index = None

        layout.addWidget(self.execute_table)

        self.execute_tab.setLayout(layout)
        self.tab_widget.addTab(self.execute_tab, "Исполнители")
        self.tab_widget.setTabIcon(3, QIcon('icons/users.png'))

        self.execute_table.setVisible(True)

    def send_notification(self, task_text):
        notification_title = "Срок задачи наступил"
        notification_message = f"Выполните задачу: {task_text}"
        notification.timeout = 10  # Время отображения уведомления (в секундах)
        notification.notify(
            title=notification_title,
            message=notification_message
        )

    def init_history_tab(self):
        layout = QVBoxLayout()
        self.history_tab.layout = QVBoxLayout()
        self.history_text = QPlainTextEdit(self)
        self.history_text.setReadOnly(True)
        layout.addWidget(self.history_text)
        self.clear_history_button = QPushButton('Очистить историю', self)
        self.clear_history_button.setIcon(QIcon('icons/clearhist.png'))
        self.clear_history_button.clicked.connect(self.clear_history)
        layout.addWidget(self.clear_history_button)
        self.load_history()
        self.history_tab.setLayout(layout)

    def add_task(self):
        current_tab_index = self.tab_widget.currentIndex()
        if current_tab_index == 0:  # Проверяем, на вкладке "Добавление новых задач"
            task_text = self.task_input.toPlainText().strip()
            due_date = self.due_date_edit.date().toString(Qt.ISODate)
            priority = self.priority_combo.currentText()
            execute = self.execute_combo.currentText()  # Получаем выбранного исполнителя

            if task_text:
                self.save_task(task_text, due_date, priority, execute)  # Передаем исполнителя
                self.task_input.clear()
                self.load_tasks()
                self.update_history(
                    f"Добавлена задача: {task_text} (Исполнитель: {execute}, До {due_date}, Приоритет: {priority})")
                self.save_history(
                    f"Добавлена задача: {task_text} (Исполнитель: {execute}, До {due_date}, Приоритет: {priority})")
                self.load_executes()

    def save_task(self, task_text, due_date, priority, execute):
        task_file_path = os.path.join('DataBases', 'tasks.md')
        with open(task_file_path, 'a', encoding='utf-8') as file:
            file.write(f"- {task_text} (Исполнитель: {execute}, До {due_date}, Приоритет: {priority})\n")

    def clear_history(self):
        history_file_path = os.path.join('DataBases', 'history.md')
        if os.path.exists(history_file_path):
            with open(history_file_path, 'w', encoding='utf-8') as file:
                file.write('')
        self.load_history()

    def delete_task(self):
        selected_item = self.tasks_list.currentItem()
        if selected_item:
            task_text = selected_item.text()
            task_to_remove = task_text.split('(', 1)[0].strip()
            self.remove_task(task_to_remove)
            self.load_tasks()
            self.update_history(f"Удалена задача: {task_to_remove}")
            self.save_history(f"Удалена задача: {task_to_remove}")
            self.load_executes()
    def remove_task(self, task_text):
        task_file_path = os.path.join('DataBases', 'tasks.md')
        with open(task_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        with open(task_file_path, 'w', encoding='utf-8') as file:
            for line in lines:
                if task_text not in line:
                    file.write(line)

    def load_tasks(self):
        task_file_path = os.path.join('DataBases', 'tasks.md')
        if os.path.exists(task_file_path):
            with open(task_file_path, 'r', encoding='utf-8') as file:
                tasks = file.read()
                self.tasks_list.clear()
                task_list = []

                for task in tasks.split('\n'):
                    if task:
                        task_list.append(task)

                # Выбираем критерий сортировки
                if self.sort_priority_radio.isChecked():
                    task_list.sort(key=lambda x: self.get_priority_value(x))
                elif self.sort_date_radio.isChecked():
                    task_list.sort(key=lambda x: self.extract_due_date(x).toPyDate())

                for task in task_list:
                    # Добавляем день недели к дате
                    task_date = self.extract_due_date(task)
                    day_of_week = self.get_day_of_week(task_date)
                    task_with_day = f"{task} ({day_of_week})"
                    item = QListWidgetItem(task_with_day)

                    # Устанавливаем цвет текста в зависимости от приоритета
                    if "Приоритет: Срочный" in task:
                        item.setForeground(QColor(Qt.white))
                    else:
                        item.setForeground(QColor(Qt.black))

                    item.setBackground(self.get_priority_color(task))
                    self.tasks_list.addItem(item)

    def get_priority_value(self, task):
        if "Приоритет: Срочный" in task:
            return 1
        elif "Приоритет: Повышенный" in task:
            return 2
        elif "Приоритет: Обычный" in task:
            return 3
        return 4

    def extract_due_date(self, task):
        # Извлекаем дату из строки задачи (пример: "До 2023-10-30, Приоритет: Обычный")
        due_date_start = task.find('До ') + len('До ')
        due_date_end = task.find(',', due_date_start)
        due_date_str = task[due_date_start:due_date_end].strip()
        due_date = QDate.fromString(due_date_str, Qt.ISODate)
        return due_date

    def get_day_of_week(self, date):
        # Получаем день недели
        days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        day_of_week = days[date.dayOfWeek() - 1]
        return day_of_week

    def get_priority_color(self, task):
        if "Приоритет: Обычный" in task:
            return QColor(Qt.green)
        elif "Приоритет: Повышенный" in task:
            return QColor(Qt.yellow)
        elif "Приоритет: Срочный" in task:
            return QColor(Qt.red)
        return QColor(Qt.white)

    def get_priority_icon(self, task):
        if "Приоритет: Обычный" in task:
            return QIcon(QPixmap("live.png"))
        elif "Приоритет: Повышенный" in task:
            return QIcon(QPixmap("middle.png"))
        elif "Приоритет: Срочный" in task:
            return QIcon(QPixmap("critical.png"))
        return QIcon()

    def update_history(self, text):
        self.history_text.appendPlainText(text)

    def save_history(self, text):
        history_file_path = os.path.join('DataBases', 'history.md')
        with open(history_file_path, 'a', encoding='utf-8') as file:
            file.write(f"{text} - {QDate.currentDate().toString(Qt.ISODate)}\n")

    def load_history(self):
        history_file_path = os.path.join('DataBases', 'history.md')
        if os.path.exists(history_file_path):
            with open(history_file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()  # Удалите лишние пробелы и символы новой строки
                    if line:  # Пропустите пустые строки
                        self.history_text.appendPlainText(line)

    def add_execute(self):
        execute_name = self.execute_input.text().strip()
        if execute_name:
            self.save_execute(execute_name)
            self.execute_input.clear()
            self.load_executes()
            self.update_history(f"Добавлен исполнитель: {execute_name}")
            self.save_history(f"Добавлен исполнитель: {execute_name}")
            # Покажите таблицу
            self.execute_table.show()

    def delete_execute(self):
        if self.selected_execute_index is not None:
            selected_row = self.selected_execute_index.row()
            if selected_row < self.execute_table.rowCount():
                item = self.execute_table.item(selected_row, 0)
                if item is not None:
                    execute_name = item.text()
                    reply = QMessageBox.question(self, 'Подтверждение',
                                                 f'Вы уверены, что хотите удалить исполнителя: {execute_name}?',
                                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        self.delete_execute_record(execute_name, selected_row)
                        self.load_executes()

    def delete_execute_record(self, execute_name, selected_row):
        execute_file_path = os.path.join('DataBases', 'execute.md')

        # Открываем старый файл на чтение и новый файл на запись
        with open(execute_file_path, 'r', encoding='utf-8') as old_file, \
                open('new_execute.md', 'w', encoding='utf-8') as new_file:
            for line in old_file:
                if line.strip() != execute_name:  # Пропускаем удаляемую запись
                    new_file.write(line)

        # Удаляем старый файл
        os.remove(execute_file_path)

        # Переименовываем новый файл в execute.md
        os.rename('new_execute.md', execute_file_path)

        # Очистите содержимое таблицы исполнителей
        self.execute_table.removeRow(selected_row)
        self.execute_table.setRowCount(self.execute_table.rowCount() - 1)

        self.update_history(f"Удален исполнитель: {execute_name}")
        self.save_history(f"Удален исполнитель: {execute_name}")
        self.load_executes()

    def save_execute(self, execute_name):
        execute_file_path = os.path.join('DataBases', 'execute.md')
        with open(execute_file_path, 'a', encoding='utf-8') as file:
            file.write(f"{execute_name}\n")

    def save_execute_table_to_file(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            for row in range(self.execute_table.rowCount()):
                item = self.execute_table.item(row, 0)
                if item is not None:
                    execute_name = item.text()
                    file.write(f"{execute_name}\n")

    def get_task_count_for_execute(self, execute_name):
        task_file_path = os.path.join('DataBases', 'tasks.md')
        count = 0
        if os.path.exists(task_file_path):
            with open(task_file_path, 'r', encoding='utf-8') as file:
                tasks = file.readlines()

            for task in tasks:
                if execute_name in task:
                    count += 1

            return count

    def handle_table_double_click(self, index):
        self.selected_execute_index = index
        self.delete_execute()

    def tab_changed(self, index):
        if index == 3:  # 4-я вкладка
            self.execute_table.setVisible(True)
            self.load_executes()
        else:
            self.execute_table.setVisible(False)


def main():
    app = QApplication(sys.argv)
    # Создание папки "DataBases", если её нет
    if not os.path.exists('DataBases'):
        os.mkdir('DataBases')

    window = DailyPlannerApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
