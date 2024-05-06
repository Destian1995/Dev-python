import os
import shutil

directory = 'путь к файлам'
file_list = []

# Рекурсивно обходит директорию и поддиректории
for root, dirs, files in os.walk(directory):
    for file in files:
        file_path = os.path.join(root, file)
        file_list.append((file_path, os.path.getmtime(file_path)))

# Сортирует файлы по дате изменения (от старых к новым)
file_list.sort(key=lambda x: x[1])

# Выбирает 100 самых старых файлов
oldest_files = file_list[:100]

# Архивирует выбранные файлы
for file_path, _ in oldest_files:
    shutil.make_archive(file_path, 'zip', os.path.dirname(file_path), os.path.basename(file_path))

print("Файлы успешно архивированы.")
