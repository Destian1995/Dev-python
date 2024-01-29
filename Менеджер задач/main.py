import os
import csv
from datetime import datetime
from operator import itemgetter
import pandas as pd
from PyQt5.QtCore import Qt, QVariant, QDateTime
from PyQt5.QtWidgets import QFrame, QComboBox, QTextBrowser, QMessageBox, QGridLayout, QInputDialog, QDateEdit, \
    QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QTableWidget, QTableWidgetItem,
    QPushButton, QVBoxLayout, QWidget, QLineEdit, QDialog,
    QLabel, QTextEdit, QHeaderView
)
import logging

logging.basicConfig(filename='debug.log', level=logging.DEBUG)

ver = "1.1.5"


class AssignExecutorDialog(QDialog):
    def __init__(self, user_names, parent=None):
        super(AssignExecutorDialog, self).__init__(parent)

        self.setWindowTitle('Назначение исполнителя')
        self.setFixedSize(300, 150)

        main_layout = QVBoxLayout(self)

        label_layout = QHBoxLayout()
        label_layout.addWidget(QLabel('Выберите исполнителя:'))

        combo_layout = QHBoxLayout()
        self.executor_combo = QComboBox()
        self.executor_combo.addItems(user_names)
        combo_layout.addWidget(self.executor_combo)

        button_layout = QHBoxLayout()
        btn_ok = QPushButton('ОК')
        btn_cancel = QPushButton('Отмена')
        btn_ok.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)
        button_layout.addWidget(btn_ok)
        button_layout.addWidget(btn_cancel)

        main_layout.addLayout(label_layout)
        main_layout.addLayout(combo_layout)
        main_layout.addLayout(button_layout)

        self.setStyleSheet(
            """
            QLabel {
                font-size: 14px;
                color: #333;
            }
            QComboBox {
                font-size: 14px;
            }
            QPushButton {
                font-size: 14px;
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;  /* Изменен цвет фона при наведении */
            }
            """
        )


class ReportDialog(QDialog):
    def __init__(self, users, parent=None):
        super(ReportDialog, self).__init__(parent)
        self.setWindowTitle('Закрытие задачи')
        self.setGeometry(750, 400, 500, 300)

        layout = QVBoxLayout(self)
        self.label = QLabel('Заполните отчет о проделанной работе:')
        self.label.setStyleSheet("font-weight: bold;")  # Apply styles to the text

        self.text_edit = QTextEdit(self)

        # Add a label for executor selection
        self.label_executor = QLabel('Кто закрывает задачу?')
        self.combo_box_executor = QComboBox(self)
        self.combo_box_executor.addItems(users)
        self.combo_box_executor.setCurrentIndex(0)  # Set the default selected index

        self.button_ok = QPushButton('Ок', self)
        self.button_ok.setStyleSheet("background-color: #3498db; color: white;")  # Apply styles to the button
        self.button_ok.clicked.connect(self.accept)

        layout.addWidget(self.label)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.label_executor)  # Add the executor label
        layout.addWidget(self.combo_box_executor)  # Add the QComboBox for executor selection
        layout.addWidget(self.button_ok)

    def get_report_text(self):
        return self.text_edit.toPlainText()

    def get_selected_executor(self):
        return self.combo_box_executor.currentText()


class CreateTaskDialog(QDialog):
    def __init__(self, parent=None):
        super(CreateTaskDialog, self).__init__(parent)
        self.setWindowTitle('Создать задачу')

        layout = QGridLayout(self)

        self.label_task_name = QLabel('Название задачи:')
        self.edit_task_name = QLineEdit(self)

        self.label_task_details = QLabel('Детали задачи:')
        self.edit_task_details = QTextEdit(self)

        self.label_task_priority = QLabel('Приоритет задачи:')
        self.edit_task_priority = QComboBox(self)
        self.edit_task_priority.addItems(['Низкий', 'Средний', 'Высокий'])

        self.label_task_deadline = QLabel('Дедлайн задачи:')
        self.date_edit_deadline = QDateEdit(self)
        self.date_edit_deadline.setCalendarPopup(True)

        self.button_create = QPushButton('Создать', self)
        self.button_cancel = QPushButton('Отмена', self)

        # Добавление элементов на сетку
        layout.addWidget(self.label_task_name, 0, 0)
        layout.addWidget(self.edit_task_name, 0, 1)
        layout.addWidget(self.label_task_details, 1, 0)
        layout.addWidget(self.edit_task_details, 1, 1)
        layout.addWidget(self.label_task_priority, 2, 0)
        layout.addWidget(self.edit_task_priority, 2, 1)
        layout.addWidget(self.label_task_deadline, 3, 0)
        layout.addWidget(self.date_edit_deadline, 3, 1)
        layout.addWidget(self.button_create, 4, 0)
        layout.addWidget(self.button_cancel, 4, 1)

        self.button_create.setStyleSheet("background-color: #008CBA; color: white;")
        self.button_cancel.setStyleSheet("background-color: #f44336; color: white;")

        self.button_create.clicked.connect(self.accept)
        self.button_cancel.clicked.connect(self.reject)


