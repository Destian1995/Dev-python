import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO
from telegram import Bot
import asyncio
import os
import re
import schedule

def connect_site(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    return driver

def parametr_files(path):
    with open(path, 'r', encoding='UTF-8') as file:
        result_parametr = file.readlines()
        url = result_parametr[0].strip()
        print(url)
        select = result_parametr[1].strip()
        print(select)
    querry_search = ''.join([url, select])
    print(querry_search)
    return connect_site(querry_search)

def clear_folder(folder):
    """Очистка каталога перед загрузкой изображений."""
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Удален файл: {file_path}")
            except Exception as e:
                print(f"Не удалось удалить файл {file_path}. Ошибка: {e}")
    else:
        os.makedirs(folder)  # Создать папку, если она не существует

def parsing_site(driver, save_folder):
    image_elements = driver.find_elements(By.XPATH, '//img')
    print(f"Найдено {len(image_elements)} изображений")

    for img in image_elements:
        img_url = img.get_attribute('src') or img.get_attribute('data-src') or img.get_attribute('srcset')
        if img_url:
            download_image(img_url, save_folder)

def download_image(url, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = url.split('/')[-1]
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = os.path.splitext(filename)[0] + '.jpg'  # Убедитесь, что имя файла имеет расширение .jpg
    filepath = os.path.join(folder, filename)

    response = requests.get(url)
    if response.status_code == 200 and 'image' in response.headers.get('Content-Type', ''):
        try:
            image = Image.open(BytesIO(response.content))
            # Проверка формата изображения
            if image.format not in ['JPEG', 'JPG']:
                print(f"Пропуск изображения {url} - не JPG или JPEG")
                return
            image = image.convert('RGB')
            image.save(filepath, 'JPEG')
            print(f"Сохранено: {filepath}")
        except Exception as e:
            print(f"Не удалось сохранить изображение: {url}. Ошибка: {e}")
    else:
        print(f"Не удалось скачать изображение: {url} (не изображение или ошибка загрузки)")

async def send_image_to_telegram(token, chat_id, image_path):
    bot = Bot(token=token)
    with open(image_path, 'rb') as image_file:
        await bot.send_photo(chat_id=chat_id, photo=image_file)

async def publish_images_on_schedule(token, chat_id, images, times):
    for time_str in times:
        schedule.every().day.at(time_str).do(lambda: asyncio.create_task(send_images(token, chat_id, images)))

    while images:
        schedule.run_pending()
        await asyncio.sleep(60)  # Проверка каждые 60 секунд на выполнение задач

async def send_images(token, chat_id, images):
    if not images:
        return
    image_path = images.pop(0)
    await send_image_to_telegram(token, chat_id, image_path)
    print(f"Изображение {image_path} отправлено")

async def main():
    path = r'C:\Users\lerdo\Desktop\parametr_bots\parameters.txt'
    save_folder = r'C:\Users\lerdo\Desktop\parametr_bots\downloaded_images'
    
    # Очистка каталога перед загрузкой изображений
    clear_folder(save_folder)

    driver = parametr_files(path)
    parsing_site(driver, save_folder)
    driver.quit()

    telegram_token = '*********************************'
    telegram_chat_id = '@girls_legs_beatiful'

    images = [os.path.join(save_folder, image_file) for image_file in os.listdir(save_folder)]
    times = [
        '08:00', '08:05', '08:10', '08:15', '08:20', '08:25', '08:30', '08:35', '08:40', '08:45', 
        '08:50', '08:55', '09:00', '09:05', '09:10', '09:15', '09:20', '09:25', '09:30', '09:35', 
        '09:40', '09:45', '09:50', '09:55', '10:00', '10:05', '10:10', '10:15', '10:20', '10:25', 
        '10:30', '10:35', '10:40', '10:45', '10:50', '10:55', '11:00', '11:05', '11:10', '11:15', 
        '11:20', '11:25', '11:30', '11:35', '11:40', '11:45', '11:50', '11:55', '12:00', '12:05', 
        '12:10', '12:15', '12:20', '12:25', '12:30', '12:35', '12:40', '12:45', '12:50', '12:55', 
        '13:00', '13:05', '13:10', '13:15', '13:20', '13:25', '13:30', '13:35', '13:40', '13:45', 
        '13:50', '13:55', '14:00', '14:05', '14:10', '14:15', '14:20', '14:25', '14:30', '14:35', 
        '14:40', '14:45', '14:50', '14:55', '15:00', '15:05', '15:10', '15:15', '15:20', '15:25', 
        '15:30', '15:35', '15:40', '15:45', '15:50', '15:55', '16:00', '16:05', '16:10', '16:15', 
        '16:20', '16:25', '16:30', '16:35', '16:40', '16:45', '16:50', '16:55', '17:00', '17:05', 
        '17:10', '17:15', '17:20', '17:25', '17:30', '17:35', '17:40', '17:45', '17:50', '17:55', 
        '18:00', '18:05', '18:10', '18:15', '18:20', '18:25', '18:30', '18:35', '18:40', '18:45', 
        '18:50', '18:55', '19:00', '19:05', '19:10', '19:15', '19:20', '19:25', '19:30', '19:35', 
        '19:40', '19:45', '19:50', '19:55', '20:00', '20:05', '20:10', '20:15', '20:20', '20:25', 
        '20:30', '20:35', '20:40', '20:45', '20:50', '20:55', '21:00', '21:05', '21:10', '21:15', 
        '21:20', '21:25', '21:30', '21:35', '21:40', '21:45', '21:50', '21:55', '22:00', '22:05', 
        '22:10', '22:15', '22:20', '22:25', '22:30', '22:35', '22:40', '22:45', '22:50', '22:55', 
        '23:00', '23:05', '23:10', '23:15', '23:20', '23:25', '23:30', '23:35', '23:40', '23:45', 
        '23:50', '23:55', '24:00'
    ]

    await publish_images_on_schedule(telegram_token, telegram_chat_id, images, times)

if __name__ == "__main__":
    asyncio.run(main())
