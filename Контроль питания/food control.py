import sys
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QListWidget,
    QMessageBox,
    QFormLayout, QTableWidgetItem, QTableWidget, QDialog
)
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class DietTrackerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Версия 1.01")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.title_label = QLabel("<h2 style='color: #333333;'>Контроль питания</h2>")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        self.meal_label = QLabel("<h3 style='color: #333333;'>Блюдо:</h3>")
        self.meal_entry = QLineEdit()
        self.form_layout.addRow(self.meal_label, self.meal_entry)

        self.category_label = QLabel("<h3 style='color: #333333;'>Категория:</h3>")
        self.category_combobox = QComboBox()
        self.category_combobox.addItems(["Завтрак", "Обед", "Ужин", "Перекус"])
        self.form_layout.addRow(self.category_label, self.category_combobox)

        self.quantity_label = QLabel("<h3 style='color: #333333;'>Количество (г):</h3>")
        self.quantity_entry = QLineEdit()
        self.form_layout.addRow(self.quantity_label, self.quantity_entry)

        self.calories_label = QLabel("<h3 style='color: #333333;'>Количество калорий (ккал/100г):</h3>")
        self.calories_entry = QLineEdit()
        self.form_layout.addRow(self.calories_label, self.calories_entry)

        self.show_calories_button = QPushButton("Показать таблицу калорийности")
        self.show_calories_button.clicked.connect(self.show_calories_table)
        self.show_calories_button.setStyleSheet(
            "background-color: #008CBA; color: white; border: none; padding: 10px 20px; text-align: center; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 5px;")
        self.layout.addWidget(self.show_calories_button)


        self.add_button = QPushButton("Добавить блюдо")
        self.add_button.clicked.connect(self.add_meal)
        self.add_button.setStyleSheet(
            "background-color: #4CAF50; color: white; border: none; padding: 10px 20px; text-align: center; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 5px;")
        self.layout.addWidget(self.add_button)

        self.meals_listbox = QListWidget()
        self.layout.addWidget(self.meals_listbox)

        self.plot_button = QPushButton("Показать график")
        self.plot_button.clicked.connect(self.show_plot)
        self.plot_button.setStyleSheet(
            "background-color: #008CBA; color: white; border: none; padding: 10px 20px; text-align: center; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 5px;")
        self.layout.addWidget(self.plot_button)

        self.timer_label = QLabel("<h3 style='color: #333333;'>Время до следующего приема пищи: </h3>")
        self.layout.addWidget(self.timer_label)

        self.interval_label = QLabel("<h3 style='color: #333333;'>Интервал между приемами пищи (в минутах):</h3>")
        self.layout.addWidget(self.interval_label)

        self.interval_entry = QLineEdit()
        self.layout.addWidget(self.interval_entry)

        self.set_interval_button = QPushButton("Установить интервал")
        self.set_interval_button.clicked.connect(self.set_interval)
        self.set_interval_button.setStyleSheet(
            "background-color: #008CBA; color: white; border: none; padding: 10px 20px; text-align: center; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 5px;")
        self.layout.addWidget(self.set_interval_button)

        self.last_meal_label = QLabel("<h3 style='color: #333333;'>Время последнего приема пищи:</h3>")
        self.layout.addWidget(self.last_meal_label)

        self.last_meal_time_entry = QLineEdit()
        self.layout.addWidget(self.last_meal_time_entry)

        self.set_current_time_button = QPushButton("Установить текущее время")
        self.set_current_time_button.clicked.connect(self.set_current_time)
        self.set_current_time_button.setStyleSheet(
            "background-color: #008CBA; color: white; border: none; padding: 10px 20px; text-align: center; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 5px;")
        self.layout.addWidget(self.set_current_time_button)

        self.meals = []

        # Инициализация таймера
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        # Установка интервала между приемами пищи (в секундах)
        self.interval_seconds = 3600  # 1 час по умолчанию

        # Запуск таймера
        self.timer.start(1000)  # обновление таймера каждую секунду



    def show_calories_table(self):
        # Создаем новое окно для отображения таблицы калорийности
        calories_window = QDialog(self)
        calories_window.setWindowTitle("Таблица калорийности")
        calories_window.resize(600, 400)  # Установка размеров окна

        calories_layout = QVBoxLayout(calories_window)

        # Добавляем строку поиска
        search_layout = QHBoxLayout()
        search_label = QLabel("Поиск:")
        search_layout.addWidget(search_label)
        self.search_entry = QLineEdit()
        self.search_entry.textChanged.connect(self.search_calories)
        search_layout.addWidget(self.search_entry)
        calories_layout.addLayout(search_layout)

        # Создаем таблицу калорийности
        self.calories_table = QTableWidget()
        self.calories_table.horizontalHeader().setStretchLastSection(True)  # Растягиваем последнюю секцию на всю ширину
        calories_layout.addWidget(self.calories_table)

        # Обновляем данные в таблице
        self.populate_calories_table()

        # Показываем окно
        calories_window.exec_()

    def search_calories(self):
        search_text = self.search_entry.text().lower()
        for row in range(self.calories_table.rowCount()):
            item = self.calories_table.item(row, 0)
            if search_text in item.text().lower():
                self.calories_table.setRowHidden(row, False)
            else:
                self.calories_table.setRowHidden(row, True)

    def populate_calories_table(self):
        # Очищаем таблицу перед обновлением данных
        self.calories_table.clear()

        # Устанавливаем количество строк и столбцов
        self.calories_table.setRowCount(0)
        self.calories_table.setColumnCount(2)

        # Устанавливаем заголовки столбцов
        self.calories_table.setHorizontalHeaderLabels(["Продукт", "Калорийность (ккал/100г)"])

        # Данные о калорийности овощей, фруктов и молочной продукции
        vegetables = {
            "Помидор": 18,
            "Огурец": 15,
            "Морковь": 41,
            "Картошка(вареная)": 80,
            "Кабачки": 30,
            "Капуста белокочанная": 31,
            # Другие виды овощей и их калорийность
        }

        fruits = {
            "Яблоко": 48,
            "Груша": 41,
            "Банан": 87,
            "Апельсин": 38,
            "Мандарин": 39,
            "Киви": 46,
            "Лимон": 30,
            "Хурма": 61,
            "Персики": 42,
            "Ананас": 49,
            # Другие виды фруктов и их калорийность
        }

        dairy_products = {
            "Молоко(0%)": 34,
            "Молоко(1%)": 43,
            "Молоко(2,5%)": 53,
            "Молоко(3,2%)": 58,
            "Молоко сухое цельное": 477,
            "Молоко сгущенное": 139,
            "Кефир(0%)": 29,
            "Кефир(1%)": 37,
            "Кефир(2,5%)": 51,
            "Кефир(3,2%)": 57,
            "Сметана(10%)": 118,
            "Сметана(15%)": 163,
            "Сметана(20%)": 208,
            "Творог Жирный": 236,
            "Творог нежирный": 89,
            "Творог полужирный": 156,
            "Йогурт(1,5%)": 65,
            "Йогурт(3,2%)": 87,
            "Сыр российский": 366,
            # Другие виды молочной продукции и их калорийность
        }

        berries = {
            "Черешня": 54,
            "Клубника": 30,
            "Виноград": 73,
            "Ежевика": 31,
            "Земляника": 40,
            "Малина": 43,
            "Смородина черная": 38,

        }

        nuts = {
            "Арахис": 555,
            "Фисташки": 555,
            "Грецкий орех": 662,
            "Фундук": 701,
        }

        bakery_products = {
            "Хлеб пшеничный": 246,
            "Хлеб ржаной": 210,
            "Сухари пшеничные": 327,
            "Батон нарезной": 261,
            "Булка": 218,
        }

        cereals = {
            "Перловая крупа": 315,
            "Манная крупа": 333,
            "Гречневая крупа": 350,
            "Рис белый длиннозерный": 365,
        }

        eggs ={
            "Куриное яйцо": 153,
            "Омлет": 181,
        }

        meat = {
            "Свинина": 484,
            "Говядина": 191,
            "Телятина": 91,
            "Баранина": 201,

        }
        bird = {
            "Курица": 161,
            "Индейка": 192,
        }

        # Заполняем таблицу данными
        current_row = 0
        for category, foods in {"Овощи": vegetables, "Фрукты": fruits, "Молочная продукция": dairy_products, "Ягоды": berries, "Орехи": nuts, "Хлебобулочные изделия": bakery_products, "Крупы": cereals, "Яйца": eggs, "Мясо": meat, "Птица": bird}.items():
            self.calories_table.insertRow(current_row)
            category_item = QTableWidgetItem(category)
            category_item.setBackground(Qt.gray)
            self.calories_table.setItem(current_row, 0, category_item)
            self.calories_table.setSpan(current_row, 0, 1, 2)  # Объединяем ячейки для названия категории
            current_row += 1

            for food, calories in foods.items():
                self.calories_table.insertRow(current_row)
                self.calories_table.setItem(current_row, 0, QTableWidgetItem(food))
                self.calories_table.setItem(current_row, 1, QTableWidgetItem(str(calories)))
                current_row += 1

    def add_meal(self):
        meal = self.meal_entry.text()
        category = self.category_combobox.currentText()
        quantity = self.quantity_entry.text()
        calories_per_100g = self.calories_entry.text()
        if meal and category and quantity and calories_per_100g:
            try:
                quantity = float(quantity)
                calories_per_100g = float(calories_per_100g)
            except ValueError:
                QMessageBox.warning(self, "Предупреждение", "Введите корректные значения.")
                return
            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            total_calories = (quantity / 100) * calories_per_100g
            self.meals.append({"timestamp": timestamp, "meal": meal, "category": category, "quantity": quantity,
                               "calories": total_calories})
            self.meals_listbox.addItem(f"{timestamp}: {meal} ({category}) - {total_calories} ккал")
            self.meal_entry.clear()
            self.quantity_entry.clear()
            self.calories_entry.clear()
        else:
            QMessageBox.warning(self, "Предупреждение", "Введите все данные.")

    def show_plot(self):
        categories = ["Завтрак", "Обед", "Ужин", "Перекус"]
        category_calories = {category: 0 for category in categories}
        for meal in self.meals:
            category_calories[meal["category"]] += meal["calories"]

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.bar(category_calories.keys(), category_calories.values(), color='#4CAF50')

        ax.set_xlabel("Категория блюда", fontsize=12)
        ax.set_ylabel("Количество потребленных калорий", fontsize=12)
        ax.set_title("Статистика потребления калорий по категориям", fontsize=14)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)

        plt.show()

    def update_timer(self):
        current_time = QDateTime.currentDateTime()
        last_meal_time = QDateTime.fromString(self.last_meal_time_entry.text(), "yyyy-MM-dd HH:mm:ss")
        next_meal_time = last_meal_time.addSecs(self.interval_seconds)
        time_diff = current_time.secsTo(next_meal_time)
        hours = time_diff // 3600
        minutes = (time_diff % 3600) // 60
        seconds = time_diff % 60
        self.timer_label.setText(
            f"<h3 style='color: #333333;'>Время до следующего приема пищи: {hours:02}:{minutes:02}:{seconds:02}</h3>")

    def set_interval(self):
        try:
            interval_minutes = int(self.interval_entry.text())
            self.interval_seconds = interval_minutes * 60  # переводим в секунды
        except ValueError:
            QMessageBox.warning(self, "Предупреждение", "Введите корректное значение интервала в минутах.")

    def set_current_time(self):
        current_time = QDateTime.currentDateTime()
        self.last_meal_time_entry.setText(current_time.toString("yyyy-MM-dd HH:mm:ss"))


def main():
    app = QApplication(sys.argv)
    window = DietTrackerApp()
    window.setGeometry(600, 200, 600, 500)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