class TaskManager(QMainWindow):
    def __init__(self):
        super(TaskManager, self).__init__()
        self.setWindowTitle('Менеджер задач "Скайлайн"')
        self.setGeometry(250, 150, 1480, 850)

        tab_home = QWidget()
        tab_home.setStyleSheet("""
            background-color: #ecf0f1; /* Clouds */
        """)
        self.check_directories_and_files()

        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        # Создаем QTableWidget для отображения задач
        self.tab_widget.addTab(tab_home, 'Главная')
        self.tab_widget.setCurrentWidget(tab_home)
        self.tree_tasks = QTableWidget()
        self.task_details = ''
        self.tree_reports = QTableWidget()
        self.current_report_search_text = ''
        self.reports = []  # Инициализируем список отчетов

        # Create interfaces and applets
        self.create_task_interface()
        self.create_reports_interface()
        self.create_users_interface()
        self.create_main_tab_applets()
        self.create_about_tab()  # Добавлен вызов метода для создания вкладки "О программе"
        self.tab_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tab_widget.setStyleSheet("""
            QTabWidget::tab:selected { background-color: #3498db; }
            QTabBar::tab { font-size: 14px; color: #2c3e50; }  # Цвет текста и размер шрифта
        """)
        self.tab_widget.setTabPosition(QTabWidget.North)
        self.tab_widget.setStyleSheet("""
            QTabBar::tab {
                background-color: #ecf0f1;  /* Clouds */
                border: 1px solid #bdc3c7;   /* Silver */
                border-radius: 5px;
                padding: 10px 20px;
                margin-right: 5px;
            }

            QTabBar::tab:selected {
                background-color: #3498db;  /* Belize Hole */
                color: white;
            }

            QTabBar::tab:hover {
                background-color: #3498db;  /* Belize Hole */
                color: white;
            }
        """)

        # Растягиваем кнопки вкладок на весь размер
        self.tab_widget.tabBar().setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Load reports during initialization
        self.load_reports()
        self.selected_executor = None

    def create_about_tab(self):
        tab_about = QWidget()
        tab_about.setStyleSheet("""
            background-color: #f0f0f0; /* Background color */
        """)
        layout_about = QVBoxLayout(tab_about)

        label_about = QLabel('О программе', self)
        label_about.setStyleSheet("""
            font-size: 18pt;
            font-weight: bold;
            color: #333333; /* Text color */
            margin-bottom: 15px;
            text-align: center;
        """)

        # Открываем и читаем файл dev.md
        dev_file_path = 'dev.md'
        if not os.path.exists(dev_file_path):
            # Если файла нет, создаем его с заглушкой
            with open(dev_file_path, 'w', encoding='utf-8') as file:
                file.write("Свяжитесь с разработчиком по адресу: Lerdonia@mail.ru")

        with open(dev_file_path, 'r', encoding='utf-8') as file:
            contacts_data = file.read()

        about_info = (
            "Менеджер задач \"Скайлайн\"\n"
             f"версия: \n{ver}.\n"
            "Программа для управления задачами и отчетами. Позволяет отслеживать текущие задачи, "
            "формировать отчеты и следить за дедлайнами.\n\n"
            f"Связь с разработчиком:\n{contacts_data}"
        )

        self.edit_about = QTextEdit(self)
        self.edit_about.setHtml(
            f'<p style="font-size: 14pt; font-weight: bold; color: #555555;">{about_info}</p>'
        )
        self.edit_about.setReadOnly(True)
        self.edit_about.setStyleSheet("""
            border: 1px solid #cccccc; /* Border color */
            padding: 15px;
            background-color: #ffffff; /* Content background color */
            color: #333333; /* Text color */
            font-size: 12pt;
            margin: 15px;
            border-radius: 10px;
        """)

        layout_about.addWidget(label_about)
        layout_about.addWidget(self.edit_about)

        tab_about.setLayout(layout_about)
        self.tab_widget.addTab(tab_about, 'О программе')

    def check_directories_and_files(self):
        # Проверяем наличие каталогов
        if not os.path.exists('db_tas'):
            os.makedirs('db_tas')

