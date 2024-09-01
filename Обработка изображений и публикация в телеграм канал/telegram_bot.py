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
    path = r'C:\Users\lerdo\OneDrive\Рабочий стол\parametr_bots\parameters.txt'
    save_folder = r'C:\Users\lerdo\OneDrive\Рабочий стол\parametr_bots\downloaded_images'
    driver = parametr_files(path)
    parsing_site(driver, save_folder)
    driver.quit()

    telegram_token = '*********************************************'
    telegram_chat_id = '@girls_legs_beatiful'

    images = [os.path.join(save_folder, image_file) for image_file in os.listdir(save_folder)]
    times = ['11:00', '12:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', 
             '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30']

    await publish_images_on_schedule(telegram_token, telegram_chat_id, images, times)


if __name__ == "__main__":
    asyncio.run(main())
