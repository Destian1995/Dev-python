import os
import shutil

# ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ
print('Бэкап релиза. версия 1.7.14')
print('_____________________________________________________________________________________')
print('Обратите внимание бэкап должен проводится ДО КОПИРОВАНИЯ ПАПКИ РЕЛИЗА в каталог Temp')
print('_____________________________________________________________________________________')
start = input('Копирование происходит ДО КОПИРОВАНИЯ ПАПКИ РЕЛИЗА? Если да нажмите Enter для продолжения, если нет закрой скрипт')
print('_____________________________________________________________________________________')
path = "R:/"
dst_path = 'Rollback'
destination = os.path.join(dst_path, r'05_SRF')
filetype = 'siebel_sia_fins_enu.srf'

print("Поиск и копирование SRF файла...")
def search_folder(path):
    list_of_files = []
    for root, directories, files in os.walk(path):
        for filename in files:
            if filename.endswith(filetype):
                list_of_files.append(os.path.join(root, filename))
    if not list_of_files:
        print(f"Файл не найден {filetype} здесь {path}.")
        return None

    latest_file = max(list_of_files, key=os.path.getmtime)
    return latest_file


latest_file = search_folder(path)
if not latest_file:
    print("Файл не найден.")
else:
    if not os.path.exists(destination):
        os.makedirs(destination)
    shutil.copy2(latest_file, os.path.join(destination, os.path.basename(latest_file))) # копирование файла в указанную директорию, сохраняя имя и метаданные
    print('SRF файл добавлен в бэкап по пути: ' + destination)

print('Копирование актуальных каталогов из последних релизов')

if not os.path.exists(dst_path):
    os.makedirs(dst_path)
    print(f"Каталог {dst_path} создан.")

# Получаем список всех каталогов с похожим именем в текущей директории и ее подкаталогах, исключая путь, указанный пользователем в dst_path
def copy_latest_directory(search_name: str, dst_path: str):
    latest_dir = None
    latest_time = 0
    for root, dirs, files in os.walk("."):
        rel_path = os.path.relpath(root, dst_path)
        if search_name in rel_path.split(os.path.sep):
            continue
        for d in dirs:
            if d.startswith(search_name):
                d_time = os.path.getctime(os.path.join(root, d))
                if d_time > latest_time:
                    latest_dir = os.path.join(root, d)
                    latest_time = d_time
    if not latest_dir:
        print(f"Нет каталогов с именем, начинающимся на {search_name}, для копирования.")
        return
    src_path = os.path.abspath(latest_dir)
    dst_path = os.path.abspath(dst_path)
    shutil.copytree(src_path, os.path.join(dst_path, os.path.basename(latest_dir)))
    print(f"Каталог {latest_dir} скопирован в {dst_path}.")
search_name = '06_KM'
copy_latest_directory(search_name, dst_path)

def copy_latest_directory_07(search_name: str, dst_path: str):
    latest_dir = None
    latest_time = 0
    for root, dirs, files in os.walk("."):
        rel_path = os.path.relpath(root, dst_path)
        if search_name in rel_path.split(os.path.sep):
            continue
        for d in dirs:
            if d.startswith(search_name):
                d_time = os.path.getctime(os.path.join(root, d))
                if d_time > latest_time:
                    latest_dir = os.path.join(root, d)
                    latest_time = d_time
    if not latest_dir:
        print(f"Нет каталогов с именем, начинающимся на {search_name}, для копирования.")
        return
    src_path = os.path.abspath(latest_dir)
    dst_path = os.path.abspath(dst_path)
    shutil.copytree(src_path, os.path.join(dst_path, os.path.basename(latest_dir)))
    print(f"Каталог {latest_dir} скопирован в {dst_path}.")
search_name = '07_SiebelServer'
copy_latest_directory_07(search_name, dst_path)

def copy_latest_directory_03(search_name: str, dst_path: str):
    latest_dir = None
    latest_time = 0
    for root, dirs, files in os.walk("."):
        rel_path = os.path.relpath(root, dst_path)
        if search_name in rel_path.split(os.path.sep):
            continue
        for d in dirs:
            if d.startswith(search_name):
                d_time = os.path.getctime(os.path.join(root, d))
                if d_time > latest_time:
                    latest_dir = os.path.join(root, d)
                    latest_time = d_time
    if not latest_dir:
        print(f"Нет каталогов с именем, начинающимся на {search_name}, для копирования.")
        return
    src_path = os.path.abspath(latest_dir)
    dst_path = os.path.abspath(dst_path)
    shutil.copytree(src_path, os.path.join(dst_path, os.path.basename(latest_dir)))
    print(f"Каталог {latest_dir} скопирован в {dst_path}.")
search_name = '03_SCHEMA'
copy_latest_directory_03(search_name, dst_path)

response = os.system("ping -n 1 web-siebel001.open.ru")
target_path = r'Rollback\08_SiebelSWE\siebelswe\eappweb\PUBLIC'
if response == 0:
    print('Веб-сервер web-siebel001.open.ru доступен, запущено копирование')
    source_path = r'\\web-siebel001.open.ru\r$\sba81\eappweb\PUBLIC'
    shutil.copytree(source_path, target_path)
    print(f'Каталог PUBLIC скопирован в {target_path}.')
else:
    # Check if web-siebel002.open.ru is reachable
    response = os.system("ping -n 1 web-siebel002.open.ru")
    if response == 0:
        print('Веб-сервер web-siebel001.open.ru не доступен, подключаюсь к web-siebel002.open.ru, запущено копирование')
        source_path = r'\\web-siebel002.open.ru\r$\sba81\eappweb\PUBLIC'
        shutil.copytree(source_path, target_path)
        print(f'Каталог PUBLIC скопирован в {target_path}.')
    else:
        print("Веб сервера не доступны, проверьте их работоспособность, каталог PUBLIC нужно сформировать вручную")
        exit()