<<<<<<< HEAD
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
=======
        # Проверяем наличие файла с задачами
        tasks_file_path = 'db_tas/tasks.csv'
        if not os.path.exists(tasks_file_path):
            with open(tasks_file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['ID', 'Задача', 'Статус'])
                writer.writeheader()

        # Проверяем наличие файла с отчетами
        reports_file_path = 'db_tas/reports.md'
        if not os.path.exists(reports_file_path):
            with open(reports_file_path, 'w', newline='', encoding='utf-8') as file:
                file.write("")

    ######################## Секция создания вкладки главная ##############################################

    def create_main_tab_applets(self):
        applet1 = self.create_applet1()
        applet2 = self.create_applet2()

        # Layout setup
        layout_home = QVBoxLayout(self.tab_widget.currentWidget())
        layout_home.addWidget(applet1)
        layout_home.addWidget(applet2)
        self.tab_widget.currentWidget().setLayout(layout_home)

    def create_applet1(self):
        applet = QWidget()
        layout = QVBoxLayout(applet)

        # Label for the applet
        label = QLabel("Задачи срок которых истекает сегодня")
        label.setStyleSheet("font-size: 16px; font-weight: bold; color: #3498db;")
        layout.addWidget(label, alignment=Qt.AlignCenter)

        # Get tasks with deadlines today
        today = datetime.now().strftime("%d.%m.%Y")
        tasks_today = [task for task in self.tasks if task.get('Дедлайн') == today]

        # Create a QTableWidget to display tasks
        table = QTableWidget()
        table.setColumnCount(4)  # Updated to add the "Исполнитель" column
        table.setHorizontalHeaderLabels(['ID', 'Задача', 'Дедлайн', 'Исполнитель'])

        for task in tasks_today:
            row_position = table.rowCount()
            table.insertRow(row_position)
            table.setItem(row_position, 0, QTableWidgetItem(task.get('ID', '')))
            table.setItem(row_position, 1, QTableWidgetItem(task.get('Задача', '')))
            table.setItem(row_position, 2, QTableWidgetItem(task.get('Дедлайн', '')))
            table.setItem(row_position, 3, QTableWidgetItem(task.get('Исполнитель', '')))  # Added "Исполнитель" column

        # Set horizontal stretch policy for the table
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(table)
        applet.setLayout(layout)
        return applet

    def create_applet2(self):
        applet = QWidget()
        layout = QVBoxLayout(applet)

        # Label for the applet
        label = QLabel("Задачи с высоким приоритетом")
        label.setStyleSheet("font-size: 16px; font-weight: bold; color: #3498db;")
        layout.addWidget(label, alignment=Qt.AlignCenter)

        # Get tasks with high priority
        high_priority_tasks = [task for task in self.tasks if task.get('Приоритет') == 'Высокий']

        # Create a QTableWidget to display tasks
        table = QTableWidget()
        table.setColumnCount(4)  # Updated to add the "Исполнитель" column
        table.setHorizontalHeaderLabels(['ID', 'Задача', 'Приоритет', 'Исполнитель'])

        for task in high_priority_tasks:
            row_position = table.rowCount()
            table.insertRow(row_position)
            table.setItem(row_position, 0, QTableWidgetItem(task.get('ID', '')))
            table.setItem(row_position, 1, QTableWidgetItem(task.get('Задача', '')))
            table.setItem(row_position, 2, QTableWidgetItem(task.get('Приоритет', '')))
            table.setItem(row_position, 3, QTableWidgetItem(task.get('Исполнитель', '')))  # Added "Исполнитель" column

        # Set horizontal stretch policy for the table
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(table)
        applet.setLayout(layout)
        return applet

    def update_main_tab_applets(self):
        applet1 = self.create_applet1()
        applet2 = self.create_applet2()

        # Clear the layout and add updated applets
        layout_home = QVBoxLayout(self.tab_widget.currentWidget())
        layout_home.addWidget(applet1)
        layout_home.addWidget(applet2)
        self.tab_widget.currentWidget().setLayout(layout_home)

    ######################## Секция создания вкладки задач ################################################

    def create_task_interface(self):
        # Создаем вкладку для задач
        tab_tasks = QWidget()
        tab_tasks.setStyleSheet("background-color: #ecf0f1;")

        # Создаем таблицу для отображения задач
        self.tree_tasks = QTableWidget(tab_tasks)
        self.tree_tasks.setColumnCount(7)  # Инкремент колонок
        self.tree_tasks.setHorizontalHeaderLabels(
            ['ID', 'Задача', 'Статус', 'Приоритет', 'Дедлайн', 'Детали', 'Исполнитель'])

        # Растягиваем столбцы на всю ширину
        header = self.tree_tasks.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Устанавливаем стили для таблицы
        self.tree_tasks.setStyleSheet("""
            QTableWidget QHeaderView::section {
                background-color: #3498db; /* Belize Hole */
                color: white;
                font-size: 14px;
                font-weight: bold;
            }

            QTableWidget::item {
                background-color: #ecf0f1; /* Clouds */
                color: #34495e; /* Midnight Blue */
            }

            QTableWidget::item:selected {
                background-color: #3498db; /* Belize Hole */
                color: white;
            }
        """)
        # Устанавливаем стили для кнопок
        btn_styles = """
                            QPushButton {
                                background-color: #3498db; /* Belize Hole */
                                color: white;
                                border: 1px solid #3498db; /* Belize Hole */
                                padding: 10px 20px;
                                font-size: 16px;
                                border-radius: 5px;
                            }

                            QPushButton:hover {
                                background-color: #2980b9; /* Darker Blue on hover */
                            }
                        """

        # Layout setup
        layout = QVBoxLayout(tab_tasks)

        sort_layout = QHBoxLayout()
        btn_sort_priority = QPushButton('Сортировать по приоритету', tab_tasks)
        btn_sort_priority.clicked.connect(self.sort_by_priority)
        btn_sort_priority.setStyleSheet(btn_styles)  # Apply the same style

        btn_sort_executor = QPushButton('Сортировать по исполнителю', tab_tasks)
        btn_sort_executor.clicked.connect(self.sort_by_executor)
        btn_sort_executor.setStyleSheet(btn_styles)  # Apply the same style

        btn_sort_deadline = QPushButton('Сортировать по дедлайну', tab_tasks)
        btn_sort_deadline.clicked.connect(self.sort_by_deadline)
        btn_sort_deadline.setStyleSheet(btn_styles)  # Apply the same style

        btn_reset_filters = QPushButton('Сброс фильтров', tab_tasks)
        btn_reset_filters.clicked.connect(self.reset_filters)
        btn_reset_filters.setStyleSheet(btn_styles)
        layout.addWidget(btn_reset_filters)

        sort_layout.addWidget(btn_sort_priority)
        sort_layout.addWidget(btn_sort_executor)
        sort_layout.addWidget(btn_sort_deadline)
        sort_layout.addWidget(btn_reset_filters)

        # Add sorting buttons layout to the main layout
        layout.addLayout(sort_layout)

        # Кнопки
        btn_create_task = QPushButton('Создать задачу', tab_tasks)
        btn_create_task.clicked.connect(self.create_task)
        btn_close_task = QPushButton('Закрыть задачу', tab_tasks)
        btn_close_task.clicked.connect(self.close_task)

        # Устанавливаем иконки для кнопок
        btn_create_task.setIcon(QIcon('icons/create.png'))
        btn_close_task.setIcon(QIcon('icons/close.png'))

        btn_assign_executor = QPushButton('Назначить исполнителя', tab_tasks)
        btn_assign_executor.clicked.connect(self.assign_executor)
        btn_assign_executor.setStyleSheet(btn_styles)
        btn_create_task.setStyleSheet(btn_styles)
        btn_close_task.setStyleSheet(btn_styles)

        # Add some spacing between the elements
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Add the table and buttons to the layout
        layout.addWidget(self.tree_tasks)
        layout.addWidget(btn_assign_executor)
        layout.addWidget(btn_create_task)
        layout.addWidget(btn_close_task)

        tab_tasks.setLayout(layout)
        self.update_task_table()

        self.tab_widget.addTab(tab_tasks, 'Задачи')

        # Загружаем задачи при запуске программы
        self.update_task_table()

    def assign_executor(self):
        selected_row = self.tree_tasks.currentRow()
        if selected_row >= 0:
            task_id = int(self.tree_tasks.item(selected_row, 0).text())

            # Создаем кастомное диалоговое окно
            dialog = AssignExecutorDialog(self.get_user_names(), self)
            result = dialog.exec_()

            if result == QDialog.Accepted:
                executor = dialog.executor_combo.currentText()

                # Остальной код остается без изменений
                self.tree_tasks.setItem(selected_row, 5, QTableWidgetItem(executor))
                task = self.get_task_by_id(task_id)
                if task:
                    task['Исполнитель'] = executor
                    task['Статус'] = 'В работе'
                    tasks_df = pd.DataFrame(self.tasks)
                    tasks_df.to_csv('db_tas/tasks.csv', index=False, encoding='utf-8')
                    self.load_tasks()
                    self.update_users(executor)
                    self.update_task_table()

    def update_users(self, new_user):
        # Load existing users
        self.load_users()

        # Check if the user is already in the list
        if new_user not in self.get_user_names():
            # Add the new user
            self.users.append({'Имя': new_user})

            # Save the updated users to the CSV file
            users_df = pd.DataFrame(self.users)
            users_df.to_csv('db_tas/users.csv', index=False, encoding='utf-8')

    def create_task(self):
        create_task_dialog = CreateTaskDialog(self)
        result = create_task_dialog.exec_()

        if result == QDialog.Accepted:
            task_name = create_task_dialog.edit_task_name.text()
            task_details = create_task_dialog.edit_task_details.toPlainText()
            task_priority = create_task_dialog.edit_task_priority.currentText()
            task_deadline = create_task_dialog.date_edit_deadline.date().toString("dd.MM.yyyy")

            # Automatically assign executor from tasks.csv
            assigned_executor = self.get_assigned_executor(task_name)

            if task_name:
                task_id = self.get_next_task_id()
                task_status = 'Открыта'
                new_task = {'ID': str(task_id), 'Задача': task_name, 'Статус': task_status,
                            'Детали': task_details, 'Приоритет': task_priority, 'Дедлайн': task_deadline,
                            'Исполнитель': assigned_executor}

                self.save_task(new_task)
                self.update_task_table()
                self.create_main_tab_applets()
                self.update_main_tab_applets()

    def get_assigned_executor(self, task_name):
        # Retrieve assigned executor from tasks.csv
        task = self.get_task_by_name(task_name)
        if task:
            return task.get('Исполнитель', '')
        return ''

    def close_task(self):
        selected_row = self.tree_tasks.currentRow()
        if selected_row >= 0:
            task_id = int(self.tree_tasks.item(selected_row, 0).text())
            task_name = self.tree_tasks.item(selected_row, 1).text()

            # Create and show the ReportDialog
            report_dialog = ReportDialog(self.get_user_names())
            result = report_dialog.exec_()

            if result == QDialog.Accepted:
                report_text = report_dialog.get_report_text()
                closing_date = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss")
                assigned_executor = report_dialog.get_selected_executor()

                # Save the report to the reports file
                self.save_report(task_name, report_text, closing_date, assigned_executor)

                # Update the task status to "Closed" in the internal data structure
                task = self.get_task_by_id(task_id)
                if task:
                    task['Статус'] = 'Закрыта'
                    task['Исполнитель'] = assigned_executor

                    # Update the CSV file excluding the closed task
                    tasks_df = pd.DataFrame(self.tasks)
                    tasks_df = tasks_df[tasks_df['ID'] != task_id]  # Exclude the closed task
                    tasks_df.to_csv('db_tas/tasks.csv', index=False, encoding='utf-8')

                    self.remove_closed_task(task_id)
                    # Load the updated tasks
                    self.load_tasks()

                    # Update the users list
                    self.update_users(assigned_executor)

                    # Update the task table
                    self.update_task_table()

                    # Load reports to update the "Отчеты" tab
                    self.load_reports()

    def get_task_by_name(self, task_name):
        self.load_tasks()
        task = next((t for t in self.tasks if t['Задача'] == task_name), None)
        return task

    def remove_closed_task(self, task_id):
        # Remove the closed task from the file tasks.csv
        tasks_file_path = 'db_tas/tasks.csv'
        temp_file_path = 'db_tas/tasks_temp.csv'

        with open(tasks_file_path, 'r', newline='', encoding='utf-8') as input_file, \
                open(temp_file_path, 'w', newline='', encoding='utf-8') as output_file:
            reader = csv.DictReader(input_file)
            fieldnames = reader.fieldnames

            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                if row['ID'] != str(task_id):
                    writer.writerow(row)

        # Close the file handles before renaming
        input_file.close()
        output_file.close()

        # Rename the temporary file to overwrite the original file
        os.replace(temp_file_path, tasks_file_path)
        self.create_main_tab_applets()

    def update_task_table(self, tasks=None):
        self.load_tasks()
        if tasks is None:
            tasks = self.tasks

        self.tree_tasks.setRowCount(0)  # Clear existing rows in the table

        for task in tasks:
            row_position = self.tree_tasks.rowCount()
            self.tree_tasks.insertRow(row_position)

            # Populate the table with task information
            self.tree_tasks.setItem(row_position, 0, QTableWidgetItem(str(task['ID'])))
            self.tree_tasks.setItem(row_position, 1, QTableWidgetItem(task['Задача']))
            self.tree_tasks.setItem(row_position, 2, QTableWidgetItem(task['Статус']))
            self.tree_tasks.setItem(row_position, 3, QTableWidgetItem(task.get('Приоритет', '')))
            self.tree_tasks.setItem(row_position, 4, QTableWidgetItem(task.get('Дедлайн', '')))
            self.tree_tasks.setItem(row_position, 5, QTableWidgetItem(task.get('Детали', '')))
            self.tree_tasks.setItem(row_position, 6, QTableWidgetItem(task.get('Исполнитель', '')))

            # Add the deadline item to the table
            deadline_item = QTableWidgetItem(task.get('Дедлайн', ''))
            self.tree_tasks.setItem(row_position, 4, deadline_item)

            # Add button to show task details
            btn_show_details = QPushButton('Показать детали задачи', self)
            btn_show_details.setStyleSheet("color: #3498db;")
            btn_show_details.clicked.connect(lambda _, row=row_position: self.toggle_details(row))
            self.tree_tasks.setCellWidget(row_position, 5, btn_show_details)

        # Refresh the table
        self.tree_tasks.viewport().update()
        self.create_main_tab_applets()

    def toggle_details(self, row):
        # Получаем текущую кнопку
        btn = self.tree_tasks.cellWidget(row, 5)
        self.show_task_details(row)

    def show_task_details(self, row):
        task_details = self.tasks[row].get('Детали', '')

        # Create a dialog window to display task details
        details_dialog = QDialog(self)
        details_dialog.setWindowTitle('Детали задачи')

        # Add a frame and rounded corners to the dialog window
        details_dialog.setStyleSheet("QDialog { background-color: #ffffff; border: 2px solid #3498DB; border-radius: 10px; }")

        # Create a layout for the dialog window
        details_dialog_layout = QVBoxLayout(details_dialog)

        # Add a label with the task details text
        details_label = QLabel(task_details)
        details_label.setWordWrap(True)  # Enable text wrapping if it doesn't fit
        details_label.setStyleSheet("font-size: 14pt; color: #34495e;")  # Style the text

        # Add a frame around the label
        details_label_frame = QFrame()
        details_label_frame.setFrameStyle(QFrame.Panel | QFrame.Plain)
        details_label_frame.setLineWidth(2)
        details_label_frame.setStyleSheet("QFrame { border-color: #3498DB; }")

        # Add the label to the frame
        details_label_frame_layout = QVBoxLayout(details_label_frame)
        details_label_frame_layout.addWidget(details_label)

        # Add the frame with the label to the layout
        details_dialog_layout.addWidget(details_label_frame)

        # Add a horizontal layout for buttons
        button_layout = QHBoxLayout()

        # Add a close button
        close_button = QPushButton('Закрыть')
        close_button.clicked.connect(details_dialog.close)
        button_layout.addWidget(close_button)

        # Style the close button
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: 1px solid #3498DB;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        # Add the button layout to the main layout
        details_dialog_layout.addLayout(button_layout)

        # Show the dialog window
        details_dialog.exec_()
