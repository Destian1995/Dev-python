import sys
import os
import json
import locale
from datetime import datetime
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QTextEdit, QPushButton, QListWidget, QFormLayout, QMessageBox, QComboBox, QCalendarWidget, QDialog, QCheckBox
from PyQt6.QtGui import QColor, QTextOption
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QFormLayout, QLineEdit, \
    QTextEdit, QPushButton, QListWidget, QComboBox, QCalendarWidget, QDialog, QCheckBox, QLabel, QSizePolicy, \
    QAbstractItemView, QListWidgetItem, QTextBrowser

ver = '1.0.1'

class TaskManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Управление задачами " + ver)
        self.setGeometry(500, 200, 900, 700)

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        self.selected_date = QDate.currentDate()

        self.create_directory_and_files()

        self.init_ui()

    def create_directory_and_files(self):
        if not os.path.exists("db_links"):
            os.mkdir("db_links")
        if not os.path.exists("db_links/users.json"):
            with open("db_links/users.json", "w") as user_file:
                json.dump([], user_file)
        if not os.path.exists("db_links/tasks.json"):
            with open("db_links/tasks.json", "w") as task_file:
                json.dump([], task_file)
        if not os.path.exists("db_links/reports.md"):
            with open("db_links/reports.md", "w") as report_file:
                report_file.write("Reports:\n\n")

    def init_ui(self):
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.tab_widget.addTab(self.tab1, "Управление задачами")
        self.tab_widget.addTab(self.tab2, "Исполнители")
        self.tab_widget.addTab(self.tab3, "Отчеты")

        self.init_task_tab()
        self.init_user_tab()
        self.init_report_tab()

    def init_task_tab(self):
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.task_entry = QTextEdit()  # Use QTextEdit instead of QLineEdit for task_entry
        self.priority_combobox = QComboBox()
        self.priority_combobox.addItems(["Низкий", "Средний", "Высокий"])
        self.user_combobox = QComboBox()
        self.load_users_to_combobox()
        self.task_list = QListWidget()

        task_entry_layout = QVBoxLayout()
        task_entry_layout.addWidget(self.task_entry)
        form_layout.addRow("Задача:", task_entry_layout)
        form_layout.addRow("Приоритет:", self.priority_combobox)
        form_layout.addRow("Назначить на исполнителя:", self.user_combobox)

        self.create_task_button = QPushButton("Создать задачу")
        self.create_task_button.clicked.connect(self.create_task)

        self.close_task_button = QPushButton("Закрыть задачу")
        self.close_task_button.clicked.connect(self.show_report_dialog)

        form_layout.addRow("Закрытие задачи (Заполнение отчета):", self.close_task_button)

        # Connect the "Сохранить" button in the CalendarDialog to the slot that hides the calendar
        self.calendar_button = QPushButton("Выбрать дату")
        self.calendar_dialog = CalendarDialog(self)
        self.calendar_button.clicked.connect(self.calendar_dialog.show)
        self.calendar_dialog.save_button.clicked.connect(self.calendar_dialog.hide)

        # Connect the signal from CalendarDialog to update the selected date
        self.calendar_dialog.calendar.clicked.connect(self.on_calendar_clicked)

        # Добавляем горизонтальный макет в форму
        form_layout.addRow("Время до закрытия:", self.calendar_button)

        layout.addLayout(form_layout)
        layout.addWidget(self.create_task_button)
        layout.addWidget(self.task_list)

        self.tab1.setLayout(layout)
        self.filter_user_combobox = QComboBox()
        self.filter_user_combobox.addItem("Все текущие задачи")
        self.filter_user_combobox.addItems(self.user_combobox.itemText(i) for i in range(self.user_combobox.count()))
        self.filter_user_combobox.currentIndexChanged.connect(self.load_tasks)
        form_layout.addRow("Отобразить задачи для исполнителя:", self.filter_user_combobox)

        # Загрузка задач из файла
        self.load_tasks()

    def init_user_tab(self):
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.user_name_entry = QLineEdit()
        self.position_entry = QLineEdit()
        self.department_entry = QLineEdit()
        self.user_list = QListWidget()

        form_layout.addRow("ФИО:", self.user_name_entry)
        form_layout.addRow("Должность:", self.position_entry)
        form_layout.addRow("Отдел:", self.department_entry)

        self.create_user_button = QPushButton("Создать исполнителя")
        self.create_user_button.clicked.connect(self.create_user)

        self.delete_user_button = QPushButton("Удалить исполнителя")
        self.delete_user_button.clicked.connect(self.delete_user)

        layout.addLayout(form_layout)
        layout.addWidget(self.create_user_button)
        layout.addWidget(self.delete_user_button)
        layout.addWidget(self.user_list)

        self.tab2.setLayout(layout)

        # Загрузка пользователей из файла
        self.load_users()

    def init_report_tab(self):
        layout = QVBoxLayout()

        # Add a search input and checkbox
        search_layout = QHBoxLayout()
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText("Поиск по задачам")
        self.search_entry.textChanged.connect(self.filter_reports)
        self.search_checkbox = QCheckBox("Поиск информации в отчетах(поставьте галочку)")
        self.search_checkbox.stateChanged.connect(self.filter_reports)
        search_layout.addWidget(self.search_entry)
        search_layout.addWidget(self.search_checkbox)
        layout.addLayout(search_layout)

        self.reports_text = QTextEdit()
        self.load_reports()
        layout.addWidget(self.reports_text)

        self.tab3.setLayout(layout)

        # Загрузка отчетов из файла
        self.load_reports()

    def filter_reports(self):
        search_text = self.search_entry.text().lower()
        search_in_reports = self.search_checkbox.isChecked()

        with open("db_links/reports.md", "r") as report_file:
            all_reports = report_file.read()

        if not search_text or not search_in_reports:
            self.reports_text.setPlainText(all_reports)
            return

        filtered_reports = ""
        for report in all_reports.split("\n\n"):
            if search_text in report.lower():
                filtered_reports += report + "\n\n"

        self.reports_text.setPlainText(filtered_reports)

    def on_calendar_clicked(self, date):
        pass

    def create_task(self):
        task_name = self.task_entry.toPlainText()
        priority = self.priority_combobox.currentText()
        assign_to = self.user_combobox.currentText()

        # Use the selected date from the calendar_dialog instance
        due_date = self.calendar_dialog.selected_date.toString("dd.MM.yyyy")

        if task_name and priority and assign_to:
            task_data = {
                "task_name": task_name,
                "priority": priority,
                "assign_to": assign_to,
                "due_date": due_date.split()
            }
            with open("db_links/tasks.json", "r") as task_file:
                tasks = json.load(task_file)
            tasks.append(task_data)
            with open("db_links/tasks.json", "w") as task_file:
                json.dump(tasks, task_file, indent=4)

            self.task_list.clear()
            self.clear_task_entries()
            self.load_tasks()
        else:
            self.show_message("Внимание", "Заполните все обязательные поля!")

    def close_task(self):
        selected_task = self.task_list.currentItem()
        if selected_task:
            self.show_report_dialog()  # Показываем диалог для ввода отчета
        else:
            self.show_message("Внимание", "Выберите задачу!")

    def show_report_dialog(self):
        selected_task_index = self.task_list.currentRow()
        if selected_task_index >= 0:
            selected_task = self.task_list.item(selected_task_index).text()
            dialog = QTextEditDialog(self)
            result = dialog.exec()
            if result == QDialog.DialogCode.Accepted:
                close_report = dialog.get_text()
                if close_report:
                    now = datetime.now().strftime("%d.%m.%Y %H:%M")

                    # Get the assigned user from the task data
                    with open("db_links/tasks.json", "r") as task_file:
                        tasks = json.load(task_file)
                    assigned_user = tasks[selected_task_index].get("assign_to", "")

                    report_text = f"Исполнитель: {assigned_user}\n"
                    report_text += f"Задача: {selected_task}\n"
                    report_text += f"Время закрытия: {now}\nОтчет:\n{close_report}\n\n"

                    with open("db_links/reports.md", "a") as report_file:
                        report_file.write(report_text)

                    # Remove the completed task from tasks.json
                    del tasks[selected_task_index]
                    with open("db_links/tasks.json", "w") as task_file:
                        json.dump(tasks, task_file, indent=4)

                    self.clear_close_report_entry()
                    self.load_reports()
                    self.load_tasks()  # Reload tasks in the UI
                else:
                    self.show_message("Внимание", "Введите отчет!")
            else:
                self.show_message("Внимание", "Выберите задачу!")

    def clear_close_report_entry(self):
        pass  # Ничего не делаем, так как очистка не требуется


    def create_user(self):
        full_name = self.user_name_entry.text()
        position = self.position_entry.text()
        department = self.department_entry.text()

        if full_name and position and department:
            user_data = {
                "full_name": full_name,
                "position": position,
                "department": department,
                "tasks": []
            }
            with open("db_links/users.json", "r") as user_file:
                users = json.load(user_file)
            users.append(user_data)
            with open("db_links/users.json", "w") as user_file:
                json.dump(users, user_file, indent=4)
            self.user_list.addItem(full_name)
            self.user_combobox.addItem(full_name)
            self.clear_user_entries()
        else:
            self.show_message("Внимание", "Заполните все обязательные поля!")
        self.load_users()

    def delete_user(self):
        selected_user_index = self.user_list.currentRow()
        if selected_user_index >= 0:
            selected_user = self.user_list.item(selected_user_index).text()

            with open("db_links/users.json", "r") as user_file:
                users = json.load(user_file)

            # Find the user in the list
            for user in users:
                full_info = f"{user['full_name']} ({user['position']}, {user['department']})"
                if full_info == selected_user:
                    # Remove the user from the list
                    users.remove(user)

            # Update the users.json file
            with open("db_links/users.json", "w") as user_file:
                json.dump(users, user_file, indent=4)

            # Clear and reload users into the dropdown menu
            self.user_combobox.clear()
            self.load_users_to_combobox()

            self.user_combobox.removeItem(self.user_combobox.findText(selected_user))
            self.user_list.takeItem(selected_user_index)
        self.load_users()

    def clear_task_entries(self):
        self.task_entry.clear()
        self.priority_combobox.setCurrentIndex(0)
        self.user_combobox.setCurrentIndex(0)

        # Access the calendar through the calendar_dialog instance
        self.calendar_dialog.calendar.setSelectedDate(QDate.currentDate())

    def clear_user_entries(self):
        self.user_name_entry.clear()
        self.position_entry.clear()
        self.department_entry.clear()

    def load_reports(self):
        with open("db_links/reports.md", "r") as report_file:
            reports = report_file.read()
        self.reports_text.setPlainText(reports)

    def load_users_to_combobox(self):
        with open("db_links/users.json", "r") as user_file:
            users = json.load(user_file)
        for user in users:
            self.user_combobox.addItem(user["full_name"])

    def load_users(self):
        # Clear the existing items from the user list
        self.user_list.clear()

        with open("db_links/users.json", "r") as user_file:
            users = json.load(user_file)
        for user in users:
            full_info = f"{user['full_name']} ({user['position']}, {user['department']})"
            self.user_list.addItem(full_info)

    def load_tasks(self):
        with open("db_links/tasks.json", "r") as task_file:
            tasks = json.load(task_file)

        selected_user_index = self.filter_user_combobox.currentIndex()
        selected_user = self.filter_user_combobox.currentText()

        self.task_list.clear()  # Clear the existing items

        today = QDate.currentDate()

        # Sort tasks by due date and priority
        tasks.sort(key=lambda x: (self.get_due_date(x), x.get("priority", "")))

        for task in tasks:
            if selected_user_index == 0 or task.get("assign_to") == selected_user:
                due_date = self.get_due_date(task)

                task_text = f"{task['task_name']} - Исполнитель: {task['assign_to']} - Дедлайн: {due_date.toString('dd.MM.yyyy')} - Приоритет: {task.get('priority', 'Н/Д')}"

                # Check if the due date is today and set light blue color
                if due_date == today:
                    item = QListWidgetItem(task_text)
                    item.setForeground(QColor(173, 216, 230))  # Light Blue color
                    self.task_list.addItem(item)
                else:
                    self.task_list.addItem(task_text)

        self.task_list.setStyleSheet("QListWidget::item { border-bottom: 1px solid white; }")

    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()

    def remove_completed_task_from_ui(self, selected_task_index):
        self.task_list.takeItem(selected_task_index)

    def get_due_date(self, task):
        due_date_str = task.get("due_date", "")

        # Check if due_date_str is a list, convert it to a string
        if isinstance(due_date_str, list):
            due_date_str = ".".join(map(str, due_date_str))

        return QDate.fromString(due_date_str, "dd.MM.yyyy")
class CalendarDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выберите дату")
        self.selected_date = QDate.currentDate()  # Add this line to initialize the selected date

        layout = QVBoxLayout()

        self.calendar = QCalendarWidget()
        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_date)

        layout.addWidget(self.calendar)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

    def save_date(self):
        # Update the selected date attribute when the "Сохранить" button is clicked
        self.selected_date = self.calendar.selectedDate()
        self.accept()  # Accept the QDialog to indicate that the user has finished interaction

    def on_calendar_clicked(self, date):
        self.selected_date = date
        self.calendar.hide()


class QTextEditDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Введите отчет")

        layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.save_button = QPushButton("Сохранить отчет")
        self.save_button.clicked.connect(self.accept)

        layout.addWidget(self.text_edit)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

    def get_text(self):
        return self.text_edit.toPlainText()

    def on_calendar_clicked(self, date):
        pass

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget {
            background-color: #333; /* Цвет фона */
            color: white; /* Цвет текста */
        }

        QPushButton {
            background-color: #6FB3D2; /* Светло-синий цвет кнопок */
            color: white;
            border: none;
            padding: 10px 20px;
        }

        QTabWidget::pane {
            border: 1px solid white;
        }

        QTabWidget::tab-bar {
            alignment: center;
        }

        QTabBar::tab {
            background-color: #444; /* Цвет закладок */
            color: white;
            padding: 5px 20px;
        }

        QTabBar::tab:selected {
            background-color: #6FB3D2; /* Цвет активной закладки */
            color: white;
        }

        QLineEdit {
            background-color: #444;
            color: white;
        }

        QComboBox {
            background-color: #444;
            color: white;
        }

        QTextEdit {
            background-color: #444;
            color: white;
        }

        QCalendarWidget {
            background-color: #444;
            color: white;
        }

        QListWidget {
            background-color: #444;
            color: white;
        }
    """)
    window = TaskManagerApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
