"""
Программа считывает данные из CSV-файла, 
содержащего информацию о продажах (дата, товар, количество, цена).
Рассчитывает общую сумму продаж.
Определяет самый продаваемый товар.
Находит средний чек по каждому товару.
Выводит результаты анализа в удобном для чтения формате.
"""
import csv


def read_data_files(path_file):
    """
    :param path_file: Путь к файлу откуда берем данные
    :return: Возвращаем содержимое файла минус заголовок
    """
    with open(path_file, 'r', encoding='UTF-8-sig') as file:
        reader = csv.reader(file, delimiter=';')
        result_data = []
        for row in reader:
            cleaned_row = [item.strip() for item in row if item.strip()]
            if cleaned_row:
                result_data.append(cleaned_row)
    return result_data[1:]  # Возвращаем данные, пропуская заголовок


def count_data_files(file):
    """
    :param file: Получаем содержимое файла из функции read_data_files
    :return: Возвращаем маскимальный доход(сумма последней графы), лучший товар по количеству проданного, и средняя стоимость товара.
    """
    brilliant_product = []

    # Словарь для хранения итогов по категориям
    totals = {
        'тетрадки': 0,
        'пеналы': 0,
        'ручки': 0,
        'фломастеры': 0,
        'учебники': 0
    }

    # Словарь для хранения цен по категориям для расчета средней цены
    averages = {key: [] for key in totals.keys()}

    for item in file:
        price = item[3].replace(" руб", "").strip()  # Убираем " руб" и пробелы
        category = item[1].strip()  # Убираем пробелы

        # Добавляем цену в соответствующую категорию
        if category in totals:
            totals[category] += float(price)
            averages[category].append(float(price))

    # Вычисляем средние цены
    average_prices = {key: (sum(values) / len(values) if values else 0) for key, values in averages.items()}

    # Определяем "лучший" продукт
    sorted_totals = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    if sorted_totals:
        max_value = sorted_totals[0][1]
        brilliant_product = [name for name, total in sorted_totals if total == max_value]

    # Суммируем все продажи
    summ_tax = sum(totals.values())

    return summ_tax, brilliant_product[0], average_prices


def result_file(result, result_path):
    """
    :param result: Получаем маскимальный доход(сумма последней графы), лучший товар по количеству проданного, и средняя стоимость товара.
    :param result_path: Путь куда будем сохранять полученные значения
    :return: Результат файл с 3 графами в каждую из которых записана полученная информация из count_data_files
    """
    with open(result_path, 'w', encoding='UTF-8-sig') as file:
        r_file = csv.writer(file, delimiter=';')
        r_file.writerow(['Общий доход', 'Самая продаваемая категория', 'Средняя цена на каждый товар'])  # Заголовки
        r_file.writerow(result)


if __name__ == '__main__':
    path = r'C:\Users\User\Desktop\test\sales.csv' # Откуда берем данные
    result_path = r'C:\Users\User\Desktop\test\result_sales.csv' # Куда сохраняем
    file = read_data_files(path)
    slovar_data = count_data_files(file)
    result_file(slovar_data, result_path)
