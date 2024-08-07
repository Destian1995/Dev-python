def load_file(file_path):
    with open(file_path, 'r', encoding='UTF-8') as f:
        file = f.readlines()
        file_new = file[1:]  # Пропускаем первую строку
        return file_new


def count_trades(file_new):
    total_sum = 0  # Переменная для хранения общей суммы

    for item in file_new:
        parts = item.strip().split(',')  # Убираем пробелы и разделяем по запятой
        if len(parts) > 4:  # Проверяем, что есть достаточно элементов
            try:
                total_sum += float(parts[4].strip())  # Используем float для работы с десятичными числами
            except ValueError:
                print(f"Ошибка преобразования значения: {parts[4]}")  # Обработка ошибок преобразования

    print(f"Общая сумма: {total_sum}")


def average_summ(file_new):
    dict_AA = {}
    dict_EE = {}
    count_AA = 0  # Счетчик для AA
    count_EE = 0  # Счетчик для EE

    for item in file_new:
        parts = item.strip().split(',')
        if len(parts) > 4:
            try:
                iter = parts[3].strip()
                value = float(parts[4].strip())  # Преобразуем значение в float
                if iter == 'AA':  # Используем == для точного сравнения
                    dict_AA[iter] = dict_AA.get(iter, 0) + value
                    count_AA += 1  # Увеличиваем счетчик для AA
                elif iter == 'EE':
                    dict_EE[iter] = dict_EE.get(iter, 0) + value
                    count_EE += 1  # Увеличиваем счетчик для EE
            except ValueError:
                print(f'Ошибка преобразования значения: {parts[4]}')

    aver_AA = dict_AA['AA'] / count_AA if count_AA > 0 else 0
    aver_EE = dict_EE['EE'] / count_EE if count_EE > 0 else 0

    print(f"Среднее для AA: {aver_AA}, Среднее для EE: {aver_EE}")


def average_5day(file_new):
    aver_day_AA = {}
    aver_day_EE = {}

    for item in file_new:
        parts = item.strip().split(",")
        if len(parts) > 4:
            day = parts[2].strip()  # Получаем день
            iter = parts[3].strip()  # Получаем тип (AA или EE)
            value = float(parts[4].strip())  # Получаем значение

            # Инициализация словарей для хранения сумм и счетчиков
            if day not in aver_day_AA:
                aver_day_AA[day] = {'sum': 0, 'count': 0}
            if day not in aver_day_EE:
                aver_day_EE[day] = {'sum': 0, 'count': 0}

            if iter == 'AA':
                aver_day_AA[day]['sum'] += value
                aver_day_AA[day]['count'] += 1
            elif iter == 'EE':
                aver_day_EE[day]['sum'] += value
                aver_day_EE[day]['count'] += 1

    # Вычисляем средние значения
    for day in aver_day_AA:
        if aver_day_AA[day]['count'] > 0:
            aver_day_AA[day]['average'] = aver_day_AA[day]['sum'] / aver_day_AA[day]['count']
        else:
            aver_day_AA[day]['average'] = 0

    for day in aver_day_EE:
        if aver_day_EE[day]['count'] > 0:
            aver_day_EE[day]['average'] = aver_day_EE[day]['sum'] / aver_day_EE[day]['count']
        else:
            aver_day_EE[day]['average'] = 0

    print("Средние значения по дням для AA:", {day: data['average'] for day, data in aver_day_AA.items()})
    print("Средние значения по дням для EE:", {day: data['average'] for day, data in aver_day_EE.items()})


if __name__ == '__main__':
    path = r'C:\Users\User\Desktop\test\data.txt'
    file_new = load_file(path)  # Сохраняем результат в переменной
    count_trades(file_new)  # Передаем переменную в функцию
    average_summ(file_new)  # Вызываем функцию для подсчета сумм
    average_5day(file_new)  # Вызываем функцию для подсчета среднего за день