>>>>>>> 8f148c897103ea5f7c8eb213de733fd0d0d73d0c

    def load_tasks(self):
        try:
            with open('db_tas/tasks.csv', 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.tasks = list(reader)
        except FileNotFoundError:
            self.tasks = []
        except Exception as e:
            print(f"Error loading tasks: {e}")
        self.load_users()

    def save_tasks(self):
        tasks_file_path = 'db_tas/tasks.csv'
        with open(tasks_file_path, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['ID', 'Задача', 'Статус', 'Приоритет', 'Детали', 'Исполнитель', 'Дедлайн']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.tasks)

    def save_task(self, task):
        self.load_tasks()
        if 'Приоритет' not in task:
            task['Приоритет'] = ''
        self.tasks.append(task)
        self.save_tasks()

<<<<<<< HEAD
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
                        
    def clear_history(self):
        history_file_path = os.path.join('DataBases', 'history.md')
        if os.path.exists(history_file_path):
            with open(history_file_path, 'w', encoding='utf-8') as file:
                file.write('')
        self.load_history()

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
=======
    def sort_by_priority(self):
        # Check if selected_executor is defined
        if hasattr(self, 'selected_executor') and self.selected_executor:
            filtered_tasks = [task for task in self.tasks if task.get('Исполнитель', '') == self.selected_executor]
>>>>>>> 8f148c897103ea5f7c8eb213de733fd0d0d73d0c
        else:
            filtered_tasks = self.tasks

        # Define a custom order for priority
        priority_order = {'Высокий': 1, 'Средний': 2, 'Низкий': 3}

        # Sort filtered tasks by priority using the custom order
        sorted_tasks = sorted(filtered_tasks, key=lambda x: priority_order.get(x.get('Приоритет', ''), float('inf')))
        self.update_task_table(sorted_tasks)

    def sort_by_executor(self):
        executor, ok_pressed = QInputDialog.getItem(
            self,
            'Сортировка',
            'Выберите исполнителя:',
            self.get_user_names(),
            0,
            False
        )

        if ok_pressed:
            self.selected_executor = executor
            self.apply_sort_filters()

    def sort_by_deadline(self):
        # Filter tasks for the selected executor if one is selected
        if self.selected_executor:
            filtered_tasks = [task for task in self.tasks if task.get('Исполнитель', '') == self.selected_executor]
        else:
            filtered_tasks = self.tasks

        # Sort tasks by deadline using the 'Дедлайн' key
        sorted_tasks = sorted(filtered_tasks, key=itemgetter('Дедлайн'))
        self.update_task_table(sorted_tasks)

    def apply_sort_filters(self):
        if self.selected_executor:
            filtered_tasks = [task for task in self.tasks if task.get('Исполнитель', '') == self.selected_executor]
            self.update_task_table(filtered_tasks)
        else:
            self.update_task_table()

    def reset_filters(self):
        self.selected_executor = None
        self.apply_sort_filters()

    #################  Секция создания вкладки отчетов  ###############################################

    def create_reports_interface(self):
        # Создаем вкладку для отчетов
        tab_reports = QWidget()
        tab_reports.setStyleSheet("background-color: #ecf0f1;")

        # Создаем таблицу для отображения отчетов
        self.tree_reports = QTableWidget(tab_reports)
        self.tree_reports.setColumnCount(5)  # Обновлено количество столбцов
        self.tree_reports.setHorizontalHeaderLabels(
            ['Задача', 'Отчет', 'Детали задачи', 'Дата закрытия', 'Исполнитель'])

        # Stretch the columns to the full width
        header = self.tree_reports.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        search_bar = QLineEdit(self)
        search_bar.setPlaceholderText("Поиск по отчетам...")

        # Set the background color of the search bar to beige
        search_bar.setStyleSheet("""
            background-color: #f5f5f5; /* Silver */
            padding: 10px;
            border: 1px solid #3498db; /* Belize Hole */
            border-radius: 5px;
            color: #34495e; /* Midnight Blue */
        """)

        # Set individual column colors
        self.tree_reports.setStyleSheet("""
            QTableWidget QHeaderView::section {
                background-color: #3498db; /* Belize Hole */
                color: white;
                font-size: 14px;
                font-weight: bold;
            }

            QTableWidget::item {
                background-color: #ecf0f1; /* Clouds */
                color: #34495e; /* Midnight Blue */
            }

            QTableWidget::item:selected {
                background-color: #3498db; /* Belize Hole */
                color: white;
            }
        """)

        # Set button styles
        btn_search_styles = """
            QPushButton {
                background-color: #3498db; /* Belize Hole */
                color: white;
                border: 1px solid #3498db; /* Belize Hole */
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #2980b9; /* Darker Blue on hover */
            }
        """

        search_bar.setStyleSheet(search_bar.styleSheet() + btn_search_styles)

        # Connect the search bar's textChanged signal to the search_reports function
        search_bar.textChanged.connect(self.search_reports)

        layout = QVBoxLayout()
        layout.addWidget(search_bar)
        layout.addWidget(self.tree_reports)

        tab_reports.setLayout(layout)

        # Вызываем метод загрузки отчетов при инициализации
        self.load_reports()

        # Показываем все отчеты при запуске
        self.update_reports_table(self.reports)

        self.tab_widget.addTab(tab_reports, 'Отчеты')
        self.tree_reports.itemDoubleClicked.connect(self.show_full_text)

    def show_full_text(self, item):
        # Create a separate window to display the full text
        self.full_text_window = QWidget()
        self.full_text_window.setWindowTitle('Полный текст')

        # Use a QVBoxLayout for the layout
        layout = QVBoxLayout(self.full_text_window)

        # Create a QTextBrowser to display the full text
        text_browser = QTextBrowser()
        text_browser.setPlainText(item.text())  # Set the full text to the content of the clicked item
        text_browser.setReadOnly(True)  # Make it read-only
        layout.addWidget(text_browser)

        # Create a close button to close the window
        close_button = QPushButton('Закрыть')
        close_button.clicked.connect(self.full_text_window.close)
        layout.addWidget(close_button)

        # Apply styles to the full_text_window
        self.full_text_window.setStyleSheet("""
            background-color: #ecf0f1; /* Clouds */
            color: #34495e; /* Midnight Blue */
            font-size: 14px;
        """)

        # Apply styles to the text_browser
        text_browser.setStyleSheet("""
            background-color: #ffffff; /* White */
            color: #34495e; /* Midnight Blue */
            border: 1px solid #3498db; /* Belize Hole */
            border-radius: 5px;
            padding: 10px;
        """)

        # Apply styles to the close_button
        close_button.setStyleSheet("""
            background-color: #3498db; /* Belize Hole */
            color: white;
            border: 1px solid #3498db; /* Belize Hole */
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 5px;
        """)

        # Show the window
        self.full_text_window.show()

    def search_reports(self, text):
        # Сохраняем текущий текст поиска
        self.current_report_search_text = text.lower()

        if not text:
            # Если поисковая строка пуста, сбрасываем состояние таблицы
            self.load_reports()
        else:
            # Иначе фильтруем отчеты и обновляем таблицу
            self.filter_reports_and_update_table(text)

    def filter_reports_and_update_table(self, search_text):
        try:
            reports_file_path = 'db_tas/reports.md'
            if os.path.exists(reports_file_path):
                with open(reports_file_path, 'r', encoding='utf-8') as file:
                    reports_content = file.read()

                # Parse reports from Markdown content
                reports = self.parse_reports_markdown(reports_content)

                # Filter reports based on the search text
                filtered_reports = [report for report in reports if self.contains_search_text(report, search_text)]

                # Update the reports table with filtered reports
                self.update_reports_table(filtered_reports)

        except Exception as e:
            print(f"Error filtering and updating reports table: {e}")

    def contains_search_text(self, report, search_text):
        # Проверяем, содержится ли поисковый текст в любом поле отчета
        for cell in report:
            if search_text in cell.lower():
                return True
        return False

    def search_all(self, text):
        # Convert the search text to lowercase for case-insensitive search
        search_text = text.lower()

        # Load all tasks and reports
        self.load_tasks()
        self.load_reports()
        self.update_task_table()

        # Filter reports based on the search text
        filtered_reports = [report for report in self.reports if
                            search_text in report['Задача'].lower() or
                            search_text in report['Отчет'].lower() or
                            search_text in report.get('Детали', '').lower()]

        # Update the tree_reports with filtered reports
        self.update_reports_table(filtered_reports)

    def update_reports_table(self, reports):
        self.tree_reports.setRowCount(0)
        for report in reports:
            row_position = self.tree_reports.rowCount()
            self.tree_reports.insertRow(row_position)
            for col in range(min(len(report), 5)):
                value = report[col]
                item = QTableWidgetItem(str(value))
                self.tree_reports.setItem(row_position, col, item)

    def load_reports(self):
        self.tree_reports.setRowCount(0)
        try:
            reports_file_path = 'db_tas/reports.md'
            if os.path.exists(reports_file_path):
                with open(reports_file_path, 'r', encoding='utf-8') as file:
                    reports_content = file.read()

                reports = self.parse_reports_markdown(reports_content)

                for row, report in enumerate(reports):
                    self.tree_reports.insertRow(row)
                    for col, value in enumerate(report):
                        if col == 1 or col == 2:
                            item = QTableWidgetItem()
                            item.setData(Qt.TextColorRole, QColor(Qt.blue))  # Устанавливаем синий цвет текста
                            item.setData(Qt.TextSingleLine, False)  # Разрешаем многострочный текст
                            item.setData(Qt.DisplayRole,
                                         QVariant(value.replace('<br>', '\n')))  # Заменяем <br> на новую строку
                            self.tree_reports.setItem(row, col, item)
                        else:
                            self.tree_reports.setItem(row, col, QTableWidgetItem(str(value)))

        except Exception as e:
            print(f"Error loading reports: {e}")

    def parse_reports_markdown(self, content):
        reports = []
        lines = content.split('\n')
        for line in lines:
            # Разделение ячеек в строке таблицы
            cells = line.split('|')
            # Исключаем пустые ячейки
            cells = [cell.strip() for cell in cells if cell.strip()]

            if cells:
                reports.append(cells)

        return reports

    def get_next_task_id(self):
        self.load_tasks()
        if not self.tasks:
            return 1
        else:
            return int(max(task['ID'] for task in self.tasks)) + 1

    def get_task_by_id(self, task_id):
        self.load_tasks()
        task = next((task for task in self.tasks if int(task['ID']) == task_id), None)

        return task

    def save_report(self, task_name, report, closing_date, assigned_executor):
        reports_file_path = 'db_tas/reports.md'
        with open(reports_file_path, 'a', encoding='utf-8') as file:
            report_line = "| {} | {} | {} | {} | {} |\n".format(
                task_name,
                self.replace_br_with_newline(report),
                self.replace_br_with_newline(self.get_task_details(task_name)),
                closing_date,
                assigned_executor
            )
            file.write(report_line)

    def replace_br_with_newline(self, value):
        return value.replace('\n', '<br>')

    def get_task_details(self, task_name):
        task = next((t for t in self.tasks if t['Задача'] == task_name), None)
        if task:
            return task.get('Детали', '')
        else:
            return ''

    ################### Секция создания вкладки пользователей #####################################################

    def create_users_interface(self):
        # Создаем вкладку для пользователей
        tab_users = QWidget()
        tab_users.setStyleSheet("background-color: #ecf0f1;")

        # Create labels for FIO and Position
        label_name = QLabel('ФИО Исполнителя', tab_users)
        label_position = QLabel('Должность', tab_users)

        # Create Line Edits for FIO and Position
        self.line_edit_name = QLineEdit(tab_users)
        self.line_edit_position = QLineEdit(tab_users)

        # Create a button for adding a new user
        btn_add_user = QPushButton('Добавить пользователя', tab_users)
        btn_add_user.clicked.connect(self.add_user)

        # Set styles for the button
        btn_add_user.setStyleSheet("""
            QPushButton {
                background-color: #3498db; /* Belize Hole */
                color: white;
                border: 1px solid #3498db; /* Belize Hole */
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #2980b9; /* Darker Blue on hover */
            }
        """)

        # Layout setup
        layout = QVBoxLayout(tab_users)

        # Add labels and Line Edits for FIO and Position using a grid layout
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        grid_layout.addWidget(label_name, 0, 0)
        grid_layout.addWidget(self.line_edit_name, 0, 1)
        grid_layout.addWidget(label_position, 1, 0)
        grid_layout.addWidget(self.line_edit_position, 1, 1)

        # Add grid layout to the main layout
        layout.addLayout(grid_layout)

        # Create таблицу для отображения пользователей
        self.tree_users = QTableWidget(tab_users)
        self.tree_users.setColumnCount(2)
        self.tree_users.setHorizontalHeaderLabels(['ФИО Исполнителя', 'Должность'])

        # Растягиваем столбцы на всю ширину
        header = self.tree_users.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        # Set individual column colors
        self.tree_users.setStyleSheet("""
            QTableWidget QHeaderView::section {
                background-color: #3498db; /* Belize Hole */
                color: white;
                font-size: 14px;
                font-weight: bold;
            }

            QTableWidget::item {
                background-color: #ecf0f1; /* Clouds */
                color: #34495e; /* Midnight Blue */
            }

            QTableWidget::item:selected {
                background-color: #3498db; /* Belize Hole */
                color: white;
            }
        """)
        btn_delete_user = QPushButton('Удалить пользователя', tab_users)
        btn_delete_user.clicked.connect(self.delete_user)

        # Set styles for the delete button
        btn_delete_user.setStyleSheet("""
                    QPushButton {
                        background-color: #e74c3c; /* Alizarin */
                        color: white;
                        border: 1px solid #e74c3c; /* Alizarin */
                        padding: 10px 20px;
                        font-size: 16px;
                        border-radius: 5px;
                    }

                    QPushButton:hover {
                        background-color: #c0392b; /* Darker Red on hover */
                    }
                """)

        # Add the delete button to the layout
        layout.addWidget(btn_add_user)
        layout.addWidget(btn_delete_user)
        layout.addWidget(self.tree_users)

        tab_users.setLayout(layout)

        # Load users when initializing the application
        self.load_users()

        # Show all users on startup
        self.update_users_table()

        # Add the "Users" tab
        self.tab_widget.addTab(tab_users, 'Пользователи')

    def add_user(self):
        name = self.line_edit_name.text()
        position = self.line_edit_position.text()

        if name and position:
            users = self.load_users() or []
            new_user = {'name': name, 'position': position}
            users.append(new_user)
            self.save_users(users)
            self.update_users_table()

            # Clear the input fields after adding a user
            self.line_edit_name.clear()
            self.line_edit_position.clear()
        else:
            QMessageBox.warning(
                self,
                'Добавление нового исполнителя',
                'Заполните все поля для создания нового исполнителя',
                QMessageBox.Ok
            )

    def delete_user(self):
        selected_row = self.tree_users.currentRow()

        if selected_row >= 0:
            # Load existing users
            users = self.load_users() or []

            # Remove the selected user
            deleted_user = users.pop(selected_row)

            # Save the updated users list
            self.save_users(users)

            # Update the table with the new user
            self.update_users_table()

            QMessageBox.information(
                self,
                'Удаление исполнителя',
                f"Исполнитель '{deleted_user['name']}' был удален.",
                QMessageBox.Ok
            )
        else:
            QMessageBox.warning(
                self,
                'Исполнитель не выбран',
                'Пожалуйста, выберите из таблицы исполнителя, а затем нажмите кнопку удаления',
                QMessageBox.Ok
            )
        self.load_users()
        self.update_task_table()

    def save_users(self, users):
        with open(r'db_tas\users.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'position']  # Adjust these based on your user data structure
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(users)

    def load_users(self):
        try:
            with open(r'db_tas\users.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                users = list(reader)
            return users
        except FileNotFoundError:
            return None

    def update_users_table(self):
        users = self.load_users()
        if users is not None:
            # Assuming you have a QTableWidget named self.tree_users
            self.tree_users.setRowCount(len(users))
            for row, user in enumerate(users):
                self.tree_users.setItem(row, 0, QTableWidgetItem(user['name']))
                self.tree_users.setItem(row, 1, QTableWidgetItem(user['position']))

    def get_user_names(self):
        users = self.load_users()
        if users is not None:
            return [f"{user['name']} ({user['position']})" for user in users]
        else:
            return []


if __name__ == "__main__":
    app = QApplication([])
    window = TaskManager()
    window.show()
    app.exec_()
