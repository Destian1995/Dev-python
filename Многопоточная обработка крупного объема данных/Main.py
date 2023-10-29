import os
import time
import datetime
import threading
import csv

ver = '2.0.1'
print('Сбор данных запущен в режиме многопоточности', 'версия - ', ver)
print('Время запуска', time.strftime("%H:%M:%S"))

def find_files_with_name(directory, keyword):
    while True:
        try:
            result = []
            for root, _, files in os.walk(directory):
                for filename in files:
                    if keyword in filename:
                        file_path = os.path.join(root, filename)
                        file_stat = os.stat(file_path)
                        mod_time = datetime.datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                        result.append([filename, file_path, mod_time])

            # Создаем уникальное имя файла на основе директории
            output_file = f'{directory.split(os.sep)[-1]}.csv'

            with open(output_file, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=';')
                csv_writer.writerows(result)

            break  # Если все успешно, выходим из цикла

        except Exception as e:
            print(f"Error in {directory}: {e}")
            print('Перезагрузка потока...')
            time.sleep(1)  

# Создаем список директорий и ключевых слов
directories_and_keywords = [
    (r'\\open.ru\files\Commons\SBLfilesystem\sfs\sfs02', 'S_ASSET_ATT'),
    (r'R:\sfs\sfs', 'S_ASSET_ATT'),
    (r'R:\sfs\sfs01', 'S_ASSET_ATT'),
    (r'R:\sfs\sfs03', 'S_ASSET_ATT'),
    (r'\\open.ru\files\Commons\SBLfilesystem\sfs\sfs04', 'S_ASSET_ATT'),
    (r'R:\sfs\sfs05', 'S_ASSET_ATT'),
    (r'\\open.ru\files\Commons\SBLfilesystem\sfs\sfs06', 'S_ASSET_ATT'),
    (r'R:\sfs\sfs07', 'S_ASSET_ATT'),
    (r'\\open.ru\files\Commons\SBLfilesystem\sfs\sfs08', 'S_ASSET_ATT'),
    (r'R:\sfs\sfs09', 'S_ASSET_ATT'),
    (r'\\open.ru\files\Commons\SBLfilesystem\sfs\sfs10', 'S_ASSET_ATT'),
    (r'R:\sfs\sfs11', 'S_ASSET_ATT'),
    (r'\\open.ru\files\Commons\SBLfilesystem\sfs\sfs12', 'S_ASSET_ATT'),
    (r'R:\sfs\sfs13', 'S_ASSET_ATT'),
    (r'R:\sfs\sfs14', 'S_ASSET_ATT'),
    (r'R:\sfs\sfs15', 'S_ASSET_ATT'),
]
# Запускаем потоки для обработки каждой директории и ключевого слова
threads = []
for directory, keyword in directories_and_keywords:
    thread = threading.Thread(target=find_files_with_name, args=(directory, keyword))
    threads.append(thread)
    thread.start()

# Ожидаем завершения всех потоков
for thread in threads:
    thread.join()

print('Данные успешно сохранены в файлы')

# Функция для считывания данных из файлов и записи их в Export_db.csv
def export_to_csv(output_file):
    with open(output_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')
        for directory, _ in directories_and_keywords:
            input_file = f'{directory.split(os.sep)[-1]}.csv'
            with open(input_file, 'r') as input_csv:
                csv_reader = csv.reader(input_csv, delimiter=';')
                csv_writer.writerows(csv_reader)

            # Удаляем временные файлы
            os.remove(input_file)

# Вызываем функцию для экспорта данных в Export_db.csv
export_to_csv('Export_to_db.csv')

print('Данные успешно экспортированы в Export_db.csv')
